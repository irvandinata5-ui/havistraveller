const fs=require('fs');const {JSDOM}=require('jsdom');
let confirmAns=true,confirmMsg='';
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};
    w.confirm=m=>{confirmMsg=m;return confirmAns;};let e=[];w.onerror=m=>e.push(m);w.__errs=e;}});
const w=dom.window,d=w.document;
let pass=0,fail=0;
const ok=(n,c,x)=>{if(c){pass++;console.log('  ✓',n);}else{fail++;console.log('  ✗',n,x===undefined?'':'→ '+x);}};

setTimeout(()=>{
console.log('\n=== CREW: KETERSEDIAAN & RIWAYAT (poin 16) ===');
const E=s=>w.eval(s);
const J=o=>JSON.stringify(o);

const tl=E(`crewList().filter(c=>c.peran==='Tour Leader')[0].id`);
const tlName=E(`crewById(${J(tl)}).nama`);
const tarif=E(`crewById(${J(tl)}).tarif`);
console.log('  crew uji:',tlName,'| tarif',tarif);

// dua trip yang tanggalnya bentrok
const trips=JSON.parse(E(`JSON.stringify(upcoming().slice(0,6).map(t=>({id:t.id,inst:t.inst,brk:t.brk,pul:t.pul,hari:tripDays(t)})))`));
console.log('  trip tersedia:',trips.map(t=>t.brk).join(', '));
// pilih pasangan trip yang benar-benar overlap (ada 3 trip di tanggal sama)
let t1=trips[0];
const pair=(()=>{for(let i=0;i<trips.length;i++)for(let j=i+1;j<trips.length;j++){
  if(E(`overlap(tripRange(allTrips().find(x=>x.id===${J(trips[i].id)})),tripRange(allTrips().find(x=>x.id===${J(trips[j].id)})))`))return[trips[i],trips[j]];}return null;})();
if(pair)t1=pair[0];
// cari trip lain yang tanggalnya overlap dengan t1
let t2=pair?pair[1]:trips.slice(1).find(t=>E(`overlap(tripRange(allTrips().find(x=>x.id===${J(t1.id)})),tripRange(allTrips().find(x=>x.id===${J(t.id)})))`));
const t3=trips.filter(t=>t.id!==t1.id&&(!t2||t.id!==t2.id)).find(t=>!E(`overlap(tripRange(allTrips().find(x=>x.id===${J(t1.id)})),tripRange(allTrips().find(x=>x.id===${J(t.id)})))`));

// --- helper dasar ---
ok('tripRange menghasilkan rentang',E(`!!tripRange(allTrips().find(x=>x.id===${J(t1.id)}))`));
ok('overlap: rentang sama = bentrok',E(`overlap([new Date('2026-12-01'),new Date('2026-12-03')],[new Date('2026-12-02'),new Date('2026-12-05')])`)===true);
ok('overlap: rentang terpisah = aman',E(`overlap([new Date('2026-12-01'),new Date('2026-12-03')],[new Date('2026-12-10'),new Date('2026-12-12')])`)===false);

// --- assign pertama: tidak ada bentrok, tidak ada konfirmasi ---
confirmMsg='';confirmAns=true;
E(`assignCrew(${J(t1.id)},'tl',${J(tl)})`);
ok('assign pertama tanpa peringatan',confirmMsg==='',confirmMsg.slice(0,60));
ok('crew tertugaskan',E(`(assignMap()[${J(t1.id)}]||{}).tl`)===tl);
ok('crewTrips mencatat 1 trip',E(`crewTrips(${J(tl)}).length`)===1);

// --- assign ke trip bentrok: harus minta konfirmasi ---
if(t2){
  console.log('  trip bentrok:',t2.brk,'vs',t1.brk);
  ok('crewSibuk mendeteksi bentrok',E(`crewSibuk(${J(tl)},${J(t2.id)})`)===true);
  confirmMsg='';confirmAns=false;
  E(`assignCrew(${J(t2.id)},'tl',${J(tl)})`);
  ok('muncul konfirmasi bentrok',confirmMsg.includes('sudah bertugas'),confirmMsg.slice(0,70));
  ok('konfirmasi sebut nama crew',confirmMsg.includes(tlName));
  ok('konfirmasi sebut trip bentrok',confirmMsg.includes(t1.inst));
  ok('tolak konfirmasi = tidak jadi ditugaskan',E(`(assignMap()[${J(t2.id)}]||{}).tl`)===undefined,E(`JSON.stringify(assignMap()[${J(t2.id)}])`));
  confirmAns=true;
  E(`assignCrew(${J(t2.id)},'tl',${J(tl)})`);
  ok('terima konfirmasi = tetap ditugaskan',E(`(assignMap()[${J(t2.id)}]||{}).tl`)===tl);
  // bersihkan supaya tes berikutnya bersih
  E(`const s=assignMap();delete s[${J(t2.id)}];save('assign',s)`);
}else{console.log('  (tidak ada trip bentrok di data, lewati)');}

// --- assign ke trip tidak bentrok: tanpa konfirmasi ---
if(t3){
  confirmMsg='';confirmAns=true;
  E(`assignCrew(${J(t3.id)},'tl',${J(tl)})`);
  ok('trip tidak bentrok: tanpa peringatan',confirmMsg==='',confirmMsg.slice(0,60));
  ok('dua trip tercatat',E(`crewTrips(${J(tl)}).length`)===2);
}

// --- statistik & gaji ---
const st=JSON.parse(E(`JSON.stringify((()=>{const s=crewStat(${J(tl)});return{n:s.n,hari:s.hari,gaji:s.gaji};})())`));
ok('crewStat hitung jumlah trip',st.n===E(`crewTrips(${J(tl)}).length`),st.n);
ok('crewStat hitung total hari',st.hari>0,st.hari);
ok('gaji = tarif × total hari',st.gaji===tarif*st.hari,`${st.gaji} vs ${tarif}×${st.hari}`);

// --- dropdown menandai crew bentrok ---
E(`go('crew');setCrewTab('penugasan')`);
const pen=d.getElementById('crewBody').innerHTML;
ok('tab penugasan render',pen.length>200);
if(t2)ok('dropdown tandai crew bentrok',pen.includes('bentrok'),pen.includes('⚠')?'ada ⚠':'tidak ada penanda');

// --- daftar crew: kolom trip & gaji ---
E(`setCrewTab('daftar')`);
const daf=d.getElementById('crewBody').innerHTML;
ok('daftar crew ada kolom Trip',daf.includes('<th>Trip</th>'));
ok('daftar crew ada kolom Total Gaji',daf.includes('Total Gaji'));
ok('daftar crew tampil jumlah trip',daf.includes('trip</td>')||daf.includes(' trip'));
ok('baris crew bisa diklik',daf.includes('openCrew('));

// --- modal riwayat crew ---
E(`openCrew(${J(tl)})`);
const ov=d.getElementById('crewOv');
ok('modal riwayat terbuka',!!ov);
const txt=ov.textContent;
ok('modal tampil nama crew',txt.includes(tlName));
ok('modal tampil Total Trip',txt.includes('Total Trip'));
ok('modal tampil Total Gaji',txt.includes('Total Gaji'));
ok('modal tampil riwayat trip',txt.includes(t1.inst),txt.slice(0,120));
ok('modal tampil peran di trip',txt.includes('Tour Leader'));
E(`document.getElementById('crewOv').remove()`);

// --- crew tanpa trip ---
const sales=E(`crewList().filter(c=>c.peran==='Sales')[0].id`);
E(`openCrew(${J(sales)})`);
ok('crew tanpa trip: pesan kosong',d.getElementById('crewOv').textContent.includes('Belum pernah ditugaskan'));
E(`document.getElementById('crewOv').remove()`);

// --- trip detail juga menandai bentrok ---
if(t2){
  E(`openTripDetail(${J(t2.id)})`);
  ok('detail trip tandai crew bentrok',d.getElementById('tripOv').innerHTML.includes('bentrok'));
  E(`document.getElementById('tripOv').remove()`);
}

// --- lepas penugasan ---
E(`assignCrew(${J(t1.id)},'tl','')`);
ok('lepas penugasan berhasil',E(`(assignMap()[${J(t1.id)}]||{}).tl`)===undefined);

console.log('\nwindow errors:',(w.__errs||[]).length?w.__errs.join(' | '):'none');
console.log(`\n${fail===0?'✓ CREW TESTS CLEAN':'✗ '+fail+' GAGAL'} — ${pass} pass, ${fail} fail`);
process.exit(fail===0&&(w.__errs||[]).length===0?0:1);
},700);
