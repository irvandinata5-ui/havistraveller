const fs=require('fs');const {JSDOM}=require('jsdom');
const html=fs.readFileSync('index.html','utf8');
const dom=new JSDOM(html,{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};let e=[];w.onerror=m=>e.push(m);w.__errs=e;}});
const w=dom.window;
const errs=w.__errs;
let pass=0,fail=0;
const ok=(n,c,extra)=>{if(c){pass++;console.log('  ✓',n);}else{fail++;console.log('  ✗',n,extra===undefined?'':'→ '+extra);}};

setTimeout(()=>{
console.log('\n=== PERSIAPAN VENDOR (poin 3) ===');
const E=s=>w.eval(s);

// pick an upcoming trip
const tid=E('upcoming()[0] && upcoming()[0].id');
ok('ada trip akan datang',!!tid,tid);
const t=E(`JSON.stringify(allTrips().find(x=>x.id===${JSON.stringify(tid)}))`);
const trip=JSON.parse(t);
console.log('  trip:',trip.inst,'|',trip.pax,'pax | brk',trip.brk);

// 1. prep kosong awal
ok('prep awal kosong',E(`prepTrip(${JSON.stringify(tid)}).length`)===0);

// 2. baseline keuangan
const keluar0=E('totalKeluar()'),vend0=E('allVendor().length');

// 3. auto fill
E(`openPrep(${JSON.stringify(tid)})`);
ok('modal prep terbuka',!!w.document.getElementById('prepOv'));
ok('timeline H-30..H-1 ada',w.document.querySelectorAll('#prepOv .tl-item').length===4,w.document.querySelectorAll('#prepOv .tl-item').length);
E(`prepAutoFill(${JSON.stringify(tid)})`);
const n=E(`prepTrip(${JSON.stringify(tid)}).length`);
ok('auto-fill membuat kebutuhan',n>=3,n+' item');
const tot=E(`prepTotal(${JSON.stringify(tid)})`);
ok('total vendor > 0',tot>0,'Rp '+tot.toLocaleString('id-ID'));
const kats=JSON.parse(E(`JSON.stringify(prepTrip(${JSON.stringify(tid)}).map(x=>x.kat))`));
ok('ada kategori armada',kats.includes('Transport / Bus'));
ok('ada kategori konsumsi',kats.includes('Konsumsi / Katering'));
ok('ada kategori tiket',kats.includes('Wisata / Tiket'));
// jatuh tempo terisi
const dues=JSON.parse(E(`JSON.stringify(prepTrip(${JSON.stringify(tid)}).map(x=>x.due))`));
ok('jatuh tempo terisi semua',dues.every(d=>!!d),dues.join(', '));

// 4. masuk ke allVendor (sinkron Keuangan)
ok('kebutuhan masuk daftar vendor',E('allVendor().length')===vend0+n,E('allVendor().length')+' vs '+(vend0+n));

// 5. bayar satu kebutuhan → Arus Kas naik
const pid=E(`prepTrip(${JSON.stringify(tid)})[0].id`);
const pnom=E(`prepTrip(${JSON.stringify(tid)})[0].nom`);
E(`addVendorPayment(${JSON.stringify(pid)},${Math.round(pnom/2)},'2026-11-16','tes dp')`);
const paidHalf=E(`prepPaid(${JSON.stringify(tid)})`);
ok('pembayaran sebagian tercatat',paidHalf===Math.round(pnom/2),paidHalf);
ok('sisa berkurang',E(`prepSisa(${JSON.stringify(tid)})`)===tot-Math.round(pnom/2));
ok('Arus Kas uang keluar naik',E('totalKeluar()')===keluar0+Math.round(pnom/2),E('totalKeluar()')+' vs '+(keluar0+Math.round(pnom/2)));

// 6. status vendor virtual
const sc=JSON.parse(E(`JSON.stringify(vendorStatusArr(allVendor().find(d=>d.no===${JSON.stringify(pid)})))`));
ok('status jadi Sebagian',sc[0]==='dp',sc.join('/'));

// 7. modal bayar vendor buka utk item prep
E(`openBayarVendor(${JSON.stringify(pid)})`);
ok('modal bayar vendor prep terbuka',!!w.document.getElementById('bayarOv'));
E(`document.getElementById('bayarOv').remove()`);

// 8. tambah manual via form
E(`openPrep(${JSON.stringify(tid)})`);
E(`document.getElementById('pp_kat').value='Operasional / Lainnya';onPrepKat(${JSON.stringify(tid)})`);
E(`document.getElementById('pp_vendor').value='Dokumentasi Drone';document.getElementById('pp_qty').value=1;document.getElementById('pp_unit').value=750000;`);
E(`submitPrep(${JSON.stringify(tid)})`);
ok('tambah manual berhasil',E(`prepTrip(${JSON.stringify(tid)}).length`)===n+1);
ok('vendor manual tersimpan',E(`prepTrip(${JSON.stringify(tid)}).some(x=>x.vendor==='Dokumentasi Drone')`));

// 9. kategori hotel isi dropdown dari katalog
E(`document.getElementById('pp_kat').value='Hotel / Villa';onPrepKat(${JSON.stringify(tid)})`);
const hv=E(`document.getElementById('pp_vendor').tagName`);
ok('hotel pakai dropdown katalog',hv==='SELECT',hv);
ok('harga satuan hotel auto-terisi',E(`+document.getElementById('pp_unit').value`)>0,E(`+document.getElementById('pp_unit').value`));

// 10. hapus
E(`prepDel(${JSON.stringify(tid)},${JSON.stringify(pid)})`);
ok('hapus kebutuhan berhasil',E(`prepTrip(${JSON.stringify(tid)}).length`)===n);
E(`const o=document.getElementById('prepOv');if(o)o.remove()`);

// 11. trip detail menampilkan persiapan
E(`openTripDetail(${JSON.stringify(tid)})`);
const txt=w.document.getElementById('tripOv').textContent;
ok('trip detail ada bagian Persiapan Vendor',txt.includes('Persiapan Vendor'));
ok('trip detail tampilkan total biaya vendor',txt.includes('Total biaya vendor'));
E(`document.getElementById('tripOv').remove()`);

// 12. keuangan vendor tab render
E(`go('keuangan');setKeuTab('vendor')`);
const kv=w.document.getElementById('keuBody').textContent;
ok('tab vendor ada panel Persiapan per Trip',kv.includes('Persiapan Vendor per Trip'));
ok('tab vendor tampilkan item prep',kv.includes('item'));

// 13. dashboard alert
E(`go('dashboard')`);
ok('dashboard render tanpa error',!!w.document.getElementById('view').textContent);

console.log('\nwindow errors:',errs.length?errs.join(' | '):'none');
console.log(`\n${fail===0?'✓ PREP TESTS CLEAN':'✗ '+fail+' GAGAL'} — ${pass} pass, ${fail} fail`);
process.exit(fail===0&&errs.length===0?0:1);
},700);
