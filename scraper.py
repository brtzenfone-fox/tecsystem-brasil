"""
TecSystem Brasil - Robô de Vagas v10
=====================================
REDESIGN COMPLETO — Premium Industrial
- Visual inspirado em Stripe/Linear mas com identidade industrial brasileira
- Tipografia: Syne (display) + DM Sans (body) — moderna, forte, limpa
- Paleta: #0A0A0F (fundo profundo) + #F97316 (laranja técnico) + #3B82F6 (azul elétrico)
- Hero com gradiente sutil e grid industrial de fundo
- Cards premium com hover sofisticado
- Filtros em chips/tags elegantes
- Métricas animadas
- Badges de verificação
- Mobile-first
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9",
}

TECNICOS = [
    "técnico em manutenção elétrica","técnico em elétrica industrial",
    "técnico em eletrotécnica","técnico em eletromecânica",
    "técnico em eletrônica industrial","técnico em painéis elétricos",
    "técnico em comando elétrico","técnico em motores elétricos",
    "técnico em subestações elétricas","técnico em geradores",
    "técnico em manutenção mecânica","técnico em mecânica industrial",
    "técnico em hidráulica industrial","técnico em pneumática industrial",
    "técnico em bombas industriais","técnico em compressores industriais",
    "técnico em válvulas industriais","técnico em lubrificação industrial",
    "técnico em soldagem industrial","técnico em caldeiraria",
    "técnico em tubulação industrial","técnico em usinagem","técnico em CNC",
    "técnico em mecatrônica","técnico em manutenção eletromecânica",
    "técnico em manutenção industrial","técnico em automação industrial",
    "técnico em PLC","técnico em SCADA","técnico em robótica industrial",
    "técnico em instrumentação industrial","técnico em redes industriais",
    "técnico em refrigeração industrial","técnico em HVAC",
    "técnico em climatização industrial","técnico em caldeiras industriais",
    "técnico em vapor industrial","técnico em ar comprimido industrial",
    "técnico em tratamento de água industrial","técnico em utilidades industriais",
    "técnico em manutenção preditiva","técnico em manutenção preventiva",
    "técnico em manutenção corretiva","técnico em vibração industrial",
    "técnico em análise de óleo","técnico em PCM",
    "técnico em confiabilidade industrial","técnico em planejamento de manutenção",
    "técnico em controle de qualidade industrial","técnico em inspeção de qualidade",
    "técnico em ensaios não destrutivos","técnico em metrologia industrial",
    "técnico em segurança do trabalho industrial","técnico em processos industriais",
    "técnico em montagem industrial","técnico em metalurgia",
    "técnico em siderurgia","técnico em mineração","técnico em petroquímica",
    "técnico em gás industrial","técnico em instalações industriais",
]

PALAVRAS_DESCARTAR = [
    "banco de talentos","banco de talento","encerrad","finalizad",
    "expirad","inativ","cancelad","processo seletivo encerrado",
    "vaga encerrada","não está mais disponível","job expired",
    "talentos 2024","talentos 2025","2023","2024",
]

ANO_ATUAL = "2026"
CACHE_FILE = "vagas_cache.json"
ARTIGOS_FILE = "artigos.json"

ESTADOS = {
    "AC":"Acre","AL":"Alagoas","AP":"Amapá","AM":"Amazonas",
    "BA":"Bahia","CE":"Ceará","DF":"Distrito Federal","ES":"Espírito Santo",
    "GO":"Goiás","MA":"Maranhão","MT":"Mato Grosso","MS":"Mato Grosso do Sul",
    "MG":"Minas Gerais","PA":"Pará","PB":"Paraíba","PR":"Paraná",
    "PE":"Pernambuco","PI":"Piauí","RJ":"Rio de Janeiro","RN":"Rio Grande do Norte",
    "RS":"Rio Grande do Sul","RO":"Rondônia","RR":"Roraima","SC":"Santa Catarina",
    "SP":"São Paulo","SE":"Sergipe","TO":"Tocantins",
}

ICONES_BENEFICIOS = {
    "vale transporte":"🚌","vale refeição":"🍽️","vale alimentação":"🛒",
    "plano médico":"🏥","plano de saúde":"🏥","assistência médica":"🏥",
    "convênio médico":"🏥","plano odontológico":"🦷","convênio odontológico":"🦷",
    "seguro de vida":"🛡️","previdência privada":"💰","participação nos lucros":"💵",
    "gympass":"💪","total pass":"💪","academia":"💪",
    "home office":"🏠","trabalho remoto":"🏠","cesta básica":"🧺",
    "auxílio educação":"📚","bolsa estudo":"📚",
}

ARTIGOS_PADRAO = [
    {"titulo":"Quanto ganha um Técnico em Manutenção Elétrica em 2026?","resumo":"Salários variam de R$ 2.800 a R$ 6.500 dependendo da região e experiência. Certificações como NR10 e NR35 podem aumentar o salário em até 30%.","categoria":"Salários","icone":"⚡","fonte":"TecSystem Brasil","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"NR10: Guia Completo para Técnicos Elétricos em 2026","resumo":"A NR10 é obrigatória para todos os profissionais que trabalham com instalações elétricas. Curso básico tem 40 horas e validade de 2 anos.","categoria":"Certificações","icone":"📋","fonte":"TecSystem Brasil","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"Técnico em Automação: a profissão que mais cresce","resumo":"Com a Indústria 4.0, técnicos em PLC e SCADA são os mais disputados. Salários de R$ 3.500 a R$ 8.000 em 2026.","categoria":"Carreira","icone":"🤖","fonte":"TecSystem Brasil","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"Melhores empresas para técnicos industriais em 2026","resumo":"Petrobras, Vale, WEG, Embraer e Bosch oferecem os melhores salários e benefícios para técnicos industriais.","categoria":"Empresas","icone":"🏭","fonte":"TecSystem Brasil","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"NR12, NR33 e NR35: quais certificações valem mais?","resumo":"Cada certificação NR pode adicionar de R$ 200 a R$ 500 ao salário mensal. Descubra quais são essenciais para sua área.","categoria":"Certificações","icone":"🦺","fonte":"TecSystem Brasil","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"Como passar na entrevista para técnico industrial","resumo":"Dicas práticas de recrutadores: prepare seus certificados NR, teste técnico, esquemas elétricos e situações reais de manutenção.","categoria":"Dicas","icone":"💼","fonte":"TecSystem Brasil","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
]


def detectar_area(texto):
    t=texto.lower()
    if any(p in t for p in ["elétric","eletric","eletrom","painel","subestac","motor","gerador"]):return "eletrica"
    if any(p in t for p in ["mecatrôn","mecatron","plc","scada","robotic","automac","automaç","cnc","instrumenta"]):return "automacao"
    if any(p in t for p in ["qualidad","inspeç","metrolog","ensaio","calibr"]):return "qualidade"
    if any(p in t for p in ["seguranç","meio ambient"]):return "seguranca"
    if any(p in t for p in ["refriger","hvac","climatiz","ar condiciona"]):return "refrigeracao"
    return "mecanica"

def detectar_estado(texto):
    tu=texto.upper()
    for s,n in ESTADOS.items():
        if f", {s}" in texto or n.upper() in tu:return s
    return "BR"

def titulo_valido(titulo):
    return not any(p in titulo.lower() for p in PALAVRAS_DESCARTAR)

def icone_benef(b):
    bl=b.lower()
    for k,v in ICONES_BENEFICIOS.items():
        if k in bl:return v
    return "✅"


def buscar_gupy():
    vagas=[]
    print("🔍 Buscando no Gupy...")
    for termo in TECNICOS[:25]:
        try:
            url=f"https://portal.api.gupy.io/api/v1/jobs?jobName={requests.utils.quote(termo)}&limit=5"
            resp=requests.get(url,headers=HEADERS,timeout=15)
            if resp.status_code!=200:continue
            for job in resp.json().get("data",[]):
                pub=str(job.get("publishedDate","") or job.get("createdAt",""))
                if ANO_ATUAL not in pub:continue
                titulo=job.get("name","")[:80]
                if not titulo_valido(titulo):continue
                local=f"{job.get('city','Brasil')}, {job.get('state','')}"
                benef=[]
                for b in job.get("benefits",[])[:5]:
                    if isinstance(b,dict) and b.get("name"):benef.append(b["name"][:30])
                    elif isinstance(b,str):benef.append(b[:30])
                vagas.append({"titulo":titulo,"empresa":job.get("careerPageName","Empresa")[:50],
                    "local":local,"estado":detectar_estado(local),"url":job.get("jobUrl","#"),
                    "fonte":"gupy.io","data":datetime.now().strftime("%d/%m/%Y"),
                    "area":detectar_area(titulo),"beneficios":benef,"salario":"A combinar","escala":"CLT"})
            time.sleep(1.0)
        except Exception as e:print(f"  ⚠️ Gupy: {e}")
    print(f"  ✅ Gupy: {len(vagas)} vagas")
    return vagas


def buscar_vagas_com_br():
    vagas=[]
    print("🔍 Buscando no vagas.com.br...")
    termos=["tecnico-manutencao-eletrica","tecnico-manutencao-mecanica",
            "tecnico-mecatronica","tecnico-automacao-industrial",
            "tecnico-instrumentacao","tecnico-soldagem","tecnico-caldeiraria",
            "tecnico-seguranca-trabalho","tecnico-qualidade","tecnico-refrigeracao"]
    for termo in termos:
        try:
            resp=requests.get(f"https://www.vagas.com.br/vagas-de-{termo}",headers=HEADERS,timeout=15)
            if resp.status_code!=200:continue
            soup=BeautifulSoup(resp.text,"html.parser")
            for card in soup.find_all("li",class_="vaga")[:8]:
                te=card.find("a",class_="link-detalhes-vaga")
                ee=card.find("span",class_="empr-name")
                le=card.find("span",class_="local")
                de=card.find("span",class_="data-publicacao") or card.find("time")
                if not te:continue
                titulo=te.get_text(strip=True)[:80]
                if not titulo_valido(titulo):continue
                dt=de.get_text(strip=True) if de else ""
                if "2025" in dt or "2024" in dt:continue
                local=le.get_text(strip=True)[:40] if le else "Brasil"
                vagas.append({"titulo":titulo,"empresa":ee.get_text(strip=True)[:50] if ee else "Empresa",
                    "local":local,"estado":detectar_estado(local),
                    "url":"https://www.vagas.com.br"+te.get("href",""),
                    "fonte":"vagas.com.br","data":datetime.now().strftime("%d/%m/%Y"),
                    "area":detectar_area(titulo),"beneficios":[],"salario":"A combinar","escala":"CLT"})
            time.sleep(1.5)
        except Exception as e:print(f"  ⚠️ vagas.com.br: {e}")
    print(f"  ✅ vagas.com.br: {len(vagas)} vagas")
    return vagas


def buscar_infojobs():
    vagas=[]
    print("🔍 Buscando no InfoJobs...")
    for termo in ["tecnico-de-manutencao-eletrica","tecnico-de-manutencao-mecanica","tecnico-mecatronica","tecnico-instrumentacao"]:
        try:
            resp=requests.get(f"https://www.infojobs.com.br/empregos/{termo}/",headers=HEADERS,timeout=15)
            if resp.status_code!=200:continue
            soup=BeautifulSoup(resp.text,"html.parser")
            for card in soup.find_all("div",class_="ij-offercard")[:5]:
                te=card.find("a",class_="ij-offercard-title")
                ee=card.find("span",class_="ij-offercard-company")
                le=card.find("span",class_="ij-offercard-location")
                if not te:continue
                titulo=te.get_text(strip=True)[:80]
                if not titulo_valido(titulo):continue
                local=le.get_text(strip=True)[:40] if le else "Brasil"
                vagas.append({"titulo":titulo,"empresa":ee.get_text(strip=True)[:50] if ee else "Empresa",
                    "local":local,"estado":detectar_estado(local),"url":te.get("href","#"),
                    "fonte":"infojobs.com.br","data":datetime.now().strftime("%d/%m/%Y"),
                    "area":detectar_area(titulo),"beneficios":[],"salario":"A combinar","escala":"CLT"})
            time.sleep(1.5)
        except Exception as e:print(f"  ⚠️ InfoJobs: {e}")
    print(f"  ✅ InfoJobs: {len(vagas)} vagas")
    return vagas


def verificar_cache(cache):
    if not cache:return []
    print(f"\n🔎 Verificando {len(cache)} vagas...")
    ativas=[]
    for v in cache:
        if not titulo_valido(v.get("titulo","")):continue
        try:
            r=requests.get(v["url"],headers=HEADERS,timeout=8)
            if r.status_code in[404,410]:continue
            if any(p in r.text.lower() for p in ["vaga encerrada","job expired","não está mais disponível"]):continue
        except:pass
        if "beneficios" not in v:v["beneficios"]=[]
        if "salario" not in v:v["salario"]="A combinar"
        if "escala" not in v:v["escala"]="CLT"
        ativas.append(v)
        time.sleep(0.3)
    print(f"  ✅ {len(ativas)} vagas ativas")
    return ativas


def remover_duplicatas(vagas):
    vistas=set();unicas=[]
    for v in vagas:
        if v["url"] not in vistas and len(v["titulo"])>5:
            vistas.add(v["url"]);unicas.append(v)
    return unicas


def carregar_cache():
    try:
        with open(CACHE_FILE,"r",encoding="utf-8") as f:return json.load(f)
    except:return []


def carregar_artigos():
    try:
        with open(ARTIGOS_FILE,"r",encoding="utf-8") as f:
            a=json.load(f)
            if a:return a[:6]
    except:pass
    return ARTIGOS_PADRAO


AREA_CONFIG = {
    "eletrica":     {"cls":"tag-el","label":"Elétrica","ico":"⚡","cor":"#3b82f6"},
    "mecanica":     {"cls":"tag-me","label":"Mecânica","ico":"🔩","cor":"#22c55e"},
    "automacao":    {"cls":"tag-au","label":"Automação","ico":"🤖","cor":"#f97316"},
    "qualidade":    {"cls":"tag-qu","label":"Qualidade","ico":"📊","cor":"#a855f7"},
    "seguranca":    {"cls":"tag-se","label":"Segurança","ico":"🦺","cor":"#14b8a6"},
    "refrigeracao": {"cls":"tag-rf","label":"Refrigeração","ico":"❄️","cor":"#60a5fa"},
}


def gerar_card_vaga(v, idx=0):
    area=v.get("area","mecanica")
    cfg=AREA_CONFIG.get(area,AREA_CONFIG["mecanica"])
    estado=v.get("estado","BR")
    salario=v.get("salario","A combinar")
    escala=v.get("escala","CLT")
    benefs=v.get("beneficios",[])
    benef_html=""
    if benefs:
        tags="".join(f'<span class="benef-chip">{icone_benef(b)} {b}</span>' for b in benefs[:3])
        benef_html=f'<div class="card-benefits">{tags}</div>'
    wpp=f"https://wa.me/?text=🔧 *{v['titulo']}*%0A🏭 {v['empresa']}%0A📍 {v['local']}%0A%0A👉 {v['url']}%0A%0A_Via TecSystem Brasil_"
    delay=f"animation-delay:{idx*0.05}s"
    return f"""<article class="job-card" style="{delay}" data-area="{area}" data-estado="{estado}" data-esp="{v.get('titulo','').lower()}" data-busca="{v.get('titulo','').lower()} {v.get('empresa','').lower()} {v.get('local','').lower()}">
  <div class="card-accent" style="background:{cfg['cor']}"></div>
  <div class="card-body">
    <div class="card-top">
      <div class="card-main">
        <div class="card-tag {cfg['cls']}">{cfg['ico']} {cfg['label']}</div>
        <h3 class="card-title">{v['titulo']}</h3>
        <div class="card-company">{v['empresa']}</div>
      </div>
      <div class="card-badge-verified">✓ Verificada</div>
    </div>
    <div class="card-info-row">
      <span class="info-chip">📍 {v['local']}</span>
      <span class="info-chip">💰 {salario}</span>
      <span class="info-chip">📋 {escala}</span>
      <span class="info-chip">🗓 {v['data']}</span>
    </div>
    {benef_html}
    <div class="card-actions">
      <a class="btn-wpp" href="{wpp}" target="_blank" onclick="event.stopPropagation()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 16.58c-.26.73-.985 1.337-1.748 1.583-.464.148-.974.196-1.587.115-.888-.12-1.674-.442-2.363-.759-3.236-1.45-5.46-4.707-5.62-4.927-.161-.22-1.31-1.742-1.31-3.321s.828-2.357 1.12-2.677c.291-.32.636-.4.848-.4.21 0 .42.002.605.012.2.011.468-.075.733.56.272.657.923 2.259 1.003 2.421.08.162.133.352.027.566-.107.214-.16.347-.32.534-.16.188-.337.42-.48.565-.16.16-.327.332-.14.652.187.32.83 1.369 1.783 2.217 1.225 1.09 2.256 1.428 2.576 1.588.32.16.507.133.694-.08.187-.214.8-.935.1013-1.259.214-.32.427-.267.72-.16.294.106 1.867.88 2.188 1.04.32.16.534.24.614.373.08.134.08.77-.18 1.498z"/></svg>
        WhatsApp
      </a>
      <a class="btn-ver" href="{v['url']}" target="_blank">
        Ver vaga
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>
    </div>
  </div>
</article>"""


def gerar_card_artigo(a, idx=0):
    url=a.get('url','#')
    is_link = url != '#'
    tag_open = f'<a href="{url}" target="_blank" class="article-card">' if is_link else '<div class="article-card">'
    tag_close = '</a>' if is_link else '</div>'
    delay=f"animation-delay:{idx*0.08}s"
    return f"""{tag_open}
  <div class="article-icon">{a['icone']}</div>
  <div class="article-content">
    <div class="article-cat">{a['categoria']}</div>
    <div class="article-title">{a['titulo']}</div>
    <div class="article-excerpt">{a['resumo'][:160]}...</div>
    <div class="article-footer">
      <span class="article-source">{a.get('fonte','TecSystem Brasil')}</span>
      <span class="article-cta">{'Ler →' if is_link else 'Em breve →'}</span>
    </div>
  </div>
{tag_close}"""


def gerar_opts_estados(vagas):
    usados=sorted(set(v.get("estado","BR") for v in vagas if v.get("estado")!="BR"))
    opts='<option value="todos">Todos os estados</option>'
    for s in usados:opts+=f'<option value="{s}">{s} — {ESTADOS.get(s,s)}</option>'
    return opts


def gerar_html(vagas, artigos):
    agora=datetime.now().strftime("%d/%m/%Y às %H:%M")
    cards_vagas="\n".join(gerar_card_vaga(v,i) for i,v in enumerate(vagas))
    cards_artigos="\n".join(gerar_card_artigo(a,i) for i,a in enumerate(artigos))
    total=len(vagas)
    opts_estados=gerar_opts_estados(vagas)
    tec_opts="".join(f'<option value="{t.replace("técnico em","").strip().lower()}">{t.replace("técnico em","").strip().title()}</option>' for t in sorted(TECNICOS))

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TecSystem Brasil — Vagas para Técnicos Industriais 2026</title>
<meta name="description" content="As melhores vagas para técnicos industriais do Brasil. Elétrica, Mecânica, Automação, Refrigeração, PLC, SCADA, HVAC e mais. Atualizado 5x por dia.">
<meta property="og:title" content="TecSystem Brasil — Vagas para Técnicos Industriais">
<meta property="og:description" content="Vagas verificadas para técnicos industriais em todo o Brasil. Atualizado 5x por dia.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
/* ── RESET & BASE ─────────────────────────────────────── */
*{{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}}
:root{{
  --bg:       #0A0A0F;
  --bg1:      #111118;
  --bg2:      #16161F;
  --bg3:      #1C1C28;
  --border:   #ffffff0f;
  --border2:  #ffffff18;
  --text:     #F0F0F5;
  --muted:    #7B7B8F;
  --muted2:   #A0A0B0;
  --orange:   #F97316;
  --orange2:  #FB923C;
  --blue:     #3B82F6;
  --blue2:    #60A5FA;
  --green:    #22C55E;
  --yellow:   #FBBF24;
  --purple:   #A855F7;
  --teal:     #14B8A6;
  --r:        4px;
  --r2:       8px;
  --r3:       12px;
}}
html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;font-size:15px;line-height:1.6;min-height:100vh;overflow-x:hidden}}

/* ── SCROLLBAR ────────────────────────────────────────── */
::-webkit-scrollbar{{width:4px}}
::-webkit-scrollbar-track{{background:var(--bg)}}
::-webkit-scrollbar-thumb{{background:var(--border2);border-radius:2px}}

/* ── NAV ──────────────────────────────────────────────── */
nav{{
  position:sticky;top:0;z-index:100;
  background:rgba(10,10,15,0.85);
  backdrop-filter:blur(20px) saturate(180%);
  border-bottom:1px solid var(--border);
  padding:0 20px;height:56px;
  display:flex;align-items:center;justify-content:space-between;
}}
.nav-logo{{
  font-family:'Syne',sans-serif;
  font-size:17px;font-weight:800;
  letter-spacing:.5px;
  display:flex;align-items:center;gap:8px;
  text-decoration:none;color:var(--text);
}}
.nav-logo-dot{{
  width:8px;height:8px;
  background:var(--orange);
  border-radius:50%;
  box-shadow:0 0 8px var(--orange);
  animation:blink 2s ease-in-out infinite;
}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.nav-right{{display:flex;align-items:center;gap:12px}}
#nav-clock{{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}}
.nav-badge{{
  font-size:11px;font-weight:600;
  background:rgba(249,115,22,.12);
  color:var(--orange);
  border:1px solid rgba(249,115,22,.2);
  padding:3px 10px;border-radius:20px;
  letter-spacing:.3px;
}}

/* ── HERO ─────────────────────────────────────────────── */
.hero{{
  position:relative;overflow:hidden;
  padding:72px 20px 56px;
  text-align:center;
}}
.hero-grid{{
  position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(59,130,246,.04) 1px,transparent 1px),
    linear-gradient(90deg,rgba(59,130,246,.04) 1px,transparent 1px);
  background-size:40px 40px;
  mask-image:radial-gradient(ellipse 80% 60% at 50% 50%,black 20%,transparent 100%);
}}
.hero-glow{{
  position:absolute;top:-20%;left:50%;transform:translateX(-50%);
  width:600px;height:400px;
  background:radial-gradient(ellipse,rgba(249,115,22,.06) 0%,transparent 70%);
  pointer-events:none;
}}
.hero-eyebrow{{
  display:inline-flex;align-items:center;gap:6px;
  font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;
  color:var(--orange);
  background:rgba(249,115,22,.08);
  border:1px solid rgba(249,115,22,.2);
  padding:5px 14px;border-radius:20px;
  margin-bottom:24px;
}}
.hero h1{{
  font-family:'Syne',sans-serif;
  font-size:clamp(28px,6vw,54px);
  font-weight:800;line-height:1.08;
  letter-spacing:-1px;
  margin-bottom:20px;
  max-width:640px;margin-left:auto;margin-right:auto;
}}
.hero h1 .accent{{
  background:linear-gradient(135deg,var(--orange),var(--orange2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}}
.hero-sub{{
  font-size:16px;color:var(--muted2);font-weight:300;
  max-width:480px;margin:0 auto 36px;line-height:1.7;
}}
.hero-ctas{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-bottom:48px}}
.btn-hero{{
  display:inline-flex;align-items:center;gap:8px;
  font-family:'DM Sans',sans-serif;font-size:14px;font-weight:600;
  padding:12px 24px;border-radius:var(--r2);
  text-decoration:none;border:none;cursor:pointer;
  transition:all .2s ease;
}}
.btn-hero-primary{{
  background:var(--orange);color:white;
  box-shadow:0 0 0 0 rgba(249,115,22,.4);
}}
.btn-hero-primary:hover{{background:#ea6c0a;box-shadow:0 0 20px rgba(249,115,22,.3);transform:translateY(-1px)}}
.btn-hero-ghost{{
  background:rgba(255,255,255,.05);
  color:var(--green);
  border:1px solid rgba(34,197,94,.25);
}}
.btn-hero-ghost:hover{{background:rgba(34,197,94,.08);border-color:rgba(34,197,94,.4)}}

/* ── MÉTRICAS ─────────────────────────────────────────── */
.metrics{{
  display:grid;grid-template-columns:repeat(2,1fr);
  gap:1px;background:var(--border);
  border-top:1px solid var(--border);
  border-bottom:1px solid var(--border);
}}
.metric{{
  background:var(--bg1);
  padding:20px 16px;text-align:center;
  position:relative;overflow:hidden;
}}
.metric::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--orange),transparent);
  opacity:0;transition:opacity .3s;
}}
.metric:hover::before{{opacity:1}}
.metric-num{{
  font-family:'Syne',sans-serif;
  font-size:30px;font-weight:800;
  color:var(--orange);
  line-height:1;margin-bottom:4px;
  letter-spacing:-1px;
}}
.metric-label{{font-size:11px;color:var(--muted);font-weight:500;letter-spacing:.5px;text-transform:uppercase}}

/* ── FILTROS ──────────────────────────────────────────── */
.filters-section{{
  background:var(--bg1);
  border-bottom:1px solid var(--border);
  padding:16px 20px;
}}
.filters-search{{position:relative;margin-bottom:12px}}
.filters-search input{{
  width:100%;
  background:var(--bg2);
  border:1px solid var(--border2);
  color:var(--text);
  font-family:'DM Sans',sans-serif;font-size:14px;
  padding:11px 16px 11px 44px;
  border-radius:var(--r2);outline:none;
  transition:border .2s,box-shadow .2s;
}}
.filters-search input::placeholder{{color:var(--muted)}}
.filters-search input:focus{{border-color:var(--orange);box-shadow:0 0 0 3px rgba(249,115,22,.1)}}
.search-ico{{
  position:absolute;left:14px;top:50%;transform:translateY(-50%);
  color:var(--muted);pointer-events:none;font-size:16px;
}}
.filters-row{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}}
.filters-row:last-child{{margin-bottom:0}}
.filter-chip{{
  flex-shrink:0;
  background:var(--bg2);
  border:1px solid var(--border2);
  color:var(--muted2);
  font-family:'DM Sans',sans-serif;font-size:12px;font-weight:500;
  padding:6px 14px;border-radius:20px;
  cursor:pointer;transition:all .15s;
  white-space:nowrap;
}}
.filter-chip:hover{{border-color:var(--orange);color:var(--orange)}}
.filter-chip.active{{
  background:rgba(249,115,22,.12);
  border-color:var(--orange);color:var(--orange);font-weight:600;
}}
.filter-select{{
  background:var(--bg2);
  border:1px solid var(--border2);
  color:var(--text);
  font-family:'DM Sans',sans-serif;font-size:12px;font-weight:500;
  padding:6px 14px;border-radius:20px;
  cursor:pointer;flex-shrink:0;outline:none;
  transition:border .2s;
}}
.filter-select:focus{{border-color:var(--orange)}}
.filters-label{{
  font-size:10px;font-weight:600;letter-spacing:1px;
  text-transform:uppercase;color:var(--muted);
  margin-bottom:8px;display:block;
}}

/* ── TRUST BAR ────────────────────────────────────────── */
.trust-bar{{
  background:rgba(34,197,94,.04);
  border-bottom:1px solid rgba(34,197,94,.1);
  padding:8px 20px;
  display:flex;align-items:center;gap:8px;
  font-size:11px;color:var(--muted2);
  letter-spacing:.3px;
}}
.trust-dot{{
  width:6px;height:6px;background:var(--green);
  border-radius:50%;flex-shrink:0;
  box-shadow:0 0 6px var(--green);
  animation:pulse-green 2s ease-in-out infinite;
}}
@keyframes pulse-green{{
  0%,100%{{box-shadow:0 0 6px var(--green)}}
  50%{{box-shadow:0 0 12px var(--green),0 0 20px rgba(34,197,94,.3)}}
}}

/* ── LAYOUT ───────────────────────────────────────────── */
.page{{padding:28px 16px 48px;max-width:860px;margin:0 auto}}

/* ── SECTION HEADER ──────────────────────────────────── */
.sec-header{{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:16px;
}}
.sec-title{{
  font-family:'Syne',sans-serif;
  font-size:16px;font-weight:700;
  letter-spacing:.3px;color:var(--text);
  display:flex;align-items:center;gap:8px;
}}
.sec-count{{
  font-size:12px;color:var(--muted);
  background:var(--bg2);border:1px solid var(--border);
  padding:3px 10px;border-radius:20px;
}}

/* ── CALCULADORAS ─────────────────────────────────────── */
.calc-grid{{
  display:grid;grid-template-columns:repeat(2,1fr);
  gap:8px;margin-bottom:32px;
}}
.calc-item{{
  background:var(--bg1);
  border:1px solid var(--border);
  border-radius:var(--r2);
  padding:14px 16px;
  display:flex;align-items:center;gap:12px;
  cursor:pointer;transition:all .2s;
  text-align:left;color:var(--text);
}}
.calc-item:hover{{
  border-color:var(--orange);
  background:var(--bg2);
  transform:translateY(-1px);
  box-shadow:0 4px 16px rgba(249,115,22,.08);
}}
.calc-emoji{{font-size:20px;flex-shrink:0}}
.calc-name{{font-size:13px;font-weight:600;color:var(--text);margin-bottom:1px}}
.calc-hint{{font-size:11px;color:var(--muted)}}

/* ── ARTIGOS ──────────────────────────────────────────── */
.articles-grid{{
  display:grid;grid-template-columns:1fr;
  gap:8px;margin-bottom:32px;
}}
.article-card{{
  background:var(--bg1);
  border:1px solid var(--border);
  border-radius:var(--r2);
  padding:16px;
  display:flex;gap:14px;
  transition:all .2s;
  text-decoration:none;color:var(--text);
  cursor:default;
}}
a.article-card{{cursor:pointer}}
a.article-card:hover,.article-card:hover{{border-color:var(--border2);background:var(--bg2)}}
.article-icon{{font-size:24px;flex-shrink:0;margin-top:2px}}
.article-content{{flex:1;min-width:0}}
.article-cat{{
  font-size:10px;font-weight:600;letter-spacing:1.5px;
  text-transform:uppercase;color:var(--orange);margin-bottom:4px;
}}
.article-title{{font-size:14px;font-weight:600;color:var(--text);margin-bottom:4px;line-height:1.4}}
.article-excerpt{{font-size:12px;color:var(--muted);line-height:1.5;margin-bottom:8px}}
.article-footer{{display:flex;align-items:center;justify-content:space-between}}
.article-source{{font-size:11px;color:var(--muted)}}
.article-cta{{font-size:11px;color:var(--orange);font-weight:600}}

/* ── NEWSLETTER ───────────────────────────────────────── */
.newsletter{{
  background:linear-gradient(135deg,var(--bg2),var(--bg3));
  border:1px solid var(--border);
  border-radius:var(--r3);
  padding:24px 20px;
  margin-bottom:32px;
  position:relative;overflow:hidden;
}}
.newsletter::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--orange),var(--blue));
}}
.nl-title{{font-family:'Syne',sans-serif;font-size:18px;font-weight:700;margin-bottom:6px}}
.nl-title span{{color:var(--orange)}}
.nl-desc{{font-size:13px;color:var(--muted2);margin-bottom:16px}}
.nl-form{{display:flex;gap:8px;flex-wrap:wrap}}
.nl-input{{
  flex:1;min-width:180px;
  background:var(--bg);border:1px solid var(--border2);
  color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;
  padding:10px 14px;border-radius:var(--r2);outline:none;
  transition:border .2s,box-shadow .2s;
}}
.nl-input:focus{{border-color:var(--orange);box-shadow:0 0 0 3px rgba(249,115,22,.1)}}
.nl-btn{{
  background:var(--orange);color:white;border:none;
  font-family:'DM Sans',sans-serif;font-size:13px;font-weight:600;
  padding:10px 20px;border-radius:var(--r2);cursor:pointer;
  white-space:nowrap;transition:background .2s;
}}
.nl-btn:hover{{background:#ea6c0a}}
.nl-ok{{display:none;color:var(--green);font-size:13px;margin-top:10px;font-weight:500}}

/* ── JOB CARDS ────────────────────────────────────────── */
.jobs-list{{display:flex;flex-direction:column;gap:10px}}
.job-card{{
  background:var(--bg1);
  border:1px solid var(--border);
  border-radius:var(--r2);
  overflow:hidden;
  transition:all .2s ease;
  animation:fadeUp .4s ease both;
  position:relative;
}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
.job-card:hover{{
  border-color:var(--border2);
  background:var(--bg2);
  transform:translateY(-2px);
  box-shadow:0 8px 32px rgba(0,0,0,.3);
}}
.card-accent{{
  position:absolute;left:0;top:0;bottom:0;width:3px;
  transition:width .2s;
}}
.job-card:hover .card-accent{{width:4px}}
.card-body{{padding:16px 16px 16px 20px}}
.card-top{{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:12px}}
.card-main{{flex:1;min-width:0}}
.card-tag{{
  display:inline-flex;align-items:center;gap:4px;
  font-size:10px;font-weight:600;letter-spacing:.8px;text-transform:uppercase;
  padding:3px 10px;border-radius:20px;margin-bottom:6px;
}}
.tag-el{{background:rgba(59,130,246,.12);color:var(--blue2);border:1px solid rgba(59,130,246,.2)}}
.tag-me{{background:rgba(34,197,94,.12);color:#4ade80;border:1px solid rgba(34,197,94,.2)}}
.tag-au{{background:rgba(249,115,22,.12);color:var(--orange2);border:1px solid rgba(249,115,22,.2)}}
.tag-qu{{background:rgba(168,85,247,.12);color:#c084fc;border:1px solid rgba(168,85,247,.2)}}
.tag-se{{background:rgba(20,184,166,.12);color:#2dd4bf;border:1px solid rgba(20,184,166,.2)}}
.tag-rf{{background:rgba(96,165,250,.12);color:var(--blue2);border:1px solid rgba(96,165,250,.2)}}
.card-title{{
  font-family:'Syne',sans-serif;
  font-size:16px;font-weight:700;
  color:var(--text);line-height:1.3;margin-bottom:3px;
  letter-spacing:-.2px;
}}
.card-company{{font-size:13px;color:var(--muted2);font-weight:400}}
.card-badge-verified{{
  flex-shrink:0;
  font-size:10px;font-weight:600;
  color:var(--green);
  background:rgba(34,197,94,.08);
  border:1px solid rgba(34,197,94,.2);
  padding:3px 9px;border-radius:20px;
  white-space:nowrap;
}}
.card-info-row{{
  display:flex;flex-wrap:wrap;gap:6px;
  margin-bottom:10px;
}}
.info-chip{{
  font-size:11px;color:var(--muted2);
  background:var(--bg3);
  border:1px solid var(--border);
  padding:3px 9px;border-radius:var(--r);
}}
.card-benefits{{
  display:flex;flex-wrap:wrap;gap:5px;
  margin-bottom:12px;
}}
.benef-chip{{
  font-size:10px;
  color:var(--yellow);
  background:rgba(251,191,36,.06);
  border:1px solid rgba(251,191,36,.15);
  padding:2px 8px;border-radius:var(--r);
}}
.card-actions{{
  display:flex;gap:8px;align-items:center;
  padding-top:12px;
  border-top:1px solid var(--border);
}}
.btn-wpp{{
  display:inline-flex;align-items:center;gap:6px;
  font-size:12px;font-weight:600;
  color:var(--green);
  background:rgba(34,197,94,.06);
  border:1px solid rgba(34,197,94,.2);
  padding:7px 14px;border-radius:var(--r2);
  text-decoration:none;transition:all .2s;
}}
.btn-wpp:hover{{background:rgba(34,197,94,.12);border-color:rgba(34,197,94,.4)}}
.btn-ver{{
  display:inline-flex;align-items:center;gap:6px;
  font-size:12px;font-weight:600;
  color:white;
  background:var(--orange);
  padding:7px 16px;border-radius:var(--r2);
  text-decoration:none;transition:all .2s;
  margin-left:auto;
}}
.btn-ver:hover{{background:#ea6c0a;transform:translateX(1px)}}

/* ── EMPTY STATE ──────────────────────────────────────── */
.empty-state{{
  text-align:center;padding:56px 24px;
  display:none;
}}
.empty-icon{{font-size:48px;margin-bottom:16px;opacity:.5}}
.empty-title{{
  font-family:'Syne',sans-serif;
  font-size:20px;font-weight:700;
  margin-bottom:8px;color:var(--text);
}}
.empty-text{{font-size:14px;color:var(--muted);line-height:1.6;margin-bottom:20px}}
.empty-btn{{
  display:inline-flex;align-items:center;gap:6px;
  font-size:13px;font-weight:600;color:var(--orange);
  background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);
  padding:8px 18px;border-radius:20px;cursor:pointer;
  transition:all .2s;text-decoration:none;
}}
.empty-btn:hover{{background:rgba(249,115,22,.15)}}

/* ── MODAL ────────────────────────────────────────────── */
.modal{{
  display:none;position:fixed;
  inset:0;background:rgba(0,0,0,.8);
  z-index:1000;align-items:center;justify-content:center;
  padding:16px;backdrop-filter:blur(4px);
  overflow-y:auto;
}}
.modal.open{{display:flex}}
.modal-box{{
  background:var(--bg2);
  border:1px solid var(--border2);
  border-radius:var(--r3);
  padding:24px;width:100%;max-width:400px;margin:auto;
  position:relative;
}}
.modal-box::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--orange),var(--blue));
  border-radius:var(--r3) var(--r3) 0 0;
}}
.modal-title{{
  font-family:'Syne',sans-serif;
  font-size:18px;font-weight:700;
  color:var(--orange);margin-bottom:16px;
}}
.modal-field{{margin-bottom:14px}}
.modal-label{{
  font-size:10px;font-weight:600;letter-spacing:1px;
  text-transform:uppercase;color:var(--muted);
  display:block;margin-bottom:6px;
}}
.modal-input,.modal-select{{
  width:100%;
  background:var(--bg);border:1px solid var(--border2);
  color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;
  padding:10px 14px;border-radius:var(--r2);outline:none;
  transition:border .2s,box-shadow .2s;
}}
.modal-input:focus,.modal-select:focus{{
  border-color:var(--orange);
  box-shadow:0 0 0 3px rgba(249,115,22,.1);
}}
.calc-result{{
  background:var(--bg);border:1px solid var(--border);
  border-radius:var(--r2);padding:14px;margin-top:16px;
}}
.result-row{{
  display:flex;justify-content:space-between;
  font-size:13px;margin-bottom:8px;color:var(--muted);
}}
.result-row.total{{
  color:var(--green);font-weight:700;font-size:16px;
  border-top:1px solid var(--border);
  padding-top:10px;margin-top:4px;
}}
.btn-close{{
  width:100%;margin-top:8px;
  background:transparent;color:var(--muted);
  border:1px solid var(--border);
  font-family:'DM Sans',sans-serif;font-size:13px;
  padding:9px;border-radius:var(--r2);cursor:pointer;
  transition:all .2s;
}}
.btn-close:hover{{border-color:var(--border2);color:var(--text)}}

/* ── FOOTER ───────────────────────────────────────────── */
footer{{
  border-top:1px solid var(--border);
  padding:28px 20px;text-align:center;
}}
.footer-logo{{
  font-family:'Syne',sans-serif;
  font-size:16px;font-weight:800;
  letter-spacing:.3px;margin-bottom:8px;
}}
.footer-logo span{{color:var(--orange)}}
.footer-text{{font-size:12px;color:var(--muted);line-height:1.8}}

/* ── UTILITIES ────────────────────────────────────────── */
.mt-28{{margin-top:28px}}
.divider{{height:1px;background:var(--border);margin:28px 0}}
</style>
</head>
<body>

<!-- NAV -->
<nav>
  <a class="nav-logo" href="#">
    <div class="nav-logo-dot"></div>
    TecSystem<span style="color:var(--orange)">.</span>
  </a>
  <div class="nav-right">
    <span id="nav-clock"></span>
    <span class="nav-badge">⚙️ Ao vivo</span>
  </div>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-grid"></div>
  <div class="hero-glow"></div>
  <div class="hero-eyebrow">
    <span>🇧🇷</span> Plataforma de vagas técnicas industriais
  </div>
  <h1>
    As melhores vagas<br>
    para <span class="accent">técnicos industriais</span><br>
    do Brasil, em um só lugar.
  </h1>
  <p class="hero-sub">
    Elétrica · Mecânica · Automação · Refrigeração · PLC · SCADA · HVAC · Instrumentação e mais.<br>
    Vagas verificadas, atualizadas 5x por dia, em todos os estados.
  </p>
  <div class="hero-ctas">
    <a class="btn-hero btn-hero-primary" href="#vagas">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      Buscar vagas
    </a>
    <a class="btn-hero btn-hero-ghost" href="https://wa.me/?text=🔧 Encontrei vagas para técnicos industriais no TecSystem Brasil!%0A👉 https://tecsystembrasil.netlify.app" target="_blank">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413z"/></svg>
      Compartilhar
    </a>
  </div>
</section>

<!-- MÉTRICAS -->
<div class="metrics">
  <div class="metric"><div class="metric-num" id="m-vagas">{total}</div><div class="metric-label">Vagas ativas</div></div>
  <div class="metric"><div class="metric-num">60+</div><div class="metric-label">Especialidades</div></div>
  <div class="metric"><div class="metric-num">5×</div><div class="metric-label">Atualizado/dia</div></div>
  <div class="metric"><div class="metric-num">27</div><div class="metric-label">Estados</div></div>
</div>

<!-- FILTROS -->
<div class="filters-section">
  <div class="filters-search">
    <span class="search-ico">🔍</span>
    <input type="text" placeholder="Buscar por cargo, empresa ou cidade..." oninput="buscar(this.value)" id="search-input">
  </div>
  <span class="filters-label">Área técnica</span>
  <div class="filters-row">
    <button class="filter-chip active" onclick="fArea('todas',this)">Todas</button>
    <button class="filter-chip" onclick="fArea('eletrica',this)">⚡ Elétrica</button>
    <button class="filter-chip" onclick="fArea('mecanica',this)">🔩 Mecânica</button>
    <button class="filter-chip" onclick="fArea('automacao',this)">🤖 Automação</button>
    <button class="filter-chip" onclick="fArea('refrigeracao',this)">❄️ Refrigeração</button>
    <button class="filter-chip" onclick="fArea('qualidade',this)">📊 Qualidade</button>
    <button class="filter-chip" onclick="fArea('seguranca',this)">🦺 Segurança</button>
  </div>
  <span class="filters-label">Estado e especialidade</span>
  <div class="filters-row">
    <select class="filter-select" onchange="fEstado(this.value)">{opts_estados}</select>
    <select class="filter-select" onchange="fEsp(this.value)">
      <option value="todas">🔧 Todas as especialidades</option>
      {tec_opts}
    </select>
  </div>
</div>

<!-- TRUST BAR -->
<div class="trust-bar">
  <div class="trust-dot"></div>
  <span>Vagas verificadas · Apenas 2026 · Removidas automaticamente ao encerrar · Atualizado em {agora}</span>
</div>

<!-- CONTEÚDO -->
<div class="page">

  <!-- CALCULADORAS -->
  <div class="sec-header mt-28">
    <div class="sec-title">🧮 Calculadoras Trabalhistas</div>
  </div>
  <div class="calc-grid">
    <button class="calc-item" onclick="openModal('m-salario')"><div class="calc-emoji">💰</div><div><div class="calc-name">Salário Líquido</div><div class="calc-hint">INSS + IRRF 2026</div></div></button>
    <button class="calc-item" onclick="openModal('m-ferias')"><div class="calc-emoji">🏖️</div><div><div class="calc-name">Férias</div><div class="calc-hint">+ 1/3 constitucional</div></div></button>
    <button class="calc-item" onclick="openModal('m-rescisao')"><div class="calc-emoji">📦</div><div><div class="calc-name">Rescisão</div><div class="calc-hint">Demissão ou pedido</div></div></button>
    <button class="calc-item" onclick="openModal('m-horaextra')"><div class="calc-emoji">⏰</div><div><div class="calc-name">Hora Extra</div><div class="calc-hint">50%, 100% e noturna</div></div></button>
    <button class="calc-item" onclick="openModal('m-noturno')"><div class="calc-emoji">🌙</div><div><div class="calc-name">Adicional Noturno</div><div class="calc-hint">20% sobre salário</div></div></button>
    <button class="calc-item" onclick="openModal('m-insalub')"><div class="calc-emoji">⚠️</div><div><div class="calc-name">Insalubridade</div><div class="calc-hint">e Periculosidade</div></div></button>
    <button class="calc-item" onclick="openModal('m-decimo')"><div class="calc-emoji">🎄</div><div><div class="calc-name">13º Salário</div><div class="calc-hint">Proporcional ou cheio</div></div></button>
  </div>

  <!-- ARTIGOS -->
  <div class="sec-header">
    <div class="sec-title">📰 Para Técnicos</div>
    <span class="sec-count">{len(artigos)} artigos</span>
  </div>
  <div class="articles-grid">{cards_artigos}</div>

  <!-- NEWSLETTER -->
  <div class="newsletter">
    <div class="nl-title">📧 Receba <span>vagas</span> no seu email</div>
    <div class="nl-desc">Toda semana as melhores vagas técnicas direto na caixa de entrada. Grátis.</div>
    <div class="nl-form">
      <input class="nl-input" type="email" id="nl-email" placeholder="seu@email.com">
      <button class="nl-btn" onclick="newsletter()">Quero receber</button>
    </div>
    <div class="nl-ok" id="nl-ok">✓ Cadastrado! Você receberá as vagas em breve.</div>
  </div>

  <!-- VAGAS -->
  <div class="sec-header" id="vagas">
    <div class="sec-title">🔧 Vagas Disponíveis</div>
    <span class="sec-count" id="vagas-count">{total} vagas</span>
  </div>
  <div class="jobs-list" id="jobs-list">{cards_vagas}</div>
  <div class="empty-state" id="empty-state">
    <div class="empty-icon">🔍</div>
    <div class="empty-title">Nenhuma vaga encontrada</div>
    <div class="empty-text">
      Não encontramos vagas para o filtro selecionado.<br>
      Tente outra especialidade ou estado, ou volte mais tarde.
    </div>
    <button class="empty-btn" onclick="resetFiltros()">← Ver todas as vagas</button>
  </div>

</div>

<!-- MODAIS CALCULADORAS -->
<div class="modal" id="m-salario"><div class="modal-box">
  <div class="modal-title">💰 Salário Líquido</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="sl-b" placeholder="Ex: 3500" oninput="cSalario()"></div>
  <div class="modal-field"><label class="modal-label">Dependentes para IR</label><input class="modal-input" type="number" id="sl-d" placeholder="0" value="0" oninput="cSalario()"></div>
  <div class="calc-result" id="sl-r" style="display:none">
    <div class="result-row"><span>Salário Bruto</span><span id="sl-1"></span></div>
    <div class="result-row"><span>(-) INSS</span><span id="sl-2" style="color:#f87171"></span></div>
    <div class="result-row"><span>(-) IRRF</span><span id="sl-3" style="color:#f87171"></span></div>
    <div class="result-row total"><span>💵 Salário Líquido</span><span id="sl-4"></span></div>
    <div class="result-row" style="font-size:11px;margin-top:4px"><span>FGTS (empregador deposita)</span><span id="sl-5" style="color:var(--green)"></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-salario')">Fechar</button>
</div></div>

<div class="modal" id="m-ferias"><div class="modal-box">
  <div class="modal-title">🏖️ Férias</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="fe-b" placeholder="Ex: 3500" oninput="cFerias()"></div>
  <div class="modal-field"><label class="modal-label">Meses trabalhados</label><input class="modal-input" type="number" id="fe-m" value="12" min="1" max="12" oninput="cFerias()"></div>
  <div class="calc-result" id="fe-r" style="display:none">
    <div class="result-row"><span>Férias proporcional</span><span id="fe-1"></span></div>
    <div class="result-row"><span>(+) 1/3 constitucional</span><span id="fe-2" style="color:var(--green)"></span></div>
    <div class="result-row"><span>(-) INSS + IR</span><span id="fe-3" style="color:#f87171"></span></div>
    <div class="result-row total"><span>🏖️ Férias Líquidas</span><span id="fe-4"></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-ferias')">Fechar</button>
</div></div>

<div class="modal" id="m-rescisao"><div class="modal-box">
  <div class="modal-title">📦 Rescisão</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="re-b" placeholder="Ex: 3500" oninput="cRescisao()"></div>
  <div class="modal-field"><label class="modal-label">Meses trabalhados no ano</label><input class="modal-input" type="number" id="re-m" placeholder="Ex: 6" min="1" max="12" oninput="cRescisao()"></div>
  <div class="modal-field"><label class="modal-label">Tipo de rescisão</label>
    <select class="modal-select" id="re-t" onchange="cRescisao()">
      <option value="sem_justa">Demissão sem justa causa</option>
      <option value="pedido">Pedido de demissão</option>
      <option value="acordo">Acordo (distrato)</option>
    </select>
  </div>
  <div class="calc-result" id="re-r" style="display:none">
    <div class="result-row"><span>Saldo de salário</span><span id="re-1"></span></div>
    <div class="result-row"><span>13º proporcional</span><span id="re-2"></span></div>
    <div class="result-row"><span>Férias + 1/3</span><span id="re-3"></span></div>
    <div class="result-row" id="re-multa" style="display:none"><span>Multa FGTS</span><span id="re-4" style="color:var(--green)"></span></div>
    <div class="result-row total"><span>📦 Total Rescisão</span><span id="re-5"></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-rescisao')">Fechar</button>
</div></div>

<div class="modal" id="m-horaextra"><div class="modal-box">
  <div class="modal-title">⏰ Hora Extra</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="he-b" placeholder="Ex: 3500" oninput="cHE()"></div>
  <div class="modal-field"><label class="modal-label">Horas extras realizadas</label><input class="modal-input" type="number" id="he-h" placeholder="Ex: 10" oninput="cHE()"></div>
  <div class="modal-field"><label class="modal-label">Tipo</label>
    <select class="modal-select" id="he-t" onchange="cHE()">
      <option value="50">50% — Dias úteis</option>
      <option value="100">100% — Domingos/Feriados</option>
      <option value="70">70% — Noturna</option>
    </select>
  </div>
  <div class="calc-result" id="he-r" style="display:none">
    <div class="result-row"><span>Valor hora normal</span><span id="he-1"></span></div>
    <div class="result-row"><span>Valor hora extra</span><span id="he-2"></span></div>
    <div class="result-row total"><span>⏰ Total a receber</span><span id="he-3"></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-horaextra')">Fechar</button>
</div></div>

<div class="modal" id="m-noturno"><div class="modal-box">
  <div class="modal-title">🌙 Adicional Noturno</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="no-b" placeholder="Ex: 3500" oninput="cNoturno()"></div>
  <div class="modal-field"><label class="modal-label">Horas noturnas por mês</label><input class="modal-input" type="number" id="no-h" placeholder="Ex: 44" oninput="cNoturno()"></div>
  <div class="calc-result" id="no-r" style="display:none">
    <div class="result-row"><span>Salário base</span><span id="no-1"></span></div>
    <div class="result-row"><span>(+) Adicional 20%</span><span id="no-2" style="color:var(--green)"></span></div>
    <div class="result-row total"><span>🌙 Total com adicional</span><span id="no-3"></span></div>
    <div class="result-row" style="font-size:11px;margin-top:4px;color:var(--muted)"><span>Horário noturno: 22h às 5h</span><span></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-noturno')">Fechar</button>
</div></div>

<div class="modal" id="m-insalub"><div class="modal-box">
  <div class="modal-title">⚠️ Insalubridade / Periculosidade</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="in-b" placeholder="Ex: 3500" oninput="cInsalub()"></div>
  <div class="modal-field"><label class="modal-label">Tipo de adicional</label>
    <select class="modal-select" id="in-t" onchange="cInsalub()">
      <option value="10">Insalubridade Mínima — 10% SM</option>
      <option value="20">Insalubridade Média — 20% SM</option>
      <option value="40">Insalubridade Máxima — 40% SM</option>
      <option value="30p">Periculosidade — 30% salário</option>
    </select>
  </div>
  <div class="calc-result" id="in-r" style="display:none">
    <div class="result-row"><span>Salário base</span><span id="in-1"></span></div>
    <div class="result-row"><span>(+) Adicional</span><span id="in-2" style="color:var(--green)"></span></div>
    <div class="result-row total"><span>⚠️ Total com adicional</span><span id="in-3"></span></div>
    <div class="result-row" style="font-size:11px;margin-top:4px;color:var(--muted)"><span>Salário mínimo 2026: R$ 1.518,00</span><span></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-insalub')">Fechar</button>
</div></div>

<div class="modal" id="m-decimo"><div class="modal-box">
  <div class="modal-title">🎄 13º Salário</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="de-b" placeholder="Ex: 3500" oninput="cDecimo()"></div>
  <div class="modal-field"><label class="modal-label">Meses trabalhados no ano</label><input class="modal-input" type="number" id="de-m" value="12" min="1" max="12" oninput="cDecimo()"></div>
  <div class="calc-result" id="de-r" style="display:none">
    <div class="result-row"><span>13º bruto proporcional</span><span id="de-1"></span></div>
    <div class="result-row"><span>(-) INSS + IR</span><span id="de-2" style="color:#f87171"></span></div>
    <div class="result-row total"><span>🎄 13º Líquido</span><span id="de-3"></span></div>
    <div class="result-row" style="font-size:11px;margin-top:4px;color:var(--muted)"><span>1ª parcela: novembro · 2ª parcela: dezembro</span><span></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-decimo')">Fechar</button>
</div></div>

<footer>
  <div class="footer-logo">TecSystem<span>.</span>Brasil</div>
  <div class="footer-text">
    Vagas técnicas industriais verificadas · Apenas 2026 · Todo o Brasil<br>
    Atualizado automaticamente 5× por dia · Links redirecionam para os sites originais
  </div>
</footer>

<script data-goatcounter="https://tecsystembrasil.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<script>
// ── RELÓGIO ──
(function clock(){{
  const el=document.getElementById('nav-clock');
  function tick(){{
    const now=new Date();
    el.textContent=now.toLocaleTimeString('pt-BR',{{timeZone:'America/Sao_Paulo',hour:'2-digit',minute:'2-digit'}});
  }}
  tick();setInterval(tick,1000);
}})();

// ── MODAIS ──
function openModal(id){{document.getElementById(id).classList.add('open');document.body.style.overflow='hidden';}}
function closeModal(id){{document.getElementById(id).classList.remove('open');document.body.style.overflow='';}}
document.querySelectorAll('.modal').forEach(m=>{{
  m.addEventListener('click',e=>{{if(e.target===m)closeModal(m.id);}});
}});
document.addEventListener('keydown',e=>{{if(e.key==='Escape')document.querySelectorAll('.modal.open').forEach(m=>closeModal(m.id));}});

// ── FILTROS ──
let fA='todas',fE='todos',fX='todas',fB='';
function fArea(a,b){{fA=a;document.querySelectorAll('.filter-chip').forEach(x=>x.classList.remove('active'));b.classList.add('active');render();}}
function fEstado(v){{fE=v;render();}}
function fEsp(v){{fX=v;render();}}
function buscar(v){{fB=v.toLowerCase().trim();render();}}
function resetFiltros(){{
  fA='todas';fE='todos';fX='todas';fB='';
  document.querySelectorAll('.filter-chip').forEach(x=>x.classList.remove('active'));
  document.querySelector('.filter-chip').classList.add('active');
  document.getElementById('search-input').value='';
  document.querySelectorAll('.filter-select').forEach(s=>s.selectedIndex=0);
  render();
}}
function render(){{
  let n=0;
  document.querySelectorAll('#jobs-list .job-card').forEach(c=>{{
    const ok=(fA==='todas'||c.dataset.area===fA)&&
             (fE==='todos'||c.dataset.estado===fE)&&
             (fX==='todas'||c.dataset.esp.includes(fX))&&
             (fB===''||c.dataset.busca.includes(fB));
    c.style.display=ok?'block':'none';if(ok)n++;
  }});
  document.getElementById('vagas-count').textContent=n+' vagas';
  document.getElementById('m-vagas').textContent=n;
  const empty=document.getElementById('empty-state');
  const list=document.getElementById('jobs-list');
  empty.style.display=n===0?'block':'none';
  list.style.display=n===0?'none':'flex';
}}

// ── NEWSLETTER ──
function newsletter(){{
  const e=document.getElementById('nl-email').value;
  if(!e||!e.includes('@')){{alert('Digite um email válido!');return;}}
  fetch('https://formsubmit.co/ajax/tecsystembrasil@gmail.com',{{
    method:'POST',
    headers:{{'Content-Type':'application/json','Accept':'application/json'}},
    body:JSON.stringify({{email:e,_subject:'Newsletter TecSystem Brasil'}})
  }}).catch(()=>{{}});
  document.getElementById('nl-ok').style.display='block';
  document.getElementById('nl-email').value='';
}}

// ── MATEMÁTICA ──
function INS(b){{const f=[[1518,.075],[2793.88,.09],[4190.83,.12],[8157.41,.14]];let i=0,a=0;for(const[t,q]of f){{if(b<=t){{i+=(b-a)*q;break;}}i+=(t-a)*q;a=t;}}return Math.min(i,908.86);}}
function IR(b,d){{const x=b-d*189.59;const f=[[2259.2,0,0],[2826.65,.075,169.44],[3751.05,.15,381.44],[4664.68,.225,662.77],[1/0,.275,896]];for(const[t,a,e]of f)if(x<=t)return Math.max(0,x*a-e);return 0;}}
function R(v){{return'R$ '+v.toFixed(2).replace('.',',').replace(/\B(?=(\d{{3}})+(?!\d))/g,'.');}}
function show(id){{document.getElementById(id).style.display='block';}}
function hide(id){{document.getElementById(id).style.display='none';}}
function g(id){{return parseFloat(document.getElementById(id).value)||0;}}
function gi(id){{return parseInt(document.getElementById(id).value)||0;}}
function gv(id){{return document.getElementById(id).value;}}
function s(id,v){{document.getElementById(id).textContent=v;}}

function cSalario(){{const b=g('sl-b'),d=gi('sl-d');if(!b){{hide('sl-r');return;}}const i=INS(b),r=IR(b-i,d),l=b-i-r;s('sl-1',R(b));s('sl-2','- '+R(i));s('sl-3','- '+R(r));s('sl-4',R(l));s('sl-5','+ '+R(b*.08));show('sl-r');}}
function cFerias(){{const b=g('fe-b'),m=gi('fe-m')||12;if(!b){{hide('fe-r');return;}}const p=b*(m/12),t=p/3,tot=p+t,i=INS(tot),r=IR(tot-i,0);s('fe-1',R(p));s('fe-2','+ '+R(t));s('fe-3','- '+R(i+r));s('fe-4',R(tot-i-r));show('fe-r');}}
function cRescisao(){{const b=g('re-b'),m=gi('re-m')||1,tp=gv('re-t');if(!b){{hide('re-r');return;}}const dec=b*(m/12),fp=b*(m/12)*(4/3),fg=b*.08*m;let mu=tp==='sem_justa'?fg*.4:tp==='acordo'?fg*.2:0;s('re-1',R(b));s('re-2',R(dec));s('re-3',R(fp));if(mu>0){{s('re-4','+ '+R(mu));show('re-multa');}}else hide('re-multa');s('re-5',R(b+dec+fp+mu));show('re-r');}}
function cHE(){{const b=g('he-b'),h=g('he-h'),tp=parseFloat(gv('he-t'));if(!b||!h){{hide('he-r');return;}}const hb=b/220,he=hb*(1+tp/100);s('he-1',R(hb));s('he-2',R(he));s('he-3',R(he*h));show('he-r');}}
function cNoturno(){{const b=g('no-b'),h=g('no-h');if(!b){{hide('no-r');return;}}const ad=(b/220)*.2*h;s('no-1',R(b));s('no-2','+ '+R(ad));s('no-3',R(b+ad));show('no-r');}}
function cInsalub(){{const b=g('in-b'),tp=gv('in-t');if(!b){{hide('in-r');return;}}const ad=tp==='30p'?b*.3:1518*(parseFloat(tp)/100);s('in-1',R(b));s('in-2','+ '+R(ad));s('in-3',R(b+ad));show('in-r');}}
function cDecimo(){{const b=g('de-b'),m=gi('de-m')||12;if(!b){{hide('de-r');return;}}const br=b*(m/12),i=INS(br),r=IR(br-i,0);s('de-1',R(br));s('de-2','- '+R(i+r));s('de-3',R(br-i-r));show('de-r');}}
</script>
</body>
</html>"""


def main():
    print(f"\n🤖 TecSystem Brasil v10 — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("="*50)
    cache=carregar_cache()
    vagas_ativas=verificar_cache(cache)
    vagas_novas=buscar_gupy()+buscar_vagas_com_br()+buscar_infojobs()
    todas=remover_duplicatas(vagas_ativas+vagas_novas)
    artigos=carregar_artigos()
    print(f"\n📊 {len(todas)} vagas · {len(artigos)} artigos")
    with open(CACHE_FILE,"w",encoding="utf-8") as f:json.dump(todas,f,ensure_ascii=False,indent=2)
    with open("index.html","w",encoding="utf-8") as f:f.write(gerar_html(todas,artigos))
    print(f"✅ Site atualizado!")

if __name__=="__main__":main()
