"""Explicit local refresh. Export selected aggregates only, never source article text."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT.with_name('horse-race-forecast-private')
SOURCES = {
 'history': 'docs/HISTORICAL_BACKFILL.md',
 'declarations': 'docs/RECOVERED_BENCHMARK_H1_2026.md',
 'engine': 'docs/FORECASTING_ENGINE.md',
 'research': 'docs/WEB_SOCIAL_RESEARCH.md',
 'checkpoint': 'docs/DEVELOPMENT_CHECKPOINT_20261105.md',
 'grounding': 'docs/EVENT_GROUNDED_REVIEW.md',
 'baseline': 'docs/STATISTICAL_BASELINES_20261111.md',
 'correction': 'docs/RESEARCH_RELEASE_20261112.md',
 'articles': 'docs/ARTICLE_COMPONENT_20261112.md',
 'article-summary': 'runs/article_component_evaluation_20261112/summary.json',
 'correction-summary': 'runs/research_release_20261112/summary.json',
 'fixture': 'tests/test_engine.py',
 'protocol': 'benchmarks/h1_2026_v2/protocol.json',
}
summary = json.loads((PRIVATE / SOURCES['article-summary']).read_text())
correction = json.loads((PRIVATE / SOURCES['correction-summary']).read_text())
extraction = summary['extraction_summary']
facts = {
 'snapshot': '2026-11-12',
 'scope': summary['scope'],
 'metrics': summary['metrics'],
 'article_minus_form': summary['agent_minus_reference']['deterministic_form'],
 'article_minus_baseline': summary['agent_minus_reference']['baseline'],
 'extraction': {k: extraction[k] for k in ['processed','model_calls','statuses','assessments','reference_scored','reference_accuracy']},
 'runners_with_article_signal': summary['runners_with_nonzero_article_features'],
 'corrected_zero_signal_max_difference': correction['agent_deterministic_max_probability_difference'],
 'market': {k: {key: v[key] for key in ['paired_races','metrics']} for k,v in summary['market_proxy'].items()},
 'verified_closing_races': summary['verified_closing_races'],
 'reliability': {k: {'ece': v['ece'], 'runners': v['runners']} for k,v in summary['reliability'].items()},
 'caveats': summary['caveats'],
}
provenance = {
 'snapshot': '2026-11-12',
 'policy': 'Curated aggregates and research explanations only. No raw sources, runner-level records, traces, labels, databases or credentials.',
 'sources': [{'id': k, 'path': v, 'sha256': hashlib.sha256((PRIVATE / v).read_bytes()).hexdigest()} for k,v in SOURCES.items()],
}
for name, data in [('facts.json',facts),('provenance.json',provenance)]:
 (ROOT / 'data' / name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print('Exported allowlisted aggregates and 13 source hashes; no raw source text.')
