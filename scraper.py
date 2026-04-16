"""
TecSystem Brasil - Robô de Vagas v8
=====================================
- Design premium industrial (cinza grafite + laranja elétrico + amarelo)
- Hero forte com frase de impacto e botões de ação
- Filtros separados em blocos (área, estado, especialidade, salário, escala)
- Cards premium com mais informações
- Prova social visual
- Barra de busca
- Newsletter
- Blog
- 7 calculadoras trabalhistas
- GoatCounter
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
    "técnico em climatização industrial","técnico em ar condicionado industrial",
    "técnico em caldeiras industriais","técnico em vapor industrial",
    "técnico em ar comprimido industrial","técnico em tratamento de água industrial",
    "técnico em torres de resfriamento","técnico em utilidades industriais",
    "técnico em manutenção preditiva","técnico em manutenção preventiva",
    "técnico em manutenção corretiva","técnico em vibração industrial",
    "técnico em análise de óleo","técnico em PCM",
    "técnico em confiabilidade industrial","técnico em planejamento de manutenção",
    "técnico em controle de qualidade industrial","técnico em inspeção de qualidade",
    "técnico em ensaios não destrutivos","técnico em metrologia industrial",
    "técnico em segurança do trabalho industrial","técnico em processos industriais",
    "técnico em operação industrial","técnico em montagem industrial",
    "técnico em comissionamento industrial","técnico em metalurgia",
    "técnico em siderurgia","técnico em mineração","técnico em petroquímica",
    "técnico em gás industrial","técnico em fornos industriais",
    "técnico em instalações industriais",
]

PALAVRAS_DESCARTAR = [
    "banco de talentos","banco de talento","encerrad","finalizad",
    "expirad","inativ","cancelad","processo seletivo encerrado",
    "vaga encerrada","não está mais disponível","job expired",
    "talentos 2024","talentos 2025","2023","2024",
]

ANO_ATUAL = "2026"
CACHE_FILE = "vagas_cache.json"

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

ARTIGOS_BLOG = [
    {"titulo":"Quanto ganha um Técnico Eletricista em 2026?","resumo":"Salários de R$ 2.500 a R$ 6.000. Veja o panorama completo do mercado.","icone":"⚡","tag":"Salários"},
    {"titulo":"Como tirar o NR10 em 2026 — Guia completo","resumo":"Obrigatório para instalações elétricas. Saiba onde fazer e quanto custa.","icone":"📋","tag":"Certificações"},
    {"titulo":"Técnico em Automação: a profissão que mais cresce","resumo":"Com a indústria 4.0, técnicos em PLC e SCADA são os mais disputados.","icone":"🤖","tag":"Carreira"},
    {"titulo":"NR12, NR33 e NR35 — Quais certificações valem mais?","resumo":"Descubra quais normas regulamentadoras aumentam seu salário.","icone":"🦺","tag":"Certificações"},
    {"titulo":"Melhores empresas para técnicos em 2026","resumo":"Petrobras, Vale, WEG e outras gigantes que mais contratam técnicos.","icone":"🏭","tag":"Empresas"},
    {"titulo":"Como passar na entrevista técnica industrial","resumo":"Dicas de recrutadores sobre o que as empresas avaliam.","icone":"💼","tag":"Dicas"},
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
    tl=titulo.lower()
    return not any(p in tl for p in PALAVRAS_DESCARTAR)

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


CORES={
    "eletrica":("b-el","⚡","ELÉTRICA"),
    "mecanica":("b-me","🔩","MECÂNICA"),
    "automacao":("b-au","🤖","AUTOMAÇÃO"),
    "qualidade":("b-qu","📊","QUALIDADE"),
    "seguranca":("b-se","🦺","SEGURANÇA"),
    "refrigeracao":("b-rf","❄️","REFRIGERAÇÃO"),
}


def gerar_benef_html(benefs):
    if not benefs:return ""
    tags="".join(f'<span class="benef-tag">{icone_benef(b)} {b}</span>' for b in benefs[:4])
    return f'<div class="beneficios">{tags}</div>'


def gerar_card(v):
    area=v.get("area","mecanica")
    cls,ico,label=CORES.get(area,CORES["mecanica"])
    estado=v.get("estado","BR")
    salario=v.get("salario","A combinar")
    escala=v.get("escala","CLT")
    wpp_txt=f"🔧 *{v['titulo']}*%0A🏭 {v['empresa']}%0A📍 {v['local']}%0A👉 {v['url']}%0A%0A_Via TecSystem Brasil_"
    return f"""<div class="card" data-area="{area}" data-estado="{estado}" data-esp="{v.get('titulo','').lower()}" data-busca="{v.get('titulo','').lower()} {v.get('empresa','').lower()} {v.get('local','').lower()}">
<div class="card-header">
  <div class="card-area-icon">{ico}</div>
  <div class="card-info">
    <div class="card-titulo">{v['titulo']}</div>
    <div class="card-empresa">{v['empresa']}</div>
  </div>
  <div class="badge {cls}">{label}</div>
</div>
<div class="card-meta">
  <span class="meta-item">📍 {v['local']}</span>
  <span class="meta-item">💰 {salario}</span>
  <span class="meta-item">📋 {escala}</span>
  <span class="meta-item">🗓️ {v['data']}</span>
</div>
{gerar_benef_html(v.get('beneficios',[]))}
<div class="card-actions">
  <a class="btn-wpp" href="https://wa.me/?text={wpp_txt}" target="_blank">📲 WhatsApp</a>
  <a class="btn-ver" href="{v['url']}" target="_blank">VER VAGA →</a>
</div>
</div>"""


def gerar_card_blog(a):
    return f"""<div class="blog-card">
<div class="blog-left"><div class="blog-icon">{a['icone']}</div></div>
<div class="blog-right">
  <div class="blog-tag">{a['tag']}</div>
  <div class="blog-titulo">{a['titulo']}</div>
  <div class="blog-resumo">{a['resumo']}</div>
  <div class="blog-link">Em breve →</div>
</div>
</div>"""


def gerar_opts_estados(vagas):
    usados=sorted(set(v.get("estado","BR") for v in vagas if v.get("estado")!="BR"))
    opts='<option value="todos">🌎 Todos os estados</option>'
    for s in usados:opts+=f'<option value="{s}">{s} — {ESTADOS.get(s,s)}</option>'
    return opts


def gerar_html(vagas):
    agora=datetime.now().strftime("%d/%m/%Y às %H:%M")
    cards="\n".join(gerar_card(v) for v in vagas)
    blog_cards="\n".join(gerar_card_blog(a) for a in ARTIGOS_BLOG)
    total=len(vagas)
    opts_estados=gerar_opts_estados(vagas)
    tec_opts="".join(f'<option value="{t.replace("técnico em","").strip().lower()}">{t.replace("técnico em","").strip().title()}</option>' for t in sorted(TECNICOS))

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TecSystem Brasil – Vagas Técnicas Industriais 2026</title>
<meta name="description" content="As melhores vagas para técnicos industriais do Brasil, em um só lugar. Elétrica, Mecânica, Automação, Refrigeração e mais.">
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Barlow:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{
  --bg:#141414;
  --bg2:#1a1a1a;
  --bg3:#222222;
  --card:#1e1e1e;
  --borda:#2e2e2e;
  --borda2:#3a3a3a;
  --laranja:#f97316;
  --amarelo:#fbbf24;
  --azul:#3b82f6;
  --cinza:#888;
  --cinza2:#aaa;
  --branco:#f5f5f5;
  --verde:#22c55e;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--branco);font-family:'Barlow',sans-serif;line-height:1.5}}

/* HEADER */
header{{
  background:rgba(20,20,20,0.95);
  border-bottom:1px solid var(--borda);
  padding:0 20px;height:60px;
  display:flex;align-items:center;justify-content:space-between;
  position:sticky;top:0;z-index:100;
  backdrop-filter:blur(10px);
}}
.logo{{font-family:'Oswald',sans-serif;font-size:20px;font-weight:700;letter-spacing:3px;text-transform:uppercase}}
.logo span{{color:var(--laranja)}}
.logo-sub{{font-size:10px;color:var(--cinza);letter-spacing:2px;font-weight:400}}

/* HERO */
.hero{{
  background:var(--bg);
  padding:48px 20px 40px;
  text-align:center;
  position:relative;
  overflow:hidden;
}}
.hero::before{{
  content:'';position:absolute;top:0;left:0;right:0;bottom:0;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(249,115,22,0.08) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 50%, rgba(59,130,246,0.06) 0%, transparent 60%);
  pointer-events:none;
}}
.hero-tag{{
  display:inline-flex;align-items:center;gap:6px;
  background:rgba(249,115,22,0.1);
  border:1px solid rgba(249,115,22,0.3);
  color:var(--laranja);font-size:11px;font-weight:700;
  letter-spacing:2px;padding:5px 14px;border-radius:2px;
  margin-bottom:20px;text-transform:uppercase;
}}
.hero h1{{
  font-family:'Oswald',sans-serif;
  font-size:clamp(28px,6vw,52px);
  font-weight:700;line-height:1.1;
  letter-spacing:1px;
  margin-bottom:16px;
  text-transform:uppercase;
}}
.hero h1 em{{color:var(--laranja);font-style:normal}}
.hero-sub{{
  color:var(--cinza2);font-size:15px;font-weight:300;
  max-width:480px;margin:0 auto 28px;
}}
.hero-btns{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
.btn-hero-primary{{
  background:var(--laranja);color:white;
  font-family:'Oswald',sans-serif;font-size:15px;font-weight:600;
  letter-spacing:2px;text-transform:uppercase;
  padding:12px 28px;border-radius:2px;
  text-decoration:none;border:none;cursor:pointer;
  transition:all 0.2s;
}}
.btn-hero-primary:hover{{background:#ea6c0a;transform:translateY(-1px)}}
.btn-hero-wpp{{
  background:transparent;color:var(--verde);
  font-family:'Oswald',sans-serif;font-size:15px;font-weight:600;
  letter-spacing:2px;text-transform:uppercase;
  padding:12px 28px;border-radius:2px;
  text-decoration:none;border:2px solid var(--verde);cursor:pointer;
  transition:all 0.2s;
}}
.btn-hero-wpp:hover{{background:rgba(34,197,94,0.1)}}

/* PROVA SOCIAL */
.social-proof{{
  background:var(--bg2);
  border-top:1px solid var(--borda);
  border-bottom:1px solid var(--borda);
  padding:20px;
  display:grid;grid-template-columns:repeat(2,1fr);gap:1px;
  background:var(--borda);
}}
.proof-item{{
  background:var(--bg2);
  padding:16px 20px;text-align:center;
}}
.proof-num{{
  font-family:'Oswald',sans-serif;font-size:28px;font-weight:700;
  color:var(--laranja);line-height:1;margin-bottom:4px;
}}
.proof-label{{font-size:11px;color:var(--cinza);letter-spacing:1px;text-transform:uppercase}}

/* FILTROS */
.filter-section{{background:var(--bg2);border-bottom:1px solid var(--borda);padding:16px 20px}}
.filter-row{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}}
.filter-row:last-child{{margin-bottom:0}}
.filter-label{{font-size:10px;color:var(--cinza);letter-spacing:1px;text-transform:uppercase;font-weight:600;margin-bottom:6px}}
.filter-btn{{
  flex-shrink:0;background:transparent;
  border:1px solid var(--borda2);color:var(--cinza2);
  font-family:'Barlow',sans-serif;font-size:12px;font-weight:600;
  padding:6px 14px;border-radius:2px;cursor:pointer;
  transition:all 0.2s;white-space:nowrap;
}}
.filter-btn:hover,.filter-btn.active{{
  background:var(--laranja);border-color:var(--laranja);color:white;
}}
.filter-sel{{
  background:var(--bg);border:1px solid var(--borda2);color:var(--branco);
  font-family:'Barlow',sans-serif;font-size:12px;font-weight:600;
  padding:6px 14px;border-radius:2px;cursor:pointer;flex-shrink:0;
}}
.search-wrap{{padding:12px 20px;background:var(--bg2);border-bottom:1px solid var(--borda);position:relative}}
.search-input{{
  width:100%;background:var(--bg);
  border:1px solid var(--borda2);color:var(--branco);
  font-family:'Barlow',sans-serif;font-size:14px;
  padding:10px 16px 10px 44px;border-radius:2px;outline:none;
  transition:border 0.2s;
}}
.search-input:focus{{border-color:var(--laranja)}}
.search-icon{{position:absolute;left:32px;top:50%;transform:translateY(-50%);color:var(--cinza);font-size:16px}}

/* CONTENT */
.content{{padding:20px 16px;max-width:840px;margin:0 auto}}
.update-bar{{
  background:rgba(34,197,94,0.05);
  border:1px solid rgba(34,197,94,0.2);
  border-radius:2px;padding:8px 14px;
  font-size:11px;color:var(--cinza2);
  margin-bottom:20px;display:flex;align-items:center;gap:8px;
  letter-spacing:0.5px;
}}
.dot{{width:7px;height:7px;background:var(--verde);border-radius:50%;animation:pulse 2s infinite;flex-shrink:0}}
@keyframes pulse{{0%,100%{{opacity:1;box-shadow:0 0 0 0 rgba(34,197,94,0.4)}}50%{{opacity:0.8;box-shadow:0 0 0 4px rgba(34,197,94,0)}}}}

/* SECTION TITLE */
.sec-title{{
  font-family:'Oswald',sans-serif;font-size:20px;font-weight:600;
  letter-spacing:2px;text-transform:uppercase;
  color:var(--branco);margin:28px 0 16px;
  display:flex;align-items:center;gap:12px;
}}
.sec-title::after{{content:'';flex:1;height:1px;background:var(--borda)}}

/* CARDS DE VAGA */
.grid{{display:flex;flex-direction:column;gap:12px}}
.card{{
  background:var(--card);
  border:1px solid var(--borda);
  border-left:3px solid var(--laranja);
  border-radius:2px;padding:18px;
  transition:all 0.2s;
}}
.card:hover{{border-color:var(--laranja);background:var(--bg3);transform:translateY(-1px);box-shadow:0 4px 20px rgba(249,115,22,0.1)}}
.card-header{{display:flex;align-items:flex-start;gap:12px;margin-bottom:12px}}
.card-area-icon{{font-size:22px;flex-shrink:0;margin-top:2px}}
.card-info{{flex:1}}
.card-titulo{{font-family:'Oswald',sans-serif;font-size:17px;font-weight:600;color:var(--branco);letter-spacing:0.5px;margin-bottom:3px}}
.card-empresa{{font-size:13px;color:var(--cinza2);font-weight:500}}
.badge{{font-size:10px;font-weight:700;padding:3px 10px;border-radius:2px;white-space:nowrap;flex-shrink:0;letter-spacing:1px;text-transform:uppercase}}
.b-el{{background:rgba(59,130,246,0.15);color:#60a5fa;border:1px solid rgba(59,130,246,0.3)}}
.b-me{{background:rgba(34,197,94,0.15);color:#4ade80;border:1px solid rgba(34,197,94,0.3)}}
.b-au{{background:rgba(249,115,22,0.15);color:#fb923c;border:1px solid rgba(249,115,22,0.3)}}
.b-qu{{background:rgba(168,85,247,0.15);color:#c084fc;border:1px solid rgba(168,85,247,0.3)}}
.b-se{{background:rgba(20,184,166,0.15);color:#2dd4bf;border:1px solid rgba(20,184,166,0.3)}}
.b-rf{{background:rgba(96,165,250,0.15);color:#93c5fd;border:1px solid rgba(96,165,250,0.3)}}
.card-meta{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px}}
.meta-item{{font-size:11px;color:var(--cinza2);background:var(--bg3);padding:3px 8px;border-radius:2px;border:1px solid var(--borda)}}
.beneficios{{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:12px}}
.benef-tag{{background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.2);color:#fbbf24;font-size:10px;padding:2px 8px;border-radius:2px}}
.card-actions{{display:flex;gap:8px;align-items:center}}
.btn-wpp{{background:rgba(34,197,94,0.1);color:var(--verde);border:1px solid rgba(34,197,94,0.3);font-family:'Barlow',sans-serif;font-size:12px;font-weight:600;padding:7px 14px;border-radius:2px;text-decoration:none;transition:all 0.2s}}
.btn-wpp:hover{{background:rgba(34,197,94,0.2)}}
.btn-ver{{background:var(--laranja);color:white;font-family:'Oswald',sans-serif;font-size:13px;font-weight:600;letter-spacing:1px;padding:7px 16px;border-radius:2px;text-decoration:none;transition:all 0.2s;margin-left:auto}}
.btn-ver:hover{{background:#ea6c0a}}

/* NEWSLETTER */
.newsletter{{
  background:linear-gradient(135deg,var(--bg2),var(--bg3));
  border:1px solid var(--borda);
  border-top:2px solid var(--laranja);
  border-radius:2px;padding:24px;margin-bottom:28px;
}}
.nl-titulo{{font-family:'Oswald',sans-serif;font-size:22px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px}}
.nl-titulo span{{color:var(--laranja)}}
.nl-desc{{font-size:13px;color:var(--cinza2);margin-bottom:16px}}
.nl-form{{display:flex;gap:8px;flex-wrap:wrap}}
.nl-input{{flex:1;min-width:200px;background:var(--bg);border:1px solid var(--borda2);color:var(--branco);font-family:'Barlow',sans-serif;font-size:14px;padding:10px 14px;border-radius:2px;outline:none}}
.nl-input:focus{{border-color:var(--laranja)}}
.nl-btn{{background:var(--laranja);color:white;border:none;font-family:'Oswald',sans-serif;font-size:14px;font-weight:600;letter-spacing:2px;text-transform:uppercase;padding:10px 20px;border-radius:2px;cursor:pointer;white-space:nowrap}}
.nl-ok{{display:none;color:var(--verde);font-size:13px;margin-top:10px;font-weight:600}}

/* CALC GRID */
.calc-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:28px}}
.calc-btn{{
  background:var(--card);border:1px solid var(--borda);
  border-radius:2px;padding:16px;cursor:pointer;
  transition:all 0.2s;text-align:left;color:var(--branco);
  display:flex;align-items:center;gap:12px;
}}
.calc-btn:hover{{border-color:var(--laranja);background:var(--bg3)}}
.calc-icon{{font-size:22px;flex-shrink:0}}
.calc-nome{{font-family:'Oswald',sans-serif;font-size:14px;font-weight:600;letter-spacing:0.5px;margin-bottom:2px}}
.calc-desc{{font-size:11px;color:var(--cinza)}}

/* BLOG */
.blog-grid{{display:flex;flex-direction:column;gap:10px;margin-bottom:28px}}
.blog-card{{background:var(--card);border:1px solid var(--borda);border-radius:2px;padding:16px;display:flex;gap:14px;transition:all 0.2s;cursor:default}}
.blog-card:hover{{border-color:var(--borda2);background:var(--bg3)}}
.blog-left{{flex-shrink:0}}
.blog-icon{{font-size:28px}}
.blog-right{{flex:1}}
.blog-tag{{font-size:10px;font-weight:700;color:var(--laranja);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px}}
.blog-titulo{{font-family:'Oswald',sans-serif;font-size:15px;font-weight:600;color:var(--branco);margin-bottom:4px;letter-spacing:0.3px}}
.blog-resumo{{font-size:12px;color:var(--cinza);line-height:1.5;margin-bottom:8px}}
.blog-link{{font-size:12px;color:var(--laranja);font-weight:600}}

/* MODAIS */
.modal{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:1000;align-items:center;justify-content:center;padding:16px;overflow-y:auto}}
.modal.open{{display:flex}}
.modal-box{{background:var(--bg2);border:1px solid var(--borda);border-top:2px solid var(--laranja);border-radius:2px;padding:24px;width:100%;max-width:400px;margin:auto}}
.modal-title{{font-family:'Oswald',sans-serif;font-size:22px;letter-spacing:2px;text-transform:uppercase;color:var(--laranja);margin-bottom:16px}}
.input-group{{margin-bottom:14px}}
.input-group label{{font-size:11px;color:var(--cinza);display:block;margin-bottom:6px;font-weight:600;letter-spacing:1px;text-transform:uppercase}}
.input-group input,.input-group select{{width:100%;background:var(--bg);border:1px solid var(--borda2);color:var(--branco);font-family:'Barlow',sans-serif;font-size:14px;padding:10px 14px;border-radius:2px;outline:none}}
.input-group input:focus,.input-group select:focus{{border-color:var(--laranja)}}
.calc-result{{background:var(--bg);border:1px solid var(--borda);border-radius:2px;padding:14px;margin-top:16px}}
.calc-line{{display:flex;justify-content:space-between;font-size:13px;margin-bottom:8px;color:var(--cinza)}}
.calc-line.destaque{{color:#4ade80;font-weight:700;font-size:15px;border-top:1px solid var(--borda);padding-top:10px;margin-top:4px}}
.btn-fechar{{background:transparent;color:var(--cinza);border:1px solid var(--borda);font-family:'Barlow',sans-serif;font-size:13px;padding:8px;border-radius:2px;cursor:pointer;width:100%;margin-top:8px;transition:all 0.2s}}
.btn-fechar:hover{{border-color:var(--borda2);color:var(--branco)}}

.sem-vagas{{text-align:center;padding:48px 24px;color:var(--cinza)}}
.sem-vagas-icon{{font-size:48px;margin-bottom:16px}}
.sem-vagas-titulo{{font-family:'Oswald',sans-serif;font-size:24px;color:var(--branco);margin-bottom:8px;letter-spacing:1px;text-transform:uppercase}}
.sem-vagas-texto{{font-size:14px;line-height:1.6}}

footer{{text-align:center;padding:32px;color:var(--cinza);font-size:12px;border-top:1px solid var(--borda);margin-top:28px}}
footer strong{{color:var(--laranja)}}
footer .footer-logo{{font-family:'Oswald',sans-serif;font-size:18px;letter-spacing:3px;margin-bottom:8px}}
</style>
</head>
<body>

<header>
  <div>
    <div class="logo">Tec<span>System</span> Brasil</div>
    <div class="logo-sub">VAGAS TÉCNICAS INDUSTRIAIS</div>
  </div>
  <span id="horario" style="font-size:11px;color:var(--cinza)"></span>
</header>

<!-- HERO -->
<div class="hero">
  <div class="hero-tag">⚙️ Atualizado diariamente · 2026</div>
  <h1>As melhores vagas<br>para <em>técnicos industriais</em><br>do Brasil, em um só lugar.</h1>
  <p class="hero-sub">Elétrica · Mecânica · Automação · Refrigeração · Manutenção Industrial</p>
  <div class="hero-btns">
    <a class="btn-hero-primary" href="#vagas" onclick="document.getElementById('vagas').scrollIntoView({{behavior:'smooth'}})">🔧 BUSCAR VAGAS</a>
    <a class="btn-hero-wpp" href="https://wa.me/?text=🔧 Encontrei vagas para técnicos industriais no TecSystem Brasil! Acesse: https://tecsystembrasil.netlify.app" target="_blank">📲 COMPARTILHAR</a>
  </div>
</div>

<!-- PROVA SOCIAL -->
<div class="social-proof">
  <div class="proof-item"><div class="proof-num" id="proof-vagas">{total}</div><div class="proof-label">Vagas publicadas</div></div>
  <div class="proof-item"><div class="proof-num">60+</div><div class="proof-label">Especialidades</div></div>
  <div class="proof-item"><div class="proof-num">5x</div><div class="proof-label">Atualizado por dia</div></div>
  <div class="proof-item"><div class="proof-num">27</div><div class="proof-label">Estados do Brasil</div></div>
</div>

<!-- FILTROS -->
<div class="filter-section">
  <div class="filter-label">Área técnica</div>
  <div class="filter-row">
    <button class="filter-btn active" onclick="filtrarArea('todas',this)">Todas</button>
    <button class="filter-btn" onclick="filtrarArea('eletrica',this)">⚡ Elétrica</button>
    <button class="filter-btn" onclick="filtrarArea('mecanica',this)">🔩 Mecânica</button>
    <button class="filter-btn" onclick="filtrarArea('automacao',this)">🤖 Automação</button>
    <button class="filter-btn" onclick="filtrarArea('refrigeracao',this)">❄️ Refrigeração</button>
    <button class="filter-btn" onclick="filtrarArea('qualidade',this)">📊 Qualidade</button>
    <button class="filter-btn" onclick="filtrarArea('seguranca',this)">🦺 Segurança</button>
  </div>
  <div class="filter-label" style="margin-top:10px">Estado e especialidade</div>
  <div class="filter-row">
    <select class="filter-sel" onchange="filtrarEstado(this.value)">{opts_estados}</select>
    <select class="filter-sel" onchange="filtrarEsp(this.value)">
      <option value="todas">🔧 Todas as especialidades</option>
      {tec_opts}
    </select>
  </div>
</div>

<!-- BUSCA -->
<div class="search-wrap">
  <span class="search-icon">🔍</span>
  <input class="search-input" type="text" placeholder="Buscar por cargo, empresa ou cidade..." oninput="buscar(this.value)">
</div>

<!-- CONTEÚDO -->
<div class="content">
  <div class="update-bar"><div class="dot"></div>Apenas vagas de 2026 · Vagas encerradas removidas automaticamente · Atualizado em {agora}</div>

  <div class="sec-title" id="vagas">🔧 Vagas Disponíveis</div>
  <div class="grid" id="grid">{cards}</div>
  <div id="sem-vagas" style="display:none" class="sem-vagas">
    <div class="sem-vagas-icon">🔍</div>
    <div class="sem-vagas-titulo">Nenhuma vaga encontrada</div>
    <div class="sem-vagas-texto">Não encontramos vagas para esse filtro no momento.<br><br>• Tente outra especialidade ou estado<br>• Volte mais tarde — atualizamos 5x por dia<br>• Clique em <strong>"Todas"</strong> para ver todas as vagas</div>
  </div>

  <!-- NEWSLETTER -->
  <div class="newsletter">
    <div class="nl-titulo">📧 Receba <span>Vagas</span> por Email</div>
    <div class="nl-desc">Toda semana as melhores vagas técnicas direto na sua caixa. Grátis, sem spam.</div>
    <div class="nl-form">
      <input class="nl-input" type="email" id="nl-email" placeholder="seu@email.com">
      <button class="nl-btn" onclick="assinarNewsletter()">QUERO RECEBER</button>
    </div>
    <div class="nl-ok" id="nl-ok">✅ Cadastro realizado! Você receberá as vagas em breve.</div>
  </div>

  <!-- CALCULADORAS -->
  <div class="sec-title">🧮 Calculadoras Trabalhistas</div>
  <div class="calc-grid">
    <button class="calc-btn" onclick="abrirModal('m-salario')"><div class="calc-icon">💰</div><div><div class="calc-nome">Salário Líquido</div><div class="calc-desc">INSS + IRRF 2026</div></div></button>
    <button class="calc-btn" onclick="abrirModal('m-ferias')"><div class="calc-icon">🏖️</div><div><div class="calc-nome">Férias</div><div class="calc-desc">+ 1/3 constitucional</div></div></button>
    <button class="calc-btn" onclick="abrirModal('m-rescisao')"><div class="calc-icon">📦</div><div><div class="calc-nome">Rescisão</div><div class="calc-desc">Demissão ou pedido</div></div></button>
    <button class="calc-btn" onclick="abrirModal('m-horaextra')"><div class="calc-icon">⏰</div><div><div class="calc-nome">Hora Extra</div><div class="calc-desc">50%, 100% e noturna</div></div></button>
    <button class="calc-btn" onclick="abrirModal('m-noturno')"><div class="calc-icon">🌙</div><div><div class="calc-nome">Adicional Noturno</div><div class="calc-desc">20% sobre salário</div></div></button>
    <button class="calc-btn" onclick="abrirModal('m-insalub')"><div class="calc-icon">⚠️</div><div><div class="calc-nome">Insalubridade</div><div class="calc-desc">e Periculosidade</div></div></button>
    <button class="calc-btn" onclick="abrirModal('m-decimo')"><div class="calc-icon">🎄</div><div><div class="calc-nome">13º Salário</div><div class="calc-desc">Proporcional ou cheio</div></div></button>
  </div>

  <!-- BLOG -->
  <div class="sec-title">📰 Para Técnicos</div>
  <div class="blog-grid">{blog_cards}</div>

</div>

<!-- MODAIS -->
<div class="modal" id="m-salario"><div class="modal-box">
  <div class="modal-title">💰 Salário Líquido</div>
  <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="sl-b" placeholder="Ex: 3500" oninput="calcSalario()"></div>
  <div class="input-group"><label>Dependentes para IR</label><input type="number" id="sl-d" placeholder="0" value="0" oninput="calcSalario()"></div>
  <div class="calc-result" id="sl-res" style="display:none">
    <div class="calc-line"><span>Salário Bruto</span><span id="sl-1"></span></div>
    <div class="calc-line"><span>(-) INSS</span><span id="sl-2" style="color:#f87171"></span></div>
    <div class="calc-line"><span>(-) IRRF</span><span id="sl-3" style="color:#f87171"></span></div>
    <div class="calc-line destaque"><span>💵 Líquido</span><span id="sl-4"></span></div>
    <div class="calc-line" style="font-size:11px;margin-top:6px"><span>FGTS (empregador deposita)</span><span id="sl-5" style="color:#4ade80"></span></div>
  </div>
  <button class="btn-fechar" onclick="fecharModal('m-salario')">✕ Fechar</button>
</div></div>

<div class="modal" id="m-ferias"><div class="modal-box">
  <div class="modal-title">🏖️ Férias</div>
  <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="fe-b" placeholder="Ex: 3500" oninput="calcFerias()"></div>
  <div class="input-group"><label>Meses trabalhados</label><input type="number" id="fe-m" placeholder="12" value="12" min="1" max="12" oninput="calcFerias()"></div>
  <div class="calc-result" id="fe-res" style="display:none">
    <div class="calc-line"><span>Férias proporcional</span><span id="fe-1"></span></div>
    <div class="calc-line"><span>(+) 1/3 constitucional</span><span id="fe-2" style="color:#4ade80"></span></div>
    <div class="calc-line"><span>Total bruto</span><span id="fe-3"></span></div>
    <div class="calc-line"><span>(-) INSS + IR</span><span id="fe-4" style="color:#f87171"></span></div>
    <div class="calc-line destaque"><span>🏖️ Férias Líquidas</span><span id="fe-5"></span></div>
  </div>
  <button class="btn-fechar" onclick="fecharModal('m-ferias')">✕ Fechar</button>
</div></div>

<div class="modal" id="m-rescisao"><div class="modal-box">
  <div class="modal-title">📦 Rescisão</div>
  <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="re-b" placeholder="Ex: 3500" oninput="calcRescisao()"></div>
  <div class="input-group"><label>Meses trabalhados no ano</label><input type="number" id="re-m" placeholder="Ex: 6" min="1" max="12" oninput="calcRescisao()"></div>
  <div class="input-group"><label>Tipo de rescisão</label>
    <select id="re-t" onchange="calcRescisao()"><option value="sem_justa">Demissão sem justa causa</option><option value="pedido">Pedido de demissão</option><option value="acordo">Acordo (distrato)</option></select>
  </div>
  <div class="calc-result" id="re-res" style="display:none">
    <div class="calc-line"><span>Saldo de salário</span><span id="re-1"></span></div>
    <div class="calc-line"><span>13º proporcional</span><span id="re-2"></span></div>
    <div class="calc-line"><span>Férias + 1/3</span><span id="re-3"></span></div>
    <div class="calc-line" id="re-multa-linha"><span>Multa FGTS</span><span id="re-4" style="color:#4ade80"></span></div>
    <div class="calc-line destaque"><span>📦 Total Rescisão</span><span id="re-5"></span></div>
  </div>
  <button class="btn-fechar" onclick="fecharModal('m-rescisao')">✕ Fechar</button>
</div></div>

<div class="modal" id="m-horaextra"><div class="modal-box">
  <div class="modal-title">⏰ Hora Extra</div>
  <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="he-b" placeholder="Ex: 3500" oninput="calcHoraExtra()"></div>
  <div class="input-group"><label>Quantidade de horas extras</label><input type="number" id="he-h" placeholder="Ex: 10" oninput="calcHoraExtra()"></div>
  <div class="input-group"><label>Tipo</label>
    <select id="he-t" onchange="calcHoraExtra()"><option value="50">50% — Dias úteis</option><option value="100">100% — Domingos/Feriados</option><option value="70">70% — Noturna</option></select>
  </div>
  <div class="calc-result" id="he-res" style="display:none">
    <div class="calc-line"><span>Valor hora normal</span><span id="he-1"></span></div>
    <div class="calc-line"><span>Valor hora extra</span><span id="he-2"></span></div>
    <div class="calc-line destaque"><span>⏰ Total a receber</span><span id="he-3"></span></div>
  </div>
  <button class="btn-fechar" onclick="fecharModal('m-horaextra')">✕ Fechar</button>
</div></div>

<div class="modal" id="m-noturno"><div class="modal-box">
  <div class="modal-title">🌙 Adicional Noturno</div>
  <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="no-b" placeholder="Ex: 3500" oninput="calcNoturno()"></div>
  <div class="input-group"><label>Horas noturnas por mês</label><input type="number" id="no-h" placeholder="Ex: 44" oninput="calcNoturno()"></div>
  <div class="calc-result" id="no-res" style="display:none">
    <div class="calc-line"><span>Salário base</span><span id="no-1"></span></div>
    <div class="calc-line"><span>(+) Adicional 20%</span><span id="no-2" style="color:#4ade80"></span></div>
    <div class="calc-line destaque"><span>🌙 Total com adicional</span><span id="no-3"></span></div>
    <div class="calc-line" style="font-size:11px;margin-top:6px;color:var(--cinza)"><span>Horário noturno: 22h às 5h</span><span></span></div>
  </div>
  <button class="btn-fechar" onclick="fecharModal('m-noturno')">✕ Fechar</button>
</div></div>

<div class="modal" id="m-insalub"><div class="modal-box">
  <div class="modal-title">⚠️ Insalubridade</div>
  <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="in-b" placeholder="Ex: 3500" oninput="calcInsalub()"></div>
  <div class="input-group"><label>Tipo de adicional</label>
    <select id="in-t" onchange="calcInsalub()">
      <option value="10">Insalubridade Mínima — 10% SM</option>
      <option value="20">Insalubridade Média — 20% SM</option>
      <option value="40">Insalubridade Máxima — 40% SM</option>
      <option value="30p">Periculosidade — 30% salário</option>
    </select>
  </div>
  <div class="calc-result" id="in-res" style="display:none">
    <div class="calc-line"><span>Salário base</span><span id="in-1"></span></div>
    <div class="calc-line"><span>(+) Adicional</span><span id="in-2" style="color:#4ade80"></span></div>
    <div class="calc-line destaque"><span>⚠️ Total com adicional</span><span id="in-3"></span></div>
    <div class="calc-line" style="font-size:11px;margin-top:6px;color:var(--cinza)"><span>Salário mínimo 2026: R$ 1.518,00</span><span></span></div>
  </div>
  <button class="btn-fechar" onclick="fecharModal('m-insalub')">✕ Fechar</button>
</div></div>

<div class="modal" id="m-decimo"><div class="modal-box">
  <div class="modal-title">🎄 13º Salário</div>
  <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="de-b" placeholder="Ex: 3500" oninput="calcDecimo()"></div>
  <div class="input-group"><label>Meses trabalhados no ano</label><input type="number" id="de-m" placeholder="12" value="12" min="1" max="12" oninput="calcDecimo()"></div>
  <div class="calc-result" id="de-res" style="display:none">
    <div class="calc-line"><span>13º bruto proporcional</span><span id="de-1"></span></div>
    <div class="calc-line"><span>(-) INSS + IR</span><span id="de-2" style="color:#f87171"></span></div>
    <div class="calc-line destaque"><span>🎄 13º Líquido</span><span id="de-3"></span></div>
    <div class="calc-line" style="font-size:11px;margin-top:6px;color:var(--cinza)"><span>1ª parcela: nov · 2ª parcela: dez</span><span></span></div>
  </div>
  <button class="btn-fechar" onclick="fecharModal('m-decimo')">✕ Fechar</button>
</div></div>

<footer>
  <div class="footer-logo">Tec<span style="color:var(--laranja)">System</span> Brasil</div>
  <strong>Vagas técnicas industriais · Apenas 2026 · Todo o Brasil</strong><br>
  <span style="font-size:11px;color:var(--cinza)">Links redirecionam para os sites originais · Atualizado automaticamente 5x por dia</span>
</footer>

<script data-goatcounter="https://tecsystembrasil.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<script>
// HORÁRIO
function atualizarHorario(){{const a=new Date();document.getElementById('horario').textContent=new Intl.DateTimeFormat('pt-BR',{{timeZone:'America/Sao_Paulo',day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'}}).format(a);}}
atualizarHorario();setInterval(atualizarHorario,60000);

// MODAIS
function abrirModal(id){{document.getElementById(id).classList.add('open');}}
function fecharModal(id){{document.getElementById(id).classList.remove('open');}}
document.querySelectorAll('.modal').forEach(m=>m.addEventListener('click',function(e){{if(e.target===this)fecharModal(this.id);}}));

// FILTROS
let aA='todas',eA='todos',xA='todas',bA='';
function filtrarArea(a,b){{aA=a;document.querySelectorAll('.filter-btn').forEach(x=>x.classList.remove('active'));b.classList.add('active');aplicar();}}
function filtrarEstado(v){{eA=v;aplicar();}}
function filtrarEsp(v){{xA=v;aplicar();}}
function buscar(v){{bA=v.toLowerCase().trim();aplicar();}}
function aplicar(){{
  let n=0;
  document.querySelectorAll('#grid .card').forEach(c=>{{
    const ok=(aA==='todas'||c.dataset.area===aA)&&
             (eA==='todos'||c.dataset.estado===eA)&&
             (xA==='todas'||c.dataset.esp.includes(xA))&&
             (bA===''||c.dataset.busca.includes(bA));
    c.style.display=ok?'block':'none';
    if(ok)n++;
  }});
  document.getElementById('contador')&&(document.getElementById('contador').textContent=n);
  document.getElementById('proof-vagas').textContent=n;
  document.getElementById('sem-vagas').style.display=n===0?'block':'none';
  document.getElementById('grid').style.display=n===0?'none':'flex';
}}

// NEWSLETTER
function assinarNewsletter(){{
  const email=document.getElementById('nl-email').value;
  if(!email||!email.includes('@')){{alert('Digite um email válido!');return;}}
  fetch('https://formsubmit.co/ajax/tecsystembrasil@gmail.com',{{method:'POST',
    headers:{{'Content-Type':'application/json','Accept':'application/json'}},
    body:JSON.stringify({{email:email,_subject:'Novo cadastro newsletter TecSystem Brasil'}})
  }}).catch(()=>{{}});
  document.getElementById('nl-ok').style.display='block';
  document.getElementById('nl-email').value='';
}}

// MATEMÁTICA
function iNSS(b){{const f=[[1518,0.075],[2793.88,0.09],[4190.83,0.12],[8157.41,0.14]];let i=0,a=0;for(const[t,q]of f){{if(b<=t){{i+=(b-a)*q;break;}}i+=(t-a)*q;a=t;}}return Math.min(i,908.86);}}
function iR(b,d){{const x=b-d*189.59;const f=[[2259.2,0,0],[2826.65,0.075,169.44],[3751.05,0.15,381.44],[4664.68,0.225,662.77],[Infinity,0.275,896]];for(const[t,a,e]of f){{if(x<=t)return Math.max(0,x*a-e);}}return 0;}}
function R(v){{return'R$ '+v.toFixed(2).replace('.',',').replace(/\B(?=(\d{{3}})+(?!\d))/g,'.');}}

// CALCULADORAS
function calcSalario(){{const b=parseFloat(document.getElementById('sl-b').value)||0,d=parseInt(document.getElementById('sl-d').value)||0;if(!b){{document.getElementById('sl-res').style.display='none';return;}}const i=iNSS(b),r=iR(b-i,d),l=b-i-r;document.getElementById('sl-1').textContent=R(b);document.getElementById('sl-2').textContent='- '+R(i);document.getElementById('sl-3').textContent='- '+R(r);document.getElementById('sl-4').textContent=R(l);document.getElementById('sl-5').textContent='+ '+R(b*0.08);document.getElementById('sl-res').style.display='block';}}
function calcFerias(){{const s=parseFloat(document.getElementById('fe-b').value)||0,m=parseInt(document.getElementById('fe-m').value)||12;if(!s){{document.getElementById('fe-res').style.display='none';return;}}const p=s*(m/12),t=p/3,tot=p+t,i=iNSS(tot),r=iR(tot-i,0);document.getElementById('fe-1').textContent=R(p);document.getElementById('fe-2').textContent='+ '+R(t);document.getElementById('fe-3').textContent=R(tot);document.getElementById('fe-4').textContent='- '+R(i+r);document.getElementById('fe-5').textContent=R(tot-i-r);document.getElementById('fe-res').style.display='block';}}
function calcRescisao(){{const s=parseFloat(document.getElementById('re-b').value)||0,m=parseInt(document.getElementById('re-m').value)||1,tp=document.getElementById('re-t').value;if(!s){{document.getElementById('re-res').style.display='none';return;}}const dec=s*(m/12),fp=(s*(m/12))*(4/3),fg=s*0.08*m;let mu=tp==='sem_justa'?fg*0.4:tp==='acordo'?fg*0.2:0;document.getElementById('re-1').textContent=R(s);document.getElementById('re-2').textContent=R(dec);document.getElementById('re-3').textContent=R(fp);document.getElementById('re-4').textContent='+ '+R(mu);document.getElementById('re-multa-linha').style.display=mu>0?'flex':'none';document.getElementById('re-5').textContent=R(s+dec+fp+mu);document.getElementById('re-res').style.display='block';}}
function calcHoraExtra(){{const s=parseFloat(document.getElementById('he-b').value)||0,h=parseFloat(document.getElementById('he-h').value)||0,tp=parseFloat(document.getElementById('he-t').value);if(!s||!h){{document.getElementById('he-res').style.display='none';return;}}const hb=s/220,he=hb*(1+tp/100);document.getElementById('he-1').textContent=R(hb);document.getElementById('he-2').textContent=R(he);document.getElementById('he-3').textContent=R(he*h);document.getElementById('he-res').style.display='block';}}
function calcNoturno(){{const s=parseFloat(document.getElementById('no-b').value)||0,h=parseFloat(document.getElementById('no-h').value)||0;if(!s){{document.getElementById('no-res').style.display='none';return;}}const ad=(s/220)*0.2*h;document.getElementById('no-1').textContent=R(s);document.getElementById('no-2').textContent='+ '+R(ad);document.getElementById('no-3').textContent=R(s+ad);document.getElementById('no-res').style.display='block';}}
function calcInsalub(){{const s=parseFloat(document.getElementById('in-b').value)||0,tp=document.getElementById('in-t').value;if(!s){{document.getElementById('in-res').style.display='none';return;}}const ad=tp==='30p'?s*0.3:1518*(parseFloat(tp)/100);document.getElementById('in-1').textContent=R(s);document.getElementById('in-2').textContent='+ '+R(ad);document.getElementById('in-3').textContent=R(s+ad);document.getElementById('in-res').style.display='block';}}
function calcDecimo(){{const s=parseFloat(document.getElementById('de-b').value)||0,m=parseInt(document.getElementById('de-m').value)||12;if(!s){{document.getElementById('de-res').style.display='none';return;}}const b=s*(m/12),i=iNSS(b),r=iR(b-i,0);document.getElementById('de-1').textContent=R(b);document.getElementById('de-2').textContent='- '+R(i+r);document.getElementById('de-3').textContent=R(b-i-r);document.getElementById('de-res').style.display='block';}}
</script>
</body>
</html>"""


def main():
    print(f"\n🤖 TecSystem Brasil v8 — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("="*50)
    cache=carregar_cache()
    vagas_ativas=verificar_cache(cache)
    vagas_novas=buscar_gupy()+buscar_vagas_com_br()+buscar_infojobs()
    todas=remover_duplicatas(vagas_ativas+vagas_novas)
    print(f"\n📊 Total: {len(todas)} vagas")
    with open(CACHE_FILE,"w",encoding="utf-8") as f:json.dump(todas,f,ensure_ascii=False,indent=2)
    with open("index.html","w",encoding="utf-8") as f:f.write(gerar_html(todas))
    print(f"✅ Site atualizado com {len(todas)} vagas!")

if __name__=="__main__":main()
