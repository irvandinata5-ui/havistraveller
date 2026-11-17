const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};w.onerror=m=>console.log('ERR',m);}});
const w=dom.window,d=w.document;const errs=[];
function run(l,f){try{f();console.log('  ok  '+l);}catch(e){console.log('  ** BUG '+l+' => '+e.message);errs.push(l);}}
setTimeout(()=>{
  w.go('keuangan');const clickTab=l=>[...d.querySelectorAll('#view .tabs .tab')].find(x=>x.textContent.trim()===l).onclick();
  run('Jadwal Vendor renders',()=>{clickTab('Jadwal Vendor');if(!d.getElementById('keuBody').innerHTML.includes('Jadwal Pembayaran Vendor'))throw new Error('no content');});
  const no=w.eval('DATA.dpvendor.find(d=>(d.status||"").toUpperCase()!=="DONE").no');
  console.log('     test vendor:',no);
  const keluarBefore=w.eval('totalKeluar()');
  run('openBayarVendor modal',()=>{w.openBayarVendor(no);if(!d.getElementById('bv_amount'))throw new Error('no field');});
  run('partial vendor payment',()=>{const nom=w.eval(`DATA.dpvendor.find(d=>d.no==='${no}').nom`);d.getElementById('bv_amount').value=Math.floor(nom/3);w.submitBayarVendor(no);
    const st=w.eval(`vendorStatusArr(DATA.dpvendor.find(d=>d.no==='${no}'))[0]`);if(st!=='dp')throw new Error('expected dp got '+st);});
  run('keluar increased',()=>{const kl=w.eval('totalKeluar()');console.log('     keluar',keluarBefore.toLocaleString('id-ID'),'->',kl.toLocaleString('id-ID'));if(kl<=keluarBefore)throw new Error('not increased');});
  run('lunasi vendor',()=>{w.openBayarVendor(no);const sisa=w.eval(`vendorSisa(DATA.dpvendor.find(d=>d.no==='${no}'))`);d.getElementById('bv_amount').value=sisa;w.submitBayarVendor(no);
    const st=w.eval(`vendorStatusArr(DATA.dpvendor.find(d=>d.no==='${no}'))[0]`);if(st!=='lunas')throw new Error('expected lunas got '+st);});
  run('DONE vendor shows paid, no form',()=>{const doneNo=w.eval('DATA.dpvendor.find(d=>(d.status||"").toUpperCase()==="DONE").no');w.openBayarVendor(doneNo);
    if(d.getElementById('bv_amount'))throw new Error('form shown for DONE');if(!d.getElementById('bayarOv').textContent.includes('sudah lunas'))throw new Error('no lunas note');d.getElementById('bayarOv').remove();});
  let bad=0;['dashboard','keuangan','katalog','acc','jadwal','karyawan','setting'].forEach(v=>{try{w.go(v);if(!d.getElementById('view').innerHTML.trim())bad++;}catch(e){bad++;console.log('THROW',v,e.message)}});
  console.log('  -- all 7 views:',bad?bad+' bad':'clean');
  console.log(errs.length?'\nBUGS: '+errs.join(', '):'\nJadwal Vendor bertahap OK');
},300);
