import json
logo = open('logo_b64.txt').read().strip()
data = open('data.json').read()
catalog = open('catalog.json').read()

html = r'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Havist Traveller — Dashboard Management</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<style>
:root{--blue:#275BB5;--blue-700:#1E4E9C;--navy:#0E244A;--navy-2:#163A6B;--gold:#F8C000;--gold-ink:#7A5E00;
--bg:#EEF1F6;--card:#FFF;--line:#E4E8EF;--ink:#141B2D;--muted:#6B7685;--muted-2:#9AA3B2;
--red:#E0564B;--red-bg:#FDECEA;--green:#2B9D6E;--green-bg:#E7F5EF;--teal:#1AA6B7;--purple:#8E63D6;--orange:#E08A1E;--radius:18px;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Plus Jakarta Sans',system-ui,sans-serif;background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}
.app{display:grid;grid-template-columns:256px 1fr;min-height:100vh}
/* sidebar */
.sidebar{background:linear-gradient(185deg,var(--navy),var(--navy-2));color:#fff;padding:26px 18px;display:flex;flex-direction:column;position:sticky;top:0;height:100vh}
.brand{padding:4px 8px 22px}.brand img{width:100%;max-width:168px;display:block}
.nav{display:flex;flex-direction:column;gap:3px;flex:1;overflow-y:auto}
.nav-label{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:rgba(255,255,255,.4);padding:14px 12px 7px;font-weight:600}
.nav a{display:flex;align-items:center;gap:12px;padding:11px 13px;border-radius:12px;color:rgba(255,255,255,.72);text-decoration:none;font-size:14px;font-weight:500;cursor:pointer;transition:.15s}
.nav a svg{width:19px;height:19px;flex-shrink:0;stroke-width:1.9}
.nav a:hover{background:rgba(255,255,255,.07);color:#fff}
.nav a.active{background:var(--gold);color:var(--navy);font-weight:700;box-shadow:0 6px 16px rgba(248,192,0,.28)}
.side-foot{margin-top:14px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:12px 13px;display:flex;align-items:center;gap:11px}
.side-foot .ava{width:38px;height:38px;border-radius:10px;background:var(--gold);color:var(--navy);display:grid;place-items:center;font-weight:800}
.side-foot .nm{font-size:13px;font-weight:700;line-height:1.2}.side-foot .rl{font-size:11px;color:rgba(255,255,255,.55)}
/* main */
.main{padding:22px 28px 40px;min-width:0}
.topbar{display:flex;align-items:center;gap:18px;margin-bottom:22px}
.search{flex:1;max-width:460px;position:relative}
.search svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);width:18px;height:18px;color:var(--muted-2)}
.search input{width:100%;border:1px solid var(--line);background:#fff;border-radius:12px;padding:11px 14px 11px 42px;font-size:14px;font-family:inherit;color:var(--ink)}
.top-actions{display:flex;align-items:center;gap:12px;margin-left:auto}
.icon-btn{width:42px;height:42px;border-radius:12px;background:#fff;border:1px solid var(--line);display:grid;place-items:center;cursor:pointer;position:relative;color:var(--ink)}
.icon-btn .dot{position:absolute;top:10px;right:11px;width:8px;height:8px;border-radius:50%;background:var(--red);border:2px solid #fff}
.me{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:5px 14px 5px 6px;cursor:pointer}
.me .ava{width:34px;height:34px;border-radius:9px;background:var(--blue);color:#fff;display:grid;place-items:center;font-weight:800}
.me .nm{font-size:13px;font-weight:700;line-height:1.15}.me .rl{font-size:11px;color:var(--muted)}
.hello{margin-bottom:20px}.hello h1{font-size:23px;font-weight:800;letter-spacing:-.01em}.hello p{color:var(--muted);font-size:14px;margin-top:3px}
.grid{display:grid;grid-template-columns:1fr 340px;gap:22px;align-items:start}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:22px}
.scard{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:16px 17px}
.scard .ic{width:40px;height:40px;border-radius:11px;display:grid;place-items:center;margin-bottom:13px}.scard .ic svg{width:20px;height:20px}
.scard .lbl{font-size:12.5px;color:var(--muted);font-weight:600}.scard .val{font-size:22px;font-weight:800;letter-spacing:-.02em;margin-top:3px}
.scard .sub{font-size:11.5px;margin-top:6px;font-weight:600}
.ic.b{background:rgba(39,91,181,.1);color:var(--blue)}.ic.g{background:rgba(248,192,0,.16);color:var(--gold-ink)}
.ic.r{background:var(--red-bg);color:var(--red)}.ic.gr{background:var(--green-bg);color:var(--green)}
.up{color:var(--green)}.down{color:var(--red)}
.panel{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;margin-bottom:22px}
.panel-h{display:flex;align-items:center;justify-content:space-between;padding:17px 19px 0}
.panel-h h3{font-size:15.5px;font-weight:800}.panel-h a,.panel-h .lnk{font-size:12.5px;color:var(--blue);text-decoration:none;font-weight:700;cursor:pointer;background:none;border:none;font-family:inherit}
.tabs{display:flex;gap:4px;padding:14px 19px 0;flex-wrap:wrap}
.tab{padding:7px 15px;border-radius:9px;font-size:13px;font-weight:600;color:var(--muted);cursor:pointer;border:none;background:transparent;font-family:inherit}
.tab.active{background:var(--blue);color:#fff}
.chartwrap{padding:16px 19px 20px}
.chart{display:flex;align-items:flex-end;gap:14px;height:150px;padding-top:10px}
.bar{flex:1;display:flex;flex-direction:column;align-items:center;gap:8px;height:100%;justify-content:flex-end;cursor:pointer}
.bar .col{width:70%;max-width:34px;border-radius:7px 7px 3px 3px;background:linear-gradient(var(--blue),#4C83D8);transition:.2s;position:relative}
.bar.hl .col{background:linear-gradient(var(--gold),#FFD63D)}
.bar:hover .col{filter:brightness(1.08)}.bar span{font-size:11px;color:var(--muted);font-weight:600}
.bar .tip{position:absolute;bottom:105%;left:50%;transform:translateX(-50%);background:var(--navy);color:#fff;font-size:11px;font-weight:700;padding:3px 8px;border-radius:6px;white-space:nowrap;opacity:0;pointer-events:none;transition:.15s}
.bar:hover .tip{opacity:1}
table{width:100%;border-collapse:collapse}
thead th{text-align:left;font-size:11.5px;letter-spacing:.03em;text-transform:uppercase;color:var(--muted-2);font-weight:700;padding:11px 19px;border-bottom:1px solid var(--line)}
tbody td{padding:13px 19px;font-size:13.5px;border-bottom:1px solid var(--line);vertical-align:middle}
tbody tr:last-child td{border-bottom:none}tbody tr.clk{cursor:pointer}tbody tr.clk:hover{background:#F7F9FC}
.trip{display:flex;align-items:center;gap:11px}
.trip .th{width:40px;height:40px;border-radius:10px;display:grid;place-items:center;font-weight:800;font-size:13px;color:#fff;flex-shrink:0}
.trip .nm{font-weight:700;font-size:13.5px}.trip .loc{font-size:11.5px;color:var(--muted)}
.pill{display:inline-flex;align-items:center;gap:5px;font-size:11.5px;font-weight:700;padding:4px 10px;border-radius:20px}
.pill.lunas{background:var(--green-bg);color:var(--green)}.pill.dp{background:rgba(248,192,0,.18);color:var(--gold-ink)}.pill.piutang{background:var(--red-bg);color:var(--red)}.pill.jadwal{background:rgba(39,91,181,.1);color:var(--blue)}
.price{font-weight:800;font-size:13.5px}
.btn-acc{font-size:12px;font-weight:700;padding:6px 13px;border-radius:9px;border:none;cursor:pointer;font-family:inherit}
.btn-acc.ok{background:var(--blue);color:#fff}.btn-acc.no{background:#fff;border:1px solid var(--line);color:var(--muted);margin-left:6px}
.btn-acc:active{transform:scale(.96)}
.side-card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:18px;margin-bottom:22px}
.cal-h{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}.cal-h .mo{font-size:14px;font-weight:800}
.cal-nav{display:flex;gap:6px}.cal-nav button{width:28px;height:28px;border-radius:8px;border:1px solid var(--line);background:#fff;cursor:pointer;color:var(--muted)}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:3px;text-align:center}
.cal .dow{font-size:10.5px;color:var(--muted-2);font-weight:700;padding:5px 0}
.cal .d{font-size:12.5px;padding:7px 0;border-radius:9px;font-weight:600;color:var(--ink);cursor:default}
.cal .d.mut{color:transparent}.cal .d.go{background:var(--gold);color:var(--navy);font-weight:800;cursor:pointer}
.cal .d.today{background:var(--blue);color:#fff}.cal .d.go:hover{filter:brightness(1.05)}
.legend{display:flex;gap:14px;margin-top:13px;font-size:11px;color:var(--muted);font-weight:600}
.legend i{display:inline-block;width:9px;height:9px;border-radius:3px;margin-right:5px;vertical-align:middle}
.bk{display:flex;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid var(--line)}.bk:last-child{border-bottom:none}
.bk .th{width:48px;height:48px;border-radius:11px;display:grid;place-items:center;font-weight:800;color:#fff;flex-shrink:0}
.bk .nm{font-weight:700;font-size:13.5px}.bk .dt{font-size:11.5px;color:var(--muted);margin-top:2px}
.remind{background:linear-gradient(135deg,var(--blue),var(--blue-700));border-radius:var(--radius);padding:18px;color:#fff}
.remind h4{font-size:14.5px;font-weight:800;margin-bottom:4px}.remind p{font-size:12.5px;color:rgba(255,255,255,.82);line-height:1.5}
.remind .r-item{display:flex;align-items:center;gap:9px;background:rgba(255,255,255,.1);border-radius:11px;padding:10px 12px;margin-top:10px;font-size:12.5px;font-weight:600}
.remind .r-item .n{margin-left:auto;background:var(--gold);color:var(--navy);font-weight:800;border-radius:7px;padding:1px 8px;font-size:12px}
.catrow{display:flex;align-items:center;gap:10px;margin-bottom:10px}.catnm{font-size:12px;font-weight:600;width:118px;flex-shrink:0}
.catbar{flex:1;height:8px;background:#EEF1F6;border-radius:6px;overflow:hidden}.catfill{height:100%;border-radius:6px}
.catval{font-size:11.5px;font-weight:700;color:var(--muted);width:66px;text-align:right;flex-shrink:0}
.kat{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.kat-card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;cursor:pointer;transition:.15s}
.kat-card:hover{border-color:var(--blue);box-shadow:0 8px 20px rgba(39,91,181,.08);transform:translateY(-2px)}
.kat-card .dn{font-size:11px;color:var(--gold-ink);background:rgba(248,192,0,.16);display:inline-block;padding:2px 9px;border-radius:7px;font-weight:700;margin-bottom:9px}
.kat-card h4{font-size:14.5px;font-weight:800;margin-bottom:5px}.kat-card .meta{font-size:12px;color:var(--muted);line-height:1.6}
.empty{background:var(--card);border:1px dashed var(--line);border-radius:var(--radius);padding:50px 24px;text-align:center;color:var(--muted)}
.empty svg{width:40px;height:40px;color:var(--muted-2);margin-bottom:14px}.empty h3{font-size:16px;color:var(--ink);margin-bottom:6px}.empty p{font-size:13px;max-width:380px;margin:0 auto}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(120px);background:var(--navy);color:#fff;padding:12px 20px;border-radius:12px;font-size:13.5px;font-weight:600;box-shadow:0 12px 30px rgba(0,0,0,.25);transition:.3s;z-index:99;display:flex;align-items:center;gap:9px}
.toast.show{transform:translateX(-50%) translateY(0)}
.toast svg{width:18px;height:18px;color:var(--gold)}
.fade{animation:fade .25s ease}@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.mono{font-variant-numeric:tabular-nums}
.finput{width:100%;border:1px solid var(--line);background:#fff;border-radius:10px;padding:10px 12px;font-size:14px;font-family:inherit;color:var(--ink);margin:5px 0 14px}
.finput:focus{outline:none;border-color:var(--blue)}
.flbl{font-size:12px;font-weight:600;color:var(--muted);display:block;margin-bottom:0}
.btn-save{background:var(--blue);color:#fff;border:none;border-radius:10px;padding:11px 18px;font-size:13.5px;font-weight:700;font-family:inherit;cursor:pointer;width:100%;margin-top:6px}
.btn-save:active{transform:scale(.98)}
.chk{display:flex;align-items:center;gap:10px;font-size:13.5px;font-weight:500;padding:9px 0;cursor:pointer}
.chk input{width:17px;height:17px;accent-color:var(--blue);cursor:pointer}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.calc-wrap{display:grid;grid-template-columns:1fr 360px;gap:22px;align-items:start}
.result-card{background:linear-gradient(160deg,var(--navy),var(--navy-2));color:#fff;border-radius:var(--radius);padding:22px;position:sticky;top:20px}
.rc-label{font-size:12.5px;color:rgba(255,255,255,.65);font-weight:600}
.rc-price{font-size:34px;font-weight:800;letter-spacing:-.02em;margin:4px 0 6px;color:var(--gold)}
.rc-dur{font-size:12px;color:rgba(255,255,255,.7);line-height:1.5;font-weight:600}
.rc-toggle{margin-top:16px;background:rgba(255,255,255,.12);border:none;color:#fff;font-family:inherit;font-size:12px;font-weight:700;padding:7px 13px;border-radius:9px;cursor:pointer}
.rc-secret{display:none;margin-top:12px;padding-top:12px;border-top:1px solid rgba(255,255,255,.14)}
.rc-secret.show{display:block}
.rc-row{display:flex;justify-content:space-between;font-size:12.5px;padding:4px 0;color:rgba(255,255,255,.8)}
.rc-row b{color:#fff;font-variant-numeric:tabular-nums}.rc-row.warn b{color:var(--gold)}.rc-row.tot{border-top:1px solid rgba(255,255,255,.16);margin-top:5px;padding-top:7px;font-weight:700}
.rc-break{margin-top:14px;padding-top:12px;border-top:1px solid rgba(255,255,255,.14)}
.bk-h{font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:rgba(255,255,255,.5);font-weight:700;margin-bottom:6px}
.note-card{background:rgba(248,192,0,.12);border:1px solid rgba(248,192,0,.3);border-radius:14px;padding:13px 15px;font-size:12px;color:var(--gold-ink);margin-top:16px;font-weight:600;line-height:1.5}
.save-box{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:16px 17px;margin-top:16px}
.save-box .sb-h{font-size:14px;font-weight:800;color:var(--ink);margin-bottom:4px}
.btn-wa{display:inline-block;background:#25D366;color:#fff;font-size:12px;font-weight:700;padding:6px 12px;border-radius:9px;text-decoration:none;margin-right:6px}
.pv-overlay{position:fixed;inset:0;background:rgba(10,20,40,.55);z-index:200;display:flex;align-items:flex-start;justify-content:center;padding:24px;overflow:auto}
.pv-modal{background:var(--bg);border-radius:16px;max-width:720px;width:100%;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.4)}
.pv-bar{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;background:var(--navy);color:#fff}
.pv-bar b{font-size:15px}.pv-bar .btn-acc{margin-left:6px}
.pv-paper{background:#fff;margin:18px;border-radius:8px;padding:34px 38px;font-size:13px;color:#222;line-height:1.6}
.pv-letterhead{border-bottom:2px solid var(--navy);padding-bottom:12px;margin-bottom:16px}
.pv-brand{font-size:22px;font-weight:800;color:var(--navy);letter-spacing:.02em}
.pv-tag{font-size:11px;font-style:italic;color:var(--gold-ink);font-weight:600}
.pv-contact{font-size:10.5px;color:var(--muted);margin-top:6px;line-height:1.5}
.pv-title{text-align:center;font-size:16px;color:var(--navy);margin:14px 0 10px;letter-spacing:.03em}
.pv-meta{font-size:11.5px;color:var(--muted);margin-bottom:12px}.pv-meta td{padding-right:10px}
.pv-to{margin:10px 0}.pv-sum{margin:10px 0;font-size:12.5px}.pv-sum td{padding:2px 0;vertical-align:top}.pv-sum td:first-child{width:150px;color:var(--muted)}
.pv-price{display:flex;justify-content:space-between;align-items:center;background:#F5F7FA;border-radius:8px;padding:10px 14px;margin:6px 0;font-size:13px}
.pv-price b{font-size:18px;color:var(--navy)}.pv-price.sub{padding:7px 14px;font-size:12px}.pv-price.sub b{font-size:13px;color:var(--muted)}
.pv-h3{font-size:13px;color:var(--navy);margin:16px 0 7px;border-bottom:1px solid var(--line);padding-bottom:4px}
.pv-fasil{margin:0 0 4px 18px;font-size:12.5px}.pv-fasil li{margin:3px 0}
.pv-itin{display:flex;flex-direction:column;gap:8px}
.pv-day{background:#F7F9FC;border-left:3px solid var(--gold);border-radius:6px;padding:9px 13px}
.pv-day-h{font-weight:800;color:var(--gold-ink);font-size:12.5px;margin-bottom:3px}
.pv-day ul{margin:0 0 0 16px;font-size:12px}.pv-day li{margin:2px 0}
.pv-close{margin-top:14px}.pv-sign{margin-top:16px;font-size:12.5px}
.pay-sum{display:flex;justify-content:space-between;gap:10px;margin-bottom:12px}
.pay-sum div{flex:1;background:#F5F7FA;border-radius:9px;padding:9px 11px;text-align:center}
.pay-sum span{display:block;font-size:10.5px;color:var(--muted);font-weight:600}.pay-sum b{font-size:14px}
.pay-hist{max-height:150px;overflow:auto}
.pay-row{display:flex;align-items:center;justify-content:space-between;font-size:12.5px;padding:6px 0;border-bottom:1px solid var(--line)}
.pay-row:last-child{border-bottom:none}.pay-row span{color:var(--muted)}
.pay-del{background:none;border:none;color:var(--red);cursor:pointer;font-size:13px;margin-left:8px;padding:0 4px}
.jgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}
.jcard{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;cursor:pointer;transition:.15s}
.jcard:hover{border-color:var(--blue);box-shadow:0 8px 22px rgba(39,91,181,.1);transform:translateY(-2px)}
.jcard-top{display:flex;gap:6px;margin-bottom:10px}
.jcard h4{font-size:15px;font-weight:800;margin-bottom:2px;line-height:1.25}
.jcard-dest{font-size:12.5px;color:var(--muted);margin-bottom:11px}
.jcard-meta{display:flex;flex-wrap:wrap;gap:10px;font-size:12px;color:var(--ink);font-weight:600;margin-bottom:11px}
.jcard-crew{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:11px}
.crew-chip{font-size:11px;font-weight:700;color:#fff;padding:3px 9px;border-radius:7px}
.crew-chip.empty{background:#EEF1F6;color:var(--muted-2)}
.jcard-foot{border-top:1px solid var(--line);padding-top:10px;display:flex;align-items:center;justify-content:space-between;gap:8px}
.td-card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 15px;margin-bottom:12px}
.td-card h5{font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted-2);font-weight:700;margin-bottom:9px}
/* ===== Area Umum — Landing Page ===== */
.umhero{background:linear-gradient(145deg,var(--navy),var(--navy-2) 55%,var(--teal));border-radius:24px;padding:48px 40px;color:#fff;position:relative;overflow:hidden;margin-bottom:28px}
.umhero::after{content:'';position:absolute;inset:0;background:radial-gradient(circle at 85% 20%,rgba(248,192,0,.18),transparent 55%);pointer-events:none}
.umhero-tag{display:inline-block;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:30px;padding:6px 16px;font-size:12px;font-weight:700;letter-spacing:.04em;margin-bottom:18px;position:relative;z-index:1}
.umhero h1{font-size:38px;font-weight:800;line-height:1.14;letter-spacing:-.02em;margin-bottom:14px;max-width:640px;position:relative;z-index:1}
.umhero h1 em{font-style:normal;color:var(--gold)}
.umhero p{font-size:14.5px;color:rgba(255,255,255,.78);max-width:520px;margin-bottom:24px;line-height:1.6;position:relative;z-index:1}
.umhero-search{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.22);border-radius:12px;padding:5px 5px 5px 14px;max-width:460px;margin-bottom:16px;position:relative;z-index:1}
.umhero-search svg{width:17px;height:17px;color:rgba(255,255,255,.6);flex-shrink:0}
.umhero-search input{flex:1;background:transparent;border:none;color:#fff;font-size:13.5px;font-family:inherit;min-width:0}
.umhero-search input::placeholder{color:rgba(255,255,255,.55)}
.umhero-search input:focus{outline:none}
.umhero-search button{background:var(--gold);color:var(--navy);font-weight:800;border:none;border-radius:8px;padding:9px 16px;font-size:12.5px;cursor:pointer;white-space:nowrap}
.umhero-cta{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:32px;position:relative;z-index:1}
.btn-um-primary{background:var(--gold);color:var(--navy);font-weight:800;padding:13px 22px;border-radius:12px;text-decoration:none;display:inline-flex;align-items:center;gap:8px;border:none;cursor:pointer;font-size:13.5px}
.btn-um-ghost{background:rgba(255,255,255,.08);color:#fff;font-weight:700;padding:13px 22px;border-radius:12px;border:1px solid rgba(255,255,255,.28);cursor:pointer;font-size:13.5px}
.umstats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;position:relative;z-index:1}
.umstat{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:15px}
.umstat .n{font-size:22px;font-weight:800}
.umstat .l{font-size:11px;color:rgba(255,255,255,.65);margin-top:2px}
.umsec-head{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:16px}
.umsec-head .tag{color:var(--blue);font-size:11.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;display:block;margin-bottom:3px}
.umsec-head h2{font-size:19px;font-weight:800}
.umwhy{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:30px}
.umwhy-card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px}
.umtrust{display:flex;align-items:center;justify-content:center;gap:10px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 20px;margin-bottom:30px;text-align:center;flex-wrap:wrap}
.umtrust svg{width:22px;height:22px;color:var(--blue);flex-shrink:0}
.umtrust p{font-size:13.5px;color:var(--ink)}
.umtrust b{color:var(--blue)}
.umfaq{margin-bottom:30px;max-width:780px}
.umfaq-item{background:var(--card);border:1px solid var(--line);border-radius:14px;margin-bottom:10px;overflow:hidden}
.umfaq-q{width:100%;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px 18px;background:none;border:none;cursor:pointer;text-align:left;font-family:inherit;font-size:14px;font-weight:700;color:var(--ink)}
.umfaq-q svg{width:18px;height:18px;flex-shrink:0;color:var(--muted);transition:transform .18s}
.umfaq-item.open .umfaq-q svg{transform:rotate(180deg);color:var(--blue)}
.umfaq-a{max-height:0;overflow:hidden;transition:max-height .22s ease}
.umfaq-a p{padding:0 18px 16px;font-size:13px;color:var(--muted);line-height:1.6}
.umfaq-item.open .umfaq-a{max-height:220px}
.umwhy-card .ic{width:44px;height:44px;border-radius:12px;background:var(--blue);color:#fff;display:grid;place-items:center;margin-bottom:14px}
.umwhy-card .ic svg{width:21px;height:21px}
.umwhy-card h4{font-size:14.5px;margin-bottom:6px}
.umwhy-card p{font-size:12.5px;color:var(--muted);line-height:1.55}
.umfeat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:30px}
.umfeat-card{border-radius:16px;overflow:hidden;position:relative;height:148px;display:flex;align-items:flex-end;padding:14px;color:#fff;background-size:cover;background-position:center}
.umfeat-card .ov{position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.55),rgba(0,0,0,.05))}
.umfeat-card .cnt{position:relative;z-index:1}
.umfeat-card .cnt b{display:block;font-size:13.5px;font-weight:800}
.umfeat-card .cnt span{font-size:11px;opacity:.85}
.umcta{background:linear-gradient(125deg,var(--navy),var(--navy-2));border-radius:20px;padding:28px 30px;color:#fff;display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap}
/* pencarian destinasi (Area Umum) */
.um-searchbar{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:18px}
.um-search{position:relative;flex:1;min-width:240px;max-width:460px}
.um-search svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);width:18px;height:18px;color:var(--muted-2)}
.um-search input{width:100%;border:1px solid var(--line);background:#fff;border-radius:12px;padding:11px 14px 11px 42px;font-size:14px;font-family:inherit;color:var(--ink)}
.um-search input:focus{outline:2px solid var(--blue);outline-offset:1px}
.um-search-count{font-size:13px;font-weight:700;color:var(--blue);white-space:nowrap}
@media(max-width:600px){.um-searchbar{flex-direction:column;align-items:stretch}.um-search{max-width:none}.um-search-count{text-align:left}}
/* ===== Testimoni — gaya "Blaze" (3 kolom: stat/CTA, foto+kutipan, marquee) ===== */
.umt-wrap{margin-bottom:30px}
.umt-head{display:flex;flex-direction:column;gap:14px;justify-content:space-between;align-items:flex-start;margin-bottom:26px}
.umt-tagrow{display:flex;align-items:center;gap:7px;margin-bottom:14px}
.umt-badge{width:36px;height:36px;border-radius:50%;border:1px solid var(--line);display:grid;place-items:center;background:#fff;flex-shrink:0}
.umt-badge svg{width:15px;height:15px;color:var(--blue);animation:um-spin 6s linear infinite}
.umt-pill{padding:8px 15px;border-radius:30px;border:1px solid var(--line);background:#fff;font-size:12.5px;font-weight:700;color:var(--ink)}
.umt-head h2{font-size:26px;font-weight:800;line-height:1.18;letter-spacing:-.01em;max-width:480px;color:var(--ink)}
.umt-head h2 span{color:var(--blue)}
.umt-sub{max-width:280px;font-size:12.5px;color:var(--muted);line-height:1.6}
.umt-grid{display:grid;grid-template-columns:1fr;gap:16px;align-items:stretch}
.umt-card-stat{display:flex;flex-direction:column;background:var(--bg);border:1px solid var(--line);border-radius:26px;padding:26px;min-height:360px}
.umt-rating-row{display:flex;align-items:flex-start;gap:10px;margin-bottom:20px}
.umt-rating-n{font-size:32px;font-weight:800;color:var(--ink);line-height:1}
.umt-rating-txt{font-size:12px;color:var(--muted);line-height:1.3;padding-top:4px}
.umt-feat{display:flex;flex-direction:column;gap:11px;margin-bottom:22px}
.umt-feat-row{display:flex;align-items:center;gap:9px;font-size:12.5px;color:var(--ink);font-weight:600}
.umt-feat-row svg{width:15px;height:15px;color:var(--muted);flex-shrink:0}
.umt-cta-block{margin-top:auto;padding-top:16px;border-top:1px solid var(--line)}
.umt-cta-block .lbl1{font-size:12px;color:var(--muted);margin-bottom:2px}
.umt-cta-block .lbl2{font-size:14px;font-weight:800;color:var(--ink);margin-bottom:13px}
.umt-cta-row{display:flex;align-items:center;gap:8px}
.umt-cta-btn{padding:11px 20px;background:var(--navy);color:#fff;font-weight:700;font-size:13px;border-radius:30px;border:none;cursor:pointer;white-space:nowrap}
.umt-cta-arrow{width:40px;height:40px;border-radius:50%;background:var(--gold);color:var(--navy);display:grid;place-items:center;border:none;cursor:pointer;flex-shrink:0}
.umt-cta-arrow svg{width:17px;height:17px}
.umt-card-photo{position:relative;border-radius:26px;overflow:hidden;min-height:360px;background-size:cover;background-position:center}
.umt-card-photo .ov{position:absolute;left:0;right:0;bottom:0;height:62%;background:linear-gradient(0deg,rgba(14,36,74,.92),rgba(14,36,74,.15) 70%,transparent)}
.umt-card-photo .cap{position:absolute;left:22px;right:22px;bottom:22px;color:#fff}
.umt-card-photo .cap .q{font-size:14.5px;font-weight:600;line-height:1.45;margin-bottom:9px}
.umt-card-photo .cap .a{font-size:11.5px;color:rgba(255,255,255,.75)}
.umt-marquee{position:relative;overflow:hidden;border-radius:26px;border:1px solid var(--line);background:var(--bg);min-height:360px;max-height:360px}
.umt-track{display:flex;flex-direction:column;gap:10px;padding:10px;animation:um-marquee 26s linear infinite}
.umt-marquee:hover .umt-track{animation-play-state:paused}
.umt-mcard{background:#fff;border:1px solid var(--line);border-radius:18px;padding:14px;flex-shrink:0}
.umt-mcard .plat{display:inline-flex;align-items:center;gap:6px;font-size:10.5px;font-weight:700;color:var(--muted);margin-bottom:7px}
.umt-mcard .q{font-size:12px;color:var(--ink);line-height:1.5;margin-bottom:10px}
.umt-mcard .who{display:flex;align-items:center;gap:8px}
.umt-mcard .ava{width:26px;height:26px;border-radius:50%;background:var(--line);color:var(--muted);display:grid;place-items:center;font-size:10.5px;font-weight:700;background-size:cover;background-position:center;flex-shrink:0}
.umt-mcard .who b{font-size:11.5px;color:var(--ink);display:block}
.umt-mcard .who span{font-size:11px;color:var(--muted-2)}
@keyframes um-spin{to{transform:rotate(360deg)}}
@keyframes um-marquee{0%{transform:translateY(0)}100%{transform:translateY(-50%)}}
@media(min-width:900px){.umt-head{flex-direction:row;align-items:flex-end}.umt-sub{text-align:right}.umt-grid{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1180px){.umt-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:1100px){.umstats{grid-template-columns:repeat(2,1fr)}.umwhy{grid-template-columns:1fr}.umfeat-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:720px){.umhero{padding:30px 22px}.umhero h1{font-size:26px}.umstats{grid-template-columns:repeat(2,1fr)}.umcta{flex-direction:column;align-items:flex-start}.umhero-search{flex-wrap:wrap;padding:10px 12px}.umhero-search input{flex-basis:100%;order:1;margin:4px 0}.umhero-search button{margin-left:auto;order:2}}
.td-row{display:flex;justify-content:space-between;font-size:13px;padding:4px 0}
.td-row span{color:var(--muted)}.td-row b{text-align:right}
.ds-row{display:flex;justify-content:space-between;align-items:center;font-size:13px;padding:9px 0;border-bottom:1px solid var(--line);cursor:pointer}
.ds-row:last-child{border-bottom:none}.ds-row span{color:var(--muted)}.ds-row b{font-variant-numeric:tabular-nums}
.ds-row:hover span{color:var(--blue)}
.tl{position:relative;padding-left:4px}
.tl-item{display:flex;gap:11px;padding:7px 0;position:relative}
.tl-item:not(:last-child)::before{content:'';position:absolute;left:5px;top:22px;bottom:-4px;width:2px;background:var(--line)}
.tl-dot{width:12px;height:12px;border-radius:50%;flex-shrink:0;margin-top:4px;border:2px solid #fff;box-shadow:0 0 0 1.5px var(--line)}
.tl-body{flex:1;min-width:0}
.tl-top{display:flex;justify-content:space-between;align-items:baseline;gap:8px;font-size:12.5px}
.tl-date{font-size:11.5px;color:var(--muted);white-space:nowrap}
.tl-body p{font-size:11.5px;color:var(--muted);margin-top:1px;line-height:1.4}
.tl-item.done .tl-body b{color:var(--muted-2)}
.pp-row{display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid var(--line)}
.pp-row:last-child{border-bottom:none}
.pp-main{flex:1;min-width:0}
.pp-nm{font-weight:700;font-size:13px;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pp-sub{font-size:11px;color:var(--muted);margin-top:1px}
.pp-num{text-align:right;white-space:nowrap}
.pp-num b{display:block;font-size:13px;font-variant-numeric:tabular-nums}
.pp-num span{font-size:10.5px}
.pp-act{display:flex;align-items:center;gap:5px;flex-shrink:0}
.cat-bar{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:14px;padding:10px 0}
.cat-bar .btn-save{display:inline-block}
.destwrap{display:flex;flex-direction:column;gap:8px;margin-top:5px}
.citybox{border:1px solid var(--line);border-radius:12px;overflow:hidden}
.citybox.has{border-color:var(--blue)}
.cityhd{display:flex;justify-content:space-between;align-items:center;padding:11px 14px;cursor:pointer;font-weight:700;font-size:13.5px;background:#F7F9FC}
.citybox.has .cityhd{background:rgba(39,91,181,.08);color:var(--blue)}
.cityhd .cnt{background:var(--muted-2);color:#fff;font-size:11px;border-radius:20px;padding:1px 8px;font-weight:700}
.citybox.has .cityhd .cnt{background:var(--blue)}
.citygrid{display:none;grid-template-columns:1fr 1fr;gap:2px 16px;padding:10px 14px}
.citybox.open .citygrid{display:grid}
.dest-item{display:flex;align-items:flex-start;gap:9px;padding:7px 0;font-size:12.5px;cursor:pointer;border-bottom:1px solid #F0F3F7}
.dest-item input{margin-top:2px;width:16px;height:16px;accent-color:var(--blue);flex-shrink:0;cursor:pointer}
.dest-item span{line-height:1.35}.dest-item em{color:var(--blue);font-style:normal;font-weight:700;font-size:11.5px;margin-left:4px}
.dest-item .opt{display:block;color:var(--muted-2);font-size:11px;font-weight:500}
@media(max-width:1100px){.calc-wrap{grid-template-columns:1fr}.result-card{position:static}.citygrid{grid-template-columns:1fr}}
@media(max-width:1100px){.grid{grid-template-columns:1fr}.cards{grid-template-columns:repeat(2,1fr)}.kat{grid-template-columns:1fr 1fr}}
@media(max-width:720px){.app{grid-template-columns:1fr}.sidebar{display:none}.cards{grid-template-columns:1fr 1fr}.kat{grid-template-columns:1fr}.main{padding-bottom:90px}}
/* bottom nav (mobile) */
.bottomnav{display:none}
@media(max-width:720px){
  .bottomnav{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:150;background:linear-gradient(185deg,var(--navy),var(--navy-2));
    padding:6px 4px calc(6px + env(safe-area-inset-bottom,0px));box-shadow:0 -8px 24px rgba(0,0,0,.18)}
  .bottomnav a{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;padding:7px 2px;border-radius:12px;color:rgba(255,255,255,.62);text-decoration:none;font-size:10.5px;font-weight:600;cursor:pointer}
  .bottomnav a svg{width:21px;height:21px;stroke-width:1.9}
  .bottomnav a.active{color:var(--gold)}
  .bottomnav a.more svg{width:21px;height:21px}
}
.sheet-overlay{position:fixed;inset:0;background:rgba(10,20,40,.55);z-index:220;display:flex;align-items:flex-end;justify-content:center}
.sheet-modal{background:var(--bg);width:100%;max-width:560px;border-radius:20px 20px 0 0;padding:10px 10px calc(14px + env(safe-area-inset-bottom,0px));box-shadow:0 -12px 40px rgba(0,0,0,.35);max-height:80vh;overflow:auto}
.sheet-handle{width:40px;height:4px;background:var(--line);border-radius:4px;margin:4px auto 10px}
.sheet-title{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted-2);font-weight:700;padding:4px 12px 8px}
.sheet-modal a{display:flex;align-items:center;gap:13px;padding:13px 12px;border-radius:12px;color:var(--ink);text-decoration:none;font-size:14.5px;font-weight:600;cursor:pointer}
.sheet-modal a:active{background:var(--line)}
.sheet-modal a svg{width:20px;height:20px;stroke-width:1.9;color:var(--blue);flex-shrink:0}
/* pagination */
.pager{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:14px;padding-top:12px;border-top:1px solid var(--line)}
.pg-info{font-size:12px;color:var(--muted)}
.pg-nav{display:flex;align-items:center;gap:4px}
.pg-btn{min-width:32px;height:32px;padding:0 8px;border-radius:8px;border:1px solid var(--line);background:#fff;color:var(--ink);font-size:12.5px;font-weight:600;cursor:pointer}
.pg-btn:hover{background:var(--bg)}
.pg-btn.active{background:var(--blue);color:#fff;border-color:var(--blue)}
.pg-btn:disabled{opacity:.4;cursor:not-allowed}
.pg-dots{padding:0 4px;color:var(--muted-2);font-size:12.5px}
@media(max-width:480px){.pg-nav .pg-num{display:none}.pg-info{width:100%;text-align:center;order:3}}
.app.public-mode{display:block!important;grid-template-columns:1fr!important;background:#f4f7fb!important}
.app.public-mode .sidebar,.app.public-mode .sb,.app.public-mode .topbar,.app.public-mode .bottomnav{display:none!important}
.app.public-mode .main{margin:0!important;padding:0 0 56px!important;max-width:none!important;width:100%!important;background:transparent}
.um-topnav{position:fixed;top:0;left:0;right:0;z-index:50;background:rgba(14,36,74,.48);-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);border-bottom:1px solid rgba(255,255,255,.18);padding:11px 40px;display:flex;align-items:center;justify-content:space-between;gap:18px}
.um-tbrand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:15.5px;color:#fff;cursor:pointer;white-space:nowrap;flex-shrink:0}
.um-tbrand img{height:38px;width:auto;object-fit:contain;border-radius:6px}
.um-tlinks{display:flex;align-items:center;gap:4px;flex-wrap:nowrap;overflow-x:auto}
.um-tlinks a{padding:7px 13px;border-radius:10px;font-size:13.5px;font-weight:600;color:rgba(255,255,255,.94);text-decoration:none;cursor:pointer;transition:.15s;white-space:nowrap}
.um-tlinks a:hover{background:rgba(255,255,255,.18);color:#fff}
.app.public-mode .umhero{width:100%;border-radius:0!important;padding:104px 40px 118px!important;text-align:center;display:flex;flex-direction:column;align-items:center;margin-bottom:0!important;box-shadow:none!important}
.app.public-mode .umhero h1{max-width:780px;font-size:clamp(30px,3.6vw,44px)!important;font-weight:800;letter-spacing:-0.025em;line-height:1.15;margin:0 auto 14px}
.app.public-mode .umhero p{max-width:580px;font-size:clamp(14.5px,1.25vw,16.5px)!important;line-height:1.6;color:rgba(255,255,255,.88)!important;margin:0 auto 24px;text-align:center}
.app.public-mode .umhero-search{max-width:640px;width:100%;margin:0 auto 18px!important;background:rgba(255,255,255,.20)!important;-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);border:1px solid rgba(255,255,255,.38)!important;box-shadow:0 12px 36px rgba(15,23,42,.22);border-radius:99px!important;padding:6px 6px 6px 18px!important}
.app.public-mode .umhero-search input{color:#fff!important}
.app.public-mode .umhero-search input::placeholder{color:rgba(255,255,255,.86)!important}
.app.public-mode .umhero-search svg{color:#fff!important}
.app.public-mode .umhero-search button{border-radius:99px!important;padding:10px 20px!important}
.app.public-mode .umhero-cta{justify-content:center}
.app.public-mode .umstats{max-width:960px;width:100%;margin:22px auto 0!important}
.app.public-mode .umstat,.app.public-mode .btn-um-ghost{background:rgba(255,255,255,.16)!important;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.28)!important}
.um-strip-wrap{max-width:1200px;margin:-74px auto 28px;padding:0 32px;position:relative;z-index:10}
.um-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.um-strip-card{background:rgba(255,255,255,.84);-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);border:1px solid rgba(255,255,255,.92);border-radius:18px;overflow:hidden;box-shadow:0 16px 38px rgba(15,23,42,.12);cursor:pointer;transition:transform .18s,box-shadow .18s}
.um-strip-card:hover{transform:translateY(-4px);box-shadow:0 22px 44px rgba(15,23,42,.16)}
.um-strip-img{height:126px;position:relative;background-size:cover;background-position:center;display:flex;align-items:flex-end;padding:10px 12px}
.um-strip-img::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,transparent 35%,rgba(14,36,74,.65))}
.um-strip-img span{position:relative;z-index:1;background:rgba(255,255,255,.92);color:var(--navy);font-size:11px;font-weight:800;padding:3px 9px;border-radius:99px}
.um-strip-body{padding:12px 14px}
.um-strip-body b{display:block;font-size:14px;color:var(--navy);margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.um-strip-body .sub{font-size:12px;color:var(--muted)}
.um-strip-body .prc{margin-top:8px;font-size:13.5px;font-weight:800;color:var(--blue)}
.um-container{max-width:1200px;margin:0 auto;padding:0 32px}
.app.public-mode .umwhy-card,.app.public-mode .umt-mcard{background:rgba(255,255,255,.86)!important;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.92)!important;box-shadow:0 10px 30px rgba(15,23,42,.06)}
.app.public-mode .umfeat-card .cnt{background:linear-gradient(180deg,transparent,rgba(14,36,74,.52));-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);border-top:1px solid rgba(255,255,255,.2)}
.umfeat-card{cursor:pointer;transition:transform .18s,box-shadow .18s}.umfeat-card:hover{transform:translateY(-3px);box-shadow:0 12px 24px rgba(15,23,42,.15)}
.umfeat-badge{position:absolute;top:12px;right:12px;z-index:2;background:rgba(255,255,255,.92);color:var(--navy);font-size:11px;font-weight:800;padding:4px 9px;border-radius:99px}
.um-wa-float{position:fixed;right:24px;bottom:24px;z-index:45;background:#16a34a;color:#fff;padding:12px 20px;border-radius:99px;font-weight:800;font-size:13.5px;text-decoration:none;box-shadow:0 12px 28px rgba(22,163,74,.38);display:none;align-items:center;gap:8px;transition:transform .15s}
.um-wa-float:hover{transform:translateY(-2px)}
.app.public-mode .um-wa-float{display:inline-flex}
@media(max-width:960px){
  .um-topnav{padding:8px 14px!important;flex-wrap:wrap;gap:6px 10px}
  .um-tlinks{order:3;width:100%;display:flex!important;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;gap:4px;padding-top:4px;border-top:1px solid rgba(255,255,255,.12)}
  .um-tlinks::-webkit-scrollbar{display:none}
  .um-tlinks a{font-size:12px;padding:5px 10px;border-radius:8px}
  .app.public-mode .umhero{padding:112px 18px 96px!important}
  .um-strip-wrap,.um-container{padding:0 16px}
  .um-strip{grid-template-columns:1fr 1fr}
}

.tbl-scroll{width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch}
.tbl-scroll table{width:100%;min-width:520px}
@media(max-width:960px){
  .app{grid-template-columns:1fr!important}
  .sidebar{display:none!important}
  .main{padding:16px 14px 96px!important;width:100%!important;max-width:100vw!important;overflow-x:hidden}
  .grid{grid-template-columns:1fr!important;gap:16px!important}
  .calc-wrap{grid-template-columns:1fr!important;gap:16px!important}
  .result-card{position:static!important}
  .cards{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:10px!important;margin-bottom:16px!important}
  .kat{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:10px!important}
  .bottomnav:empty,.app.public-mode ~ .bottomnav{display:none!important}
  .bottomnav{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:150;background:linear-gradient(185deg,var(--navy),var(--navy-2));padding:6px 4px calc(6px + env(safe-area-inset-bottom,0px));box-shadow:0 -8px 24px rgba(0,0,0,.18)}
}
@media(max-width:680px){
  html,body{overflow-x:hidden;width:100%}
  .topbar{gap:8px;margin-bottom:14px}
  .search{max-width:none}
  .search input{padding:9px 10px 9px 34px;font-size:13px;border-radius:10px}
  .search svg{left:11px;width:15px;height:15px}
  .top-actions{gap:6px}
  .icon-btn{width:36px;height:36px;border-radius:10px;flex-shrink:0}
  .me{padding:4px 10px 4px 5px;gap:7px;border-radius:10px}
  .me .ava{width:28px;height:28px;font-size:12px;border-radius:7px}
  .me .nm{font-size:12px;max-width:88px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .me .rl{display:none}
  .hello{margin-bottom:14px}
  .hello h1{font-size:19px;line-height:1.25}
  .hello p{font-size:12.5px;line-height:1.45}
  .scard{padding:12px 13px;border-radius:14px;min-width:0}
  .scard .ic{width:34px;height:34px;border-radius:9px;margin-bottom:8px}
  .scard .ic svg{width:17px;height:17px}
  .scard .lbl{font-size:11.5px;line-height:1.25}
  .scard .val{font-size:16.5px;line-height:1.2;word-break:break-word}
  .scard .sub{font-size:10.5px;margin-top:4px;line-height:1.3}
  .panel{border-radius:14px;margin-bottom:16px}
  .panel-h{padding:14px 14px 0;flex-wrap:wrap;gap:6px}
  .panel-h h3{font-size:14.5px}
  .tabs{flex-wrap:nowrap!important;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding:10px 14px 4px;gap:6px}
  .tabs::-webkit-scrollbar{display:none}
  .tab{white-space:nowrap;flex-shrink:0;padding:7px 12px;font-size:12.5px}
  thead th{padding:9px 12px;font-size:10.5px;white-space:nowrap}
  tbody td{padding:10px 12px;font-size:12.5px}
  .frow{grid-template-columns:1fr!important;gap:6px!important}
  .finput{font-size:13.5px;padding:9px 11px;margin:4px 0 10px}
  .citygrid{grid-template-columns:1fr!important;padding:8px 12px}
  .pay-sum{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:8px!important;margin:10px 14px 4px!important}
  .jgrid{grid-template-columns:1fr!important;gap:10px}
  .kat{grid-template-columns:1fr!important}
  .catrow{gap:8px}.catnm{width:96px!important;font-size:11.5px}.catval{width:58px!important;font-size:11px}
  .pp-row{flex-wrap:wrap;gap:8px}
  .pp-main{flex-basis:calc(100% - 90px)}
  .pp-act{width:100%;justify-content:flex-end;padding-top:4px}
  .pv-overlay{padding:10px;align-items:flex-end}
  .pv-modal{border-radius:16px;max-height:90vh;overflow-y:auto}
  .pv-bar{padding:11px 14px;flex-wrap:wrap;gap:6px}
  .pv-bar b{font-size:13.5px}
  .pv-paper{margin:10px;padding:16px 14px;font-size:12px}
  .pv-price{flex-direction:column;align-items:flex-start;gap:4px}
  /* Public page (Umum) mobile polish */
  .um-topnav{padding:9px 14px!important;gap:8px}
  .um-tbrand img{height:30px!important}
  .app.public-mode .umhero{padding:108px 16px 68px!important}
  .app.public-mode .umhero h1{font-size:24px!important;line-height:1.22;margin-bottom:10px}
  .app.public-mode .umhero p{font-size:13px!important;margin-bottom:18px;padding:0 4px}
  .app.public-mode .umhero-search{flex-wrap:nowrap!important;padding:4px 4px 4px 12px!important;border-radius:99px!important;margin-bottom:14px!important}
  .app.public-mode .umhero-search input{flex:1!important;flex-basis:auto!important;order:0!important;margin:0!important;font-size:12.5px!important}
  .app.public-mode .umhero-search button{order:0!important;margin-left:0!important;padding:8px 14px!important;font-size:12px!important}
  .umhero-cta{gap:8px;width:100%;margin-bottom:20px}
  .umhero-cta .btn-um-primary,.umhero-cta .btn-um-ghost{flex:1 1 calc(50% - 6px);justify-content:center;padding:10px 12px;font-size:12.5px;text-align:center}
  .umstats{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:8px!important}
  .umstat{padding:11px 10px;border-radius:12px}
  .umstat .n{font-size:18px}
  .umstat .l{font-size:10.5px}
  .um-strip-wrap{margin:-38px auto 20px!important;padding:0 14px!important}
  .um-strip{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:10px!important}
  .um-strip-img{height:92px}
  .um-strip-body{padding:10px 11px}
  .um-strip-body b{font-size:12.5px}
  .um-strip-body .sub{font-size:11px}
  .um-strip-body .prc{font-size:11.5px;margin-top:5px}
  .um-container{padding:0 14px!important}
  .umsec-head{flex-direction:column;align-items:flex-start;gap:4px;margin-bottom:12px}
  .umsec-head h2{font-size:17px}
  .umwhy{grid-template-columns:1fr!important;gap:10px!important;margin-bottom:22px}
  .umwhy-card{padding:16px}
  .umfeat-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:10px!important;margin-bottom:22px}
  .umfeat-card{height:128px;padding:10px;border-radius:13px}
  .umfeat-card .cnt b{font-size:12px}
  .umfeat-badge{top:8px;right:8px;font-size:9.5px;padding:3px 7px}
  .umt-head h2{font-size:20px}
  .umt-card-stat,.umt-card-photo{min-height:250px;padding:18px;border-radius:18px}
  .umt-marquee{min-height:260px;max-height:260px;border-radius:18px}
  .umcta{padding:20px 18px;border-radius:16px;gap:12px}
  .umcta div{width:100%}
  .umcta .btn-um-primary,.umcta .btn-um-ghost{width:100%;justify-content:center}
  .rc-price{font-size:26px}
  .rc-row{font-size:12px;gap:8px}
  .rc-row b{text-align:right}
  .um-wa-float{right:14px;bottom:14px;padding:10px 15px;font-size:12.5px}
}

.um-strip-img{justify-content:space-between;align-items:flex-end}
.um-pkg-dur{position:relative;z-index:1;background:rgba(14,36,74,.78);color:var(--gold);font-style:normal;font-size:10.5px;font-weight:700;padding:3px 8px;border-radius:99px;border:1px solid rgba(255,255,255,.2)}
.um-pkg-list{margin-top:7px;display:flex;flex-direction:column;gap:3px;font-size:11.5px;color:var(--ink);line-height:1.4}
.um-pkg-dest{color:var(--muted);font-size:11px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:30px}
.um-pkg-foot{margin-top:10px;padding-top:8px;border-top:1px solid var(--line);display:flex;align-items: flex-end;justify-content:space-between;gap:6px}
.um-pkg-foot small{display:block;font-size:10px;color:var(--muted);font-weight:600}
.um-pkg-foot .prc{margin-top:1px!important;font-size:15px;font-weight:800;color:var(--blue)}
.um-pkg-foot .prc span{font-size:11px;font-weight:600;color:var(--muted)}
.um-pkg-btn{background:rgba(39,91,181,.1);color:var(--blue);font-size:11px;font-weight:800;padding:5px 10px;border-radius:99px;white-space:nowrap}
@media(max-width:680px){
  .um-pkg-list{font-size:10.5px;gap:2px}
  .um-pkg-dest{font-size:10px;min-height:26px}
  .um-pkg-foot .prc{font-size:13px}
  .um-pkg-btn{padding:4px 8px;font-size:10px}
}

.umsteps{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:32px}
.umstep-card{background:rgba(255,255,255,.88);border:1px solid var(--line);border-radius:16px;padding:18px;position:relative;box-shadow:0 8px 24px rgba(15,23,42,.04)}
.umstep-no{width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,var(--navy),var(--blue));color:var(--gold);font-weight:800;font-size:13px;display:grid;place-items:center;margin-bottom:10px}
.umstep-card h4{font-size:14px;font-weight:800;color:var(--navy);margin-bottom:5px}
.umstep-card p{font-size:12px;color:var(--muted);line-height:1.55}
.um-preset-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.um-preset-btn{background:#F4F7FB;border:1px solid var(--line);color:var(--ink);font-family:inherit;font-size:12px;font-weight:700;padding:8px 13px;border-radius:99px;cursor:pointer;transition:.15s}
.um-preset-btn:hover{border-color:var(--blue);color:var(--blue)}
.um-preset-btn.active{background:var(--blue);color:#fff;border-color:var(--blue);box-shadow:0 4px 12px rgba(39,91,181,.22)}
.um-calc-actions{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}
.umfoot{margin-top:34px;background:linear-gradient(160deg,var(--navy),#091730);color:#fff;border-radius:22px;padding:34px 32px 22px;box-shadow:0 18px 42px rgba(14,36,74,.18)}
.umfoot-grid{display:grid;grid-template-columns:1.3fr .8fr 1.1fr;gap:28px;padding-bottom:24px;border-bottom:1px solid rgba(255,255,255,.12)}
.umfoot-brand{display:flex;align-items:center;gap:10px;font-size:17px;font-weight:800;margin-bottom:10px}
.umfoot-brand img{height:38px;width:auto;border-radius:6px}
.umfoot-desc{font-size:12.5px;color:rgba(255,255,255,.74);line-height:1.6;margin-bottom:12px}
.umfoot-badges{display:flex;flex-wrap:wrap;gap:6px}
.umfoot-badges span{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.16);border-radius:99px;padding:4px 10px;font-size:11px;font-weight:600;color:var(--gold)}
.umfoot h5{font-size:13.5px;font-weight:800;color:var(--gold);margin-bottom:11px;letter-spacing:.02em}
.umfoot-links{list-style:none;display:flex;flex-direction:column;gap:7px}
.umfoot-links a{font-size:12.5px;color:rgba(255,255,255,.78);text-decoration:none;cursor:pointer;transition:.15s}
.umfoot-links a:hover{color:#fff;padding-left:3px}
.umfoot-contact{display:flex;flex-direction:column;gap:7px;font-size:12.5px;color:rgba(255,255,255,.82);line-height:1.5}
.umfoot-copy{padding-top:16px;text-align:center;font-size:11.5px;color:rgba(255,255,255,.55)}
@media(max-width:960px){
  .umsteps{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:10px}
  .umfoot-grid{grid-template-columns:1fr!important;gap:20px}
}
@media(max-width:680px){
  .umsteps{grid-template-columns:1fr!important}
  .um-calc-actions{grid-template-columns:1fr!important}
  .um-preset-row{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:4px;scrollbar-width:none}
  .um-preset-row::-webkit-scrollbar{display:none}
  .um-preset-btn{white-space:nowrap;flex-shrink:0}
  .umfoot{padding:24px 18px 18px;border-radius:16px}
}

.um-city-pills{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.um-city-pill{display:inline-flex;align-items:center;gap:7px;background:#fff;border:1px solid var(--line);border-radius:99px;padding:8px 14px;font-family:inherit;font-size:12.5px;font-weight:700;color:var(--ink);cursor:pointer;transition:.16s;box-shadow:0 2px 6px rgba(15,23,42,.03)}
.um-city-pill:hover{border-color:var(--blue);color:var(--blue);transform:translateY(-1px)}
.um-city-pill em{font-style:normal;background:#EEF1F6;color:var(--muted);font-size:10.5px;font-weight:800;padding:2px 7px;border-radius:99px}
.um-city-pill.active{background:var(--navy);color:#fff;border-color:var(--navy);box-shadow:0 6px 16px rgba(14,36,74,.2)}
.um-city-pill.active em{background:var(--gold);color:var(--navy)}
.um-search-hint{font-size:12px;color:var(--blue);font-weight:700;background:rgba(39,91,181,.08);padding:7px 12px;border-radius:99px}
.um-dgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:14px}
.um-dcard{background:#fff;border:1.5px solid var(--line);border-radius:16px;overflow:hidden;cursor:pointer;transition:transform .16s,box-shadow .16s,border-color .16s;display:flex;flex-direction:column}
.um-dcard:hover{transform:translateY(-3px);box-shadow:0 12px 26px rgba(15,23,42,.1);border-color:var(--blue)}
.um-dcard.selected{border-color:var(--blue);box-shadow:0 0 0 3px rgba(39,91,181,.18),0 12px 26px rgba(39,91,181,.14)}
.um-dcard-visual{height:108px;position:relative;background-size:cover;background-position:center;display:flex;align-items:flex-end;justify-content:space-between;padding:10px 12px}
.um-dcard-ov{position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,36,74,.18),rgba(14,36,74,.68))}
.um-dcard-cat{position:relative;z-index:1;background:rgba(255,255,255,.92);color:var(--navy);font-size:10.5px;font-weight:800;padding:3px 9px;border-radius:99px;box-shadow:0 2px 6px rgba(0,0,0,.12)}
.um-dcard-city{position:relative;z-index:1;color:rgba(255,255,255,.92);font-size:10.5px;font-weight:700}
.um-dcard-ic{position:absolute;right:12px;top:10px;z-index:1;font-size:24px;opacity:.85;filter:drop-shadow(0 2px 6px rgba(0,0,0,.25))}
.um-dcard-body{padding:13px 14px;display:flex;flex-direction:column;flex:1}
.um-dcard-body h4{font-size:14px;font-weight:800;color:var(--navy);line-height:1.3;margin-bottom:4px}
.um-dcard-body p{font-size:11.5px;color:var(--muted);line-height:1.45;margin-bottom:11px;flex:1}
.um-dcard-foot{border-top:1px solid #F0F3F7;padding-top:9px;display:flex;justify-content:space-between;align-items:center}
.um-dcard-pick{font-size:11.5px;font-weight:800;color:var(--blue);background:rgba(39,91,181,.08);padding:5px 11px;border-radius:99px;transition:.15s;width:100%;text-align:center}
.um-dcard-pick.on{background:var(--blue);color:#fff}
.um-cart-bar{position:sticky;bottom:16px;z-index:40;background:linear-gradient(135deg,var(--navy),var(--navy-2));color:#fff;border-radius:16px;padding:13px 18px;display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;box-shadow:0 16px 38px rgba(14,36,74,.35);border:1px solid rgba(255,255,255,.16);margin-top:12px}
.um-cart-info{flex:1;min-width:200px;font-size:12.5px;line-height:1.45}
.um-cart-info b{color:var(--gold);margin-right:6px}
.um-cart-info span{color:rgba(255,255,255,.9)}
.um-cart-act{display:flex;align-items:center;gap:8px}
@media(max-width:680px){
  .um-city-pills{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:6px;scrollbar-width:none}
  .um-city-pills::-webkit-scrollbar{display:none}
  .um-city-pill{white-space:nowrap;flex-shrink:0;padding:7px 12px;font-size:12px}
  .um-dgrid{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:10px}
  .um-dcard-visual{height:88px;padding:8px}
  .um-dcard-cat{font-size:9.5px;padding:2px 7px}
  .um-dcard-city{display:none}
  .um-dcard-body{padding:10px}
  .um-dcard-body h4{font-size:12.5px}
  .um-dcard-body p{font-size:10.5px;margin-bottom:8px}
  .um-dcard-pick{font-size:10.5px;padding:4px 8px}
  .um-cart-bar{padding:12px 14px;bottom:10px}
  .um-cart-act{width:100%;justify-content:space-between}
}
</style>
</head>
<body>
<div class="app">
  <aside class="sidebar">
    <div class="brand"><img src="__LOGO__" alt="Havist Traveller"></div>
    <nav class="nav" id="nav">
      <a data-view="umum"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 12h18M12 3c3 3 4 6 4 9s-1 6-4 9c-3-3-4-6-4-9s1-6 4-9z"/></svg>Umum (Halaman Publik)</a>
      <a data-view="dashboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>Dashboard</a>
      <span class="nav-label">Operasional</span>
      <a data-view="keuangan"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 10h18M7 15h4M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>Keuangan</a>
      <a data-view="katalog"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M20.6 8.4 12 3 3.4 8.4v7.2L12 21l8.6-5.4z"/><path d="M12 12 3.4 8.4M12 12v9M12 12l8.6-3.6"/></svg>Harga &amp; Katalog</a>
      <a data-view="acc"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>ACC Klien</a>
      <a data-view="jadwal"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>Jadwal Trip</a>
      <a data-view="crew"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0M16 3.5a3.2 3.2 0 0 1 0 6M21 20a6 6 0 0 0-5-5.9"/></svg>Crew</a>
      <a data-view="tl"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="4" y="4" width="16" height="18" rx="2"/><path d="M9 2h6v4H9z"/><path d="m8 13 2 2 4-4"/></svg>Tour Leader &amp; Media</a>
      <span class="nav-label">Sistem</span>
      <a data-view="sales"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>Sales</a>
      <a data-view="laporan"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M4 19V5a2 2 0 0 1 2-2h9l5 5v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/><path d="M14 3v5h5M8 13h8M8 17h5"/></svg>Laporan</a>
      <a data-view="setting"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1V21a2 2 0 1 1-4 0v-.1A1.6 1.6 0 0 0 6.8 19l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1A1.6 1.6 0 0 0 3 13.6H3a2 2 0 1 1 0-4h.1A1.6 1.6 0 0 0 4.6 7L4.5 7a2 2 0 1 1 2.8-2.8l.1.1A1.6 1.6 0 0 0 10 3.4V3a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 2.7 1.1l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0 1.1 2.7H21a2 2 0 1 1 0 4h-.1a1.6 1.6 0 0 0-1.5 1z"/></svg>Setting Web</a>
    </nav>
    <div class="side-foot"><div class="ava">H</div><div><div class="nm">Havist Pusat</div><div class="rl">Curug, Tangerang</div></div></div>
  </aside>

  <main class="main">
    <div class="topbar">
      <div class="search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg><input id="globalSearch" placeholder="Cari trip, instansi, atau vendor..."></div>
      <div class="top-actions">
        <button class="icon-btn" onclick="toast('Tidak ada notifikasi baru')"><span class="dot"></span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0"/></svg></button>
        <div class="me" onclick="openLoginModal()" title="Klik untuk Login / Ganti Akun"><div class="ava" id="meAva">O</div><div><div class="nm" id="meName">Owner / Management</div><div class="rl" id="meRole">Owner · Ganti Akun ▾</div></div></div>
      </div>
    </div>
    <div id="view"></div>
  </main>
</div>
<nav class="bottomnav" id="bottomnav"></nav>
<div class="toast" id="toast"></div>

<script>
const DATA = __DATA__;
const CATALOG = __CATALOG__;
const today = new Date('2026-11-15');
// --- mini Excel (.xlsx / OOXML) writer, tanpa CDN — dibangun sendiri (zip+XML) supaya tidak bergantung jaringan luar ---
window.XLSX=(function(){
  function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
  function colName(n){n++;let s='';while(n>0){const m=(n-1)%26;s=String.fromCharCode(65+m)+s;n=Math.floor((n-1)/26);}return s;}
  function sheetXML(rows){
    let rowsXML='';
    rows.forEach(function(row,ri){
      let cellsXML='';
      row.forEach(function(val,ci){
        if(val===null||val===undefined||val==='')return;
        const ref=colName(ci)+(ri+1);
        if(typeof val==='number'&&isFinite(val))cellsXML+='<c r="'+ref+'"><v>'+val+'</v></c>';
        else cellsXML+='<c r="'+ref+'" t="inlineStr"><is><t xml:space="preserve">'+esc(val)+'</t></is></c>';
      });
      rowsXML+='<row r="'+(ri+1)+'">'+cellsXML+'</row>';
    });
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'+rowsXML+'</sheetData></worksheet>';
  }
  function contentTypesXML(n){
    let ov='';for(let i=1;i<=n;i++)ov+='<Override PartName="/xl/worksheets/sheet'+i+'.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>';
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'+ov+'</Types>';
  }
  function relsXML(){
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>';
  }
  function workbookXML(sheets){
    let sx='';sheets.forEach(function(sh,i){sx+='<sheet name="'+esc(sh.name)+'" sheetId="'+(i+1)+'" r:id="rId'+(i+1)+'"/>';});
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'+sx+'</sheets></workbook>';
  }
  function workbookRelsXML(n){
    let r='';for(let i=1;i<=n;i++)r+='<Relationship Id="rId'+i+'" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet'+i+'.xml"/>';
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+r+'</Relationships>';
  }
  // --- zip (store, no compression) ---
  const CRC_TABLE=(function(){const t=new Uint32Array(256);for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=(c&1)?(0xEDB88320^(c>>>1)):(c>>>1);t[n]=c>>>0;}return t;})();
  function crc32(bytes){let c=0xFFFFFFFF;for(let i=0;i<bytes.length;i++)c=CRC_TABLE[(c^bytes[i])&0xFF]^(c>>>8);return (c^0xFFFFFFFF)>>>0;}
  function buildZip(files){
    let offset=0;const localParts=[],centralParts=[];
    files.forEach(function(f){
      const nameBytes=new TextEncoder().encode(f.name);
      const crc=crc32(f.data),size=f.data.length;
      const lh=new Uint8Array(30+nameBytes.length);const ldv=new DataView(lh.buffer);
      ldv.setUint32(0,0x04034b50,true);ldv.setUint16(4,20,true);ldv.setUint16(6,0,true);ldv.setUint16(8,0,true);
      ldv.setUint16(10,0,true);ldv.setUint16(12,0,true);ldv.setUint32(14,crc,true);ldv.setUint32(18,size,true);ldv.setUint32(22,size,true);
      ldv.setUint16(26,nameBytes.length,true);ldv.setUint16(28,0,true);lh.set(nameBytes,30);
      localParts.push(lh,f.data);
      const ch=new Uint8Array(46+nameBytes.length);const cdv=new DataView(ch.buffer);
      cdv.setUint32(0,0x02014b50,true);cdv.setUint16(4,20,true);cdv.setUint16(6,20,true);cdv.setUint16(8,0,true);cdv.setUint16(10,0,true);
      cdv.setUint16(12,0,true);cdv.setUint16(14,0,true);cdv.setUint32(16,crc,true);cdv.setUint32(20,size,true);cdv.setUint32(24,size,true);
      cdv.setUint16(28,nameBytes.length,true);cdv.setUint16(30,0,true);cdv.setUint16(32,0,true);cdv.setUint16(34,0,true);cdv.setUint16(36,0,true);
      cdv.setUint32(38,0,true);cdv.setUint32(42,offset,true);ch.set(nameBytes,46);
      centralParts.push(ch);
      offset+=lh.length+f.data.length;
    });
    const centralStart=offset;let centralSize=0;centralParts.forEach(function(c){centralSize+=c.length;});
    const eocd=new Uint8Array(22);const edv=new DataView(eocd.buffer);
    edv.setUint32(0,0x06054b50,true);edv.setUint16(4,0,true);edv.setUint16(6,0,true);edv.setUint16(8,files.length,true);
    edv.setUint16(10,files.length,true);edv.setUint32(12,centralSize,true);edv.setUint32(16,centralStart,true);edv.setUint16(20,0,true);
    const all=localParts.concat(centralParts,[eocd]);
    let total=0;all.forEach(function(p){total+=p.length;});
    const out=new Uint8Array(total);let pos=0;all.forEach(function(p){out.set(p,pos);pos+=p.length;});
    return out;
  }
  return{
    utils:{
      book_new:function(){return{sheets:[]};},
      aoa_to_sheet:function(rows){return{rows:rows};},
      book_append_sheet:function(wb,ws,name){wb.sheets.push({name:String(name).slice(0,31).replace(/[\\\/\?\*\[\]:]/g,' '),rows:ws.rows});}
    },
    writeFile:function(wb,filename){
      const n=wb.sheets.length;
      const enc=function(s){return new TextEncoder().encode(s);};
      const files=[
        {name:'[Content_Types].xml',data:enc(contentTypesXML(n))},
        {name:'_rels/.rels',data:enc(relsXML())},
        {name:'xl/workbook.xml',data:enc(workbookXML(wb.sheets))},
        {name:'xl/_rels/workbook.xml.rels',data:enc(workbookRelsXML(n))}
      ];
      wb.sheets.forEach(function(sh,i){files.push({name:'xl/worksheets/sheet'+(i+1)+'.xml',data:enc(sheetXML(sh.rows))});});
      const zipBytes=buildZip(files);
      const blob=new Blob([zipBytes],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
      saveFileToViewer(filename,blob);
    }
  };
})();
function triggerBrowserDownload(filename,blob){
  try{
    const url=URL.createObjectURL(blob);
    const a=document.createElement('a');
    a.href=url;a.download=filename;document.body.appendChild(a);a.click();
    setTimeout(()=>{URL.revokeObjectURL(url);a.remove();},1000);
    return true;
  }catch(e){return false;}
}
async function saveFileToViewer(filename,blob){
  try{
    const downloads=window.claude&&typeof window.claude.use==='function'?await window.claude.use('downloads'):null;
    if(!downloads){
      if(triggerBrowserDownload(filename,blob)){toast(filename+' diunduh');return;}
      toast('Unduh file tidak didukung di tampilan ini');return;
    }
    await downloads.save({filename:filename,data:blob});
    toast(filename+' diunduh');
  }catch(e){
    const code=e&&e.code;
    if(code==='declined')return;
    if(code==='rejected_extension'||code==='extension_not_enabled')toast('Format file ini tidak didukung untuk diunduh di sini');
    else toast('Gagal mengunduh file, coba lagi');
  }
}
const MONTHS=['2026-07 Juli','2026-08 Agustus','2026-09 September','2026-10 Oktober','2026-11 November','2026-12 Desember','2027-01 Januari','2027-02 Februari','2027-03 Maret','2027-04 April','2027-05 Mei','2027-06 Juni'];
const MLBL={'2026-07 Juli':'Jul','2026-08 Agustus':'Agu','2026-09 September':'Sep','2026-10 Oktober':'Okt','2026-11 November':'Nov','2026-12 Desember':'Des','2027-01 Januari':'Jan','2027-02 Februari':'Feb','2027-03 Maret':'Mar','2027-04 April':'Apr','2027-05 Mei':'Mei','2027-06 Juni':'Jun'};
const COLORS=['#275BB5','#E08A1E','#1AA6B7','#8E63D6','#2B9D6E','#F8C000'];
function jt(n){return 'Rp '+(n/1e6).toLocaleString('id-ID',{minimumFractionDigits:1,maximumFractionDigits:1})+' jt';}
function rp(n){return 'Rp '+Math.round(n).toLocaleString('id-ID');}
function ab(s){s=(s||'').replace(/^(SDN|SMPN|SMAN|SMP|SMA|SMK|PT|SDIT)\s*/i,'');return (s.trim().slice(0,2)||'TR').toUpperCase();}
function col(i){return COLORS[i%COLORS.length];}
function dateID(s){if(!s)return '-';const d=new Date(s);return d.toLocaleDateString('id-ID',{day:'2-digit',month:'short'});}
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}

// aggregates
const MONTH_NAMES=['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember'];
function tripPeriode(t){if(t.per)return t.per;if(!t.brk)return '';const d=new Date(t.brk);if(isNaN(d))return '';return t.brk.slice(0,7)+' '+MONTH_NAMES[d.getMonth()];}
function monthAgg(){const m={};MONTHS.forEach(k=>m[k]={n:0,pax:0,bus:0,laba:0});allTrips().forEach(t=>{const k=tripPeriode(t);if(m[k]){m[k].n++;m[k].pax+=t.pax||0;m[k].bus+=t.bus||0;m[k].laba+=t.laba||0;}});return m;}
function refreshActiveView(){
  if(document.getElementById('keuBody'))renderKeu();
  else if(document.getElementById('cal')){document.getElementById('view').innerHTML=vDashboard();buildCal();initChartTabs();}
  else if(document.getElementById('jadwalBody'))renderJadwalBody();
  else if(document.getElementById('lapBody'))renderLap();
}
// ===== MODEL PEMBAYARAN TERPADU (satu sumber data, semua tab baca dari sini) =====
function payClientList(id){return (store('payClient',{})[id])||[];}
function clientPaid(p){return (p.dp||0)+payClientList(p.id).reduce((a,x)=>a+(+x.amount||0),0);}
function clientSisa(p){return Math.max(0,(p.tagih||0)-clientPaid(p));}
function clientStatus(p){const paid=clientPaid(p);if(p.tagih>0&&paid>=p.tagih)return['lunas','Lunas'];if(paid>0)return['dp','DP sebagian'];return['piutang','Belum bayar'];}
function addClientPayment(id,termin,amount,date){const s=store('payClient',{});(s[id]=s[id]||[]).push({termin,amount:+amount,date:date||new Date().toISOString().slice(0,10)});save('payClient',s);}
function delClientPayment(id,idx){const s=store('payClient',{});if(s[id]){s[id].splice(idx,1);save('payClient',s);refreshActiveView();}}
function payVendorList(no){return (store('payVendor',{})[no])||[];}
function vendorBasePaid(d){return (d.status||'').toUpperCase()==='DONE'?(d.nom||0):0;}
function vendorPaid(d){const ui=payVendorList(d.no).reduce((a,x)=>a+(+x.amount||0),0);return Math.min(d.nom||0,vendorBasePaid(d)+ui);}
function vendorSisa(d){return Math.max(0,(d.nom||0)-vendorPaid(d));}
function vendorStatusArr(d){const paid=vendorPaid(d);if(d.nom>0&&paid>=d.nom)return['lunas','Lunas'];if(paid>0)return['dp','DP sebagian'];return['piutang','Belum bayar'];}
function addVendorPayment(no,amount,date,ket){const s=store('payVendor',{});(s[no]=s[no]||[]).push({amount:+amount,date:date||new Date().toISOString().slice(0,10),ket:ket||''});save('payVendor',s);}
function delVendorPayment(no,idx){const s=store('payVendor',{});if(s[no]){s[no].splice(idx,1);save('payVendor',s);refreshActiveView();}}
// ===== PERSIAPAN VENDOR PER TRIP (pengadaan: armada, hotel, makan, kaos, tiket) =====
const PREPKAT=[['Transport / Bus','armada'],['Hotel / Villa','hotels'],['Konsumsi / Katering',''],['Kaos & Merchandise','kaos'],['Wisata / Tiket','dests'],['Operasional / Lainnya','']];
const PREPDUE={'Transport / Bus':14,'Hotel / Villa':14,'Konsumsi / Katering':7,'Kaos & Merchandise':7,'Wisata / Tiket':7,'Operasional / Lainnya':3};
const PREPTL=[[30,'Hubungi vendor & booking','Konfirmasi ketersediaan armada, hotel, dan tiket wisata.'],[14,'DP armada & hotel','Bayar DP supaya slot terjamin.'],[7,'Pelunasan & konfirmasi final','Lunasi vendor, konfirmasi jumlah peserta final.'],[1,'Checklist akhir','Pastikan armada, konsumsi, kaos, dan dokumen siap.']];
function prepStore(){return store('prep',{});}
function prepTrip(id){return prepStore()[id]||[];}
function savePrep(id,arr){const s=prepStore();s[id]=arr;save('prep',s);refreshActiveView();}
function dminus(brk,n){if(!brk)return '';const d=new Date(brk);d.setDate(d.getDate()-n);return d.toISOString().slice(0,10);}
function prepAdd(tripId,kat,vendor,ket,qty,unit,due){
  const arr=prepTrip(tripId);const q=+qty||1,u=+unit||0;
  arr.push({id:'P'+tripId+'_'+Date.now().toString(36)+Math.random().toString(36).slice(2,5),kat,vendor:vendor||kat,ket:ket||'',qty:q,unit:u,nom:Math.round(q*u),due:due||'',trip:tripId});
  savePrep(tripId,arr);return arr[arr.length-1];
}
function prepDel(tripId,pid){savePrep(tripId,prepTrip(tripId).filter(x=>x.id!==pid));}
function prepEditUnit(tripId,pid,newUnit){
  const arr=prepTrip(tripId).map(x=>{if(x.id!==pid)return x;const u=Math.max(0,parseInt(newUnit)||0);return Object.assign({},x,{unit:u,nom:Math.round((x.qty||1)*u)});});
  savePrep(tripId,arr);
}
// tiap kebutuhan persiapan jadi entri vendor virtual, supaya ikut terbaca di Keuangan & Arus Kas
function prepAsVendor(){const s=prepStore();const out=[];Object.keys(s).forEach(tid=>{(s[tid]||[]).forEach(x=>out.push({no:x.id,tgl:x.due||'-',kat:x.kat,vendor:x.vendor,ket:x.ket||'Persiapan trip',nom:x.nom,status:'',trip:tid,qty:x.qty,unit:x.unit,_prep:true}));});return out;}
function mergeByKey(base,overrides,key){
  const map=new Map();base.forEach(x=>map.set(String(x[key]),x));
  (overrides||[]).forEach(o=>{const k=String(o[key]);map.set(k,Object.assign({},map.get(k)||{},o));});
  return Array.from(map.values());
}
function allVendor(){return mergeByKey(DATA.dpvendor.concat(prepAsVendor()),store('excelVendor',[]),'no');}
function prepTotal(tripId){return prepTrip(tripId).reduce((a,x)=>a+x.nom,0);}
function prepPaid(tripId){return prepTrip(tripId).reduce((a,x)=>a+vendorPaid({no:x.id,nom:x.nom,status:''}),0);}
function prepSisa(tripId){return Math.max(0,prepTotal(tripId)-prepPaid(tripId));}
function tripsNoPrep(){return upcoming().filter(t=>!prepTrip(t.id).length);}
// uang masuk/keluar aktual (cash flow nyata)
function totalGajiAssigned(){return allTrips().reduce((s,t)=>s+tripGaji(t),0);}
function totalVendorKeluar(){return allVendor().reduce((a,d)=>a+vendorPaid(d),0);}
function totalMasuk(){return allPiutang().reduce((a,p)=>a+clientPaid(p),0);}
function totalKeluar(){return totalVendorKeluar()+totalGajiAssigned();}
function piutangTot(){let tag=0,dp=0,sisa=0;allPiutang().forEach(p=>{tag+=p.tagih;dp+=clientPaid(p);sisa+=clientSisa(p);});return{tag,dp,sisa};}
function dpCat(){const c={};allVendor().forEach(d=>{c[d.kat]=(c[d.kat]||0)+d.nom;});return c;}
// --- penawaran (new trips from calculator) merge into live data ---
let lastQuote=null;
function penawaran(){return store('penawaran',[]);}
function syncTripFromPrep(t){
  const prep=prepTrip(t.id);
  if(!prep.length)return t;
  const days=t.malam!=null&&t._new?(t.malam||0)+1:(t.brk&&t.pul?Math.max(1,Math.round((new Date(t.pul)-new Date(t.brk))/86400000)+1):1);
  const buses=prep.filter(x=>x.kat==='Transport / Bus');
  const hotels=prep.filter(x=>x.kat==='Hotel / Villa');
  const busCount=buses.reduce((s,x)=>s+Math.max(1,Math.round((x.qty||1)/days)),0);
  const armNames=[...new Set(buses.map(x=>x.vendor).filter(Boolean))].join(', ');
  const htlNames=[...new Set(hotels.map(x=>x.vendor).filter(Boolean))].join(', ');
  return Object.assign({},t,{
    bus:buses.length?busCount:0,
    armada:buses.length?armNames:'—',
    hotel:hotels.length?htlNames:(t.hotel||'')
  });
}
function allTrips(){
  const pnw=penawaran().filter(p=>p.status==='approved').map(p=>({
    id:p.id,inst:p.klien,dest:p.dest,pax:p.pax,bus:p.bus||0,brk:p.tgl,pul:'',
    malam:p.malam||0,hari:p.hari||((p.malam||0)+1),
    armada:p.armName||'',armRate:p.armRate||0,
    hotel:p.malam>0?(p.hotelName||''):'',hotelRate:p.hotelRate||0,
    mFreq:p.mFreq,mPrice:p.mPrice||35000,
    kaosName:p.kaosName||'',kaosRate:p.kaosRate||0,
    dests:p.dests||[],laba:p.laba||0,jenis:'Paket Wisata',status:'Baru',_new:true
  }));
  const tov=store('tripOverride',{});
  return mergeByKey(DATA.trips.concat(pnw),store('excelTrips',[]),'id').map(t=>tov[t.id]?Object.assign({},t,tov[t.id]):t).map(syncTripFromPrep);
}
function allPiutang(){
  const pnw=penawaran().filter(p=>p.status==='approved').map(p=>({id:p.id,tgl:p.tgl,inst:p.klien,inv:'(dari penawaran)',pax:p.pax,tagih:p.total||0,dp:0,_new:true}));
  const custom=store('customPiutang',[]);
  const ov=store('piutOverride',{});
  return mergeByKey(DATA.piutang.concat(pnw,custom),store('excelPiutang',[]),'id').map(p=>ov[p.id]?Object.assign({},p,ov[p.id]):p);
}
function openCreateInvoiceFromTrip(preId){
  const exist=new Set(allPiutang().map(p=>p.id));
  const avail=allTrips().filter(t=>t.id&&!exist.has(t.id));
  if(!avail.length){toast('Semua trip sudah memiliki tagihan di Pelunasan Klien');return;}
  const old=document.getElementById('invTripOv');if(old)old.remove();
  const opts=avail.map(t=>`<option value="${t.id}" ${t.id===preId?'selected':''}>${esc(t.inst)} — ${t.brk?dateID(t.brk):'—'} (${t.pax||0} pax)</option>`).join('');
  const selT=avail.find(t=>t.id===preId)||avail[0];
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='invTripOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:460px"><div class="pv-bar"><b>Buat Tagihan dari Trip</b><button class="btn-acc no" onclick="document.getElementById('invTripOv').remove()">Tutup</button></div>
    <div style="background:#fff;margin:16px;border-radius:10px;padding:18px">
      <label class="flbl">Pilih Trip (${avail.length} trip belum punya tagihan)</label>
      <select id="ci_trip" class="finput" onchange="document.getElementById('ci_inv').value='INV/HT/'+(this.value||'NEW')">${opts}</select>
      <div class="frow">
        <div><label class="flbl">Total Tagihan (Rp)</label><input id="ci_tagih" class="finput" type="number" placeholder="mis. 50000000"></div>
        <div><label class="flbl">DP Awal Masuk (Rp)</label><input id="ci_dp" class="finput" type="number" value="0"></div>
      </div>
      <label class="flbl">No. Invoice (opsional)</label>
      <input id="ci_inv" class="finput" value="INV/HT/${esc(selT.id)}">
      <button class="btn-save" style="margin-top:8px" onclick="submitCreateInvoiceFromTrip()">✓ Simpan Tagihan &amp; Masuk ke Pelunasan</button>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function submitCreateInvoiceFromTrip(){
  const id=(document.getElementById('ci_trip')||{}).value;
  const t=allTrips().find(x=>x.id===id);if(!t)return;
  const tagih=Math.max(0,parseInt((document.getElementById('ci_tagih')||{}).value)||0);
  const dp=Math.max(0,parseInt((document.getElementById('ci_dp')||{}).value)||0);
  const inv=((document.getElementById('ci_inv')||{}).value||'').trim()||('INV/HT/'+t.id);
  if(tagih<=0&&dp<=0){toast('Isi Total Tagihan atau DP Awal');return;}
  const list=store('customPiutang',[]);
  if(!list.some(x=>x.id===t.id))list.push({id:t.id,tgl:t.brk||'',inst:t.inst,inv:inv,pax:t.pax||0,tagih:tagih,dp:dp});
  save('customPiutang',list);
  const ov=document.getElementById('invTripOv');if(ov)ov.remove();
  toast('Tagihan dibuat untuk '+t.inst);
  refreshActiveView();
}
function savePiutTagih(id,tagih){
  const ov=store('piutOverride',{});ov[id]=Object.assign({},ov[id]||{},{tagih:Math.max(0,parseInt(tagih)||0)});save('piutOverride',ov);
  toast('Tagihan klien diperbarui');refreshActiveView();
}
function markClientLunas(id){
  const p=allPiutang().find(x=>x.id===id);if(!p)return;
  const paid=clientPaid(p);
  if((p.tagih||0)<=0&&paid>0){savePiutTagih(id,paid);return;}
  const sisa=clientSisa(p);
  if(sisa>0)addClientPayment(id,'Pelunasan',sisa,new Date().toISOString().slice(0,10));
  toast('Status klien ditandai Lunas ✓');refreshActiveView();
}
function upcoming(){return allTrips().filter(t=>t.brk && new Date(t.brk)>=today).sort((a,b)=>a.brk<b.brk?-1:1);}
function piutMap(){const m={};allPiutang().forEach(p=>m[p.id]=p);return m;}
function payStatus(t){const p=piutMap()[t.id];if(!p)return ['jadwal','Terjadwal'];if(p.tagih>0||clientPaid(p)>0)return clientStatus(p);return['jadwal','Terjadwal'];}

function toast(msg){const t=document.getElementById('toast');t.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6 9 17l-5-5"/></svg>'+msg;t.classList.add('show');clearTimeout(window._tt);window._tt=setTimeout(()=>t.classList.remove('show'),2200);}

// ---------- VIEWS ----------
const ROLE_CFG={
  owner:{lbl:'Owner / Management',views:['umum','dashboard','keuangan','katalog','acc','jadwal','crew','tl','sales','laporan','setting'],keuTabs:['ringkasan','pelunasan','aging','vendor','reimburse','aruskas','profit']},
  admin:{lbl:'Admin Operasional',views:['umum','keuangan','jadwal','crew','katalog','acc'],keuTabs:['pelunasan','aging','vendor','reimburse']},
  sales:{lbl:'Sales',views:['umum','sales','jadwal'],keuTabs:[]},
  tl:{lbl:'Tour Leader & Media',views:['umum','tl'],keuTabs:[]},
  publik:{lbl:'Publik (Tamu)',views:['umum'],keuTabs:[]}
};
function accounts(){
  let list=store('accounts',null);
  if(!Array.isArray(list)||!list.length||(list.length===1&&list[0].id==='ACC_OWNER')){
    list=[
      {id:'ACC_OWNER',username:'owner',pin:'1234',nama:'Owner / Management',role:'owner',active:true,crewId:'',crewName:''},
      {id:'ACC_ADMIN',username:'admin',pin:'1234',nama:'Admin Operasional',role:'admin',active:true,crewId:'',crewName:''},
      {id:'ACC_SALES',username:'sales',pin:'1234',nama:'Dewi Lestari',role:'sales',active:true,crewId:'K1',crewName:'Dewi Lestari'},
      {id:'ACC_TL',username:'tl',pin:'1234',nama:'Bayu Pratama',role:'tl',active:true,crewId:'K4',crewName:'Bayu Pratama'}
    ];
    save('accounts',list);
  }
  return list;
}
function currentUser(){
  const u=store('currentUser',null);
  if(u&&ROLE_CFG[u.role])return u;
  return {id:'PUBLIK',username:'publik',nama:'Pengunjung',role:'publik'};
}
function roleCfg(){return ROLE_CFG[currentUser().role]||ROLE_CFG.publik;}
function canView(v){return roleCfg().views.includes(v);}
function canKeuTab(k){return roleCfg().keuTabs.includes(k);}
const NAV_META={
  umum:['Umum','<path d="M3 12h18M12 3c3 3 4 6 4 9s-1 6-4 9c-3-3-4-6-4-9s1-6 4-9z"/>'],
  dashboard:['Dashboard','<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>'],
  keuangan:['Keuangan','<path d="M3 10h18M7 15h4M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'],
  katalog:['Katalog','<path d="M20.6 8.4 12 3 3.4 8.4v7.2L12 21l8.6-5.4z"/><path d="M12 12 3.4 8.4M12 12v9M12 12l8.6-3.6"/>'],
  acc:['ACC Klien','<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'],
  jadwal:['Jadwal','<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>'],
  crew:['Crew','<circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0M16 3.5a3.2 3.2 0 0 1 0 6M21 20a6 6 0 0 0-5-5.9"/>'],
  tl:['TL & Media','<rect x="4" y="4" width="16" height="18" rx="2"/><path d="M9 2h6v4H9z"/><path d="m8 13 2 2 4-4"/>'],
  sales:['Sales','<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'],
  laporan:['Laporan','<path d="M4 19V5a2 2 0 0 1 2-2h9l5 5v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/><path d="M14 3v5h5M8 13h8M8 17h5"/>'],
  setting:['Setting','<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1V21a2 2 0 1 1-4 0v-.1A1.6 1.6 0 0 0 6.8 19l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1A1.6 1.6 0 0 0 3 13.6H3a2 2 0 1 1 0-4h.1A1.6 1.6 0 0 0 4.6 7L4.5 7a2 2 0 1 1 2.8-2.8l.1.1A1.6 1.6 0 0 0 10 3.4V3a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 2.7 1.1l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0 1.1 2.7H21a2 2 0 1 1 0 4h-.1a1.6 1.6 0 0 0-1.5 1z"/>']
};
function applyRoleUI(){
  const u=currentUser(),cfg=roleCfg();
  const ava=document.getElementById('meAva'),nm=document.getElementById('meName'),rl=document.getElementById('meRole');
  if(ava)ava.textContent=(u.nama||'U')[0].toUpperCase();
  if(nm)nm.textContent=u.nama||'Pengguna';
  if(rl)rl.textContent=cfg.lbl+' · Ganti ▾';
  document.querySelectorAll('#nav a[data-view]').forEach(a=>{
    a.style.display=canView(a.dataset.view)?'':'none';
  });
  const bnav=document.getElementById('bottomnav');
  if(bnav){
    const allowed=cfg.views.filter(v=>NAV_META[v]);
    if(u.role==='publik'||allowed.length<=1){
      bnav.innerHTML='';
    }else{
      const direct=allowed.length<=5?allowed:allowed.slice(0,4);
      const hasMore=allowed.length>5;
      const cur=(location.hash||'#umum').slice(1)||'umum';
      bnav.innerHTML=direct.map(v=>`<a data-view="${v}" class="${v===cur?'active':''}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor">${NAV_META[v][1]}</svg>${NAV_META[v][0]}</a>`).join('')
        +(hasMore?`<a class="more" onclick="openMoreSheet()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="5" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="19" cy="12" r="1.6"/></svg>Lainnya</a>`:'');
    }
  }
}
function openLoginModal(){
  const old=document.getElementById('loginOv');if(old)old.remove();
  const u=currentUser();
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='loginOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:420px"><div class="pv-bar"><b>${u.role==='publik'?'Login Staf':'Akun & Ganti Staf'}</b><button class="btn-acc no" onclick="document.getElementById('loginOv').remove()">Tutup</button></div>
    <div style="background:#fff;margin:16px;border-radius:10px;padding:18px">
      <div style="font-size:12px;color:var(--muted);margin-bottom:10px">Akun aktif: <b>${esc(u.nama)}</b> (${esc(roleCfg().lbl)})</div>
      <label class="flbl">Username / ID</label><input id="lg_user" class="finput" placeholder="mis. owner / sales1">
      <label class="flbl">PIN / Password</label><input id="lg_pin" class="finput" type="password" placeholder="••••" onkeydown="if(event.key==='Enter')doLogin()">
      <div style="display:flex;gap:8px;margin-top:6px">
        <button class="btn-save" style="flex:1" onclick="doLogin()">Masuk</button>
        ${u.role!=='publik'?`<button class="btn-acc no" style="color:var(--red);border-color:rgba(220,38,38,.3)" onclick="switchToPublik()">Keluar (Logout)</button>`:''}
      </div>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function doLogin(){
  const un=(document.getElementById('lg_user').value||'').trim().toLowerCase();
  const pin=(document.getElementById('lg_pin').value||'').trim();
  const acc=accounts().find(a=>a.active!==false&&(a.username||'').toLowerCase()===un&&String(a.pin)===pin);
  if(!acc){toast('Username atau PIN/Password salah');return;}
  let cid=acc.crewId||'';
  if(!cid&&(acc.role==='tl'||acc.role==='sales')){
    const m=crewList().find(c=>c.nama.toLowerCase()===(acc.crewName||acc.nama||'').toLowerCase());
    if(m)cid=m.id;
  }
  save('currentUser',{id:acc.id,username:acc.username,nama:acc.nama,role:acc.role,crewId:cid,crewName:acc.crewName||acc.nama||''});
  if(acc.role==='tl'&&cid)save('currentTL',cid);
  if(acc.role==='sales'&&cid)save('currentSales',cid);
  const ov=document.getElementById('loginOv');if(ov)ov.remove();
  applyRoleUI();
  const dest=ROLE_CFG[acc.role].views.includes('dashboard')?'dashboard':(ROLE_CFG[acc.role].views[1]||'umum');
  toast('Login sebagai '+acc.nama+' ('+ROLE_CFG[acc.role].lbl+')');
  go(dest);
}
function quickSwitchAcc(id){
  const acc=accounts().find(a=>a.id===id&&a.active!==false);if(!acc)return;
  let cid=acc.crewId||'';
  if(!cid&&(acc.role==='tl'||acc.role==='sales')){
    const m=crewList().find(c=>c.nama.toLowerCase()===(acc.crewName||acc.nama||'').toLowerCase());
    if(m)cid=m.id;
  }
  save('currentUser',{id:acc.id,username:acc.username,nama:acc.nama,role:acc.role,crewId:cid,crewName:acc.crewName||acc.nama||''});
  if(acc.role==='tl'&&cid)save('currentTL',cid);
  if(acc.role==='sales'&&cid)save('currentSales',cid);
  const ov=document.getElementById('loginOv');if(ov)ov.remove();
  applyRoleUI();
  const dest=ROLE_CFG[acc.role].views.includes('dashboard')?'dashboard':(ROLE_CFG[acc.role].views[1]||'umum');
  toast('Beralih ke '+acc.nama);
  go(dest);
}
function switchToPublik(){
  save('currentUser',{id:'PUBLIK',username:'publik',nama:'Tamu Publik',role:'publik'});
  const ov=document.getElementById('loginOv');if(ov)ov.remove();
  applyRoleUI();
  toast('Anda telah keluar ke Mode Publik');
  applyRoleUI();go('umum');
}
function addStaffAccount(){
  const role=document.getElementById('na_role').value;
  const nama=(document.getElementById('na_nama').value||'').trim();
  const username=(document.getElementById('na_user').value||'').trim().toLowerCase();
  const pin=(document.getElementById('na_pin').value||'').trim();
  if(!nama||!username||!pin){toast('Lengkapi nama, username, dan PIN');return;}
  const list=accounts();
  if(list.some(a=>(a.username||'').toLowerCase()===username)){toast('Username sudah dipakai');return;}
  let crewId='';
  if(role==='tl'||role==='sales'){
    const cl=crewList();
    let ex=cl.find(c=>c.nama.toLowerCase()===nama.toLowerCase());
    if(!ex){
      ex={id:'K'+Date.now().toString(36).toUpperCase(),nama,peran:role==='sales'?'Sales':'Tour Leader',hp:'',tarif:role==='tl'?175000:0,status:'Aktif'};
      cl.push(ex);saveCrewList(cl);
    }
    crewId=ex.id;
  }
  list.push({id:'ACC_'+Date.now(),username,pin,nama,role,active:true,crewId,crewName:nama});
  save('accounts',list);
  toast('Akun '+nama+' ('+ROLE_CFG[role].lbl+') dibuat ✓');
  go('setting');
}
function toggleAccActive(id){
  const list=accounts();const a=list.find(x=>x.id===id);if(!a)return;
  if(a.role==='owner'&&a.active!==false&&list.filter(x=>x.role==='owner'&&x.active!==false).length<=1){toast('Minimal harus ada 1 akun Owner aktif');return;}
  a.active=a.active===false?true:false;
  save('accounts',list);
  go('setting');
}
function deleteAcc(id){
  const list=accounts();const a=list.find(x=>x.id===id);if(!a)return;
  if(a.role==='owner'&&list.filter(x=>x.role==='owner').length<=1){toast('Minimal harus ada 1 akun Owner');return;}
  save('accounts',list.filter(x=>x.id!==id));
  toast('Akun dihapus');go('setting');
}
function vDashboard(){
  const m=monthAgg(),pt=piutangTot(),up=upcoming();
  const masuk=totalMasuk(),keluar=totalKeluar(),saldo=masuk-keluar;
  const nov=m['2026-11 November'];
  const target=store('target',100000000);const pctTarget=target>0?Math.round(nov.laba/target*100):0;
  const day=86400000;
  const invOverdue=allPiutang().filter(p=>{if(p.tagih<=0||clientStatus(p)[0]==='lunas')return false;const due=p.tgl?new Date(new Date(p.tgl)-7*day):null;return due&&today>due;});
  const vendOverdue=allVendor().filter(d=>{const[sc]=vendorStatusArr(d);if(sc==='lunas')return false;const due=(d.tgl&&d.tgl!=='-')?new Date(d.tgl):null;return due&&today>due;});
  const vendOverdueNom=vendOverdue.reduce((a,d)=>a+vendorSisa(d),0);
  const pnwPending=penawaran().filter(p=>p.status==='pending').length;
  const reimbPending=reimburseList().filter(r=>r.status==='pending');
  const noCrew=up.filter(t=>{const a=tripAssign(t.id);return !a.tls.length&&!a.medias.length;}).length;
  const weekEnd=new Date(today.getTime()+7*day);
  const weekTrips=allTrips().filter(t=>t.brk&&new Date(t.brk)>=today&&new Date(t.brk)<=weekEnd);
  const weekPax=weekTrips.reduce((s,t)=>s+(t.pax||0),0);
  const activeToday=allTrips().filter(t=>tripStatus(t)==='berlangsung');
  const crewTodaySet=new Set();activeToday.forEach(t=>{const a=tripAssign(t.id);a.tls.forEach(x=>crewTodaySet.add(x.id));a.medias.forEach(x=>crewTodaySet.add(x.id));});
  const unpaid=allPiutang().filter(p=>p.tagih>0&&clientSisa(p)>0).sort((a,b)=>clientSisa(b)-clientSisa(a)).slice(0,5);
  const rec=['2026-07 Juli','2026-08 Agustus','2026-09 September','2026-10 Oktober','2026-11 November'];
  const mx=Math.max(1,...rec.map(k=>m[k].laba))*1.08;
  const bars=rec.map(k=>{const v=m[k].laba,h=v/mx*100,hl=k.includes('November')?' hl':'';return `<div class="bar${hl}" onclick="toast('${MLBL[k]}: ${m[k].n} trip, laba ${jt(v)}')"><div class="col" style="height:${h}%"><span class="tip">${jt(v)}</span></div><span>${MLBL[k]}</span></div>`;}).join('');
  const tripRows=up.slice(0,6).map(t=>{const[pc,pl]=payStatus(t),i=DATA.trips.findIndex(x=>x.id===t.id);const p=piutMap()[t.id];const val=p?(clientPaid(p)>0?jt(clientPaid(p)):(p.tagih>0?jt(p.tagih):'—')):'—';const tls=tripCrewNames(t.id,'tl');const tl=tls[0];
    return `<tr class="clk" onclick="openTripDetail('${t.id}')"><td><div class="trip"><div class="th" style="background:${i>=0?col(i):'var(--gold)'};color:${i>=0?'#fff':'var(--navy)'}">${ab(t.inst)}</div><div><div class="nm">${esc(t.inst)}</div><div class="loc">${esc((t.dest||'').split('(')[0])}${tl?' · TL '+esc(tl.nama.split(' ')[0]):''}</div></div></div></td><td>${dateID(t.brk)}</td><td>${t.pax} pax</td><td class="price">${val}</td><td><span class="pill ${pc}">${pl}</span></td></tr>`;}).join('');
  const alerts=[
    {n:invOverdue.length,txt:'Piutang lewat jatuh tempo',go:"go('keuangan');setTimeout(()=>setKeuTab('aging'),40)",ic:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'},
    {n:vendOverdue.length,txt:'DP vendor lewat jatuh tempo',go:"go('keuangan');setTimeout(()=>setKeuTab('vendor'),40)",ic:'<path d="M3 10h18M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'},
    {n:pnwPending,txt:'Penawaran menunggu ACC',go:"go('acc')",ic:'<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'},
    {n:reimbPending.length,txt:'Reimburse crew belum diproses',go:"go('keuangan');setTimeout(()=>setKeuTab('reimburse'),40)",ic:'<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>'},
    {n:noCrew,txt:'Trip belum ada crew',go:"go('crew');setTimeout(()=>setCrewTab('penugasan'),40)",ic:'<circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/>'},
    {n:tripsNoPrep().length,txt:'Trip belum diatur vendornya',go:"go('keuangan');setTimeout(()=>setKeuTab('vendor'),40)",ic:'<path d="M3 7h18M3 12h18M3 17h10"/>'},
  ].filter(a=>a.n>0);
  const alertHTML=alerts.length?alerts.map(a=>`<div class="r-item" style="cursor:pointer" onclick="${a.go}"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${a.ic}</svg>${a.txt}<span class="n">${a.n}</span></div>`).join(''):'<div style="font-size:12.5px;color:rgba(255,255,255,.8);padding:6px 0">Semua beres, tidak ada yang mendesak 🎉</div>';
  const nextTrip=up[0];const nextTL=nextTrip?tripCrewNames(nextTrip.id,'tl')[0]:null;
  return `<div class="hello fade"><h1>Halo, Management 👋</h1><p>${up.length} trip akan datang · saldo kas ${jt(saldo)} · ${alerts.reduce((s,a)=>s+a.n,0)} hal perlu tindak lanjut</p></div>
  <div class="cards fade" style="grid-template-columns:repeat(3,1fr)">
    <div class="scard" onclick="go('keuangan');setTimeout(()=>setKeuTab('aruskas'),40)" style="cursor:pointer;border-color:${saldo<0?'var(--red)':'var(--line)'}"><div class="ic ${saldo<0?'r':'gr'}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 10h18M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg></div><div class="lbl">Saldo Kas</div><div class="val mono" style="color:${saldo<0?'var(--red)':'var(--ink)'}">${saldo<0?'- ':''}${jt(Math.abs(saldo))}</div><div class="sub" style="color:var(--muted)">masuk ${jt(masuk)} · keluar ${jt(keluar)}</div></div>
    <div class="scard" onclick="go('keuangan');setTimeout(()=>setKeuTab('pelunasan'),40)" style="cursor:pointer"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div class="lbl">Piutang Jatuh Tempo</div><div class="val mono">${jt(pt.sisa)}</div><div class="sub down">${invOverdue.length} invoice lewat target</div></div>
    <div class="scard" onclick="go('keuangan');setTimeout(()=>setKeuTab('vendor'),40)" style="cursor:pointer;${vendOverdue.length?'border-color:var(--red)':''}"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg></div><div class="lbl">DP Vendor Jatuh Tempo</div><div class="val mono" style="${vendOverdue.length?'color:var(--red)':''}">${jt(vendOverdueNom)}</div><div class="sub" style="color:var(--muted)">${vendOverdue.length} vendor lewat tempo</div></div>
    <div class="scard" onclick="go('keuangan');setTimeout(()=>setKeuTab('profit'),40)" style="cursor:pointer"><div class="ic b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 10h18M7 15h4"/></svg></div><div class="lbl">Laba Bulan Ini (Nov)</div><div class="val mono">${jt(nov.laba)}</div><div class="sub ${nov.laba>=target?'up':'down'}">${pctTarget}% dari target ${jt(target)}</div></div>
    <div class="scard" onclick="go('jadwal')" style="cursor:pointer"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg></div><div class="lbl">Trip Minggu Ini</div><div class="val mono">${weekTrips.length} trip</div><div class="sub" style="color:var(--muted)">${weekPax} pax · total ${up.length} akan datang</div></div>
    <div class="scard" onclick="go('crew')" style="cursor:pointer"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/></svg></div><div class="lbl">Crew Bertugas Hari Ini</div><div class="val mono">${crewTodaySet.size} crew</div><div class="sub" style="color:var(--muted)">${activeToday.length} trip berlangsung · gaji ${jt(totalGajiAssigned())}</div></div>
  </div>
  <div class="grid fade">
    <div>
      <div class="panel"><div class="panel-h"><h3>Tren Kinerja &amp; Arus Kas</h3><button class="lnk" onclick="go('keuangan')">Laporan lengkap →</button></div><div class="tabs" id="chartTabs"><button class="tab active">Laba</button><button class="tab">Arus Kas</button><button class="tab">Pax</button><button class="tab">Bus</button></div><div class="chartwrap"><div class="chart" id="chart">${bars}</div></div></div>
      <div class="panel"><div class="panel-h"><h3>Trip Terdekat</h3><button class="lnk" onclick="go('jadwal')">Lihat semua →</button></div><div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Destinasi · Crew</th><th>Tanggal</th><th>Peserta</th><th>Dibayar</th><th>Status</th></tr></thead><tbody>${tripRows}</tbody></table></div></div>
      <div class="panel" style="margin-bottom:0"><div class="panel-h"><h3>Piutang — Belum Lunas <span style="color:var(--red);font-size:13px">(${unpaid.length})</span></h3><button class="lnk" onclick="go('keuangan');setTimeout(()=>setKeuTab('pelunasan'),40)">Rekap →</button></div><div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Pelanggan</th><th>Sisa</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${unpaid.map(p=>`<tr><td><div class="nm" style="font-weight:700">${esc(p.inst)}</div></td><td class="price mono">${jt(clientSisa(p))}</td><td style="text-align:right"><button class="btn-acc ok" onclick="go('keuangan');setTimeout(()=>{setKeuTab('pelunasan');openBayar('${p.id}')},50)">Bayar</button></td></tr>`).join('')}</tbody></table></div></div>
    </div>
    <div>
      <div class="remind"><h4>Perlu Tindak Lanjut</h4><p>Klik untuk langsung ke halamannya.</p>${alertHTML}</div>
      <div class="side-card" style="margin-top:22px"><div class="cal-h"><div class="mo">November 2026</div></div><div class="cal" id="cal"></div><div class="legend"><span><i style="background:var(--gold)"></i>Berangkat</span><span><i style="background:var(--blue)"></i>Hari ini</span></div></div>
      <div class="side-card"><div class="panel-h" style="padding:0 0 12px"><h3 style="font-size:14.5px">Rangkuman Semua Menu</h3></div>
        <div class="ds-row" onclick="go('keuangan');setTimeout(()=>setKeuTab('aruskas'),40)"><span>Keuangan · Pengeluaran</span><b>${jt(keluar)}</b></div>
        <div class="ds-row" onclick="go('keuangan');setTimeout(()=>setKeuTab('vendor'),40)"><span>Vendor · Belum dibayar</span><b>${jt(allVendor().reduce((a,d)=>a+vendorSisa(d),0))}</b></div>
        <div class="ds-row" onclick="go('jadwal')"><span>Jadwal · ${nextTrip?esc(nextTrip.inst.slice(0,18)):'Tidak ada'}</span><b>${nextTrip?dateID(nextTrip.brk)+(nextTL?' · '+esc(nextTL.nama.split(' ')[0]):''):'—'}</b></div>
        <div class="ds-row" onclick="go('crew')"><span>Crew · Bertugas / Gaji</span><b>${crewTodaySet.size} · ${jt(totalGajiAssigned())}</b></div>
        <div class="ds-row" onclick="go('acc')"><span>ACC · Menunggu persetujuan</span><b>${pnwPending}</b></div>
        <div class="ds-row" onclick="go('keuangan');setTimeout(()=>setKeuTab('reimburse'),40)"><span>Reimburse · Menunggu ACC</span><b>${reimbPending.length}</b></div>
      </div>
    </div>
  </div>`;
}
function buildCal(){
  const cal=document.getElementById('cal');if(!cal)return;
  const dows=['Sen','Sel','Rab','Kam','Jum','Sab','Min'];
  const go={};allTrips().forEach(t=>{if(t.brk&&t.brk.startsWith('2026-11')){const d=+t.brk.slice(8);(go[d]=go[d]||[]).push(t);}});
  let h=dows.map(d=>`<div class="dow">${d}</div>`).join('');
  for(let i=0;i<6;i++)h+='<div class="d mut"></div>';
  for(let d=1;d<=30;d++){let c='d';if(d===15)c+=' today';else if(go[d])c+=' go';
    const oc=go[d]?`onclick="dayTrips(${d})"`:'';h+=`<div class="${c}" ${oc}>${d}</div>`;}
  cal.innerHTML=h;
}
function dayTrips(d){const ts=allTrips().filter(t=>t.brk===`2026-11-${String(d).padStart(2,'0')}`);toast(`${d} Nov: ${ts.map(t=>t.inst.slice(0,20)).join(', ')}`);}

let keuTab='ringkasan';
function setKeuTab(k){keuTab=k;const nav=document.querySelector('#view .tabs');if(nav)nav.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.kt===k));renderKeu();}
function renderKeu(){const b=document.getElementById('keuBody');if(!b)return;b.innerHTML=keuTab==='aruskas'?keuAruskas():keuTab==='aging'?keuAging():keuTab==='pelunasan'?keuPelunasan():keuTab==='vendor'?keuJadwalVendor():keuTab==='profit'?keuProfit():keuTab==='reimburse'?keuReimburse():keuRingkasan();}
function adminOpsCards(){
  const pt=piutangTot(),up=upcoming(),day=86400000;
  const invOverdue=allPiutang().filter(p=>{if(p.tagih<=0||clientStatus(p)[0]==='lunas')return false;const due=p.tgl?new Date(new Date(p.tgl)-7*day):null;return due&&today>due;});
  const vendOverdue=allVendor().filter(d=>{const[sc]=vendorStatusArr(d);if(sc==='lunas')return false;const due=(d.tgl&&d.tgl!=='-')?new Date(d.tgl):null;return due&&today>due;});
  const vendOverdueNom=vendOverdue.reduce((a,d)=>a+vendorSisa(d),0);
  const weekEnd=new Date(today.getTime()+7*day);
  const weekTrips=allTrips().filter(t=>t.brk&&new Date(t.brk)>=today&&new Date(t.brk)<=weekEnd);
  const weekPax=weekTrips.reduce((s,t)=>s+(t.pax||0),0);
  const activeToday=allTrips().filter(t=>tripStatus(t)==='berlangsung');
  const crewTodaySet=new Set();activeToday.forEach(t=>{const a=tripAssign(t.id);a.tls.forEach(x=>crewTodaySet.add(x.id));a.medias.forEach(x=>crewTodaySet.add(x.id));});
  return `<div class="cards fade" style="grid-template-columns:repeat(4,1fr);margin-bottom:18px">
    <div class="scard" onclick="setKeuTab('pelunasan')" style="cursor:pointer"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div class="lbl">Piutang Jatuh Tempo</div><div class="val mono">${jt(pt.sisa)}</div><div class="sub down">${invOverdue.length} invoice lewat target</div></div>
    <div class="scard" onclick="setKeuTab('vendor')" style="cursor:pointer;${vendOverdue.length?'border-color:var(--red)':''}"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg></div><div class="lbl">DP Vendor Jatuh Tempo</div><div class="val mono" style="${vendOverdue.length?'color:var(--red)':''}">${jt(vendOverdueNom)}</div><div class="sub" style="color:var(--muted)">${vendOverdue.length} vendor lewat tempo</div></div>
    <div class="scard" onclick="go('jadwal')" style="cursor:pointer"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg></div><div class="lbl">Trip Minggu Ini</div><div class="val mono">${weekTrips.length} trip</div><div class="sub" style="color:var(--muted)">${weekPax} pax · total ${up.length} akan datang</div></div>
    <div class="scard" onclick="go('crew')" style="cursor:pointer"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/></svg></div><div class="lbl">Crew Bertugas</div><div class="val mono">${crewTodaySet.size} crew</div><div class="sub" style="color:var(--muted)">${activeToday.length} trip berlangsung hari ini</div></div>
  </div>`;
}
function vKeuangan(){
  const isAdmin=currentUser().role==='admin';
  const tabs=[['ringkasan','Ringkasan'],['pelunasan','Pelunasan Klien'],['aging','Aging Piutang'],['vendor','Jadwal Vendor'],['reimburse','Reimburse Lapangan'],['aruskas','Arus Kas'],['profit','Profitabilitas']].filter(([k])=>canKeuTab(k));
  if(tabs.length&&!tabs.some(([k])=>k===keuTab))keuTab=tabs[0][0];
  const nav=tabs.map(([k,l])=>`<button class="tab ${keuTab===k?'active':''}" data-kt="${k}" onclick="setKeuTab('${k}')">${l}</button>`).join('');
  return `<div class="hello fade" style="display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:10px"><div><h1>${isAdmin?'Operasional &amp; Keuangan':'Keuangan'}</h1><p>${isAdmin?'Fokus operasional: pelunasan klien, aging piutang, jadwal DP vendor &amp; reimburse lapangan':'Laba, arus kas, piutang, dan pengeluaran DP vendor dari Master Data Trip'}</p></div><button class="btn-acc" style="background:var(--gold);color:var(--navy);margin-bottom:18px" onclick="openExcelSync()">⬆ Impor &amp; Sinkron Excel</button></div>
  ${isAdmin?adminOpsCards():''}
  <div class="tabs" style="padding:0 0 16px">${nav}</div><div id="keuBody"></div>`;
}
function keuRingkasan(){
  const m=monthAgg(),pt=piutangTot(),cat=dpCat();
  const rows=MONTHS.map(k=>`<tr><td style="font-weight:700">${esc(k.slice(8))}</td><td>${m[k].n}</td><td class="mono">${m[k].pax.toLocaleString('id-ID')}</td><td class="mono">${m[k].bus}</td><td class="price mono">${m[k].laba?jt(m[k].laba):'<span style=color:var(--muted-2)>—</span>'}</td></tr>`).join('');
  const totLaba=Object.values(m).reduce((a,b)=>a+b.laba,0);
  const piutRows=allPiutang().filter(p=>p.tagih>0).map(p=>{const paid=clientPaid(p),sisa=clientSisa(p);const st=clientStatus(p);
    return `<tr><td><div class="nm" style="font-weight:700">${esc(p.inst)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${esc(p.inv)||'—'}</div></td><td class="mono">${p.tagih>0?jt(p.tagih):'<span style=color:var(--muted)>Belum diset</span>'}</td><td class="mono" style="color:var(--green)">${paid?jt(paid):'—'}</td><td class="price mono">${sisa>0?jt(sisa):'<span style=color:var(--green)>Lunas</span>'}</td><td><span class="pill ${st[0]}">${st[1]}</span></td></tr>`;}).join('');
  const catMax=Math.max(...Object.values(cat));
  const catRows=Object.entries(cat).sort((a,b)=>b[1]-a[1]).map(([k,v],i)=>`<div class="catrow"><div class="catnm" style="width:150px">${esc(k)}</div><div class="catbar"><div class="catfill" style="width:${v/catMax*100}%;background:${col(i)}"></div></div><div class="catval">${jt(v)}</div></div>`).join('');
  return `<div class="cards fade">
    <div class="scard"><div class="ic b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 10h18M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg></div><div class="lbl">Total Laba Tercatat</div><div class="val mono">${jt(totLaba)}</div><div class="sub" style="color:var(--muted)">Jul–Nov 2026</div></div>
    <div class="scard"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 12 5 5L20 7"/></svg></div><div class="lbl">Total DP Masuk</div><div class="val mono">${jt(pt.dp)}</div><div class="sub up">dari pelanggan</div></div>
    <div class="scard"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div class="lbl">Sisa Piutang</div><div class="val mono">${jt(pt.sisa)}</div><div class="sub down">belum tertagih</div></div>
    <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h10"/></svg></div><div class="lbl">Pengeluaran DP Vendor</div><div class="val mono">${jt(Object.values(cat).reduce((a,b)=>a+b,0))}</div><div class="sub" style="color:var(--muted)">${allVendor().length} transaksi</div></div>
  </div>
  <div class="panel fade"><div class="panel-h"><h3>Kinerja per Bulan</h3></div><div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Bulan</th><th>Jml Trip</th><th>Pax</th><th>Bus</th><th>Laba Persiapan</th></tr></thead><tbody>${rows}</tbody></table></div></div>
  <div class="grid fade" style="grid-template-columns:1fr 1fr">
    <div class="panel" style="margin:0"><div class="panel-h"><h3>Rekap Piutang (Invoice)</h3></div><div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Pelanggan</th><th>Tagihan</th><th>DP Masuk</th><th>Sisa</th><th>Status</th></tr></thead><tbody>${piutRows}</tbody></table></div></div>
    <div class="panel" style="margin:0"><div class="panel-h"><h3>DP Vendor per Kategori</h3></div><div style="padding:18px 19px">${catRows}</div></div>
  </div>`;
}
function keuAruskas(){
  const masuk=totalMasuk();const keluar=totalKeluar();const saldo=masuk-keluar;
  const komitmen=allVendor().reduce((a,d)=>a+vendorSisa(d),0);
  const inRows=allPiutang().map(p=>({p,paid:clientPaid(p)})).filter(x=>x.paid>0).sort((a,b)=>b.paid-a.paid).slice(0,10).map(x=>`<tr><td><div class="nm" style="font-weight:700">${esc(x.p.inst)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${x.p.tgl?dateID(x.p.tgl):'—'}</div></td><td class="price mono" style="color:var(--green)">+ ${jt(x.paid)}</td></tr>`).join('');
  const gajiCrew=totalGajiAssigned();
  const vpaid={};allVendor().forEach(d=>{const pd=vendorPaid(d);if(pd>0)vpaid[d.kat]=(vpaid[d.kat]||0)+pd;});
  if(gajiCrew>0)vpaid['Gaji Crew (TL & Media)']=gajiCrew;
  const catMax=Math.max(1,...Object.values(vpaid));
  const outRows=Object.entries(vpaid).sort((a,b)=>b[1]-a[1]).map(([k,v],i)=>`<div class="catrow"><div class="catnm" style="width:155px">${esc(k)}</div><div class="catbar"><div class="catfill" style="width:${v/catMax*100}%;background:${col(i)}"></div></div><div class="catval">${jt(v)}</div></div>`).join('')||'<div style="color:var(--muted);font-size:12.5px">Belum ada pengeluaran</div>';
  const mx=Math.max(masuk,keluar,1);
  return `<div class="cards fade" style="grid-template-columns:repeat(3,1fr)">
    <div class="scard"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19V5M5 12l7-7 7 7"/></svg></div><div class="lbl">Uang Masuk (pembayaran klien)</div><div class="val mono" style="color:var(--green)">${jt(masuk)}</div><div class="sub" style="color:var(--muted)">DP + pelunasan</div></div>
    <div class="scard"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12l7 7 7-7"/></svg></div><div class="lbl">Uang Keluar (vendor + gaji crew)</div><div class="val mono" style="color:var(--red)">${jt(keluar)}</div><div class="sub" style="color:var(--muted)">vendor ${jt(totalVendorKeluar())} · gaji crew ${jt(gajiCrew)} · komitmen ${jt(komitmen)}</div></div>
    <div class="scard" style="border-color:${saldo<0?'var(--red)':'var(--green)'}"><div class="ic ${saldo<0?'r':'gr'}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 10h18M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg></div><div class="lbl">Saldo Kas</div><div class="val mono" style="color:${saldo<0?'var(--red)':'var(--green)'}">${saldo<0?'- ':''}${jt(Math.abs(saldo))}</div><div class="sub" style="color:var(--muted)">masuk − keluar</div></div>
  </div>
  <div class="panel fade"><div class="panel-h"><h3>Masuk vs Keluar (aktual)</h3><button class="btn-acc ok" onclick="exportAruskasExcel()">⬇ Export Excel</button></div><div style="padding:18px 19px">
    <div class="catrow"><div class="catnm" style="width:120px;color:var(--green)">Uang Masuk</div><div class="catbar" style="height:14px"><div class="catfill" style="width:${masuk/mx*100}%;background:var(--green)"></div></div><div class="catval" style="width:90px">${jt(masuk)}</div></div>
    <div class="catrow"><div class="catnm" style="width:120px;color:var(--red)">Uang Keluar</div><div class="catbar" style="height:14px"><div class="catfill" style="width:${keluar/mx*100}%;background:var(--red)"></div></div><div class="catval" style="width:90px">${jt(keluar)}</div></div>
  </div></div>
  <div class="grid fade" style="grid-template-columns:1fr 1fr">
    <div class="panel" style="margin:0"><div class="panel-h"><h3>Uang Masuk — Pembayaran Klien</h3></div><div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Klien</th><th style="text-align:right">Total Dibayar</th></tr></thead><tbody>${inRows}</tbody></table></div></div>
    <div class="panel" style="margin:0"><div class="panel-h"><h3>Uang Keluar — per Kategori (dibayar)</h3></div><div style="padding:18px 19px">${outRows}</div></div>
  </div>
  <p style="font-size:12px;color:var(--muted-2);margin-top:14px">Arus kas = uang masuk dari pembayaran klien (Pelunasan), uang keluar dari pembayaran vendor (Jadwal Vendor) + gaji crew yang ditugaskan (tarif/hari × durasi trip).</p>`;
}
let pelFilter='semua';
function setPelFilter(f){pelFilter=f;renderKeu();}
function keuPelunasan(){
  const day=86400000;const allP=allPiutang().filter(p=>p.tagih>0||clientPaid(p)>0);
  const P=allP.filter(p=>pelFilter==='semua'||(pelFilter==='belum'?clientStatus(p)[0]!=='lunas':clientStatus(p)[0]==='lunas'))
    .sort((a,b)=>(clientStatus(a)[0]==='lunas'?1:0)-(clientStatus(b)[0]==='lunas'?1:0)||(b.tagih||0)-(a.tagih||0));
  const rows=P.map(p=>{const[sc,sl]=clientStatus(p);const paid=clientPaid(p);const sisa=clientSisa(p);
    const due=p.tgl?new Date(new Date(p.tgl)-7*day):null;
    const overdue=due&&today>due&&sc!=='lunas';
    const target=due?due.toLocaleDateString('id-ID',{day:'2-digit',month:'short'}):'—';
    const plist=payClientList(p.id);
    const termLabels=[];if(p.dp>0)termLabels.push('DP Awal');plist.forEach(x=>termLabels.push(x.termin||'DP'));
    const termText=termLabels.length?termLabels.join(', '):'Belum ada termin';
    const btn=`<button class="btn-acc no" style="margin-right:4px" onclick="genInvoicePDF('${p.id}')" title="Unduh invoice PDF">⬇ Invoice</button>`+(sc==='lunas'?`<button class="btn-acc no" onclick="openBayar('${p.id}')">Detail</button>`:`<button class="btn-acc ok" onclick="openBayar('${p.id}')">+ Bayar</button>`);
    return `<tr class="clk" onclick="openBayar('${p.id}')"><td><div class="nm" style="font-weight:700">${esc(p.inst)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${esc(p.inv)||'—'} · ${esc(termText)}</div></td><td class="mono">${jt(p.tagih)}</td><td class="mono" style="color:var(--green)">${paid?jt(paid):'—'}</td><td class="price mono">${sisa>0?jt(sisa):'<span style=color:var(--green)>Lunas</span>'}</td><td style="font-size:12.5px;${overdue?'color:var(--red);font-weight:700':'color:var(--muted)'}">${target}${overdue?' ⚠':''}</td><td><span class="pill ${sc}">${sl}</span></td><td style="text-align:right" onclick="event.stopPropagation()">${btn}</td></tr>`;}).join('');
  const lunasN=allP.filter(p=>clientStatus(p)[0]==='lunas').length;
  const jtN=allP.filter(p=>{const due=p.tgl?new Date(new Date(p.tgl)-7*day):null;return due&&today>due&&clientStatus(p)[0]!=='lunas';}).length;
  const pt=piutangTot();
  return `<div class="cards fade" style="grid-template-columns:repeat(4,1fr)">
    <div class="scard"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 12 5 5L20 7"/></svg></div><div class="lbl">Sudah Lunas</div><div class="val mono">${lunasN} <span style="font-size:14px;color:var(--muted)">/ ${allP.length}</span></div></div>
    <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19V5M5 12l7-7 7 7"/></svg></div><div class="lbl">Total DP Masuk</div><div class="val mono" style="color:var(--green)">${jt(pt.dp)}</div></div>
    <div class="scard"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div class="lbl">Sisa Piutang</div><div class="val mono">${jt(pt.sisa)}</div></div>
    <div class="scard" style="${jtN?'border-color:var(--red)':''}"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg></div><div class="lbl">Lewat Target (H-7)</div><div class="val mono" style="${jtN?'color:var(--red)':''}">${jtN}</div></div>
  </div>
  <div class="panel fade" style="margin:0"><div class="panel-h" style="flex-wrap:wrap;gap:8px"><h3>Status Pelunasan Klien</h3><div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap"><button class="btn-acc ok" onclick="openCreateInvoiceFromTrip()">+ Buat Tagihan dari Trip</button><button class="tab ${pelFilter==='semua'?'active':''}" onclick="setPelFilter('semua')">Semua (${allP.length})</button><button class="tab ${pelFilter==='belum'?'active':''}" onclick="setPelFilter('belum')">Belum Lunas (${allP.length-lunasN})</button><button class="tab ${pelFilter==='lunas'?'active':''}" onclick="setPelFilter('lunas')">Lunas (${lunasN})</button></div></div>
  <div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Pelanggan</th><th>Tagihan</th><th>Dibayar</th><th>Sisa</th><th>Target</th><th>Status</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${rows}</tbody></table></div></div>
  <p style="font-size:12px;color:var(--muted-2);margin-top:14px">Catat pembayaran bertahap (DP 1, DP 2, pelunasan). Setiap termin otomatis mengurangi sisa & menambah uang masuk di Arus Kas dan Aging Piutang.</p>`;
}
function openBayar(id){
  const p=allPiutang().find(x=>x.id===id);if(!p)return;
  const paid=clientPaid(p),sisa=clientSisa(p);const list=payClientList(p.id);
  const termOpts=['DP 1','DP 2','DP 3','DP 4','Pelunasan'];
  const termIdx=Math.min(termOpts.length-1,list.length+(p.dp>0?1:0));
  const nextTermin=termOpts[termIdx];
  const hist=[];
  if(p.dp>0)hist.push(`<div class="pay-row"><span>DP 1 (data awal)</span><b style="color:var(--green)">${jt(p.dp)}</b></div>`);
  list.forEach((x,i)=>hist.push(`<div class="pay-row"><span>${esc(x.termin)} · ${x.date}</span><b style="color:var(--green)">${jt(x.amount)}</b> <button class="pay-del" onclick="document.getElementById('bayarOv').remove();delClientPayment('${p.id}',${i});openBayar('${p.id}')">✕</button></div>`));
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='bayarOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:460px"><div class="pv-bar"><b>Pembayaran — ${esc(p.inst)}</b><div><button class="btn-acc ok" style="margin-right:6px" onclick="genInvoicePDF('${p.id}')">⬇ Invoice PDF</button><button class="btn-acc no" onclick="document.getElementById('bayarOv').remove()">Tutup</button></div></div>
    <div style="background:#fff;margin:16px;border-radius:10px;padding:18px">
      <div class="pay-sum"><div><span>Tagihan</span><b>${p.tagih>0?jt(p.tagih):'Belum diset'}</b><div style="margin-top:4px;display:flex;gap:4px;justify-content:center"><input id="b_tagih_edit" class="finput" type="number" style="width:105px;margin:0;padding:3px 6px;font-size:11px" value="${p.tagih||paid}" title="Edit total tagihan"><button class="btn-acc no" style="padding:2px 6px;font-size:11px" onclick="savePiutTagih('${p.id}',document.getElementById('b_tagih_edit').value);document.getElementById('bayarOv').remove();openBayar('${p.id}')">Set</button></div></div><div><span>Total DP Masuk</span><b style="color:var(--green)">${jt(paid)}</b></div><div><span>Sisa Piutang</span><b style="color:${sisa>0?'var(--red)':'var(--green)'}">${jt(sisa)}</b></div></div>
      <div class="pay-hist">${hist.join('')||'<div style="color:var(--muted);font-size:12.5px;text-align:center;padding:8px">Belum ada pembayaran</div>'}</div>
      ${(sisa>0||p.tagih<=0)?`<div style="border-top:1px solid var(--line);margin-top:12px;padding-top:12px">
        <div class="frow"><div><label class="flbl">Termin</label><select id="b_termin" class="finput">${termOpts.map(o=>`<option value="${o}" ${o===nextTermin?'selected':''}>${o}</option>`).join('')}</select></div><div><label class="flbl">Tanggal</label><input id="b_tgl" class="finput" type="date" value="${new Date().toISOString().slice(0,10)}"></div></div>
        <label class="flbl">Jumlah (Rp)</label><input id="b_amount" class="finput" type="number" placeholder="${sisa}" value="${sisa}">
        <div style="display:flex;gap:8px"><button class="btn-save" style="flex:1" onclick="submitBayar('${p.id}')">Catat Pembayaran</button><button class="btn-save" style="flex:1;background:var(--green)" onclick="document.getElementById('bayarOv').remove();markClientLunas('${p.id}')">✓ Tandai Lunas</button></div>
      </div>`:'<div style="text-align:center;color:var(--green);font-weight:700;padding:10px">✓ Lunas</div>'}
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function submitBayar(id){
  const amt=parseInt(document.getElementById('b_amount').value)||0;
  const termin=(document.getElementById('b_termin').value||'DP').trim();
  const tgl=document.getElementById('b_tgl').value;
  if(amt<=0){toast('Isi jumlah pembayaran');return;}
  addClientPayment(id,termin,amt,tgl);toast('Pembayaran dicatat: '+jt(amt));
  const ov=document.getElementById('bayarOv');if(ov)ov.remove();refreshActiveView();
}
const VCAT={'Transport / Bus':'var(--blue)','Hotel / Villa':'var(--teal)','Operasional / Lainnya':'var(--purple)','Aset & Perlengkapan':'var(--orange)','Kaos & Merchandise':'var(--gold-ink)','Wisata / Tiket':'var(--green)','Konsumsi / Katering':'var(--orange)'};
function vendDue(d){return (d.tgl&&d.tgl!=='-')?new Date(d.tgl):null;}
function ensureApprovedPrep(){
  penawaran().filter(p=>p.status==='approved'&&prepTrip(p.id).length===0).forEach(p=>prepAutoFill(p.id,true));
}
function keuJadwalVendor(){
  ensureApprovedPrep();
  const list=allVendor().map(d=>{const[sc,sl]=vendorStatusArr(d);return{...d,sc,sl,paid:vendorPaid(d),sisa:vendorSisa(d)};});
  const lunas=list.filter(d=>d.sc==='lunas'),belum=list.filter(d=>d.sc!=='lunas');
  const totPaid=list.reduce((a,d)=>a+d.paid,0),totSisa=list.reduce((a,d)=>a+d.sisa,0);
  const order=[...belum.sort((a,b)=>b.sisa-a.sisa),...lunas.sort((a,b)=>b.nom-a.nom)];
  const rows=order.map(d=>{const isL=d.sc==='lunas';const due=vendDue(d);const overdue=due&&today>due&&!isL;
    return `<tr class="clk" style="${isL?'opacity:.6':''}" onclick="openBayarVendor('${d.no}')"><td><div class="nm" style="font-weight:700">${esc(d.vendor)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${esc(d.ket).slice(0,38)}</div></td><td><span class="pill jadwal" style="background:${(VCAT[d.kat]||'#888')}1a;color:${VCAT[d.kat]||'#888'};font-size:11px">${esc(d.kat.split(' ')[0])}</span></td><td class="price mono">${jt(d.nom)}</td><td class="mono" style="color:var(--green)">${d.paid?jt(d.paid):'—'}</td><td class="price mono">${d.sisa>0?jt(d.sisa):'<span style=color:var(--green)>0</span>'}</td><td style="font-size:12px;${overdue?'color:var(--red);font-weight:700':'color:var(--muted)'}">${due?dateID(d.tgl):'—'}${overdue?' ⚠':''}</td><td><span class="pill ${d.sc}">${d.sl}</span></td><td style="text-align:right" onclick="event.stopPropagation()"><button class="btn-acc ${isL?'no':'ok'}" onclick="openBayarVendor('${d.no}')">${isL?'Detail':'+ Bayar'}</button></td></tr>`;}).join('');
  const overdueN=belum.filter(d=>{const due=vendDue(d);return due&&today>due;}).length;
  const prepList=allTrips().filter(t=>t.id&&(t._new||prepTrip(t.id).length>0||(piutMap()[t.id]&&clientPaid(piutMap()[t.id])>0)||(t.brk&&new Date(t.brk)>=today)))
    .sort((a,b)=>((b._new?1:0)-(a._new?1:0))||((prepTrip(b.id).length?1:0)-(prepTrip(a.id).length?1:0))||(a.brk<b.brk?-1:1)).slice(0,20);
  const prepRows=prepList.map(t=>{const n=prepTrip(t.id).length,tt=prepTotal(t.id),ss=prepSisa(t.id);const[psc,psl]=payStatus(t);
    return `<tr class="clk" onclick="openPrep('${t.id}')"><td><div class="nm" style="font-weight:700">${esc(t.inst)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${esc((t.dest||'').split('(')[0]).slice(0,34)}</div></td><td style="font-size:12.5px">${t.brk?dateID(t.brk):'—'}</td><td class="mono">${t.pax}</td><td><span class="pill ${psc}">${psl}</span></td><td>${n?`<span class="pill lunas">${n} item</span>`:'<span class="pill piutang">Belum diatur</span>'}</td><td class="mono">${n?rp(tt):'—'}</td><td class="mono" style="color:${ss>0?'var(--red)':'var(--green)'}">${n?(ss>0?rp(ss):'Lunas'):'—'}</td><td style="text-align:right" onclick="event.stopPropagation()"><button class="btn-acc ${n?'no':'ok'}" onclick="openPrep('${t.id}')">${n?'Kelola':'+ Atur'}</button></td></tr>`;}).join('');
  return `<div class="cards fade" style="grid-template-columns:repeat(4,1fr)">
    <div class="scard" style="border-color:var(--red)"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div class="lbl">Belum Dibayar</div><div class="val mono" style="color:var(--red)">${jt(totSisa)}</div><div class="sub" style="color:var(--muted)">${belum.length} transaksi</div></div>
    <div class="scard"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 12 5 5L20 7"/></svg></div><div class="lbl">Sudah Dibayar</div><div class="val mono" style="color:var(--green)">${jt(totPaid)}</div><div class="sub" style="color:var(--muted)">${lunas.length} lunas</div></div>
    <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h10"/></svg></div><div class="lbl">Total Komitmen</div><div class="val mono">${jt(totPaid+totSisa)}</div><div class="sub" style="color:var(--muted)">${list.length} transaksi</div></div>
    <div class="scard" style="${overdueN?'border-color:var(--red)':''}"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg></div><div class="lbl">Lewat Jatuh Tempo</div><div class="val mono" style="${overdueN?'color:var(--red)':''}">${overdueN}</div></div>
  </div>
  <div class="panel fade"><div class="panel-h"><h3>Persiapan Vendor per Trip</h3><span style="font-size:12px;color:var(--muted)">pilih armada, hotel, konsumsi, tiket untuk trip yang akan datang</span></div>
  <div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Trip</th><th>Berangkat</th><th>Pax</th><th>Bayar Klien</th><th>Kebutuhan</th><th>Total Vendor</th><th>Sisa Bayar</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${prepRows||'<tr><td colspan="8" style="color:var(--muted);font-size:12.5px">Tidak ada trip akan datang.</td></tr>'}</tbody></table></div></div>
  <div class="panel fade" style="margin:0"><div class="panel-h"><h3>Jadwal Pembayaran Vendor</h3><div style="display:flex;align-items:center;gap:10px"><span style="font-size:12px;color:var(--muted)">belum lunas di atas · klik baris untuk bayar</span></div></div>
  <div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Vendor / Keperluan</th><th>Kategori</th><th>Nominal</th><th>Dibayar</th><th>Sisa</th><th>Jatuh Tempo</th><th>Status</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${rows}</tbody></table></div></div>
  <p style="font-size:12px;color:var(--muted-2);margin-top:14px">Catat pembayaran vendor bertahap (bisa dicicil). Status: <b>Belum bayar</b> → <b>Sebagian</b> → <b>Lunas</b>. Jatuh tempo lewat ditandai merah. Tiap pembayaran menambah Uang Keluar di Arus Kas.</p>`;
}
function openBayarVendor(no){
  const d=allVendor().find(x=>x.no===no);if(!d)return;
  const old=document.getElementById('bayarOv');if(old)old.remove();
  const paid=vendorPaid(d),sisa=vendorSisa(d);const base=vendorBasePaid(d);const list=payVendorList(no);
  const termOpts=['DP 1','DP 2','DP 3','Pelunasan'];
  const defTerm=list.length===0&&base===0?'DP 1':(list.length===1?'DP 2':'Pelunasan');
  const dp30=Math.round((d.nom||0)*0.3), dp50=Math.round((d.nom||0)*0.5);
  const hist=[];
  if(base>0)hist.push(`<div class="pay-row"><span>Sudah dibayar (dari data)</span><b style="color:var(--green)">${jt(base)}</b></div>`);
  list.forEach((x,i)=>hist.push(`<div class="pay-row"><span>${x.date}${x.ket?' · '+esc(x.ket):''}</span><b style="color:var(--green)">${jt(x.amount)}</b> <button class="pay-del" onclick="delVendorPayment('${no}',${i});openBayarVendor('${no}')">✕</button></div>`));
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='bayarOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:480px"><div class="pv-bar"><b>Bayar Vendor — ${esc(d.vendor)}</b><button class="btn-acc no" onclick="document.getElementById('bayarOv').remove()">Tutup</button></div>
    <div style="background:#fff;margin:16px;border-radius:10px;padding:18px">
      <div style="font-size:12px;color:var(--muted);margin-bottom:10px">${esc(d.ket)} · ${esc(d.kat)}</div>
      <div class="pay-sum"><div><span>Nominal</span><b>${jt(d.nom)}</b></div><div><span>Dibayar</span><b style="color:var(--green)">${jt(paid)}</b></div><div><span>Sisa</span><b style="color:${sisa>0?'var(--red)':'var(--green)'}">${jt(sisa)}</b></div></div>
      <div class="pay-hist">${hist.join('')||'<div style="color:var(--muted);font-size:12.5px;text-align:center;padding:8px">Belum ada pembayaran</div>'}</div>
      ${base>0?'<div style="font-size:11px;color:var(--muted);margin-top:8px">Transaksi ini sudah lunas di data awal.</div>':(sisa>0?`<div style="border-top:1px solid var(--line);margin-top:12px;padding-top:12px">
        <div class="frow">
          <div><label class="flbl">Jenis Pembayaran</label><select id="bv_jenis" class="finput">${termOpts.map(o=>`<option value="${o}" ${o===defTerm?'selected':''}>${o}</option>`).join('')}</select></div>
          <div><label class="flbl">Tanggal</label><input id="bv_tgl" class="finput" type="date" value="${new Date().toISOString().slice(0,10)}"></div>
        </div>
        <label class="flbl">Keterangan (opsional)</label><input id="bv_ket" class="finput" placeholder="mis. transfer BCA">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
          <label class="flbl" style="margin:0">Jumlah Bayar (Rp)</label>
          <div style="display:flex;gap:4px">
            ${dp30>0&&dp30<sisa?`<button type="button" class="btn-acc no" style="padding:2px 7px;font-size:11px" onclick="document.getElementById('bv_jenis').value='DP 1';document.getElementById('bv_amount').value=${dp30}">DP 30%</button>`:''}
            ${dp50>0&&dp50<sisa?`<button type="button" class="btn-acc no" style="padding:2px 7px;font-size:11px" onclick="document.getElementById('bv_jenis').value='DP 1';document.getElementById('bv_amount').value=${dp50}">DP 50%</button>`:''}
            <button type="button" class="btn-acc no" style="padding:2px 7px;font-size:11px" onclick="document.getElementById('bv_jenis').value='Pelunasan';document.getElementById('bv_amount').value=${sisa}">100%</button>
          </div>
        </div>
        <input id="bv_amount" class="finput" type="number" value="${defTerm==='DP 1'&&dp30>0&&dp30<sisa?dp30:sisa}">
        <div style="display:flex;gap:8px;margin-top:4px">
          <button class="btn-save" style="flex:1" onclick="submitBayarVendor('${no}')">✓ Catat Pembayaran</button>
          <button class="btn-save" style="flex:1;background:var(--green)" onclick="document.getElementById('bv_jenis').value='Pelunasan';document.getElementById('bv_amount').value=${sisa};submitBayarVendor('${no}')">Lunasi Semua (${jt(sisa)})</button>
        </div>
      </div>`:'<div style="text-align:center;color:var(--green);font-weight:700;padding:10px">✓ Lunas</div>')}
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function submitBayarVendor(no){
  const amt=parseInt(document.getElementById('bv_amount').value)||0;
  if(amt<=0){toast('Isi jumlah pembayaran');return;}
  const jenis=(document.getElementById('bv_jenis')?document.getElementById('bv_jenis').value:'DP');
  const note=(document.getElementById('bv_ket').value||'').trim();
  const ket=note?(jenis+' · '+note):jenis;
  addVendorPayment(no,amt,document.getElementById('bv_tgl').value,ket);
  toast('Pembayaran vendor dicatat ('+jenis+'): '+jt(amt));
  const ov=document.getElementById('bayarOv');if(ov)ov.remove();refreshActiveView();
}
// ---------- MODAL PERSIAPAN VENDOR ----------
function prepUnitOpts(kat,sel){
  const customOpt='<option value="__custom__|0">✎ Input Vendor &amp; Harga Custom...</option>';
  if(kat==='Konsumsi / Katering'){
    const meals=[['Nasi Box Standar',25000],['Nasi Box Premium',35000],['Makan Prasmanan',45000],['Snack Box',15000]];
    return meals.map(([n,p])=>`<option value="${esc(n)}|${p}" ${n===sel?'selected':''}>${esc(n)} (${rp(p)}/porsi)</option>`).join('')+customOpt;
  }
  const s=(PREPKAT.find(k=>k[0]===kat)||[])[1];
  if(!s)return '';
  if(s==='hotels'){const regions=[...new Set(CAT.hotels.map(h=>h.region))];
    return regions.map(r=>`<optgroup label="${esc(r)}">`+CAT.hotels.filter(h=>h.region===r).map(h=>`<option value="${esc(h.name)}|${h.wd}" ${h.name===sel?'selected':''}>${esc(h.name)} (${rp(h.wd)}/kamar)</option>`).join('')+'</optgroup>').join('')+customOpt;}
  if(s==='dests'){const cities=[...new Set(CAT.dests.map(d=>d.city))];
    return cities.map(c=>`<optgroup label="${esc(c)}">`+CAT.dests.filter(d=>d.city===c).map(d=>`<option value="${esc(d.name)}|${d.price}" ${d.name===sel?'selected':''}>${esc(d.name)} (${rp(d.price)}/pax)</option>`).join('')+'</optgroup>').join('')+customOpt;}
  if(s==='armada')return CAT.armada.map(a=>`<option value="${esc(a.name)}|${a.rate}" ${a.name===sel?'selected':''}>${esc(a.name)} (${rp(a.rate)}/bus/hari)</option>`).join('')+customOpt;
  if(s==='kaos')return CAT.kaos.filter(k=>k.price>0).map(k=>`<option value="${esc(k.name)}|${k.price}" ${k.name===sel?'selected':''}>${esc(k.name)} (${rp(k.price)}/pax)</option>`).join('')+customOpt;
  return '';
}
function prepQtyDefault(kat,t){
  const hari=tripDays(t),pax=t.pax||0,malam=t.malam!=null?t.malam:Math.max(0,hari-1);
  const bus=Math.max(1,t.bus||1),kmr=Math.ceil(pax/(t.share||4));
  if(kat==='Transport / Bus')return bus*hari;
  if(kat==='Hotel / Villa')return malam>0?(malam*kmr):0;
  if(kat==='Konsumsi / Katering'){const mf=t.mFreq!=null?t.mFreq:(hari===1?1:3);return pax*mf;}
  if(kat==='Kaos & Merchandise')return pax;
  if(kat==='Wisata / Tiket')return pax;
  return 1;
}
function prepKetDefault(kat,t){
  const hari=tripDays(t),pax=t.pax||0,malam=t.malam!=null?t.malam:Math.max(0,hari-1);
  const bus=Math.max(1,t.bus||1),kmr=Math.ceil(pax/(t.share||4));
  if(kat==='Transport / Bus')return bus+' bus × '+hari+' hari';
  if(kat==='Hotel / Villa')return malam>0?(kmr+' kamar × '+malam+' malam'):'Tanpa inap (0 malam)';
  if(kat==='Konsumsi / Katering'){const mf=t.mFreq!=null?t.mFreq:(hari===1?1:3);return pax+' pax × '+mf+' makan';}
  if(kat==='Kaos & Merchandise')return pax+' pcs';
  if(kat==='Wisata / Tiket')return pax+' pax';
  return '1 unit';
}
function prepQtyLabel(kat){
  return kat==='Transport / Bus'?'bus × hari':kat==='Hotel / Villa'?'kamar × malam':kat==='Konsumsi / Katering'?'porsi (pax × frekuensi)':kat==='Kaos & Merchandise'?'pcs':kat==='Wisata / Tiket'?'tiket (pax)':'qty';
}
function onPrepHotelShare(tripId){
  const t=allTrips().find(x=>x.id===tripId);if(!t)return;
  const sh=+(document.getElementById('pp_hotel_share')||{}).value||(t.share||4);
  const hari=tripDays(t),pax=t.pax||0,malam=t.malam!=null?t.malam:Math.max(0,hari-1);
  const kmr=Math.ceil(pax/sh);
  document.getElementById('pp_qty').value=malam>0?(kmr*malam):0;
  document.getElementById('pp_ket').value=malam>0?(kmr+' kamar (isi '+sh+' org, '+pax+' pax) × '+malam+' malam'):'Tanpa inap (0 malam)';
  prepCalcTotal();
}
function onPrepBusChange(tripId){
  const t=allTrips().find(x=>x.id===tripId);if(!t)return;
  const v=document.getElementById('pp_vendor');if(!v||!v.value)return;
  const busName=String(v.value).split('|')[0];
  if(busName==='__custom__')return;
  const seat=kapasitas(busName)||45;
  const hari=tripDays(t),pax=t.pax||0;
  const unitBus=pax>0?Math.ceil(pax/seat):Math.max(1,t.bus||1);
  document.getElementById('pp_qty').value=unitBus*hari;
  document.getElementById('pp_ket').value=unitBus+' bus ('+seat+' seat, '+pax+' pax) × '+hari+' hari';
  prepCalcTotal();
}
function onPrepKat(tripId){
  const t=allTrips().find(x=>x.id===tripId);if(!t)return;
  const kat=document.getElementById('pp_kat').value;
  const opts=prepUnitOpts(kat,'');
  const vw=document.getElementById('pp_vwrap');
  const shDef=t.share||4;
  const shareHTML=kat==='Hotel / Villa'?`<div style="margin-bottom:8px"><label class="flbl">Kamar Isi Berapa Orang</label><select id="pp_hotel_share" class="finput" style="margin:4px 0 0" onchange="onPrepHotelShare('${tripId}')">
    <option value="4" ${shDef==4?'selected':''}>Isi 4 orang / kamar (Quad Share)</option>
    <option value="3" ${shDef==3?'selected':''}>Isi 3 orang / kamar (Triple Share)</option>
    <option value="2" ${shDef==2?'selected':''}>Isi 2 orang / kamar (Twin Share)</option>
    <option value="1" ${shDef==1?'selected':''}>Isi 1 orang / kamar (Single)</option>
  </select></div>`:'';
  vw.innerHTML=opts?`<label class="flbl">Pilih dari Data (${esc(kat)})</label><select id="pp_vendor" class="finput" style="margin:4px 0 8px" onchange="onPrepVendor('${tripId}')">${opts}</select>
    ${shareHTML}
    <div id="pp_custom_wrap" style="display:none;margin-bottom:8px"><label class="flbl">Nama Vendor / Item Custom</label><input id="pp_vendor_custom" class="finput" style="margin:4px 0 0" placeholder="mis. PO Bus Khusus / Hotel Lokal"></div>`
    :`<label class="flbl">Vendor / Keperluan</label><input id="pp_vendor" class="finput" style="margin:4px 0 8px" placeholder="mis. Tol, parkir, dokumentasi drone">`;
  document.getElementById('pp_qlbl').textContent='('+prepQtyLabel(kat)+')';
  document.getElementById('pp_qty').value=prepQtyDefault(kat,t);
  document.getElementById('pp_ket').value=prepKetDefault(kat,t);
  document.getElementById('pp_due').value=dminus(t.brk,PREPDUE[kat]||7);
  const cp=document.getElementById('pp_custom_price');if(cp)cp.checked=false;
  if(opts)onPrepVendor(tripId);else{document.getElementById('pp_unit').value=0;prepCalcTotal();}
  if(kat==='Hotel / Villa')onPrepHotelShare(tripId);
}
function onPrepVendor(tripId){
  const v=document.getElementById('pp_vendor');if(!v||!v.value)return;
  const parts=String(v.value).split('|');
  const cw=document.getElementById('pp_custom_wrap');
  const isCustom=parts[0]==='__custom__';
  if(cw)cw.style.display=isCustom?'block':'none';
  const cp=document.getElementById('pp_custom_price');
  if(isCustom){if(cp)cp.checked=true;document.getElementById('pp_unit').value='';}
  else if((!cp||!cp.checked)&&parts.length>1){document.getElementById('pp_unit').value=parts[1];}
  const kat=(document.getElementById('pp_kat')||{}).value;
  if(kat==='Transport / Bus'&&tripId)onPrepBusChange(tripId);
  prepCalcTotal();
}
function onToggleCustomPrice(){
  const cp=document.getElementById('pp_custom_price');
  if(cp&&!cp.checked)onPrepVendor();
}
function prepCalcTotal(){
  const q=+(document.getElementById('pp_qty')||{}).value||0,u=+(document.getElementById('pp_unit')||{}).value||0;
  const el=document.getElementById('pp_total');if(el)el.textContent=rp(q*u);
}
function submitPrep(tripId){
  const kat=document.getElementById('pp_kat').value;
  const vEl=document.getElementById('pp_vendor');
  const parts=vEl?String(vEl.value||'').split('|'):[''];
  let vendor=parts[0]==='__custom__'?((document.getElementById('pp_vendor_custom')||{}).value||'').trim():parts[0];
  if(!vendor){toast('Pilih atau isi nama vendor dulu');return;}
  const qty=+document.getElementById('pp_qty').value||0,unit=+document.getElementById('pp_unit').value||0;
  if(qty<=0||unit<=0){toast('Isi jumlah & harga satuan');return;}
  const ket=(document.getElementById('pp_ket')?document.getElementById('pp_ket').value.trim():'')||(prepQtyLabel(kat)+': '+qty);
  prepAdd(tripId,kat,vendor,ket,qty,unit,document.getElementById('pp_due').value);
  toast('Kebutuhan ditambah: '+vendor);openPrep(tripId);
}
function prepAutoFill(tripId,silent){
  const t=allTrips().find(x=>x.id===tripId);if(!t)return;
  if(prepTrip(tripId).length){if(!silent)toast('Sudah ada data persiapan');return;}
  const hari=tripDays(t),pax=t.pax||0,malam=t.malam!=null?t.malam:Math.max(0,hari-1);
  const isWe=t.brk&&[0,6].includes(new Date(t.brk).getDay());
  const busQty=Math.max(1,t.bus||1)*hari;
  const arm=t.armada?{name:t.armada,rate:t.armRate||((CAT.armada.find(a=>a.name===t.armada)||{}).rate||2500000)}:(CAT.armada.find(a=>kapasitas(a.name)>=Math.ceil(pax/Math.max(1,(t.bus||1))))||CAT.armada[CAT.armada.length-1]);
  prepAdd(tripId,'Transport / Bus',arm.name,(t.bus||1)+' unit × '+hari+' hari',busQty,arm.rate,dminus(t.brk,14));
  if(malam>0){
    const htName=t.hotel||CAT.hotels[0].name;
    const htFound=CAT.hotels.find(h=>htName.includes(h.name));
    const htRate=t.hotelRate||(htFound?(isWe?htFound.we:htFound.wd):CAT.hotels[0].wd);
    const kmr=Math.ceil(pax/4)*malam;
    prepAdd(tripId,'Hotel / Villa',htFound?htFound.name:htName,Math.ceil(pax/4)+' kamar × '+malam+' malam',kmr,htRate,dminus(t.brk,14));
  }
  if(pax>0){
    const mf=t.mFreq!=null?t.mFreq:3, mp=t.mPrice||25000;
    if(mf>0)prepAdd(tripId,'Konsumsi / Katering','Katering / Konsumsi',mf+'× makan × '+pax+' pax',pax*mf,mp,dminus(t.brk,7));
  }
  if(t.kaosRate>0&&pax>0){
    prepAdd(tripId,'Kaos & Merchandise',t.kaosName||'Kaos Peserta',pax+' pcs',pax,t.kaosRate,dminus(t.brk,7));
  }
  if(t.dests&&t.dests.length&&pax>0){
    t.dests.forEach(d=>{if(d.price>0)prepAdd(tripId,'Wisata / Tiket',d.name,'Tiket × '+pax+' pax',pax,d.price,dminus(t.brk,7));});
  }else if(pax>0){
    prepAdd(tripId,'Wisata / Tiket','Tiket masuk wisata',pax+' pax',pax,30000,dminus(t.brk,7));
  }
  if(!silent){toast('Draf persiapan dibuat sesuai data trip');openPrep(tripId);}
}
function prepTimelineHTML(t){
  return PREPTL.map(([n,ttl,desc])=>{const d=dminus(t.brk,n);const dt=d?new Date(d):null;
    const lewat=dt&&today>dt,kini=dt&&Math.abs(today-dt)<86400000;
    return `<div class="tl-item ${lewat?'done':''}"><div class="tl-dot" style="background:${lewat?'var(--green)':kini?'var(--gold)':'var(--line2,#d8d8d8)'}"></div>
      <div class="tl-body"><div class="tl-top"><b>H-${n} · ${ttl}</b><span class="tl-date" style="${lewat?'color:var(--green)':kini?'color:var(--gold-ink);font-weight:700':''}">${d?dateID(d):'—'}${lewat?' ✓':kini?' ← hari ini':''}</span></div><p>${desc}</p></div></div>`;}).join('');
}
function openPrep(tripId){
  const t=allTrips().find(x=>x.id===tripId);if(!t)return;
  const old=document.getElementById('prepOv');if(old)old.remove();
  const items=prepTrip(tripId);const tot=prepTotal(tripId),paid=prepPaid(tripId),sisa=prepSisa(tripId);
  const rows=items.map(x=>{const vd=vendorPaid({no:x.id,nom:x.nom,status:''});const vs=Math.max(0,x.nom-vd);
    const due=x.due?new Date(x.due):null;const over=due&&today>due&&vs>0;
    return `<div class="pp-row"><div class="pp-main"><span class="pill jadwal" style="background:${(VCAT[x.kat]||'#888')}1a;color:${VCAT[x.kat]||'#888'};font-size:10.5px">${esc(x.kat.split(' ')[0])}</span>
        <div class="pp-nm">${esc(x.vendor)}</div><div class="pp-sub">${esc(x.ket)} · <input type="number" class="finput" style="display:inline-block;width:100px;margin:0;padding:2px 6px;font-size:11.5px" value="${x.unit}" title="Edit harga satuan custom" onchange="prepEditUnit('${tripId}','${x.id}',this.value);openPrep('${tripId}')">/unit${x.due?' · tempo '+dateID(x.due):''}${over?' <b style=color:var(--red)>⚠ lewat</b>':''}</div></div>
      <div class="pp-num"><b>${rp(x.nom)}</b><span style="color:${vs===0?'var(--green)':(vd>0?'var(--gold-ink)':'var(--red)')}">${vs===0?'✓ Lunas':(vd>0?'DP '+rp(vd)+' · sisa '+rp(vs):'Belum bayar · sisa '+rp(vs))}</span></div>
      <div class="pp-act"><button class="btn-acc ${vs>0?'ok':'no'}" onclick="document.getElementById('prepOv').remove();openBayarVendor('${x.id}')">${vs>0?'Bayar':'Detail'}</button><button class="pay-del" onclick="prepDel('${tripId}','${x.id}');openPrep('${tripId}')">✕</button></div></div>`;}).join('');
  const katOpts=PREPKAT.map(([k])=>`<option value="${esc(k)}">${esc(k)}</option>`).join('');
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='prepOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:650px"><div class="pv-bar"><b>Persiapan Vendor — ${esc(t.inst)}</b><button class="btn-acc no" onclick="document.getElementById('prepOv').remove()">Tutup</button></div>
    <div style="background:var(--bg);padding:16px;max-height:80vh;overflow:auto">
      <div class="pay-sum" style="margin-bottom:14px"><div><span>Total Kebutuhan</span><b>${rp(tot)}</b></div><div><span>Sudah Dibayar</span><b style="color:var(--green)">${rp(paid)}</b></div><div><span>Sisa</span><b style="color:${sisa>0?'var(--red)':'var(--green)'}">${rp(sisa)}</b></div></div>
      <div class="td-card"><h5>Kebutuhan Vendor ${items.length?`(${items.length})`:''}</h5>
        ${rows||`<div style="font-size:12.5px;color:var(--muted);padding:4px 0 8px">Belum ada kebutuhan. Gunakan <b>Isi Otomatis</b> atau tambah manual di bawah.</div>
        <button class="btn-save" onclick="prepAutoFill('${tripId}')">⚡ Isi Otomatis dari Data Trip</button>`}
      </div>
      <div class="td-card"><h5>Tambah Kebutuhan Manual (Data Katalog / Harga Custom)</h5>
        <div style="font-size:11.5px;color:var(--blue);background:#eef4ff;padding:6px 10px;border-radius:7px;margin-bottom:10px">Data paket trip: <b>${t.pax||0} pax</b> · <b>${tripDays(t)} hari</b> (${t.malam!=null?t.malam:Math.max(0,tripDays(t)-1)} malam) · <b>${Math.max(1,t.bus||1)} bus</b></div>
        <div class="frow">
          <div><label class="flbl">Kategori</label><select id="pp_kat" class="finput" style="margin:4px 0 8px" onchange="onPrepKat('${tripId}')">${katOpts}</select></div>
          <div><label class="flbl">Keterangan</label><input id="pp_ket" class="finput" style="margin:4px 0 8px" placeholder="mis. 1 bus × 2 hari"></div>
        </div>
        <div id="pp_vwrap"></div>
        <label style="display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--muted);margin:2px 0 8px;cursor:pointer"><input type="checkbox" id="pp_custom_price" onchange="onToggleCustomPrice()"> Gunakan harga custom (tidak ikut harga katalog)</label>
        <div class="frow"><div><label class="flbl">Jumlah <span id="pp_qlbl" style="color:var(--muted);font-weight:400"></span></label><input id="pp_qty" class="finput" type="number" oninput="prepCalcTotal()"></div>
          <div><label class="flbl">Harga Satuan (Rp)</label><input id="pp_unit" class="finput" type="number" oninput="document.getElementById('pp_custom_price').checked=true;prepCalcTotal()"></div></div>
        <div class="frow"><div><label class="flbl">Jatuh Tempo Bayar</label><input id="pp_due" class="finput" type="date"></div>
          <div><label class="flbl">Total</label><div class="finput" style="background:#f4f6fa;font-weight:800" id="pp_total">Rp 0</div></div></div>
        <button class="btn-save" style="margin-top:8px" onclick="submitPrep('${tripId}')">+ Tambah ke Persiapan</button>
      </div>
      <details class="td-card" style="cursor:pointer"><summary style="font-size:12.5px;font-weight:700;color:var(--muted)">Timeline Persiapan · ${t.pax} pax · ${tripDays(t)} hari · berangkat ${dateID(t.brk)}</summary><div class="tl" style="margin-top:10px">${prepTimelineHTML(t)}</div></details>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
  onPrepKat(tripId);
}
let profitMonth='semua',profitQ='',profitPage=1;
function setProfitMonth(m){profitMonth=m;profitPage=1;renderKeu();}
function setProfitQ(q){profitQ=q;profitPage=1;renderKeu();}
function setProfitPage(p){profitPage=p;renderKeu();}
function tripFinanceRow(t){
  const p=piutMap()[t.id];
  const masuk=p?clientPaid(p):0, tagih=p?(p.tagih||0):0;
  const vends=allVendor().filter(d=>d.trip===t.id);
  const vendNom=vends.reduce((s,d)=>s+(d.nom||0),0);
  const vendPaid=vends.reduce((s,d)=>s+vendorPaid(d),0);
  const vendSisa=Math.max(0,vendNom-vendPaid);
  const gaji=tripGaji(t);
  const reimbs=reimburseList().filter(r=>r.tripId===t.id&&r.status==='approved');
  const reimb=reimbs.reduce((s,r)=>s+(r.nominal||0),0);
  const keluar=vendNom+gaji+reimb;
  const kasKeluar=vendPaid+gaji+reimb;
  const labaKotor=masuk-vendNom;
  const labaBersih=labaKotor-gaji-reimb;
  return {t,p,masuk,tagih,vendNom,vendPaid,vendSisa,gaji,reimb,keluar,kasKeluar,labaKotor,labaBersih,vends,reimbs};
}
function openTripFinanceDetail(id){
  const t=allTrips().find(x=>x.id===id);if(!t)return;
  const f=tripFinanceRow(t);const a=tripAssign(t.id);const hari=tripDays(t);
  const old=document.getElementById('tripFinOv');if(old)old.remove();
  const inRows=f.p?((f.p.dp>0?`<div class="td-row"><span>DP Awal</span><b style="color:var(--green)">${rp(f.p.dp)}</b></div>`:'')+
    payClientList(f.p.id).map(x=>`<div class="td-row"><span>${esc(x.termin)} (${x.date?dateID(x.date):'—'})</span><b style="color:var(--green)">${rp(x.amount)}</b></div>`).join('')):'';
  const vendRows=f.vends.map(d=>{const pd=vendorPaid(d),ss=Math.max(0,(d.nom||0)-pd);return `<div class="td-row"><span>Vendor: ${esc(d.vendor)} (${esc((d.kat||'').split(' ')[0])}) <em style="font-size:11px;color:${ss>0?'var(--red)':'var(--green)'}">[${ss>0?'dibayar '+rp(pd):'lunas'}]</em></span><b style="color:var(--red)">${rp(d.nom||0)}</b></div>`;}).join('');
  const crewRows=a.tls.concat(a.medias).map(x=>{const c=crewById(x.id);if(!c)return '';return `<div class="td-row"><span>Crew: ${esc(c.nama)} (${esc(c.peran)} · ${rp(x.tarif)}×${hari}hr)</span><b style="color:var(--red)">${rp((+x.tarif||0)*hari)}</b></div>`;}).join('');
  const reimbRows=f.reimbs.map(r=>`<div class="td-row"><span>Reimburse: ${esc(r.item)}</span><b style="color:var(--red)">${rp(r.nominal)}</b></div>`).join('');
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='tripFinOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:560px"><div class="pv-bar"><b>Laporan Keuangan Trip — ${esc(t.inst)}</b><div><button class="btn-acc ok" style="margin-right:6px" onclick="document.getElementById('tripFinOv').remove();openTripDetail('${t.id}')">Detail Trip</button><button class="btn-acc no" onclick="document.getElementById('tripFinOv').remove()">Tutup</button></div></div>
    <div style="background:var(--bg);padding:16px;max-height:78vh;overflow:auto">
      <div class="pay-sum" style="margin-bottom:12px">
        <div><span>Uang Masuk</span><b style="color:var(--green)">${rp(f.masuk)}</b></div>
        <div><span>Total Biaya / Keluar</span><b style="color:var(--red)">${rp(f.keluar)}</b></div>
        <div><span>Laba Bersih</span><b style="color:${f.labaBersih<0?'var(--red)':'var(--green)'}">${rp(f.labaBersih)}</b></div>
      </div>
      <div class="td-card"><h5>Ringkasan Laba</h5>
        <div class="td-row"><span>Tanggal &amp; Tujuan</span><b>${t.brk?dateID(t.brk):'—'} · ${esc((t.dest||'').split('(')[0])}</b></div>
        <div class="td-row"><span>Tagihan Klien</span><b>${f.tagih?rp(f.tagih):'—'}</b></div>
        <div class="td-row"><span>Biaya Vendor (Persiapan)</span><b style="color:var(--red)">${rp(f.vendNom)} <span style="font-size:11px;color:var(--muted)">(dibayar ${rp(f.vendPaid)})</span></b></div>
        <div class="td-row"><span>Laba Kotor (Masuk − Vendor)</span><b style="color:${f.labaKotor<0?'var(--red)':'var(--blue)'}">${rp(f.labaKotor)}</b></div>
        <div class="td-row"><span>Laba Bersih (− Crew &amp; Reimburse)</span><b style="color:${f.labaBersih<0?'var(--red)':'var(--green)'}">${rp(f.labaBersih)}</b></div>
        <div class="td-row"><span>Estimasi Laba Persiapan</span><b>${rp(t.laba||0)}</b></div>
      </div>
      <div class="td-card"><h5>Rincian Uang Masuk (${rp(f.masuk)})</h5>${inRows||'<div style="font-size:12px;color:var(--muted)">Belum ada pembayaran klien tercatat</div>'}</div>
      <div class="td-card"><h5>Rincian Biaya &amp; Uang Keluar (${rp(f.keluar)})</h5>${(vendRows+crewRows+reimbRows)||'<div style="font-size:12px;color:var(--muted)">Belum ada biaya vendor atau crew tercatat</div>'}</div>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function keuProfit(){
  const trips=allTrips().filter(t=>t.id);
  const totLaba=trips.reduce((a,t)=>a+(t.laba||0),0);
  const totGaji=trips.reduce((a,t)=>a+tripGaji(t),0);
  const labaBersih=totLaba-totGaji;
  const withLaba=trips.filter(t=>t.laba!==0);
  const rugi=trips.filter(t=>/Rugi|Selisih/i.test(t.status)||(t.laba-tripGaji(t))<0);
  const avg=withLaba.length?labaBersih/withLaba.length:0;
  const rekTrips=trips.filter(t=>t.labaRekap);const totRek=rekTrips.reduce((a,t)=>a+t.labaRekap,0);
  // per daerah
  const reg={};trips.forEach(t=>{const d=(t.dest||'').split('(')[0].trim();if(!d||d==='-')return;reg[d]=(reg[d]||0)+t.laba;});
  const topReg=Object.entries(reg).filter(([k,v])=>v>0).sort((a,b)=>b[1]-a[1]).slice(0,8);
  const regMax=topReg.length?topReg[0][1]:1;
  const regRows=topReg.map(([k,v],i)=>`<div class="catrow"><div class="catnm" style="width:150px">${esc(k)}</div><div class="catbar"><div class="catfill" style="width:${v/regMax*100}%;background:${col(i)}"></div></div><div class="catval" style="width:84px">${jt(v)}</div></div>`).join('');
  // per jenis
  const jen={};trips.forEach(t=>{const j=t.jenis||'Lainnya';if(!jen[j])jen[j]={laba:0,n:0};jen[j].laba+=t.laba;jen[j].n++;});
  const jenRows=Object.entries(jen).sort((a,b)=>b[1].laba-a[1].laba).map(([k,v])=>`<tr><td style="font-weight:600">${esc(k)}</td><td class="mono">${v.n}</td><td class="price mono">${jt(v.laba)}</td><td class="mono" style="color:var(--muted)">${jt(v.laba/v.n)}</td></tr>`).join('');
  // top & rugi trips
  const top=[...withLaba].sort((a,b)=>b.laba-a.laba).slice(0,5);
  const topRows=top.map(t=>`<tr><td><div class="nm" style="font-weight:700">${esc(t.inst)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${esc((t.dest||'').split('(')[0])}</div></td><td class="price mono" style="color:var(--green)">${jt(t.laba)}</td></tr>`).join('');
  const rugiRows=rugi.length?rugi.map(t=>`<tr><td><div class="nm" style="font-weight:700">${esc(t.inst)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${esc((t.dest||'').split('(')[0])}</div></td><td class="price mono" style="color:var(--red)">${t.laba<0?jt(t.laba):esc(t.status)}</td></tr>`).join(''):`<tr><td colspan="2" style="text-align:center;color:var(--muted);padding:20px">Tidak ada trip rugi 🎉</td></tr>`;
  const months=[...new Set(trips.filter(t=>t.brk).map(t=>String(t.brk).slice(0,7)))].sort();
  const mOpts='<option value="semua">Semua Bulan</option>'+months.map(ym=>{const d=new Date(ym+'-01');const lbl=isNaN(d)?ym:(MONTH_NAMES[d.getMonth()]+' '+d.getFullYear());return `<option value="${ym}" ${profitMonth===ym?'selected':''}>${lbl}</option>`;}).join('');
  const ql=profitQ.trim().toLowerCase();
  const filtTrips=trips.filter(t=>(profitMonth==='semua'||String(t.brk||'').slice(0,7)===profitMonth)&&(!ql||(t.inst||'').toLowerCase().includes(ql)||(t.dest||'').toLowerCase().includes(ql)));
  const finRows=filtTrips.map(tripFinanceRow);
  const sumIn=finRows.reduce((s,f)=>s+f.masuk,0), sumOut=finRows.reduce((s,f)=>s+f.keluar,0);
  const sumKotor=finRows.reduce((s,f)=>s+f.labaKotor,0), sumBersih=finRows.reduce((s,f)=>s+f.labaBersih,0);
  const PER_P=15;
  const pageFin=pageSlice(finRows,profitPage,PER_P);
  const tripFinRowsHTML=pageFin.map(f=>{
    const t=f.t;const outSub=[f.vendNom?'Vnd '+jt(f.vendNom):'',f.gaji?'Crew '+jt(f.gaji):'',f.reimb?'Rmb '+jt(f.reimb):''].filter(Boolean).join(' · ')||'—';
    return `<tr class="clk" onclick="openTripFinanceDetail('${t.id}')">
      <td><div class="nm" style="font-weight:700">${esc(t.inst)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${t.brk?dateID(t.brk):'—'} · ${esc((t.dest||'').split('(')[0])}</div></td>
      <td class="price mono" style="color:var(--green)">${f.masuk?rp(f.masuk):'<span style="color:var(--muted-2)">Rp 0</span>'}${f.tagih?`<div style="font-size:10.5px;color:var(--muted)">tagih ${jt(f.tagih)}</div>`:''}</td>
      <td class="price mono" style="color:var(--red)">${f.keluar?rp(f.keluar):'<span style="color:var(--muted-2)">Rp 0</span>'}<div style="font-size:10.5px;color:var(--muted)">${outSub}</div></td>
      <td class="price mono" style="color:${f.labaKotor<0?'var(--red)':'var(--blue)'}">${rp(f.labaKotor)}</td>
      <td class="price mono" style="font-weight:700;color:${f.labaBersih<0?'var(--red)':'var(--green)'}">${rp(f.labaBersih)}${t.laba?`<div style="font-size:10.5px;color:var(--muted);font-weight:400">est. ${jt(t.laba)}</div>`:''}</td>
    </tr>`;}).join('')||'<tr><td colspan="5" style="text-align:center;color:var(--muted);padding:20px">Tidak ada trip sesuai filter</td></tr>';
  return `<div class="cards fade" style="grid-template-columns:repeat(4,1fr)">
    <div class="scard"><div class="ic b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 10h18M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg></div><div class="lbl">Laba Kotor (Persiapan)</div><div class="val mono">${jt(totLaba)}</div><div class="sub" style="color:var(--muted)">${withLaba.length} trip · gaji crew −${jt(totGaji)}</div></div>
    <div class="scard"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19V5M5 12l7-7 7 7"/></svg></div><div class="lbl">Laba Bersih (− Gaji Crew)</div><div class="val mono">${jt(labaBersih)}</div><div class="sub up">rata-rata ${jt(avg)} / trip</div></div>
    <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 12 5 5L20 7"/></svg></div><div class="lbl">Laba Rekap Final</div><div class="val mono">${jt(totRek)}</div><div class="sub" style="color:var(--muted)">terisi ${rekTrips.length} trip</div></div>
    <div class="scard" style="${rugi.length?'border-color:var(--red)':''}"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg></div><div class="lbl">Trip Rugi / Selisih</div><div class="val mono" style="${rugi.length?'color:var(--red)':''}">${rugi.length} <span style="font-size:14px;color:var(--muted)">trip</span></div></div>
  </div>
  <div class="panel fade">
    <div class="panel-h" style="flex-wrap:wrap;gap:10px">
      <div><h3>Laporan Keuangan per Trip <span style="color:var(--muted);font-size:12px">(${filtTrips.length} trip)</span></h3></div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
        <input class="finput" style="width:180px;margin:0;padding:6px 10px;font-size:12.5px" placeholder="Cari instansi / tujuan..." value="${esc(profitQ)}" onchange="setProfitQ(this.value)">
        <select class="finput" style="width:auto;margin:0;padding:6px 10px;font-size:12.5px" onchange="setProfitMonth(this.value)">${mOpts}</select>
      </div>
    </div>
    <div class="pay-sum" style="margin:10px 19px 4px;grid-template-columns:repeat(4,1fr)">
      <div><span>Total Uang Masuk</span><b style="color:var(--green)">${jt(sumIn)}</b></div>
      <div><span>Total Uang Keluar</span><b style="color:var(--red)">${jt(sumOut)}</b></div>
      <div><span>Total Laba Kotor</span><b style="color:${sumKotor<0?'var(--red)':'var(--blue)'}">${jt(sumKotor)}</b></div>
      <div><span>Total Laba Bersih</span><b style="color:${sumBersih<0?'var(--red)':'var(--green)'}">${jt(sumBersih)}</b></div>
    </div>
    <div class="tbl-scroll"><table style="margin-top:8px"><thead><tr><th>Trip &amp; Tanggal</th><th>Uang Masuk</th><th>Uang Keluar</th><th>Laba Kotor</th><th>Laba Bersih</th></tr></thead><tbody>${tripFinRowsHTML}</tbody></table></div>
    ${pagerHTML(finRows.length,profitPage,PER_P,'setProfitPage')}
  </div>
  <div class="grid fade" style="grid-template-columns:1fr 1fr">
    <div class="panel" style="margin:0"><div class="panel-h"><h3>Laba per Daerah <span style="font-size:12px;color:var(--muted)">(top 8)</span></h3></div><div style="padding:18px 19px">${regRows}</div></div>
    <div class="panel" style="margin:0"><div class="panel-h"><h3>Laba per Jenis Layanan</h3></div><div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Jenis</th><th>Trip</th><th>Total Laba</th><th>Rata/Trip</th></tr></thead><tbody>${jenRows}</tbody></table></div></div>
  </div>
  <div class="grid fade" style="grid-template-columns:1fr 1fr">
    <div class="panel" style="margin:0"><div class="panel-h"><h3>5 Trip Paling Untung</h3></div><div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Trip</th><th style="text-align:right">Laba</th></tr></thead><tbody>${topRows}</tbody></table></div></div>
    <div class="panel" style="margin:0"><div class="panel-h"><h3>Trip Rugi / Perlu Dicek</h3></div><div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Trip</th><th style="text-align:right">Keterangan</th></tr></thead><tbody>${rugiRows}</tbody></table></div></div>
  </div>
  <p style="font-size:12px;color:var(--muted-2);margin-top:14px">Laba per sales belum bisa ditampilkan karena data trip belum menandai sales penanggung jawab — muncul otomatis setelah area Sales aktif. "Laba Rekap Final" baru terisi di ${rekTrips.length} trip; sisanya memakai laba persiapan.</p>`;
}
function keuAging(){
  const day=86400000;
  const items=allPiutang().map(p=>({...p,sisa:clientSisa(p)})).filter(p=>p.sisa>0);
  function bucket(p){if(!p.tgl)return 3;const d=Math.floor((today-new Date(p.tgl))/day);if(d<=0)return 0;if(d<=30)return 1;if(d<=60)return 2;return 3;}
  const B=[{k:'Belum jatuh tempo',c:'var(--blue)',pill:'jadwal'},{k:'Lewat 1–30 hari',c:'var(--gold-ink)',pill:'dp'},{k:'Lewat 31–60 hari',c:'var(--orange)',pill:'dp'},{k:'Lewat > 60 hari',c:'var(--red)',pill:'piutang'}];
  const sums=[0,0,0,0],cnts=[0,0,0,0];items.forEach(p=>{const b=bucket(p);sums[b]+=p.sisa;cnts[b]++;});
  const cards=B.map((b,i)=>`<div class="scard"><div class="lbl" style="font-weight:700;color:${b.c}">${b.k}</div><div class="val mono">${sums[i]?jt(sums[i]):'Rp 0'}</div><div class="sub" style="color:var(--muted)">${cnts[i]} invoice</div></div>`).join('');
  const rows=items.map(p=>({...p,b:bucket(p),days:p.tgl?Math.floor((today-new Date(p.tgl))/day):null})).sort((a,b)=>b.b-a.b||b.sisa-a.sisa).map(p=>{const bb=B[p.b];const ket=p.b===0?'Jatuh tempo '+(p.tgl?dateID(p.tgl):'—'):(p.days+' hari lalu');
    return `<tr class="clk" onclick="openBayar('${p.id}')"><td><div class="nm" style="font-weight:700">${esc(p.inst)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${esc(p.inv)||'—'}</div></td><td>${p.tgl?dateID(p.tgl):'—'}</td><td class="price mono">${jt(p.sisa)}</td><td style="font-size:12.5px;color:${bb.c};font-weight:600">${ket}</td><td><span class="pill ${bb.pill}">${bb.k.replace('Lewat ','').replace('Belum jatuh tempo','Belum JT')}</span></td><td style="text-align:right" onclick="event.stopPropagation()"><button class="btn-acc ok" onclick="openBayar('${p.id}')">Bayar</button></td></tr>`;}).join('');
  const tot=sums.reduce((a,b)=>a+b,0);
  return `<div class="cards fade" style="grid-template-columns:repeat(4,1fr)">${cards}</div>
  <div class="panel fade" style="margin:0"><div class="panel-h"><h3>Rincian Piutang per Umur <span style="color:var(--muted);font-size:13px">(total ${jt(tot)})</span></h3><button class="btn-acc ok" onclick="exportAgingExcel()">⬇ Export Excel</button></div>
  <div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Pelanggan</th><th>Tgl Trip</th><th>Sisa Piutang</th><th>Umur</th><th>Status</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${rows}</tbody></table></div></div>
  <p style="font-size:12px;color:var(--muted-2);margin-top:14px">Umur dihitung dari tanggal trip (patokan pelunasan) terhadap hari ini. Klik baris untuk catat pembayaran — sisa langsung berkurang di semua tab. Hanya invoice dengan sisa &gt; 0 yang tampil.</p>`;
}
function xlsxStamp(){return new Date().toISOString().slice(0,10);}
function exportAruskasExcel(){
  if(!window.XLSX){toast('Gagal memuat modul Excel, coba lagi');return;}
  const masuk=totalMasuk(),keluar=totalKeluar(),saldo=masuk-keluar;
  const komitmen=allVendor().reduce((a,d)=>a+vendorSisa(d),0);
  const gaji=totalGajiCrew();
  const ring=[['ARUS KAS — RINGKASAN',''],['Diekspor',new Date().toLocaleDateString('id-ID',{day:'2-digit',month:'long',year:'numeric'})],[''],
    ['Uang Masuk (pembayaran klien)',masuk],['Uang Keluar (dibayar ke vendor)',keluar],['Saldo Kas',saldo],
    ['Komitmen vendor (belum dibayar)',komitmen],['Gaji crew (trip berjalan)',gaji]];
  const masukRows=[['Klien','No. Invoice','Tanggal Trip','Total Dibayar (Rp)']];
  allPiutang().forEach(p=>{const paid=clientPaid(p);if(paid>0)masukRows.push([p.inst,p.inv||'-',p.tgl?dateID(p.tgl):'-',paid]);});
  const keluarRows=[['Kategori','Vendor','No','Keterangan','Nominal Kontrak (Rp)','Dibayar (Rp)','Sisa (Rp)']];
  allVendor().forEach(d=>{const pd=vendorPaid(d);if(pd>0)keluarRows.push([d.kat||'-',d.vendor||'-',d.no||'-',d.ket||'-',d.nom||0,pd,vendorSisa(d)]);});
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(ring),'Ringkasan');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(masukRows),'Uang Masuk (Klien)');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(keluarRows),'Uang Keluar (Vendor)');
  XLSX.writeFile(wb,'Havist_ArusKas_'+xlsxStamp()+'.xlsx');
  toast('Arus Kas diekspor ke Excel');
}
function exportAgingExcel(){
  if(!window.XLSX){toast('Gagal memuat modul Excel, coba lagi');return;}
  const day=86400000;
  const items=allPiutang().map(p=>({...p,sisa:clientSisa(p)})).filter(p=>p.sisa>0);
  function bucket(p){if(!p.tgl)return 3;const d=Math.floor((today-new Date(p.tgl))/day);if(d<=0)return 0;if(d<=30)return 1;if(d<=60)return 2;return 3;}
  const BL=['Belum jatuh tempo','Lewat 1–30 hari','Lewat 31–60 hari','Lewat > 60 hari'];
  const rows=[['Pelanggan','No. Invoice','Tanggal Trip','Sisa Piutang (Rp)','Umur (hari)','Kelompok Umur']];
  items.map(p=>({...p,b:bucket(p),days:p.tgl?Math.floor((today-new Date(p.tgl))/day):null})).sort((a,b)=>b.b-a.b||b.sisa-a.sisa).forEach(p=>{
    rows.push([p.inst,p.inv||'-',p.tgl?dateID(p.tgl):'-',p.sisa,p.days==null?'-':p.days,BL[p.b]]);
  });
  const tot=items.reduce((a,p)=>a+p.sisa,0);
  rows.push(['','','TOTAL',tot,'','']);
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet([['AGING PIUTANG'],['Diekspor',new Date().toLocaleDateString('id-ID',{day:'2-digit',month:'long',year:'numeric'})],['']].concat(rows)),'Aging Piutang');
  XLSX.writeFile(wb,'Havist_AgingPiutang_'+xlsxStamp()+'.xlsx');
  toast('Aging Piutang diekspor ke Excel');
}
function xlsStampRow(judul){return [[judul],['Diekspor',new Date().toLocaleDateString('id-ID',{day:'2-digit',month:'long',year:'numeric'})],['']];}
function xlsRowsRingkasanTotal(){
  const m=monthAgg(),pt=piutangTot(),cat=dpCat();
  const totLaba=Object.values(m).reduce((a,b)=>a+b.laba,0);
  return xlsStampRow('RINGKASAN KEUANGAN').concat([
    ['Total Laba Tercatat',totLaba],['Total DP Masuk',pt.dp],['Sisa Piutang',pt.sisa],
    ['Pengeluaran DP Vendor',Object.values(cat).reduce((a,b)=>a+b,0)]]);
}
function xlsRowsKinerjaBulan(){
  const m=monthAgg();const rows=[['Bulan','Jumlah Trip','Pax','Bus','Laba Persiapan (Rp)']];
  MONTHS.forEach(k=>rows.push([k.slice(8),m[k].n,m[k].pax,m[k].bus,m[k].laba]));
  return rows;
}
function xlsRowsPiutangRekap(){
  const rows=[['Pelanggan','No Invoice','Tagihan (Rp)','DP Masuk (Rp)','Sisa (Rp)','Status']];
  allPiutang().filter(p=>p.tagih>0).forEach(p=>{const paid=clientPaid(p),sisa=clientSisa(p);rows.push([p.inst,p.inv||'-',p.tagih,paid,sisa,clientStatus(p)[1]]);});
  return rows;
}
function xlsRowsDPVendorKategori(){
  const cat=dpCat();const rows=[['Kategori','Total DP (Rp)']];
  Object.entries(cat).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>rows.push([k,v]));
  return rows;
}
function exportRingkasanExcel(){
  if(!window.XLSX){toast('Gagal memuat modul Excel, coba lagi');return;}
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsRingkasanTotal()),'Ringkasan');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsKinerjaBulan()),'Kinerja per Bulan');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsPiutangRekap()),'Rekap Piutang');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsDPVendorKategori()),'DP Vendor per Kategori');
  XLSX.writeFile(wb,'Havist_RingkasanKeuangan_'+xlsxStamp()+'.xlsx');
  toast('Ringkasan Keuangan diekspor ke Excel');
}
function xlsRowsPelunasan(){
  const day=86400000;const P=allPiutang().filter(p=>p.tagih>0);
  const rows=[['Pelanggan','No Invoice','Tagihan (Rp)','Dibayar (Rp)','Sisa (Rp)','Target H-7','Status','Jumlah Termin']];
  P.forEach(p=>{const[,sl]=clientStatus(p);const paid=clientPaid(p),sisa=clientSisa(p);
    const due=p.tgl?new Date(new Date(p.tgl)-7*day):null;
    const termN=(p.dp>0?1:0)+payClientList(p.id).length;
    rows.push([p.inst,p.inv||'-',p.tagih,paid,sisa,due?dateID(due):'-',sl,termN]);
  });
  return rows;
}
function exportPelunasanExcel(){
  if(!window.XLSX){toast('Gagal memuat modul Excel, coba lagi');return;}
  const pt=piutangTot();
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsStampRow('PELUNASAN KLIEN').concat([['Total DP Masuk',pt.dp],['Sisa Piutang',pt.sisa]])),'Ringkasan');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsPelunasan()),'Pelunasan Klien');
  XLSX.writeFile(wb,'Havist_PelunasanKlien_'+xlsxStamp()+'.xlsx');
  toast('Pelunasan Klien diekspor ke Excel');
}
function xlsRowsVendor(){
  const list=allVendor().map(d=>{const[,sl]=vendorStatusArr(d);return{...d,sl,paid:vendorPaid(d),sisa:vendorSisa(d)};});
  const rows=[['Kategori','Vendor','No','Keterangan','Nominal (Rp)','Dibayar (Rp)','Sisa (Rp)','Jatuh Tempo','Status']];
  list.forEach(d=>rows.push([d.kat||'-',d.vendor||'-',d.no||'-',d.ket||'-',d.nom||0,d.paid,d.sisa,vendDue(d)?dateID(d.tgl):'-',d.sl]));
  return rows;
}
function exportVendorExcel(){
  if(!window.XLSX){toast('Gagal memuat modul Excel, coba lagi');return;}
  const list=allVendor().map(d=>({...d,paid:vendorPaid(d),sisa:vendorSisa(d)}));
  const totPaid=list.reduce((a,d)=>a+d.paid,0),totSisa=list.reduce((a,d)=>a+d.sisa,0);
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsStampRow('JADWAL VENDOR').concat([['Sudah Dibayar',totPaid],['Belum Dibayar',totSisa],['Total Komitmen',totPaid+totSisa]])),'Ringkasan');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsVendor()),'Jadwal Vendor');
  XLSX.writeFile(wb,'Havist_JadwalVendor_'+xlsxStamp()+'.xlsx');
  toast('Jadwal Vendor diekspor ke Excel');
}
function xlsRowsProfitDaerah(){
  const reg={};allTrips().filter(t=>t.id).forEach(t=>{const d=(t.dest||'').split('(')[0].trim();if(!d||d==='-')return;reg[d]=(reg[d]||0)+t.laba;});
  const rows=[['Daerah','Total Laba (Rp)']];
  Object.entries(reg).filter(([,v])=>v>0).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>rows.push([k,v]));
  return rows;
}
function xlsRowsProfitJenis(){
  const jen={};allTrips().filter(t=>t.id).forEach(t=>{const j=t.jenis||'Lainnya';if(!jen[j])jen[j]={laba:0,n:0};jen[j].laba+=t.laba;jen[j].n++;});
  const rows=[['Jenis Layanan','Jumlah Trip','Total Laba (Rp)','Rata-rata/Trip (Rp)']];
  Object.entries(jen).sort((a,b)=>b[1].laba-a[1].laba).forEach(([k,v])=>rows.push([k,v.n,v.laba,Math.round(v.laba/v.n)]));
  return rows;
}
function xlsRowsProfitTripRows(trips){
  const rows=[['Trip / Instansi','Daerah','Laba / Keterangan (Rp)']];
  trips.forEach(t=>rows.push([t.inst,(t.dest||'').split('(')[0].trim()||'-',t.laba]));
  return rows;
}
function exportProfitExcel(){
  if(!window.XLSX){toast('Gagal memuat modul Excel, coba lagi');return;}
  const trips=allTrips().filter(t=>t.id);
  const totLaba=trips.reduce((a,t)=>a+t.laba,0);
  const withLaba=trips.filter(t=>t.laba!==0);
  const rugi=trips.filter(t=>/Rugi|Selisih/i.test(t.status)||t.laba<0);
  const avg=withLaba.length?totLaba/withLaba.length:0;
  const top=[...withLaba].sort((a,b)=>b.laba-a.laba).slice(0,10);
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsStampRow('PROFITABILITAS').concat([['Total Laba (Persiapan)',totLaba],['Rata-rata / Trip',Math.round(avg)],['Trip Rugi / Selisih',rugi.length]])),'Ringkasan');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsProfitDaerah()),'Laba per Daerah');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsProfitJenis()),'Laba per Jenis');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsProfitTripRows(top)),'Top 10 Trip');
  if(rugi.length)XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsProfitTripRows(rugi)),'Trip Rugi');
  XLSX.writeFile(wb,'Havist_Profitabilitas_'+xlsxStamp()+'.xlsx');
  toast('Profitabilitas diekspor ke Excel');
}
function xlsRowsReimburse(){
  const rows=[['Crew','Trip','Item','Keterangan','Nominal (Rp)','Tanggal','Status']];
  reimburseList().sort((a,b)=>b.createdAt-a.createdAt).forEach(r=>{const t=allTrips().find(x=>x.id===r.tripId);
    const plabel=r.status==='approved'?'Disetujui':r.status==='rejected'?'Ditolak':'Menunggu';
    rows.push([r.crewName,t?t.inst:'(trip dihapus)',r.item,r.ket||'-',r.nominal,dateID(r.tgl),plabel]);
  });
  return rows;
}
function exportReimburseExcel(){
  if(!window.XLSX){toast('Gagal memuat modul Excel, coba lagi');return;}
  const list=reimburseList();
  const pend=list.filter(r=>r.status==='pending'),appr=list.filter(r=>r.status==='approved'),rej=list.filter(r=>r.status==='rejected');
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsStampRow('REIMBURSE LAPANGAN').concat([['Menunggu Persetujuan',pend.length],['Disetujui',appr.length],['Ditolak',rej.length]])),'Ringkasan');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsReimburse()),'Reimburse Lapangan');
  XLSX.writeFile(wb,'Havist_Reimburse_'+xlsxStamp()+'.xlsx');
  toast('Reimburse Lapangan diekspor ke Excel');
}
function exportAllKeuanganExcel(){
  if(!window.XLSX){toast('Gagal memuat modul Excel, coba lagi');return;}
  const masuk=totalMasuk(),keluar=totalKeluar();
  const komitmen=allVendor().reduce((a,d)=>a+vendorSisa(d),0),gaji=totalGajiCrew();
  const masukRows=[['Klien','No. Invoice','Tanggal Trip','Total Dibayar (Rp)']];
  allPiutang().forEach(p=>{const paid=clientPaid(p);if(paid>0)masukRows.push([p.inst,p.inv||'-',p.tgl?dateID(p.tgl):'-',paid]);});
  const keluarRows=[['Kategori','Vendor','No','Keterangan','Nominal Kontrak (Rp)','Dibayar (Rp)','Sisa (Rp)']];
  allVendor().forEach(d=>{const pd=vendorPaid(d);if(pd>0)keluarRows.push([d.kat||'-',d.vendor||'-',d.no||'-',d.ket||'-',d.nom||0,pd,vendorSisa(d)]);});
  const day=86400000;const agItems=allPiutang().map(p=>({...p,sisa:clientSisa(p)})).filter(p=>p.sisa>0);
  function bucket(p){if(!p.tgl)return 3;const d=Math.floor((today-new Date(p.tgl))/day);if(d<=0)return 0;if(d<=30)return 1;if(d<=60)return 2;return 3;}
  const BL=['Belum jatuh tempo','Lewat 1–30 hari','Lewat 31–60 hari','Lewat > 60 hari'];
  const agingRows=[['Pelanggan','No. Invoice','Tanggal Trip','Sisa Piutang (Rp)','Umur (hari)','Kelompok Umur']];
  agItems.map(p=>({...p,b:bucket(p),days:p.tgl?Math.floor((today-new Date(p.tgl))/day):null})).sort((a,b)=>b.b-a.b||b.sisa-a.sisa).forEach(p=>agingRows.push([p.inst,p.inv||'-',p.tgl?dateID(p.tgl):'-',p.sisa,p.days==null?'-':p.days,BL[p.b]]));
  const trips=allTrips().filter(t=>t.id);
  const totLabaP=trips.reduce((a,t)=>a+t.laba,0);
  const rugi=trips.filter(t=>/Rugi|Selisih/i.test(t.status)||t.laba<0);
  const pt=piutangTot();
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsStampRow('LAPORAN KEUANGAN LENGKAP — HAVIST TRAVELLER').concat([
    ['Uang Masuk (kas, pembayaran klien)',masuk],['Uang Keluar (kas, dibayar ke vendor)',keluar],['Saldo Kas',masuk-keluar],
    ['Komitmen vendor (belum dibayar)',komitmen],['Gaji crew (trip berjalan)',gaji],
    ['Total Laba Tercatat (persiapan)',totLabaP],['Total DP Masuk (piutang)',pt.dp],['Sisa Piutang',pt.sisa],['Trip Rugi/Selisih',rugi.length]])),'Ringkasan');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsKinerjaBulan()),'Kinerja per Bulan');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(masukRows),'Arus Kas - Masuk');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(keluarRows),'Arus Kas - Keluar');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(agingRows),'Aging Piutang');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsPelunasan()),'Pelunasan Klien');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsVendor()),'Jadwal Vendor');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsProfitDaerah()),'Laba per Daerah');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsProfitJenis()),'Laba per Jenis');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsRowsReimburse()),'Reimburse Lapangan');
  XLSX.writeFile(wb,'Havist_LaporanKeuanganLengkap_'+xlsxStamp()+'.xlsx');
  toast('Semua laporan keuangan diekspor ke 1 file Excel (10 sheet)');
}

// ===== MODE IMPOR & SINKRON EXCEL (.xlsx pure JS, zero CDN) =====
async function unzipEntries(buf){
  const u8=new Uint8Array(buf),dv=new DataView(buf);
  let eocd=-1;for(let i=u8.length-22;i>=Math.max(0,u8.length-65557);i--){if(dv.getUint32(i,true)===0x06054b50){eocd=i;break;}}
  if(eocd<0)throw new Error('File bukan arsip .xlsx yang valid');
  const cdSize=dv.getUint32(eocd+12,true),cdOff=dv.getUint32(eocd+16,true),entries={};
  let p=cdOff;
  while(p<cdOff+cdSize){
    if(dv.getUint32(p,true)!==0x02014b50)break;
    const method=dv.getUint16(p+10,true),csize=dv.getUint32(p+20,true),nlen=dv.getUint16(p+28,true),elen=dv.getUint16(p+30,true),clen=dv.getUint16(p+32,true),lhoff=dv.getUint32(p+42,true);
    const name=new TextDecoder().decode(u8.slice(p+46,p+46+nlen));
    const lnlen=dv.getUint16(lhoff+26,true),lelen=dv.getUint16(lhoff+28,true),dataOff=lhoff+30+lnlen+lelen;
    const raw=u8.slice(dataOff,dataOff+csize);
    if(method===0){entries[name]=raw;}
    else if(method===8){
      if(typeof DecompressionStream==='undefined')throw new Error('Browser tidak mendukung DecompressionStream untuk membaca .xlsx terkompresi');
      const ds=new DecompressionStream('deflate-raw');
      const ab=await new Response(new Blob([raw]).stream().pipeThrough(ds)).arrayBuffer();
      entries[name]=new Uint8Array(ab);
    }
    p+=46+nlen+elen+clen;
  }
  return entries;
}
function xmlDecode(s){return String(s||'').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;|&apos;/g,"'");}
function colLettersToIdx(ref){const m=/^([A-Z]+)/.exec(ref||'');if(!m)return 0;let n=0;for(let i=0;i<m[1].length;i++)n=n*26+(m[1].charCodeAt(i)-64);return n-1;}
function parseSharedStrings(xml){
  const out=[];if(!xml)return out;
  const re=/<si>([\s\S]*?)<\/si>/g;let m;
  while((m=re.exec(xml))){const ts=[...m[1].matchAll(/<t[^>]*>([\s\S]*?)<\/t>/g)].map(x=>xmlDecode(x[1]));out.push(ts.join(''));}
  return out;
}
function parseSheetRows(xml,sst){
  const rows=[];const rRe=/<row[^>]*>([\s\S]*?)<\/row>/g;let rm;
  while((rm=rRe.exec(xml))){
    const row=[];const cRe=/<c\b([^>]*)>([\s\S]*?)<\/c>/g;let cm;
    while((cm=cRe.exec(rm[1]))){
      const attrs=cm[1],body=cm[2];
      const refM=/\br="([^"]+)"/.exec(attrs),tM=/\bt="([^"]+)"/.exec(attrs);
      const col=refM?colLettersToIdx(refM[1]):row.length;
      const typ=tM?tM[1]:'';
      let val='';
      if(typ==='inlineStr'){const tm=/<t[^>]*>([\s\S]*?)<\/t>/.exec(body);val=tm?xmlDecode(tm[1]):'';}
      else{const vm=/<v[^>]*>([\s\S]*?)<\/v>/.exec(body);val=vm?vm[1]:'';if(typ==='s')val=sst[+val]??'';else if(typ!=='str'&&val!==''&&!isNaN(+val))val=+val;}
      row[col]=val;
    }
    rows.push(row);
  }
  return rows;
}
async function readXlsxSheets(buf){
  const entries=await unzipEntries(buf),dec=new TextDecoder();
  const sst=entries['xl/sharedStrings.xml']?parseSharedStrings(dec.decode(entries['xl/sharedStrings.xml'])):[];
  const wbXml=dec.decode(entries['xl/workbook.xml']||'');
  const relsXml=dec.decode(entries['xl/_rels/workbook.xml.rels']||'');
  const relMap={};for(const m of relsXml.matchAll(/<Relationship[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"/g)){relMap[m[1]]=m[2].replace(/^\//,'');}
  const sheets={};
  for(const m of wbXml.matchAll(/<sheet\b([^>]+)\/?>/g)){
    const attrs=m[1],nmM=/\bname="([^"]+)"/.exec(attrs),ridM=/\br:id="([^"]+)"/.exec(attrs);
    if(!nmM||!ridM)continue;
    let tgt=relMap[ridM[1]]||'';if(!tgt.startsWith('xl/'))tgt='xl/'+tgt.replace(/^\.\//,'');
    if(entries[tgt])sheets[xmlDecode(nmM[1])]=parseSheetRows(dec.decode(entries[tgt]),sst);
  }
  return sheets;
}
function excelDateISO(v){
  if(v===''||v==null)return '';
  if(typeof v==='number'&&v>20000&&v<80000){const d=new Date(Math.round((v-25569)*86400000));return isNaN(d)?'':d.toISOString().slice(0,10);}
  const s=String(v).trim();
  if(/^\d{4}-\d{2}-\d{2}/.test(s))return s.slice(0,10);
  const d=new Date(s);return isNaN(d)?'':d.toISOString().slice(0,10);
}
function excelNum(v){if(typeof v==='number')return Math.round(v);return Math.round(Number(String(v||'').replace(/[^\d.-]/g,''))||0);}
function exportSyncTemplateExcel(){
  if(!window.XLSX){toast('Modul Excel belum siap');return;}
  const tripRows=[['ID','Instansi','Destinasi','Tgl_Berangkat','Tgl_Pulang','Pax','Bus','Laba_Persiapan','Status_Trip']];
  allTrips().forEach(t=>tripRows.push([t.id,t.inst||'',t.dest||'',t.brk||'',t.pul||'',t.pax||0,t.bus||0,t.laba||0,STLBL[tripStatus(t)]||'Akan Datang']));
  const piutRows=[['ID_Trip','Instansi','No_Invoice','Tagihan','DP_1','Tgl_DP_1','DP_2','Tgl_DP_2','DP_3','Tgl_DP_3','DP_4','Tgl_DP_4','Pelunasan','Tgl_Pelunasan']];
  allPiutang().filter(p=>p.tagih>0||p.id).forEach(p=>{
    const pays=[];if(p.dp>0)pays.push({termin:'DP 1',amount:p.dp,date:p.tgl||''});
    payClientList(p.id).forEach(x=>pays.push(x));
    const slot=n=>pays[n]?[pays[n].amount||0,pays[n].date||'']:[0,''];
    const s0=slot(0),s1=slot(1),s2=slot(2),s3=slot(3),s4=slot(4);
    piutRows.push([p.id,p.inst||'',p.inv||'',p.tagih||0,s0[0],s0[1],s1[0],s1[1],s2[0],s2[1],s3[0],s3[1],s4[0],s4[1]]);
  });
  const vendRows=[['No_Transaksi','ID_Trip','Kategori','Vendor','Keterangan','Nominal','Sudah_Dibayar','Tgl_Bayar','Jatuh_Tempo']];
  allVendor().forEach(d=>{
    const list=payVendorList(d.no);const lastDate=list.length?list[list.length-1].date:'';
    vendRows.push([d.no,d.trip||'',d.kat||'',d.vendor||'',d.ket||'',d.nom||0,vendorPaid(d),lastDate,d.tgl&&d.tgl!=='-'?d.tgl:'']);
  });
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(tripRows),'Trips');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(piutRows),'Pelunasan_Klien');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(vendRows),'Jadwal_Vendor');
  XLSX.writeFile(wb,'Havist_Template_Sinkron_'+xlsxStamp()+'.xlsx');
  toast('Template sinkron Excel diunduh (3 sheet)');
}
function rowsToObjects(rows){
  if(!rows||rows.length<2)return [];
  const hdr=rows[0].map(h=>String(h||'').trim());
  return rows.slice(1).filter(r=>r.some(c=>c!==''&&c!=null)).map(r=>{const o={};hdr.forEach((h,i)=>{if(h)o[h]=r[i]??'';});return o;});
}
let pendingSyncPlan=null;
function buildExcelSyncPlan(sheets){
  const curTrips=new Map(allTrips().map(t=>[String(t.id),t]));
  const curPiut=new Map(allPiutang().map(p=>[String(p.id),p]));
  const curVend=new Map(allVendor().map(d=>[String(d.no),d]));
  const plan={trips:[],piutang:[],vendor:[],stats:{tNew:0,tUpd:0,pNew:0,pUpd:0,vNew:0,vUpd:0}};
  rowsToObjects(sheets['Trips']).forEach((r,idx)=>{
    const inst=String(r.Instansi||'').trim();if(!inst)return;
    const id=String(r.ID||'').trim()||('XLS-T-'+Date.now()+'-'+idx);
    if(curTrips.has(id))plan.stats.tUpd++;else plan.stats.tNew++;
    const stRaw=String(r.Status_Trip||'').toLowerCase();
    const stCode=stRaw.includes('selesai')?'selesai':stRaw.includes('langsung')?'berlangsung':'akan';
    plan.trips.push({id,inst,dest:String(r.Destinasi||'').trim(),brk:excelDateISO(r.Tgl_Berangkat),pul:excelDateISO(r.Tgl_Pulang),pax:excelNum(r.Pax),bus:excelNum(r.Bus),laba:excelNum(r.Laba_Persiapan),_stCode:stCode,_excel:true});
  });
  rowsToObjects(sheets['Pelunasan_Klien']).forEach((r,idx)=>{
    const inst=String(r.Instansi||'').trim();if(!inst)return;
    const id=String(r.ID_Trip||'').trim()||('XLS-P-'+Date.now()+'-'+idx);
    if(curPiut.has(id))plan.stats.pUpd++;else plan.stats.pNew++;
    const terms=[];
    [['DP 1',r.DP_1,r.Tgl_DP_1],['DP 2',r.DP_2,r.Tgl_DP_2],['DP 3',r.DP_3,r.Tgl_DP_3],['DP 4',r.DP_4,r.Tgl_DP_4],['Pelunasan',r.Pelunasan,r.Tgl_Pelunasan]].forEach(([lbl,amt,dt])=>{
      const a=excelNum(amt);if(a>0)terms.push({termin:lbl,amount:a,date:excelDateISO(dt)||new Date().toISOString().slice(0,10)});
    });
    const tripMatch=plan.trips.find(t=>t.id===id)||curTrips.get(id);
    plan.piutang.push({id,inst,inv:String(r.No_Invoice||'').trim()||'(dari Excel)',tagih:excelNum(r.Tagihan),pax:tripMatch?tripMatch.pax:0,tgl:tripMatch?tripMatch.brk:'',dp:0,_terms:terms,_excel:true});
  });
  rowsToObjects(sheets['Jadwal_Vendor']).forEach((r,idx)=>{
    const vendor=String(r.Vendor||'').trim();if(!vendor)return;
    const no=String(r.No_Transaksi||'').trim()||('XLS-V-'+Date.now()+'-'+idx);
    if(curVend.has(no))plan.stats.vUpd++;else plan.stats.vNew++;
    const paid=excelNum(r.Sudah_Dibayar),dt=excelDateISO(r.Tgl_Bayar)||new Date().toISOString().slice(0,10);
    plan.vendor.push({no,trip:String(r.ID_Trip||'').trim(),kat:String(r.Kategori||'Operasional / Lainnya').trim(),vendor,ket:String(r.Keterangan||'').trim(),nom:excelNum(r.Nominal),tgl:excelDateISO(r.Jatuh_Tempo)||'-',status:'',_paid:paid,_paidDate:dt,_excel:true});
  });
  return plan;
}
function applyExcelSync(plan){
  if(!plan)return;
  if(plan.trips.length){
    const stMap=store('tripStatus',{});
    const cleanTrips=plan.trips.map(t=>{stMap[t.id]=t._stCode;const c=Object.assign({},t);delete c._stCode;return c;});
    save('tripStatus',stMap);save('excelTrips',mergeByKey(store('excelTrips',[]),cleanTrips,'id'));
  }
  if(plan.piutang.length){
    const pc=store('payClient',{});
    const cleanPiut=plan.piutang.map(p=>{pc[p.id]=p._terms;const c=Object.assign({},p);delete c._terms;return c;});
    save('payClient',pc);save('excelPiutang',mergeByKey(store('excelPiutang',[]),cleanPiut,'id'));
  }
  if(plan.vendor.length){
    const pv=store('payVendor',{});
    const cleanVend=plan.vendor.map(v=>{pv[v.no]=v._paid>0?[{amount:v._paid,date:v._paidDate,ket:'Sinkron Excel'}]:[];const c=Object.assign({},v);delete c._paid;delete c._paidDate;return c;});
    save('payVendor',pv);save('excelVendor',mergeByKey(store('excelVendor',[]),cleanVend,'no'));
  }
}
async function previewExcelSync(input){
  const f=input&&input.files&&input.files[0];if(!f)return;
  const box=document.getElementById('syncPrev');
  try{
    const buf=await f.arrayBuffer();
    const sheets=await readXlsxSheets(buf);
    const plan=buildExcelSyncPlan(sheets);
    pendingSyncPlan=plan;
    const s=plan.stats,tot=s.tNew+s.tUpd+s.pNew+s.pUpd+s.vNew+s.vUpd;
    if(box)box.innerHTML=`<div style="background:#eaf7f1;border:1px solid #a7dfc3;border-radius:8px;padding:12px;font-size:12.5px;color:#145a3a">
      <b>Preview Sinkronisasi (${esc(f.name)}):</b><br>
      • <b>Trips:</b> ${s.tUpd} diperbarui, ${s.tNew} baru<br>
      • <b>Pelunasan Klien:</b> ${s.pUpd} diperbarui, ${s.pNew} baru<br>
      • <b>Jadwal Vendor:</b> ${s.vUpd} diperbarui, ${s.vNew} baru
      ${tot?`<button class="btn-save" style="margin-top:10px" onclick="confirmExcelSync()">✓ Terapkan Sinkronisasi (${tot} baris)</button>`:'<div style="color:var(--red);margin-top:6px">Tidak ada sheet Trips / Pelunasan_Klien / Jadwal_Vendor yang terbaca.</div>'}
    </div>`;
  }catch(e){
    if(box)box.innerHTML=`<div style="background:#fdf0f0;border:1px solid #f5b7b7;border-radius:8px;padding:12px;font-size:12.5px;color:var(--red)">Gagal membaca file: ${esc(e.message||'pastikan format .xlsx sesuai template')}</div>`;
  }
}
function confirmExcelSync(){
  if(!pendingSyncPlan)return;
  applyExcelSync(pendingSyncPlan);pendingSyncPlan=null;
  const ov=document.getElementById('syncOv');if(ov)ov.remove();
  toast('✓ Data Excel berhasil disinkronkan ke seluruh tab');
  refreshActiveView();
}
function openExcelSync(){
  pendingSyncPlan=null;
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='syncOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:520px"><div class="pv-bar"><b>Mode Impor &amp; Sinkron Excel</b><button class="btn-acc no" onclick="document.getElementById('syncOv').remove()">Tutup</button></div>
    <div style="background:#fff;margin:16px;border-radius:10px;padding:18px;font-size:13px;line-height:1.55">
      <div style="margin-bottom:14px">
        <div style="font-weight:700;margin-bottom:4px">1. Unduh Template Sinkron (.xlsx)</div>
        <div style="color:var(--muted);font-size:12px;margin-bottom:8px">Berisi 3 sheet (<b>Trips</b>, <b>Pelunasan_Klien</b>, <b>Jadwal_Vendor</b>) lengkap dengan ID unik. Jangan ubah kolom ID.</div>
        <button class="btn-acc ok" onclick="exportSyncTemplateExcel()">⬇ Unduh Template Sinkron (.xlsx)</button>
      </div>
      <div style="border-top:1px solid var(--line);padding-top:14px;margin-bottom:12px">
        <div style="font-weight:700;margin-bottom:4px">2. Upload File Excel yang Sudah Diedit</div>
        <div style="color:var(--muted);font-size:12px;margin-bottom:8px">Pilih file <code>.xlsx</code> untuk melihat preview perubahan sebelum disinkronkan.</div>
        <input type="file" id="xlsSyncFile" accept=".xlsx" class="finput" style="padding:8px" onchange="previewExcelSync(this)">
      </div>
      <div id="syncPrev"></div>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}

function keuReimburse(){
  const list=reimburseList().sort((a,b)=>b.createdAt-a.createdAt);
  const pend=list.filter(r=>r.status==='pending'),appr=list.filter(r=>r.status==='approved'),rej=list.filter(r=>r.status==='rejected');
  const row=r=>{const t=allTrips().find(x=>x.id===r.tripId);const pillc=r.status==='approved'?'lunas':r.status==='rejected'?'piutang':'dp';const plabel=r.status==='approved'?'Disetujui':r.status==='rejected'?'Ditolak':'Menunggu';
    return `<tr><td><div class="nm" style="font-weight:700">${esc(r.crewName)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${t?esc(t.inst):'(trip dihapus)'}</div></td><td>${esc(r.item)}<div style="font-size:11px;color:var(--muted)">${esc(r.ket||'')}</div></td><td class="price mono">${rp(r.nominal)}</td><td>${dateID(r.tgl)}</td><td><span class="pill ${pillc}">${plabel}</span></td><td style="text-align:right">${r.status==='pending'?`<button class="btn-acc ok" style="margin-right:4px" onclick="decideReimburse('${r.id}','approved')">Setuju</button><button class="btn-acc no" onclick="decideReimburse('${r.id}','rejected')">Tolak</button>`:'—'}</td></tr>`;};
  return `<div class="cards fade" style="grid-template-columns:repeat(3,1fr)">
    <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div class="lbl">Menunggu Persetujuan</div><div class="val mono">${pend.length}</div><div class="sub" style="color:var(--muted)">${rp(reimburseSum(pend))}</div></div>
    <div class="scard"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 12 5 5L20 7"/></svg></div><div class="lbl">Disetujui</div><div class="val mono">${appr.length}</div><div class="sub up">${rp(reimburseSum(appr))}</div></div>
    <div class="scard"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></div><div class="lbl">Ditolak</div><div class="val mono">${rej.length}</div><div class="sub down">${rp(reimburseSum(rej))}</div></div>
  </div>
  <div class="panel fade" style="margin:0"><div class="panel-h"><h3>Pengajuan Reimburse Lapangan</h3></div>
  ${list.length?`<div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Crew</th><th>Keterangan</th><th>Nominal</th><th>Tanggal</th><th>Status</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${list.map(row).join('')}</tbody></table></div>`:`<div style="padding:34px 19px;text-align:center;color:var(--muted);font-size:13.5px">Belum ada pengajuan reimburse dari Tour Leader/Media.</div>`}
  </div>
  <p style="font-size:12px;color:var(--muted-2);margin-top:14px">Diajukan oleh Tour Leader/Media dari menu Area Tour Leader &amp; Media. Nominal yang disetujui tercatat di sini sebagai biaya lapangan — belum otomatis mengurangi laba trip pada versi ini.</p>`;
}
let jadwalFilter='akan',jadwalMonth='semua',jadwalView='kartu';
const CHECKLIST_DEF=['Armada dikonfirmasi','Hotel dibooking','Tiket wisata dipesan','Konsumsi diatur','Data peserta lengkap','Kaos & merchandise siap'];
function tripStatus(t){const ov=store('tripStatus',{})[t.id];if(ov)return ov;const b=t.brk?new Date(t.brk):null,p=t.pul?new Date(t.pul):(t.malam!=null?new Date(new Date(t.brk).getTime()+t.malam*86400000):b);if(p&&today>p)return'selesai';if(b&&today>=b&&(!p||today<=p))return'berlangsung';return'akan';}
function setTripStatus(id,st){const s=store('tripStatus',{});s[id]=st;save('tripStatus',s);toast('Status trip: '+STLBL[st]);refreshActiveView();const ov=document.getElementById('tripOv');if(ov&&st==='selesai')ov.remove();}
const STLBL={akan:'Akan Datang',berlangsung:'Berlangsung',selesai:'Selesai'};
const STPILL={akan:'jadwal',berlangsung:'dp',selesai:'lunas'};
function setJadwalFilter(f){jadwalFilter=f;const nav=document.querySelector('#view .tabs');if(nav)nav.querySelectorAll('.tab[data-jf]').forEach(t=>t.classList.toggle('active',t.dataset.jf===f));renderJadwalBody();}
function setJadwalMonth(m){jadwalMonth=m;renderJadwalBody();}
function setJadwalView(v){jadwalView=v;const b1=document.getElementById('jv_kartu'),b2=document.getElementById('jv_tl');if(b1)b1.className='btn-acc '+(v==='kartu'?'ok':'no');if(b2)b2.className='btn-acc '+(v==='timeline'?'ok':'no');renderJadwalBody();}
function jadwalTrips(){
  return allTrips().filter(t=>t.brk)
    .sort((a,b)=>a.brk<b.brk?(jadwalFilter==='selesai'?1:-1):(jadwalFilter==='selesai'?-1:1))
    .filter(t=>jadwalFilter==='semua'||tripStatus(t)===jadwalFilter)
    .filter(t=>jadwalMonth==='semua'||String(t.brk).slice(0,7)===jadwalMonth);
}
function renderJadwal(){const v=document.getElementById('view');if(v&&v.querySelector('#jadwalBody'))renderJadwalBody();}
function renderJadwalBody(){
  const b=document.getElementById('jadwalBody');if(!b)return;
  const list=jadwalTrips();
  if(!list.length){b.innerHTML='<div class="empty"><h3>Tidak ada trip</h3><p>Tidak ada trip pada filter bulan/status ini.</p></div>';return;}
  if(jadwalView==='timeline'){
    const groups={};list.forEach(t=>{const ym=String(t.brk).slice(0,7);(groups[ym]=groups[ym]||[]).push(t);});
    b.innerHTML=Object.entries(groups).map(([ym,ts])=>{
      const d=new Date(ym+'-01');const lbl=isNaN(d)?ym:(MONTH_NAMES[d.getMonth()]+' '+d.getFullYear());
      const items=ts.map(t=>{const[pc,pl]=payStatus(t);const st=tripStatus(t);const tls=tripCrewNames(t.id,'tl'),mds=tripCrewNames(t.id,'media');
        const tlLbl=tls.length?tls.map(c=>esc(c.nama.split(' ')[0])).join(', '):'-';
        const mdLbl=mds.length?mds.map(c=>esc(c.nama.split(' ')[0])).join(', '):'-';
        return `<div class="tl-item" style="cursor:pointer;padding:10px 12px;border-radius:10px;background:#fff;border:1px solid var(--line);margin-bottom:8px" onclick="openTripDetail('${t.id}')">
          <div class="tl-dot" style="background:${st==='selesai'?'var(--green)':st==='berlangsung'?'var(--gold)':'var(--blue)'}"></div>
          <div class="tl-body" style="width:100%">
            <div class="tl-top"><b>${esc(t.inst)} ${t._new?'<span class="pill dp" style="background:var(--gold);color:var(--navy);font-size:10px">BARU</span>':''}</b><span class="tl-date">${dateID(t.brk)}${t.pul?' – '+dateID(t.pul):''} · <span class="pill ${STPILL[st]}">${STLBL[st]}</span></span></div>
            <div style="font-size:12px;color:var(--muted);margin-top:3px">${esc((t.dest||'').split('(')[0])} · ${t.pax} pax · ${t.bus||'-'} bus · TL: ${tlLbl} · Media: ${mdLbl}</div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px"><span class="pill ${pc}">${pl}</span><button class="btn-acc no" style="font-size:10.5px;padding:3px 8px" onclick="event.stopPropagation();genRundownPDF('${t.id}')">⬇ Rundown</button></div>
          </div></div>`;}).join('');
      return `<div class="panel fade" style="margin-bottom:16px"><div class="panel-h"><h3>${lbl} <span style="color:var(--muted);font-size:12px">(${ts.length} trip)</span></h3></div><div class="tl" style="padding:12px 16px">${items}</div></div>`;
    }).join('');
    return;
  }
  b.innerHTML='<div class="jgrid">'+list.map(t=>{const[pc,pl]=payStatus(t);const st=tripStatus(t);const tls=tripCrewNames(t.id,'tl'),mds=tripCrewNames(t.id,'media');
    const tlChips=tls.length?tls.map(c=>`<span class="crew-chip" style="background:var(--teal)">TL: ${esc(c.nama.split(' ')[0])}</span>`).join(''):'<span class="crew-chip empty">TL: -</span>';
    const mdChips=mds.length?mds.map(c=>`<span class="crew-chip" style="background:var(--purple)">Media: ${esc(c.nama.split(' ')[0])}</span>`).join(''):'<span class="crew-chip empty">Media: -</span>';
    return `<div class="jcard" onclick="openTripDetail('${t.id}')">
      <div class="jcard-top"><span class="pill ${STPILL[st]}">${STLBL[st]}</span>${t._new?'<span class="pill dp" style="background:var(--gold);color:var(--navy)">BARU</span>':''}</div>
      <h4>${esc(t.inst)}</h4><div class="jcard-dest">${esc((t.dest||'').split('(')[0])}</div>
      <div class="jcard-meta"><span>📅 ${dateID(t.brk)}</span><span>👥 ${t.pax} pax</span><span>🚌 ${t.bus||'-'} bus</span></div>
      <div class="jcard-crew">${tlChips}${mdChips}</div>
      <div class="jcard-foot"><span class="pill ${pc}">${pl}</span><button class="btn-acc no" style="font-size:10.5px;padding:3px 8px" onclick="event.stopPropagation();genRundownPDF('${t.id}')">⬇ Rundown</button></div>
    </div>`;}).join('')+'</div>';
}
function vJadwal(){
  const all=allTrips().filter(t=>t.brk);const akan=all.filter(t=>tripStatus(t)==='akan').length;
  const filters=[['akan','Akan Datang'],['berlangsung','Berlangsung'],['selesai','Selesai'],['semua','Semua']];
  const nav=filters.map(([k,l])=>`<button class="tab ${jadwalFilter===k?'active':''}" data-jf="${k}" onclick="setJadwalFilter('${k}')">${l}</button>`).join('');
  const months=[...new Set(all.map(t=>String(t.brk).slice(0,7)))].sort();
  const mOpts='<option value="semua">Semua Bulan</option>'+months.map(ym=>{const d=new Date(ym+'-01');const lbl=isNaN(d)?ym:(MONTH_NAMES[d.getMonth()]+' '+d.getFullYear());return `<option value="${ym}" ${jadwalMonth===ym?'selected':''}>${lbl}</option>`;}).join('');
  return `<div class="hello fade"><h1>Jadwal Trip</h1><p>${akan} trip akan datang · klik kartu atau baris timeline untuk detail, crew &amp; checklist</p></div>
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;padding-bottom:16px">
    <div class="tabs" style="padding:0">${nav}</div>
    <div style="display:flex;align-items:center;gap:8px">
      <select id="jadwalMonthSel" class="finput" style="width:auto;margin:0;padding:7px 10px;font-size:12.5px" onchange="setJadwalMonth(this.value)">${mOpts}</select>
      <button id="jv_kartu" class="btn-acc ${jadwalView==='kartu'?'ok':'no'}" onclick="setJadwalView('kartu')">Kartu</button>
      <button id="jv_tl" class="btn-acc ${jadwalView==='timeline'?'ok':'no'}" onclick="setJadwalView('timeline')">Timeline</button>
    </div>
  </div><div id="jadwalBody"></div>`;
}
function openEditTrip(id){
  const t=allTrips().find(x=>x.id===id);if(!t)return;
  const old=document.getElementById('editTripOv');if(old)old.remove();
  const jenisOpts=['Paket Wisata','Sewa Bus Only','Outing / Gathering','Study Tour','Lainnya'];
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='editTripOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:500px"><div class="pv-bar"><b>✎ Edit Data Trip — ${esc(t.inst)}</b><button class="btn-acc no" onclick="document.getElementById('editTripOv').remove()">Tutup</button></div>
    <div style="background:#fff;margin:16px;border-radius:10px;padding:18px">
      <label class="flbl">Nama Instansi / Klien</label>
      <input id="et_inst" class="finput" value="${esc(t.inst||'')}">
      <div class="frow">
        <div><label class="flbl">Destinasi / Wilayah</label><input id="et_dest" class="finput" value="${esc(t.dest||'')}"></div>
        <div><label class="flbl">Jenis Trip</label><select id="et_jenis" class="finput">${jenisOpts.map(j=>`<option value="${j}" ${(t.jenis||'Paket Wisata')===j?'selected':''}>${j}</option>`).join('')}</select></div>
      </div>
      <div class="frow">
        <div><label class="flbl">Tanggal Berangkat</label><input id="et_brk" class="finput" type="date" value="${esc(t.brk||'')}"></div>
        <div><label class="flbl">Tanggal Pulang</label><input id="et_pul" class="finput" type="date" value="${esc(t.pul||t.brk||'')}"></div>
      </div>
      <div class="frow">
        <div><label class="flbl">Jumlah Pax</label><input id="et_pax" class="finput" type="number" min="0" value="${t.pax||0}"></div>
        <div><label class="flbl">Jumlah Bus (jika belum atur vendor)</label><input id="et_bus" class="finput" type="number" min="0" value="${t.bus||0}"></div>
      </div>
      <div class="frow">
        <div><label class="flbl">Armada</label><input id="et_armada" class="finput" value="${esc(t.armada||'')}" placeholder="mis. BIG BUS (50 Seat)"></div>
        <div><label class="flbl">Hotel</label><input id="et_hotel" class="finput" value="${esc(t.hotel||'')}" placeholder="mis. Hotel Bandung"></div>
      </div>
      <button class="btn-save" style="margin-top:8px" onclick="saveEditTrip('${id}')">✓ Simpan Perubahan Data Trip</button>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function saveEditTrip(id){
  const inst=(document.getElementById('et_inst').value||'').trim();
  if(!inst){toast('Nama instansi wajib diisi');return;}
  const dest=(document.getElementById('et_dest').value||'').trim();
  const jenis=document.getElementById('et_jenis').value||'Paket Wisata';
  const brk=document.getElementById('et_brk').value||'';
  const pul=document.getElementById('et_pul').value||brk;
  const pax=Math.max(0,parseInt(document.getElementById('et_pax').value)||0);
  const bus=Math.max(0,parseInt(document.getElementById('et_bus').value)||0);
  const armada=(document.getElementById('et_armada').value||'').trim();
  const hotel=(document.getElementById('et_hotel').value||'').trim();
  const tov=store('tripOverride',{});
  tov[id]={inst,dest,jenis,brk,pul,pax,bus,armada,hotel};
  save('tripOverride',tov);
  if(piutMap()[id]){
    const pov=store('piutOverride',{});
    pov[id]=Object.assign({},pov[id]||{},{inst,pax,tgl:brk});
    save('piutOverride',pov);
  }
  const eov=document.getElementById('editTripOv');if(eov)eov.remove();
  const tovModal=document.getElementById('tripOv');if(tovModal)tovModal.remove();
  toast('Data trip diperbarui & disinkronkan ✓');
  refreshActiveView();
  openTripDetail(id);
}
function openTripDetail(id){
  const t=allTrips().find(x=>x.id===id);if(!t)return;
  const[pc,pl]=payStatus(t);const st=tripStatus(t);const a=tripAssign(t.id);const hari=tripDays(t);
  const p=piutMap()[t.id];const paid=p?clientPaid(p):0,sisa=p?clientSisa(p):0;
  const tls=crewList().filter(c=>c.peran==='Tour Leader');const mds=crewList().filter(c=>c.peran==='Media');
  const optAdd=(arr,assigned,roleLbl)=>`<option value="">+ Tambah ${roleLbl}...</option>`+arr.filter(c=>!assigned.some(x=>x.id===c.id)).map(c=>{const busy=crewSibuk(c.id,id);return `<option value="${c.id}">${esc(c.nama)} (${rp(c.tarif||0)}/hr)${busy?' ⚠ bentrok':''}</option>`;}).join('');
  const crewRows=(assigned,role)=>(assigned.map(x=>{const c=crewById(x.id);if(!c)return '';return `<div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;background:#f7f8fb;padding:6px 8px;border-radius:8px"><span style="flex:1;font-size:12.5px;font-weight:600">${esc(c.nama)}</span><input class="finput" type="number" style="width:105px;margin:0;padding:4px 7px;font-size:12px" value="${x.tarif}" title="Tarif per hari (Rp)" onchange="setTripCrewTarif('${id}','${role}','${c.id}',this.value);document.getElementById('tripOv').remove();openTripDetail('${id}')"><span style="font-size:11px;color:var(--muted)">/hr</span><button class="pay-del" onclick="removeTripCrew('${id}','${role}','${c.id}');document.getElementById('tripOv').remove();openTripDetail('${id}')">✕</button></div>`;}).join(''))||'<div style="font-size:12px;color:var(--muted-2);margin-bottom:6px">Belum ada</div>';
  const cl=store('checklist',{})[id]||CHECKLIST_DEF.map(x=>({item:x,done:false}));
  const clHTML=cl.map((c,i)=>`<label class="chk"><input type="checkbox" ${c.done?'checked':''} onchange="toggleChecklist('${id}',${i})"> ${esc(c.item)}</label>`).join('');
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='tripOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:560px"><div class="pv-bar"><b>${esc(t.inst)}</b><div><button class="btn-acc ok" style="margin-right:6px" onclick="genRundownPDF('${id}')">⬇ Rundown PDF</button>${p?`<button class="btn-acc no" style="margin-right:6px" onclick="genInvoicePDF('${id}')">⬇ Invoice</button>`:''}<button class="btn-acc no" onclick="document.getElementById('tripOv').remove()">Tutup</button></div></div>
    <div style="background:var(--bg);padding:16px;max-height:76vh;overflow:auto">
      <div style="display:flex;gap:8px;margin-bottom:12px">${Object.keys(STLBL).map(s=>`<button class="btn-acc ${st===s?'ok':'no'}" style="flex:1" onclick="setTripStatus('${id}','${s}')">${STLBL[s]}</button>`).join('')}</div>
      <div class="td-card"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px"><h5 style="margin:0">Info Trip</h5><button class="btn-acc no" style="padding:3px 9px;font-size:11px" onclick="openEditTrip('${id}')">✎ Edit Data Trip</button></div>
        <div class="td-row"><span>Destinasi</span><b>${esc((t.dest||'').split('(')[0])}</b></div>
        <div class="td-row"><span>Tanggal</span><b>${dateID(t.brk)}${t.pul?' – '+dateID(t.pul):''} (${hari} hari)</b></div>
        <div class="td-row"><span>Peserta</span><b>${t.pax} pax</b></div>
        <div class="td-row"><span>Armada</span><b>${esc(t.armada||(t.bus?t.bus+' unit':'—'))}</b></div>
        ${t.hotel?`<div class="td-row"><span>Hotel</span><b>${esc(t.hotel)}</b></div>`:''}
      </div>
      <div class="td-card"><h5>Penugasan Crew (bisa lebih dari 1 &amp; edit tarif/hari)</h5>
        <label class="flbl">Tour Leader (${a.tls.length})</label>
        <div style="margin:4px 0 6px">${crewRows(a.tls,'tl')}</div>
        <select class="finput" style="margin:0 0 10px" onchange="if(this.value){addTripCrew('${id}','tl',this.value);document.getElementById('tripOv').remove();openTripDetail('${id}');}">${optAdd(tls,a.tls,'Tour Leader')}</select>
        <label class="flbl">Media (${a.medias.length})</label>
        <div style="margin:4px 0 6px">${crewRows(a.medias,'media')}</div>
        <select class="finput" style="margin:0" onchange="if(this.value){addTripCrew('${id}','media',this.value);document.getElementById('tripOv').remove();openTripDetail('${id}');}">${optAdd(mds,a.medias,'Media')}</select>
        <div style="font-size:12px;color:var(--muted);margin-top:8px">Total gaji crew trip ini: <b>${rp(tripGaji(t))}</b> (${hari} hari)</div>
      </div>
      <div class="td-card"><h5>Pembayaran</h5>
        ${p?`<div class="td-row"><span>Tagihan</span><b>${jt(p.tagih)}</b></div><div class="td-row"><span>Dibayar</span><b style="color:var(--green)">${jt(paid)}</b></div><div class="td-row"><span>Sisa</span><b style="color:${sisa>0?'var(--red)':'var(--green)'}">${jt(sisa)}</b></div><button class="btn-save" style="margin-top:8px" onclick="document.getElementById('tripOv').remove();go('keuangan');setTimeout(()=>{setKeuTab('pelunasan');openBayar('${id}')},50)">Catat Pembayaran</button>`:`<div style="font-size:12.5px;color:var(--muted);margin-bottom:8px">Belum ada invoice piutang untuk trip ini.</div><button class="btn-save" onclick="document.getElementById('tripOv').remove();openCreateInvoiceFromTrip('${id}')">+ Buat Tagihan &amp; Catat Pembayaran</button>`}
      </div>
      <div class="td-card"><h5>Persiapan Vendor</h5>
        ${prepTrip(id).length?`<div class="td-row"><span>Kebutuhan tercatat</span><b>${prepTrip(id).length} item</b></div><div class="td-row"><span>Total biaya vendor</span><b>${rp(prepTotal(id))}</b></div><div class="td-row"><span>Sisa harus dibayar</span><b style="color:${prepSisa(id)>0?'var(--red)':'var(--green)'}">${rp(prepSisa(id))}</b></div>`:'<div style="font-size:12.5px;color:var(--muted);margin-bottom:8px">Belum ada vendor dipilih (armada, hotel, konsumsi, tiket).</div>'}
        <button class="btn-save" style="margin-top:8px" onclick="document.getElementById('tripOv').remove();openPrep('${id}')">${prepTrip(id).length?'Kelola Persiapan Vendor':'🧰 Atur Persiapan Vendor'}</button>
      </div>
      <div class="td-card"><h5>Checklist Persiapan</h5>${clHTML}</div>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function toggleChecklist(id,i){const s=store('checklist',{});const cl=s[id]||CHECKLIST_DEF.map(x=>({item:x,done:false}));cl[i].done=!cl[i].done;s[id]=cl;save('checklist',s);}

let katTab='kalkulator',katHotelPage=1,katDestPage=1;
function setKatHotelPage(p){katHotelPage=p;renderKat();}
function setKatDestPage(p){katDestPage=p;renderKat();}
// ===== KATALOG BISA DIEDIT (master data) =====
// CATALOG = data dasar dari Excel. CAT = yang dipakai aplikasi (dasar + hasil edit di web).
function catGet(kind){const v=store('cat_'+kind,null);return (v&&Array.isArray(v))?v:CATALOG[kind];}
function catSet(kind,arr){save('cat_'+kind,arr);}
function catEdited(kind){return Array.isArray(store('cat_'+kind,null));}
const CAT={get hotels(){return catGet('hotels');},get armada(){return catGet('armada');},get kaos(){return catGet('kaos');},get dests(){return catGet('dests');},get rooms(){return CATALOG.rooms;}};
const CATFIELDS={
  hotels:[['name','Nama Hotel','text'],['region','Daerah','list'],['wd','Harga Weekday / kamar (Rp)','number'],['we','Harga Weekend / kamar (Rp)','number']],
  dests:[['name','Nama Destinasi','text'],['city','Kota / Daerah','list'],['note','Aktivitas','text'],['price','Harga Tiket / pax (Rp)','number']],
  armada:[['name','Nama Armada','text'],['rate','Tarif / bus / hari (Rp)','number'],['seat','Kapasitas (seat)','number']],
  kaos:[['name','Nama Kaos','text'],['price','Harga / pcs (Rp)','number']]
};
const CATLBL={hotels:'Hotel',dests:'Destinasi',armada:'Armada',kaos:'Kaos'};
const CATGRP={hotels:'region',dests:'city'};
function catAdd(kind,obj){const a=catGet(kind).slice();a.push(obj);catSet(kind,a);}
function catUpdate(kind,i,obj){const a=catGet(kind).slice();if(i<0||i>=a.length)return;a[i]=obj;catSet(kind,a);}
function catDel(kind,i){const a=catGet(kind).slice();if(i<0||i>=a.length)return;a.splice(i,1);catSet(kind,a);}
function catReset(kind){delete _memStore['havist_cat_'+kind];try{localStorage.removeItem('havist_cat_'+kind);}catch(e){}toast(CATLBL[kind]+' dikembalikan ke data Excel');renderKat();}
function armSeat(a){return a.seat||kapasitas(a.name);}
function openCatForm(kind,i){
  const flds=CATFIELDS[kind];const cur=i>=0?catGet(kind)[i]:{};
  const grp=CATGRP[kind];
  const listVals=grp?[...new Set(catGet(kind).map(x=>x[grp]))]:[];
  const body=flds.map(([k,lbl,ty])=>{
    if(ty==='list')return `<label class="flbl">${lbl}</label><input id="cf_${k}" class="finput" list="cf_dl" value="${esc(String(cur[k]==null?'':cur[k]))}" placeholder="ketik baru atau pilih"><datalist id="cf_dl">${listVals.map(v=>`<option value="${esc(v)}">`).join('')}</datalist>`;
    return `<label class="flbl">${lbl}</label><input id="cf_${k}" class="finput" type="${ty}" value="${esc(String(cur[k]==null?'':cur[k]))}">`;
  }).join('');
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='catOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:440px"><div class="pv-bar"><b>${i>=0?'Edit':'Tambah'} ${CATLBL[kind]}</b><button class="btn-acc no" onclick="document.getElementById('catOv').remove()">Tutup</button></div>
    <div style="background:#fff;margin:16px;border-radius:10px;padding:18px">${body}
      <button class="btn-save" style="margin-top:12px" onclick="submitCatForm('${kind}',${i})">${i>=0?'Simpan Perubahan':'+ Tambah ke Katalog'}</button>
      ${i>=0?`<button class="btn-save" style="margin-top:8px;background:var(--red)" onclick="if(confirm('Hapus ${esc(String(cur.name||''))} dari katalog?')){catDel('${kind}',${i});document.getElementById('catOv').remove();toast('Dihapus dari katalog');renderKat();}">Hapus dari Katalog</button>`:''}
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function submitCatForm(kind,i){
  const o={};let bad='';
  CATFIELDS[kind].forEach(([k,lbl,ty])=>{const el=document.getElementById('cf_'+k);let v=el?el.value:'';
    if(ty==='number'){v=+v||0;}else{v=String(v||'').trim();}
    if(k==='name'&&!v)bad=lbl;
    if((k==='region'||k==='city')&&!v)bad=lbl;
    o[k]=v;});
  if(bad){toast('Isi dulu: '+bad);return;}
  if(i>=0)catUpdate(kind,i,o);else catAdd(kind,o);
  document.getElementById('catOv').remove();toast(CATLBL[kind]+' '+(i>=0?'diperbarui':'ditambahkan'));renderKat();
}
function catToolbar(kind,extra){
  return `<div class="cat-bar"><div><button class="btn-save" style="width:auto;padding:8px 14px" onclick="openCatForm('${kind}',-1)">+ Tambah ${CATLBL[kind]}</button>
    ${catEdited(kind)?`<button class="btn-acc no" style="margin-left:8px" onclick="if(confirm('Kembalikan ${CATLBL[kind]} ke data Excel? Semua perubahan di web hilang.'))catReset('${kind}')">↺ Reset ke data Excel</button>`:''}</div>
    <span style="font-size:12px;color:var(--muted)">${extra||''}${catEdited(kind)?' · <b style="color:var(--gold-ink)">sudah diubah di web</b>':''}</span></div>`;
}
function kapasitas(name){
  const f=(typeof CAT!=='undefined'&&CAT.armada)?CAT.armada.find(a=>a.name===name):null;
  if(f&&f.seat)return +f.seat;
  const m=String(name||'').match(/(\d+)(?:\s*[–-]\s*(\d+))?\s*SEAT/i);
  if(m)return +(m[2]||m[1]);
  const u=String(name||'').toUpperCase();if(u.includes('ELF'))return 15;if(u.includes('HIACE'))return 14;if(u.includes('MEDIUM'))return 33;if(u.includes('LEGRES'))return 32;return 45;
}
function vKatalog(){
  const tabs=[['kalkulator','Kalkulator Harga'],['hotel','Hotel'],['destinasi','Destinasi Wisata'],['armada','Armada & Kaos']];
  const nav=tabs.map(([k,l])=>`<button class="tab ${katTab===k?'active':''}" data-kt="${k}" onclick="setKatTab('${k}')">${l}</button>`).join('');
  return `<div class="hello fade"><h1>Harga &amp; Katalog</h1><p>Kalkulator estimasi otomatis + daftar harga hotel, destinasi, armada, dan kaos</p></div>
  <div class="tabs" style="padding:0 0 16px">${nav}</div><div id="katBody"></div>`;
}
function setKatTab(k){
  katTab=k;katHotelPage=1;katDestPage=1;
  const nav=document.querySelector('#view .tabs');
  if(nav)nav.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.kt===k));
  renderKat();
}
function renderKat(){
  const b=document.getElementById('katBody');if(!b)return;
  if(katTab==='kalkulator')b.innerHTML=katKalkulator();
  else if(katTab==='hotel')b.innerHTML=katHotel();
  else if(katTab==='destinasi')b.innerHTML=katDestinasi();
  else b.innerHTML=katArmada();
  if(katTab==='kalkulator')calcQuote();
}
function katKalkulator(){
  const markup=store('markup',20);
  const armOpt=CAT.armada.map((a,i)=>`<option value="${a.rate}" data-name="${esc(a.name)}" data-seat="${armSeat(a)}" ${i===1?'selected':''}>${esc(a.name)} — ${rp(a.rate)}/hari (${armSeat(a)} seat)</option>`).join('');
  const regions=[...new Set(CAT.hotels.map(h=>h.region))];
  const hotOpt='<option value="0|0">— Tanpa Hotel —</option>'+regions.map(r=>`<optgroup label="${esc(r)}">`+CAT.hotels.filter(h=>h.region===r).map(h=>`<option value="${h.wd}|${h.we}">${esc(h.name)} (${rp(h.wd)}/${rp(h.we)})</option>`).join('')+'</optgroup>').join('');
  const kaosOpt=CAT.kaos.map(k=>`<option value="${k.price}">${esc(k.name)}${k.price?' — '+rp(k.price):''}</option>`).join('');
  const cities=[...new Set(CAT.dests.map(d=>d.city))];
  const destBoxes=cities.map(c=>{const items=CAT.dests.filter(d=>d.city===c).map((d,i)=>{const gi=CAT.dests.indexOf(d);return `<label class="dest-item"><input type="checkbox" class="qdest" data-price="${d.price}" data-name="${esc(d.name)}" data-city="${esc(c)}" data-note="${esc(d.note||'')}" onchange="calcQuote()"><span>${esc(d.name)} <em>${d.price?rp(d.price):'Gratis'}</em>${d.note?'<span class="opt">'+esc(d.note)+'</span>':''}</span></label>`;}).join('');
    return `<div class="citybox"><div class="cityhd" onclick="this.parentNode.classList.toggle('open')"><span>${esc(c)}</span><span class="cnt">${CAT.dests.filter(d=>d.city===c).length}</span></div><div class="citygrid">${items}</div></div>`;}).join('');
  return `<div class="calc-wrap fade">
    <div class="panel" style="margin:0">
      <div class="panel-h"><h3>Input Paket</h3><span style="font-size:12px;color:var(--muted)">markup ${markup}% (ubah di Setting)</span></div>
      <div style="padding:16px 19px">
        <div class="frow">
          <div><label class="flbl">Total Peserta (pax)</label><input id="q_pax" class="finput" type="number" value="50" oninput="calcQuote()"></div>
          <div><label class="flbl">Durasi (malam inap)</label><input id="q_malam" class="finput" type="number" value="1" oninput="calcQuote()"></div>
        </div>
        <div class="frow">
          <div><label class="flbl">Tanggal Berangkat</label><input id="q_tgl" class="finput" type="date" style="cursor:pointer" onclick="try{this.showPicker()}catch(e){}" onchange="calcQuote()"></div>
          <div><label class="flbl">Konfigurasi Kamar</label><select id="q_share" class="finput" onchange="calcQuote()"><option value="4">Quad Share (isi 4)</option><option value="2">Twin Share (isi 2)</option></select></div>
        </div>
        <label class="flbl">Armada Transportasi</label><select id="q_arm" class="finput" onchange="calcQuote()">${armOpt}</select>
        <label class="flbl">Akomodasi Hotel</label><select id="q_hotel" class="finput" onchange="calcQuote()">${hotOpt}</select>
        <div class="frow">
          <div><label class="flbl">Frekuensi Makan</label><input id="q_mfreq" class="finput" type="number" value="3" oninput="calcQuote()"></div>
          <div><label class="flbl">Budget Makan / pax</label><input id="q_mprice" class="finput" type="number" value="35000" oninput="calcQuote()"></div>
        </div>
        <label class="flbl">Merchandise / Kaos</label><select id="q_kaos" class="finput" onchange="calcQuote()">${kaosOpt}</select>
        <label class="flbl" style="margin-top:6px">Destinasi Wisata <span style="color:var(--muted-2);font-weight:500">(klik kota untuk buka)</span></label>
        <div class="destwrap">${destBoxes}</div>
      </div>
    </div>
    <div>
      <div class="result-card">
        <div class="rc-label">Estimasi Harga Per Pax</div>
        <div class="rc-price" id="q_perpax">Rp 0</div>
        <div class="rc-dur" id="q_dur">—</div>
        <button class="rc-toggle" onclick="document.getElementById('q_secret').classList.toggle('show');this.textContent=document.getElementById('q_secret').classList.contains('show')?'🔓 Sembunyikan':'🔒 Data Internal'">🔒 Data Internal</button>
        <div class="rc-secret" id="q_secret">
          <div class="rc-row"><span>FOC Unit (1:10)</span><b id="q_foc">0 pax</b></div>
          <div class="rc-row"><span>Diskon Klien</span><b id="q_diskonshow">Rp 0</b></div>
          <div class="rc-row warn"><span>Komisi Sales (5%)</span><b id="q_komisi">Rp 0</b></div>
          <div class="rc-row"><span>Total Jual Grup (setelah diskon)</span><b id="q_grup">Rp 0</b></div>
          ${currentUser().role==='owner'?`<div class="rc-row"><span>Estimasi Laba Bersih (Owner)</span><b id="q_laba">Rp 0</b></div>`:''}
        </div>
        <div class="rc-break" id="q_break"></div>
      </div>
      <div class="save-box">
        <div class="sb-h">Buat Penawaran</div>
        <input id="q_klien" class="finput" list="q_kliendl" style="margin:6px 0" placeholder="Nama klien / instansi" oninput="calcQuote()">
        <datalist id="q_kliendl">${klienList().map(k=>`<option value="${esc(k.nama)}">`).join('')}</datalist>
        <input id="q_dest" class="finput" style="margin:0 0 8px" placeholder="Tujuan (mis. Jogja)">
        <input id="q_hp" class="finput" style="margin:0 0 10px" placeholder="No. HP klien (untuk WA)">
        <label class="flbl">Diskon Klien (Rp, opsional)</label>
        <input id="q_diskon" class="finput" type="number" value="0" style="margin:4px 0 10px" oninput="calcQuote()" placeholder="0">
        <button class="btn-save" onclick="saveQuote()">Simpan &amp; Kirim ke ACC →</button>
        <button class="btn-save" style="background:var(--gold);color:var(--navy);margin-top:8px" onclick="showPenawaran()">📄 Surat Penawaran + Itinerary</button>
        <div id="q_saved_banner" style="display:none;margin-top:10px;padding:10px 12px;border-radius:8px;background:#eaf7f1;border:1px solid #a7dfc3;font-size:12px;color:#145a3a;line-height:1.5"></div>
        <p style="font-size:11px;color:var(--muted);margin-top:8px;line-height:1.5">Tersimpan sebagai penawaran, menunggu ACC Management. Surat penawaran bisa dilihat & diunduh PDF, itinerary dibuat otomatis dari destinasi yang dicentang.</p>
      </div>
      <div class="note-card">Pembayaran: DP 30% saat konfirmasi, pelunasan maksimal 7 hari sebelum perjalanan.</div>
    </div>
  </div>`;
}
function calcQuote(){
  const g=id=>document.getElementById(id);if(!g('q_pax'))return;
  const p=+g('q_pax').value||0, malam=+g('q_malam').value||0, share=+g('q_share').value||4;
  const armSel=g('q_arm').selectedOptions[0], armRate=+armSel.value, cap=(+armSel.dataset.seat)||kapasitas(armSel.dataset.name);
  const mFreq=+g('q_mfreq').value||0, mPrice=+g('q_mprice').value||0, kaosRate=+g('q_kaos').value||0;
  const hd=g('q_hotel').value.split('|'); const tgl=g('q_tgl').value;
  const isWknd=tgl&&([0,6].includes(new Date(tgl).getDay())); const hotelRate=isWknd?+hd[1]:+hd[0];
  const markup=1+(store('markup',20)/100);
  const bus=Math.ceil(p/cap)||0, hari=malam+1;
  const cT=armRate*bus*hari, cM=mFreq*mPrice*p, cH=malam>0?hotelRate*malam*Math.ceil(p/share):0, cK=kaosRate*p;
  let cW=0;document.querySelectorAll('.qdest:checked').forEach(d=>{cW+=(+d.dataset.price)*p;d.closest('.citybox').classList.add('has');});
  document.querySelectorAll('.citybox').forEach(b=>{if(!b.querySelectorAll('.qdest:checked').length)b.classList.remove('has');});
  const modal=cT+cM+cH+cW+cK, mk=modal*markup;
  const foc=Math.min(Math.floor(p/10),25), subsidi=foc*(p>0?mk/p:0);
  const jualGrup=mk-subsidi;
  const diskon=Math.max(0,+(g('q_diskon')?g('q_diskon').value:0)||0);
  const grupFinal=Math.max(0,jualGrup-diskon);
  const perpax=p>0?Math.ceil((grupFinal/p)/1000)*1000:0, komisi=grupFinal*0.05, labaBersih=grupFinal-modal;
  g('q_perpax').textContent='Rp '+perpax.toLocaleString('id-ID');
  g('q_dur').textContent=hari+' Hari '+malam+' Malam · '+p+' pax · '+bus+' unit '+armSel.dataset.name.split(' ')[0]+(isWknd?' · Weekend':' · Weekday');
  g('q_foc').textContent=foc+' pax';
  if(g('q_diskonshow'))g('q_diskonshow').textContent=(diskon>0?'- ':'')+'Rp '+Math.round(diskon).toLocaleString('id-ID');
  g('q_komisi').textContent='Rp '+Math.round(komisi).toLocaleString('id-ID');g('q_grup').textContent='Rp '+Math.round(grupFinal).toLocaleString('id-ID');
  if(g('q_laba'))g('q_laba').innerHTML=(labaBersih<0?'<span style="color:var(--red)">Rp '+Math.round(labaBersih).toLocaleString('id-ID')+' ⚠ rugi</span>':'Rp '+Math.round(labaBersih).toLocaleString('id-ID'));
  const br=[['Transport ('+bus+' unit × '+hari+' hari)',cT],['Makan ('+mFreq+'× × '+p+' pax)',cM],['Hotel',cH],['Wisata',cW],['Kaos',cK],['Markup '+Math.round((markup-1)*100)+'%',mk-modal]];
  g('q_break').innerHTML='<div class="bk-h">Rincian Modal Grup</div>'+br.map(([l,v])=>`<div class="rc-row"><span>${l}</span><b>Rp ${Math.round(v).toLocaleString('id-ID')}</b></div>`).join('')+`<div class="rc-row tot"><span>Total Jual Grup (sebelum diskon)</span><b>Rp ${Math.round(jualGrup).toLocaleString('id-ID')}</b></div>`;
  const dsel=[];document.querySelectorAll('.qdest:checked').forEach(x=>dsel.push({name:x.dataset.name,city:x.dataset.city,note:x.dataset.note,price:+x.dataset.price}));
  const kamar=malam>0?Math.ceil(p/share):0;
  lastQuote={pax:p,bus,malam,hari,kamar,perpax,total:Math.round(grupFinal),laba:Math.round(labaBersih),tgl:tgl,diskon:Math.round(diskon),komisi:Math.round(komisi),
    armName:armSel.dataset.name,armRate:armRate,hotelName:g('q_hotel').selectedOptions[0].text,hotelRate:hotelRate,mFreq:mFreq,mPrice:mPrice,
    kaosName:g('q_kaos').selectedOptions[0].text,kaosRate:kaosRate,share:share,isWknd:isWknd,dests:dsel};
}
let lastSavedQuoteId=null;
function resetQuoteForm(){
  const g=id=>document.getElementById(id);
  if(g('q_klien'))g('q_klien').value='';
  if(g('q_dest'))g('q_dest').value='';
  if(g('q_hp'))g('q_hp').value='';
  if(g('q_diskon'))g('q_diskon').value='0';
  const b=g('q_saved_banner');if(b)b.style.display='none';
  calcQuote();
}
function saveQuote(){
  const g=id=>document.getElementById(id);
  const klien=(g('q_klien').value||'').trim(), dest=(g('q_dest').value||'').trim()||'Paket Custom', tgl=g('q_tgl').value, hp=(g('q_hp').value||'').trim();
  if(!klien){toast('Isi nama klien/instansi dulu');return;}
  if(!tgl){toast('Pilih tanggal berangkat dulu');return;}
  if(!lastQuote||!lastQuote.pax){toast('Isi detail paket dulu');return;}
  const q=lastQuote;const list=penawaran();
  const sid=currentSales(),sc=sid?crewById(sid):null;
  const newId='PNW-'+Date.now();
  list.push({id:newId,klien,dest,tgl,hp,pax:q.pax,bus:q.bus,malam:q.malam,hari:q.hari,perpax:q.perpax,total:q.total,laba:q.laba,
    diskon:q.diskon||0,komisi:q.komisi||0,salesId:sid||'',salesName:sc?sc.nama:'',
    armName:q.armName,armRate:q.armRate||0,hotelName:q.hotelName,hotelRate:q.hotelRate||0,kamar:q.kamar||0,mFreq:q.mFreq,mPrice:q.mPrice||35000,share:q.share||4,kaosRate:q.kaosRate,kaosName:q.kaosName,extraCost:0,extraNote:'',dests:q.dests,status:'pending',created:Date.now()});
  save('penawaran',list);
  lastSavedQuoteId=newId;
  upsertKlien(klien,hp,sc?sc.nama:'');
  toast('✓ Penawaran '+klien+' tersimpan'+(sc?' — a.n. '+sc.nama:''));
  const b=g('q_saved_banner');
  if(b){
    b.style.display='block';
    b.innerHTML=`<div><b>✓ Penawaran tersimpan</b> untuk ${esc(klien)} (menunggu ACC). Data kalkulator tetap aman.</div>
      <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
      <button class="btn-acc" style="background:var(--gold);color:var(--navy)" onclick="showPenawaran('${newId}')">⬇ Unduh PDF</button>
      <button class="btn-acc ok" onclick="go('acc')">Buka Halaman ACC →</button>
      <button class="btn-acc no" onclick="resetQuoteForm()">Buat Baru</button></div>`;
  }
}
// ===== SALES: pilih siapa yang sedang login, data klien, performa =====
function currentSales(){
  const u=currentUser();
  if(u.role==='sales'){
    if(u.crewId&&crewById(u.crewId))return u.crewId;
    const m=crewList().find(c=>c.nama.toLowerCase()===(u.crewName||u.nama||'').toLowerCase());
    if(m)return m.id;
    const firstS=crewList().find(c=>c.peran==='Sales');
    if(firstS)return firstS.id;
  }
  return store('currentSales','');
}
function setCurrentSales(id){save('currentSales',id);renderSales();}
function klienList(){return store('klien',[]);}
function upsertKlien(nama,hp,sales){
  const list=klienList();const ex=list.find(k=>k.nama.toLowerCase()===nama.toLowerCase());
  if(ex){if(hp)ex.hp=hp;if(sales)ex.sales=sales;}
  else list.push({id:'KL'+Date.now().toString(36),nama,hp:hp||'',instansi:'',catatan:'',sales:sales||'',created:Date.now()});
  save('klien',list);
}
function addKlienManual(){
  const g=id=>document.getElementById(id);
  const nama=(g('kl_nama').value||'').trim();if(!nama){toast('Isi nama klien dulu');return;}
  const list=klienList();
  list.push({id:'KL'+Date.now().toString(36),nama,hp:(g('kl_hp').value||'').trim(),instansi:(g('kl_instansi').value||'').trim(),catatan:(g('kl_catatan').value||'').trim(),sales:crewById(currentSales())?crewById(currentSales()).nama:'',created:Date.now()});
  save('klien',list);toast('Klien '+nama+' ditambahkan');renderSales();
}
function delKlien(id){save('klien',klienList().filter(k=>k.id!==id));renderSales();}
function klienPenawaranCount(nama){return penawaran().filter(p=>p.klien.toLowerCase()===nama.toLowerCase()).length;}
function salesPerforma(){
  const sales=crewList().filter(c=>c.peran==='Sales');const pnw=penawaran();
  return sales.map(s=>{
    const mine=pnw.filter(p=>p.salesId===s.id);
    const acc=mine.filter(p=>p.status==='approved');
    const nilaiACC=acc.reduce((a,p)=>a+(p.total||0),0);
    const komisi=acc.reduce((a,p)=>a+(p.komisi||0),0);
    const klien=new Set(mine.map(p=>p.klien.toLowerCase())).size;
    return{id:s.id,nama:s.nama,hp:s.hp,jumlahPenawaran:mine.length,jumlahACC:acc.length,klien,nilaiACC,komisi};
  }).sort((a,b)=>b.nilaiACC-a.nilaiACC);
}
let salesTab='dashboard';
function setSalesTab(k){salesTab=k;const nav=document.querySelector('#view .tabs');if(nav)nav.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.st===k));renderSales();}
function renderSales(){const b=document.getElementById('salesBody');if(!b)return;
  b.innerHTML=salesTab==='penawaran'?salesPenawaranTab():salesTab==='klien'?salesKlienTab():salesTab==='performa'?salesPerformaTab():salesDashboard();
  if(salesTab==='penawaran')calcQuote();
}
function vSales(){
  const tabs=[['dashboard','Dashboard'],['penawaran','Buat Penawaran'],['klien','Data Klien'],['performa','Performa Sales']];
  const nav=tabs.map(([k,l])=>`<button class="tab ${salesTab===k?'active':''}" data-st="${k}" onclick="setSalesTab('${k}')">${l}</button>`).join('');
  return `<div class="hello fade"><h1>Area Sales</h1><p>Katalog, penawaran, data klien, dan performa tim sales</p></div>
    <div class="tabs fade">${nav}</div><div id="salesBody"></div>`;
}
function salesPicker(){
  const u=currentUser();const sales=crewList().filter(c=>c.peran==='Sales');const sid=currentSales();
  if(u.role==='sales'){
    const me=crewById(sid);
    return `<div class="cat-bar" style="padding:0 0 14px"><div style="display:flex;align-items:center;gap:10px"><span class="pill lunas">Akun Pribadi</span><b>${esc(me?me.nama:u.nama)}</b> <span style="font-size:12px;color:var(--muted)">(Sales)</span></div></div>`;
  }
  return `<div class="cat-bar" style="padding:0 0 14px"><div><label class="flbl" style="display:inline;margin-right:8px">Filter Tim Sales</label>
    <select class="finput" style="width:auto;display:inline-block;margin:0;padding:8px 12px" onchange="setCurrentSales(this.value)">
      <option value="">— pilih sales —</option>${sales.map(s=>`<option value="${s.id}" ${s.id===sid?'selected':''}>${esc(s.nama)}</option>`).join('')}</select></div>
    <span style="font-size:12px;color:var(--muted)">Mode tinjauan ${esc(roleCfg().lbl)}</span></div>`;
}
function salesDashboard(){
  const sid=currentSales();const sc=sid?crewById(sid):null;
  const all=salesPerforma();const mine=sc?all.find(x=>x.id===sid):null;
  const pending=penawaran().filter(p=>p.salesId===sid&&p.status==='pending');
  return `${salesPicker()}
    ${!sc?`<div class="panel fade" style="margin:0"><div style="padding:34px 19px;text-align:center;color:var(--muted);font-size:13.5px">Pilih nama Anda di atas untuk melihat dashboard pribadi, atau langsung buat penawaran di tab <b>Buat Penawaran</b>.</div></div>`:`
    <div class="cards fade" style="grid-template-columns:repeat(4,1fr)">
      <div class="scard"><div class="ic b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg></div><div class="lbl">Penawaran Dibuat</div><div class="val mono">${mine.jumlahPenawaran}</div><div class="sub" style="color:var(--muted)">${pending.length} menunggu ACC</div></div>
      <div class="scard"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg></div><div class="lbl">Di-ACC Management</div><div class="val mono">${mine.jumlahACC}</div><div class="sub" style="color:var(--muted)">${mine.jumlahPenawaran?Math.round(mine.jumlahACC/mine.jumlahPenawaran*100):0}% konversi</div></div>
      <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div><div class="lbl">Nilai Trip Di-ACC</div><div class="val mono">${jt(mine.nilaiACC)}</div></div>
      <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div class="lbl">Komisi (5%)</div><div class="val mono">${jt(mine.komisi)}</div><div class="sub" style="color:var(--muted)">dari penawaran yang di-ACC</div></div>
    </div>
    <div class="panel fade" style="margin:0"><div class="panel-h"><h3>Penawaran Saya</h3></div>
      <div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Klien</th><th>Tujuan</th><th>Nilai</th><th>Status</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${
        penawaran().filter(p=>p.salesId===sid).slice().reverse().slice(0,10).map(p=>{const wa=p.hp?waLink(p.hp,waPesan(p)):'';return `<tr><td style="font-weight:600">${esc(p.klien)}</td><td style="font-size:12.5px">${esc(String(p.dest||'').split('(')[0])}</td><td class="price mono">${jt(p.total||0)}</td><td><span class="pill ${p.status==='approved'?'lunas':p.status==='rejected'?'piutang':'dp'}">${p.status==='approved'?'Di-ACC':p.status==='rejected'?'Ditolak':'Menunggu'}</span></td><td style="text-align:right;white-space:nowrap"><button class="btn-acc" style="background:var(--gold);color:var(--navy)" onclick="showPenawaran('${p.id}')">⬇ PDF</button>${wa?`<a class="btn-wa" href="${wa}" target="_blank" rel="noopener">WA</a>`:''}</td></tr>`;}).join('')||'<tr><td colspan="5" style="color:var(--muted);font-size:12.5px">Belum pernah membuat penawaran.</td></tr>'
      }</tbody></table></div></div>`}`;
}
function salesPenawaranTab(){
  const sid=currentSales();const sc=sid?crewById(sid):null;
  return `${salesPicker()}<p style="font-size:12.5px;color:var(--muted);margin:-6px 0 14px">${sc?'Penawaran akan tercatat atas nama <b>'+esc(sc.nama)+'</b>.':'<span style="color:var(--gold-ink)">Pilih nama Anda dulu supaya komisi tercatat dengan benar.</span>'}</p>${katKalkulator()}`;
}
function salesKlienTab(){
  const list=klienList().slice().reverse();
  const rows=list.map(k=>`<tr><td style="font-weight:700">${esc(k.nama)}</td><td style="font-size:12.5px">${esc(k.instansi||'—')}</td><td>${esc(k.hp||'—')}</td><td style="font-size:12px">${esc(k.sales||'—')}</td><td class="mono">${klienPenawaranCount(k.nama)}</td><td style="text-align:right"><button class="pay-del" onclick="if(confirm('Hapus data klien ${esc(k.nama)}?'))delKlien('${k.id}')">✕</button></td></tr>`).join('');
  return `<div class="grid fade" style="grid-template-columns:1fr 320px">
    <div class="panel" style="margin:0"><div class="panel-h"><h3>Data Klien</h3><span style="font-size:12px;color:var(--muted)">${list.length} klien tercatat</span></div>
      <div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Nama</th><th>Instansi</th><th>No. HP</th><th>Sales</th><th>Penawaran</th><th></th></tr></thead><tbody>${rows||'<tr><td colspan="6" style="color:var(--muted);font-size:12.5px">Belum ada data klien. Klien otomatis tercatat saat penawaran dibuat.</td></tr>'}</tbody></table></div></div>
    <div class="side-card" style="margin:0"><div class="panel-h" style="padding:0 0 14px"><h3 style="font-size:14.5px">Tambah Klien</h3></div>
      <label class="flbl">Nama Klien / Instansi</label><input id="kl_nama" class="finput" placeholder="Nama">
      <label class="flbl">Instansi / Asal</label><input id="kl_instansi" class="finput" placeholder="mis. Sekolah, Perusahaan">
      <label class="flbl">No. HP</label><input id="kl_hp" class="finput" placeholder="0812-...">
      <label class="flbl">Catatan</label><textarea id="kl_catatan" class="finput" rows="2" placeholder="Preferensi, catatan khusus..."></textarea>
      <button class="btn-save" onclick="addKlienManual()">+ Tambah Klien</button>
    </div></div>`;
}
function salesPerformaTab(){
  const perf=salesPerforma();
  const tot=perf.reduce((a,s)=>({nilaiACC:a.nilaiACC+s.nilaiACC,komisi:a.komisi+s.komisi,jumlahACC:a.jumlahACC+s.jumlahACC}),{nilaiACC:0,komisi:0,jumlahACC:0});
  const rows=perf.map((s,i)=>`<tr><td style="font-weight:700">${i===0&&s.nilaiACC>0?'🏆 ':''}${esc(s.nama)}</td><td class="mono">${s.jumlahPenawaran}</td><td class="mono">${s.jumlahACC}</td><td class="mono">${s.klien}</td><td class="price mono">${jt(s.nilaiACC)}</td><td class="price mono" style="color:var(--gold-ink)">${jt(s.komisi)}</td></tr>`).join('');
  return `<div class="cards fade" style="grid-template-columns:repeat(3,1fr)">
      <div class="scard"><div class="ic b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/></svg></div><div class="lbl">Tim Sales</div><div class="val mono">${perf.length}</div><div class="sub" style="color:var(--muted)">${tot.jumlahACC} penawaran di-ACC</div></div>
      <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div><div class="lbl">Total Nilai Di-ACC</div><div class="val mono">${jt(tot.nilaiACC)}</div></div>
      <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div class="lbl">Total Komisi</div><div class="val mono">${jt(tot.komisi)}</div></div>
    </div>
    <div class="panel fade" style="margin:0"><div class="panel-h"><h3>Rekap Performa per Sales</h3><span style="font-size:12px;color:var(--muted)">diurutkan dari nilai ACC tertinggi</span></div>
      <div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Nama</th><th>Penawaran</th><th>Di-ACC</th><th>Klien</th><th>Nilai Di-ACC</th><th>Komisi</th></tr></thead>
      <tbody>${rows||'<tr><td colspan="6" style="color:var(--muted);font-size:12.5px">Belum ada data sales. Tambah sales baru di menu Crew.</td></tr>'}</tbody></table></div></div>`;
}
function pnwDecide(id,act){const list=penawaran();const p=list.find(x=>x.id===id);if(p){p.status=act;save('penawaran',list);if(act==='approved')prepAutoFill(id,true);}toast(act==='approved'?'Penawaran di-ACC → masuk Jadwal, Keuangan & Jadwal Vendor':'Penawaran ditolak');go('acc');}
function waLink(hp,text){let n=(hp||'').replace(/\D/g,'');if(!n)return '';if(n[0]==='0')n='62'+n.slice(1);else if(n.slice(0,2)!=='62')n='62'+n;return 'https://wa.me/'+n+'?text='+encodeURIComponent(text);}
function buildItinerary(q,dest){
  const days=Math.max(1,(q.malam||0)+1);const D=(q.dests||[]).slice();const per=Math.max(1,Math.ceil(D.length/days));
  const out=[];
  for(let i=0;i<days;i++){
    const slice=D.slice(i*per,(i+1)*per);const acts=[];
    if(i===0)acts.push('Titik kumpul & keberangkatan menuju '+dest);else acts.push('Sarapan di hotel');
    slice.forEach(d=>acts.push('Kunjungan '+d.name+(d.note?' - '+d.note:'')));
    if(q.malam>0&&i<days-1){acts.push('Makan siang & makan malam');acts.push('Check-in / istirahat di '+(q.hotelName&&!/Tanpa Hotel/i.test(q.hotelName)?q.hotelName:'hotel'));}
    else if(i<days-1){acts.push('Makan siang');}
    if(i===days-1){acts.push('Belanja oleh-oleh khas');acts.push('Perjalanan kembali ke titik kumpul');}
    out.push({hari:i+1,acts});
  }
  return out;
}
let pvActive=null;
function penawaranDetail(rec){
  const g=id=>document.getElementById(id);
  const info=store('info',{nama:'Havist Traveller',hp:'0895 3385 99354',email:'kalabyentertainment@gmail.com',alamat:'Komplek Keluarga Besar H. Mamat, Ds. Kadu, Kec. Curug, Kab. Tangerang'});
  let q,klien,dest,hp;
  if(rec){q={pax:rec.pax,bus:rec.bus,malam:rec.malam,hari:rec.hari||(rec.malam+1),perpax:rec.perpax,total:rec.total,tgl:rec.tgl,armName:rec.armName||'Armada',hotelName:rec.hotelName||'hotel',mFreq:rec.mFreq||3,kaosRate:rec.kaosRate||0,kaosName:rec.kaosName||'',dests:rec.dests||[]};klien=rec.klien;dest=rec.dest;hp=rec.hp||'';}
  else{q=lastQuote;klien=(g('q_klien')?g('q_klien').value.trim():'')||'(Calon Pelanggan)';dest=(g('q_dest')?g('q_dest').value.trim():'')||(q.dests&&q.dests[0]?q.dests[0].city:'Paket Wisata');hp=g('q_hp')?g('q_hp').value.trim():'';}
  const tglTrip=q.tgl?new Date(q.tgl).toLocaleDateString('id-ID',{weekday:'long',day:'numeric',month:'long',year:'numeric'}):'(tanggal menyusul)';
  const no=rec?('PNW/'+(new Date().getFullYear())+'/'+String(rec.created||Date.now()).slice(-5)):('PNW/'+(new Date().getFullYear())+'/'+String(Date.now()).slice(-5));
  const tglSurat=new Date().toLocaleDateString('id-ID',{day:'numeric',month:'long',year:'numeric'});
  const fasil=['Transportasi '+q.armName+' ('+q.bus+' unit)',(q.malam>0?'Akomodasi '+q.malam+' malam ('+(q.hotelName||'hotel')+')':'Trip tanpa menginap'),'Makan '+q.mFreq+'x','Tiket masuk destinasi wisata',(q.kaosRate>0?q.kaosName:'Dokumentasi perjalanan'),'Tour Leader & P3K'];
  return {q,info,klien,dest,hp,tglTrip,no,tglSurat,fasil,itin:buildItinerary(q,dest)};
}
function showPenawaran(id){
  const rec=id?penawaran().find(x=>x.id===id):null;
  if(!rec&&(!lastQuote||!lastQuote.pax)){toast('Isi detail paket & hitung dulu');return;}
  const D=penawaranDetail(rec);pvActive=D;const q=D.q;
  const fasilHTML=D.fasil.map(f=>`<li>${esc(f)}</li>`).join('');
  const itinHTML=D.itin.map(d=>`<div class="pv-day"><div class="pv-day-h">Hari ${d.hari}</div><ul>${d.acts.map(a=>`<li>${esc(a)}</li>`).join('')}</ul></div>`).join('');
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='pvOverlay';
  ov.innerHTML=`<div class="pv-modal">
    <div class="pv-bar"><b>Surat Penawaran</b><div><button class="btn-acc ok" onclick="genPenawaranPDF()">⬇ Unduh PDF</button><button class="btn-acc no" onclick="document.getElementById('pvOverlay').remove()">Tutup</button></div></div>
    <div class="pv-paper" id="pvPaper">
      <div class="pv-letterhead"><div class="pv-brand">HAVIST TRAVELLER</div><div class="pv-tag">Your Travel Dream Makers</div><div class="pv-contact">${esc(D.info.alamat)}<br>${esc(D.info.hp)} · ${esc(D.info.email)}</div></div>
      <h2 class="pv-title">SURAT PENAWARAN HARGA</h2>
      <table class="pv-meta"><tr><td>Nomor</td><td>: ${esc(D.no)}</td><td>Tanggal</td><td>: ${esc(D.tglSurat)}</td></tr></table>
      <p class="pv-to">Kepada Yth.<br><b>${esc(D.klien)}</b>${D.hp?'<br>'+esc(D.hp):''}</p>
      <p>Dengan hormat, berikut kami sampaikan penawaran paket perjalanan wisata sesuai permintaan Bapak/Ibu:</p>
      <table class="pv-sum">
        <tr><td>Tujuan</td><td>: <b>${esc(D.dest)}</b></td></tr>
        <tr><td>Tanggal Berangkat</td><td>: ${esc(D.tglTrip)}</td></tr>
        <tr><td>Durasi</td><td>: ${q.hari} Hari ${q.malam} Malam</td></tr>
        <tr><td>Jumlah Peserta</td><td>: ${q.pax} pax</td></tr>
        <tr><td>Armada</td><td>: ${esc(q.armName)} (${q.bus} unit)</td></tr>
        <tr><td>Akomodasi</td><td>: ${esc(q.malam>0?q.hotelName:'—')}</td></tr>
      </table>
      <div class="pv-price"><span>Harga per Pax</span><b>${rp(q.perpax)}</b></div>
      <div class="pv-price sub"><span>Estimasi Total (${q.pax} pax)</span><b>${rp(q.total)}</b></div>
      <h3 class="pv-h3">Fasilitas Termasuk</h3><ul class="pv-fasil">${fasilHTML}</ul>
      <h3 class="pv-h3">Itinerary Perjalanan</h3><div class="pv-itin">${itinHTML}</div>
      <h3 class="pv-h3">Syarat & Ketentuan</h3><ul class="pv-fasil"><li>DP 30% saat konfirmasi pemesanan.</li><li>Pelunasan maksimal 7 hari sebelum keberangkatan.</li><li>Harga dapat berubah sewaktu-waktu sebelum konfirmasi.</li></ul>
      <p class="pv-close">Demikian penawaran ini kami sampaikan. Atas perhatian dan kerja samanya kami ucapkan terima kasih.</p>
      <div class="pv-sign">Hormat kami,<br><br><b>Havist Traveller</b></div>
    </div>
  </div>`;
  document.body.appendChild(ov);
  ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
async function genPenawaranPDF(){
  if(!window.jspdf){toast('Pustaka PDF belum siap, coba lagi');return;}
  const D=pvActive||penawaranDetail();const q=D.q;const {jsPDF}=window.jspdf;const doc=new jsPDF({unit:'mm',format:'a4'});
  const L=18,R=192,W=R-L;let y=16;
  const NAVY=[14,36,74],GOLD=[180,140,0],GREY=[110,120,135];
  function pageBreak(h){if(y+h>282){doc.addPage();y=16;}}
  function txt(s,x,opt={}){doc.setFont('helvetica',opt.b?'bold':'normal');doc.setFontSize(opt.s||10);if(opt.c)doc.setTextColor(...opt.c);else doc.setTextColor(30,30,30);const lines=doc.splitTextToSize(s,opt.w||W);lines.forEach(ln=>{pageBreak(opt.lh||5.2);doc.text(ln,x,y);y+=opt.lh||5.2;});}
  // letterhead
  doc.setFont('helvetica','bold');doc.setFontSize(20);doc.setTextColor(...NAVY);doc.text('HAVIST TRAVELLER',L,y);y+=6;
  doc.setFont('helvetica','italic');doc.setFontSize(9);doc.setTextColor(...GOLD);doc.text('Your Travel Dream Makers',L,y);y+=5;
  doc.setFont('helvetica','normal');doc.setFontSize(8);doc.setTextColor(...GREY);
  doc.splitTextToSize(D.info.alamat+'  |  '+D.info.hp+'  |  '+D.info.email,W).forEach(ln=>{doc.text(ln,L,y);y+=3.8;});
  y+=2;doc.setDrawColor(...NAVY);doc.setLineWidth(.6);doc.line(L,y,R,y);y+=8;
  doc.setFont('helvetica','bold');doc.setFontSize(13);doc.setTextColor(...NAVY);doc.text('SURAT PENAWARAN HARGA',105,y,{align:'center'});y+=8;
  txt('Nomor : '+D.no+'        Tanggal : '+D.tglSurat,L,{s:9,c:GREY});y+=2;
  txt('Kepada Yth.',L,{s:10});txt(D.klien,L,{b:true,s:10});if(D.hp)txt(D.hp,L,{s:9,c:GREY});y+=2;
  txt('Dengan hormat, berikut kami sampaikan penawaran paket perjalanan wisata sesuai permintaan Bapak/Ibu:',L,{s:10});y+=2;
  const sum=[['Tujuan',D.dest],['Tanggal Berangkat',D.tglTrip],['Durasi',q.hari+' Hari '+q.malam+' Malam'],['Jumlah Peserta',q.pax+' pax'],['Armada',q.armName+' ('+q.bus+' unit)'],['Akomodasi',q.malam>0?q.hotelName:'—']];
  sum.forEach(([k,v])=>{pageBreak(5.4);doc.setFont('helvetica','normal');doc.setFontSize(10);doc.setTextColor(60,60,60);doc.text(k,L,y);doc.text(':',L+42,y);doc.setFont('helvetica','bold');doc.setTextColor(30,30,30);doc.splitTextToSize(String(v),W-46).forEach((ln,i)=>{if(i>0)y+=5;doc.text(ln,L+46,y);});y+=5.4;});
  y+=2;pageBreak(16);doc.setFillColor(245,247,250);doc.rect(L,y,W,14,'F');doc.setTextColor(...NAVY);doc.setFont('helvetica','normal');doc.setFontSize(10);doc.text('Harga per Pax',L+4,y+6);doc.setFont('helvetica','bold');doc.setFontSize(14);doc.text(rp(q.perpax),R-4,y+7,{align:'right'});doc.setFont('helvetica','normal');doc.setFontSize(9);doc.setTextColor(...GREY);doc.text('Estimasi total '+q.pax+' pax : '+rp(q.total),L+4,y+11.5);y+=20;
  function section(t){pageBreak(10);doc.setFont('helvetica','bold');doc.setFontSize(11);doc.setTextColor(...NAVY);doc.text(t,L,y);y+=6;}
  section('Fasilitas Termasuk');D.fasil.forEach(f=>txt('•  '+f,L+2,{s:9.5}));y+=2;
  section('Itinerary Perjalanan');
  D.itin.forEach(d=>{pageBreak(8);doc.setFont('helvetica','bold');doc.setFontSize(10);doc.setTextColor(...GOLD);doc.text('Hari '+d.hari,L+2,y);y+=5;d.acts.forEach(a=>txt('•  '+a,L+6,{s:9.5,w:W-8}));y+=2;});
  section('Syarat & Ketentuan');['DP 30% saat konfirmasi pemesanan.','Pelunasan maksimal 7 hari sebelum keberangkatan.','Harga dapat berubah sewaktu-waktu sebelum konfirmasi.'].forEach(s=>txt('•  '+s,L+2,{s:9.5}));y+=4;
  txt('Demikian penawaran ini kami sampaikan. Atas perhatian dan kerja samanya kami ucapkan terima kasih.',L,{s:10});y+=8;
  txt('Hormat kami,',L,{s:10});y+=10;txt('Havist Traveller',L,{b:true,s:10});
  const blob=doc.output('blob');
  await saveFileToViewer('Penawaran-'+D.klien.replace(/[^\w]+/g,'_')+'.pdf',blob);
}
function waPesan(p){return 'Halo '+p.klien+', berikut penawaran trip '+p.dest+' ('+p.pax+' pax, '+p.malam+' malam): Rp '+p.perpax.toLocaleString('id-ID')+'/pax, total Rp '+p.total.toLocaleString('id-ID')+'. Terima kasih — Havist Traveller.';}
// ---------- PDF: kerangka bersama (kop surat + helper) ----------
function infoPerusahaan(){return store('info',{nama:'Havist Traveller',hp:'0895 3385 99354',email:'kalabyentertainment@gmail.com',alamat:'Komplek Keluarga Besar H. Mamat, Ds. Kadu, Kec. Curug, Kab. Tangerang',rek:''});}
function pdfKit(judul){
  const {jsPDF}=window.jspdf;const doc=new jsPDF({unit:'mm',format:'a4'});
  const info=infoPerusahaan();
  const uph=umumPhotos();
  const L=18,R=192,W=R-L;const NAVY=[14,36,74],GOLD=[180,140,0],GREY=[110,120,135];
  const K={doc,L,R,W,NAVY,GOLD,GREY,info,y:16};
  K.pageBreak=h=>{if(K.y+h>282){doc.addPage();K.y=16;}};
  K.txt=(s,x,opt={})=>{doc.setFont('helvetica',opt.b?'bold':'normal');doc.setFontSize(opt.s||10);doc.setTextColor(...(opt.c||[30,30,30]));doc.splitTextToSize(String(s),opt.w||W).forEach(ln=>{K.pageBreak(opt.lh||5.2);doc.text(ln,x,K.y);K.y+=opt.lh||5.2;});};
  K.section=t=>{K.pageBreak(11);doc.setFont('helvetica','bold');doc.setFontSize(11);doc.setTextColor(...NAVY);doc.text(t,L,K.y);K.y+=6;};
  K.kv=(k,v,wk)=>{K.pageBreak(5.4);doc.setFont('helvetica','normal');doc.setFontSize(10);doc.setTextColor(60,60,60);doc.text(k,L,K.y);doc.text(':',L+(wk||42),K.y);doc.setFont('helvetica','bold');doc.setTextColor(30,30,30);doc.splitTextToSize(String(v),W-(wk||42)-4).forEach((ln,i)=>{if(i>0)K.y+=5;doc.text(ln,L+(wk||42)+4,K.y);});K.y+=5.4;};
  K.rowAmt=(k,v,opt={})=>{K.pageBreak(5.6);doc.setFont('helvetica',opt.b?'bold':'normal');doc.setFontSize(opt.s||10);doc.setTextColor(...(opt.c||[45,45,45]));doc.text(k,L+2,K.y);doc.text(String(v),R-2,K.y,{align:'right'});K.y+=opt.lh||5.6;};
  K.hr=()=>{doc.setDrawColor(215,219,226);doc.setLineWidth(.3);doc.line(L,K.y,R,K.y);K.y+=4;};
  // kop surat
  doc.setFont('helvetica','bold');doc.setFontSize(20);doc.setTextColor(...NAVY);doc.text('HAVIST TRAVELLER',L,K.y);K.y+=6;
  doc.setFont('helvetica','italic');doc.setFontSize(9);doc.setTextColor(...GOLD);doc.text('Your Travel Dream Makers',L,K.y);K.y+=5;
  doc.setFont('helvetica','normal');doc.setFontSize(8);doc.setTextColor(...GREY);
  doc.splitTextToSize(info.alamat+'  |  '+info.hp+'  |  '+info.email,W).forEach(ln=>{doc.text(ln,L,K.y);K.y+=3.8;});
  K.y+=2;doc.setDrawColor(...NAVY);doc.setLineWidth(.6);doc.line(L,K.y,R,K.y);K.y+=8;
  doc.setFont('helvetica','bold');doc.setFontSize(13);doc.setTextColor(...NAVY);doc.text(judul,105,K.y,{align:'center'});K.y+=8;
  return K;
}
async function pdfSave(doc,filename){
  const blob=doc.output('blob');
  await saveFileToViewer(filename,blob);
  return true;
}
function noInvoice(p){return p.inv&&p.inv!=='(dari penawaran)'?p.inv:'INV/'+new Date().getFullYear()+'/'+String(p.id).replace(/\D/g,'').slice(-5).padStart(4,'0');}
// ---------- PDF: INVOICE KLIEN ----------
async function genInvoicePDF(id){
  if(!window.jspdf){toast('Pustaka PDF belum siap, coba lagi');return;}
  const p=allPiutang().find(x=>x.id===id);if(!p){toast('Data piutang tidak ditemukan');return;}
  const t=allTrips().find(x=>x.id===id);
  const paid=clientPaid(p),sisa=clientSisa(p);const[,sl]=clientStatus(p);
  const K=pdfKit('INVOICE');const{doc,L,R,W,NAVY,GOLD,GREY}=K;
  const tglSurat=new Date().toLocaleDateString('id-ID',{day:'numeric',month:'long',year:'numeric'});
  K.txt('Nomor : '+noInvoice(p)+'        Tanggal : '+tglSurat,L,{s:9,c:GREY});K.y+=2;
  K.txt('Kepada Yth.',L,{s:10});K.txt(p.inst,L,{b:true,s:11});K.y+=3;
  K.section('Rincian Tagihan');
  K.kv('Keperluan',t?('Paket wisata '+String(t.dest||'').split('(')[0].trim()):'Paket perjalanan wisata');
  if(t&&t.brk)K.kv('Tanggal Trip',new Date(t.brk).toLocaleDateString('id-ID',{weekday:'long',day:'numeric',month:'long',year:'numeric'}));
  K.kv('Jumlah Peserta',(p.pax||0)+' pax');
  if(p.pax>0)K.kv('Harga per Pax',rp(Math.round((p.tagih||0)/p.pax)));
  K.y+=3;K.hr();
  K.rowAmt('Total Tagihan',rp(p.tagih||0),{b:true,s:11});K.hr();
  K.section('Riwayat Pembayaran');
  const hist=[];if(p.dp>0)hist.push(['DP awal','',p.dp]);
  payClientList(p.id).forEach(x=>hist.push([x.termin||'Pembayaran',x.date||'',+x.amount||0]));
  if(hist.length)hist.forEach(([k,d,v])=>K.rowAmt(k+(d?'  ('+new Date(d).toLocaleDateString('id-ID',{day:'2-digit',month:'short',year:'numeric'})+')':''),'- '+rp(v),{s:9.5,c:[43,157,110]}));
  else K.txt('Belum ada pembayaran yang tercatat.',L+2,{s:9.5,c:GREY});
  K.y+=1;K.hr();
  K.pageBreak(18);doc.setFillColor(sisa>0?253:245,sisa>0?240:250,sisa>0?240:247);doc.rect(L,K.y,W,15,'F');
  doc.setFont('helvetica','normal');doc.setFontSize(10);doc.setTextColor(...NAVY);doc.text(sisa>0?'Sisa yang Harus Dibayar':'Status Pembayaran',L+4,K.y+6);
  doc.setFont('helvetica','bold');doc.setFontSize(14);doc.setTextColor(...(sisa>0?[197,48,48]:[43,157,110]));doc.text(sisa>0?rp(sisa):'LUNAS',R-4,K.y+8,{align:'right'});
  doc.setFont('helvetica','normal');doc.setFontSize(9);doc.setTextColor(...GREY);doc.text('Sudah dibayar '+rp(paid)+' dari '+rp(p.tagih||0)+'  ('+sl+')',L+4,K.y+12);K.y+=21;
  if(sisa>0){
    K.section('Pembayaran');
    if(K.info.rek)K.txt('Transfer ke: '+K.info.rek,L+2,{s:10,b:true});
    else K.txt('Hubungi '+K.info.hp+' untuk informasi rekening pembayaran.',L+2,{s:9.5});
    if(t&&t.brk){const batas=new Date(t.brk);batas.setDate(batas.getDate()-7);
      K.txt('Pelunasan paling lambat '+batas.toLocaleDateString('id-ID',{day:'numeric',month:'long',year:'numeric'})+' (H-7 keberangkatan).',L+2,{s:9.5,c:GREY});}
    K.y+=2;
  }
  K.txt('Mohon konfirmasi setelah melakukan pembayaran. Terima kasih atas kepercayaan Bapak/Ibu.',L,{s:10});K.y+=8;
  K.txt('Hormat kami,',L,{s:10});K.y+=10;K.txt('Havist Traveller',L,{b:true,s:10});
  await pdfSave(doc,'Invoice-'+String(p.inst).replace(/[^\w]+/g,'_')+'.pdf');
}
// ---------- PDF: RUNDOWN / ITINERARY TRIP ----------
function rundownItin(t){
  const hari=tripDays(t);
  const dsts=prepTrip(t.id).filter(x=>x.kat==='Wisata / Tiket'&&!/belum ditentukan/i.test(x.vendor)).map(x=>({name:x.vendor,note:''}));
  const dest=String(t.dest||'').split('(')[0].trim()||'destinasi';
  const q={malam:Math.max(0,hari-1),dests:dsts.length?dsts:[{name:'destinasi wisata '+dest,note:''}],hotelName:(prepTrip(t.id).find(x=>x.kat==='Hotel / Villa')||{}).vendor||t.hotel||''};
  return buildItinerary(q,dest);
}
async function genRundownPDF(id){
  if(!window.jspdf){toast('Pustaka PDF belum siap, coba lagi');return;}
  const t=allTrips().find(x=>x.id===id);if(!t){toast('Trip tidak ditemukan');return;}
  const tls=tripCrewNames(t.id,'tl'),mds=tripCrewNames(t.id,'media');const tl=tls[0],md=mds[0];
  const hari=tripDays(t);const items=prepTrip(t.id);
  const arm=items.find(x=>x.kat==='Transport / Bus'),hot=items.find(x=>x.kat==='Hotel / Villa');
  const K=pdfKit('RUNDOWN PERJALANAN');const{doc,L,R,W,NAVY,GOLD,GREY}=K;
  K.txt(t.inst,L,{b:true,s:12});K.txt(String(t.dest||'').split('(')[0].trim(),L,{s:10,c:GOLD});K.y+=3;
  K.section('Informasi Trip');
  K.kv('Tanggal',(t.brk?new Date(t.brk).toLocaleDateString('id-ID',{weekday:'long',day:'numeric',month:'long',year:'numeric'}):'—')+(t.pul?' s/d '+new Date(t.pul).toLocaleDateString('id-ID',{day:'numeric',month:'long'}):''));
  K.kv('Durasi',hari+' hari '+Math.max(0,hari-1)+' malam');
  K.kv('Jumlah Peserta',(t.pax||0)+' pax');
  K.kv('Armada',arm?arm.vendor:(t.armada||(t.bus?t.bus+' unit bus':'—')));
  K.kv('Akomodasi',hot?hot.vendor:(t.hotel||'—'));
  K.kv('Status',STLBL[tripStatus(t)]);
  K.y+=3;
  K.section('Crew Bertugas');
  K.kv('Tour Leader',tls.length?tls.map(c=>c.nama+(c.hp?' ('+c.hp+')':'')).join(', '):'belum ditugaskan');
  K.kv('Media / Dokumentasi',mds.length?mds.map(c=>c.nama+(c.hp?' ('+c.hp+')':'')).join(', '):'belum ditugaskan');
  K.kv('Narahubung',K.info.nama+' — '+K.info.hp);
  K.y+=3;
  K.section('Susunan Acara');
  rundownItin(t).forEach(d=>{K.pageBreak(9);doc.setFont('helvetica','bold');doc.setFontSize(10);doc.setTextColor(...GOLD);doc.text('Hari '+d.hari,L+2,K.y);K.y+=5;
    d.acts.forEach(x=>K.txt('•  '+x,L+6,{s:9.5,w:W-8}));K.y+=2;});
  if(items.length){
    K.section('Vendor & Perlengkapan');
    items.forEach(x=>K.rowAmt(x.kat.split(' ')[0]+' — '+x.vendor,x.due?'tempo '+new Date(x.due).toLocaleDateString('id-ID',{day:'2-digit',month:'short'}):'—',{s:9.5}));
    K.y+=2;
  }
  const cl=store('checklist',{})[id]||CHECKLIST_DEF.map(x=>({item:x,done:false}));
  K.section('Checklist Persiapan');
  cl.forEach(c=>K.txt((c.done?'[v]  ':'[  ]  ')+c.item,L+2,{s:9.5,c:c.done?[43,157,110]:[45,45,45]}));
  K.y+=5;
  K.txt('Dokumen ini dibuat otomatis dari data Management Havist Traveller.',L,{s:8.5,c:GREY});
  await pdfSave(doc,'Rundown-'+String(t.inst).replace(/[^\w]+/g,'_')+'.pdf');
}
function katHotel(){
  const H=CAT.hotels;const regions=[...new Set(H.map(h=>h.region))];
  const PER=3;const pageRegions=pageSlice(regions,katHotelPage,PER);
  const blocks=pageRegions.map(r=>{const rows=H.map((h,i)=>[h,i]).filter(([h])=>h.region===r).map(([h,i])=>`<tr class="clk" onclick="openCatForm('hotels',${i})"><td style="font-weight:600">${esc(h.name)}</td><td class="mono">${rp(h.wd)}</td><td class="mono">${rp(h.we)}</td><td style="text-align:right"><button class="btn-acc no" onclick="event.stopPropagation();openCatForm('hotels',${i})">Edit</button></td></tr>`).join('');
    return `<div class="panel" style="margin-bottom:18px"><div class="panel-h"><h3 style="font-size:14px">${esc(r)} <span style="color:var(--muted);font-size:12px;font-weight:600">(${H.filter(h=>h.region===r).length})</span></h3></div><div class="tbl-scroll"><table style="margin-top:10px"><thead><tr><th>Hotel</th><th>Weekday</th><th>Weekend</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;}).join('');
  return `<div class="fade">${catToolbar('hotels',H.length+' hotel di '+regions.length+' wilayah · harga per kamar/malam')}${blocks}${pagerHTML(regions.length,katHotelPage,PER,'setKatHotelPage')}</div>`;
}
function katDestinasi(){
  const D=CAT.dests;const cities=[...new Set(D.map(d=>d.city))];
  const PER=3;const pageCities=pageSlice(cities,katDestPage,PER);
  const blocks=pageCities.map(c=>{const rows=D.map((d,i)=>[d,i]).filter(([d])=>d.city===c).map(([d,i])=>`<tr class="clk" onclick="openCatForm('dests',${i})"><td style="font-weight:600">${esc(d.name)}</td><td style="color:var(--muted);font-size:12.5px">${esc(d.note)}</td><td class="mono">${d.price?rp(d.price):'<span style=color:var(--green)>Gratis</span>'}</td><td style="text-align:right"><button class="btn-acc no" onclick="event.stopPropagation();openCatForm('dests',${i})">Edit</button></td></tr>`).join('');
    return `<div class="panel" style="margin-bottom:18px"><div class="panel-h"><h3 style="font-size:14px">${esc(c)} <span style="color:var(--muted);font-size:12px;font-weight:600">(${D.filter(d=>d.city===c).length})</span></h3></div><div class="tbl-scroll"><table style="margin-top:10px"><thead><tr><th>Destinasi</th><th>Aktivitas</th><th>Harga/pax</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;}).join('');
  return `<div class="fade">${catToolbar('dests',D.length+' destinasi di '+cities.length+' kota')}${blocks}${pagerHTML(cities.length,katDestPage,PER,'setKatDestPage')}</div>`;
}
function katArmada(){
  const A=CAT.armada,K=CAT.kaos;
  const arm=A.map((a,i)=>`<tr class="clk" onclick="openCatForm('armada',${i})"><td style="font-weight:600">${esc(a.name)}</td><td class="mono">${rp(a.rate)} / hari</td><td class="mono">${armSeat(a)} seat</td><td style="text-align:right"><button class="btn-acc no" onclick="event.stopPropagation();openCatForm('armada',${i})">Edit</button></td></tr>`).join('');
  const kaos=K.map((k,i)=>[k,i]).filter(([k])=>k.price>0).map(([k,i])=>`<tr class="clk" onclick="openCatForm('kaos',${i})"><td style="font-weight:600">${esc(k.name)}</td><td class="mono">${rp(k.price)} / pcs</td><td style="text-align:right"><button class="btn-acc no" onclick="event.stopPropagation();openCatForm('kaos',${i})">Edit</button></td></tr>`).join('');
  return `<div class="grid fade" style="grid-template-columns:1fr 1fr">
    <div class="panel" style="margin:0"><div class="panel-h"><h3>Armada Transportasi</h3></div>${catToolbar('armada',A.length+' jenis')}<div class="tbl-scroll"><table style="margin-top:4px"><thead><tr><th>Jenis</th><th>Tarif</th><th>Kapasitas</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${arm}</tbody></table></div></div>
    <div class="panel" style="margin:0"><div class="panel-h"><h3>Merchandise / Kaos</h3></div>${catToolbar('kaos',K.filter(k=>k.price>0).length+' jenis')}<div class="tbl-scroll"><table style="margin-top:4px"><thead><tr><th>Jenis</th><th>Harga</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${kaos}</tbody></table></div></div>
  </div>`;
}

// ---- prototype state (localStorage, aman dengan try/catch) ----
const _memStore={};
function store(k,def){
  const key='havist_'+k;
  try{const v=localStorage.getItem(key);if(v!=null)return JSON.parse(v);}catch(e){}
  return key in _memStore?JSON.parse(_memStore[key]):def;
}
function save(k,v){
  const key='havist_'+k,str=JSON.stringify(v);
  _memStore[key]=str;
  try{localStorage.setItem(key,str);}catch(e){}
  if(k!=='currentUser'&&k!=='fbConfig'){clearTimeout(_hostSyncTimer);_hostSyncTimer=setTimeout(()=>pushToHosting(true),600);}
}

const SEED_ACC=[
  {id:'A1',klien:'SMPN 4 Cikupa',pax:280,dest:'Yogyakarta (Malioboro, Keraton)',sales:'Dewi',nilai:154000000,dp:30},
  {id:'A2',klien:'PT Surya Toto',pax:60,dest:'Bandung (Tangkuban Perahu)',sales:'Fajar',nilai:33000000,dp:50},
  {id:'A3',klien:'SDN Kutabumi 2',pax:120,dest:'Bogor (Pelita Desa)',sales:'Rian',nilai:42000000,dp:0},
];
function accState(){return store('acc',{});}  // {id:'approved'|'rejected'}
function seedAccItems(){const ed=store('seedAccEdits',{});return SEED_ACC.map(a=>ed[a.id]?Object.assign({},a,ed[a.id]):a);}
function accDecide(id,act){const s=accState();s[id]=act;save('acc',s);toast(act==='approved'?'Klien di-ACC → masuk jadwal':'Pengajuan ditolak, dikembalikan ke Sales');go('acc');}
let accDonePage=1;
function setAccDonePage(p){accDonePage=p;go('acc');}
function inferArmRate(p){
  if(p.armRate!=null&&p.armRate>0)return +p.armRate;
  const f=CAT.armada.find(a=>a.name===p.armName);return f?f.rate:0;
}
function inferHotelRate(p){
  if(p.hotelRate!=null&&p.hotelRate>0)return +p.hotelRate;
  if(!p.hotelName||/Tanpa Hotel/i.test(p.hotelName))return 0;
  const f=CAT.hotels.find(h=>(p.hotelName||'').includes(h.name));
  return f?(p.isWknd?f.we:f.wd):0;
}
function openAccReview(id){
  const p=penawaran().find(x=>x.id===id);if(!p)return;
  const old=document.getElementById('accRevOv');if(old)old.remove();
  const pax=p.pax||1, hari=p.hari||((p.malam||0)+1), malam=p.malam||0, bus=p.bus||1;
  const kamar=malam>0?(p.kamar||Math.ceil(pax/(p.share||4))):0;
  const armRate=inferArmRate(p), hotelRate=inferHotelRate(p);
  const mFreq=p.mFreq!=null?p.mFreq:3, mPrice=p.mPrice||35000, kaosRate=p.kaosRate||0;
  const destRows=(p.dests&&p.dests.length)?p.dests.map((d,i)=>`<tr>
    <td><div style="font-weight:600">${esc(d.name)}</div><div style="font-size:11px;color:var(--muted)">Tiket × ${pax} pax</div></td>
    <td><input id="ar_dest_${i}" class="finput ar-dest-price" data-idx="${i}" type="number" style="margin:0;padding:6px 8px;width:125px" value="${d.price||0}" oninput="calcAccReview('${p.id}',true)"></td>
    <td class="price mono" id="ar_sub_dest_${i}">${rp((d.price||0)*pax)}</td>
  </tr>`).join(''):'<tr><td colspan="3" style="color:var(--muted);font-size:12px">Tidak ada destinasi berbayar yang dipilih</td></tr>';
  const wa=p.hp?waLink(p.hp,waPesan(p)):'';
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='accRevOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:660px"><div class="pv-bar"><b>Review &amp; Edit Harga Item — ${esc(p.klien)}</b><div><button class="btn-acc" style="background:var(--gold);color:var(--navy);margin-right:6px" onclick="saveAccRevision('${p.id}',false,true)">⬇ PDF</button><button class="btn-acc no" onclick="document.getElementById('accRevOv').remove()">Tutup</button></div></div>
    <div style="background:var(--bg);padding:16px;max-height:80vh;overflow:auto">
      <div class="td-card"><h5>Info Pengajuan (${esc(p.salesName||'Sales')})</h5>
        <div class="td-row"><span>Klien / Tujuan</span><b>${esc(p.klien)} · ${esc(p.dest)}</b></div>
        <div class="td-row"><span>Jadwal &amp; Peserta</span><b>${p.tgl?dateID(p.tgl):'—'} · ${hari} hari ${malam} malam · ${pax} pax</b></div>
        <div class="td-row"><span>No. HP</span><b>${esc(p.hp||'—')}</b></div>
      </div>
      <div class="td-card"><h5>Edit Harga Item yang Dipilih Sales</h5>
        <div class="tbl-scroll"><table style="margin-top:6px"><thead><tr><th>Item Dipilih</th><th>Harga Satuan (Rp)</th><th style="text-align:right">Subtotal</th></tr></thead><tbody>
          <tr><td><div style="font-weight:600">${esc(p.armName||'Armada')}</div><div style="font-size:11px;color:var(--muted)">${bus} unit × ${hari} hari</div></td>
            <td><input id="ar_arm_rate" class="finput" type="number" style="margin:0;padding:6px 8px;width:125px" value="${armRate}" oninput="calcAccReview('${p.id}',true)"></td>
            <td class="price mono" id="ar_sub_arm">${rp(armRate*bus*hari)}</td></tr>
          ${malam>0?`<tr><td><div style="font-weight:600">${esc(p.hotelName||'Hotel')}</div><div style="font-size:11px;color:var(--muted)">${kamar} kamar × ${malam} malam</div></td>
            <td><input id="ar_hotel_rate" class="finput" type="number" style="margin:0;padding:6px 8px;width:125px" value="${hotelRate}" oninput="calcAccReview('${p.id}',true)"></td>
            <td class="price mono" id="ar_sub_hotel">${rp(hotelRate*kamar*malam)}</td></tr>`:''}
          <tr><td><div style="font-weight:600">Konsumsi / Makan</div><div style="font-size:11px;color:var(--muted)">${mFreq}× × ${pax} pax</div></td>
            <td><input id="ar_mprice" class="finput" type="number" style="margin:0;padding:6px 8px;width:125px" value="${mPrice}" oninput="calcAccReview('${p.id}',true)"></td>
            <td class="price mono" id="ar_sub_makan">${rp(mFreq*mPrice*pax)}</td></tr>
          ${kaosRate>0||(p.kaosName&&!/Tanpa/i.test(p.kaosName))?`<tr><td><div style="font-weight:600">${esc(p.kaosName||'Kaos')}</div><div style="font-size:11px;color:var(--muted)">${pax} pcs</div></td>
            <td><input id="ar_kaos_rate" class="finput" type="number" style="margin:0;padding:6px 8px;width:125px" value="${kaosRate}" oninput="calcAccReview('${p.id}',true)"></td>
            <td class="price mono" id="ar_sub_kaos">${rp(kaosRate*pax)}</td></tr>`:''}
          ${destRows}
          <tr><td><div style="font-weight:600">Biaya Tambahan</div><input id="ar_extra_note" class="finput" style="margin:4px 0 0;padding:4px 7px;font-size:11.5px" placeholder="mis. Tol, parkir, tip" value="${esc(p.extraNote||'')}"></td>
            <td><input id="ar_extra_cost" class="finput" type="number" style="margin:0;padding:6px 8px;width:125px" value="${p.extraCost||0}" oninput="calcAccReview('${p.id}',true)"></td>
            <td class="price mono" id="ar_sub_extra">${rp(p.extraCost||0)}</td></tr>
        </tbody></table></div>
      </div>
      <div class="td-card"><h5>Total &amp; Harga Jual ke Klien</h5>
        <div id="ar_modal_info" style="font-size:12px;color:var(--muted);margin-bottom:8px"></div>
        <div class="frow">
          <div><label class="flbl">Harga Jual per Pax (Rp)</label><input id="ar_perpax" class="finput" type="number" value="${p.perpax||0}" oninput="calcAccReview('${p.id}',false)"></div>
          <div><label class="flbl">Diskon Klien (Rp)</label><input id="ar_diskon" class="finput" type="number" value="${p.diskon||0}" oninput="calcAccReview('${p.id}',false)"></div>
        </div>
        <label class="flbl">Catatan Revisi (opsional)</label>
        <input id="ar_note" class="finput" placeholder="mis. Penyesuaian harga hotel &amp; bus untuk pengajuan ulang" value="${esc(p.revisiNote||'')}">
        <div class="pay-sum" style="margin-top:10px">
          <div><span>Total Baru</span><b id="ar_total">${rp(p.total||0)}</b></div>
          <div><span>Komisi Sales (5%)</span><b id="ar_komisi" style="color:var(--gold-ink)">${rp(p.komisi||0)}</b></div>
          <div><span>Est. Laba</span><b id="ar_laba" style="color:${(p.laba||0)<0?'var(--red)':'var(--green)'}">${rp(p.laba||0)}</b></div>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px">
          <button class="btn-save" style="flex:1;background:var(--blue)" onclick="saveAccRevision('${p.id}',false)">Simpan Revisi Harga</button>
          <button class="btn-save" style="flex:1;background:var(--green)" onclick="saveAccRevision('${p.id}',true)">✓ ACC Sekarang</button>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">
          <button class="btn-acc" style="background:var(--gold);color:var(--navy);flex:1;padding:8px" onclick="saveAccRevision('${p.id}',false,true)">⬇ Simpan &amp; Buka PDF</button>
          ${wa?`<a class="btn-wa" style="flex:1;text-align:center;padding:8px" href="${wa}" target="_blank" rel="noopener">💬 Kirim WA</a>`:''}
          <button class="btn-acc no" style="color:var(--red);padding:8px 12px" onclick="document.getElementById('accRevOv').remove();pnwDecide('${p.id}','rejected')">Tolak</button>
        </div>
      </div>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
  calcAccReview(id,false);
}
function readAccItemPrices(p){
  const g=id=>document.getElementById(id);
  const pax=p.pax||1, hari=p.hari||((p.malam||0)+1), malam=p.malam||0, bus=p.bus||1;
  const kamar=malam>0?(p.kamar||Math.ceil(pax/(p.share||4))):0;
  const armRate=Math.max(0,+(g('ar_arm_rate')?g('ar_arm_rate').value:inferArmRate(p))||0);
  const hotelRate=malam>0?Math.max(0,+(g('ar_hotel_rate')?g('ar_hotel_rate').value:inferHotelRate(p))||0):0;
  const mFreq=p.mFreq!=null?p.mFreq:3;
  const mPrice=Math.max(0,+(g('ar_mprice')?g('ar_mprice').value:(p.mPrice||35000))||0);
  const kaosEl=g('ar_kaos_rate');
  const kaosRate=kaosEl?Math.max(0,+kaosEl.value||0):(p.kaosRate||0);
  const extraCost=Math.max(0,+(g('ar_extra_cost')?g('ar_extra_cost').value:(p.extraCost||0))||0);
  const extraNote=g('ar_extra_note')?g('ar_extra_note').value.trim():(p.extraNote||'');
  const dests=(p.dests||[]).map((d,i)=>{const el=g('ar_dest_'+i);const pr=el?Math.max(0,+el.value||0):(d.price||0);return Object.assign({},d,{price:pr});});
  const subArm=armRate*bus*hari, subHotel=hotelRate*kamar*malam, subMakan=mFreq*mPrice*pax, subKaos=kaosRate*pax;
  const subDest=dests.reduce((s,d)=>s+d.price*pax,0);
  const modal=Math.round(subArm+subHotel+subMakan+subKaos+subDest+extraCost);
  const markup=1+(store('markup',20)/100), mk=modal*markup;
  const foc=Math.min(Math.floor(pax/10),25), jualGrup=mk-(foc*(mk/pax));
  const diskon=Math.max(0,+(g('ar_diskon')?g('ar_diskon').value:(p.diskon||0))||0);
  const recPerpax=Math.ceil((Math.max(0,jualGrup-diskon)/pax)/1000)*1000;
  return {pax,armRate,hotelRate,kamar,mPrice,kaosRate,extraCost,extraNote,dests,subArm,subHotel,subMakan,subKaos,modal,diskon,recPerpax};
}
function calcAccReview(id,recalcPerpax){
  const g=id=>document.getElementById(id);if(!g('ar_perpax'))return;
  const p=penawaran().find(x=>x.id===id);if(!p)return;
  const c=readAccItemPrices(p);
  if(g('ar_sub_arm'))g('ar_sub_arm').textContent=rp(c.subArm);
  if(g('ar_sub_hotel'))g('ar_sub_hotel').textContent=rp(c.subHotel);
  if(g('ar_sub_makan'))g('ar_sub_makan').textContent=rp(c.subMakan);
  if(g('ar_sub_kaos'))g('ar_sub_kaos').textContent=rp(c.subKaos);
  if(g('ar_sub_extra'))g('ar_sub_extra').textContent=rp(c.extraCost);
  c.dests.forEach((d,i)=>{if(g('ar_sub_dest_'+i))g('ar_sub_dest_'+i).textContent=rp(d.price*c.pax);});
  if(recalcPerpax)g('ar_perpax').value=c.recPerpax;
  const perpax=Math.max(0,parseInt(g('ar_perpax').value)||0);
  const totalBaru=Math.max(0,perpax*c.pax-c.diskon);
  const komisiBaru=Math.round(totalBaru*0.05);
  const labaBaru=totalBaru-c.modal;
  if(g('ar_modal_info'))g('ar_modal_info').innerHTML=`Total modal item: <b>${rp(c.modal)}</b> · saran harga jual sistem: <b>${rp(c.recPerpax)}/pax</b>`;
  g('ar_total').textContent=rp(totalBaru);
  g('ar_komisi').textContent=rp(komisiBaru);
  const le=g('ar_laba');le.textContent=rp(labaBaru);le.style.color=labaBaru<0?'var(--red)':'var(--green)';
}
function saveAccRevision(id,andApprove,andPdf){
  const g=id=>document.getElementById(id);
  const list=penawaran();const p=list.find(x=>x.id===id);if(!p)return;
  const c=readAccItemPrices(p);
  const perpax=Math.max(0,parseInt(g('ar_perpax').value)||0);
  const totalBaru=Math.max(0,perpax*c.pax-c.diskon);
  p.armRate=c.armRate;p.hotelRate=c.hotelRate;p.kamar=c.kamar;
  p.mPrice=c.mPrice;p.kaosRate=c.kaosRate;p.extraCost=c.extraCost;p.extraNote=c.extraNote;p.dests=c.dests;
  p.perpax=perpax;p.diskon=c.diskon;p.total=totalBaru;p.komisi=Math.round(totalBaru*0.05);p.laba=totalBaru-c.modal;
  p.revisi=true;p.revisiNote=(g('ar_note').value||'').trim();
  if(andApprove)p.status='approved';
  save('penawaran',list);
  if(andApprove)prepAutoFill(id,true);
  const ov=document.getElementById('accRevOv');if(ov)ov.remove();
  toast(andApprove?'✓ Harga item diperbarui & Penawaran di-ACC':'✓ Harga item penawaran diperbarui — siap diajukan ulang');
  go('acc');
  if(andPdf)setTimeout(()=>showPenawaran(id),40);
}
function openSeedAccReview(id){
  const a=seedAccItems().find(x=>x.id===id);if(!a)return;
  const old=document.getElementById('accRevOv');if(old)old.remove();
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='accRevOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:460px"><div class="pv-bar"><b>Review Pengajuan — ${esc(a.klien)}</b><button class="btn-acc no" onclick="document.getElementById('accRevOv').remove()">Tutup</button></div>
    <div style="background:var(--bg);padding:16px">
      <div class="td-card"><h5>Detail Pengajuan Sales</h5>
        <div class="td-row"><span>Klien</span><b>${esc(a.klien)}</b></div>
        <div class="td-row"><span>Destinasi</span><b>${esc(a.dest)}</b></div>
        <div class="td-row"><span>Sales</span><b>${esc(a.sales)}</b></div>
        <div class="td-row"><span>Peserta</span><b>${a.pax} pax</b></div>
        <div class="td-row"><span>DP Awal</span><b>${a.dp}%</b></div>
      </div>
      <div class="td-card"><h5>Edit Nilai Penawaran (Rp)</h5>
        <input id="sa_nilai" class="finput" type="number" value="${a.nilai||0}">
        <div style="display:flex;gap:8px;margin-top:10px">
          <button class="btn-save" style="flex:1;background:var(--blue)" onclick="saveSeedAccEdit('${a.id}',false)">Simpan Nilai</button>
          <button class="btn-save" style="flex:1;background:var(--green)" onclick="saveSeedAccEdit('${a.id}',true)">✓ ACC Sekarang</button>
        </div>
      </div>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function saveSeedAccEdit(id,andApprove){
  const nilai=Math.max(0,parseInt(document.getElementById('sa_nilai').value)||0);
  const ed=store('seedAccEdits',{});ed[id]={nilai};save('seedAccEdits',ed);
  const ov=document.getElementById('accRevOv');if(ov)ov.remove();
  if(andApprove){accDecide(id,'approved');return;}
  toast('Nilai pengajuan diperbarui');go('acc');
}
function vACC(){
  const s=accState();const seeds=seedAccItems();const pending=seeds.filter(a=>!s[a.id]);
  const done=seeds.filter(a=>s[a.id]);
  const rows=pending.map(a=>`<tr class="clk" onclick="openSeedAccReview('${a.id}')"><td><div class="trip"><div class="th" style="background:var(--blue)">${ab(a.klien)}</div><div><div class="nm">${esc(a.klien)}</div><div class="loc">${esc(a.dest.split('(')[0])} · ${a.pax} pax</div></div></div></td><td style="font-size:12.5px">${esc(a.sales)}</td><td class="price mono">${jt(a.nilai)}</td><td><span class="pill ${a.dp>0?'dp':'piutang'}">DP ${a.dp}%</span></td><td style="text-align:right;white-space:nowrap" onclick="event.stopPropagation()"><button class="btn-acc no" style="margin-right:4px" onclick="openSeedAccReview('${a.id}')">Review</button><button class="btn-acc ok" onclick="accDecide('${a.id}','approved')">ACC</button><button class="btn-acc no" onclick="accDecide('${a.id}','rejected')">Tolak</button></td></tr>`).join('');
  const doneRowsArr=done.map(a=>`<tr><td><div class="nm" style="font-weight:700">${esc(a.klien)}</div><div class="loc" style="font-size:11.5px;color:var(--muted)">${esc(a.sales)} · ${jt(a.nilai)}</div></td><td><span class="pill ${s[a.id]==='approved'?'lunas':'piutang'}">${s[a.id]==='approved'?'Di-ACC':'Ditolak'}</span></td><td style="text-align:right"><button class="btn-acc no" onclick="(function(){const x=accState();delete x['${a.id}'];save('acc',x);go('acc');})()">Batalkan</button></td></tr>`);
  const pnwPending=penawaran().filter(p=>p.status==='pending');
  const pnwRows=pnwPending.map(p=>{const wa=p.hp?waLink(p.hp,waPesan(p)):'';
    return `<tr class="clk" onclick="openAccReview('${p.id}')"><td><div class="trip"><div class="th" style="background:var(--gold);color:var(--navy)">${ab(p.klien)}</div><div><div class="nm">${esc(p.klien)} ${p.revisi?'<span class="pill dp" style="font-size:10px">Revisi</span>':''}</div><div class="loc">${esc(p.dest)} · ${p.pax} pax · ${p.malam} malam${p.hp?' · '+esc(p.hp):''}${p.revisiNote?' · <i>'+esc(p.revisiNote)+'</i>':''}</div></div></div></td><td class="mono">${rp(p.perpax)}/pax</td><td class="price mono">${jt(p.total)}</td><td style="text-align:right;white-space:nowrap" onclick="event.stopPropagation()"><button class="btn-acc no" style="margin-right:4px" onclick="openAccReview('${p.id}')">Review / Edit</button><button class="btn-acc" style="background:var(--gold);color:var(--navy)" onclick="showPenawaran('${p.id}')">PDF</button>${wa?`<a class="btn-wa" href="${wa}" target="_blank" rel="noopener">WA</a>`:''}<button class="btn-acc ok" onclick="pnwDecide('${p.id}','approved')">ACC</button><button class="btn-acc no" onclick="pnwDecide('${p.id}','rejected')">Tolak</button></td></tr>`;}).join('');
  const pnwDone=penawaran().filter(p=>p.status&&p.status!=='pending');
  const pnwDoneRowsArr=pnwDone.map(p=>`<tr><td><div class="nm" style="font-weight:700">${esc(p.klien)}</div><div class="loc" style="font-size:11.5px;color:var(--muted)">${esc(p.dest)} · ${jt(p.total)}</div></td><td><span class="pill ${p.status==='approved'?'lunas':'piutang'}">${p.status==='approved'?'Di-ACC':'Ditolak'}</span></td><td style="text-align:right;white-space:nowrap"><button class="btn-acc" style="background:var(--gold);color:var(--navy)" onclick="showPenawaran('${p.id}')">PDF</button><button class="btn-acc no" onclick="pnwDecide('${p.id}','pending')">Kembalikan</button></td></tr>`);
  const allDoneArr=pnwDoneRowsArr.concat(doneRowsArr);
  const PER_DONE=10;const doneRowsHTML=pageSlice(allDoneArr,accDonePage,PER_DONE).join('');
  const totalPending=pending.length+pnwPending.length;
  return `<div class="hello fade"><h1>ACC Klien</h1><p>${totalPending} pengajuan menunggu persetujuan · klik baris untuk review detail &amp; edit harga</p></div>
  ${pnwPending.length?`<div class="panel fade"><div class="panel-h"><h3>Penawaran Baru dari Kalkulator <span style="color:var(--gold-ink);font-size:13px">(${pnwPending.length})</span></h3></div><div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Klien & Tujuan</th><th>Harga/pax</th><th>Nilai Total</th><th style="text-align:right">Keputusan</th></tr></thead><tbody>${pnwRows}</tbody></table></div></div>`:''}
  <div class="panel fade"><div class="panel-h"><h3>Pengajuan Sales (contoh) <span style="color:var(--red);font-size:13px">(${pending.length})</span></h3></div>
  ${pending.length?`<div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Klien</th><th>Sales</th><th>Nilai</th><th>DP</th><th style="text-align:right">Keputusan</th></tr></thead><tbody>${rows}</tbody></table></div>`:`<div style="padding:34px 19px;text-align:center;color:var(--muted);font-size:13.5px">Semua pengajuan contoh sudah diproses 🎉</div>`}
  </div>
  ${allDoneArr.length?`<div class="panel fade" style="margin:0"><div class="panel-h"><h3>Sudah Diproses</h3></div><div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Klien</th><th>Status</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${doneRowsHTML}</tbody></table></div>${pagerHTML(allDoneArr.length,accDonePage,PER_DONE,'setAccDonePage')}</div>`:''}
  <p style="font-size:12px;color:var(--muted-2);margin-top:14px">Klik baris penawaran untuk meninjau rincian paket (armada, hotel, destinasi, laba) dan mengubah harga sebelum diajukan ulang atau di-ACC.</p>`;
}

const SEED_CREW=[
  {id:'K1',nama:'Dewi Lestari',peran:'Sales',hp:'0812-1111-2201',tarif:0,status:'Aktif'},
  {id:'K2',nama:'Fajar Nugroho',peran:'Sales',hp:'0812-1111-2202',tarif:0,status:'Aktif'},
  {id:'K3',nama:'Rian Saputra',peran:'Sales',hp:'0812-1111-2203',tarif:0,status:'Aktif'},
  {id:'K4',nama:'Bayu Pratama',peran:'Tour Leader',hp:'0813-2222-3301',tarif:175000,status:'Aktif'},
  {id:'K5',nama:'Sinta Maharani',peran:'Tour Leader',hp:'0813-2222-3302',tarif:175000,status:'Aktif'},
  {id:'K7',nama:'Yoga Prasetya',peran:'Tour Leader',hp:'0813-2222-3304',tarif:150000,status:'Aktif'},
  {id:'K6',nama:'Arga Wibowo',peran:'Media',hp:'0813-2222-3303',tarif:150000,status:'Aktif'},
  {id:'K8',nama:'Nadia Putri',peran:'Media',hp:'0813-2222-3305',tarif:130000,status:'Aktif'},
];
let crewTab='daftar';
function crewList(){const s=store('crew_list',null);return Array.isArray(s)?s:SEED_CREW.concat(store('crew_add',[]));}
function saveCrewList(arr){save('crew_list',arr);}
function crewById(id){return crewList().find(c=>c.id===id);}
function tripDays(t){if(t.malam!=null&&t._new)return (t.malam||0)+1;if(t.brk&&t.pul){const dd=Math.round((new Date(t.pul)-new Date(t.brk))/86400000)+1;return dd>0?dd:1;}return 1;}
function assignMap(){return store('assign',{});}
function normAssignEntry(v){
  if(!v)return {tls:[],medias:[]};
  const toArr=(arr,legacy)=>{
    if(Array.isArray(arr))return arr.filter(x=>x&&x.id&&crewById(x.id)).map(x=>({id:x.id,tarif:x.tarif!=null?+x.tarif:(crewById(x.id)?.tarif||0)}));
    if(legacy&&crewById(legacy))return [{id:legacy,tarif:crewById(legacy).tarif||0}];
    return [];
  };
  return {tls:toArr(v.tls,v.tl),medias:toArr(v.medias,v.media)};
}
function tripAssign(tripId){return normAssignEntry(assignMap()[tripId]);}
function saveTripAssign(tripId,a){const s=assignMap();s[tripId]={tls:a.tls,medias:a.medias};save('assign',s);}
function addTripCrew(tripId,role,crewId){
  if(!crewId)return;
  const c=crewById(crewId);if(!c)return;
  const key=role==='tl'?'tls':'medias';
  const a=tripAssign(tripId);
  if(a[key].some(x=>x.id===crewId)){toast(c.nama+' sudah ditugaskan di trip ini');return;}
  const b=crewBentrok(crewId,tripId);
  if(b.length)toast('⚠ Jadwal '+c.nama+' bentrok dengan '+b[0].inst);
  a[key].push({id:crewId,tarif:c.tarif||0});
  saveTripAssign(tripId,a);
  if(document.getElementById('crewBody'))renderCrew();
  refreshActiveView();
}
function removeTripCrew(tripId,role,crewId){
  const key=role==='tl'?'tls':'medias';
  const a=tripAssign(tripId);
  a[key]=a[key].filter(x=>x.id!==crewId);
  saveTripAssign(tripId,a);
  if(document.getElementById('crewBody'))renderCrew();
  refreshActiveView();
}
function setTripCrewTarif(tripId,role,crewId,tarif){
  const key=role==='tl'?'tls':'medias';
  const a=tripAssign(tripId);
  const item=a[key].find(x=>x.id===crewId);
  if(item){item.tarif=Math.max(0,parseInt(tarif)||0);saveTripAssign(tripId,a);}
  if(document.getElementById('crewBody'))renderCrew();
  refreshActiveView();
}
function assignCrew(tripId,role,crewId){
  if(!crewId){const a=tripAssign(tripId);a[role==='tl'?'tls':'medias']=[];saveTripAssign(tripId,a);if(document.getElementById('crewBody'))renderCrew();refreshActiveView();return;}
  addTripCrew(tripId,role,crewId);
}
function tripCrewNames(tripId,role){
  const a=tripAssign(tripId);const arr=role==='tl'?a.tls:a.medias;
  return arr.map(x=>crewById(x.id)).filter(Boolean);
}
// --- ketersediaan crew: cek tanggal trip yang tumpang tindih ---
function tripRange(t){if(!t.brk)return null;const a=new Date(t.brk);const b=t.pul?new Date(t.pul):new Date(a.getTime()+(tripDays(t)-1)*86400000);return[a,b];}
function overlap(r1,r2){return r1&&r2&&r1[0]<=r2[1]&&r2[0]<=r1[1];}
function crewTrips(crewId){return allTrips().filter(t=>{const a=tripAssign(t.id);return a.tls.some(x=>x.id===crewId)||a.medias.some(x=>x.id===crewId);});}
function crewBentrok(crewId,tripId){
  const t=allTrips().find(x=>x.id===tripId);const r=tripRange(t);if(!r)return[];
  return crewTrips(crewId).filter(o=>o.id!==tripId&&overlap(r,tripRange(o)));
}
function crewSibuk(crewId,tripId){return crewBentrok(crewId,tripId).length>0;}
function crewTripTarif(crewId,tripId){
  const a=tripAssign(tripId);
  const x=a.tls.find(i=>i.id===crewId)||a.medias.find(i=>i.id===crewId);
  if(x&&x.tarif!=null)return +x.tarif;
  const c=crewById(crewId);return c?(c.tarif||0):0;
}
function crewGaji(crewId){return crewTrips(crewId).reduce((s,t)=>s+crewTripTarif(crewId,t.id)*tripDays(t),0);}
function crewStat(crewId){const ts=crewTrips(crewId);return{n:ts.length,hari:ts.reduce((s,t)=>s+tripDays(t),0),gaji:crewGaji(crewId),trips:ts};}
function tripGaji(t){const a=tripAssign(t.id);const hari=tripDays(t);return a.tls.concat(a.medias).reduce((s,x)=>s+(+x.tarif||0)*hari,0);}
function totalGajiCrew(){return upcoming().reduce((s,t)=>s+tripGaji(t),0);}
// ===== Reimburse biaya lapangan (Tour Leader & Media) =====
function currentTL(){
  const u=currentUser();
  if(u.role==='tl'){
    if(u.crewId&&crewById(u.crewId))return u.crewId;
    const m=crewList().find(c=>c.nama.toLowerCase()===(u.crewName||u.nama||'').toLowerCase());
    if(m)return m.id;
    const firstTL=crewList().find(c=>c.peran==='Tour Leader'||c.peran==='Media');
    if(firstTL)return firstTL.id;
  }
  return store('currentTL','');
}
function setCurrentTL(id){save('currentTL',id);renderTL();}
function reimburseList(){return store('reimburse',[]);}
function reimburseByCrew(crewId){return reimburseList().filter(r=>r.crewId===crewId).sort((a,b)=>b.createdAt-a.createdAt);}
function reimburseByTrip(tripId){return reimburseList().filter(r=>r.tripId===tripId);}
function reimburseSum(list){return list.reduce((s,r)=>s+(r.nominal||0),0);}
function submitReimburse(){
  const crewId=currentTL();if(!crewId){toast('Pilih nama Anda dulu');return;}
  const g=id=>document.getElementById(id);
  const tripId=g('rb_trip')?g('rb_trip').value:'';
  const item=(g('rb_item')?g('rb_item').value:'').trim();
  const nominal=Math.max(0,+(g('rb_nominal')?g('rb_nominal').value:0)||0);
  const ket=g('rb_ket')?g('rb_ket').value.trim():'';
  if(!tripId){toast('Pilih trip dulu');return;}
  if(!item||!nominal){toast('Isi jenis & nominal biaya');return;}
  const c=crewById(crewId);
  const list=reimburseList();
  list.push({id:'RB-'+Date.now(),tripId,crewId,crewName:c?c.nama:'',item,nominal,ket,tgl:new Date().toISOString().slice(0,10),status:'pending',createdAt:Date.now()});
  save('reimburse',list);
  toast('✓ Reimburse diajukan — menunggu persetujuan Management');
  renderTL();
}
function decideReimburse(id,status){
  const list=reimburseList();const r=list.find(x=>x.id===id);if(!r)return;
  r.status=status;r.decidedAt=Date.now();save('reimburse',list);
  toast(status==='approved'?'✓ Reimburse '+r.crewName+' disetujui':'Reimburse '+r.crewName+' ditolak');
  renderKeu();
}
function delReimburse(id){save('reimburse',reimburseList().filter(x=>x.id!==id));renderTL();}
// ===== Area Tour Leader & Media =====
let tlTab='jadwal';
let tlChecklistTrip='';
function setTLTab(k){tlTab=k;const nav=document.querySelector('#view .tabs');if(nav)nav.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.tt===k));renderTL();}
function setTLChecklistTrip(id){tlChecklistTrip=id;renderTL();}
function renderTL(){
  const b=document.getElementById('tlBody');if(!b)return;
  b.innerHTML=tlPicker()+(tlTab==='checklist'?tlChecklistTab():tlTab==='reimburse'?tlReimburseTab():tlTab==='gaji'?tlGajiTab():tlJadwalTab());
}
function vTL(){
  const tabs=[['jadwal','Jadwal Saya'],['checklist','Checklist'],['reimburse','Reimburse'],['gaji','Gaji Saya']];
  const nav=tabs.map(([k,l])=>`<button class="tab ${tlTab===k?'active':''}" data-tt="${k}" onclick="setTLTab('${k}')">${l}</button>`).join('');
  return `<div class="hello fade"><h1>Tour Leader &amp; Media</h1><p>Jadwal tugas, checklist persiapan, reimburse biaya lapangan &amp; gaji per trip</p></div>
    <div class="tabs fade">${nav}</div><div id="tlBody"></div>`;
}
function tlPicker(){
  const u=currentUser();const crew=crewList().filter(c=>c.peran==='Tour Leader'||c.peran==='Media');const cid=currentTL();
  if(u.role==='tl'){
    const me=crewById(cid);
    return `<div class="cat-bar" style="padding:0 0 14px"><div style="display:flex;align-items:center;gap:10px"><span class="pill lunas">Akun Pribadi</span><b>${esc(me?me.nama:u.nama)}</b> <span style="font-size:12px;color:var(--muted)">(${esc(me?me.peran:'Tour Leader & Media')})</span></div></div>`;
  }
  return `<div class="cat-bar" style="padding:0 0 14px"><div><label class="flbl" style="display:inline;margin-right:8px">Filter Tour Leader / Media</label>
    <select class="finput" style="width:auto;display:inline-block;margin:0;padding:8px 12px" onchange="setCurrentTL(this.value)">
      <option value="">— pilih Tour Leader / Media —</option>${crew.map(c=>`<option value="${c.id}" ${c.id===cid?'selected':''}>${esc(c.nama)} (${c.peran})</option>`).join('')}</select></div>
    <span style="font-size:12px;color:var(--muted)">Mode tinjauan ${esc(roleCfg().lbl)}</span></div>`;
}
function tlJadwalTab(){
  const cid=currentTL();
  if(!cid)return '<div class="empty"><h3>Pilih nama Anda</h3><p>Pilih nama di atas untuk melihat jadwal tugas Anda.</p></div>';
  const stat=crewStat(cid);
  const up=stat.trips.filter(t=>tripStatus(t)!=='selesai').sort((a,b)=>a.brk<b.brk?-1:1);
  const done=stat.trips.filter(t=>tripStatus(t)==='selesai');
  const pend=reimburseByCrew(cid).filter(r=>r.status==='pending');
  const cardHTML=t=>{const st=tripStatus(t);const a=tripAssign(t.id);const peran=a.tls.some(x=>x.id===cid)?'Tour Leader':'Media';
    return `<div class="jcard" onclick="openTLTrip('${t.id}')">
      <div class="jcard-top"><span class="pill ${STPILL[st]}">${STLBL[st]}</span><span class="pill jadwal" style="background:var(--navy);color:#fff">${peran}</span></div>
      <h4>${esc(t.inst)}</h4><div class="jcard-dest">${esc((t.dest||'').split('(')[0])}</div>
      <div class="jcard-meta"><span>📅 ${dateID(t.brk)}${t.pul?'–'+dateID(t.pul):''}</span><span>👥 ${t.pax} pax</span><span>🧰 ${prepTrip(t.id).length} item vendor</span></div>
    </div>`;};
  return `<div class="cards fade" style="grid-template-columns:repeat(4,1fr)">
    <div class="scard"><div class="ic b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg></div><div class="lbl">Trip Mendatang</div><div class="val mono">${up.length}</div></div>
    <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div class="lbl">Total Hari Tugas</div><div class="val mono">${stat.hari}</div></div>
    <div class="scard"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 10h18M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg></div><div class="lbl">Estimasi Gaji</div><div class="val mono">${rp(stat.gaji)}</div></div>
    <div class="scard"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4m0 4h.01M10.3 3.9 1.8 18a1.5 1.5 0 0 0 1.3 2.2h17.8a1.5 1.5 0 0 0 1.3-2.2L13.7 3.9a1.5 1.5 0 0 0-2.6 0z"/></svg></div><div class="lbl">Reimburse Pending</div><div class="val mono">${pend.length}</div></div>
  </div>
  <div class="panel fade" style="margin:0"><div class="panel-h"><h3>Trip Mendatang &amp; Berlangsung</h3></div>
  ${up.length?`<div class="jgrid" style="margin-top:12px">${up.map(cardHTML).join('')}</div>`:`<div style="padding:30px 0;text-align:center;color:var(--muted);font-size:13px">Tidak ada trip aktif.</div>`}
  </div>
  ${done.length?`<div class="panel fade" style="margin:0"><div class="panel-h"><h3>Riwayat Trip Selesai</h3></div><div class="jgrid" style="margin-top:12px">${done.map(cardHTML).join('')}</div></div>`:''}`;
}
function openTLTrip(id){
  const t=allTrips().find(x=>x.id===id);if(!t)return;
  const cid=currentTL();const a=tripAssign(id);const peran=a.tls.some(x=>x.id===cid)?'Tour Leader':'Media';
  const cl=store('checklist',{})[id]||CHECKLIST_DEF.map(x=>({item:x,done:false}));
  const clHTML=cl.map((c,i)=>`<label class="chk"><input type="checkbox" ${c.done?'checked':''} onchange="toggleChecklist('${id}',${i});openTLTrip('${id}')"> ${esc(c.item)}</label>`).join('');
  const prep=prepTrip(id);
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='tlOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:520px"><div class="pv-bar"><b>${esc(t.inst)}</b><button class="btn-acc no" onclick="document.getElementById('tlOv').remove()">Tutup</button></div>
  <div style="background:var(--bg);padding:16px;max-height:76vh;overflow:auto">
    <div class="td-card"><h5>Info Trip</h5>
      <div class="td-row"><span>Peran Anda</span><b>${peran}</b></div>
      <div class="td-row"><span>Destinasi</span><b>${esc((t.dest||'').split('(')[0])}</b></div>
      <div class="td-row"><span>Tanggal</span><b>${dateID(t.brk)}${t.pul?' – '+dateID(t.pul):''}</b></div>
      <div class="td-row"><span>Peserta</span><b>${t.pax} pax</b></div>
      <div class="td-row"><span>Armada</span><b>${esc(t.armada||(t.bus?t.bus+' unit':'—'))}</b></div>
    </div>
    <div class="td-card"><h5>Checklist Persiapan</h5>${clHTML}</div>
    <div class="td-card"><h5>Persiapan Vendor</h5>${prep.length?prep.map(p=>`<div class="td-row"><span>${esc(p.kat)}</span><b>${esc(p.vendor||'-')}</b></div>`).join(''):'<div style="font-size:12.5px;color:var(--muted)">Belum ada data vendor.</div>'}</div>
    <button class="btn-save" onclick="document.getElementById('tlOv').remove();setTLTab('reimburse');setTimeout(()=>{const s=document.getElementById('rb_trip');if(s)s.value='${id}';},50)">💸 Ajukan Reimburse untuk Trip Ini</button>
  </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function tlChecklistTab(){
  const cid=currentTL();if(!cid)return '<div class="empty"><h3>Pilih nama Anda</h3></div>';
  const trips=crewTrips(cid).filter(t=>tripStatus(t)!=='selesai').sort((a,b)=>a.brk<b.brk?-1:1);
  if(!trips.length)return '<div class="empty"><h3>Tidak ada trip aktif</h3><p>Checklist muncul untuk trip yang sedang berjalan atau akan datang.</p></div>';
  const sel=tlChecklistTrip&&trips.find(t=>t.id===tlChecklistTrip)?tlChecklistTrip:trips[0].id;
  const cl=store('checklist',{})[sel]||CHECKLIST_DEF.map(x=>({item:x,done:false}));
  const done=cl.filter(c=>c.done).length;
  const clHTML=cl.map((c,i)=>`<label class="chk"><input type="checkbox" ${c.done?'checked':''} onchange="toggleChecklist('${sel}',${i});renderTL()"> ${esc(c.item)}</label>`).join('');
  return `<div class="panel fade" style="margin:0"><div class="panel-h"><h3>Checklist Persiapan</h3></div>
    <div style="padding:16px 19px 0"><label class="flbl">Pilih Trip</label>
    <select class="finput" onchange="setTLChecklistTrip(this.value)">${trips.map(x=>`<option value="${x.id}" ${x.id===sel?'selected':''}>${esc(x.inst)} — ${dateID(x.brk)}</option>`).join('')}</select></div>
    <div style="padding:16px 19px"><div style="font-size:12.5px;color:var(--muted);margin-bottom:10px">${done}/${cl.length} selesai</div>${clHTML}</div>
  </div>`;
}
function tlReimburseTab(){
  const cid=currentTL();if(!cid)return '<div class="empty"><h3>Pilih nama Anda</h3></div>';
  const trips=crewTrips(cid).sort((a,b)=>a.brk<b.brk?-1:1);
  const mine=reimburseByCrew(cid);
  const row=r=>{const t=allTrips().find(x=>x.id===r.tripId);const pillc=r.status==='approved'?'lunas':r.status==='rejected'?'piutang':'dp';const plabel=r.status==='approved'?'Disetujui':r.status==='rejected'?'Ditolak':'Menunggu';
    return `<tr><td><div class="nm" style="font-weight:700">${t?esc(t.inst):'(trip dihapus)'}</div><div class="loc" style="font-size:11px;color:var(--muted)">${dateID(r.tgl)}</div></td><td>${esc(r.item)}<div style="font-size:11px;color:var(--muted)">${esc(r.ket||'')}</div></td><td class="price mono">${rp(r.nominal)}</td><td><span class="pill ${pillc}">${plabel}</span></td><td style="text-align:right">${r.status==='pending'?`<button class="btn-acc no" onclick="delReimburse('${r.id}')">Batal</button>`:'—'}</td></tr>`;};
  return `<div class="panel fade" style="margin:0"><div class="panel-h"><h3>Ajukan Reimburse Biaya Lapangan</h3></div>
    <div style="padding:16px 19px">
      <label class="flbl">Trip</label><select id="rb_trip" class="finput" style="margin-bottom:10px"><option value="">— pilih trip —</option>${trips.map(t=>`<option value="${t.id}">${esc(t.inst)} — ${dateID(t.brk)}</option>`).join('')}</select>
      <div class="frow"><div><label class="flbl">Jenis Biaya</label><input id="rb_item" class="finput" placeholder="mis. Parkir, Tol, Makan darurat"></div><div><label class="flbl">Nominal (Rp)</label><input id="rb_nominal" class="finput" type="number" placeholder="0"></div></div>
      <label class="flbl">Keterangan (opsional)</label><input id="rb_ket" class="finput" style="margin-bottom:10px" placeholder="catatan tambahan">
      <button class="btn-save" onclick="submitReimburse()">Ajukan Reimburse</button>
    </div>
  </div>
  <div class="panel fade" style="margin:0"><div class="panel-h"><h3>Riwayat Pengajuan Saya</h3></div>
  ${mine.length?`<div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Trip</th><th>Keterangan</th><th>Nominal</th><th>Status</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${mine.map(row).join('')}</tbody></table></div>`:`<div style="padding:30px 0;text-align:center;color:var(--muted);font-size:13px">Belum ada pengajuan.</div>`}
  </div>`;
}
function tlGajiTab(){
  const cid=currentTL();if(!cid)return '<div class="empty"><h3>Pilih nama Anda</h3></div>';
  const c=crewById(cid);const stat=crewStat(cid);
  const rows=stat.trips.slice().sort((a,b)=>a.brk<b.brk?1:-1).map(t=>{const hari=tripDays(t);const gaji=(c.tarif||0)*hari;const st=tripStatus(t);
    return `<tr><td><div class="nm" style="font-weight:700">${esc(t.inst)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${dateID(t.brk)}${t.pul?'–'+dateID(t.pul):''}</div></td><td>${hari} hari</td><td><span class="pill ${STPILL[st]}">${STLBL[st]}</span></td><td class="price mono">${rp(gaji)}</td></tr>`;}).join('');
  return `<div class="cards fade" style="grid-template-columns:repeat(3,1fr)">
    <div class="scard"><div class="ic b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 10h18M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg></div><div class="lbl">Tarif / Hari</div><div class="val mono">${rp(c?c.tarif:0)}</div></div>
    <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div class="lbl">Total Hari Tugas</div><div class="val mono">${stat.hari}</div></div>
    <div class="scard"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 12 5 5L20 7"/></svg></div><div class="lbl">Total Estimasi Gaji</div><div class="val mono">${rp(stat.gaji)}</div></div>
  </div>
  <div class="panel fade" style="margin:0"><div class="panel-h"><h3>Rincian Gaji per Trip</h3></div>
  ${rows?`<div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Trip</th><th>Durasi</th><th>Status</th><th>Gaji</th></tr></thead><tbody>${rows}</tbody></table></div>`:`<div style="padding:30px 0;text-align:center;color:var(--muted);font-size:13px">Belum ada trip ditugaskan.</div>`}
  </div>
  <p style="font-size:12px;color:var(--muted-2);margin-top:14px">Estimasi dihitung dari tarif harian × jumlah hari trip. Belum termasuk reimburse biaya lapangan yang disetujui.</p>`;
}
// ===== Area Umum / Halaman Publik =====
let umumTab='paket';
let lastUmumEst=null;
let umumDestQ='';
function setUmumTab(k){umumTab=k;umumDestQ='';const nav=document.querySelector('#view .tabs');if(nav)nav.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.ut===k));renderUmum();}
function setUmumDestQ(v){umumDestQ=v;renderUmum();}
function renderUmum(){
  const b=document.getElementById('umumBody');if(!b)return;
  b.innerHTML=umumTab==='hotel'?umumHotelTab():umumTab==='armada'?umumArmadaTab():umumTab==='estimasi'?umumEstimasiTab():umumPaketTab();
  if(umumTab==='estimasi')calcUmum();
  if(umumTab==='paket'){const q=document.getElementById('umDestSearch');if(q){q.value=umumDestQ;if(umumDestQ)q.focus();}}
}
const DESTPHOTO={}; // isi {'Nama Destinasi':'data:image/...;base64,...'} di sini begitu foto asli Havist sudah ada — otomatis dipakai menggantikan gradasi warna.
const UMGRAD=['linear-gradient(135deg,#275BB5,#1AA6B7)','linear-gradient(135deg,#163A6B,#8E63D6)','linear-gradient(135deg,#0E244A,#275BB5)','linear-gradient(135deg,#1AA6B7,#2B9D6E)','linear-gradient(135deg,#8E63D6,#275BB5)','linear-gradient(135deg,#2B9D6E,#1AA6B7)','linear-gradient(135deg,#275BB5,#163A6B)','linear-gradient(135deg,#1AA6B7,#275BB5)'];
const UMUM_BEST_PKGS=[
  {
    id:'pkg_bdg',
    title:'Paket Edukasi & Budaya Bandung',
    city:'BANDUNG',
    durLbl:'One Day Trip (1 Hari)',
    pax:50, malam:0, share:4,
    armada:'BIG BUS (50 Seat)',
    hotel:'',
    mFreq:2,
    kaos:'Kaos Cotton Combed 30s Pendek',
    dests:['Museum Geologi','Saung Udjo','Masjid Al Jabbar'],
    grad:'linear-gradient(135deg,#1E4E9C,#1AA6B7)'
  },
  {
    id:'pkg_jog',
    title:'Paket Study Tour Yogyakarta',
    city:'JOGJA',
    durLbl:'3 Hari 2 Malam',
    pax:50, malam:2, share:4,
    armada:'BIG BUS (50 Seat)',
    hotel:'The Cube',
    mFreq:6,
    kaos:'Kaos Cotton Combed 30s Pendek',
    dests:['Kraton Yogyakarta','Museum Vredeburg','Hutan Pinus Pengger','Goa Pindul','Malioboro'],
    grad:'linear-gradient(135deg,#163A6B,#8E63D6)'
  },
  {
    id:'pkg_dng',
    title:'Paket Eksotika Dieng Plateau',
    city:'DIENG',
    durLbl:'2 Hari 1 Malam',
    pax:33, malam:1, share:4,
    armada:'MEDIUM BUS (31-35 Seat)',
    hotel:'QUEEN VILLA SIKUNIR',
    mFreq:4,
    kaos:'Kaos Cotton Combed 30s Pendek',
    dests:['Sunrise Sikunir','Kawah Sikidang','Candi Arjuna','Bukit Ratapan Angin'],
    grad:'linear-gradient(135deg,#1AA6B7,#2B9D6E)'
  },
  {
    id:'pkg_mlg',
    title:'Paket Petualangan Malang & Bromo',
    city:'MALANG & BROMO',
    durLbl:'3 Hari 2 Malam',
    pax:50, malam:2, share:4,
    armada:'BIG BUS (50 Seat)',
    hotel:'LAVA VIEW LODGE HOTEL',
    mFreq:6,
    kaos:'Kaos Cotton Combed 30s Pendek',
    dests:['Bromo Sunrise','Petik Apel'],
    grad:'linear-gradient(135deg,#0E244A,#275BB5)'
  }
];
function calcBestPkg(pk){
  const pax=pk.pax||50, malam=pk.malam||0, hari=malam+1, share=pk.share||4;
  const arm=CAT.armada.find(a=>a.name===pk.armada)||CAT.armada[3]||CAT.armada[0]||{name:'Big Bus',rate:6000000};
  const cap=armSeat(arm);
  const bus=Math.max(1,Math.ceil(pax/cap));
  const hot=pk.hotel?CAT.hotels.find(h=>h.name===pk.hotel):null;
  const hotelRate=hot?(hot.wd||0):0;
  const kamar=(malam>0&&hotelRate>0)?Math.ceil(pax/share):0;
  const kaosObj=pk.kaos?CAT.kaos.find(k=>k.name===pk.kaos):null;
  const kaosRate=kaosObj?(kaosObj.price||0):0;
  const destObjs=(pk.dests||[]).map(nm=>CAT.dests.find(d=>d.name===nm&&d.city===pk.city)||CAT.dests.find(d=>d.name===nm)).filter(Boolean);
  const destPrice=destObjs.reduce((s,d)=>s+(d.price||0),0);
  const cT=(arm.rate||0)*bus*hari;
  const cH=malam>0?hotelRate*kamar*malam:0;
  const cM=(pk.mFreq||0)*35000*pax;
  const cK=kaosRate*pax;
  const cW=destPrice*pax;
  const modal=cT+cH+cM+cK+cW;
  const markup=1+(store('markup',20)/100);
  const mk=modal*markup;
  const foc=Math.min(Math.floor(pax/10),25);
  const subsidi=foc*(pax>0?mk/pax:0);
  const jualGrup=Math.max(0,mk-subsidi);
  const perpax=pax>0?Math.ceil((jualGrup/pax)/1000)*1000:0;
  return {pax,malam,hari,bus,armName:arm.name,hotName:hot?hot.name:'Tanpa Menginap',kamar,mFreq:pk.mFreq||0,kaosName:kaosObj?kaosObj.name:'',destNames:destObjs.map(d=>d.name),foc,perpax,totalPaket:perpax*pax};
}
function applyBestPkg(idx){
  const pk=UMUM_BEST_PKGS[idx];if(!pk)return;
  setUmumTab('estimasi');
  setTimeout(()=>{
    const g=id=>document.getElementById(id);
    if(g('u_pax'))g('u_pax').value=pk.pax;
    if(g('u_malam'))g('u_malam').value=pk.malam;
    if(g('u_share'))g('u_share').value=pk.share||4;
    if(g('u_mfreq'))g('u_mfreq').value=pk.mFreq||0;
    if(g('u_armada')){
      const o=[...g('u_armada').options].find(x=>x.dataset.name===pk.armada);
      if(o)g('u_armada').value=o.value;
    }
    if(g('u_hotel')){
      if(!pk.hotel)g('u_hotel').value='0|0';
      else{const o=[...g('u_hotel').options].find(x=>x.dataset.name===pk.hotel);if(o)g('u_hotel').value=o.value;}
    }
    if(g('u_kaos')){
      const o=[...g('u_kaos').options].find(x=>x.dataset.name===pk.kaos);
      if(o)g('u_kaos').value=o.value;
    }
    document.querySelectorAll('.udest').forEach(cb=>{
      cb.checked=(pk.dests||[]).includes(cb.dataset.name);
      const box=cb.closest('.citybox');
      if(cb.checked&&box)box.classList.add('open');
    });
    calcUmum();
    const resEl=document.getElementById('umTabsSec');
    if(resEl)resEl.scrollIntoView({behavior:'smooth',block:'start'});
    toast('Paket '+pk.city+' dimuat ke kalkulator ✓');
  },40);
}

function umumFeatured(){
  const cities=[...new Set(CAT.dests.map(d=>d.city))];
  return cities.map(c=>CAT.dests.find(d=>d.city===c)).filter(Boolean).slice(0,8);
}
function umumStats(){
  const nCity=[...new Set(CAT.dests.map(d=>d.city))].length;
  return [[CAT.dests.length+'+','Destinasi Wisata'],[nCity,'Kota/Wilayah Tujuan'],[allTrips().length+'+','Trip Terlaksana'],[(CAT.hotels.length+CAT.armada.length)+'+','Mitra Hotel &amp; Armada']];
}
function umumHeroSearch(e){
  e.preventDefault();
  const v=(document.getElementById('umHeroSearch').value||'').trim();
  umumTab='paket';umumDestQ=v;
  const nav=document.querySelector('#view .tabs');if(nav)nav.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.ut==='paket'));
  renderUmum();
  const b=document.getElementById('umumBody');if(b)b.scrollIntoView({behavior:'smooth'});
}
// Band kepercayaan — dihitung dari jumlah nama klien/rombongan berbeda di data trip asli (bukan logo/nama karangan).
function umumTrustBand(){
  const n=new Set(allTrips().map(t=>t.inst).filter(Boolean)).size;
  return `<div class="umtrust fade"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 21h18M5 21V7l7-4 7 4v14"/><path d="M9 9h1M9 13h1M9 17h1M14 9h1M14 13h1M14 17h1"/></svg>
    <p>Dipercaya oleh <b>${n}+</b> sekolah, instansi &amp; rombongan berbeda untuk perjalanan mereka</p></div>`;
}
// FAQ halaman publik — isi pertanyaan yang sering ditanyakan lewat WhatsApp, supaya calon klien bisa cari tahu sendiri dulu.
const UMUM_FAQ=[
  ['Bagaimana cara memesan paket wisata?','Hubungi tim Sales kami via WhatsApp dengan info jumlah peserta, tujuan, dan perkiraan tanggal keberangkatan. Tim kami akan membuatkan penawaran harga sesuai kebutuhan rombongan Anda.'],
  ['Berapa minimal jumlah peserta?','Paket rombongan umumnya menyesuaikan kapasitas armada (mis. 1 bus), namun kami juga membantu menghitungkan kebutuhan yang lebih kecil — silakan tanyakan langsung ke tim Sales.'],
  ['Bagaimana sistem pembayarannya?','DP 30% saat konfirmasi booking, dan pelunasan maksimal 7 hari sebelum tanggal keberangkatan.'],
  ['Bisakah request destinasi, hotel, atau armada tertentu?','Bisa. Kami terbuka untuk request destinasi, hotel, dan armada sesuai kebutuhan — tim Sales akan menghitungkan estimasi biayanya lewat Kalkulator di halaman ini.'],
  ['Apakah ada tour leader & dokumentasi selama perjalanan?','Ya, setiap trip didampingi tour leader berpengalaman, dan untuk sebagian trip disertai tim media untuk dokumentasi perjalanan.'],
];

function umumStepsSection(){
  const steps=[
    ['01','Pilih Paket & Hitung Estimasi','Pilih salah satu paket terbaik atau atur sendiri jumlah peserta, bus, hotel, dan objek wisata di kalkulator halaman ini.'],
    ['02','Unduh Proposal & Konsultasi','Unduh draf Estimasi Proposal PDF untuk bahan rapat panitia/sekolah, lalu konsultasikan detail jadwal dengan tim Sales kami.'],
    ['03','Konfirmasi Booking & DP 30%','Setelah tanggal & fasilitas disepakati, amankan kursi armada dan kamar hotel dengan pembayaran DP 30% ke rekening resmi.'],
    ['04','Pelunasan H-7 & Berangkat!','Pelunasan dilakukan H-7 keberangkatan. Tim Tour Leader & Media kami siap mendampingi perjalanan rombongan Anda dari awal hingga pulang.']
  ];
  return `<div class="umsec-head" style="margin-top:6px"><div><span class="tag">Alur Pemesanan Mudah</span><h2>4 Langkah Merencanakan Trip Rombongan</h2></div></div>
  <div class="umsteps fade">${steps.map(([no,t,d])=>`<div class="umstep-card"><div class="umstep-no">${no}</div><h4>${t}</h4><p>${d}</p></div>`).join('')}</div>`;
}
function umumFooterSection(){
  const info=infoPerusahaan();
  return `<footer id="umFootSec" class="umfoot fade">
    <div class="umfoot-grid">
      <div>
        <div class="umfoot-brand"><img src="__LOGO__" alt="${esc(info.nama)}"><span>${esc(info.nama)}</span></div>
        <p class="umfoot-desc">Mitra perjalanan wisata, study tour sekolah, outing class, dan gathering instansi dengan layanan All-In: Armada Pariwisata, Hotel, Konsumsi, Tour Leader &amp; Dokumentasi Media.</p>
        <div class="umfoot-badges">
          <span>✓ Harga Transparan All-In</span>
          <span>✓ Free Kuota Guru/Pendamping (FOC)</span>
          <span>✓ Tim TL &amp; Media Berpengalaman</span>
        </div>
      </div>
      <div>
        <h5>Navigasi Cepat</h5>
        <ul class="umfoot-links">
          <li><a onclick="window.scrollTo({top:0,behavior:'smooth'})">Beranda &amp; Paket Unggulan</a></li>
          <li><a onclick="umumGo('paket','umTabsSec')">Katalog Destinasi Wisata</a></li>
          <li><a onclick="umumGo('hotel','umTabsSec')">Daftar Mitra Hotel</a></li>
          <li><a onclick="umumGo('armada','umTabsSec')">Pilihan Armada Bus</a></li>
          <li><a onclick="umumGo('estimasi','umTabsSec')">Kalkulator Estimasi Biaya</a></li>
          <li><a onclick="umumGo(null,'umFaqSec')">Pertanyaan Umum (FAQ)</a></li>
        </ul>
      </div>
      <div>
        <h5>Kantor &amp; Kontak Resmi</h5>
        <div class="umfoot-contact">
          <div>📍 <b>Alamat:</b> ${esc(info.alamat)}</div>
          <div>📞 <b>WhatsApp / Telp:</b> ${esc(info.hp)}</div>
          <div>✉️ <b>Email:</b> ${esc(info.email)}</div>
          ${info.rek?`<div>🏦 <b>Rekening Resmi:</b> ${esc(info.rek)}</div>`:'<div>🏦 <b>Pembayaran:</b> DP 30% saat konfirmasi · Pelunasan H-7</div>'}
        </div>
        <a class="btn-um-primary" style="margin-top:14px;text-decoration:none;display:inline-flex" target="_blank" href="${waLink(info.hp,'Halo '+info.nama+', saya ingin konsultasi rencana perjalanan rombongan kami.')}">💬 Hubungi Tim Kami via WhatsApp</a>
      </div>
    </div>
    <div class="umfoot-copy">© ${new Date().getFullYear()} ${esc(info.nama)} · Your Travel Dream Makers. Hak cipta dilindungi.</div>
  </footer>`;
}
function setUmumPreset(pax,armName){
  const g=id=>document.getElementById(id);
  if(g('u_pax'))g('u_pax').value=pax;
  if(g('u_armada')&&armName){
    const o=[...g('u_armada').options].find(x=>x.dataset.name===armName);
    if(o)g('u_armada').value=o.value;
  }
  document.querySelectorAll('.um-preset-btn').forEach(b=>b.classList.toggle('active',+b.dataset.pax===pax));
  calcUmum();
}
function openUmumProposalModal(){
  if(!lastUmumEst||!lastUmumEst.pax){calcUmum();}
  const e=lastUmumEst;if(!e)return;
  const old=document.getElementById('umPropOv');if(old)old.remove();
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='umPropOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:450px">
    <div class="pv-bar"><b>📄 Unduh Estimasi Proposal (PDF)</b><button class="btn-acc no" onclick="document.getElementById('umPropOv').remove()">Tutup</button></div>
    <div style="background:#fff;margin:16px;border-radius:12px;padding:18px">
      <p style="font-size:12.5px;color:var(--muted);margin-bottom:12px;line-height:1.5">Isi nama sekolah/instansi Anda agar tertera resmi di lembar <b>Surat Estimasi Proposal</b> yang siap dibawa ke rapat panitia:</p>
      <label class="flbl">Nama Sekolah / Instansi / Rombongan *</label>
      <input id="up_inst" class="finput" placeholder="mis. SMPN 1 Curug / PT Maju Jaya">
      <label class="flbl">Nama Bapak / Ibu Panitia (PIC)</label>
      <input id="up_pic" class="finput" placeholder="mis. Bpk. Hendra (Ketua Panitia)">
      <label class="flbl">No. WhatsApp Aktif *</label>
      <input id="up_hp" class="finput" placeholder="mis. 0812-3456-7890" onkeydown="if(event.key==='Enter')submitUmumProposal()">
      <div style="background:var(--bg);border-radius:10px;padding:10px 12px;font-size:12px;color:var(--ink);margin-bottom:12px">
        <b>Ringkasan Paket:</b> ${e.pax} Pax · ${e.hari}H${e.malam}M · ${e.bus} unit ${esc(e.armName)} · <b>${rp(e.perpax)}/pax</b>
      </div>
      <button class="btn-save" onclick="submitUmumProposal()">⬇ Lihat &amp; Unduh Proposal PDF</button>
    </div>
  </div>`;
  document.body.appendChild(ov);ov.addEventListener('click',ev=>{if(ev.target===ov)ov.remove();});
}
function submitUmumProposal(){
  const g=id=>document.getElementById(id);
  const inst=(g('up_inst')?g('up_inst').value:'').trim();
  const pic=(g('up_pic')?g('up_pic').value:'').trim();
  const hp=(g('up_hp')?g('up_hp').value:'').trim();
  if(!inst||!hp){toast('Mohon isi Nama Sekolah/Instansi dan No. WhatsApp');return;}
  const ov=document.getElementById('umPropOv');if(ov)ov.remove();
  const e=lastUmumEst;
  const klienLabel=pic?`${inst} (PIC: ${pic})`:inst;
  // Save automatically into Data Klien for Sales follow-up
  const list=klienList();
  const catNote=`Estimasi Web: ${e.pax} pax (${e.hari}H${e.malam}M), ${e.bus}x ${e.armName}, ${e.destNames.length?e.destNames.join(', '):'Custom'} — ${rp(e.perpax)}/pax`;
  const ex=list.find(k=>k.nama.toLowerCase()===inst.toLowerCase());
  if(ex){ex.hp=hp;if(pic)ex.instansi=pic;ex.catatan=catNote;}
  else list.push({id:'KL'+Date.now().toString(36),nama:inst,instansi:pic||'Prospek Web Publik',hp,catatan:catNote,sales:'Web Publik (Proposal)',created:Date.now()});
  save('klien',list);
  // Build official proposal preview & trigger PDF download
  const info=infoPerusahaan();
  const dNow=new Date();
  const rom=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII'][dNow.getMonth()];
  const no=`EST-${String(dNow.getDate()).padStart(2,'0')}${String(dNow.getMonth()+1).padStart(2,'0')}/HVST-WEB/${rom}/${dNow.getFullYear()}`;
  const tglSurat=dNow.toLocaleDateString('id-ID',{day:'2-digit',month:'long',year:'numeric'});
  const tglInput=document.getElementById('u_tgl')?document.getElementById('u_tgl').value:'';
  const tglTrip=tglInput?new Date(tglInput).toLocaleDateString('id-ID',{weekday:'long',day:'2-digit',month:'long',year:'numeric'}):'Menyesuaikan jadwal sekolah/instansi';
  const destObjs=(e.destNames||[]).map(nm=>CAT.dests.find(d=>d.name===nm)).filter(Boolean);
  const cities=[...new Set(destObjs.map(d=>d.city))];
  const destLabel=cities.length?cities.join(' · ')+(e.destNames.length?' ('+e.destNames.join(', ')+')':''):(e.destNames.length?e.destNames.join(', '):'Paket Wisata Rombongan');
  const fasil=[
    `Transportasi ${e.armName} (${e.bus} unit, AC, Audio/Karaoke, Reclining Seat) selama ${e.hari} hari`,
    e.kamar>0?`Akomodasi Hotel ${e.hotName} (${e.kamar} kamar × ${e.malam} malam)`:'Perjalanan One Day Trip (Tanpa Menginap)',
    e.mFreq>0?`Konsumsi ${e.mFreq}× makan selama perjalanan (${e.pax} pax)`:'Konsumsi menyesuaikan kebutuhan rombongan',
  ];
  if(e.kaosName&&!e.kaosName.includes('Tanpa'))fasil.push(`Merchandise ${e.kaosName} (${e.pax} pcs)`);
  if(e.destNames.length)fasil.push(`Tiket masuk objek wisata: ${e.destNames.join(', ')}`);
  fasil.push(`Gratis kuota pendamping/guru (FOC) ${e.foc} orang + Pendampingan Tour Leader & Dokumentasi`);
  const itin=buildItinerary(destObjs.map(d=>({name:d.name,city:d.city,note:d.note||''})),e.hari,e.malam,e.mFreq,e.hotName);
  pvActive={
    no,tglSurat,klien:klienLabel,hp,dest:destLabel,tglTrip,info,fasil,itin,
    q:{pax:e.pax,hari:e.hari,malam:e.malam,bus:e.bus,armName:e.armName,hotelName:e.hotName,perpax:e.perpax,total:e.totalPaket}
  };
  const fasilHTML=fasil.map(f=>`<li>${esc(f)}</li>`).join('');
  const itinHTML=itin.map(d=>`<div class="pv-day"><div class="pv-day-h">Hari ${d.hari}</div><ul>${d.acts.map(a=>`<li>${esc(a)}</li>`).join('')}</ul></div>`).join('');
  const pov=document.createElement('div');pov.className='pv-overlay';pov.id='pvOverlay';
  pov.innerHTML=`<div class="pv-modal">
    <div class="pv-bar"><b>Estimasi Proposal — ${esc(inst)}</b><div><button class="btn-acc ok" onclick="genPenawaranPDF()">⬇ Unduh PDF</button><button class="btn-acc no" onclick="document.getElementById('pvOverlay').remove()">Tutup</button></div></div>
    <div class="pv-paper" id="pvPaper">
      <div class="pv-letterhead"><div class="pv-brand">HAVIST TRAVELLER</div><div class="pv-tag">Your Travel Dream Makers</div><div class="pv-contact">${esc(info.alamat)}<br>${esc(info.hp)} · ${esc(info.email)}</div></div>
      <h2 class="pv-title">SURAT ESTIMASI PENAWARAN PAKET WISATA</h2>
      <table class="pv-meta"><tr><td>Nomor</td><td>: ${esc(no)}</td><td>Tanggal</td><td>: ${esc(tglSurat)}</td></tr></table>
      <p class="pv-to">Kepada Yth.<br><b>${esc(klienLabel)}</b><br>${esc(hp)}</p>
      <p>Dengan hormat, berikut kami sampaikan estimasi penawaran paket perjalanan wisata rombongan:</p>
      <table class="pv-sum">
        <tr><td>Tujuan Wisata</td><td>: <b>${esc(destLabel)}</b></td></tr>
        <tr><td>Rencana Berangkat</td><td>: ${esc(tglTrip)}</td></tr>
        <tr><td>Durasi Perjalanan</td><td>: ${e.hari} Hari ${e.malam} Malam</td></tr>
        <tr><td>Jumlah Peserta</td><td>: ${e.pax} pax (+ Free ${e.foc} FOC Pendamping)</td></tr>
        <tr><td>Armada Bus</td><td>: ${esc(e.armName)} (${e.bus} unit)</td></tr>
        <tr><td>Akomodasi Hotel</td><td>: ${esc(e.kamar>0?e.hotName:'One Day Trip (Tanpa Menginap)')}</td></tr>
      </table>
      <div class="pv-price"><span>Estimasi Harga Paket per Pax (All-In)</span><b>${rp(e.perpax)}</b></div>
      <div class="pv-price sub"><span>Estimasi Total Rombongan (${e.pax} pax)</span><b>${rp(e.totalPaket)}</b></div>
      <h3 class="pv-h3">Fasilitas Paket Termasuk</h3><ul class="pv-fasil">${fasilHTML}</ul>
      <h3 class="pv-h3">Rencana Itinerary Perjalanan</h3><div class="pv-itin">${itinHTML}</div>
      <h3 class="pv-h3">Syarat &amp; Ketentuan Pemesanan</h3><ul class="pv-fasil"><li>DP 30% saat konfirmasi pemesanan untuk penguncian jadwal armada &amp; hotel.</li><li>Pelunasan maksimal 7 hari (H-7) sebelum tanggal keberangkatan.</li><li>Estimasi ini bersifat fleksibel dan dapat disesuaikan kembali bersama tim Sales Havist Traveller.</li></ul>
      <p class="pv-close">Demikian surat estimasi penawaran ini kami sampaikan untuk dapat dijadikan bahan pertimbangan rapat panitia. Atas perhatian dan kerja samanya kami ucapkan terima kasih.</p>
      <div class="pv-sign">Hormat kami,<br><br><b>Manajemen Havist Traveller</b></div>
    </div>
  </div>`;
  document.body.appendChild(pov);
  pov.addEventListener('click',ev=>{if(ev.target===pov)pov.remove();});
  setTimeout(()=>genPenawaranPDF(),150);
}

function umumFaqSection(){
  const items=UMUM_FAQ.map(([q,a])=>`<div class="umfaq-item"><button class="umfaq-q" onclick="this.parentNode.classList.toggle('open')"><span>${esc(q)}</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M6 9l6 6 6-6"/></svg></button><div class="umfaq-a"><p>${esc(a)}</p></div></div>`).join('');
  return `<div class="umsec-head"><div><span class="tag">Pertanyaan Umum</span><h2>Yang Sering Ditanyakan</h2></div></div>
  <div id="umFaqSec" class="umfaq fade">${items}</div>`;
}
// Testimoni asli dari pelanggan — isi array ini begitu ada komentar/review asli dari Instagram, YouTube, atau DM/WhatsApp.
// Format tiap item: {quote, name, sumber, tur, platform (emoji), foto (url/base64, opsional)}. Kosong = tampil placeholder "menunggu testimoni".
const TESTIMONI=[];
function umumPhotos(){return store('umumPhotos',{hero:'',dest:{},testi:[]});}
function umumTestiSection(){
  const uph=umumPhotos();
  const customTesti=Array.isArray(uph.testi)?uph.testi:[];
  const allTesti=TESTIMONI.concat(customTesti);
  const has=allTesti.length>0;
  const nTrip=allTrips().length,nDest=CAT.dests.length,nPartner=CAT.hotels.length+CAT.armada.length;
  const nPax=allTrips().reduce((s,t)=>s+(t.pax||0),0);
  const statCard=`<div class="umt-card-stat">
    <div class="umt-rating-row"><div class="umt-rating-n">${nPax.toLocaleString('id-ID')}+</div><div class="umt-rating-txt">Peserta sudah<br>kami layani</div></div>
    <div class="umt-feat">
      <div class="umt-feat-row"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s7-7.5 7-12a7 7 0 1 0-14 0c0 4.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg> ${nDest}+ destinasi wisata tersedia</div>
      <div class="umt-feat-row"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6l7-3z"/></svg> ${nPartner}+ mitra hotel &amp; armada terpilih</div>
      <div class="umt-feat-row"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg> ${nTrip}+ trip sudah terlaksana</div>
    </div>
    <div class="umt-cta-block">
      <div class="lbl1">Siap merencanakan perjalanan sendiri?</div>
      <div class="lbl2">Yuk, mulai sekarang!</div>
      <div class="umt-cta-row">
        <button class="umt-cta-btn" onclick="setUmumTab('estimasi');document.getElementById('umumBody').scrollIntoView({behavior:'smooth'})">Rencanakan Trip</button>
        <button class="umt-cta-arrow" onclick="setUmumTab('estimasi');document.getElementById('umumBody').scrollIntoView({behavior:'smooth'})"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3"><path d="M7 17 17 7M9 7h8v8"/></svg></button>
      </div>
    </div>
  </div>`;
  const first=has?allTesti[0]:null;
  const photoBg=first&&first.foto?`background-image:url('${first.foto}')`:`background:${UMGRAD[0]}`;
  const sampleTrips=allTrips().filter(t=>t.inst&&t.pax>0&&t.dest&&t.dest!=='-').slice(0,4);
  const photoCard=`<div class="umt-card-photo" style="${photoBg}"><div class="ov"></div>
    <div class="cap">
      <div class="q">${first?('“'+esc(first.quote)+'”'):'Dipercaya puluhan sekolah, kampus & instansi untuk perjalanan outing class dan study tour yang tertata rapi.'}</div>
      <div class="a">${first?('— '+esc(first.name)+(first.sumber?', '+esc(first.sumber):'')):'Havist Traveller · Your Travel Dream Makers'}</div>
    </div>
  </div>`;
  const listSrc=has?allTesti:(sampleTrips.length?sampleTrips.map(t=>({
    quote:`Outing & Study Tour ke ${(t.dest||'').split('(')[0].trim()} berjalan lancar bersama ${t.pax} peserta dan tim Tour Leader Havist Traveller.`,
    name:t.inst,
    sumber:`${t.pax} Peserta · ${t.bus||1} Bus`,
    platform:'🚌',
    tur:(t.dest||'').split('(')[0].trim()
  })):[{quote:'Perjalanan rombongan tertata mulai dari armada, konsumsi, tiket wisata hingga dokumentasi.',name:'Mitra Sekolah & Instansi',sumber:'Outing & Study Tour',platform:'🚌'}]);
  const doubled=listSrc.concat(listSrc);
  const mcards=doubled.map(t=>`<div class="umt-mcard"><div class="plat">${t.platform||'💬'} ${esc(t.sumber||'')}</div><div class="q">“${esc(t.quote)}”</div><div class="who"><div class="ava" ${t.foto?`style="background-image:url('${t.foto}')"`:''}>${t.foto?'':'?'}</div><div><b>${esc(t.name)}</b><span>${esc(t.tur||'')}</span></div></div></div>`).join('');
  return `<div class="umt-wrap">
    <div class="umt-head">
      <div>
        <div class="umt-tagrow"><div class="umt-badge"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l1.8 5.2L19 9l-5.2 1.8L12 16l-1.8-5.2L5 9l5.2-1.8L12 2z"/></svg></div><div class="umt-pill">Testimoni</div></div>
        <h2>Apa kata mereka<br><span>tentang perjalanan bersama kami</span></h2>
      </div>
      <div class="umt-sub">Setiap perjalanan yang kami susun dibangun dari kepercayaan dan pengalaman nyata peserta.</div>
    </div>
    <div class="umt-grid">${statCard}${photoCard}<div class="umt-marquee"><div class="umt-track">${mcards}</div></div></div>
  </div>`;
}
function umumGo(tab,secId){
  if(tab){setUmumTab(tab);}
  setTimeout(()=>{const el=document.getElementById(secId);if(el)el.scrollIntoView({behavior:'smooth',block:'start'});},40);
}
function vUmum(){
  const tabs=[['paket','Paket & Destinasi'],['hotel','Hotel'],['armada','Armada'],['estimasi','Estimasi Biaya']];
  const nav=tabs.map(([k,l])=>`<button class="tab ${umumTab===k?'active':''}" data-ut="${k}" onclick="setUmumTab('${k}')">${l}</button>`).join('');
  const info=infoPerusahaan();
  const uph=umumPhotos();
  const stats=umumStats();
  const feat=umumFeatured();
  const nCity=[...new Set(CAT.dests.map(d=>d.city))].length;
  const featHTML=feat.map((d,i)=>{const photo=(uph.dest&&uph.dest[d.name])||DESTPHOTO[d.name];const bg=photo?`background-image:url('${photo}')`:`background:${UMGRAD[i%UMGRAD.length]}`;
    return `<div class="umfeat-card" style="${bg}" onclick="umumDestQ='${esc(d.city)}';umumGo('paket','umTabsSec')"><div class="ov"></div><span class="umfeat-badge">Paket Rombongan</span><div class="cnt"><b>${esc(d.name)}</b><span>📍 ${esc(d.city)}</span></div></div>`;}).join('');
  const cu=currentUser();
  const staffBtn=cu.role==='publik'
    ?`<button class="btn-um-ghost" style="padding:8px 18px;border-radius:99px;font-size:13px" onclick="openLoginModal()">Masuk</button>`
    :`<button class="btn-um-primary" style="padding:8px 16px;border-radius:99px;font-size:13px" onclick="go(roleCfg().views.includes('dashboard')?'dashboard':roleCfg().views[1])">Dashboard →</button><button class="btn-um-ghost" style="padding:8px 14px;border-radius:99px;font-size:13px" onclick="openLoginModal()">${esc(cu.nama.split(' ')[0])}</button>`;
  return `
  <header class="um-topnav">
    <div class="um-tbrand" onclick="window.scrollTo({top:0,behavior:'smooth'})"><img src="__LOGO__" alt="${esc(info.nama)}"></div>
    <nav class="um-tlinks">
      <a onclick="window.scrollTo({top:0,behavior:'smooth'})">Beranda</a>
      <a onclick="umumGo('paket','umTabsSec')">Destinasi Trip</a>
      <a onclick="umumGo('hotel','umTabsSec')">Hotel &amp; Armada</a>
      <a onclick="umumGo('estimasi','umTabsSec')">Hitung Biaya</a>
      <a onclick="umumGo(null,'umFaqSec')">FAQ</a>
      <a onclick="umumGo(null,'umFootSec')">Hubungi Kami</a>
    </nav>
    <div style="display:flex;align-items:center;gap:8px">${staffBtn}</div>
  </header>
  <div class="umhero fade" ${uph.hero?`style="background-image:linear-gradient(120deg,rgba(14,36,74,.86),rgba(39,91,181,.78)),url('${esc(uph.hero)}');background-size:cover;background-position:center"`:''}>
    <h1>Jelajahi Indonesia Bersama <em>${esc(info.nama)}</em></h1>
    <p>Paket wisata, outing, dan study tour dengan armada, hotel, dan tour leader berpengalaman — rencanakan perjalanan rombongan Anda tanpa ribet.</p>
    <form class="umhero-search" onsubmit="umumHeroSearch(event)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      <input id="umHeroSearch" placeholder="Coba cari destinasi, mis. Jogja, Pantai, Candi...">
      <button type="submit">Cari →</button>
    </form>
    <div class="umhero-cta">
      <button class="btn-um-primary" onclick="umumGo('paket','umTabsSec')">Lihat Paket Wisata →</button>
      <button class="btn-um-ghost" onclick="umumGo('estimasi','umTabsSec')">▶ Hitung Estimasi Biaya</button>
      <a class="btn-um-ghost" style="text-decoration:none;border-color:rgba(34,197,94,.55);background:rgba(22,163,74,.22)" target="_blank" href="${waLink(info.hp,'Halo '+info.nama+', saya ingin konsultasi paket wisata rombongan.')}">💬 Konsultasi WhatsApp</a>
    </div>
    <div class="umstats">${stats.map(([n,l])=>`<div class="umstat"><div class="n">${n}</div><div class="l">${l}</div></div>`).join('')}</div>
  </div>

  <div class="um-strip-wrap fade">
    <div class="um-strip">
      ${UMUM_BEST_PKGS.map((pk,i)=>{
        const c=calcBestPkg(pk);
        const firstDest=pk.dests[0]||'';
        const photo=(uph.dest&&uph.dest[firstDest])||DESTPHOTO[firstDest];
        const bg=photo?`background-image:url('${photo}')`:`background:${pk.grad}`;
        return `<div class="um-strip-card" onclick="applyBestPkg(${i})">
          <div class="um-strip-img" style="${bg}">
            <span>📍 ${esc(pk.city)}</span>
            <em class="um-pkg-dur">${esc(pk.durLbl)}</em>
          </div>
          <div class="um-strip-body">
            <b>${esc(pk.title)}</b>
            <div class="um-pkg-list">
              <div>👥 <b>${c.pax} Pax</b> · 🚌 ${c.bus} ${esc(c.armName.split('(')[0].trim())}</div>
              <div>🏨 ${c.malam>0?esc(c.hotName)+' ('+c.malam+' mlm)':'One Day Trip (Tanpa Inap)'}</div>
              <div>🍱 ${c.mFreq}× Makan${c.kaosName?' · 👕 Kaos':''} · 🎁 Free ${c.foc} FOC</div>
              <div class="um-pkg-dest">🎟️ ${esc(pk.dests.join(', '))}</div>
            </div>
            <div class="um-pkg-foot">
              <div><small>Mulai dari</small><div class="prc">${rp(c.perpax)}<span>/pax</span></div></div>
              <span class="um-pkg-btn">Pilih →</span>
            </div>
          </div>
        </div>`;
      }).join('')}
    </div>
  </div>

  <div class="um-container">
  <div class="umsec-head"><div><span class="tag">Kenapa Memilih Kami</span><h2>Setiap Perjalanan, Kami Pastikan Berkesan</h2></div></div>
  <div class="umwhy fade">
    <div class="umwhy-card"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0M16 3.5a3.2 3.2 0 0 1 0 6M21 20a6 6 0 0 0-5-5.9"/></svg></div><h4>Tour Leader &amp; Media Berpengalaman</h4><p>Setiap trip didampingi tour leader yang memahami rute &amp; destinasi, serta tim media untuk dokumentasi perjalanan.</p></div>
    <div class="umwhy-card"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.6 8.4 12 3 3.4 8.4v7.2L12 21l8.6-5.4z"/><path d="M12 12 3.4 8.4M12 12v9M12 12l8.6-3.6"/></svg></div><h4>Armada &amp; Hotel Terpilih</h4><p>Bekerja sama dengan ${CAT.armada.length}+ armada dan ${CAT.hotels.length}+ hotel/penginapan di berbagai daerah.</p></div>
    <div class="umwhy-card"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 10h18M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg></div><h4>Harga Transparan</h4><p>Hitung sendiri estimasi biaya di halaman ini — tanpa biaya tersembunyi, konfirmasi akhir dari tim sales kami.</p></div>
  </div>

  ${umumTrustBand()}

  ${umumStepsSection()}

  <div id="umTabsSec" class="umsec-head" style="margin-top:10px"><div><span class="tag">Katalog &amp; Kalkulator Paket</span><h2>Simulasi Harga Paket, Destinasi, Hotel &amp; Armada</h2></div></div>
  <div class="tabs fade" style="padding:0 0 16px">${nav}</div><div id="umumBody" style="margin-bottom:34px"></div>

  <div class="umsec-head"><div><span class="tag">Destinasi Populer</span><h2>Jelajahi ${nCity} Kota/Wilayah Tujuan</h2></div></div>
  <div class="umfeat-grid fade">${featHTML}</div>

  ${umumTestiSection()}

  ${umumFaqSection()}

  <div class="umcta fade">
    <div><h3 style="margin-bottom:4px">Siap merencanakan trip?</h3><p style="color:rgba(255,255,255,.7);font-size:13px">Tim kami siap bantu susun paket sesuai kebutuhan rombongan Anda.</p></div>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <a class="btn-um-primary" style="text-decoration:none" target="_blank" href="${waLink(info.hp,'Halo '+info.nama+', saya ingin tanya paket wisata.')}">💬 Chat via WhatsApp</a>
      ${cu.role==='publik'?`<button class="btn-um-ghost" onclick="umumGo('estimasi','umTabsSec')">▶ Hitung Estimasi Biaya</button>`:`<button class="btn-um-ghost" onclick="go(roleCfg().views.includes('dashboard')?'dashboard':roleCfg().views[1])">Masuk ke Panel Staf →</button>`}
    </div>
  </div>

  ${umumFooterSection()}
  </div>
  <a class="um-wa-float" target="_blank" href="${waLink(info.hp,'Halo '+info.nama+', saya ingin tanya paket wisata.')}">💬 Chat WhatsApp</a>`;
}

let umumActiveCity='BANDUNG';
let umumSelDests=[];
const CITY_ICONS={'BANTEN':'🏖️','JAKARTA':'🎡','BOGOR':'🌿','SUBANG':'♨️','SUKABUMI':'🌊','BANDUNG':'🔥','JOGJA':'🏛️','DIENG':'🌋','MALANG & BROMO':'⛰️','BALI':'🏝️'};
function destKey(d){return (d.city||'')+'::'+(d.name||'')+'::'+(d.note||'');}
function destDisplayName(d){
  const nm=(d.name||'').trim(), nt=(d.note||'').trim();
  if(!nt)return nm;
  if(/^(TMII|Ancol|Ragunan\/Monas)$/i.test(nm)&&nm.toLowerCase()!==nt.toLowerCase()){
    return nm+' — '+nt;
  }
  return nm;
}
function destCatInfo(d){
  const s=((d.name||'')+' '+(d.note||'')).toLowerCase();
  if(/yakult|pocari|industri|pabrik/.test(s))return {lbl:'🏭 Kunjungan Industri',cls:'cat-ind',grad:'linear-gradient(135deg,#0E244A,#275BB5)',ic:'🏭'};
  if(/museum|iptek|sejarah|edukasi|observatorium|geologi|vredeburg|kraton|candi|monas|monumen|peternakan|perikanan|botani|tanaman|biologi|sains/.test(s))return {lbl:'🎓 Wisata Edukasi',cls:'cat-edu',grad:'linear-gradient(135deg,#1E4E9C,#1AA6B7)',ic:'🎓'};
  if(/dufan|fantasi|jungleland|wonderland|seaworld|atlantis|samudra|safari|wahana|atv|jetski|kereta gantung|sky world|scooter|waterpark/.test(s))return {lbl:'🎢 Wahana & Rekreasi',cls:'cat-fun',grad:'linear-gradient(135deg,#5B21B6,#8E63D6)',ic:'🎢'};
  if(/udjo|angklung|budaya|batik|barong|kecak|jimbaran|malioboro|braga|al jabbar/.test(s))return {lbl:'🎭 Budaya & Ikonik',cls:'cat-cul',grad:'linear-gradient(135deg,#9A3412,#E08A1E)',ic:'🎭'};
  return {lbl:'🌿 Alam & Outbound',cls:'cat-nat',grad:'linear-gradient(135deg,#115E59,#2B9D6E)',ic:'🌿'};
}
function getDestPhoto(d){
  const uph=umumPhotos();
  const map=uph.dest||{};
  const disp=destDisplayName(d);
  return map[disp]||map[d.name]||DESTPHOTO[disp]||DESTPHOTO[d.name]||'';
}
function setUmumCity(c){
  umumActiveCity=c;
  umumDestQ='';
  const inp=document.getElementById('umDestSearch');if(inp)inp.value='';
  renderUmum();
}
function toggleUmumDestSelect(key){
  const idx=umumSelDests.indexOf(key);
  if(idx>=0)umumSelDests.splice(idx,1);
  else umumSelDests.push(key);
  renderUmum();
}
function clearUmumDestSelect(){
  umumSelDests=[];
  renderUmum();
}
function applyUmumSelectedToCalc(){
  if(!umumSelDests.length){umumGo('estimasi','umTabsSec');return;}
  const chosen=CAT.dests.filter(d=>umumSelDests.includes(destKey(d)));
  setUmumTab('estimasi');
  setTimeout(()=>{
    const chosenKeys=new Set(umumSelDests);
    document.querySelectorAll('.udest').forEach(cb=>{
      const k=cb.dataset.key||'';
      cb.checked=chosenKeys.has(k);
      const box=cb.closest('.citybox');
      if(cb.checked&&box)box.classList.add('open');
    });
    calcUmum();
    const el=document.getElementById('umumResult')||document.getElementById('umTabsSec');
    if(el)el.scrollIntoView({behavior:'smooth',block:'center'});
    toast(chosen.length+' destinasi dimasukkan ke simulasi paket ✓');
  },40);
}

function umumPaketTab(){
  const all=CAT.dests;
  if(!all.length)return '<div class="empty"><h3>Belum ada destinasi</h3></div>';
  const allCities=[...new Set(all.map(d=>d.city))];
  if(umumActiveCity!=='SEMUA'&&!allCities.includes(umumActiveCity))umumActiveCity=allCities.includes('BANDUNG')?'BANDUNG':allCities[0];
  const q=umumDestQ.trim().toLowerCase();
  const cityPills=`<div class="um-city-pills">
    ${allCities.map(c=>{
      const cnt=all.filter(d=>d.city===c).length;
      const ic=CITY_ICONS[c]||'📍';
      const act=(!q&&umumActiveCity===c)?'active':'';
      return `<button type="button" class="um-city-pill ${act}" onclick="setUmumCity('${esc(c)}')"><span>${ic} ${esc(c)}</span><em>${cnt}</em></button>`;
    }).join('')}
    <button type="button" class="um-city-pill ${(!q&&umumActiveCity==='SEMUA')?'active':''}" onclick="setUmumCity('SEMUA')"><span>🌐 Semua Kota</span><em>${all.length}</em></button>
  </div>`;
  const searchBar=`<div class="um-searchbar">
    <div class="um-search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      <input id="umDestSearch" value="${esc(umumDestQ)}" placeholder="Cari objek wisata, museum, pabrik, pantai, atau kota..." oninput="setUmumDestQ(this.value)"></div>
    <div class="um-search-hint">💡 Klik destinasi untuk memilih &amp; langsung hitung harga paket rombongan</div>
  </div>`;
  const matched=q
    ?all.filter(d=>destDisplayName(d).toLowerCase().includes(q)||d.city.toLowerCase().includes(q)||(d.note||'').toLowerCase().includes(q))
    :(umumActiveCity==='SEMUA'?all:all.filter(d=>d.city===umumActiveCity));
  if(!matched.length)return cityPills+searchBar+`<div class="empty"><h3>Tidak ditemukan</h3><p>Tidak ada destinasi yang cocok dengan "${esc(umumDestQ)}".</p></div>`;
  const showCities=[...new Set(matched.map(d=>d.city))];
  const blocks=showCities.map(c=>{
    const cItems=matched.filter(d=>d.city===c);
    const cards=cItems.map(d=>{
      const key=destKey(d);
      const sel=umumSelDests.includes(key);
      const disp=destDisplayName(d);
      const cat=destCatInfo(d);
      const photo=getDestPhoto(d);
      const bgStyle=photo?`background-image:url('${esc(photo)}')`:`background:${cat.grad}`;
      const subNote=(d.note&&!disp.includes(d.note))?d.note:'Cocok untuk Study Tour & Outing Rombongan';
      return `<div class="um-dcard ${sel?'selected':''}" onclick="toggleUmumDestSelect('${esc(key).replace(/'/g,"\'")}')">
        <div class="um-dcard-visual" style="${bgStyle}">
          <div class="um-dcard-ov"></div>
          <span class="um-dcard-cat">${cat.lbl}</span>
          ${!photo?`<div class="um-dcard-ic">${cat.ic}</div>`:''}
          <span class="um-dcard-city">📍 ${esc(c)}</span>
        </div>
        <div class="um-dcard-body">
          <h4>${esc(disp)}</h4>
          <p>${esc(subNote)}</p>
          <div class="um-dcard-foot">
            <span class="um-dcard-pick ${sel?'on':''}">${sel?'✓ Masuk Paket':'+ Pilih ke Paket'}</span>
          </div>
        </div>
      </div>`;
    }).join('');
    return `<div class="panel fade" style="margin-bottom:18px;padding:18px">
      <div class="panel-h" style="padding:0 0 14px;border-bottom:1px solid var(--line)">
        <div>
          <h3 style="font-size:17px">${CITY_ICONS[c]||'📍'} Destinasi Wisata ${esc(c)} <span style="color:var(--muted);font-size:12.5px;font-weight:600">(${cItems.length} objek wisata)</span></h3>
          <p style="font-size:12px;color:var(--muted);margin-top:2px">Pilih satu atau beberapa objek wisata di ${esc(c)} untuk melihat simulasi harga paket per peserta</p>
        </div>
        <button class="btn-acc ok" onclick="applyUmumSelectedToCalc()">🧮 Buka Kalkulator Paket →</button>
      </div>
      <div class="um-dgrid" style="margin-top:14px">${cards}</div>
    </div>`;
  }).join('');
  const selObjs=all.filter(d=>umumSelDests.includes(destKey(d)));
  const cartBar=selObjs.length?`<div class="um-cart-bar fade">
    <div class="um-cart-info">
      <b>🎒 ${selObjs.length} Destinasi Dipilih:</b>
      <span>${esc(selObjs.map(d=>destDisplayName(d)).join(', '))}</span>
    </div>
    <div class="um-cart-act">
      <button type="button" class="btn-acc no" onclick="clearUmumDestSelect()">Reset</button>
      <button type="button" class="btn-um-primary" style="padding:9px 16px;font-size:12.5px" onclick="applyUmumSelectedToCalc()">Hitung Harga Paket (${selObjs.length} Wisata) →</button>
    </div>
  </div>`:'';
  return cityPills+searchBar+blocks+cartBar;
}
function umumHotelTab(){
  const regions=[...new Set(CAT.hotels.map(h=>h.region))];
  if(!regions.length)return '<div class="empty"><h3>Belum ada data hotel</h3></div>';
  return regions.map(r=>{
    const rows=CAT.hotels.filter(h=>h.region===r).map(h=>`<tr><td style="font-weight:600">${esc(h.name)}</td><td>${esc(r)}</td><td><span class="pill lunas">Mitra Resmi · Paket Rombongan</span></td></tr>`).join('');
    return `<div class="panel fade" style="margin-bottom:18px"><div class="panel-h"><h3>${esc(r)} <span style="color:var(--muted);font-size:12px;font-weight:600">(${CAT.hotels.filter(h=>h.region===r).length} hotel)</span></h3><button class="lnk" onclick="umumGo('estimasi','umTabsSec')">Pilih di Kalkulator →</button></div>
      <div class="tbl-scroll"><table style="margin-top:10px"><thead><tr><th>Nama Hotel</th><th>Wilayah</th><th>Keterangan</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
  }).join('');
}
function umumArmadaTab(){
  const rows=CAT.armada.map(a=>`<tr><td style="font-weight:600">${esc(a.name)}</td><td>${armSeat(a)} seat</td><td><span class="pill jadwal">Full AC · Audio/Karaoke · Reclining Seat</span></td></tr>`).join('');
  return `<div class="panel fade"><div class="panel-h"><h3>Pilihan Armada Pariwisata</h3><button class="lnk" onclick="umumGo('estimasi','umTabsSec')">Hitung Estimasi Paket →</button></div>
    <div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Jenis Armada</th><th>Kapasitas</th><th>Fasilitas Standar</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
}
function umumEstimasiTab(){
  const regions=[...new Set(CAT.hotels.map(h=>h.region))];
  const cities=[...new Set(CAT.dests.map(d=>d.city))];
  const kaosOpt=CAT.kaos.map(k=>`<option value="${k.price}" data-name="${esc(k.name)}">${esc(k.name)}</option>`).join('');
  const presets=[[33,'MEDIUM BUS (31-35 Seat)','1 Medium Bus (33 Pax)'],[50,'BIG BUS (50 Seat)','1 Big Bus (50 Pax)'],[100,'BIG BUS (50 Seat)','2 Big Bus (100 Pax)'],[150,'BIG BUS (50 Seat)','3 Big Bus (150 Pax)'],[300,'BIG BUS (50 Seat)','6 Big Bus (300 Pax)']];
  return `<div class="panel fade"><div class="panel-h"><h3>Simulasi Harga Paket Wisata (All-In per Pax)</h3><span style="font-size:12px;color:var(--muted)">Pilih kapasitas cepat atau sesuaikan fasilitas rombongan</span></div>
    <div style="padding:16px 19px">
      <label class="flbl" style="margin-bottom:6px">Pilih Cepat Kapasitas Rombongan:</label>
      <div class="um-preset-row">${presets.map(([px,arm,lbl])=>`<button type="button" class="um-preset-btn ${px===50?'active':''}" data-pax="${px}" onclick="setUmumPreset(${px},'${arm}')">🚌 ${lbl}</button>`).join('')}</div>
      <div class="frow">
        <div><label class="flbl">Jumlah Peserta (pax)</label><input id="u_pax" class="finput" type="number" value="50" min="1" oninput="calcUmum()"></div>
        <div><label class="flbl">Durasi Menginap (malam)</label><input id="u_malam" class="finput" type="number" value="1" min="0" oninput="calcUmum()"></div>
      </div>
      <div class="frow">
        <div><label class="flbl">Tanggal Keberangkatan (opsional)</label><input id="u_tgl" class="finput" type="date" onchange="calcUmum()"></div>
        <div><label class="flbl">Konfigurasi Kamar Hotel</label><select id="u_share" class="finput" onchange="calcUmum()"><option value="4">Quad Share (1 kamar 4 peserta)</option><option value="2">Twin Share (1 kamar 2 peserta)</option></select></div>
      </div>
      <label class="flbl">Pilihan Armada</label><select id="u_armada" class="finput" style="margin-bottom:10px" onchange="calcUmum()">${CAT.armada.map((a,i)=>`<option value="${a.rate}" data-name="${esc(a.name)}" data-seat="${armSeat(a)}" ${i===3?'selected':''}>${esc(a.name)} (Kapasitas ${armSeat(a)} seat)</option>`).join('')}</select>
      <label class="flbl">Pilihan Hotel (opsional)</label><select id="u_hotel" class="finput" style="margin-bottom:10px" onchange="calcUmum()"><option value="0|0" data-name="Tanpa Hotel">— Tanpa Menginap (One Day Trip) —</option>${regions.map(r=>`<optgroup label="${esc(r)}">`+CAT.hotels.filter(h=>h.region===r).map(h=>`<option value="${h.wd}|${h.we}" data-name="${esc(h.name)}">${esc(h.name)}</option>`).join('')+'</optgroup>').join('')}</select>
      <div class="frow">
        <div><label class="flbl">Frekuensi Makan Selama Trip</label><input id="u_mfreq" class="finput" type="number" value="3" min="0" oninput="calcUmum()"></div>
        <div><label class="flbl">Merchandise / Kaos Rombongan</label><select id="u_kaos" class="finput" onchange="calcUmum()">${kaosOpt}</select></div>
      </div>
      <label class="flbl" style="margin-top:6px">Pilih Destinasi Wisata <span style="color:var(--muted-2);font-weight:500">(klik kota untuk membuka daftar objek wisata)</span></label>
      <div class="destwrap">${cities.map(c=>{const items=CAT.dests.filter(d=>d.city===c).map(d=>{const disp=destDisplayName(d);const sub=(d.note&&!disp.includes(d.note))?d.note:'';return `<label class="dest-item"><input type="checkbox" class="udest" data-key="${esc(destKey(d))}" data-price="${d.price}" data-name="${esc(disp)}" onchange="calcUmum()"><span>${esc(disp)}${sub?'<span class="opt">'+esc(sub)+'</span>':''}</span></label>`;}).join('');
        return `<div class="citybox"><div class="cityhd" onclick="this.parentNode.classList.toggle('open')"><span>${esc(c)}</span><span class="cnt">${CAT.dests.filter(d=>d.city===c).length} destinasi</span></div><div class="citygrid">${items}</div></div>`;}).join('')}</div>
      <div id="umumResult" style="margin-top:16px"></div>
    </div>
  </div>`;
}
function calcUmum(){
  const g=id=>document.getElementById(id);
  const pax=Math.max(1,+(g('u_pax')?g('u_pax').value:0)||1);
  const malam=Math.max(0,+(g('u_malam')?g('u_malam').value:0)||0);
  const share=Math.max(1,+(g('u_share')?g('u_share').value:4)||4);
  const hari=malam+1;
  const armEl=g('u_armada');
  const armOpt=armEl&&armEl.selectedOptions&&armEl.selectedOptions[0];
  const armRate=+(armEl?armEl.value:0)||0;
  const armName=armOpt?(armOpt.dataset.name||'Armada'):'Armada';
  const cap=+(armOpt?armOpt.dataset.seat:0)||kapasitas(armName);
  const bus=Math.max(1,Math.ceil(pax/cap));
  const hotEl=g('u_hotel');
  const hotOpt=hotEl&&hotEl.selectedOptions&&hotEl.selectedOptions[0];
  const hotName=hotOpt?(hotOpt.dataset.name||'Tanpa Hotel'):'Tanpa Hotel';
  const hd=(hotEl?hotEl.value:'0|0').split('|');
  const tgl=g('u_tgl')?g('u_tgl').value:'';
  const isWknd=tgl&&([0,6].includes(new Date(tgl).getDay()));
  const hotelRate=isWknd?(+hd[1]||0):(+hd[0]||0);
  const kamar=(malam>0&&hotelRate>0)?Math.ceil(pax/share):0;
  const mFreq=Math.max(0,+(g('u_mfreq')?g('u_mfreq').value:0)||0);
  const mPrice=35000;
  const kaosEl=g('u_kaos');
  const kaosRate=+(kaosEl?kaosEl.value:0)||0;
  const kaosName=(kaosEl&&kaosEl.selectedOptions&&kaosEl.selectedOptions[0])?kaosEl.selectedOptions[0].dataset.name:'';
  const checkedDests=[...document.querySelectorAll('.udest:checked')];
  const destPrice=checkedDests.reduce((s,el)=>s+(+el.dataset.price||0),0);
  const destNames=checkedDests.map(el=>el.dataset.name).filter(Boolean);
  checkedDests.forEach(el=>{const box=el.closest('.citybox');if(box)box.classList.add('has');});
  document.querySelectorAll('.destwrap .citybox').forEach(b=>{if(!b.querySelectorAll('.udest:checked').length)b.classList.remove('has');});
  const cT=armRate*bus*hari, cH=malam>0?hotelRate*kamar*malam:0, cM=mFreq*mPrice*pax, cK=kaosRate*pax, cW=destPrice*pax;
  const modal=cT+cH+cM+cK+cW;
  const markup=1+(store('markup',20)/100);
  const mk=modal*markup;
  const foc=Math.min(Math.floor(pax/10),25);
  const subsidi=foc*(pax>0?mk/pax:0);
  const jualGrup=Math.max(0,mk-subsidi);
  const perpax=pax>0?Math.ceil((jualGrup/pax)/1000)*1000:0;
  const totalPaket=perpax*pax;
  lastUmumEst={pax,malam,hari,bus,armName,hotName,kamar,mFreq,kaosName,destNames,foc,totalPaket,perpax};
  const r=document.getElementById('umumResult');if(!r)return;
  const info=infoPerusahaan();
  const waText=`Halo ${info.nama}, saya ingin konsultasi paket wisata untuk ${pax} peserta (${hari} Hari ${malam} Malam, ${bus} unit ${armName}${destNames.length?', tujuan: '+destNames.join(', '):''}). Estimasi di web ${rp(perpax)}/pax. Mohon penawaran resminya.`;
  r.innerHTML=`<div class="result-card" style="margin:0">
    <div class="rc-label">Estimasi Harga Paket Per Peserta (All-In)</div>
    <div class="rc-price">${rp(perpax)} <span style="font-size:14px;font-weight:500;opacity:.85">/ pax</span></div>
    <div class="rc-dur">${hari} Hari ${malam} Malam · ${pax} Peserta · Estimasi Total Rombongan: <b>${rp(totalPaket)}</b></div>
    <div class="rc-break" style="margin-top:12px">
      <div class="bk-h">Fasilitas Paket yang Termasuk</div>
      <div class="rc-row"><span>🚌 Transportasi Pariwisata</span><b>${bus} unit × ${esc(armName)} (${hari} hari)</b></div>
      <div class="rc-row"><span>🏨 Akomodasi Hotel</span><b>${kamar>0?`${kamar} kamar × ${malam} malam (${esc(hotName)})`:'One Day Trip (Tanpa Menginap)'}</b></div>
      <div class="rc-row"><span>🍱 Konsumsi Peserta</span><b>${mFreq>0?`${mFreq}× makan selama perjalanan`:'Tanpa paket makan'}</b></div>
      ${kaosRate>0?`<div class="rc-row"><span>👕 Merchandise Rombongan</span><b>${esc(kaosName)} (${pax} pcs)</b></div>`:''}
      <div class="rc-row"><span>🎟️ Tiket Objek Wisata</span><b>${destNames.length?esc(destNames.join(', ')):'Belum ada objek wisata dipilih'}</b></div>
      <div class="rc-row"><span>🎁 Bonus Pendamping (FOC)</span><b>Gratis ${foc} kuota guru/pendamping + Tour Leader</b></div>
    </div>
    <div class="um-calc-actions">
      <button type="button" class="btn-save" style="margin:0;background:var(--gold);color:var(--navy)" onclick="openUmumProposalModal()">📄 Unduh Estimasi Proposal (PDF)</button>
      <a class="btn-save" style="margin:0;display:inline-flex;align-items:center;justify-content:center;text-align:center;text-decoration:none;background:#16a34a;color:#fff" target="_blank" href="${waLink(info.hp,waText)}">💬 Konsultasi &amp; Nego via WhatsApp</a>
    </div>
  </div>`;
}
function addCrew(){
  const nama=document.getElementById('k_nama').value.trim();const peran=document.getElementById('k_peran').value;
  const hp=document.getElementById('k_hp').value.trim();const tarif=parseInt(document.getElementById('k_tarif').value)||0;
  if(!nama){toast('Nama wajib diisi');return;}
  const list=crewList().slice();list.push({id:'K'+Date.now(),nama,peran,hp:hp||'-',tarif,status:'Aktif'});saveCrewList(list);
  toast('Crew '+nama+' ditambahkan');renderCrew();
}
function updateCrew(id,patch){
  const list=crewList().map(c=>c.id===id?Object.assign({},c,patch):c);
  saveCrewList(list);
}
function deleteCrew(id){
  const c=crewById(id);if(!c)return;
  saveCrewList(crewList().filter(x=>x.id!==id));
  const am=assignMap();let chg=false;
  Object.keys(am).forEach(tid=>{const a=normAssignEntry(am[tid]);const n1=a.tls.length,n2=a.medias.length;a.tls=a.tls.filter(x=>x.id!==id);a.medias=a.medias.filter(x=>x.id!==id);if(a.tls.length!==n1||a.medias.length!==n2){am[tid]=a;chg=true;}});
  if(chg)save('assign',am);
  if(currentSales()===id)save('currentSales','');
  if(currentTL()===id)save('currentTL','');
  toast('Crew '+c.nama+' dihapus');renderCrew();
}
function confirmDeleteCrew(id){
  const c=crewById(id);if(!c)return;
  const old=document.getElementById('delCrewOv');if(old)old.remove();
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='delCrewOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:380px"><div class="pv-bar"><b>Konfirmasi Hapus Crew</b><button class="btn-acc no" onclick="document.getElementById('delCrewOv').remove()">Batal</button></div>
    <div style="background:#fff;margin:16px;border-radius:10px;padding:18px;font-size:13.5px;line-height:1.5">
      <p style="margin:0 0 14px">Yakin ingin menghapus <b>${esc(c.nama)}</b> (${esc(c.peran)}) dari daftar crew? Penugasan trip terkait juga akan dibersihkan.</p>
      <div style="display:flex;gap:8px;justify-content:flex-end">
        <button class="btn-acc no" onclick="document.getElementById('delCrewOv').remove()">Batal</button>
        <button class="btn-acc" style="background:var(--red);color:#fff" onclick="execDeleteCrew('${c.id}')">Ya, Hapus</button>
      </div>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function execDeleteCrew(id){
  ['delCrewOv','crewOv','editCrewOv'].forEach(mid=>{const el=document.getElementById(mid);if(el)el.remove();});
  deleteCrew(id);
}
function openEditCrew(id){
  const c=crewById(id);if(!c)return;
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='editCrewOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:440px"><div class="pv-bar"><b>Edit Crew — ${esc(c.nama)}</b><button class="btn-acc no" onclick="document.getElementById('editCrewOv').remove()">Tutup</button></div>
    <div style="background:#fff;margin:16px;border-radius:10px;padding:18px">
      <label class="flbl">Nama</label><input id="ec_nama" class="finput" value="${esc(c.nama)}">
      <div class="frow">
        <div><label class="flbl">Bagian</label><select id="ec_peran" class="finput">${['Tour Leader','Media','Sales'].map(p=>`<option ${c.peran===p?'selected':''}>${p}</option>`).join('')}</select></div>
        <div><label class="flbl">Status</label><select id="ec_status" class="finput">${['Aktif','Nonaktif'].map(s=>`<option ${c.status===s?'selected':''}>${s}</option>`).join('')}</select></div>
      </div>
      <div class="frow">
        <div><label class="flbl">No. HP</label><input id="ec_hp" class="finput" value="${esc(c.hp||'')}"></div>
        <div><label class="flbl">Tarif / hari (Rp)</label><input id="ec_tarif" class="finput" type="number" value="${c.tarif||0}"></div>
      </div>
      <div style="display:flex;gap:8px;margin-top:10px">
        <button class="btn-save" style="flex:1" onclick="submitEditCrew('${c.id}')">Simpan Perubahan</button>
        <button class="btn-save" style="background:var(--red);width:auto;padding:10px 14px" onclick="confirmDeleteCrew('${c.id}')">Hapus</button>
      </div>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function submitEditCrew(id){
  const nama=(document.getElementById('ec_nama').value||'').trim();
  if(!nama){toast('Nama wajib diisi');return;}
  updateCrew(id,{
    nama,
    peran:document.getElementById('ec_peran').value,
    status:document.getElementById('ec_status').value,
    hp:(document.getElementById('ec_hp').value||'').trim()||'-',
    tarif:parseInt(document.getElementById('ec_tarif').value)||0
  });
  const ov=document.getElementById('editCrewOv');if(ov)ov.remove();
  toast('Data crew '+nama+' diperbarui');renderCrew();
}
function setCrewTab(k){crewTab=k;const nav=document.querySelector('#view .tabs');if(nav)nav.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.kt===k));renderCrew();}
function renderCrew(){const b=document.getElementById('crewBody');if(!b)return;b.innerHTML=crewTab==='penugasan'?crewPenugasan():crewDaftar();}
function vCrew(){
  const tabs=[['daftar','Daftar Crew'],['penugasan','Penugasan Trip']];
  const nav=tabs.map(([k,l])=>`<button class="tab ${crewTab===k?'active':''}" data-kt="${k}" onclick="setCrewTab('${k}')">${l}</button>`).join('');
  return `<div class="hello fade"><h1>Crew</h1><p>Tour Leader, Sales & Media — daftar, penugasan trip, dan gaji per trip</p></div>
  <div class="tabs" style="padding:0 0 16px">${nav}</div><div id="crewBody"></div>`;
}
const CREWBADGE={Sales:'var(--blue)','Tour Leader':'var(--teal)',Media:'var(--purple)'};
function crewDaftar(){
  const list=crewList();const by=p=>list.filter(k=>k.peran===p).length;
  const rows=list.map(k=>{const st=crewStat(k.id);
    return `<tr class="clk" onclick="openCrew('${k.id}')"><td><div class="trip"><div class="th" style="background:${CREWBADGE[k.peran]||'var(--muted)'}">${k.nama.slice(0,2).toUpperCase()}</div><div><div class="nm">${esc(k.nama)}</div><div class="loc">${esc(k.hp)}</div></div></div></td><td><span class="pill jadwal" style="background:${CREWBADGE[k.peran]}22;color:${CREWBADGE[k.peran]}">${k.peran}</span></td><td class="price mono">${k.tarif?rp(k.tarif)+' /hari':'<span style=color:var(--muted-2)>—</span>'}</td><td class="mono">${st.n?st.n+' trip':'<span style=color:var(--muted-2)>—</span>'}</td><td class="price mono">${st.gaji?rp(st.gaji):'<span style=color:var(--muted-2)>—</span>'}</td><td><span class="pill ${k.status==='Aktif'?'lunas':'dp'}">${k.status}</span></td><td style="text-align:right;white-space:nowrap" onclick="event.stopPropagation()"><button class="btn-acc no" style="margin-right:4px" onclick="openEditCrew('${k.id}')">Edit</button><button class="pay-del" onclick="confirmDeleteCrew('${k.id}')" title="Hapus crew">✕</button></td></tr>`;}).join('');
  return `<div class="grid fade" style="grid-template-columns:1fr 320px">
    <div class="panel" style="margin:0"><div class="panel-h"><h3>Daftar Crew</h3><span style="font-size:12px;color:var(--muted)">${by('Tour Leader')} TL · ${by('Media')} Media · ${by('Sales')} Sales</span></div><div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Nama</th><th>Bagian</th><th>Tarif</th><th>Trip</th><th>Total Gaji</th><th>Status</th><th style="text-align:right">Aksi</th></tr></thead><tbody>${rows}</tbody></table></div></div>
    <div class="side-card" style="margin:0"><div class="panel-h" style="padding:0 0 14px"><h3 style="font-size:14.5px">Tambah Crew</h3></div>
      <label class="flbl">Nama</label><input id="k_nama" class="finput" placeholder="Nama crew">
      <label class="flbl">Bagian</label><select id="k_peran" class="finput"><option>Tour Leader</option><option>Media</option><option>Sales</option></select>
      <label class="flbl">No. HP</label><input id="k_hp" class="finput" placeholder="0812-...">
      <label class="flbl">Tarif / hari (Rp)</label><input id="k_tarif" class="finput" type="number" placeholder="150000">
      <button class="btn-save" onclick="addCrew()">+ Tambah Crew</button>
    </div>
  </div>
  <p style="font-size:12px;color:var(--muted-2);margin-top:14px">Klik baris crew untuk melihat riwayat trip & total gajinya. Gaji per trip = tarif/hari × jumlah hari. Atur penugasan di tab "Penugasan Trip".</p>`;
}
function openCrew(crewId){
  const c=crewById(crewId);if(!c)return;const st=crewStat(crewId);
  const sorted=st.trips.slice().sort((a,b)=>(a.brk||'')<(b.brk||'')?1:-1);
  const rows=sorted.map(t=>{const a=tripAssign(t.id);const role=a.tls.some(x=>x.id===crewId)?'Tour Leader':'Media';const hari=tripDays(t);
    const trf=crewTripTarif(crewId,t.id);
    const r=tripRange(t);const bentrok=sorted.some(o=>o.id!==t.id&&overlap(r,tripRange(o)));
    return `<div class="pp-row"><div class="pp-main"><div class="pp-nm">${esc(t.inst)}</div><div class="pp-sub">${dateID(t.brk)}${t.pul?' – '+dateID(t.pul):''} · ${hari} hari · ${role} (${rp(trf)}/hr)${bentrok?' · <b style="color:var(--red)">⚠ bentrok</b>':''}</div></div>
      <div class="pp-num"><b>${rp(trf*hari)}</b><span style="color:var(--muted)">${STLBL[tripStatus(t)]}</span></div></div>`;}).join('');
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='crewOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:520px"><div class="pv-bar"><b>${esc(c.nama)} — ${esc(c.peran)}</b><div><button class="btn-acc ok" style="margin-right:6px" onclick="document.getElementById('crewOv').remove();openEditCrew('${c.id}')">Edit</button><button class="btn-acc no" style="margin-right:6px;color:var(--red)" onclick="confirmDeleteCrew('${c.id}')">Hapus</button><button class="btn-acc no" onclick="document.getElementById('crewOv').remove()">Tutup</button></div></div>
    <div style="background:var(--bg);padding:16px;max-height:76vh;overflow:auto">
      <div class="pay-sum" style="margin-bottom:14px"><div><span>Total Trip</span><b>${st.n}</b></div><div><span>Total Hari</span><b>${st.hari}</b></div><div><span>Total Gaji</span><b style="color:var(--green)">${rp(st.gaji)}</b></div></div>
      <div class="td-card"><h5>Info</h5>
        <div class="td-row"><span>No. HP</span><b>${esc(c.hp||'—')}</b></div>
        <div class="td-row"><span>Tarif per hari</span><b>${c.tarif?rp(c.tarif):'—'}</b></div>
        <div class="td-row"><span>Status</span><b>${esc(c.status)}</b></div>
      </div>
      <div class="td-card"><h5>Riwayat & Jadwal Trip ${st.n?`(${st.n})`:''}</h5>
        ${rows||'<div style="font-size:12.5px;color:var(--muted);padding:6px 0">Belum pernah ditugaskan ke trip mana pun.</div>'}</div>
      <p style="font-size:11.5px;color:var(--muted-2);padding:0 2px">Trip dengan tanda ⚠ tanggalnya tumpang tindih dengan trip lain crew ini.</p>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function crewPenugasan(){
  const up=upcoming();const tls=crewList().filter(c=>c.peran==='Tour Leader');const mds=crewList().filter(c=>c.peran==='Media');
  const optAdd=(arr,assigned,tid,lbl)=>`<option value="">+ Tambah ${lbl}...</option>`+arr.filter(c=>!assigned.some(x=>x.id===c.id)).map(c=>{const busy=crewSibuk(c.id,tid);return `<option value="${c.id}">${esc(c.nama)} (${rp(c.tarif||0)}/hr)${busy?' ⚠ bentrok':''}</option>`;}).join('');
  const cell=(assigned,arr,tid,role,lbl)=>{
    const chips=assigned.map(x=>{const c=crewById(x.id);if(!c)return '';
      return `<div style="display:flex;align-items:center;gap:4px;margin-bottom:4px;background:#f4f6fa;padding:4px 6px;border-radius:7px"><span style="font-size:12px;font-weight:600;flex:1;min-width:75px">${esc(c.nama.split(' ')[0])}</span><input class="finput" type="number" style="width:86px;margin:0;padding:3px 6px;font-size:11.5px" value="${x.tarif}" title="Edit gaji/hari (Rp)" onchange="setTripCrewTarif('${tid}','${role}','${c.id}',this.value)"><span style="font-size:10.5px;color:var(--muted)">/hr</span><button class="pay-del" onclick="removeTripCrew('${tid}','${role}','${c.id}')">✕</button></div>`;}).join('');
    return chips+`<select class="finput" style="margin:0;padding:6px 8px;font-size:12px" onchange="if(this.value)addTripCrew('${tid}','${role}',this.value)">${optAdd(arr,assigned,tid,lbl)}</select>`;
  };
  const rows=up.map(t=>{const a=tripAssign(t.id);const hari=tripDays(t);const g=tripGaji(t);
    return `<tr><td><div class="nm" style="font-weight:700">${esc(t.inst)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${dateID(t.brk)} · ${hari} hari · ${t.pax} pax</div></td>
    <td>${cell(a.tls,tls,t.id,'tl','TL')}</td>
    <td>${cell(a.medias,mds,t.id,'media','Media')}</td>
    <td class="price mono">${g?rp(g):'—'}</td></tr>`;}).join('');
  const tot=totalGajiCrew();const assignedN=up.filter(t=>{const a=tripAssign(t.id);return a.tls.length||a.medias.length;}).length;
  return `<div class="cards fade" style="grid-template-columns:repeat(3,1fr)">
    <div class="scard"><div class="ic b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg></div><div class="lbl">Trip Mendatang</div><div class="val mono">${up.length}</div><div class="sub" style="color:var(--muted)">${assignedN} sudah ada crew</div></div>
    <div class="scard"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/></svg></div><div class="lbl">Total Gaji Crew (ditugaskan)</div><div class="val mono">${jt(tot)}</div><div class="sub" style="color:var(--muted)">masuk pengeluaran Keuangan</div></div>
    <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div><div class="lbl">Rata-rata / Trip</div><div class="val mono">${assignedN?jt(tot/assignedN):'Rp 0'}</div></div>
  </div>
  <div class="panel fade" style="margin:0"><div class="panel-h"><h3>Penugasan Tour Leader & Media per Trip</h3><span style="font-size:12px;color:var(--muted)">gaji = tarif/hari × jumlah hari</span></div>
  <div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Trip</th><th>Tour Leader</th><th>Media</th><th>Gaji Trip</th></tr></thead><tbody>${rows}</tbody></table></div></div>
  <p style="font-size:12px;color:var(--muted-2);margin-top:14px">Pilih TL & Media untuk tiap trip. Gaji otomatis dilipatkan sesuai jumlah hari trip, dan totalnya ikut di Keuangan (Arus Kas) & Dashboard.</p>`;
}

const SYNC_KEYS=['acc','accounts','assign','checklist','crew_add','crew_list','customPiutang','excelPiutang','excelTrips','excelVendor','info','klien','markup','payClient','payVendor','penawaran','piutOverride','prep','prices','reimburse','seedAccEdits','target','tripOverride','tripStatus','umumPhotos','cat_dests','cat_hotels','cat_meals','cat_armada'];
let _hostSyncTimer=null,_hostOnline=false;
function collectStateObj(){
  const dump={_exportedAt:new Date().toISOString(),_app:'Havist Traveller'};
  SYNC_KEYS.forEach(k=>{const v=localStorage.getItem('havist_'+k);if(v!==null)try{dump[k]=JSON.parse(v);}catch(e){dump[k]=v;}});
  return dump;
}
function applyStateObj(obj){
  if(!obj||typeof obj!=='object')return;
  SYNC_KEYS.forEach(k=>{if(k in obj){const str=JSON.stringify(obj[k]);_memStore['havist_'+k]=str;try{localStorage.setItem('havist_'+k,str);}catch(e){}}});
}
async function pushToHosting(silent){
  try{
    const res=await fetch('api.php?action=save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(collectStateObj())});
    if(!res.ok)throw new Error('HTTP '+res.status);
    _hostOnline=true;
    if(!silent)toast('Tersimpan ke Server Hosting (api.php) ✓');
  }catch(e){if(!silent)toast('api.php belum terdeteksi di server ini');}
}
async function pullFromHosting(silent){
  try{
    const res=await fetch('api.php?action=load&_='+Date.now());
    if(!res.ok)return false;
    const ct=res.headers.get('content-type')||'';
    if(!ct.includes('json'))return false;
    const obj=await res.json();
    _hostOnline=true;
    if(obj&&!obj._empty){applyStateObj(obj);applyRoleUI();go(location.hash.slice(1)||'umum');pullFromHosting(true);if(!silent)toast('Data dimuat dari Server Hosting ✓');return true;}
  }catch(e){if(!silent)toast('api.php belum terdeteksi di server ini');}
  return false;
}
function saveUmumHero(val){const p=umumPhotos();p.hero=(val||'').trim();save('umumPhotos',p);toast('Foto hero disimpan ✓');}
function saveUmumDestPhoto(name,val){
  const p=umumPhotos();p.dest=p.dest||{};
  if((val||'').trim())p.dest[name]=(val||'').trim();
  else delete p.dest[name];
  save('umumPhotos',p);toast('Foto '+name+' diperbarui ✓');
}
function savePickedDestPhoto(){
  const k=document.getElementById('sp_dest_key')?document.getElementById('sp_dest_key').value:'';
  const u=document.getElementById('sp_dest_url')?document.getElementById('sp_dest_url').value:'';
  if(!k||!u.trim()){toast('Pilih destinasi dan isi URL foto terlebih dahulu');return;}
  saveUmumDestPhoto(k,u.trim());
  go('setting');
}
function uploadPickedDestPhoto(inp){
  const k=document.getElementById('sp_dest_key')?document.getElementById('sp_dest_key').value:'';
  if(!k){toast('Pilih destinasi terlebih dahulu');return;}
  uploadUmumFile(inp,'dest',k);
}
async function uploadUmumFile(input,target,name){
  const f=input.files&&input.files[0];if(!f)return;
  try{
    const fd=new FormData();fd.append('file',f);
    const res=await fetch('api.php?action=upload',{method:'POST',body:fd});
    if(res.ok){const j=await res.json();if(j&&j.ok&&j.url){
      if(target==='hero'){saveUmumHero(j.url);const el=document.getElementById('up_hero');if(el)el.value=j.url;}
      else if(target==='dest'){saveUmumDestPhoto(name,j.url);go('setting');}
      return;
    }}
  }catch(e){}
  const r=new FileReader();
  r.onload=()=>{
    if(target==='hero'){saveUmumHero(r.result);const el=document.getElementById('up_hero');if(el)el.value=r.result;}
    else if(target==='dest'){saveUmumDestPhoto(name,r.result);go('setting');}
  };
  r.readAsDataURL(f);
}
function addUmumTesti(){
  const name=(document.getElementById('ut_name').value||'').trim();
  const sumber=(document.getElementById('ut_src').value||'').trim()||'WhatsApp';
  const quote=(document.getElementById('ut_quote').value||'').trim();
  const foto=(document.getElementById('ut_foto').value||'').trim();
  if(!name||!quote){toast('Isi nama dan kutipan testimoni');return;}
  const p=umumPhotos();p.testi=p.testi||[];
  p.testi.push({name,sumber,quote,foto,platform:'💬',tur:sumber});
  save('umumPhotos',p);toast('Testimoni ditambahkan ✓');go('setting');
}
function delUmumTesti(idx){
  const p=umumPhotos();p.testi=(p.testi||[]).filter((_,i)=>i!==idx);
  save('umumPhotos',p);toast('Testimoni dihapus');go('setting');
}
function buildJsonDump(){return JSON.stringify(collectStateObj(),null,2);}
function exportAllJSON(){
  const txt=buildJsonDump();
  try{
    const blob=new Blob([txt],{type:'application/json'});
    const a=document.createElement('a');a.href=URL.createObjectURL(blob);
    a.download='havist-traveller-backup-'+new Date().toISOString().slice(0,10)+'.json';
    document.body.appendChild(a);a.click();a.remove();
  }catch(e){}
  const old=document.getElementById('jsonOv');if(old)old.remove();
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='jsonOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:560px"><div class="pv-bar"><b>Backup Data JSON</b><button class="btn-acc no" onclick="document.getElementById('jsonOv').remove()">Tutup</button></div>
    <div style="background:#fff;margin:16px;border-radius:10px;padding:16px">
      <div style="font-size:12px;color:var(--muted);margin-bottom:8px">Jika download otomatis diblokir oleh preview browser, klik <b>Salin JSON</b> lalu simpan di Notes/file:</div>
      <textarea id="jsonDumpBox" class="finput" rows="8" style="font-family:monospace;font-size:11.5px">${esc(txt)}</textarea>
      <div style="display:flex;gap:8px;margin-top:8px">
        <button class="btn-save" style="flex:1" onclick="copyJsonDump()">Salin Teks JSON</button>
      </div>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
  toast('Backup JSON siap ✓');
}
function copyJsonDump(){
  const el=document.getElementById('jsonDumpBox');if(!el)return;
  el.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(el.value).then(()=>toast('JSON disalin ke clipboard ✓')).catch(()=>{document.execCommand('copy');toast('JSON disalin ✓');});}
  else{document.execCommand('copy');toast('JSON disalin ✓');}
}
function openRestoreJsonModal(){
  const old=document.getElementById('jsonOv');if(old)old.remove();
  const ov=document.createElement('div');ov.className='pv-overlay';ov.id='jsonOv';
  ov.innerHTML=`<div class="pv-modal" style="max-width:560px"><div class="pv-bar"><b>Pulihkan Data JSON</b><button class="btn-acc no" onclick="document.getElementById('jsonOv').remove()">Tutup</button></div>
    <div style="background:#fff;margin:16px;border-radius:10px;padding:16px">
      <div style="font-size:12px;color:var(--muted);margin-bottom:8px">Pilih file <code>.json</code> atau tempel teks JSON backup di bawah ini:</div>
      <input type="file" accept=".json,application/json" class="finput" onchange="importAllJSON(this)">
      <textarea id="jsonRestoreBox" class="finput" rows="7" style="font-family:monospace;font-size:11.5px" placeholder='Tempel isi backup JSON di sini...'></textarea>
      <button class="btn-save" style="margin-top:8px" onclick="restoreJsonText()">Pulihkan dari Teks JSON</button>
    </div></div>`;
  document.body.appendChild(ov);ov.addEventListener('click',e=>{if(e.target===ov)ov.remove();});
}
function restoreJsonText(){
  const el=document.getElementById('jsonRestoreBox');if(!el||!el.value.trim()){toast('Tempel teks JSON dulu');return;}
  try{
    const obj=JSON.parse(el.value);
    applyStateObj(obj);pushToHosting(true);
    const ov=document.getElementById('jsonOv');if(ov)ov.remove();
    toast('Data backup berhasil dipulihkan ✓');applyRoleUI();go('setting');
  }catch(e){toast('Format JSON tidak valid');}
}
function importAllJSON(input){
  const f=input.files&&input.files[0];if(!f)return;
  const r=new FileReader();
  r.onload=()=>{
    try{
      const obj=JSON.parse(r.result);
      applyStateObj(obj);pushToHosting(true);
      toast('Data backup berhasil dipulihkan ✓');applyRoleUI();go('setting');
    }catch(e){toast('File JSON tidak valid');}
  };
  r.readAsText(f);
}
function saveFbConfig(){
  const url=(document.getElementById('fb_url').value||'').trim().replace(/\/+$/,'');
  const secret=(document.getElementById('fb_sec').value||'').trim();
  save('fbConfig',{url,secret});toast('Konfigurasi Firebase disimpan ✓');
}
async function pushToFirebase(){
  const cfg=store('fbConfig',{});
  if(!cfg.url){toast('Isi URL Firebase Realtime Database dulu');return;}
  const dump=collectStateObj();dump._updatedAt=new Date().toISOString();
  const ep=cfg.url+'/havist_db.json'+(cfg.secret?'?auth='+encodeURIComponent(cfg.secret):'');
  try{
    const res=await fetch(ep,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(dump)});
    if(!res.ok)throw new Error('HTTP '+res.status);
    toast('Data berhasil di-Push ke Firebase ✓');
  }catch(e){toast('Gagal Push ke Firebase: '+e.message);}
}
async function pullFromFirebase(){
  const cfg=store('fbConfig',{});
  if(!cfg.url){toast('Isi URL Firebase Realtime Database dulu');return;}
  const ep=cfg.url+'/havist_db.json'+(cfg.secret?'?auth='+encodeURIComponent(cfg.secret):'');
  try{
    const res=await fetch(ep);if(!res.ok)throw new Error('HTTP '+res.status);
    const obj=await res.json();if(!obj||typeof obj!=='object'){toast('Database Firebase masih kosong');return;}
    applyStateObj(obj);pushToHosting(true);
    toast('Data berhasil ditarik dari Firebase ✓');applyRoleUI();go('setting');
  }catch(e){toast('Gagal tarik dari Firebase: '+e.message);}
}
function vSetting(){
  const info=store('info',{nama:'Havist Traveller',hp:'0895 3385 99354',email:'kalabyentertainment@gmail.com',alamat:'Komplek Keluarga Besar H. Mamat, Ds. Kadu, Kec. Curug, Kab. Tangerang'});
  const markup=store('markup',20);
  // destinations for price editing
  const dset={};DATA.trips.forEach(t=>{const d=t.dest.split('(')[0].trim();if(d&&d!=='-')dset[d]=(dset[d]||0)+1;});
  const topDest=Object.entries(dset).sort((a,b)=>b[1]-a[1]).slice(0,8);
  const prices=store('prices',{});
  const priceRows=topDest.map(([d])=>`<tr><td style="font-weight:600">${esc(d)}</td><td style="width:180px"><div style="display:flex;align-items:center;gap:6px"><span style="color:var(--muted);font-size:13px">Rp</span><input class="finput" style="margin:0;padding:8px 10px" type="number" value="${prices[d]||''}" placeholder="Harga publish" data-dest="${esc(d)}" oninput="savePrice(this)"></div></td></tr>`).join('');
  return `<div class="hello fade"><h1>Setting Web</h1><p>Info perusahaan, harga paket, dan konten area Umum</p></div>
  <div class="grid fade" style="grid-template-columns:1fr 1fr">
    <div class="panel" style="margin:0"><div class="panel-h"><h3>Info Perusahaan</h3></div><div style="padding:16px 19px">
      <label class="flbl">Nama</label><input id="s_nama" class="finput" value="${esc(info.nama)}">
      <label class="flbl">No. HP / WA</label><input id="s_hp" class="finput" value="${esc(info.hp)}">
      <label class="flbl">Email</label><input id="s_email" class="finput" value="${esc(info.email)}">
      <label class="flbl">Alamat</label><textarea id="s_alamat" class="finput" rows="2">${esc(info.alamat)}</textarea>
      <label class="flbl">Rekening pembayaran (tampil di invoice)</label><input id="s_rek" class="finput" value="${esc(info.rek||'')}" placeholder="mis. BCA 1234567890 a/n Havist Traveller">
      <button class="btn-save" onclick="saveInfo()">Simpan Info</button>
    </div></div>
    <div>
      <div class="panel" style="margin-bottom:22px"><div class="panel-h"><h3>Margin Harga</h3></div><div style="padding:16px 19px">
        <label class="flbl">Markup default (%) untuk estimasi paket</label>
        <div style="display:flex;align-items:center;gap:14px"><input id="s_markup" class="finput" style="margin:0" type="range" min="0" max="50" value="${markup}" oninput="document.getElementById('mkv').textContent=this.value+'%'"><span id="mkv" style="font-weight:800;font-size:18px;color:var(--blue);width:52px">${markup}%</span></div>
        <label class="flbl" style="margin-top:12px">Target laba per bulan (Rp)</label><input id="s_target" class="finput" type="number" value="${store('target',100000000)}">
        <button class="btn-save" onclick="saveMarkup()">Simpan</button>
      </div></div>
      <div class="panel" style="margin:0"><div class="panel-h"><h3>Konten Area Umum</h3></div><div style="padding:16px 19px">
        <label class="chk"><input type="checkbox" checked onchange="toast('Pengaturan disimpan')"> Tampilkan banner promo</label>
        <label class="chk"><input type="checkbox" checked onchange="toast('Pengaturan disimpan')"> Tampilkan katalog destinasi</label>
        <label class="chk"><input type="checkbox" onchange="toast('Pengaturan disimpan')"> Tampilkan harga ke pengunjung</label>
        <label class="chk"><input type="checkbox" checked onchange="toast('Pengaturan disimpan')"> Aktifkan form pemesanan</label>
      </div></div>
    </div>
  </div>
  <div class="panel fade" style="margin-top:22px"><div class="panel-h"><h3>Foto Landing Page, Thumbnail &amp; Testimoni</h3><span style="font-size:12px;color:var(--muted)">Bisa isi path GitHub (mis. assets/foto/ciletuh.jpg), URL, atau upload langsung</span></div>
    <div style="padding:16px 19px">
      <label class="flbl">Foto Banner Hero Utama</label>
      <div style="display:flex;gap:8px;align-items:center;margin-bottom:14px">
        <input id="up_hero" class="finput" style="margin:0;flex:1" value="${esc(umumPhotos().hero||'')}" placeholder="assets/hero.jpg atau https://..." onchange="saveUmumHero(this.value)">
        <label class="btn-acc ok" style="cursor:pointer;white-space:nowrap">Upload Foto<input type="file" accept="image/*" style="display:none" onchange="uploadUmumFile(this,'hero')"></label>
      </div>
      <label class="flbl">Foto 4 Paket Unggulan di Beranda</label>
      <div class="tbl-scroll"><table style="margin-bottom:16px"><thead><tr><th>Paket Beranda</th><th>Daerah</th><th>URL / Path GitHub / Upload Foto</th></tr></thead><tbody>
        ${UMUM_BEST_PKGS.map(pk=>{const key=pk.dests[0]||pk.title;const val=(umumPhotos().dest||{})[key]||'';return `<tr><td style="font-weight:700">${esc(pk.title)}</td><td><span class="pill jadwal">${esc(pk.city)}</span></td><td><div style="display:flex;gap:6px;align-items:center">${val?`<img src="${esc(val)}" style="width:42px;height:28px;object-fit:cover;border-radius:6px;border:1px solid var(--line)">`:''}<input class="finput" style="margin:0;padding:6px 9px;font-size:12px;flex:1" value="${esc(val)}" placeholder="https://... atau upload foto" onchange="saveUmumDestPhoto('${esc(key)}',this.value)"><label class="btn-acc ok" style="cursor:pointer;font-size:11px;padding:6px 10px;white-space:nowrap">Upload<input type="file" accept="image/*" style="display:none" onchange="uploadUmumFile(this,'dest','${esc(key)}')"></label></div></td></tr>`;}).join('')}
      </tbody></table></div>
      <label class="flbl">Tambah / Ganti Foto Objek Wisata (Semua 122 Destinasi Katalog)</label>
      <div class="frow" style="grid-template-columns:1.2fr 1.4fr auto auto;gap:8px;align-items:end;margin-top:6px;margin-bottom:12px">
        <div>
          <label class="flbl" style="font-size:11px">Pilih Objek Wisata</label>
          <select id="sp_dest_key" class="finput" style="margin:0">
            ${[...new Set(CAT.dests.map(d=>d.city))].map(c=>`<optgroup label="${esc(c)}">${CAT.dests.filter(d=>d.city===c).map(d=>{const disp=destDisplayName(d);return `<option value="${esc(disp)}">${esc(disp)}</option>`;}).join('')}</optgroup>`).join('')}
          </select>
        </div>
        <div>
          <label class="flbl" style="font-size:11px">Link URL Foto / Path GitHub</label>
          <input id="sp_dest_url" class="finput" style="margin:0" placeholder="https://... atau klik Upload Foto">
        </div>
        <button class="btn-save" style="margin:0;white-space:nowrap;width:auto" onclick="savePickedDestPhoto()">Simpan URL</button>
        <label class="btn-acc ok" style="cursor:pointer;padding:10px 14px;white-space:nowrap;display:inline-flex;align-items:center">📷 Upload Foto<input type="file" accept="image/*" style="display:none" onchange="uploadPickedDestPhoto(this)"></label>
      </div>
      ${Object.keys(umumPhotos().dest||{}).filter(k=>(umumPhotos().dest||{})[k]).length?`<div class="tbl-scroll"><table style="margin-bottom:14px"><thead><tr><th>Destinasi yang Sudah Ada Fotonya</th><th>Pratinjau</th><th style="text-align:right">Aksi</th></tr></thead><tbody>
        ${Object.entries(umumPhotos().dest||{}).filter(([,v])=>v).map(([k,v])=>`<tr><td style="font-weight:600">${esc(k)}</td><td><img src="${esc(v)}" style="width:56px;height:36px;object-fit:cover;border-radius:6px;border:1px solid var(--line)"></td><td style="text-align:right"><button class="pay-del" onclick="saveUmumDestPhoto('${esc(k).replace(/'/g,"\'")}','');go('setting')">✕ Hapus Foto</button></td></tr>`).join('')}
      </tbody></table></div>`:'<div style="font-size:12px;color:var(--muted);margin-bottom:14px">Belum ada foto destinasi kustom yang diunggah. Pilih objek wisata di atas lalu klik <b>📷 Upload Foto</b>.</div>'}
      <label class="flbl">Tambah Testimoni Asli (Instagram / WhatsApp / Sekolah)</label>
      <div class="frow" style="grid-template-columns:1fr 1fr 1.6fr 1fr auto;gap:8px;align-items:end">
        <div><input id="ut_name" class="finput" style="margin:0" placeholder="Nama / Instansi"></div>
        <div><input id="ut_src" class="finput" style="margin:0" placeholder="Sumber (IG/WA)"></div>
        <div><input id="ut_quote" class="finput" style="margin:0" placeholder="Isi testimoni..."></div>
        <div><input id="ut_foto" class="finput" style="margin:0" placeholder="URL foto (opsional)"></div>
        <button class="btn-save" style="margin:0;white-space:nowrap" onclick="addUmumTesti()">+ Tambah</button>
      </div>
      ${(umumPhotos().testi||[]).length?`<div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">${(umumPhotos().testi||[]).map((t,i)=>`<span class="pill lunas" style="gap:6px">${esc(t.name)}: “${esc(t.quote.slice(0,28))}…” <button class="pay-del" onclick="delUmumTesti(${i})">✕</button></span>`).join('')}</div>`:''}
    </div>
  </div>
  <div class="panel fade" style="margin-top:22px"><div class="panel-h"><h3>Backup JSON &amp; Sinkronisasi Cloud (Firebase)</h3><span style="font-size:12px;color:var(--muted)">Untuk sinkron antar perangkat &amp; cadangan data</span></div>
    <div style="padding:16px 19px">
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px">
        <button class="btn-acc ok" style="padding:9px 14px" onclick="pushToHosting(false)">☁ Simpan ke Server Hosting (api.php)</button>
        <button class="btn-acc no" style="padding:9px 14px" onclick="pullFromHosting(false)">↻ Muat dari Server Hosting</button>
        <button class="btn-acc ok" style="padding:9px 14px" onclick="exportAllJSON()">⬇ Unduh / Salin Backup JSON</button>
        <button class="btn-acc no" style="padding:9px 14px" onclick="openRestoreJsonModal()">⬆ Pulihkan dari JSON</button>
      </div>
      <div class="frow" style="grid-template-columns:1.6fr 1fr auto;gap:8px;align-items:end">
        <div><label class="flbl">URL Firebase Realtime Database</label><input id="fb_url" class="finput" style="margin:0" value="${esc((store('fbConfig',{}).url)||'')}" placeholder="https://project-id-default-rtdb.asia-southeast1.firebasedatabase.app"></div>
        <div><label class="flbl">Database Secret / Token (opsional)</label><input id="fb_sec" class="finput" style="margin:0" type="password" value="${esc((store('fbConfig',{}).secret)||'')}" placeholder="Opsional"></div>
        <button class="btn-save" style="margin:0;white-space:nowrap" onclick="saveFbConfig()">Simpan Koneksi</button>
      </div>
      <div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap">
        <button class="btn-acc ok" onclick="pushToFirebase()">⬆ Push Data ke Firebase</button>
        <button class="btn-acc no" onclick="pullFromFirebase()">⬇ Tarik Data dari Firebase</button>
      </div>
    </div>
  </div>
  <div class="panel fade" style="margin-top:22px"><div class="panel-h"><h3>Manajemen Akun Staf (5 Peran)</h3><span style="font-size:12px;color:var(--muted)">Owner · Admin Operasional · Sales · TL/Media · Publik</span></div>
    <div style="padding:16px 19px">
      <div class="frow" style="grid-template-columns:1fr 1.2fr 1fr 1fr auto;align-items:end;gap:8px">
        <div><label class="flbl">Peran</label><select id="na_role" class="finput" style="margin:0"><option value="admin">Admin Operasional</option><option value="sales">Sales</option><option value="tl">Tour Leader &amp; Media</option><option value="owner">Owner / Management</option></select></div>
        <div><label class="flbl">Nama Staf</label><input id="na_nama" class="finput" style="margin:0" placeholder="mis. Nadia / Bayu"></div>
        <div><label class="flbl">Username</label><input id="na_user" class="finput" style="margin:0" placeholder="mis. nadia"></div>
        <div><label class="flbl">PIN / Password</label><input id="na_pin" class="finput" style="margin:0" placeholder="mis. 1234"></div>
        <button class="btn-save" style="margin:0;white-space:nowrap" onclick="addStaffAccount()">+ Buat Akun</button>
      </div>
      <div class="tbl-scroll"><table style="margin-top:14px"><thead><tr><th>Nama</th><th>Username</th><th>Peran</th><th>PIN</th><th>Status</th><th style="text-align:right">Aksi</th></tr></thead>
        <tbody>${accounts().map(a=>`<tr><td style="font-weight:700">${esc(a.nama)}</td><td class="mono">${esc(a.username)}</td><td><span class="pill ${a.role==='owner'?'lunas':(a.role==='admin'?'dp':'jadwal')}">${esc(ROLE_CFG[a.role]?.lbl||a.role)}</span></td><td class="mono">${esc(a.pin)}</td><td>${a.active!==false?'<span class="pill lunas">Aktif</span>':'<span class="pill piutang">Nonaktif</span>'}</td><td style="text-align:right;white-space:nowrap"><button class="btn-acc no" onclick="toggleAccActive('${a.id}')">${a.active!==false?'Nonaktifkan':'Aktifkan'}</button> <button class="pay-del" onclick="deleteAcc('${a.id}')">✕</button></td></tr>`).join('')}</tbody>
      </table></div>
    </div>
  </div>
  <div class="panel fade" style="margin-top:22px"><div class="panel-h"><h3>Harga Publish per Destinasi</h3><span style="font-size:12px;color:var(--muted)">tersimpan otomatis</span></div><div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Destinasi</th><th>Harga Publish (per pax)</th></tr></thead><tbody>${priceRows}</tbody></table></div></div>`;
}
function saveInfo(){const g=i=>document.getElementById(i);const info={nama:g('s_nama').value,hp:g('s_hp').value,email:g('s_email').value,alamat:g('s_alamat').value,rek:g('s_rek')?g('s_rek').value:''};save('info',info);toast('Info perusahaan disimpan');}
function saveMarkup(){save('markup',parseInt(document.getElementById('s_markup').value)||0);const tg=document.getElementById('s_target');if(tg)save('target',parseInt(tg.value)||0);toast('Pengaturan disimpan');}
function savePrice(el){const p=store('prices',{});p[el.dataset.dest]=parseInt(el.value)||0;save('prices',p);}

function openTrip(id){openTripDetail(id);}

// ===== LAPORAN PERIODIK & ARSIP TRIP =====
let lapTab='rekap',lapPeriode='3',arsipQ='',arsipPage=1;
function setArsipPage(p){arsipPage=p;renderLap();}
const PERIODE={'1':'Bulan Ini','3':'3 Bulan','6':'6 Bulan','12':'1 Tahun','all':'Semua'};
function periodeMulai(p){if(p==='all')return new Date('2000-01-01');const d=new Date(today.getFullYear(),today.getMonth(),1);d.setMonth(d.getMonth()-(+p-1));return d;}
function tripsPeriode(p){const m=periodeMulai(p);return allTrips().filter(t=>{if(!t.brk)return false;const b=new Date(t.brk);return b>=m&&b<=new Date(today.getFullYear(),today.getMonth()+1,0,23,59,59);});}
function rekapPeriode(p){
  const ts=tripsPeriode(p);let pax=0,laba=0,tagih=0,bayar=0;
  ts.forEach(t=>{pax+=t.pax||0;laba+=t.laba||0;const pi=piutMap()[t.id];if(pi){tagih+=pi.tagih||0;bayar+=clientPaid(pi);}});
  const gaji=ts.reduce((s,t)=>s+tripGaji(t),0);
  const vendor=ts.reduce((s,t)=>s+prepTotal(t.id),0);
  return{n:ts.length,pax,laba,tagih,bayar,sisa:Math.max(0,tagih-bayar),gaji,vendor,bersih:laba-gaji,trips:ts};
}
function bulanKunci(d){const y=d.getFullYear(),mo=d.getMonth();return y+'-'+String(mo+1).padStart(2,'0');}
const BLN=['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des'];
function trenBulanan(n){
  const out=[];
  for(let i=n-1;i>=0;i--){const d=new Date(today.getFullYear(),today.getMonth()-i,1);const k=bulanKunci(d);
    let trip=0,pax=0,laba=0;
    allTrips().forEach(t=>{if(t.brk&&bulanKunci(new Date(t.brk))===k){trip++;pax+=t.pax||0;laba+=t.laba||0;}});
    out.push({k,lbl:BLN[d.getMonth()],thn:d.getFullYear(),trip,pax,laba});}
  return out;
}
function setLapTab(k){lapTab=k;const nav=document.querySelector('#view .tabs');if(nav)nav.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.lt===k));renderLap();}
function setPeriode(p){lapPeriode=p;const s=document.getElementById('lapPeriode');if(s)s.value=p;renderLap();}
function setArsipQ(v){arsipQ=v;arsipPage=1;renderLap();}
function renderLap(){const b=document.getElementById('lapBody');if(!b)return;b.innerHTML=lapTab==='arsip'?lapArsip():lapRekap();
  if(lapTab==='arsip'){const q=document.getElementById('arsipSearch');if(q){q.value=arsipQ;if(arsipQ)q.focus();}}}
function vLaporan(){
  const tabs=[['rekap','Rekap Periodik'],['arsip','Arsip Trip']];
  const nav=tabs.map(([k,l])=>`<button class="tab ${lapTab===k?'active':''}" data-lt="${k}" onclick="setLapTab('${k}')">${l}</button>`).join('');
  return `<div class="hello fade"><h1>Laporan</h1><p>Rekap kinerja per periode dan arsip trip yang sudah selesai</p></div>
    <div class="tabs fade">${nav}</div><div id="lapBody"></div>`;
}
function lapRekap(){
  const r=rekapPeriode(lapPeriode);
  const tren=trenBulanan(6);
  const mx=Math.max(1,...tren.map(x=>x.laba))*1.1;
  const bars=tren.map((x,i)=>{const prev=i>0?tren[i-1].laba:null;const naik=prev!==null&&x.laba>prev;const turun=prev!==null&&x.laba<prev;
    const ini=i===tren.length-1;
    return `<div class="bar${ini?' hl':''}" onclick="toast('${x.lbl} ${x.thn}: ${x.trip} trip, ${x.pax} pax, laba ${jt(x.laba)}')"><div class="col" style="height:${x.laba/mx*100}%"><span class="tip">${jt(x.laba)}</span></div><span>${x.lbl}${prev!==null?(naik?' ▲':turun?' ▼':''):''}</span></div>`;}).join('');
  const rows=tren.slice().reverse().map((x,i,arr)=>{const prev=arr[i+1];
    const d=prev&&prev.laba>0?Math.round((x.laba-prev.laba)/prev.laba*100):null;
    return `<tr><td style="font-weight:700">${x.lbl} ${x.thn}</td><td class="mono">${x.trip}</td><td class="mono">${x.pax}</td><td class="price mono">${x.laba?jt(x.laba):'—'}</td>
      <td>${d===null?'<span style="color:var(--muted-2)">—</span>':`<span style="color:${d>=0?'var(--green)':'var(--red)'};font-weight:700">${d>=0?'▲ +':'▼ '}${d}%</span>`}</td></tr>`;}).join('');
  const marg=r.laba>0?Math.round(r.bersih/r.laba*100):0;
  return `<div class="cat-bar fade" style="padding:0 0 4px">
      <div><label class="flbl" style="display:inline;margin-right:8px">Periode</label>
        <select id="lapPeriode" class="finput" style="width:auto;display:inline-block;margin:0;padding:8px 12px" onchange="setPeriode(this.value)">
          ${Object.entries(PERIODE).map(([k,l])=>`<option value="${k}" ${lapPeriode===k?'selected':''}>${l}</option>`).join('')}</select></div>
      <button class="btn-acc ok" style="margin-right:8px" onclick="genLaporanPDF()">⬇ Unduh Laporan PDF</button>
      <button class="btn-acc ok" onclick="exportLapRekapExcel()">⬇ Export Excel</button></div>
    <div class="cards fade" style="grid-template-columns:repeat(4,1fr)">
      <div class="scard"><div class="ic b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg></div><div class="lbl">Total Trip</div><div class="val mono">${r.n}</div><div class="sub" style="color:var(--muted)">${r.pax.toLocaleString('id-ID')} peserta</div></div>
      <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div><div class="lbl">Laba Kotor</div><div class="val mono">${jt(r.laba)}</div><div class="sub" style="color:var(--muted)">${r.n?jt(Math.round(r.laba/r.n))+' / trip':'—'}</div></div>
      <div class="scard"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 17l6-6 4 4 7-7"/></svg></div><div class="lbl">Laba Bersih (− gaji crew)</div><div class="val mono">${jt(r.bersih)}</div><div class="sub ${marg>=0?'up':'down'}">margin ${marg}%</div></div>
      <div class="scard" onclick="go('keuangan');setTimeout(()=>setKeuTab('pelunasan'),40)" style="cursor:pointer"><div class="ic r"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div class="lbl">Belum Tertagih</div><div class="val mono">${jt(r.sisa)}</div><div class="sub" style="color:var(--muted)">dari ${jt(r.tagih)} ditagihkan</div></div>
    </div>
    <div class="grid fade" style="grid-template-columns:1fr 1fr">
      <div class="panel" style="margin:0"><div class="panel-h"><h3>Tren Laba 6 Bulan</h3><span style="font-size:12px;color:var(--muted)">klik batang untuk rincian</span></div><div class="chart" style="margin-top:14px">${bars}</div></div>
      <div class="panel" style="margin:0"><div class="panel-h"><h3>Perbandingan Bulan ke Bulan</h3></div>
        <div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Bulan</th><th>Trip</th><th>Pax</th><th>Laba</th><th>vs Bulan Lalu</th></tr></thead><tbody>${rows}</tbody></table></div></div>
    </div>
    <div class="panel fade" style="margin:0"><div class="panel-h"><h3>Rincian Periode — ${PERIODE[lapPeriode]}</h3></div>
      <div class="tbl-scroll"><table style="margin-top:12px"><tbody>
        <tr><td>Jumlah trip</td><td class="mono" style="text-align:right;font-weight:700">${r.n}</td></tr>
        <tr><td>Total peserta</td><td class="mono" style="text-align:right;font-weight:700">${r.pax.toLocaleString('id-ID')} pax</td></tr>
        <tr><td>Laba kotor</td><td class="price mono" style="text-align:right">${jt(r.laba)}</td></tr>
        <tr><td>Biaya vendor tercatat</td><td class="mono" style="text-align:right">${r.vendor?jt(r.vendor):'—'}</td></tr>
        <tr><td>Gaji crew</td><td class="mono" style="text-align:right;color:var(--red)">− ${jt(r.gaji)}</td></tr>
        <tr style="border-top:2px solid var(--line2,#e3e6ec)"><td style="font-weight:800">Laba bersih</td><td class="price mono" style="text-align:right;font-weight:800">${jt(r.bersih)}</td></tr>
      </tbody></table></div></div>`;
}
function arsipTrips(){
  const q=arsipQ.trim().toLowerCase();
  return allTrips().filter(t=>t.brk&&tripStatus(t)==='selesai')
    .filter(t=>!q||String(t.inst||'').toLowerCase().includes(q)||String(t.dest||'').toLowerCase().includes(q)||String(t.jenis||'').toLowerCase().includes(q))
    .sort((a,b)=>a.brk<b.brk?1:-1);
}
function lapArsip(){
  const ts=arsipTrips();
  const pax=ts.reduce((s,t)=>s+(t.pax||0),0),laba=ts.reduce((s,t)=>s+(t.laba||0),0);
  const PER=20;const pageTs=pageSlice(ts,arsipPage,PER);
  const rows=pageTs.map(t=>{const pi=piutMap()[t.id];const[pc,pl]=payStatus(t);const tl=tripCrewNames(t.id,'tl')[0];
    return `<tr class="clk" onclick="openTripDetail('${t.id}')"><td><div class="nm" style="font-weight:700">${esc(t.inst)}</div><div class="loc" style="font-size:11px;color:var(--muted)">${esc(String(t.dest||'').split('(')[0]).slice(0,38)}</div></td>
      <td style="font-size:12.5px">${dateID(t.brk)}</td><td class="mono">${t.pax||0}</td><td class="mono">${tripDays(t)} hr</td>
      <td style="font-size:12px">${tl?esc(tl.nama):'<span style=color:var(--muted-2)>—</span>'}</td>
      <td class="price mono">${t.laba?jt(t.laba):'—'}</td><td><span class="pill ${pc}">${pl}</span></td>
      <td style="text-align:right" onclick="event.stopPropagation()"><button class="btn-acc no" onclick="genRundownPDF('${t.id}')">⬇</button></td></tr>`;}).join('');
  return `<div class="cards fade" style="grid-template-columns:repeat(3,1fr)">
      <div class="scard"><div class="ic b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 8v13H3V8M1 3h22v5H1zM10 12h4"/></svg></div><div class="lbl">Trip Selesai</div><div class="val mono">${ts.length}</div><div class="sub" style="color:var(--muted)">${arsipQ?'hasil pencarian':'seluruh arsip'}</div></div>
      <div class="scard"><div class="ic gr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/></svg></div><div class="lbl">Total Peserta Terlayani</div><div class="val mono">${pax.toLocaleString('id-ID')}</div></div>
      <div class="scard"><div class="ic g"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div><div class="lbl">Total Laba Arsip</div><div class="val mono">${jt(laba)}</div></div>
    </div>
    <div class="panel fade" style="margin:0"><div class="panel-h"><h3>Arsip Trip Selesai</h3>
      <div style="display:flex;align-items:center;gap:8px"><input id="arsipSearch" class="finput" style="width:220px;margin:0;padding:8px 12px" placeholder="Cari instansi / daerah..." oninput="setArsipQ(this.value)"><button class="btn-acc ok" onclick="exportArsipExcel()">⬇ Export Excel</button></div></div>
      <div class="tbl-scroll"><table style="margin-top:12px"><thead><tr><th>Instansi</th><th>Tanggal</th><th>Pax</th><th>Durasi</th><th>Tour Leader</th><th>Laba</th><th>Pembayaran</th><th style="text-align:right">Rundown</th></tr></thead>
      <tbody>${rows||`<tr><td colspan="8" style="color:var(--muted);font-size:12.5px">${arsipQ?'Tidak ada trip yang cocok dengan "'+esc(arsipQ)+'".':'Belum ada trip yang selesai.'}</td></tr>`}</tbody></table></div>
      ${pagerHTML(ts.length,arsipPage,PER,'setArsipPage')}
      <p style="font-size:11.5px;color:var(--muted-2);margin-top:12px">Klik baris untuk melihat rekap lengkap trip (crew, pembayaran, persiapan vendor, checklist).</p></div>`;
}
function exportLapRekapExcel(){
  if(!window.XLSX){toast('Gagal memuat modul Excel, coba lagi');return;}
  const r=rekapPeriode(lapPeriode);const tren=trenBulanan(12);
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsStampRow('REKAP PERIODIK — '+PERIODE[lapPeriode]).concat([
    ['Jumlah trip',r.n],['Total peserta',r.pax],['Laba kotor (Rp)',r.laba],['Biaya vendor tercatat (Rp)',r.vendor],
    ['Gaji crew (Rp)',r.gaji],['Laba bersih (Rp)',r.bersih],['Total ditagihkan (Rp)',r.tagih],['Belum tertagih (Rp)',r.sisa]])),'Rincian Periode');
  const trenRows=[['Bulan','Tahun','Jumlah Trip','Pax','Laba (Rp)']];
  tren.forEach(x=>trenRows.push([x.lbl,x.thn,x.trip,x.pax,x.laba]));
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(trenRows),'Tren Bulanan');
  XLSX.writeFile(wb,'Havist_RekapPeriodik_'+xlsxStamp()+'.xlsx');
  toast('Rekap Periodik diekspor ke Excel');
}
function exportArsipExcel(){
  if(!window.XLSX){toast('Gagal memuat modul Excel, coba lagi');return;}
  const ts=arsipTrips();
  const pax=ts.reduce((s,t)=>s+(t.pax||0),0),laba=ts.reduce((s,t)=>s+(t.laba||0),0);
  const rows=[['Instansi','Tanggal','Pax','Durasi (hari)','Tour Leader','Laba (Rp)','Status Pembayaran']];
  ts.forEach(t=>{const tl=tripCrewNames(t.id,'tl')[0];const[,pl]=payStatus(t);
    rows.push([t.inst,dateID(t.brk),t.pax||0,tripDays(t),tl?tl.nama:'-',t.laba||0,pl]);
  });
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(xlsStampRow('ARSIP TRIP SELESAI').concat([['Jumlah trip selesai',ts.length],['Total peserta terlayani',pax],['Total laba arsip (Rp)',laba]])),'Ringkasan');
  XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(rows),'Arsip Trip');
  XLSX.writeFile(wb,'Havist_ArsipTrip_'+xlsxStamp()+'.xlsx');
  toast('Arsip Trip diekspor ke Excel');
}
async function genLaporanPDF(){
  if(!window.jspdf){toast('Pustaka PDF belum siap, coba lagi');return;}
  const r=rekapPeriode(lapPeriode);const tren=trenBulanan(6);
  const K=pdfKit('LAPORAN KINERJA');const{doc,L,R,GREY,NAVY}=K;
  K.txt('Periode: '+PERIODE[lapPeriode]+'   ·   Dicetak '+new Date().toLocaleDateString('id-ID',{day:'numeric',month:'long',year:'numeric'}),L,{s:9,c:GREY});K.y+=3;
  K.section('Ringkasan Periode');
  K.kv('Jumlah Trip',r.n+' trip');K.kv('Total Peserta',r.pax.toLocaleString('id-ID')+' pax');
  K.kv('Laba Kotor',rp(r.laba));K.kv('Biaya Vendor',r.vendor?rp(r.vendor):'belum dicatat');
  K.kv('Gaji Crew',rp(r.gaji));K.kv('Laba Bersih',rp(r.bersih));
  K.kv('Ditagihkan',rp(r.tagih));K.kv('Sudah Dibayar',rp(r.bayar));K.kv('Belum Tertagih',rp(r.sisa));
  K.y+=3;K.section('Tren 6 Bulan Terakhir');
  K.rowAmt('Bulan','Trip / Pax / Laba',{b:true,s:9.5});K.hr();
  tren.slice().reverse().forEach(x=>K.rowAmt(x.lbl+' '+x.thn,x.trip+' trip / '+x.pax+' pax / '+rp(x.laba),{s:9.5}));
  K.y+=3;K.section('Daftar Trip Periode Ini');
  if(r.trips.length)r.trips.slice().sort((a,b)=>a.brk<b.brk?1:-1).forEach(t=>K.rowAmt(String(t.inst).slice(0,46)+'  ('+dateID(t.brk)+')',(t.pax||0)+' pax · '+rp(t.laba||0),{s:9}));
  else K.txt('Tidak ada trip pada periode ini.',L+2,{s:9.5,c:GREY});
  K.y+=5;K.txt('Dibuat otomatis dari data Management Havist Traveller.',L,{s:8.5,c:GREY});
  await pdfSave(doc,'Laporan-'+PERIODE[lapPeriode].replace(/\s+/g,'-')+'.pdf');
}
const VIEWS={umum:vUmum,dashboard:vDashboard,keuangan:vKeuangan,katalog:vKatalog,acc:vACC,jadwal:vJadwal,crew:vCrew,tl:vTL,sales:vSales,laporan:vLaporan,setting:vSetting};
function go(name){
  if(!VIEWS[name])name='dashboard';
  if(!canView(name)){
    const fallback=roleCfg().views.includes('dashboard')?'dashboard':(roleCfg().views[0]||'umum');
    name=fallback;
  }
  document.querySelectorAll('#nav a').forEach(a=>a.classList.toggle('active',a.dataset.view===name));
  document.querySelectorAll('#bottomnav a').forEach(a=>a.classList.toggle('active',a.dataset.view===name));
  closeSheet();
  const sh=document.querySelector('.app');if(sh)sh.classList.toggle('public-mode',name==='umum');document.getElementById('view').innerHTML=VIEWS[name]();
  if(name==='dashboard'){buildCal();initChartTabs();}
  if(name==='katalog'){renderKat();}
  if(name==='keuangan'){renderKeu();}
  if(name==='crew'){renderCrew();}
  if(name==='jadwal'){renderJadwalBody();}
  if(name==='laporan'){renderLap();}
  if(name==='sales'){renderSales();}
  if(name==='tl'){renderTL();}
  if(name==='umum'){renderUmum();}
  if(location.hash.slice(1)!==name)history.replaceState(null,'','#'+name);
  window.scrollTo(0,0);
}
function monthCashAgg(){
  const m={};MONTHS.forEach(k=>m[k]={in:0,out:0});
  allPiutang().forEach(p=>{const k=tripPeriode(p);if(m[k])m[k].in+=clientPaid(p);});
  allVendor().forEach(d=>{const k=d.tgl&&d.tgl!=='-'?tripPeriode({brk:d.tgl}):'';if(m[k])m[k].out+=vendorPaid(d);});
  allTrips().forEach(t=>{const k=tripPeriode(t);if(m[k])m[k].out+=tripGaji(t);});
  return m;
}
function initChartTabs(){
  const tabs=document.getElementById('chartTabs');if(!tabs)return;
  const m=monthAgg(),cm=monthCashAgg();
  const rec=['2026-07 Juli','2026-08 Agustus','2026-09 September','2026-10 Oktober','2026-11 November'];
  const keys=['laba','aruskas','pax','bus'];
  tabs.querySelectorAll('.tab').forEach((b,idx)=>b.onclick=()=>{
    tabs.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));b.classList.add('active');
    const key=keys[idx];
    if(key==='aruskas'){
      const mx=Math.max(1,...rec.map(k=>Math.max(cm[k].in,cm[k].out)))*1.08;
      document.getElementById('chart').innerHTML=rec.map(k=>{
        const vi=cm[k].in,vo=cm[k].out,hi=vi/mx*100,ho=vo/mx*100,hl=k.includes('November')?' hl':'';
        return `<div class="bar${hl}" onclick="toast('${MLBL[k]}: Masuk ${jt(vi)} · Keluar ${jt(vo)}')"><div style="display:flex;gap:3px;align-items:flex-end;height:100%;width:100%;justify-content:center"><div class="col" style="height:${hi}%;width:42%;background:var(--green)"><span class="tip">Masuk ${jt(vi)}</span></div><div class="col" style="height:${ho}%;width:42%;background:var(--red)"><span class="tip">Keluar ${jt(vo)}</span></div></div><span>${MLBL[k]}</span></div>`;
      }).join('');
      return;
    }
    const mx=Math.max(...rec.map(k=>m[k][key]))*1.08||1;
    document.getElementById('chart').innerHTML=rec.map(k=>{const v=m[k][key],h=v/mx*100,hl=k.includes('November')?' hl':'';const lab=key==='laba'?jt(v):v.toLocaleString('id-ID')+(key==='pax'?' pax':' bus');
      return `<div class="bar${hl}"><div class="col" style="height:${h}%"><span class="tip">${lab}</span></div><span>${MLBL[k]}</span></div>`;}).join('');
  });
}
// global search -> jump to jadwal and filter
document.getElementById('globalSearch').addEventListener('input',function(){
  const q=this.value.toLowerCase().trim();
  if(!q){if(document.getElementById('jadwalBody'))renderJadwalBody();return;}
  if(!document.getElementById('jadwalBody')){jadwalFilter='semua';go('jadwal');}
  const b=document.getElementById('jadwalBody');if(!b)return;
  b.querySelectorAll('.jcard').forEach(c=>{c.style.display=c.textContent.toLowerCase().includes(q)?'':'none';});
});
document.getElementById('nav').addEventListener('click',e=>{const a=e.target.closest('a');if(a)go(a.dataset.view);});
document.getElementById('bottomnav').addEventListener('click',e=>{const a=e.target.closest('a');if(a&&a.dataset.view)go(a.dataset.view);});
// --- bottom-nav "Lainnya" sheet (mobile) ---
const MORE_ITEMS=[
  ['keuangan','Keuangan','<path d="M3 10h18M7 15h4M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'],
  ['katalog','Harga &amp; Katalog','<path d="M20.6 8.4 12 3 3.4 8.4v7.2L12 21l8.6-5.4z"/><path d="M12 12 3.4 8.4M12 12v9M12 12l8.6-3.6"/>'],
  ['acc','ACC Klien','<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'],
  ['crew','Crew','<circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0M16 3.5a3.2 3.2 0 0 1 0 6M21 20a6 6 0 0 0-5-5.9"/>'],
  ['sales','Sales','<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'],
  ['laporan','Laporan','<path d="M4 19V5a2 2 0 0 1 2-2h9l5 5v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/><path d="M14 3v5h5M8 13h8M8 17h5"/>'],
  ['setting','Setting Web','<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1V21a2 2 0 1 1-4 0v-.1A1.6 1.6 0 0 0 6.8 19l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1A1.6 1.6 0 0 0 3 13.6H3a2 2 0 1 1 0-4h.1A1.6 1.6 0 0 0 4.6 7L4.5 7a2 2 0 1 1 2.8-2.8l.1.1A1.6 1.6 0 0 0 10 3.4V3a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 2.7 1.1l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0 1.1 2.7H21a2 2 0 1 1 0 4h-.1a1.6 1.6 0 0 0-1.5 1z"/>'],
];
function openMoreSheet(){
  closeSheet();
  const allowed=roleCfg().views.filter(v=>NAV_META[v]);
  const extra=allowed.length>5?allowed.slice(4):allowed;
  const items=extra.map(k=>`<a onclick="closeSheet();go('${k}')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor">${NAV_META[k][1]}</svg>${NAV_META[k][0]}</a>`).join('');
  const ov=document.createElement('div');ov.className='sheet-overlay';ov.id='moreSheet';
  ov.innerHTML=`<div class="sheet-modal"><div class="sheet-handle"></div><div class="sheet-title">Menu Lainnya (${esc(roleCfg().lbl)})</div>${items}</div>`;
  ov.addEventListener('click',e=>{if(e.target===ov)closeSheet();});
  document.body.appendChild(ov);
}
function closeSheet(){const s=document.getElementById('moreSheet');if(s)s.remove();}
// --- reusable pagination (Prev/Next + numbered pages + "Menampilkan X-Y dari Z") ---
function pageSlice(arr,page,per){const tp=Math.max(1,Math.ceil(arr.length/per));if(page>tp)page=tp;if(page<1)page=1;return arr.slice((page-1)*per,page*per);}
function pagerHTML(total,page,per,setFn){
  const tp=Math.max(1,Math.ceil(total/per));if(page>tp)page=tp;if(page<1)page=1;
  if(tp<=1)return '';
  const start=total===0?0:(page-1)*per+1,end=Math.min(page*per,total);
  let nums=[];
  if(tp<=7){for(let i=1;i<=tp;i++)nums.push(i);}
  else{nums.push(1);if(page>4)nums.push('…');
    for(let i=Math.max(2,page-1);i<=Math.min(tp-1,page+1);i++)nums.push(i);
    if(page<tp-3)nums.push('…');nums.push(tp);}
  const numHTML=nums.map(p=>p==='…'?`<span class="pg-dots">…</span>`:`<button class="pg-btn pg-num ${p===page?'active':''}" onclick="${setFn}(${p})">${p}</button>`).join('');
  return `<div class="pager"><span class="pg-info">Menampilkan ${start}-${end} dari ${total}</span>
    <div class="pg-nav"><button class="pg-btn" ${page<=1?'disabled':''} onclick="${setFn}(${page-1})" aria-label="Sebelumnya">‹</button>${numHTML}<button class="pg-btn" ${page>=tp?'disabled':''} onclick="${setFn}(${page+1})" aria-label="Berikutnya">›</button></div></div>`;
}
window.addEventListener('hashchange',()=>go(location.hash.slice(1)||'umum'));
go(location.hash.slice(1)||'umum');
</script>
</body>
</html>'''

html = html.replace("__DATA__", data).replace("__CATALOG__", catalog).replace("__LOGO__", logo)
open('index.html','w').write(html)
print("built", len(html))
