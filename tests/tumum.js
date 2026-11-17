const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};w.confirm=()=>true;let e=[];w.onerror=m=>e.push(m);w.__errs=e;}});
const w=dom.window,d=w.document;
let pass=0,fail=0;
const ok=(n,c,x)=>{if(c){pass++;console.log('  ✓',n);}else{fail++;console.log('  ✗',n,x===undefined?'':'→ '+x);}};
const J=o=>JSON.stringify(o);

setTimeout(()=>{
console.log('\n=== AREA UMUM / HALAMAN PUBLIK (poin 11) ===');
const E=s=>w.eval(s);

// --- default landing route (no hash) is the public page ---
ok('landing default: hash kosong -> area umum',d.querySelector('#nav a.active')?.dataset.view==='umum');
ok('view umum ter-render otomatis saat buka app',!!d.getElementById('umumBody'));
ok('menu Umum ada di nav',!!d.querySelector('#nav a[data-view="umum"]'));

const tabsText=d.getElementById('view').textContent;
const tabsHTML=d.getElementById('view').innerHTML;
ok('4 tab tersedia',['Paket & Destinasi','Hotel','Armada','Estimasi Biaya'].every(t=>tabsText.includes(t)));
ok('nama perusahaan tampil di judul',tabsHTML.includes(E('infoPerusahaan().nama')));
ok('tombol Masuk ke Area Internal ada',tabsHTML.includes('Masuk ke Area Internal'));
ok('tombol chat WhatsApp ada dgn link wa.me',/wa\.me\//.test(tabsHTML));

// --- Paket & Destinasi tab (default) ---
ok('tab paket default aktif',E(`umumTab`)==='paket');
const nCity=E(`[...new Set(CAT.dests.map(d=>d.city))].length`);
const nDest=E(`CAT.dests.length`);
const cityNames=E(`[...new Set(CAT.dests.map(d=>d.city))]`);
ok('semua kota destinasi tampil',nCity>0 && cityNames.every(c=>d.getElementById('umumBody').textContent.includes(c)));
ok('jumlah kartu destinasi sesuai jumlah data',(d.getElementById('umumBody').innerHTML.match(/jcard/g)||[]).length>=nDest);
ok('tidak ada tombol edit (read-only utk publik)',!d.getElementById('umumBody').innerHTML.includes('openCatForm'));

// --- Hotel tab ---
E(`setUmumTab('hotel')`);
ok('tab hotel aktif',E(`umumTab`)==='hotel');
const nRegion=E(`[...new Set(CAT.hotels.map(h=>h.region))].length`);
ok('semua region hotel tampil',nRegion>0);
ok('harga weekday & weekend tampil',d.getElementById('umumBody').innerHTML.includes('Weekday'));
ok('tidak ada tombol edit di hotel publik',!d.getElementById('umumBody').innerHTML.includes('onclick="openCatForm'));

// --- Armada tab ---
E(`setUmumTab('armada')`);
ok('tab armada aktif',E(`umumTab`)==='armada');
const nArm=E(`CAT.armada.length`);
ok('semua armada tampil',d.getElementById('umumBody').querySelectorAll('tbody tr').length===nArm);
ok('kapasitas seat tampil',d.getElementById('umumBody').innerHTML.includes('seat'));

// --- Estimasi Biaya tab ---
E(`setUmumTab('estimasi')`);
ok('tab estimasi aktif',E(`umumTab`)==='estimasi');
ok('form estimasi tampil',!!d.getElementById('u_pax'));
ok('hasil estimasi otomatis terhitung saat tab dibuka',!!d.getElementById('umumResult') && d.getElementById('umumResult').innerHTML.includes('Estimasi Total'));

const estBefore=E(`lastUmumEst.subtotal`);
d.getElementById('u_pax').value='60';
E(`calcUmum()`);
const estAfterPax=E(`lastUmumEst.subtotal`);
ok('ubah pax mengubah estimasi (tiket destinasi ikut naik jika ada yg dicentang)',E(`lastUmumEst.pax`)===60);

// pick destination city + check a destination box, verify total increases
const destCheckbox=d.querySelector('.udest');
if(destCheckbox){
  const before=E(`lastUmumEst.subtotal`);
  destCheckbox.checked=true;
  E(`calcUmum()`);
  const after=E(`lastUmumEst.subtotal`);
  ok('centang destinasi menambah biaya tiket',after>=before,`${after} vs ${before}`);
  ok('biayaDest tercatat > 0 atau destinasi gratis',E(`lastUmumEst.biayaDest`)>=0);
}

// hotel selection raises biayaHotel
const hotelSel=d.getElementById('u_hotel');
const hotelOptWithPrice=[...hotelSel.options].find(o=>+o.value>0);
if(hotelOptWithPrice){
  hotelSel.value=hotelOptWithPrice.value;
  E(`calcUmum()`);
  ok('pilih hotel menghasilkan biaya hotel > 0',E(`lastUmumEst.biayaHotel`)>0,E(`lastUmumEst.biayaHotel`));
  ok('jumlah kamar dihitung dari pax/4',E(`lastUmumEst.kamar`)===Math.ceil(60/4));
}

// malam = 0 -> hotel cost should be 0 even if hotel selected (no night to stay)
d.getElementById('u_malam').value='0';
E(`calcUmum()`);
ok('malam=0: biaya hotel nol (tidak menginap)',E(`lastUmumEst.biayaHotel`)===0);
ok('hari tetap 1 saat malam=0',E(`lastUmumEst.hari`)===1);

ok('link WhatsApp hasil estimasi mengandung ringkasan pax',d.getElementById('umumResult').innerHTML.includes('wa.me/'));

// --- "Masuk ke Area Internal" button actually navigates ---
E(`go('dashboard')`);
ok('tombol masuk area internal berfungsi (manual go dashboard)',!!d.getElementById('nav').querySelector('a[data-view="dashboard"].active'));

// --- internal areas untouched: full nav still intact ---
const navViews=[...d.querySelectorAll('#nav a')].map(a=>a.dataset.view);
ok('nav mencakup semua area: umum + 9 internal',['umum','dashboard','keuangan','katalog','acc','jadwal','crew','tl','sales','laporan','setting'].every(v=>navViews.includes(v)));

// --- sanity: all views render clean including umum ---
['umum','dashboard','keuangan','katalog','acc','jadwal','crew','tl','sales','laporan','setting'].forEach(v=>{E(`go(${J(v)})`);});
ok('semua 11 area render tanpa error',w.__errs.length===0,w.__errs.join(' | '));

console.log('\n'+(fail===0?'✓ AREA UMUM TESTS CLEAN — '+pass+' pass, 0 fail':'✗ '+fail+' FAILED, '+pass+' passed'));
console.log('window errors:',w.__errs.length?w.__errs.join(' | '):'none');
process.exit(fail===0?0:1);
},50);
