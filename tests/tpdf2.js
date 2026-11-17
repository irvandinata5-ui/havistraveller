const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};let e=[];w.onerror=m=>e.push(m);w.__errs=e;}});
const w=dom.window,d=w.document;
let pass=0,fail=0;
const ok=(n,c,x)=>{if(c){pass++;console.log('  ✓',n);}else{fail++;console.log('  ✗',n,x===undefined?'':'→ '+x);}};

// capture the PDF instead of downloading: stub claude.use('downloads')
const captured=[];

setTimeout(()=>{
console.log('\n=== INVOICE & RUNDOWN PDF (poin 13) ===');
const E=s=>w.eval(s);

// load jspdf into the jsdom window (CDN script won't load offline)
const jspdfPath=require.resolve('jspdf/dist/jspdf.umd.min.js');
try{
  const code=fs.readFileSync(jspdfPath,'utf8');
  w.eval(code);
}catch(e){console.log('  (jspdf local load failed:',e.message,')');}
ok('pustaka jsPDF tersedia',!!w.jspdf,typeof w.jspdf);

// stub downloads capability to capture the blob text
w.eval(`window.claude={use:async(n)=>({save:async({filename,data})=>{window.__cap=window.__cap||[];window.__cap.push({filename,size:data.size});return true;}})};`);

// ---- INVOICE ----
const pid=E('allPiutang().filter(p=>p.tagih>0)[0].id');
const pnm=E('allPiutang().filter(p=>p.tagih>0)[0].inst');
console.log('  invoice utk:',pnm);
// record a payment first so riwayat ada isinya
E(`addClientPayment(${JSON.stringify(pid)},'DP 1',5000000,'2026-11-10')`);

// verify the PDF text by building the doc directly through the same code path
let invText='';
w.eval(`window.__pdfText=null;const _o=window.jspdf.jsPDF;window.jspdf.jsPDF=function(o){const inst=new _o(o);const _t=inst.text.bind(inst);window.__t=[];inst.text=function(s,x,y,op){window.__t.push(String(s));return _t(s,x,y,op);};return inst;};`);
E(`genInvoicePDF(${JSON.stringify(pid)})`);
setTimeout(()=>{
  invText=(w.__t||[]).join(' | ');
  ok('invoice: ada kop HAVIST TRAVELLER',invText.includes('HAVIST TRAVELLER'));
  ok('invoice: judul INVOICE',invText.includes('INVOICE'));
  ok('invoice: nama klien',invText.includes(pnm));
  ok('invoice: nomor invoice',/INV\/|\bINV/.test(invText)||invText.includes('Nomor'));
  ok('invoice: rincian tagihan',invText.includes('Rincian Tagihan'));
  ok('invoice: total tagihan',invText.includes('Total Tagihan'));
  ok('invoice: riwayat pembayaran',invText.includes('Riwayat Pembayaran'));
  ok('invoice: termin DP 1 tercatat',invText.includes('DP 1'));
  ok('invoice: jumlah peserta',invText.includes('Jumlah Peserta'));
  ok('invoice: blok sisa/lunas',/Sisa yang Harus Dibayar|LUNAS/.test(invText));
  ok('invoice: tanda tangan',invText.includes('Hormat kami,'));
  ok('invoice: file tersimpan',(w.__cap||[]).some(c=>c.filename.startsWith('Invoice-')),JSON.stringify(w.__cap));
  ok('invoice: ukuran PDF wajar',(w.__cap||[])[0]&&w.__cap[0].size>1000,(w.__cap||[])[0]&&w.__cap[0].size);

  // ---- RUNDOWN ----
  const tid=E('upcoming()[0].id');const tnm=E('upcoming()[0].inst');
  console.log('\n  rundown utk:',tnm);
  E(`prepAutoFill(${JSON.stringify(tid)})`);
  E(`const o=document.getElementById('prepOv');if(o)o.remove()`);
  const tls=E('crewList().filter(c=>c.peran==="Tour Leader")[0].id');
  const mds=E('crewList().filter(c=>c.peran==="Media")[0].id');
  E(`assignCrew(${JSON.stringify(tid)},'tl',${JSON.stringify(tls)});assignCrew(${JSON.stringify(tid)},'media',${JSON.stringify(mds)})`);
  E(`toggleChecklist(${JSON.stringify(tid)},0)`);
  w.__t=[];
  E(`genRundownPDF(${JSON.stringify(tid)})`);
  setTimeout(()=>{
    const r=(w.__t||[]).join(' | ');
    ok('rundown: judul RUNDOWN PERJALANAN',r.includes('RUNDOWN PERJALANAN'));
    ok('rundown: nama trip',r.includes(tnm));
    ok('rundown: informasi trip',r.includes('Informasi Trip'));
    ok('rundown: durasi',r.includes('Durasi'));
    ok('rundown: crew bertugas',r.includes('Crew Bertugas'));
    ok('rundown: TL terisi (bukan "belum")',r.includes('Tour Leader')&&!/Tour Leader[^|]*\|\s*belum ditugaskan/.test(r));
    ok('rundown: nama TL muncul',r.includes(E(`crewById(${JSON.stringify(tls)}).nama`)));
    ok('rundown: nama Media muncul',r.includes(E(`crewById(${JSON.stringify(mds)}).nama`)));
    ok('rundown: susunan acara',r.includes('Susunan Acara'));
    ok('rundown: ada Hari 1',r.includes('Hari 1'));
    ok('rundown: vendor & perlengkapan',r.includes('Vendor & Perlengkapan'));
    ok('rundown: armada dari persiapan',r.includes('Transport'));
    ok('rundown: checklist persiapan',r.includes('Checklist Persiapan'));
    ok('rundown: item checklist dicentang',r.includes('[v]'));
    ok('rundown: file tersimpan',(w.__cap||[]).some(c=>c.filename.startsWith('Rundown-')),JSON.stringify((w.__cap||[]).map(c=>c.filename)));

    // UI buttons wired
    E(`go('keuangan');setKeuTab('pelunasan')`);
    ok('UI: tombol Invoice di tabel pelunasan',d.getElementById('keuBody').innerHTML.includes('genInvoicePDF'));
    E(`go('jadwal')`);
    ok('UI: tombol Rundown di kartu jadwal',d.getElementById('view').innerHTML.includes('genRundownPDF'));
    E(`openTripDetail(${JSON.stringify(tid)})`);
    ok('UI: tombol Rundown di detail trip',d.getElementById('tripOv').innerHTML.includes('genRundownPDF'));
    E(`document.getElementById('tripOv').remove()`);
    E(`go('setting')`);
    ok('UI: field rekening di Setting',!!d.getElementById('s_rek'));
    d.getElementById('s_rek').value='BCA 1234567890 a/n Havist';w.saveInfo();
    ok('rekening tersimpan',E(`store('info',{}).rek`)==='BCA 1234567890 a/n Havist',E(`store('info',{}).rek`));

    console.log('\nwindow errors:',(w.__errs||[]).length?w.__errs.join(' | '):'none');
    console.log(`\n${fail===0?'✓ PDF TESTS CLEAN':'✗ '+fail+' GAGAL'} — ${pass} pass, ${fail} fail`);
    process.exit(fail===0?0:1);
  },400);
},400);
},700);
