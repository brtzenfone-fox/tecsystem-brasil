def gerar_html(vagas, artigos):
    agora=datetime.now().strftime("%d/%m/%Y às %H:%M")
    cards_vagas="\n".join(gerar_card_vaga(v,i) for i,v in enumerate(vagas))
    cards_artigos="\n".join(gerar_card_artigo(a,i) for i,a in enumerate(artigos))
    total=len(vagas)
    opts_estados=gerar_opts_estados(vagas)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TecVagas — Vagas para Técnicos Industriais 2026</title>
<meta name="description" content="As melhores vagas para técnicos industriais do Brasil. Elétrica, Mecânica, Automação, Refrigeração, PLC, SCADA, HVAC e mais.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@700;800&display=swap" rel="stylesheet">

<style>
*{{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}}
:root{{
  --bg:#f6f8fc;
  --surface:#ffffff;
  --surface-2:#f1f5fb;
  --surface-3:#e9eef7;
  --line:#dbe4f0;
  --line-2:#c7d4e5;

  --text:#0f172a;
  --text-2:#334155;
  --muted:#64748b;
  --muted-2:#94a3b8;

  --navy:#0b1f3a;
  --navy-2:#102a4c;
  --navy-3:#16355f;
  --blue:#1d4ed8;
  --blue-2:#2563eb;
  --blue-3:#3b82f6;
  --blue-soft:#eff6ff;

  --green:#16a34a;
  --green-soft:#f0fdf4;
  --orange:#ea580c;
  --orange-soft:#fff7ed;
  --purple:#7c3aed;
  --purple-soft:#f5f3ff;
  --teal:#0f766e;
  --teal-soft:#f0fdfa;
  --yellow:#ca8a04;
  --yellow-soft:#fefce8;

  --danger:#dc2626;
  --danger-soft:#fef2f2;

  --shadow-sm:0 4px 16px rgba(15,23,42,.05);
  --shadow-md:0 10px 30px rgba(15,23,42,.08);
  --shadow-lg:0 22px 60px rgba(15,23,42,.10);

  --r:8px;
  --r2:14px;
  --r3:22px;
}}

html{{scroll-behavior:smooth}}
body{{
  background:
    radial-gradient(circle at top left, rgba(37,99,235,.05), transparent 30%),
    radial-gradient(circle at top right, rgba(11,31,58,.06), transparent 28%),
    var(--bg);
  color:var(--text);
  font-family:'Inter',sans-serif;
  font-size:15px;
  line-height:1.6;
  overflow-x:hidden;
}}

::-webkit-scrollbar{{width:8px}}
::-webkit-scrollbar-track{{background:var(--bg)}}
::-webkit-scrollbar-thumb{{background:#cbd5e1;border-radius:999px}}

nav{{
  position:sticky;top:0;z-index:100;
  background:rgba(255,255,255,.92);
  backdrop-filter:blur(18px);
  border-bottom:1px solid rgba(15,23,42,.06);
  padding:0 22px;
  height:72px;
  display:flex;
  align-items:center;
  justify-content:space-between;
}}

.nav-logo{{
  font-family:'Manrope',sans-serif;
  font-size:18px;
  font-weight:800;
  letter-spacing:-.3px;
  display:flex;
  align-items:center;
  gap:10px;
  text-decoration:none;
  color:var(--navy);
}}

.nav-dot{{
  width:9px;height:9px;
  background:var(--blue-2);
  border-radius:50%;
  box-shadow:0 0 0 6px rgba(37,99,235,.10);
  animation:blink 2s ease-in-out infinite;
}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.45}}}}

.nav-right{{display:flex;align-items:center;gap:10px}}
#nav-clock{{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}}
.nav-badge{{
  font-size:11px;font-weight:700;
  background:var(--blue-soft);
  color:var(--blue-2);
  border:1px solid rgba(37,99,235,.14);
  padding:6px 12px;border-radius:999px;
}}

.hero{{
  position:relative;
  overflow:hidden;
  padding:86px 24px 66px;
  text-align:center;
  background:
    radial-gradient(circle at 50% -20%, rgba(37,99,235,.20), transparent 45%),
    linear-gradient(180deg, #ffffff 0%, #f7faff 100%);
  border-bottom:1px solid rgba(15,23,42,.05);
}}

.hero-grid{{
  position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(15,23,42,.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(15,23,42,.03) 1px,transparent 1px);
  background-size:56px 56px;
  mask-image:radial-gradient(ellipse 100% 85% at 50% 0%, black 0%, transparent 78%);
}}

.hero-glow{{
  position:absolute;top:-40px;left:50%;transform:translateX(-50%);
  width:900px;height:340px;
  background:radial-gradient(circle, rgba(29,78,216,.18), transparent 62%);
  pointer-events:none;
}}

.hero-eyebrow{{
  display:inline-flex;align-items:center;gap:8px;
  font-size:12px;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;
  color:var(--blue-2);
  margin-bottom:18px;
  background:rgba(255,255,255,.78);
  border:1px solid rgba(37,99,235,.12);
  padding:8px 14px;
  border-radius:999px;
  box-shadow:var(--shadow-sm);
}}

.hero h1{{
  font-family:'Manrope',sans-serif;
  font-size:clamp(36px,8vw,70px);
  font-weight:800;
  line-height:1.02;
  letter-spacing:-2.4px;
  color:var(--navy);
  margin-bottom:18px;
  max-width:820px;
  margin-left:auto;margin-right:auto;
}}

.hero h1 .accent{{
  color:var(--blue-2);
}}

.hero-sub{{
  font-size:17px;
  color:var(--text-2);
  font-weight:500;
  max-width:650px;
  margin:0 auto;
  line-height:1.7;
}}

.metrics{{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:14px;
  max-width:1120px;
  margin:24px auto 0;
  padding:0 18px 10px;
}}

.metric{{
  background:var(--surface);
  border:1px solid rgba(15,23,42,.06);
  border-radius:18px;
  padding:22px 16px;
  text-align:center;
  position:relative;
  overflow:hidden;
  box-shadow:var(--shadow-sm);
}}
.metric::before{{
  content:'';
  position:absolute;
  top:0;left:0;right:0;height:4px;
  background:linear-gradient(90deg,var(--navy),var(--blue-2),#60a5fa);
}}
.metric-num{{
  font-family:'Manrope',sans-serif;
  font-size:30px;
  font-weight:800;
  color:var(--navy);
  line-height:1;
  margin-bottom:6px;
  letter-spacing:-1px;
}}
.metric-label{{
  font-size:11px;
  color:var(--muted);
  font-weight:700;
  letter-spacing:.08em;
  text-transform:uppercase;
}}

.filters-section{{
  background:transparent;
  max-width:1120px;
  margin:14px auto 0;
  padding:14px 18px 4px;
}}

.filters-search{{position:relative;margin-bottom:12px}}
.filters-search input{{
  width:100%;
  background:var(--surface);
  border:1px solid var(--line);
  color:var(--text);
  font-family:'Inter',sans-serif;
  font-size:14px;
  padding:15px 16px 15px 46px;
  border-radius:16px;
  outline:none;
  transition:border .2s, box-shadow .2s, transform .2s;
  box-shadow:var(--shadow-sm);
}}
.filters-search input::placeholder{{color:var(--muted)}}
.filters-search input:focus{{
  border-color:rgba(37,99,235,.35);
  box-shadow:0 0 0 4px rgba(37,99,235,.10);
}}
.s-ico{{
  position:absolute;left:16px;top:50%;
  transform:translateY(-50%);
  color:var(--blue-2);
  font-size:16px;
  pointer-events:none;
}}

.f-row{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}}
.f-row:last-child{{margin-bottom:0}}
.f-lbl{{
  font-size:11px;font-weight:800;
  letter-spacing:.08em;
  text-transform:uppercase;
  color:var(--muted);
  margin-bottom:8px;
  display:block;
}}

.chip{{
  flex-shrink:0;
  background:var(--surface);
  border:1px solid var(--line);
  color:var(--text-2);
  font-family:'Inter',sans-serif;
  font-size:12px;
  font-weight:600;
  padding:8px 14px;
  border-radius:999px;
  cursor:pointer;
  transition:all .18s;
  white-space:nowrap;
  box-shadow:var(--shadow-sm);
}}
.chip:hover{{
  border-color:rgba(37,99,235,.22);
  color:var(--blue-2);
  transform:translateY(-1px);
}}
.chip.active{{
  background:var(--navy);
  border-color:var(--navy);
  color:#fff;
}}

.f-sel{{
  background:var(--surface);
  border:1px solid var(--line);
  color:var(--text);
  font-family:'Inter',sans-serif;
  font-size:12px;
  padding:8px 13px;
  border-radius:999px;
  cursor:pointer;
  flex-shrink:0;
  outline:none;
  box-shadow:var(--shadow-sm);
}}

.trust-bar{{
  max-width:1120px;
  margin:12px auto 0;
  background:linear-gradient(90deg, rgba(37,99,235,.05), rgba(11,31,58,.06));
  border:1px solid rgba(37,99,235,.10);
  border-radius:16px;
  padding:11px 16px;
  display:flex;align-items:center;gap:10px;
  font-size:12px;
  color:var(--text-2);
}}
.trust-dot{{
  width:8px;height:8px;
  background:var(--green);
  border-radius:50%;
  flex-shrink:0;
  box-shadow:0 0 0 6px rgba(22,163,74,.12);
}}

.page{{
  padding:28px 18px 56px;
  max-width:1120px;
  margin:0 auto;
}}

.sec-hdr{{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:16px;
  margin-top:34px;
}}

.sec-title{{
  font-family:'Manrope',sans-serif;
  font-size:18px;
  font-weight:800;
  color:var(--navy);
  display:flex;
  align-items:center;
  gap:10px;
  letter-spacing:-.3px;
}}

.sec-count{{
  font-size:11px;
  color:var(--blue-2);
  background:var(--blue-soft);
  border:1px solid rgba(37,99,235,.14);
  padding:6px 12px;
  border-radius:999px;
  font-weight:700;
}}

.calc-grid{{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:12px;
}}

.calc-item{{
  background:var(--surface);
  border:1px solid rgba(15,23,42,.06);
  border-radius:18px;
  padding:16px 16px;
  display:flex;
  align-items:center;
  gap:12px;
  cursor:pointer;
  transition:all .2s;
  text-align:left;
  color:var(--text);
  box-shadow:var(--shadow-sm);
}}
.calc-item:hover{{
  border-color:rgba(37,99,235,.18);
  transform:translateY(-2px);
  box-shadow:var(--shadow-md);
}}
.calc-emoji{{font-size:22px;flex-shrink:0}}
.calc-name{{font-size:14px;font-weight:700;margin-bottom:2px;color:var(--navy)}}
.calc-hint{{font-size:11px;color:var(--muted)}}

.articles-grid{{display:flex;flex-direction:column;gap:12px}}
.article-card{{
  background:var(--surface);
  border:1px solid rgba(15,23,42,.06);
  border-radius:18px;
  padding:16px;
  display:flex;
  gap:14px;
  transition:all .2s;
  cursor:pointer;
  box-shadow:var(--shadow-sm);
}}
.article-card:hover{{
  border-color:rgba(37,99,235,.16);
  transform:translateY(-2px);
  box-shadow:var(--shadow-md);
}}
.article-icon{{font-size:24px;flex-shrink:0;margin-top:2px}}
.article-content{{flex:1;min-width:0}}
.article-cat{{
  font-size:10px;font-weight:800;
  letter-spacing:.12em;
  text-transform:uppercase;
  color:var(--blue-2);
  margin-bottom:4px;
}}
.article-title{{
  font-size:15px;
  font-weight:800;
  color:var(--navy);
  margin-bottom:5px;
  line-height:1.35;
}}
.article-excerpt{{font-size:13px;color:var(--text-2);line-height:1.55;margin-bottom:8px}}
.article-footer{{display:flex;align-items:center;justify-content:space-between;gap:8px}}
.article-source{{font-size:11px;color:var(--muted)}}
.article-cta{{font-size:12px;color:var(--blue-2);font-weight:800}}

.newsletter{{
  background:linear-gradient(135deg, #ffffff, #f5f9ff);
  border:1px solid rgba(37,99,235,.10);
  border-radius:22px;
  padding:24px 20px;
  margin-bottom:4px;
  position:relative;
  overflow:hidden;
  box-shadow:var(--shadow-md);
}}
.newsletter::before{{
  content:'';
  position:absolute;
  top:0;left:0;right:0;height:5px;
  background:linear-gradient(90deg,var(--navy),var(--blue-2),#60a5fa);
}}
.nl-title{{font-family:'Manrope',sans-serif;font-size:20px;font-weight:800;margin-bottom:5px;color:var(--navy)}}
.nl-title span{{color:var(--blue-2)}}
.nl-desc{{font-size:13px;color:var(--text-2);margin-bottom:16px}}
.nl-form{{display:flex;gap:10px;flex-wrap:wrap}}
.nl-input{{
  flex:1;min-width:180px;
  background:#fff;
  border:1px solid var(--line);
  color:var(--text);
  font-family:'Inter',sans-serif;
  font-size:14px;
  padding:12px 14px;
  border-radius:14px;
  outline:none;
}}
.nl-input:focus{{border-color:rgba(37,99,235,.35);box-shadow:0 0 0 4px rgba(37,99,235,.10)}}
.nl-btn{{
  background:var(--navy);
  color:#fff;border:none;
  font-family:'Inter',sans-serif;
  font-size:14px;font-weight:700;
  padding:12px 18px;
  border-radius:14px;
  cursor:pointer;
  white-space:nowrap;
}}
.nl-btn:hover{{background:var(--navy-2)}}
.nl-ok{{display:none;color:var(--green);font-size:12px;margin-top:8px;font-weight:700}}

.jobs-list{{display:flex;flex-direction:column;gap:14px}}

.job-card{{
  background:var(--surface);
  border:1px solid rgba(15,23,42,.06);
  border-radius:22px;
  overflow:hidden;
  transition:all .22s;
  animation:fadeUp .35s ease both;
  position:relative;
  box-shadow:var(--shadow-sm);
}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
.job-card:hover{{
  border-color:rgba(37,99,235,.16);
  transform:translateY(-3px);
  box-shadow:var(--shadow-lg);
}}

.card-accent{{
  position:absolute;
  left:0;top:0;bottom:0;
  width:5px;
  border-radius:22px 0 0 22px;
}}

.card-body{{padding:20px 20px 18px 24px}}
.card-top{{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:12px}}
.card-main{{flex:1;min-width:0}}

.card-tag{{
  display:inline-flex;align-items:center;gap:6px;
  font-size:10px;font-weight:800;
  letter-spacing:.08em;text-transform:uppercase;
  padding:5px 10px;border-radius:999px;
  margin-bottom:8px;
}}

.tag-el{{background:#eff6ff;color:#1d4ed8;border:1px solid rgba(37,99,235,.12)}}
.tag-me{{background:#f0fdf4;color:#15803d;border:1px solid rgba(22,163,74,.12)}}
.tag-au{{background:#fff7ed;color:#ea580c;border:1px solid rgba(234,88,12,.12)}}
.tag-qu{{background:#f5f3ff;color:#7c3aed;border:1px solid rgba(124,58,237,.12)}}
.tag-se{{background:#f0fdfa;color:#0f766e;border:1px solid rgba(15,118,110,.12)}}
.tag-rf{{background:#eff6ff;color:#2563eb;border:1px solid rgba(37,99,235,.12)}}

.card-title{{
  font-family:'Manrope',sans-serif;
  font-size:20px;
  font-weight:800;
  color:var(--navy);
  line-height:1.25;
  margin-bottom:4px;
  letter-spacing:-.4px;
}}
.card-company{{font-size:13px;color:var(--text-2);font-weight:600}}

.card-badge-verified{{
  flex-shrink:0;
  font-size:11px;
  font-weight:800;
  color:var(--green);
  background:var(--green-soft);
  border:1px solid rgba(22,163,74,.12);
  padding:6px 10px;
  border-radius:999px;
  white-space:nowrap;
}}

.card-info-row{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}}
.info-chip{{
  font-size:11px;
  color:var(--text-2);
  background:var(--surface-2);
  border:1px solid var(--line);
  padding:6px 10px;
  border-radius:999px;
  font-weight:600;
}}

.card-benefits{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}}
.benef-chip{{
  font-size:11px;
  color:var(--yellow);
  background:var(--yellow-soft);
  border:1px solid rgba(202,138,4,.14);
  padding:5px 9px;
  border-radius:999px;
  font-weight:700;
}}

.card-actions{{
  display:flex;
  gap:8px;
  padding-top:14px;
  border-top:1px solid rgba(15,23,42,.06);
}}

.btn-wpp{{
  display:inline-flex;align-items:center;gap:6px;
  font-size:13px;font-weight:700;
  color:var(--green);
  background:var(--green-soft);
  border:1px solid rgba(22,163,74,.14);
  padding:10px 14px;
  border-radius:14px;
  text-decoration:none;
  transition:all .2s;
}}
.btn-wpp:hover{{background:#e8faef}}

.btn-ver{{
  display:inline-flex;align-items:center;gap:6px;
  font-size:13px;font-weight:700;
  color:#fff;
  background:linear-gradient(135deg,var(--navy),var(--blue-2));
  padding:10px 16px;
  border-radius:14px;
  text-decoration:none;
  transition:all .2s;
  margin-left:auto;
  box-shadow:0 10px 24px rgba(29,78,216,.18);
}}
.btn-ver:hover{{transform:translateY(-1px)}}

.empty-state{{text-align:center;padding:56px 20px;display:none}}
.page[data-searching] .calc-section,
.page[data-searching] .articles-section,
.page[data-searching] .newsletter{{display:none!important}}

.empty-icon{{font-size:46px;margin-bottom:14px;opacity:.5}}
.empty-title{{font-family:'Manrope',sans-serif;font-size:20px;font-weight:800;margin-bottom:8px;color:var(--navy)}}
.empty-text{{font-size:14px;color:var(--muted);line-height:1.7;margin-bottom:20px}}
.empty-btn{{
  display:inline-flex;align-items:center;gap:6px;
  font-size:13px;font-weight:700;
  color:var(--blue-2);
  background:var(--blue-soft);
  border:1px solid rgba(37,99,235,.14);
  padding:10px 18px;border-radius:999px;
  cursor:pointer;transition:all .2s;
}}
.empty-btn:hover{{background:#dbeafe}}

.modal{{
  display:none;position:fixed;inset:0;
  background:rgba(15,23,42,.45);
  z-index:1000;
  align-items:center;justify-content:center;
  padding:16px;
  backdrop-filter:blur(7px);
  overflow-y:auto;
}}
.modal.open{{display:flex}}

.modal-box{{
  background:var(--surface);
  border:1px solid rgba(15,23,42,.06);
  border-radius:24px;
  padding:24px;
  width:100%;
  max-width:420px;
  margin:auto;
  position:relative;
  box-shadow:var(--shadow-lg);
}}
.modal-box::before{{
  content:'';
  position:absolute;
  top:0;left:0;right:0;height:5px;
  background:linear-gradient(90deg,var(--navy),var(--blue-2),#60a5fa);
  border-radius:24px 24px 0 0;
}}

.modal-article{{max-width:660px;max-height:86vh;overflow-y:auto}}
.modal-article-cat{{
  font-size:11px;font-weight:800;
  letter-spacing:.12em;text-transform:uppercase;
  color:var(--blue-2);
  margin-bottom:10px;
}}
.modal-article-title{{
  font-family:'Manrope',sans-serif;
  font-size:28px;
  font-weight:800;
  line-height:1.15;
  margin-bottom:10px;
  letter-spacing:-.6px;
  color:var(--navy);
}}
.modal-article-meta{{
  font-size:12px;color:var(--muted);
  margin-bottom:18px;padding-bottom:14px;
  border-bottom:1px solid rgba(15,23,42,.06);
}}
.modal-article-body{{
  font-size:15px;
  color:var(--text-2);
  line-height:1.78;
  margin-bottom:20px;
}}
.modal-article-body strong{{color:var(--navy);font-weight:800}}
.modal-article-link{{
  display:inline-flex;align-items:center;gap:6px;
  font-size:13px;font-weight:700;
  color:var(--blue-2);
  background:var(--blue-soft);
  border:1px solid rgba(37,99,235,.14);
  padding:10px 16px;
  border-radius:14px;
  text-decoration:none;
  margin-bottom:12px;
  transition:all .2s;
}}
.modal-article-link:hover{{background:#dbeafe}}

.modal-title{{
  font-family:'Manrope',sans-serif;
  font-size:20px;
  font-weight:800;
  color:var(--navy);
  margin-bottom:16px;
}}

.modal-field{{margin-bottom:13px}}
.modal-label{{
  font-size:11px;font-weight:800;
  letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);
  display:block;margin-bottom:6px;
}}

.modal-input,.modal-select{{
  width:100%;
  background:#fff;
  border:1px solid var(--line);
  color:var(--text);
  font-family:'Inter',sans-serif;
  font-size:14px;
  padding:11px 13px;
  border-radius:14px;
  outline:none;
  transition:border .2s, box-shadow .2s;
}}
.modal-input:focus,.modal-select:focus{{
  border-color:rgba(37,99,235,.35);
  box-shadow:0 0 0 4px rgba(37,99,235,.10);
}}

.calc-result{{
  background:var(--surface-2);
  border:1px solid var(--line);
  border-radius:16px;
  padding:14px;
  margin-top:14px;
}}
.result-row{{
  display:flex;justify-content:space-between;
  font-size:13px;margin-bottom:8px;color:var(--text-2);
}}
.result-row.total{{
  color:var(--navy);
  font-weight:800;
  font-size:16px;
  border-top:1px solid var(--line);
  padding-top:10px;
  margin-top:5px;
}}

.btn-close{{
  width:100%;
  margin-top:10px;
  background:#fff;
  color:var(--text-2);
  border:1px solid var(--line);
  font-family:'Inter',sans-serif;
  font-size:13px;
  font-weight:700;
  padding:11px;
  border-radius:14px;
  cursor:pointer;
  transition:all .2s;
}}
.btn-close:hover{{
  border-color:var(--line-2);
  background:var(--surface-2);
}}

footer{{
  border-top:1px solid rgba(15,23,42,.06);
  padding:30px 20px 34px;
  text-align:center;
  background:linear-gradient(180deg, rgba(255,255,255,0), rgba(255,255,255,.7));
}}
.footer-logo{{
  font-family:'Manrope',sans-serif;
  font-size:18px;
  font-weight:800;
  margin-bottom:8px;
  color:var(--navy);
}}
.footer-logo span{{color:var(--blue-2)}}
.footer-text{{font-size:12px;color:var(--muted);line-height:1.8}}

@media (max-width: 860px){{
  .metrics{{grid-template-columns:repeat(2,1fr)}}
}}

@media (max-width: 640px){{
  nav{{height:66px;padding:0 16px}}
  .hero{{padding:72px 18px 52px}}
  .hero h1{{letter-spacing:-1.6px}}
  .hero-sub{{font-size:15px}}
  .metrics{{padding:0 14px 8px;gap:10px}}
  .filters-section,.page{{padding-left:14px;padding-right:14px}}
  .calc-grid{{grid-template-columns:1fr}}
  .card-top{{flex-direction:column}}
  .card-badge-verified{{align-self:flex-start}}
  .card-actions{{flex-wrap:wrap}}
  .btn-ver{{margin-left:0}}
  .modal-box{{padding:18px}}
  .modal-article-title{{font-size:22px}}
}}
</style>
</head>
<body>

<nav>
  <a class="nav-logo" href="#">
    <div class="nav-dot"></div>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 44" height="28" style="display:block">
      <defs>
        <linearGradient id="ng" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#0b1f3a"/>
          <stop offset="100%" style="stop-color:#2563eb"/>
        </linearGradient>
      </defs>
      <g transform="translate(20,22)">
        <path d="M0,-14 L2,-10 L-2,-10 Z" fill="url(#ng)"/>
        <path d="M9.9,-9.9 L7.5,-6.5 L10.5,-5 Z" fill="url(#ng)"/>
        <path d="M14,0 L10,-1.5 L10,1.5 Z" fill="url(#ng)"/>
        <path d="M9.9,9.9 L6.5,7.5 L5,10.5 Z" fill="url(#ng)"/>
        <path d="M0,14 L2,10 L-2,10 Z" fill="url(#ng)"/>
        <path d="M-9.9,9.9 L-7.5,6.5 L-10.5,5 Z" fill="url(#ng)"/>
        <path d="M-14,0 L-10,-1.5 L-10,1.5 Z" fill="url(#ng)"/>
        <path d="M-9.9,-9.9 L-6.5,-7.5 L-5,-10.5 Z" fill="url(#ng)"/>
        <circle cx="0" cy="0" r="10" fill="none" stroke="url(#ng)" stroke-width="2.5"/>
        <circle cx="0" cy="0" r="5" fill="#ffffff" stroke="url(#ng)" stroke-width="1"/>
        <circle cx="0" cy="-1.5" r="2.5" fill="url(#ng)"/>
        <path d="M-2,-1.5 Q-2,2 0,5.5 Q2,2 2,-1.5 Z" fill="url(#ng)"/>
        <circle cx="0" cy="-1.5" r="1" fill="#ffffff"/>
      </g>
      <text x="38" y="30" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="22" fill="#0b1f3a" letter-spacing="-0.5">Tec</text>
      <text x="80" y="30" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="22" fill="url(#ng)" letter-spacing="-0.5">Vagas</text>
    </svg>
  </a>
  <div class="nav-right">
    <span id="nav-clock"></span>
    <span class="nav-badge">⚙️ Ao vivo</span>
  </div>
</nav>

<section class="hero">
  <div class="hero-grid"></div>
  <div class="hero-glow"></div>
  <div class="hero-eyebrow">🇧🇷 Vagas para técnicos industriais · 2026</div>
  <h1>As melhores vagas<br>para <span class="accent">técnicos industriais</span><br>do Brasil.</h1>
  <p class="hero-sub">Elétrica · Mecânica · Automação · Refrigeração<br>Vagas verificadas, atualizadas 5× por dia.</p>
</section>

<div class="metrics">
  <div class="metric"><div class="metric-num" id="m-vagas">{total}</div><div class="metric-label">Vagas ativas</div></div>
  <div class="metric"><div class="metric-num">60+</div><div class="metric-label">Especialidades</div></div>
  <div class="metric"><div class="metric-num">5×</div><div class="metric-label">Atualizado/dia</div></div>
  <div class="metric"><div class="metric-num">27</div><div class="metric-label">Estados</div></div>
</div>

<div class="filters-section">
  <div class="filters-search">
    <span class="s-ico">🔍</span>
    <input type="text" id="s-inp" placeholder="Buscar por cargo, empresa ou cidade..." oninput="buscar(this.value)">
  </div>
  <span class="f-lbl">Área técnica</span>
  <div class="f-row">
    <button class="chip active" onclick="fA('todas',this)">Todas</button>
    <button class="chip" onclick="fA('eletrica',this)">⚡ Elétrica</button>
    <button class="chip" onclick="fA('mecanica',this)">🔩 Mecânica</button>
    <button class="chip" onclick="fA('automacao',this)">🤖 Automação</button>
    <button class="chip" onclick="fA('refrigeracao',this)">❄️ Refrigeração</button>
    <button class="chip" onclick="fA('qualidade',this)">📊 Qualidade</button>
    <button class="chip" onclick="fA('seguranca',this)">🦺 Segurança</button>
  </div>
  <span class="f-lbl">Estado</span>
  <div class="f-row">
    <select class="f-sel" onchange="fE(this.value)">{opts_estados}</select>
  </div>
</div>

<div class="trust-bar">
  <div class="trust-dot"></div>
  Vagas verificadas · Apenas 2026 · Encerradas removidas automaticamente · Atualizado em {agora}
</div>

<div class="page">

  <div class="calc-section">
    <div class="sec-hdr"><div class="sec-title">🧮 Calculadoras Trabalhistas</div></div>
    <div class="calc-grid">
      <button class="calc-item" onclick="openModal('m-sal')"><div class="calc-emoji">💰</div><div><div class="calc-name">Salário Líquido</div><div class="calc-hint">INSS + IRRF 2026</div></div></button>
      <button class="calc-item" onclick="openModal('m-fer')"><div class="calc-emoji">🏖️</div><div><div class="calc-name">Férias</div><div class="calc-hint">+ 1/3 constitucional</div></div></button>
      <button class="calc-item" onclick="openModal('m-res')"><div class="calc-emoji">📦</div><div><div class="calc-name">Rescisão</div><div class="calc-hint">Demissão ou pedido</div></div></button>
      <button class="calc-item" onclick="openModal('m-he')"><div class="calc-emoji">⏰</div><div><div class="calc-name">Hora Extra</div><div class="calc-hint">50%, 100% e noturna</div></div></button>
      <button class="calc-item" onclick="openModal('m-not')"><div class="calc-emoji">🌙</div><div><div class="calc-name">Adicional Noturno</div><div class="calc-hint">20% sobre salário</div></div></button>
      <button class="calc-item" onclick="openModal('m-ins')"><div class="calc-emoji">⚠️</div><div><div class="calc-name">Insalubridade</div><div class="calc-hint">e Periculosidade</div></div></button>
      <button class="calc-item" onclick="openModal('m-dec')"><div class="calc-emoji">🎄</div><div><div class="calc-name">13º Salário</div><div class="calc-hint">Proporcional ou cheio</div></div></button>
    </div>
  </div>

  <div class="articles-section">
    <div class="sec-hdr"><div class="sec-title">📰 Para Técnicos</div><span class="sec-count">{len(artigos)} artigos</span></div>
    <div class="articles-grid">{cards_artigos}</div>
  </div>

  <div class="newsletter">
    <div class="nl-title">📧 Receba <span>vagas</span> no seu email</div>
    <div class="nl-desc">Toda semana as melhores vagas técnicas. Grátis.</div>
    <div class="nl-form">
      <input class="nl-input" type="email" id="nl-e" placeholder="seu@email.com">
      <button class="nl-btn" onclick="newsletter()">Quero receber</button>
    </div>
    <div class="nl-ok" id="nl-ok">✓ Cadastrado! Você receberá as vagas em breve.</div>
  </div>

  <div class="sec-hdr" id="vagas"><div class="sec-title">🔧 Vagas Disponíveis</div><span class="sec-count" id="vc">{total} vagas</span></div>
  <div class="jobs-list" id="jl">{cards_vagas}</div>
  <div class="empty-state" id="es">
    <div class="empty-icon">🔍</div>
    <div class="empty-title">Nenhuma vaga encontrada</div>
    <div class="empty-text">Tente outra especialidade, estado ou termo de busca.<br>Atualizamos 5x por dia com novas vagas.</div>
    <button class="empty-btn" onclick="resetF()">← Ver todas as vagas</button>
  </div>

</div>

<!-- MODAIS CALCULADORAS -->
<div class="modal" id="m-sal"><div class="modal-box">
  <div class="modal-title">💰 Salário Líquido</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="s1" placeholder="Ex: 3500" oninput="cS()"></div>
  <div class="modal-field"><label class="modal-label">Dependentes para IR</label><input class="modal-input" type="number" id="s2" placeholder="0" value="0" oninput="cS()"></div>
  <div class="calc-result" id="s-r" style="display:none">
    <div class="result-row"><span>Salário Bruto</span><span id="s-a"></span></div>
    <div class="result-row"><span>(-) INSS</span><span id="s-b" style="color:#dc2626"></span></div>
    <div class="result-row"><span>(-) IRRF</span><span id="s-c" style="color:#dc2626"></span></div>
    <div class="result-row total"><span>💵 Salário Líquido</span><span id="s-d"></span></div>
    <div class="result-row" style="font-size:11px;margin-top:3px"><span>FGTS (empregador)</span><span id="s-e" style="color:var(--green)"></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-sal')">Fechar</button>
</div></div>

<div class="modal" id="m-fer"><div class="modal-box">
  <div class="modal-title">🏖️ Férias</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="f1" placeholder="Ex: 3500" oninput="cF()"></div>
  <div class="modal-field"><label class="modal-label">Meses trabalhados</label><input class="modal-input" type="number" id="f2" value="12" min="1" max="12" oninput="cF()"></div>
  <div class="calc-result" id="f-r" style="display:none">
    <div class="result-row"><span>Férias proporcional</span><span id="f-a"></span></div>
    <div class="result-row"><span>(+) 1/3</span><span id="f-b" style="color:var(--green)"></span></div>
    <div class="result-row"><span>(-) INSS + IR</span><span id="f-c" style="color:#dc2626"></span></div>
    <div class="result-row total"><span>🏖️ Férias Líquidas</span><span id="f-d"></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-fer')">Fechar</button>
</div></div>

<div class="modal" id="m-res"><div class="modal-box">
  <div class="modal-title">📦 Rescisão</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="r1" placeholder="Ex: 3500" oninput="cR()"></div>
  <div class="modal-field"><label class="modal-label">Meses trabalhados no ano</label><input class="modal-input" type="number" id="r2" placeholder="Ex: 6" min="1" max="12" oninput="cR()"></div>
  <div class="modal-field"><label class="modal-label">Tipo</label>
    <select class="modal-select" id="r3" onchange="cR()"><option value="sj">Demissão sem justa causa</option><option value="pd">Pedido de demissão</option><option value="ac">Acordo (distrato)</option></select>
  </div>
  <div class="calc-result" id="r-r" style="display:none">
    <div class="result-row"><span>Saldo de salário</span><span id="r-a"></span></div>
    <div class="result-row"><span>13º proporcional</span><span id="r-b"></span></div>
    <div class="result-row"><span>Férias + 1/3</span><span id="r-c"></span></div>
    <div class="result-row" id="r-ml" style="display:none"><span>Multa FGTS</span><span id="r-d" style="color:var(--green)"></span></div>
    <div class="result-row total"><span>📦 Total Rescisão</span><span id="r-e"></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-res')">Fechar</button>
</div></div>

<div class="modal" id="m-he"><div class="modal-box">
  <div class="modal-title">⏰ Hora Extra</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="h1" placeholder="Ex: 3500" oninput="cHE()"></div>
  <div class="modal-field"><label class="modal-label">Horas extras</label><input class="modal-input" type="number" id="h2" placeholder="Ex: 10" oninput="cHE()"></div>
  <div class="modal-field"><label class="modal-label">Tipo</label>
    <select class="modal-select" id="h3" onchange="cHE()"><option value="50">50% — Dias úteis</option><option value="100">100% — Dom/Feriados</option><option value="70">70% — Noturna</option></select>
  </div>
  <div class="calc-result" id="h-r" style="display:none">
    <div class="result-row"><span>Valor hora normal</span><span id="h-a"></span></div>
    <div class="result-row"><span>Valor hora extra</span><span id="h-b"></span></div>
    <div class="result-row total"><span>⏰ Total a receber</span><span id="h-c"></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-he')">Fechar</button>
</div></div>

<div class="modal" id="m-not"><div class="modal-box">
  <div class="modal-title">🌙 Adicional Noturno</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="n1" placeholder="Ex: 3500" oninput="cN()"></div>
  <div class="modal-field"><label class="modal-label">Horas noturnas por mês</label><input class="modal-input" type="number" id="n2" placeholder="Ex: 44" oninput="cN()"></div>
  <div class="calc-result" id="n-r" style="display:none">
    <div class="result-row"><span>Salário base</span><span id="n-a"></span></div>
    <div class="result-row"><span>(+) Adicional 20%</span><span id="n-b" style="color:var(--green)"></span></div>
    <div class="result-row total"><span>🌙 Total com adicional</span><span id="n-c"></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-not')">Fechar</button>
</div></div>

<div class="modal" id="m-ins"><div class="modal-box">
  <div class="modal-title">⚠️ Insalubridade</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="i1" placeholder="Ex: 3500" oninput="cI()"></div>
  <div class="modal-field"><label class="modal-label">Tipo</label>
    <select class="modal-select" id="i2" onchange="cI()"><option value="10">Insalubridade Mínima 10% SM</option><option value="20">Insalubridade Média 20% SM</option><option value="40">Insalubridade Máxima 40% SM</option><option value="30p">Periculosidade 30% salário</option></select>
  </div>
  <div class="calc-result" id="i-r" style="display:none">
    <div class="result-row"><span>Salário base</span><span id="i-a"></span></div>
    <div class="result-row"><span>(+) Adicional</span><span id="i-b" style="color:var(--green)"></span></div>
    <div class="result-row total"><span>⚠️ Total</span><span id="i-c"></span></div>
    <div class="result-row" style="font-size:10px;margin-top:3px;color:var(--muted)"><span>Salário mínimo 2026: R$ 1.518,00</span><span></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-ins')">Fechar</button>
</div></div>

<div class="modal" id="m-dec"><div class="modal-box">
  <div class="modal-title">🎄 13º Salário</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="d1" placeholder="Ex: 3500" oninput="cD()"></div>
  <div class="modal-field"><label class="modal-label">Meses trabalhados</label><input class="modal-input" type="number" id="d2" value="12" min="1" max="12" oninput="cD()"></div>
  <div class="calc-result" id="d-r" style="display:none">
    <div class="result-row"><span>13º bruto proporcional</span><span id="d-a"></span></div>
    <div class="result-row"><span>(-) INSS + IR</span><span id="d-b" style="color:#dc2626"></span></div>
    <div class="result-row total"><span>🎄 13º Líquido</span><span id="d-c"></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-dec')">Fechar</button>
</div></div>

<footer>
  <div class="footer-logo">Tec<span>Vagas</span></div>
  <div class="footer-text">Vagas técnicas industriais verificadas · Apenas 2026 · Todo o Brasil<br>Atualizado automaticamente 5× por dia · Links redirecionam para os sites originais</div>
</footer>

<script data-goatcounter="https://tecvagas.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<script>
// RELÓGIO
(function(){{const el=document.getElementById('nav-clock');function t(){{el.textContent=new Date().toLocaleTimeString('pt-BR',{{timeZone:'America/Sao_Paulo',hour:'2-digit',minute:'2-digit'}});}}t();setInterval(t,1000);}})();

// MODAIS
function openModal(id){{document.getElementById(id).classList.add('open');document.body.style.overflow='hidden';}}
function closeModal(id){{document.getElementById(id).classList.remove('open');document.body.style.overflow='';}}
function openArticle(idx){{openModal('article-'+idx);}}
document.querySelectorAll('.modal').forEach(m=>m.addEventListener('click',e=>{{if(e.target===m)closeModal(m.id);}}));
document.addEventListener('keydown',e=>{{if(e.key==='Escape')document.querySelectorAll('.modal.open').forEach(m=>closeModal(m.id));}});

// FILTROS
let _a='todas',_e='todos',_x='todas',_b='';
function fA(a,b){{_a=a;document.querySelectorAll('.chip').forEach(x=>x.classList.remove('active'));b.classList.add('active');render();}}
function fE(v){{_e=v;render();}}
function fX(v){{_x=v;render();}}
function buscar(v){{
  _b=v.toLowerCase().trim();
  const hasSearch=_b.length>0;
  const page=document.querySelector('.page');
  if(hasSearch){{
    page.setAttribute('data-searching','1');
  }} else {{
    page.removeAttribute('data-searching');
  }}
  render();
}}
function resetF(){{
  _a='todas';_e='todos';_x='todas';_b='';
  document.querySelectorAll('.chip').forEach(x=>x.classList.remove('active'));
  document.querySelector('.chip').classList.add('active');
  document.getElementById('s-inp').value='';
  document.querySelectorAll('.f-sel').forEach(s=>s.selectedIndex=0);
  document.querySelector('.page').removeAttribute('data-searching');
  render();
}}
function render(){{
  let n=0;
  document.querySelectorAll('#jl .job-card').forEach(c=>{{
    const ok=(_a==='todas'||c.dataset.area===_a)&&(_e==='todos'||c.dataset.estado===_e)&&(_x==='todas'||c.dataset.esp.includes(_x))&&(_b===''||c.dataset.busca.includes(_b));
    c.style.display=ok?'block':'none';
    if(ok)n++;
  }});
  document.getElementById('vc').textContent=n+' vagas';
  document.getElementById('m-vagas').textContent=n;
  document.getElementById('es').style.display=n===0?'block':'none';
  document.getElementById('jl').style.display=n===0?'none':'flex';
}}

// NEWSLETTER
function newsletter(){{
  const e=document.getElementById('nl-e').value;
  if(!e||!e.includes('@')){{alert('Digite um email válido!');return;}}
  fetch('https://formsubmit.co/ajax/tecvagas@gmail.com',{{method:'POST',headers:{{'Content-Type':'application/json','Accept':'application/json'}},body:JSON.stringify({{email:e,_subject:'Newsletter TecVagas'}})}}).catch(()=>{{}});
  document.getElementById('nl-ok').style.display='block';
  document.getElementById('nl-e').value='';
}}

// MATEMÁTICA
function IN(b){{const f=[[1518,.075],[2793.88,.09],[4190.83,.12],[8157.41,.14]];let i=0,a=0;for(const[t,q]of f){{if(b<=t){{i+=(b-a)*q;break;}}i+=(t-a)*q;a=t;}}return Math.min(i,908.86);}}
function IR(b,d){{const x=b-d*189.59;const f=[[2259.2,0,0],[2826.65,.075,169.44],[3751.05,.15,381.44],[4664.68,.225,662.77],[1/0,.275,896]];for(const[t,a,e]of f)if(x<=t)return Math.max(0,x*a-e);return 0;}}
function R(v){{return'R$ '+v.toFixed(2).replace('.',',').replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,'.');}}
function G(id){{return parseFloat(document.getElementById(id).value)||0;}}
function GI(id){{return parseInt(document.getElementById(id).value)||0;}}
function GV(id){{return document.getElementById(id).value;}}
function S(id,v){{document.getElementById(id).textContent=v;}}
function SH(id,d){{document.getElementById(id).style.display=d?'block':'none';}}

function cS(){{const b=G('s1'),d=GI('s2');if(!b){{SH('s-r',0);return;}}const i=IN(b),r=IR(b-i,d),l=b-i-r;S('s-a',R(b));S('s-b','- '+R(i));S('s-c','- '+R(r));S('s-d',R(l));S('s-e','+ '+R(b*.08));SH('s-r',1);}}
function cF(){{const b=G('f1'),m=GI('f2')||12;if(!b){{SH('f-r',0);return;}}const p=b*(m/12),t=p/3,tot=p+t,i=IN(tot),r=IR(tot-i,0);S('f-a',R(p));S('f-b','+ '+R(t));S('f-c','- '+R(i+r));S('f-d',R(tot-i-r));SH('f-r',1);}}
function cR(){{const b=G('r1'),m=GI('r2')||1,tp=GV('r3');if(!b){{SH('r-r',0);return;}}const dec=b*(m/12),fp=b*(m/12)*(4/3),fg=b*.08*m;let mu=tp==='sj'?fg*.4:tp==='ac'?fg*.2:0;S('r-a',R(b));S('r-b',R(dec));S('r-c',R(fp));if(mu>0){{S('r-d','+ '+R(mu));SH('r-ml',1);}}else SH('r-ml',0);S('r-e',R(b+dec+fp+mu));SH('r-r',1);}}
function cHE(){{const b=G('h1'),h=G('h2'),tp=parseFloat(GV('h3'));if(!b||!h){{SH('h-r',0);return;}}const hb=b/220,he=hb*(1+tp/100);S('h-a',R(hb));S('h-b',R(he));S('h-c',R(he*h));SH('h-r',1);}}
function cN(){{const b=G('n1'),h=G('n2');if(!b){{SH('n-r',0);return;}}const ad=(b/220)*.2*h;S('n-a',R(b));S('n-b','+ '+R(ad));S('n-c',R(b+ad));SH('n-r',1);}}
function cI(){{const b=G('i1'),tp=GV('i2');if(!b){{SH('i-r',0);return;}}const ad=tp==='30p'?b*.3:1518*(parseFloat(tp)/100);S('i-a',R(b));S('i-b','+ '+R(ad));S('i-c',R(b+ad));SH('i-r',1);}}
function cD(){{const b=G('d1'),m=GI('d2')||12;if(!b){{SH('d-r',0);return;}}const br=b*(m/12),i=IN(br),r=IR(br-i,0);S('d-a',R(br));S('d-b','- '+R(i+r));S('d-c',R(br-i-r));SH('d-r',1);}}
</script>
</body>
</html>"""
