// Number citations after generated sections are inserted, keeping stable source IDs.
export function numberReferences(html) {
 const bibliography=html.match(/<ol class="source-list">([\s\S]*?)<\/ol>/);
 if(!bibliography)throw new Error('Missing bibliography');
 const entries=new Map();
 for(const match of bibliography[1].matchAll(/<li\b[^>]*id="(source-[^"]+)"[^>]*>[\s\S]*?<\/li>/g)) {
  if(entries.has(match[1]))throw new Error(`Duplicate bibliography entry: ${match[1]}`);
  entries.set(match[1],match[0]);
 }
 const numbers=new Map();
 for(const match of html.matchAll(/<a\b[^>]*href="#(source-[^"]+)"[^>]*>/g)) {
  if(!entries.has(match[1]))throw new Error(`Missing bibliography entry: ${match[1]}`);
  if(!numbers.has(match[1]))numbers.set(match[1],numbers.size+1);
 }
 for(const id of entries.keys())if(!numbers.has(id))throw new Error(`Uncited bibliography entry: ${id}`);
 html=html.replace(/(<a\b[^>]*href="#(source-[^"]+)"[^>]*>)\[\d+\](<\/a>)/g,(_,open,id,close)=>`${open}[${numbers.get(id)}]${close}`);
 return html.replace(/<ol class="source-list">[\s\S]*?<\/ol>/,`<ol class="source-list">${[...numbers.keys()].map(id=>entries.get(id)).join('\n')}</ol>`);
}
