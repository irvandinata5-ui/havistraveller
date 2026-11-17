const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};w.confirm=()=>true;let e=[];w.onerror=m=>e.push(m);w.__errs=e;}});
const w=dom.window,d=w.document;
let pass=0,fail=0;
const ok=(n,c,x)=>{if(c){pass++;console.log('  ✓',n);}else{fail++;console.log('  ✗',n,x===undefined?'':'→ '+x);}};
const J=o=>JSON.stringify(o);

setTimeout(()=>{
console.log('\n=== AREA SALES (poin 9) ===');
const E=s=>w.eval(s);

ok('menu Sales ada di nav',!!d.querySelector('#nav a[data-view="sales"]'));
E(`go('sales')`);
ok('view sales render',!!d.getElementById('salesBody'));
const tabs=d.getElementById('view').innerHTML;
ok('4 tab tersedia',['Dashboard','Buat Penawaran','Data Klien','Performa Sales'].every(t=>tabs.includes(t)));

// --- picker sales ---
ok('dashboard: picker tampil tanpa sales terpilih',d.getElementById('salesBody').innerHTML.includes('pilih sales'));
const salesId=E(`crewList().filter(c=>c.peran==='Sales')[0].id`);
const salesName=E(`crewById(${J(salesId)}).nama`);
console.log('  sales uji:',salesName);
E(`setCurrentSales(${J(salesId)})`);
ok('currentSales tersimpan',E(`currentSales()`)===salesId);
ok('dashboard tampil nama sales setelah pilih',d.getElementById('salesBody').innerHTML.includes('Penawaran Dibuat'));

// --- diskon di kalkulator (regresi + fitur baru) ---
E(`setSalesTab('penawaran')`);
ok('tab penawaran reuse kalkulator',!!d.getElementById('q_pax'));
ok('field diskon ada',!!d.getElementById('q_diskon'));
d.getElementById('q_pax').value='50';d.getElementById('q_malam').value='0';d.getElementById('q_tgl').value='2026-12-10';
E(`calcQuote()`);
const perpaxNoDisc=E(`lastQuote.perpax`),totalNoDisc=E(`lastQuote.total`),labaNoDisc=E(`lastQuote.laba`);
ok('tanpa diskon: harga > 0',perpaxNoDisc>0,perpaxNoDisc);
d.getElementById('q_diskon').value='2000000';
E(`calcQuote()`);
const totalDisc=E(`lastQuote.total`),labaDisc=E(`lastQuote.laba`),perpaxDisc=E(`lastQuote.perpax`);
ok('diskon mengurangi total jual',totalDisc===totalNoDisc-2000000,`${totalDisc} vs ${totalNoDisc}-2jt`);
ok('diskon mengurangi laba',labaDisc===labaNoDisc-2000000,`${labaDisc} vs ${labaNoDisc}-2jt`);
ok('diskon mengurangi perpax',perpaxDisc<=perpaxNoDisc);
ok('lastQuote.diskon tercatat',E(`lastQuote.diskon`)===2000000);
ok('komisi dihitung dari harga setelah diskon',E(`lastQuote.komisi`)===Math.round(totalDisc*0.05),`${E('lastQuote.komisi')} vs ${Math.round(totalDisc*0.05)}`);
ok('tampilan diskon di UI',d.getElementById('q_diskonshow').textContent.includes('2.000.000'));

// diskon berlebihan -> warning rugi tapi tidak crash
d.getElementById('q_diskon').value='999999999';
E(`calcQuote()`);
ok('diskon ekstrem tidak membuat total negatif',E(`lastQuote.total`)>=0,E(`lastQuote.total`));
ok('peringatan rugi muncul',d.getElementById('q_laba').innerHTML.includes('rugi'));
d.getElementById('q_diskon').value='0';
E(`calcQuote()`);

// --- simpan penawaran dengan atribusi sales ---
d.getElementById('q_klien').value='SMA Uji Coba Sales';
d.getElementById('q_dest').value='Bandung';
d.getElementById('q_hp').value='081234567890';
d.getElementById('q_diskon').value='1000000';
E(`calcQuote()`);
const n0=E(`penawaran().length`);
E(`saveQuote()`);
ok('penawaran baru tersimpan',E(`penawaran().length`)===n0+1);
const saved=JSON.parse(E(`JSON.stringify(penawaran()[penawaran().length-1])`));
ok('penawaran tercatat atas nama sales',saved.salesId===salesId&&saved.salesName===salesName,J(saved.salesName));
ok('diskon ikut tersimpan',saved.diskon===1000000,saved.diskon);
ok('komisi ikut tersimpan',saved.komisi>0,saved.komisi);
ok('form kosong setelah simpan',d.getElementById('q_klien').value==='');

// --- klien otomatis tercatat (CRM ringan) ---
ok('klien baru otomatis masuk klienList',E(`klienList().some(k=>k.nama==='SMA Uji Coba Sales')`));
const kl=JSON.parse(E(`JSON.stringify(klienList().find(k=>k.nama==='SMA Uji Coba Sales'))`));
ok('klien tersimpan dengan hp',kl.hp==='081234567890',kl.hp);
ok('klien tersimpan dengan nama sales',kl.sales===salesName,kl.sales);

// --- tambah klien manual ---
E(`setSalesTab('klien')`);
const kb=d.getElementById('salesBody').innerHTML;
ok('tab klien tampil daftar',kb.includes('Data Klien'));
ok('klien baru muncul di tabel',kb.includes('SMA Uji Coba Sales'));
d.getElementById('kl_nama').value='PT Manual Entry';
d.getElementById('kl_hp').value='089988887777';
d.getElementById('kl_instansi').value='Perusahaan Swasta';
const kn0=E(`klienList().length`);
E(`addKlienManual()`);
ok('tambah klien manual berhasil',E(`klienList().length`)===kn0+1);
ok('nama kosong ditolak',(()=>{const kn1=E('klienList().length');d.getElementById('kl_nama').value='';w.addKlienManual();return E('klienList().length')===kn1;})());

// hapus klien
const delId=E(`klienList().find(k=>k.nama==='PT Manual Entry').id`);
E(`delKlien(${J(delId)})`);
ok('hapus klien berhasil',!E(`klienList().some(k=>k.id===${J(delId)})`));

// --- ACC lalu cek performa ---
const pid=saved.id;
E(`pnwDecide(${J(pid)},'approved')`);
ok('penawaran berstatus approved',E(`penawaran().find(p=>p.id===${J(pid)}).status`)==='approved');

const perf=JSON.parse(E(`JSON.stringify(salesPerforma())`));
const mine=perf.find(p=>p.id===salesId);
ok('salesPerforma menghitung jumlah penawaran',mine.jumlahPenawaran>=1,mine.jumlahPenawaran);
ok('salesPerforma menghitung ACC',mine.jumlahACC>=1,mine.jumlahACC);
ok('salesPerforma menghitung nilai ACC',mine.nilaiACC>=saved.total,mine.nilaiACC);
ok('salesPerforma menghitung komisi',mine.komisi>=saved.komisi,mine.komisi);
ok('salesPerforma menghitung klien unik',mine.klien>=1,mine.klien);
ok('diurutkan dari nilai ACC tertinggi',perf.every((p,i)=>i===0||perf[i-1].nilaiACC>=p.nilaiACC));

// --- UI performa tab ---
E(`go('sales');setSalesTab('performa')`);
const pb=d.getElementById('salesBody').innerHTML;
ok('tab performa tampil tabel sales',pb.includes('Rekap Performa per Sales'));
ok('nama sales muncul di rekap',pb.includes(esc_check(salesName)));
function esc_check(s){return s.replace(/&/g,'&amp;');}
ok('kolom komisi tampil',pb.includes('Komisi'));

// --- dashboard setelah ada data ---
E(`setSalesTab('dashboard')`);
const db=d.getElementById('salesBody').innerHTML;
ok('dashboard tampil penawaran saya',db.includes('Penawaran Saya'));
ok('dashboard tampil klien uji coba',db.includes('SMA Uji Coba Sales'));
ok('status Di-ACC tampil',db.includes('Di-ACC'));

// --- regresi: management kalkulator tetap tak terganggu ---
E(`go('katalog');setKatTab('kalkulator')`);
ok('kalkulator management masih render',!!d.getElementById('q_pax'));
d.getElementById('q_pax').value='50';d.getElementById('q_malam').value='1';
E(`calcQuote()`);
ok('kalkulator management hitung normal (diskon default 0)',E(`lastQuote.diskon`)===0,E(`lastQuote.diskon`));

console.log('\nwindow errors:',(w.__errs||[]).length?w.__errs.join(' | '):'none');
console.log(`\n${fail===0?'✓ SALES TESTS CLEAN':'✗ '+fail+' GAGAL'} — ${pass} pass, ${fail} fail`);
process.exit(fail===0&&(w.__errs||[]).length===0?0:1);
},700);
