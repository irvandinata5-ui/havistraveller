const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};let errs=[];w.onerror=m=>errs.push(m);w.__errs=errs;}});
const w=dom.window,d=w.document;let fail=0;
function ok(c,l){if(c)console.log('  ok  '+l);else{console.log('  ** FAIL '+l);fail++;}}
setTimeout(()=>{
  // all views
  ['dashboard','keuangan','katalog','acc','jadwal','crew','setting'].forEach(v=>{w.go(v);ok(d.getElementById('view').innerHTML.trim().length>50,'view '+v);});
  // keu subtabs
  w.go('keuangan');['Ringkasan','Arus Kas','Aging Piutang','Pelunasan Klien','Jadwal Vendor','Profitabilitas'].forEach(t=>{[...d.querySelectorAll('#view .tabs .tab')].find(x=>x.textContent.trim()===t).onclick();ok(d.getElementById('keuBody').innerHTML.trim().length>50,'keu tab '+t);});
  // katalog subtabs
  w.go('katalog');['Kalkulator Harga','Hotel','Destinasi Wisata','Armada & Kaos'].forEach(t=>{[...d.querySelectorAll('#view .tabs .tab')].find(x=>x.textContent.trim()===t).onclick();ok(d.getElementById('katBody').innerHTML.trim().length>50,'kat tab '+t);});
  // crew subtabs
  w.go('crew');['Daftar Crew','Penugasan Trip'].forEach(t=>{[...d.querySelectorAll('#view .tabs .tab')].find(x=>x.textContent.trim()===t).onclick();ok(d.getElementById('crewBody').innerHTML.trim().length>50,'crew tab '+t);});
  // jadwal filters
  w.go('jadwal');['Akan Datang','Berlangsung','Selesai','Semua'].forEach(t=>{[...d.querySelectorAll('#view .tabs .tab')].find(x=>x.textContent.trim()===t).onclick();ok(!!d.getElementById('jadwalBody'),'jadwal filter '+t);});
  // setting target save
  w.go('setting');d.getElementById('s_target').value='150000000';w.saveMarkup();ok(w.eval("store('target',0)")===150000000,'target saved');
  // end-to-end: penawaran -> acc -> approve -> payment -> crew assign
  w.go('katalog');w.setKatTab('kalkulator');d.getElementById('q_pax').value='300';d.getElementById('q_malam').value='2';d.getElementById('q_tgl').value='2026-12-24';d.getElementById('q_arm').selectedIndex=4;w.calcQuote();
  d.getElementById('q_klien').value='SDN Test E2E';d.getElementById('q_dest').value='Bandung';d.getElementById('q_hp').value='08111';w.saveQuote();
  const pid=w.penawaran()[0].id;w.pnwDecide(pid,'approved');
  ok(w.eval(`allTrips().some(t=>t.id==='${pid}')`),'penawaran -> jadwal');
  ok(w.eval(`allPiutang().some(p=>p.id==='${pid}')`),'penawaran -> piutang');
  w.eval(`addClientPayment('${pid}','DP 1',10000000,'2026-11-16')`);
  ok(w.eval(`clientPaid(allPiutang().find(p=>p.id==='${pid}'))`)===10000000,'payment recorded');
  const tl=w.eval('crewList().find(c=>c.peran==="Tour Leader").id');w.assignCrew(pid,'tl',tl);
  ok(w.eval(`(assignMap()['${pid}']||{}).tl==='${tl}'`),'crew assigned to new trip');
  console.log('  -- window errors:',(w.__errs&&w.__errs.length)?w.__errs.join(' | '):'none');
  console.log(fail?('\n'+fail+' FAILURES'):'\n✓ FULL REGRESSION CLEAN');
},400);
