const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};w.confirm=()=>true;let e=[];w.onerror=m=>e.push(m);w.__errs=e;}});
const w=dom.window,d=w.document;
let pass=0,fail=0;
const ok=(n,c,x)=>{if(c){pass++;console.log('  ✓',n);}else{fail++;console.log('  ✗',n,x===undefined?'':'→ '+x);}};
const J=o=>JSON.stringify(o);

setTimeout(()=>{
console.log('\n=== LAPORAN PERIODIK & ARSIP (poin 15+17) ===');
const E=s=>w.eval(s);

// --- nav & view ---
ok('menu Laporan ada di nav',!!d.querySelector('#nav a[data-view="laporan"]'));
E(`go('laporan')`);
ok('view laporan render',!!d.getElementById('lapBody'));
ok('ada tab Rekap & Arsip',d.getElementById('view').innerHTML.includes('Rekap Periodik')&&d.getElementById('view').innerHTML.includes('Arsip Trip'));

// --- periode ---
ok('periodeMulai 1 bulan = awal bulan ini',E(`periodeMulai('1').getMonth()`)===E(`today.getMonth()`));
ok('periodeMulai 3 bulan mundur 2 bulan',E(`(today.getMonth()-periodeMulai('3').getMonth()+12)%12`)===2,E(`(today.getMonth()-periodeMulai('3').getMonth()+12)%12`));
ok('periode "all" sangat awal',E(`periodeMulai('all').getFullYear()`)<2010);

const r1=JSON.parse(E(`JSON.stringify((()=>{const r=rekapPeriode('1');return{n:r.n,pax:r.pax,laba:r.laba,gaji:r.gaji,bersih:r.bersih};})())`));
const r3=JSON.parse(E(`JSON.stringify((()=>{const r=rekapPeriode('3');return{n:r.n,pax:r.pax,laba:r.laba};})())`));
const rall=JSON.parse(E(`JSON.stringify((()=>{const r=rekapPeriode('all');return{n:r.n,pax:r.pax,laba:r.laba};})())`));
console.log(`  1bln: ${r1.n} trip | 3bln: ${r3.n} trip | all: ${rall.n} trip`);
ok('periode lebih panjang ⊇ lebih pendek',r3.n>=r1.n&&rall.n>=r3.n,`${r1.n} ≤ ${r3.n} ≤ ${rall.n}`);
ok('rekap menghitung pax',r3.pax>0,r3.pax);
ok('rekap menghitung laba',r3.laba>0,'Rp '+r3.laba.toLocaleString('id-ID'));
ok('laba bersih = laba − gaji',r1.bersih===r1.laba-r1.gaji,`${r1.bersih} = ${r1.laba} - ${r1.gaji}`);

// gaji crew ikut terhitung setelah assign
const tid=E(`rekapPeriode('1').trips.length?rekapPeriode('1').trips[0].id:(tripsPeriode('3')[0]||{}).id`);
if(tid){
  const tl=E(`crewList().filter(c=>c.peran==='Tour Leader')[0].id`);
  const g0=E(`rekapPeriode('3').gaji`);
  E(`assignCrew(${J(tid)},'tl',${J(tl)})`);
  const g1=E(`rekapPeriode('3').gaji`);
  ok('gaji crew masuk rekap setelah assign',g1>g0,`${g0} → ${g1}`);
  ok('laba bersih ikut turun',E(`rekapPeriode('3').bersih`)===E(`rekapPeriode('3').laba`)-g1);
}

// --- tren bulanan ---
const tren=JSON.parse(E(`JSON.stringify(trenBulanan(6))`));
ok('tren menghasilkan 6 bulan',tren.length===6,tren.length);
ok('tren berurutan lama→baru',tren[5].k>tren[0].k,`${tren[0].k} → ${tren[5].k}`);
ok('bulan terakhir = bulan ini',tren[5].k===E(`bulanKunci(today)`),tren[5].k);
ok('tren punya data trip',tren.some(x=>x.trip>0),tren.map(x=>x.lbl+':'+x.trip).join(' '));
const sumTren=tren.reduce((s,x)=>s+x.trip,0);
ok('total tren 6bln ≈ rekap 6bln',sumTren===E(`rekapPeriode('6').n`),`${sumTren} vs ${E(`rekapPeriode('6').n`)}`);

// --- UI rekap ---
E(`setLapTab('rekap')`);
const rek=d.getElementById('lapBody').innerHTML;
ok('kartu Total Trip tampil',rek.includes('Total Trip'));
ok('kartu Laba Bersih tampil',rek.includes('Laba Bersih'));
ok('grafik tren tampil',rek.includes('Tren Laba 6 Bulan'));
ok('tabel perbandingan bulan tampil',rek.includes('Perbandingan Bulan ke Bulan'));
ok('ada penanda naik/turun',/▲|▼/.test(rek));
ok('dropdown periode ada',!!d.getElementById('lapPeriode'));
ok('tombol unduh laporan ada',rek.includes('genLaporanPDF'));

// ganti periode -> angka berubah
E(`setPeriode('1')`);
const a1=d.getElementById('lapBody').innerHTML;
E(`setPeriode('all')`);
const a2=d.getElementById('lapBody').innerHTML;
ok('ganti periode mengubah tampilan',a1!==a2);
ok('periode tersimpan di state',E(`lapPeriode`)==='all');
ok('label periode ikut berubah',a2.includes('Semua'));
E(`setPeriode('3')`);

// --- ARSIP ---
E(`setLapTab('arsip')`);
ok('tab arsip aktif',E(`lapTab`)==='arsip');
const ars=d.getElementById('lapBody').innerHTML;
ok('kartu Trip Selesai tampil',ars.includes('Trip Selesai'));
ok('kolom Tour Leader ada',ars.includes('Tour Leader'));
ok('ada kotak pencarian',!!d.getElementById('arsipSearch'));
ok('tombol rundown per baris',ars.includes('genRundownPDF'));

const nArs=E(`arsipTrips().length`);
console.log('  trip di arsip:',nArs);
ok('arsip hanya berisi trip selesai',E(`arsipTrips().every(t=>tripStatus(t)==='selesai')`),nArs);
ok('arsip urut terbaru dulu',nArs<2||E(`arsipTrips()[0].brk >= arsipTrips()[arsipTrips().length-1].brk`));

// pencarian
if(nArs>0){
  const nm=E(`arsipTrips()[0].inst`);
  const kata=String(nm).split(' ')[0];
  E(`setArsipQ(${J(kata)})`);
  const hasil=E(`arsipTrips().length`);
  ok('pencarian menyaring hasil',hasil>0&&hasil<=nArs,`"${kata}" → ${hasil} dari ${nArs}`);
  ok('hasil pencarian cocok',E(`arsipTrips().every(t=>(t.inst+' '+t.dest+' '+(t.jenis||'')).toLowerCase().includes(${J(kata.toLowerCase())}))`));
  E(`setArsipQ('zzzxxxtidakada')`);
  ok('pencarian tanpa hasil ditangani',E(`arsipTrips().length`)===0&&d.getElementById('lapBody').innerHTML.includes('Tidak ada trip yang cocok'));
  E(`setArsipQ('')`);
  ok('reset pencarian kembalikan semua',E(`arsipTrips().length`)===nArs);
  // klik baris -> detail
  E(`openTripDetail(${J(E(`arsipTrips()[0].id`))})`);
  ok('klik arsip buka rekap trip',!!d.getElementById('tripOv'));
  E(`document.getElementById('tripOv').remove()`);
}

// --- PDF laporan ---
try{w.eval(fs.readFileSync(require.resolve('jspdf/dist/jspdf.umd.min.js'),'utf8'));}catch(e){}
w.eval(`window.claude={use:async()=>({save:async({filename,data})=>{window.__cap=window.__cap||[];window.__cap.push({filename,size:data.size});return true;}})};
  const _o=window.jspdf.jsPDF;window.jspdf.jsPDF=function(o){const i=new _o(o);const _t=i.text.bind(i);window.__t=[];i.text=function(s,x,y,op){window.__t.push(String(s));return _t(s,x,y,op);};return i;};`);
E(`setLapTab('rekap');genLaporanPDF()`);
setTimeout(()=>{
  const t=(w.__t||[]).join(' | ');
  ok('PDF: judul LAPORAN KINERJA',t.includes('LAPORAN KINERJA'));
  ok('PDF: periode tercantum',t.includes('Periode:'));
  ok('PDF: ringkasan periode',t.includes('Ringkasan Periode'));
  ok('PDF: laba bersih',t.includes('Laba Bersih'));
  ok('PDF: tren 6 bulan',t.includes('Tren 6 Bulan Terakhir'));
  ok('PDF: daftar trip',t.includes('Daftar Trip Periode Ini'));
  ok('PDF: file tersimpan',(w.__cap||[]).some(c=>c.filename.startsWith('Laporan-')),J((w.__cap||[]).map(c=>c.filename)));

  // semua view tetap sehat
  ['dashboard','keuangan','katalog','acc','jadwal','crew','laporan','setting'].forEach(v=>{
    E(`go('${v}')`);
    if(!d.getElementById('view').innerHTML.length){fail++;console.log('  ✗ view',v,'kosong');}
  });
  ok('8 view render semua',true);

  console.log('\nwindow errors:',(w.__errs||[]).length?w.__errs.join(' | '):'none');
  console.log(`\n${fail===0?'✓ LAPORAN TESTS CLEAN':'✗ '+fail+' GAGAL'} — ${pass} pass, ${fail} fail`);
  process.exit(fail===0&&(w.__errs||[]).length===0?0:1);
},400);
},700);
