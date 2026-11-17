"""Outcome-selected case studies and exploratory, later-period subgroup checks.

Case studies are surprises, not evidence of ex-ante model-market disagreement.
Subgroups use field/distance/race type known from the race description. H1
ranks candidates; H2 is a later descriptive confirmation, not untouched new data
(the pooled 2024 calibration has already been inspected). No model is fitted.
"""
import argparse
import bisect
import collections
from datetime import datetime, timezone
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import random
import zipfile
from analyze_market_calibration import EXPECTED_SHA, URL, seconds, quantile

ROOT=Path(__file__).resolve().parents[1]
SEED=20261114
DRAWS=4000
MIN_DISCOVERY_RACES=250


def retained_markets(path):
    blob=path.read_bytes()
    if hashlib.sha256(blob).hexdigest()!=EXPECTED_SHA:raise ValueError('Changed source archive')
    markets=collections.defaultdict(list)
    with zipfile.ZipFile(path) as z:
        for name in sorted(z.namelist()):
            if name.endswith('.csv'):
                for row in csv.DictReader(io.TextIOWrapper(z.open(name),encoding='utf-8-sig')):
                    markets[row['WIN_MARKET_ID']].append(row)
    for mid,rs in sorted(markets.items()):
        if len({r['SELECTION_ID'] for r in rs})!=len(rs):continue
        if any(r['WIN_RESULT'] not in ['WINNER','LOSER'] for r in rs):continue
        if sum(r['WIN_RESULT']=='WINNER' for r in rs)!=1 or len(rs)<2:continue
        try:
            if len({r['ACTUAL_OFF_TIME'] for r in rs})!=1 or len({r['SCHEDULED_RACE_TIME'] for r in rs})!=1:continue
            lag=seconds(rs[0]['ACTUAL_OFF_TIME'])-seconds(rs[0]['SCHEDULED_RACE_TIME'])
            if lag<=0:continue
            odds=[float(r['BEST_AVAIL_BACK_AT_SCHEDULED_OFF']) for r in rs]
            if any(not math.isfinite(o) or o<=1 for o in odds):continue
        except (ValueError,TypeError):continue
        raw=[1/o for o in odds];total=sum(raw);q=[p/total for p in raw]
        y=[int(r['WIN_RESULT']=='WINNER') for r in rs]
        yield mid,rs,odds,raw,q,y,total


def interval(rows,seed=SEED):
    clusters=collections.defaultdict(lambda:[0,0.])
    for r in rows:
        a=clusters[r['meeting']];a[0]+=1;a[1]+=r['y']-r['p']
    items=list(clusters.values());rng=random.Random(seed);values=[]
    for _ in range(DRAWS):
        n=0;s=0.
        for _ in items:
            a=items[rng.randrange(len(items))];n+=a[0];s+=a[1]
        values.append(s/n)
    return [quantile(values,.025),quantile(values,.975)]


def summarize(rows):
    n=len(rows)
    return dict(races=n,wins=sum(r['y'] for r in rows),mean_probability=sum(r['p'] for r in rows)/n,
        observed_win_rate=sum(r['y'] for r in rows)/n,
        observed_minus_predicted=sum(r['y']-r['p'] for r in rows)/n,
        meeting_clusters=len({r['meeting'] for r in rows}))


def analyze(path):
    cases=[];groups=collections.defaultdict(list);scores=[];n=0;counts=collections.Counter()
    definitions={
        'field_small':'Fields of 2–7 runners', 'field_medium':'Fields of 8–11 runners','field_large':'Fields of 12+ runners',
        'distance_sprint':'Distances up to 1,200 m','distance_mile':'Distances 1,201–1,600 m',
        'distance_middle':'Distances 1,601–2,200 m','distance_staying':'Distances above 2,200 m',
        'type_maiden':'Maiden races','type_handicap':'Explicit handicap race-type codes','type_other':'Other race-type codes',
        'favorite_below_20':'Favorite assigned below 20%','favorite_20_40':'Favorite assigned 20–40%',
        'favorite_40_60':'Favorite assigned 40–60%','favorite_60_plus':'Favorite assigned at least 60%'}
    for mid,rs,odds,raw,q,y,total in retained_markets(path):
        n+=1
        winner=y.index(1);fav=max(range(len(q)),key=lambda i:q[i]);r=rs[0]
        score=sum((p-t)**2 for p,t in zip(q,y));scores.append(score)
        if .95<=total<=1.10:
            counts['case_quality_eligible']+=1
            cases.append(dict(market_id=mid,date=r['LOCAL_MEETING_DATE'],track=r['TRACK'],state=r['STATE_CODE'],race_number=r['RACE_NO'],
                race_name=r['WIN_MARKET_NAME'],distance_m=int(float(r['DISTANCE'])),field_size=len(rs),probability_total=total,
                favorite=dict(name=rs[fav]['SELECTION_NAME'],odds=odds[fav],raw_probability=raw[fav],probability=q[fav],won=bool(y[fav])),
                winner=dict(name=rs[winner]['SELECTION_NAME'],odds=odds[winner],raw_probability=raw[winner],probability=q[winner]),
                market_race_brier=score,market_expected_brier=1-sum(p*p for p in q)))
        if q.count(q[fav])>1:
            counts['tied_favorite_excluded_from_groups']+=1;continue
        p=q[fav];dist=float(r['DISTANCE']);typ=r['RACE_TYPE'].lower()
        selected=[
            'field_small' if len(rs)<=7 else 'field_medium' if len(rs)<=11 else 'field_large',
            'distance_sprint' if dist<=1200 else 'distance_mile' if dist<=1600 else 'distance_middle' if dist<=2200 else 'distance_staying',
            'type_maiden' if 'mdn' in typ or 'maiden' in typ else 'type_handicap' if 'hcp' in typ or 'hcap' in typ or 'handicap' in typ else 'type_other',
            'favorite_below_20' if p<.2 else 'favorite_20_40' if p<.4 else 'favorite_40_60' if p<.6 else 'favorite_60_plus']
        record=dict(date=r['LOCAL_MEETING_DATE'],meeting=(r['LOCAL_MEETING_DATE'],r['TRACK'],r['STATE_CODE']),p=p,y=y[fav])
        for key in selected:groups[key].append(record)
    scores.sort();cases.sort(key=lambda r:(-r['market_race_brier'],r['market_id']))
    for case in cases[:3]:case['brier_percentile']=bisect.bisect_right(scores,case['market_race_brier'])/n
    candidates=[]
    for key,rows in groups.items():
        first=[r for r in rows if r['date']<'2024-07-01']
        later=[r for r in rows if r['date']>='2024-07-01']
        if len(first)<MIN_DISCOVERY_RACES or not later:continue
        a=summarize(first);b=summarize(later)
        candidates.append(dict(key=key,label=definitions[key],first_half=a,second_half=b,_later=later))
    candidates.sort(key=lambda r:(-abs(r['first_half']['observed_minus_predicted']),r['key']))
    selected=candidates[:3]
    for candidate in selected:
        b=candidate['second_half'];a=candidate['first_half']
        b['gap_interval_95']=interval(candidate.pop('_later'))
        candidate['same_direction']=a['observed_minus_predicted']*b['observed_minus_predicted']>0
    for candidate in candidates[3:]:candidate.pop('_later')
    return dict(study='anz-2024-market-scenarios-v1',computed_at=datetime.now(timezone.utc).isoformat(),code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),source=dict(url=URL,sha256=EXPECTED_SHA),
        cohort=dict(races=n,case_quality_eligible=counts['case_quality_eligible'],tied_favorite_exclusions=counts['tied_favorite_excluded_from_groups']),
        case_studies=dict(selection='Three highest realized normalized Brier losses among recorded markets with raw inverse-price total in [0.95,1.10]; outcome-selected diagnostics, not opportunities',races=cases[:3]),
        subgroup_check=dict(definitions=definitions,selection='Largest absolute favorite win-frequency minus normalized probability gaps in January–June, minimum 250 races per candidate; report July–December without retuning',candidate_groups=len(candidates),selected=selected,all_first_half_rankings=[dict(key=r['key'],label=r['label'],first_half=r['first_half'],second_half=r['second_half']) for r in candidates]),
        uncertainty=dict(draws=DRAWS,seed=SEED,method='Whole-meeting percentile bootstrap of later-period mean favorite outcome-minus-probability gap'),
        caveats=['No independent model probabilities for this ANZ cohort: model-market disagreement is not measured.',
            'High realized error identifies an outcome surprise; a well-calibrated forecast can have rare large errors.',
            'Fourteen overlapping pre-race subgroup definitions explored; discovery gaps are selection-biased. Later intervals are pointwise and not multiple-testing adjusted.',
            'Later half is a chronological descriptive check, not fresh blind evidence: pooled 2024 outcomes were already inspected in the calibration study.',
            'The same source, timing, settled-field, liquidity and execution limitations as the parent study apply.',
            'Race examples use an additional quote-quality screen of 95–110% raw total, solely to avoid highlighting extreme book totals; the published calibration cohort is unchanged.',
            'No demonstrated predictive edge, fitted recalibration or profitability test.'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--out',type=Path,default=ROOT/'data/market_scenarios.json');a=p.parse_args()
    r=analyze(a.archive);a.out.write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(cohort=r['cohort'],cases=r['case_studies']['races'],subgroups=r['subgroup_check']['selected']),indent=2))
