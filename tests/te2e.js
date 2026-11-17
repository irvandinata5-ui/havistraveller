const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};w.onerror=m=>console.log('ERR',m);}});
const w=dom.window,d=w.document;const errs=[];
function run(l,f){try{f();console.log('  ok  '+l);}catch(e){console.log('  ** BUG '+l+' => '+e.message);errs.push(l);}}
const txt=()=>d.getElementById('view').textContent;
setTimeout(()=>{
  // 1. go to katalog kalkulator, fill Jogja 1000 pax 3 malam
  w.go('katalog');w.katTab='kalkulator';w.renderKat();
  run('fill calc Jogja 1000pax 3malam',()=>{
    d.getElementById('q_pax').value='1000';d.getElementById('q_malam').value='3';d.getElementById('q_tgl').value='2026-12-20';
    // pick a Yogya hotel
    const h=d.getElementById('q_hotel');const opt=[...h.options].find(o=>/Front One|Malioboro|Yogya/i.test(o.text)); if(opt)h.value=opt.value;
    // check a Jogja dest
    const c=[...d.querySelectorAll('.qdest')][60]; if(c){c.checked=true;}
    w.calcQuote();
    const pp=d.getElementById('q_perpax').textContent; if(!/Rp [1-9]/.test(pp))throw new Error('no price '+pp);
    console.log('     harga/pax:',pp,'| bus:',w.eval('lastQuote.bus'),'| total:',w.eval('lastQuote.total').toLocaleString('id-ID'));
  });
  run('save penawaran requires klien',()=>{d.getElementById('q_klien').value='';w.saveQuote();if(w.penawaran().length!==0)throw new Error('saved without klien');});
  run('save penawaran valid',()=>{d.getElementById('q_klien').value='SMPN 4 Cikupa';d.getElementById('q_dest').value='Jogja';w.saveQuote();if(w.penawaran().length!==1)throw new Error('not saved');});
  run('penawaran lands in ACC pending',()=>{w.go('acc');if(!txt().includes('SMPN 4 Cikupa')||!txt().includes('Penawaran Baru'))throw new Error('not in ACC');});
  run('ACC approve the penawaran',()=>{const id=w.penawaran()[0].id;w.pnwDecide(id,'approved');if(w.penawaran()[0].status!=='approved')throw new Error('not approved');});
  run('appears in Jadwal Trip (BARU)',()=>{w.go('jadwal');const t=txt();if(!t.includes('SMPN 4 Cikupa')||!t.includes('BARU'))throw new Error('not in jadwal');});
  run('appears in Keuangan Pelunasan',()=>{w.go('keuangan');const clickTab=l=>[...d.querySelectorAll('#view .tabs .tab')].find(x=>x.textContent.trim()===l).onclick();clickTab('Pelunasan Klien');if(!txt().includes('SMPN 4 Cikupa'))throw new Error('not in pelunasan');});
  run('appears in Aging Piutang',()=>{const clickTab=l=>[...d.querySelectorAll('#view .tabs .tab')].find(x=>x.textContent.trim()===l).onclick();clickTab('Aging Piutang');if(!txt().includes('SMPN 4 Cikupa'))throw new Error('not in aging');});
  run('sisa piutang grew',()=>{const pt=w.eval('piutangTot()');console.log('     sisa piutang total:',pt.sisa.toLocaleString('id-ID'));if(pt.sisa<=48740000)throw new Error('sisa did not grow');});
  run('reject path works',()=>{const id=w.penawaran()[0].id;w.pnwDecide(id,'rejected');w.go('jadwal');if(txt().includes('SMPN 4 Cikupa'))throw new Error('rejected still in jadwal');});
  // full regression
  let bad=0;['dashboard','keuangan','katalog','acc','jadwal','karyawan','setting'].forEach(v=>{try{w.go(v);if(!d.getElementById('view').innerHTML.trim())bad++;}catch(e){console.log('THROW',v,e.message);bad++;}});
  console.log('  -- all 7 views:',bad?bad+' bad':'clean');
  console.log(errs.length?'\nBUGS: '+errs.join(', '):'\nEnd-to-end flow OK');
},300);
