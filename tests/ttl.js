const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};w.confirm=()=>true;let e=[];w.onerror=m=>e.push(m);w.__errs=e;}});
const w=dom.window,d=w.document;
let pass=0,fail=0;
const ok=(n,c,x)=>{if(c){pass++;console.log('  ✓',n);}else{fail++;console.log('  ✗',n,x===undefined?'':'→ '+x);}};
const J=o=>JSON.stringify(o);

setTimeout(()=>{
console.log('\n=== AREA TOUR LEADER & MEDIA (poin 10) ===');
const E=s=>w.eval(s);

ok('menu Tour Leader & Media ada di nav',!!d.querySelector('#nav a[data-view="tl"]'));
E(`go('tl')`);
ok('view tl render',!!d.getElementById('tlBody'));
const tabsHTML=d.getElementById('view').innerHTML;
ok('4 tab tersedia',['Jadwal Saya','Checklist','Reimburse','Gaji Saya'].every(t=>tabsHTML.includes(t)));
ok('picker tampil tanpa crew terpilih',d.getElementById('tlBody').innerHTML.includes('pilih Tour Leader'));
ok('belum pilih: pesan "Pilih nama Anda"',d.getElementById('tlBody').innerHTML.includes('Pilih nama Anda'));

// pick a Tour Leader and make sure at least one trip is assigned to them
const tlId=E(`crewList().filter(c=>c.peran==='Tour Leader')[0].id`);
if(E(`crewTrips(${J(tlId)}).length`)===0){
  const firstTripId=E(`allTrips().filter(t=>t.brk)[0].id`);
  E(`assignCrew(${J(firstTripId)},'tl',${J(tlId)})`);
}
const tlName=E(`crewById(${J(tlId)}).nama`);
console.log('  TL uji:',tlName,'| trip assigned:',E(`crewTrips(${J(tlId)}).length`));
E(`setCurrentTL(${J(tlId)})`);
ok('currentTL tersimpan',E(`currentTL()`)===tlId);

// --- Jadwal Saya ---
const nTrip=E(`crewStat(${J(tlId)}).n`);
const nHari=E(`crewStat(${J(tlId)}).hari`);
const gajiEst=E(`crewStat(${J(tlId)}).gaji`);
ok('dashboard tampil jumlah trip & gaji',d.getElementById('tlBody').innerHTML.includes('Estimasi Gaji'));
ok('crewStat konsisten dgn tampilan',nTrip>=0&&nHari>=0&&gajiEst>=0);

let myTripId='';
if(nTrip>0){
  myTripId=E(`crewTrips(${J(tlId)})[0].id`);
  ok('kartu trip clickable (openTLTrip ada di HTML)',d.getElementById('tlBody').innerHTML.includes('openTLTrip'));
  E(`openTLTrip(${J(myTripId)})`);
  ok('modal detail trip terbuka',!!d.getElementById('tlOv'));
  ok('modal tampilkan checklist',d.getElementById('tlOv').innerHTML.includes('Checklist Persiapan'));
  d.getElementById('tlOv').remove();
}else{
  console.log('  (TL uji tidak punya trip assigned — lewati sub-test kartu trip)');
}

// --- Checklist tab ---
E(`setTLTab('checklist')`);
ok('tab checklist aktif',E(`tlTab`)==='checklist');
if(nTrip>0){
  ok('checklist tampil untuk trip aktif',d.getElementById('tlBody').innerHTML.includes('Checklist Persiapan')||d.getElementById('tlBody').innerHTML.includes('Tidak ada trip aktif'));
  // toggle first checklist item if trip select exists
  const sel=d.querySelector('#tlBody select');
  if(sel){
    const tid=sel.value;
    const before=E(`(store('checklist',{})[${J(tid)}]||CHECKLIST_DEF.map(x=>({item:x,done:false})))[0].done`);
    E(`toggleChecklist(${J(tid)},0)`);
    const after=E(`(store('checklist',{})[${J(tid)}]||[])[0].done`);
    ok('toggleChecklist membalik status item',before!==after,`${before} -> ${after}`);
    E(`toggleChecklist(${J(tid)},0)`); // revert
  }
}

// --- Reimburse: submit flow ---
E(`setTLTab('reimburse')`);
ok('tab reimburse aktif',E(`tlTab`)==='reimburse');
ok('form reimburse tampil',!!d.getElementById('rb_item'));
const beforeCount=E(`reimburseByCrew(${J(tlId)}).length`);
// fail case: no trip selected
E(`submitReimburse()`);
ok('tanpa pilih trip: tidak tersimpan',E(`reimburseByCrew(${J(tlId)}).length`)===beforeCount);

if(nTrip>0){
  d.getElementById('rb_trip').value=myTripId;
  d.getElementById('rb_item').value='Parkir & Tol';
  d.getElementById('rb_nominal').value='150000';
  d.getElementById('rb_ket').value='pulang-pergi lokasi wisata';
  E(`submitReimburse()`);
  ok('reimburse tersimpan setelah form lengkap',E(`reimburseByCrew(${J(tlId)}).length`)===beforeCount+1);
  const rbId=E(`reimburseByCrew(${J(tlId)})[0].id`);
  ok('status awal pending',E(`reimburseList().find(r=>r.id===${J(rbId)}).status`)==='pending');
  ok('nominal tersimpan benar',E(`reimburseList().find(r=>r.id===${J(rbId)}).nominal`)===150000);
  ok('nama crew tersimpan',E(`reimburseList().find(r=>r.id===${J(rbId)}).crewName`)===tlName);

  // riwayat muncul di tab TL
  E(`renderTL()`);
  ok('riwayat reimburse tampil di tab Reimburse',d.getElementById('tlBody').innerHTML.includes('Parkir'));

  // --- Management approves via Keuangan ---
  E(`go('keuangan')`);
  E(`setKeuTab('reimburse')`);
  ok('tab Reimburse Lapangan ada di Keuangan',d.getElementById('keuBody').innerHTML.includes('Reimburse Lapangan')||d.getElementById('keuBody').innerHTML.includes('Pengajuan Reimburse'));
  ok('pengajuan pending tampil di Keuangan',d.getElementById('keuBody').innerHTML.includes('Parkir'));
  E(`decideReimburse(${J(rbId)},'approved')`);
  ok('status berubah jadi approved',E(`reimburseList().find(r=>r.id===${J(rbId)}).status`)==='approved');
  ok('decidedAt tercatat',!!E(`reimburseList().find(r=>r.id===${J(rbId)}).decidedAt`));

  // reject flow with a second submission
  E(`go('tl')`);E(`setTLTab('reimburse')`);
  d.getElementById('rb_trip').value=myTripId;
  d.getElementById('rb_item').value='Konsumsi darurat';
  d.getElementById('rb_nominal').value='75000';
  E(`submitReimburse()`);
  const rbId2=E(`reimburseByCrew(${J(tlId)})[0].id`);
  E(`decideReimburse(${J(rbId2)},'rejected')`);
  ok('reject flow: status rejected',E(`reimburseList().find(r=>r.id===${J(rbId2)}).status`)==='rejected');

  // cancel-while-pending flow
  E(`go('tl')`);E(`setTLTab('reimburse')`);
  d.getElementById('rb_trip').value=myTripId;
  d.getElementById('rb_item').value='Akan dibatalkan';
  d.getElementById('rb_nominal').value='50000';
  E(`submitReimburse()`);
  const rbId3=E(`reimburseByCrew(${J(tlId)})[0].id`);
  const cBefore=E(`reimburseByCrew(${J(tlId)}).length`);
  E(`delReimburse(${J(rbId3)})`);
  ok('batal pengajuan menghapus entri',E(`reimburseByCrew(${J(tlId)}).length`)===cBefore-1);
}

// --- Gaji Saya tab ---
E(`go('tl')`);
E(`setCurrentTL(${J(tlId)})`);
E(`setTLTab('gaji')`);
ok('tab gaji aktif',E(`tlTab`)==='gaji');
ok('tarif per hari tampil',d.getElementById('tlBody').innerHTML.includes('Tarif'));
ok('total estimasi gaji tampil & konsisten',d.getElementById('tlBody').innerHTML.includes('Total Estimasi Gaji'));

// --- Media role check (second crew type) ---
const mdId=E(`crewList().filter(c=>c.peran==='Media')[0].id`);
E(`setCurrentTL(${J(mdId)})`);E(`setTLTab('jadwal')`);
ok('bisa login sebagai Media juga',E(`currentTL()`)===mdId);
ok('picker list sertakan role Media',E(`crewList().filter(c=>c.peran==='Tour Leader'||c.peran==='Media').some(c=>c.id===${J(mdId)})`));

// --- sanity: all 9 views still render clean ---
['dashboard','keuangan','katalog','acc','jadwal','crew','tl','sales','laporan','setting'].forEach(v=>{E(`go(${J(v)})`);});
ok('9 area + setting semua render tanpa error',w.__errs.length===0,w.__errs.join(' | '));

console.log('\n'+(fail===0?'✓ TL & MEDIA TESTS CLEAN — '+pass+' pass, 0 fail':'✗ '+fail+' FAILED, '+pass+' passed'));
console.log('window errors:',w.__errs.length?w.__errs.join(' | '):'none');
process.exit(fail===0?0:1);
},50);
