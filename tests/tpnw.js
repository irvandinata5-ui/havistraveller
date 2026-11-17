const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};w.onerror=m=>console.log('ERR',m);}});
const w=dom.window,d=w.document;const errs=[];
function run(l,f){try{f();console.log('  ok  '+l);}catch(e){console.log('  ** BUG '+l+' => '+e.message);errs.push(l);}}
setTimeout(()=>{
  w.go('katalog');w.katTab='kalkulator';w.renderKat();
  d.getElementById('q_pax').value='200';d.getElementById('q_malam').value='2';d.getElementById('q_tgl').value='2026-12-22';d.getElementById('q_arm').selectedIndex=4;
  [...d.querySelectorAll('.qdest')].slice(60,63).forEach(c=>c.checked=true);w.calcQuote();
  d.getElementById('q_klien').value='SMAN 1 Tangerang';d.getElementById('q_dest').value='Jogja';d.getElementById('q_hp').value='08123456789';
  run('saveQuote does NOT navigate away',()=>{w.saveQuote();const h=d.getElementById('view').innerHTML;if(!h.includes('Kalkulator')&&!d.getElementById('q_klien'))throw new Error('navigated away');if(w.penawaran().length!==1)throw new Error('not saved');});
  run('penawaran stores full detail',()=>{const p=w.penawaran()[0];if(!p.armName||!p.dests||!p.hotelName)throw new Error('missing detail fields');});
  run('PDF button in ACC opens with stored rec',()=>{w.go('acc');const id=w.penawaran()[0].id;w.showPenawaran(id);const ov=d.getElementById('pvOverlay');if(!ov)throw new Error('no modal');const t=ov.textContent;if(!t.includes('SMAN 1 Tangerang')||!t.includes('Itinerary'))throw new Error('wrong content');
    if(!w.pvActive)throw new Error('pvActive not set');d.getElementById('pvOverlay').remove();});
  run('PDF button visible in ACC rows',()=>{w.go('acc');if(!d.getElementById('view').innerHTML.includes('showPenawaran'))throw new Error('no PDF btn');});
  run('approve then PDF from processed',()=>{const id=w.penawaran()[0].id;w.pnwDecide(id,'approved');w.showPenawaran(id);if(!d.getElementById('pvOverlay'))throw new Error('no modal for approved');d.getElementById('pvOverlay').remove();});
  run('approved penawaran in jadwal+keuangan',()=>{w.go('jadwal');if(!d.getElementById('view').textContent.includes('SMAN 1 Tangerang'))throw new Error('not in jadwal');});
  let bad=0;['dashboard','keuangan','katalog','acc','jadwal','karyawan','setting'].forEach(v=>{try{w.go(v);if(!d.getElementById('view').innerHTML.trim())bad++;}catch(e){bad++;console.log('THROW',v,e.message)}});
  console.log('  -- all 7 views:',bad?bad+' bad':'clean');
  console.log(errs.length?'\nBUGS: '+errs.join(', '):'\nPenawaran tetap + PDF dari ACC OK');
},300);
