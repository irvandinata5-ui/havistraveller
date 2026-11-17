const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};w.onerror=m=>console.log('ERR',m);}});
const w=dom.window,d=w.document;const errs=[];
function run(l,f){try{f();console.log('  ok  '+l);}catch(e){console.log('  ** BUG '+l+' => '+e.message);errs.push(l);}}
setTimeout(()=>{
  w.go('keuangan');
  const clickTab=label=>[...d.querySelectorAll('#view .tabs .tab')].find(t=>t.textContent.trim()===label).onclick();
  run('tab Profitabilitas',()=>{clickTab('Profitabilitas');const h=d.getElementById('keuBody').innerHTML;if(!h.includes('Laba per Daerah')||!h.includes('Laba per Jenis'))throw new Error('no content');
    const act=[...d.querySelectorAll('#view .tabs .tab')].find(t=>t.classList.contains('active'));if(act.textContent.trim()!=='Profitabilitas')throw new Error('active wrong');});
  run('all 6 keu tabs switch',()=>{['Ringkasan','Arus Kas','Aging Piutang','Pelunasan Klien','Jadwal Vendor','Profitabilitas'].forEach(t=>{clickTab(t);if(!d.getElementById('keuBody').innerHTML.trim())throw new Error('empty '+t);});});
  // numbers
  const r=w.eval(`(function(){const t=DATA.trips.filter(x=>x.id);const tot=t.reduce((a,x)=>a+x.laba,0);const wl=t.filter(x=>x.laba!==0);const rugi=t.filter(x=>/Rugi|Selisih/i.test(x.status)||x.laba<0);const jen={};t.forEach(x=>{jen[x.jenis||'?']=(jen[x.jenis||'?']||0)+x.laba});return{tot,avg:Math.round(tot/wl.length),rugi:rugi.length,jen}})()`);
  console.log('  -- total laba:',r.tot.toLocaleString('id-ID'),'| avg/trip:',r.avg.toLocaleString('id-ID'),'| rugi:',r.rugi);
  console.log('  -- per jenis:',JSON.stringify(Object.fromEntries(Object.entries(r.jen).map(([k,v])=>[k,v.toLocaleString('id-ID')]))));
  // full regression
  let bad=0;['dashboard','keuangan','katalog','acc','jadwal','karyawan','setting'].forEach(v=>{try{w.go(v);if(!d.getElementById('view').innerHTML.trim())bad++;}catch(e){console.log('THROW',v);bad++;}});
  console.log('  -- all 7 views:',bad?bad+' bad':'clean');
  console.log(errs.length?'\nBUGS: '+errs.join(', '):'\nProfitabilitas OK');
},300);
