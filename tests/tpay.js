const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};w.onerror=m=>console.log('ERR',m);}});
const w=dom.window,d=w.document;const errs=[];
function run(l,f){try{f();console.log('  ok  '+l);}catch(e){console.log('  ** BUG '+l+' => '+e.message);errs.push(l);}}
setTimeout(()=>{
  w.go('keuangan');
  const clickTab=l=>[...d.querySelectorAll('#view .tabs .tab')].find(x=>x.textContent.trim()===l).onclick();
  run('Pelunasan tab renders',()=>{clickTab('Pelunasan Klien');if(!d.getElementById('keuBody').innerHTML.includes('Status Pelunasan'))throw new Error('no content');});
  // pick an invoice with tagihan>0 and partial/zero paid
  const inv=w.eval('allPiutang().find(p=>p.tagih>0 && clientSisa(p)>0).id');
  console.log('     test invoice:',inv);
  run('openBayar modal',()=>{w.openBayar(inv);if(!d.getElementById('bayarOv'))throw new Error('no modal');if(!d.getElementById('b_amount'))throw new Error('no amount field');});
  const sisaBefore=w.eval(`clientSisa(allPiutang().find(p=>p.id==='${inv}'))`);
  run('record DP termin',()=>{d.getElementById('b_amount').value=Math.floor(sisaBefore/2);d.getElementById('b_termin').value='DP 1';w.submitBayar(inv);
    const sisaAfter=w.eval(`clientSisa(allPiutang().find(p=>p.id==='${inv}'))`);
    if(sisaAfter>=sisaBefore)throw new Error('sisa not reduced '+sisaBefore+'->'+sisaAfter);console.log('     sisa',sisaBefore.toLocaleString('id-ID'),'->',sisaAfter.toLocaleString('id-ID'));});
  run('arus kas masuk reflects payment',()=>{const masuk=w.eval('totalMasuk()');console.log('     total masuk now:',masuk.toLocaleString('id-ID'));if(!masuk)throw new Error('zero');});
  run('aging reflects reduced sisa',()=>{clickTab('Aging Piutang');/* just render ok */ if(!d.getElementById('keuBody').innerHTML.includes('per Umur'))throw new Error('aging broke');});
  run('lunasi sisa makes it lunas',()=>{w.openBayar(inv);const sisaNow=w.eval(`clientSisa(allPiutang().find(p=>p.id==='${inv}'))`);d.getElementById('b_amount').value=sisaNow;w.submitBayar(inv);
    const st=w.eval(`clientStatus(allPiutang().find(p=>p.id==='${inv}'))[0]`);if(st!=='lunas')throw new Error('status '+st);});
  run('arus kas tab renders',()=>{clickTab('Arus Kas');if(!d.getElementById('keuBody').innerHTML.includes('Saldo Kas'))throw new Error('no arus kas');
    console.log('     saldo:',w.eval('(totalMasuk()-totalKeluar())').toLocaleString('id-ID'));});
  // regression
  let bad=0;['dashboard','keuangan','katalog','acc','jadwal','karyawan','setting'].forEach(v=>{try{w.go(v);if(!d.getElementById('view').innerHTML.trim())bad++;}catch(e){bad++;console.log('THROW',v,e.message)}});
  console.log('  -- all 7 views:',bad?bad+' bad':'clean');
  console.log(errs.length?'\nBUGS: '+errs.join(', '):'\nModel pembayaran + pelunasan termin OK');
},300);
