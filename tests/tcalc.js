const fs=require('fs');const {JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app',
  beforeParse(w){const s={};w.localStorage={getItem:k=>k in s?s[k]:null,setItem:(k,v)=>s[k]=''+v,removeItem:k=>delete s[k]};w.scrollTo=()=>{};w.history.replaceState=()=>{};w.onerror=m=>console.log('ERR',m);}});
const w=dom.window,d=w.document;const bugs=[];
// reference formula from original quotation system
function kap(name){
  const m=String(name||'').match(/(\d+)(?:\s*[–-]\s*(\d+))?\s*SEAT/i);
  if(m)return +(m[2]||m[1]);
  const u=String(name||'').toUpperCase();if(u.includes('ELF'))return 15;if(u.includes('HIACE'))return 14;if(u.includes('MEDIUM'))return 33;if(u.includes('LEGRES'))return 32;return 45;
}
function ref({pax,malam,armRate,armName,share,mFreq,mPrice,kaosRate,hWd,hWe,isWknd,markupPct,dests}){
  const cap=kap(armName);const hotelRate=isWknd?hWe:hWd;const bus=Math.ceil(pax/cap)||0;const hari=malam+1;
  const cT=armRate*bus*hari, cM=mFreq*mPrice*pax, cH=malam>0?hotelRate*malam*Math.ceil(pax/share):0, cK=kaosRate*pax;
  let cW=0;dests.forEach(p=>cW+=p*pax);
  const modal=cT+cM+cH+cW+cK, mk=modal*(1+markupPct/100);
  const foc=Math.min(Math.floor(pax/10),25), subsidi=foc*(pax>0?mk/pax:0);
  const jual=mk-subsidi; return pax>0?Math.ceil((jual/pax)/1000)*1000:0;
}
function setForm({pax,malam,tgl,armIdx,hotelVal,mFreq,mPrice,kaosVal,share,destIdxs=[]}){
  const g=id=>d.getElementById(id);
  g('q_pax').value=pax;g('q_malam').value=malam;g('q_tgl').value=tgl||'';
  g('q_arm').selectedIndex=armIdx;g('q_hotel').value=hotelVal;g('q_mfreq').value=mFreq;g('q_mprice').value=mPrice;g('q_kaos').value=kaosVal;g('q_share').value=share;
  d.querySelectorAll('.qdest').forEach(c=>c.checked=false);
  destIdxs.forEach(i=>{d.querySelectorAll('.qdest')[i].checked=true;});
  w.calcQuote();
  return parseInt(g('q_perpax').textContent.replace(/\D/g,''))||0;
}
function check(label,got,exp){const ok=got===exp;console.log((ok?'  ok  ':'  ** BUG ')+label+'  got '+got.toLocaleString('id-ID')+(ok?'':' != exp '+exp.toLocaleString('id-ID')));if(!ok)bugs.push(label);}
setTimeout(()=>{
  w.go('katalog');w.katTab='kalkulator';w.renderKat();
  const arm=w.eval('CATALOG.armada');
  // helper to get armRate/name by idx
  const A=i=>({armRate:arm[i].rate,armName:arm[i].name});
  // scenario A: default-ish, HIACE idx1, no hotel, no dest, weekday
  let got=setForm({pax:50,malam:1,tgl:'',armIdx:1,hotelVal:'0|0',mFreq:3,mPrice:35000,kaosVal:'0',share:4});
  check('A 50pax HIACE 1mlm noHotel',got,ref({pax:50,malam:1,...A(1),share:4,mFreq:3,mPrice:35000,kaosRate:0,hWd:0,hWe:0,isWknd:false,markupPct:20,dests:[]}));
  // B: big bus(50) idx4, 2 malam, hotel 170000|225900 weekday, kaos 50000, 2 dests
  const dps=[...d.querySelectorAll('.qdest')];const d1=+dps[10].dataset.price,d2=+dps[20].dataset.price;
  got=setForm({pax:120,malam:2,tgl:'2026-12-21',armIdx:4,hotelVal:'170000|225900',mFreq:4,mPrice:40000,kaosVal:'50000',share:4,destIdxs:[10,20]});
  check('B 120pax BigBus weekday+hotel+kaos+2dest',got,ref({pax:120,malam:2,...A(4),share:4,mFreq:4,mPrice:40000,kaosRate:50000,hWd:170000,hWe:225900,isWknd:false,markupPct:20,dests:[d1,d2]}));
  // C: same but weekend date (2026-12-20 Sunday) -> weekend hotel rate
  const wd=new Date('2026-12-20').getDay();console.log('     (2026-12-20 getDay='+wd+' -> weekend='+[0,6].includes(wd)+')');
  got=setForm({pax:120,malam:2,tgl:'2026-12-20',armIdx:4,hotelVal:'170000|225900',mFreq:4,mPrice:40000,kaosVal:'50000',share:4,destIdxs:[10,20]});
  check('C weekend hotel rate applied',got,ref({pax:120,malam:2,...A(4),share:4,mFreq:4,mPrice:40000,kaosRate:50000,hWd:170000,hWe:225900,isWknd:[0,6].includes(wd),markupPct:20,dests:[d1,d2]}));
  // D: pax 0
  got=setForm({pax:0,malam:1,tgl:'',armIdx:1,hotelVal:'0|0',mFreq:3,mPrice:35000,kaosVal:'0',share:4});
  check('D pax=0 -> 0',got,0);
  // E: FOC cap at 25 (300 pax)
  got=setForm({pax:300,malam:1,tgl:'',armIdx:4,hotelVal:'0|0',mFreq:3,mPrice:35000,kaosVal:'0',share:4});
  check('E 300pax FOC cap 25',got,ref({pax:300,malam:1,...A(4),share:4,mFreq:3,mPrice:35000,kaosRate:0,hWd:0,hWe:0,isWknd:false,markupPct:20,dests:[]}));
  // F: markup change to 30% via setting
  w.save('markup',30);w.go('katalog');w.katTab='kalkulator';w.renderKat();
  got=setForm({pax:50,malam:1,tgl:'',armIdx:1,hotelVal:'0|0',mFreq:3,mPrice:35000,kaosVal:'0',share:4});
  check('F markup 30% applied',got,ref({pax:50,malam:1,...A(1),share:4,mFreq:3,mPrice:35000,kaosRate:0,hWd:0,hWe:0,isWknd:false,markupPct:30,dests:[]}));
  w.save('markup',20);
  // G: twin share (2)
  w.go('katalog');w.katTab='kalkulator';w.renderKat();
  got=setForm({pax:40,malam:2,tgl:'2026-12-21',armIdx:0,hotelVal:'300000|400000',mFreq:3,mPrice:35000,kaosVal:'0',share:2});
  check('G twin share hotel calc',got,ref({pax:40,malam:2,...A(0),share:2,mFreq:3,mPrice:35000,kaosRate:0,hWd:300000,hWe:400000,isWknd:false,markupPct:20,dests:[]}));
  console.log(bugs.length?'\n'+bugs.length+' BUG(S): '+bugs.join(', '):'\nKalkulator: semua skenario cocok dengan rumus asli ✓');
},300);
