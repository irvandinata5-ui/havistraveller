const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};w.confirm=()=>true;let e=[];w.onerror=m=>e.push(m);w.__errs=e;}});
const w=dom.window,d=w.document;
let pass=0,fail=0;
const ok=(n,c,x)=>{if(c){pass++;console.log('  ✓',n);}else{fail++;console.log('  ✗',n,x===undefined?'':'→ '+x);}};

setTimeout(()=>{
console.log('\n=== KATALOG EDITABLE (poin 14) ===');
const E=s=>w.eval(s);

const n0=E('CAT.hotels.length'),a0=E('CAT.armada.length'),d0=E('CAT.dests.length');
ok('CAT baca data dasar',n0>50&&a0>0&&d0>100,`${n0} hotel, ${a0} armada, ${d0} dest`);
ok('belum ada perubahan',E(`!catEdited('hotels')`));

// --- TAMBAH HOTEL ---
E(`go('katalog');setKatTab('hotel')`);
ok('tab hotel ada tombol Tambah',d.getElementById('katBody').innerHTML.includes("openCatForm('hotels',-1)"));
E(`openCatForm('hotels',-1)`);
ok('form tambah hotel terbuka',!!d.getElementById('catOv'));
ok('form punya field nama',!!d.getElementById('cf_name'));
ok('field daerah pakai datalist',(d.getElementById('cf_region')||{}).getAttribute&&d.getElementById('cf_region').getAttribute('list')==='cf_dl');
d.getElementById('cf_name').value='HOTEL UJI COBA';
d.getElementById('cf_region').value='TANGERANG';
d.getElementById('cf_wd').value='350000';
d.getElementById('cf_we').value='450000';
E(`submitCatForm('hotels',-1)`);
ok('hotel bertambah',E('CAT.hotels.length')===n0+1,E('CAT.hotels.length'));
ok('ditandai sudah diubah',E(`catEdited('hotels')`));
const nh=E(`JSON.stringify(CAT.hotels[CAT.hotels.length-1])`);
ok('data hotel baru benar',JSON.parse(nh).name==='HOTEL UJI COBA'&&JSON.parse(nh).wd===350000,nh);

// --- MUNCUL DI KALKULATOR (yang paling penting) ---
E(`setKatTab('kalkulator')`);
const hopt=d.getElementById('q_hotel').innerHTML;
ok('hotel baru muncul di kalkulator',hopt.includes('HOTEL UJI COBA'));
ok('harga hotel baru di kalkulator',hopt.includes('350.000'),hopt.match(/HOTEL UJI COBA[^<]*/)||'');
ok('grup daerah baru muncul',hopt.includes('TANGERANG'));

// --- MUNCUL DI PERSIAPAN VENDOR ---
const tid=E('upcoming()[0].id');
E(`openPrep(${JSON.stringify(tid)})`);
E(`document.getElementById('pp_kat').value='Hotel / Villa';onPrepKat(${JSON.stringify(tid)})`);
ok('hotel baru muncul di persiapan vendor',d.getElementById('pp_vendor').innerHTML.includes('HOTEL UJI COBA'));
E(`document.getElementById('prepOv').remove()`);

// --- EDIT HOTEL ---
E(`setKatTab('hotel');openCatForm('hotels',0)`);
const nm0=E('CAT.hotels[0].name');
d.getElementById('cf_wd').value='999000';
E(`submitCatForm('hotels',0)`);
ok('edit harga hotel tersimpan',E('CAT.hotels[0].wd')===999000,E('CAT.hotels[0].wd'));
ok('nama hotel tidak berubah',E('CAT.hotels[0].name')===nm0);
ok('edit terbaca kalkulator',(()=>{E(`setKatTab('kalkulator')`);return d.getElementById('q_hotel').innerHTML.includes('999.000');})());

// --- HAPUS ---
E(`setKatTab('hotel')`);
const before=E('CAT.hotels.length');
E(`catDel('hotels',CAT.hotels.length-1)`);
ok('hapus hotel berhasil',E('CAT.hotels.length')===before-1);
ok('hotel terhapus hilang dari kalkulator',(()=>{E(`setKatTab('kalkulator')`);return !d.getElementById('q_hotel').innerHTML.includes('HOTEL UJI COBA');})());

// --- ARMADA (dengan seat) ---
E(`setKatTab('armada');openCatForm('armada',-1)`);
d.getElementById('cf_name').value='BUS TINGKAT UJI';
d.getElementById('cf_rate').value='4500000';
d.getElementById('cf_seat').value='59';
E(`submitCatForm('armada',-1)`);
ok('armada bertambah',E('CAT.armada.length')===a0+1);
ok('kapasitas custom dipakai',E(`armSeat(CAT.armada[CAT.armada.length-1])`)===59,E(`armSeat(CAT.armada[CAT.armada.length-1])`));
E(`setKatTab('armada')`);
ok('tabel armada tampilkan 59 seat',d.getElementById('katBody').innerHTML.includes('59 seat'));
ok('armada baru di kalkulator',(()=>{E(`setKatTab('kalkulator')`);return d.getElementById('q_arm').innerHTML.includes('BUS TINGKAT UJI');})());

// --- DESTINASI ---
E(`setKatTab('destinasi');openCatForm('dests',-1)`);
d.getElementById('cf_name').value='Pantai Uji Coba';
d.getElementById('cf_city').value='BANTEN';
d.getElementById('cf_note').value='Rekreasi';
d.getElementById('cf_price').value='25000';
E(`submitCatForm('dests',-1)`);
ok('destinasi bertambah',E('CAT.dests.length')===d0+1);
ok('destinasi baru di kalkulator',(()=>{E(`setKatTab('kalkulator')`);return d.getElementById('view').innerHTML.includes('Pantai Uji Coba');})());

// --- KAOS ---
E(`setKatTab('armada');openCatForm('kaos',-1)`);
d.getElementById('cf_name').value='Kaos Premium Uji';
d.getElementById('cf_price').value='85000';
E(`submitCatForm('kaos',-1)`);
ok('kaos baru di kalkulator',(()=>{E(`setKatTab('kalkulator')`);return d.getElementById('q_kaos').innerHTML.includes('Kaos Premium Uji');})());

// --- KALKULATOR TETAP MENGHITUNG BENAR ---
E(`setKatTab('kalkulator')`);
d.getElementById('q_pax').value='50';d.getElementById('q_malam').value='0';d.getElementById('q_tgl').value='2026-12-15';
E(`calcQuote()`);
const pp=E('lastQuote&&lastQuote.perpax');
ok('kalkulator tetap menghitung',pp>0,'Rp '+(pp||0).toLocaleString('id-ID'));

// --- RESET ---
E(`catReset('hotels')`);
ok('reset hotel kembali ke Excel',E('CAT.hotels.length')===n0,E('CAT.hotels.length')+' vs '+n0);
ok('harga hotel pulih',E('CAT.hotels[0].wd')!==999000);
ok('armada tetap (reset per-jenis)',E('CAT.armada.length')===a0+1);

// --- VALIDASI ---
E(`setKatTab('hotel');openCatForm('hotels',-1)`);
d.getElementById('cf_name').value='';
const cnt=E('CAT.hotels.length');
E(`submitCatForm('hotels',-1)`);
ok('nama kosong ditolak',E('CAT.hotels.length')===cnt);
ok('modal tetap terbuka saat invalid',!!d.getElementById('catOv'));
E(`document.getElementById('catOv').remove()`);

console.log('\nwindow errors:',(w.__errs||[]).length?w.__errs.join(' | '):'none');
console.log(`\n${fail===0?'✓ KATALOG TESTS CLEAN':'✗ '+fail+' GAGAL'} — ${pass} pass, ${fail} fail`);
process.exit(fail===0&&(w.__errs||[]).length===0?0:1);
},700);
