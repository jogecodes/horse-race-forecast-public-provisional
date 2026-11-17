import { readFile, readdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
const root=fileURLToPath(new URL('../dist/',import.meta.url));
const html=await readFile(path.join(root,'index.html'),'utf8');
assert.match(html, /<html lang="en">/);
assert.doesNotMatch(html, /<!--MARKET_CALIBRATION-->|<!--ODDS_ROWS-->|<!--RESULT_ROWS-->|<!--INTERVAL_FIGURE-->/);
assert.deepEqual([...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)].map(m=>[m[1].trim(),m[2]]), [['src="forecast.js?v=2" defer','']], 'Only the local forecast script is allowed');
assert.doesNotMatch(html, /\son[a-z]+\s*=|javascript:/i, 'No inline event handlers');
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
assert.equal(new Set(ids).size,ids.length,'Duplicate HTML IDs');
for(const [,target] of html.matchAll(/href="#([^"]+)"/g)) assert.ok(ids.includes(target),`Missing anchor ${target}`);
for(const [,target] of html.matchAll(/(?:href|src)="([^"#]+)"/g)) {
 if(/^https?:/.test(target))continue;
 await readFile(path.join(root,target.split(/[?#]/)[0]));
}
const bibliography=html.match(/<ol class="source-list">([\s\S]*?)<\/ol>/)[1];
const bibliographyIds=[...bibliography.matchAll(/<li\b[^>]*id="(source-[^"]+)"/g)].map(m=>m[1]);
const citedIds=[];
for(const [,id,label] of html.matchAll(/<a\b[^>]*href="#(source-[^"]+)"[^>]*>\[(\d+)\]<\/a>/g)) {
 if(!citedIds.includes(id))citedIds.push(id);
 assert.equal(Number(label),citedIds.indexOf(id)+1,`Citation number for ${id}`);
}
assert.deepEqual(bibliographyIds,citedIds,'Bibliography must follow first citation order');
const files=await readdir(root,{recursive:true});
assert.deepEqual(files.filter(f=>!['data'].includes(f)).sort(), ['_headers','data/facts.json','data/provenance.json','data/market_calibration.json','data/market_scenarios.json','favicon.svg','index.html','styles.css','forecast.js'].sort());
const facts=JSON.parse(await readFile(path.join(root,'data/facts.json'),'utf8'));
assert.equal(facts.extraction.processed,368);
assert.equal(facts.extraction.model_calls,34);
assert.equal(facts.verified_closing_races,0);
assert.equal(facts.market.optional_agent.paired_races,17);
assert.doesNotMatch(JSON.stringify(facts),/source_quote|reference_rows|runner_id|source_text|raw_response/);
console.log('Passed: local assets, anchor integrity, English document, local forecast script, aggregate cohorts, explicit public file set.');
