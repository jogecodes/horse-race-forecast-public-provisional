"""Aggregate-only market calibration study from Betfair's public 2024 ANZ archive.

No fitting, private research inputs, accounts, or paid data. Network is opt-in.
"""
import argparse
import collections
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import math
from pathlib import Path
import random
import zipfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://betfair-datascientists.github.io/data/assets/ANZ_Thoroughbreds_2024.zip'
LISTING = 'https://betfair-datascientists.github.io/data/dataListing/'
EXPECTED_SHA = 'effe8d4183ffe6dfd410467561f788d199fc6164dd874610a93cb95e93765fef'
BAND = (.375, .425)
SEED = 20261113
DRAWS = 4000


def seconds(clock):
    h, m, s = clock.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def quantile(rows, p):
    rows = sorted(rows)
    pos = (len(rows) - 1) * p
    a = int(pos)
    b = min(a + 1, len(rows) - 1)
    return rows[a] + (rows[b] - rows[a]) * (pos - a)


def analyze(archive):
    blob = archive.read_bytes()
    sha = hashlib.sha256(blob).hexdigest()
    if sha != EXPECTED_SHA:
        raise ValueError('Source archive differs from frozen input; inspect before a new study')
    markets = collections.defaultdict(list)
    with zipfile.ZipFile(archive) as z:
        members = sorted(n for n in z.namelist() if n.endswith('.csv'))
        for name in members:
            for row in csv.DictReader(io.TextIOWrapper(z.open(name), encoding='utf-8-sig')):
                markets[row['WIN_MARKET_ID']].append(row)
    exclusions = collections.Counter()
    clusters = collections.defaultdict(lambda: [0.] * 11)
    bins = {name: [dict(lower=k/10, upper=(k+1)/10, runners=0, wins=0, predicted_sum=0.) for k in range(10)] for name in ['raw', 'normalized']}
    scores = collections.defaultdict(float)
    totals = []
    dates = []
    count = runners = 0
    for market_id, rows in sorted(markets.items()):
        if len({r['SELECTION_ID'] for r in rows}) != len(rows):
            exclusions['duplicate_runner_identity'] += 1
            continue
        if any(r['WIN_RESULT'] not in ['WINNER', 'LOSER'] for r in rows):
            exclusions['non_binary_outcome_status'] += 1
            continue
        if sum(r['WIN_RESULT'] == 'WINNER' for r in rows) != 1:
            exclusions['not_exactly_one_winner_including_dead_heats'] += 1
            continue
        if len(rows) < 2:
            exclusions['single_runner'] += 1
            continue
        try:
            if len({r['ACTUAL_OFF_TIME'] for r in rows}) != 1 or len({r['SCHEDULED_RACE_TIME'] for r in rows}) != 1:
                raise ValueError('Inconsistent timing')
            lag = seconds(rows[0]['ACTUAL_OFF_TIME']) - seconds(rows[0]['SCHEDULED_RACE_TIME'])
        except (ValueError, TypeError):
            exclusions['unknown_or_inconsistent_timing'] += 1
            continue
        if lag <= 0:
            exclusions['scheduled_clock_not_strictly_before_actual_clock'] += 1
            continue
        try:
            odds = [float(r['BEST_AVAIL_BACK_AT_SCHEDULED_OFF']) for r in rows]
            if any(not math.isfinite(o) or o <= 1 for o in odds):
                raise ValueError('Invalid quote')
        except (ValueError, TypeError):
            exclusions['missing_or_invalid_back_price'] += 1
            continue
        raw = [1 / o for o in odds]
        total = sum(raw)
        normalized = [p / total for p in raw]
        target = [int(r['WIN_RESULT'] == 'WINNER') for r in rows]
        key = (rows[0]['LOCAL_MEETING_DATE'], rows[0]['TRACK'], rows[0]['STATE_CODE'])
        c = clusters[key]
        c[0] += 1
        raw_score = sum((p-y)**2 for p,y in zip(raw,target))
        norm_score = sum((p-y)**2 for p,y in zip(normalized,target))
        c[1] += norm_score - raw_score
        scores['raw_race_sum'] += raw_score
        scores['normalized_race_sum'] += norm_score
        c[10] += len(rows)
        for name, probs, offset in [('raw',raw,2), ('normalized',normalized,6)]:
            for p,y in zip(probs,target):
                b = bins[name][min(9,int(p * 10))]
                b['runners'] += 1
                b['wins'] += y
                b['predicted_sum'] += p
                if BAND[0] <= p < BAND[1]:
                    c[offset] += 1
                    c[offset+1] += y
                    c[offset+2] += p
                    c[offset+3] += y-p
        count += 1
        runners += len(rows)
        totals.append(total)
        dates.append(rows[0]['LOCAL_MEETING_DATE'])
    for group in bins.values():
        for b in group:
            n = b['runners']
            b['mean_probability'] = b.pop('predicted_sum') / n if n else None
            b['observed_win_rate'] = b['wins'] / n if n else None
    cluster_rows = list(clusters.values())
    band_report = {}
    for name,offset in [('raw',2),('normalized',6)]:
        n,w,p,gap = [sum(c[k] for c in cluster_rows) for k in range(offset,offset+4)]
        band_report[name] = dict(lower=BAND[0], upper=BAND[1], runners=int(n), wins=int(w), losses=int(n-w),
            mean_probability=p/n, observed_win_rate=w/n, observed_minus_predicted=gap/n)
    rng = random.Random(SEED)
    boot = {k: [] for k in ['paired_score_difference','raw_band_win_rate','normalized_band_win_rate','raw_band_gap','normalized_band_gap']}
    for _ in range(DRAWS):
        acc = [0.] * 11
        for _ in cluster_rows:
            c = cluster_rows[rng.randrange(len(cluster_rows))]
            for k in [0,1,2,3,5,6,7,9]:
                acc[k] += c[k]
        boot['paired_score_difference'].append(acc[1]/acc[0])
        for name,offset in [('raw',2),('normalized',6)]:
            if acc[offset]:
                boot[name+'_band_win_rate'].append(acc[offset+1]/acc[offset])
                boot[name+'_band_gap'].append(acc[offset+3]/acc[offset])
    intervals = {k: [quantile(v,.025),quantile(v,.975)] for k,v in boot.items()}
    for name in ['raw','normalized']:
        band_report[name]['win_rate_interval_95'] = intervals[name+'_band_win_rate']
        band_report[name]['observed_minus_predicted_interval_95'] = intervals[name+'_band_gap']
    raw_score = scores['raw_race_sum']/count
    norm_score = scores['normalized_race_sum']/count
    return dict(
        study='anz-2024-scheduled-off-back-prices-v1', computed_at=datetime.now(timezone.utc).isoformat(),
        source=dict(listing_url=LISTING, archive_url=URL, archive_sha256=sha, archive_bytes=len(blob),csv_files=len(members),
            scope='Australia and New Zealand thoroughbred racing, calendar 2024',price_column='BEST_AVAIL_BACK_AT_SCHEDULED_OFF',
            outcome_column='WIN_RESULT',timing='Publisher-reported scheduled-off snapshot, kept only when scheduled clock precedes reported actual-off clock on the same local date'),
        coverage=dict(source_markets=len(markets),source_runner_rows=sum(map(len,markets.values())),races=count,runners=runners,
            meeting_clusters=len(clusters),first_date=min(dates),last_date=max(dates),excluded_markets=dict(exclusions)),
        probability_total=dict(mean=sum(totals)/len(totals),median=quantile(totals,.5),minimum=min(totals),maximum=max(totals)),
        metrics=dict(raw_mean_race_sum_squared_error=raw_score,normalized_mean_race_brier=norm_score,
            normalized_minus_raw=norm_score-raw_score,paired_difference_interval_95=intervals['paired_score_difference'],
            raw_mean_runner_binary_brier=scores['raw_race_sum']/runners,
            normalized_mean_runner_binary_brier=scores['normalized_race_sum']/runners),
        near_40_percent=band_report,reliability=bins,
        uncertainty=dict(method='Whole-meeting percentile bootstrap; same draws for raw/normalized; race-weighted score means; runner-weighted frequency bins',draws=DRAWS,seed=SEED),
        caveats=[
            'Independent market-only study; not the Spanish 2026 model cohort and not a model-versus-market comparison.',
            'Exchange back prices, not bookmaker fixed odds or BSP; exchange commission, liquidity and executable size not evaluated.',
            'Provider historical compilation; timing and complete-field availability not independently certified. Same-day time ordering excludes possible midnight crossovers conservatively.',
            'The recorded settled runner set is used; later withdrawals and full contemporaneous field completeness are not independently reconstructed.',
            'Raw inverse prices are evaluated as binary marginal predictions and need not be a coherent race distribution. Race sum of binary Brier losses is compared with the same sum for normalized probabilities.',
            'Ten fixed 10-percentage-point bins; the 40% band is [37.5%,42.5%). Raw and normalized band membership differs.',
            'Intervals resample meetings, not independent horses. This is descriptive analysis without fitted recalibration or a held-out profitability test.',
            'Source accuracy and completeness are not warranted by the provider. No demonstrated betting edge follows from a calibration difference.'
        ])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--archive',type=Path,required=True)
    parser.add_argument('--out',type=Path,default=ROOT/'data/market_calibration.json')
    parser.add_argument('--download',action='store_true')
    args=parser.parse_args()
    if not args.archive.exists():
        if not args.download:
            raise FileNotFoundError('Supply the frozen archive, or explicitly use --download')
        args.archive.parent.mkdir(parents=True,exist_ok=True)
        with urlopen(URL,timeout=60) as response:
            blob=response.read(100_000_001)
        if len(blob)>100_000_000:
            raise ValueError('Download exceeds 100 MB budget')
        args.archive.write_bytes(blob)
    report=analyze(args.archive)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:report[k] for k in ['coverage','metrics','near_40_percent']},indent=2))

if __name__=='__main__':
    main()
