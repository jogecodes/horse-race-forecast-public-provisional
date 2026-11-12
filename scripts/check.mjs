import { readFile, readdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
const root=fileURLToPath(new URL('../dist/',import.meta.url));
const html=await readFile(path.join(root,'index.html'),'utf8');
assert.match(html, /<html lang="en">/);
assert.doesNotMatch(html, /<script|<!--RESULT_ROWS-->|<!--INTERVAL_FIGURE-->/);
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
assert.equal(new Set(ids).size,ids.length,'Duplicate HTML IDs');
for(const [,target] of html.matchAll(/href="#([^"]+)"/g)) assert.ok(ids.includes(target),`Missing anchor ${target}`);
for(const [,target] of html.matchAll(/(?:href|src)="([^"#]+)"/g)) {
 if(/^https?:/.test(target))continue;
 await readFile(path.join(root,target));
}
const files=await readdir(root,{recursive:true});
assert.deepEqual(files.filter(f=>!['data'].includes(f)).sort(), ['_headers','data/facts.json','data/provenance.json','favicon.svg','index.html','styles.css'].sort());
const facts=JSON.parse(await readFile(path.join(root,'data/facts.json'),'utf8'));
assert.equal(facts.extraction.processed,368);
assert.equal(facts.extraction.model_calls,34);
assert.equal(facts.verified_closing_races,0);
assert.equal(facts.market.optional_agent.paired_races,17);
assert.doesNotMatch(JSON.stringify(facts),/source_quote|reference_rows|runner_id|source_text|raw_response/);
console.log('Passed: local assets, anchor integrity, English document, no scripts, aggregate cohorts, explicit public file set.');
