"""
TecSystem Brasil - Robô de Vagas v6
=====================================
- 90+ tipos de técnicos industriais
- 7 calculadoras trabalhistas
- Filtro por especialidade, estado e área
- Filtra só vagas de 2026
- Remove vagas encerradas automaticamente
- Mensagem amigável quando não há vagas
- Contador GoatCounter
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
    "técnico em refrigeração industrial","técnico em elétrica industrial",
    "técnico em eletrotécnica","técnico em eletrônica industrial",
    "técnico em automação industrial","técnico em mecatrônica",
    "técnico em mecânica industrial","técnico em manutenção industrial",
    "técnico em manutenção mecânica","técnico em manutenção elétrica",
    "técnico em manutenção eletromecânica","técnico em instrumentação industrial",
    "técnico em processos industriais","técnico em química industrial",
    "técnico em petroquímica","técnico em metalurgia","técnico em soldagem",
    "técnico em caldeiraria","técnico em tubulação industrial",
    "técnico em hidráulica industrial","técnico em pneumática",
    "técnico em utilidades industriais","técnico em caldeiras",
    "técnico em vapor e utilidades","técnico em ar comprimido",
    "técnico em HVAC","técnico em climatização","técnico em comando elétrico",
    "técnico em painéis elétricos","técnico em PLC","técnico em SCADA",
    "técnico em robótica industrial","técnico em CNC","técnico em usinagem",
    "técnico em ferramentaria","técnico em produção industrial",
    "técnico em controle de qualidade","técnico em inspeção de qualidade",
    "técnico em ensaios não destrutivos","técnico em metrologia",
    "técnico em segurança do trabalho","técnico em meio ambiente",
    "técnico em saneamento industrial","técnico em logística industrial",
    "técnico em manutenção preditiva","técnico em manutenção preventiva",
    "técnico em manutenção corretiva","técnico em vibração",
    "técnico em análise de óleo","técnico em lubrificação industrial",
    "técnico em motores elétricos","técnico em geradores",
    "técnico em subestações","técnico em energia",
    "técnico em telecomunicações industriais","técnico em redes industriais",
    "técnico em automação predial","técnico em alimentos","técnico em laticínios",
    "técnico em biotecnologia industrial","técnico em papel e celulose",
    "técnico em mineração","técnico em siderurgia","técnico em plástico",
    "técnico em borracha","técnico em cerâmica","técnico em têxtil",
    "técnico em embalagens","técnico em farmacêutica","técnico em cosméticos",
    "técnico em laboratório industrial","técnico em operação de máquinas",
    "técnico em comissionamento","técnico em assistência técnica industrial",
    "técnico em manutenção de compressores","técnico em bombas industriais",
    "técnico em válvulas industriais","técnico em torres de resfriamento",
    "técnico em tratamento de água","técnico em efluentes industriais",
    "técnico em gás industrial","técnico em combustão industrial",
    "técnico em fornos industriais","técnico em instalações industriais",
    "técnico em montagem industrial","técnico em planejamento de manutenção",
    "técnico em PCM","técnico em confiabilidade industrial",
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
    "home office":"🏠","trabalho remoto":"🏠","híbrido":"🔄","cesta básica":"🧺",
    "auxílio educação":"📚","bolsa estudo":"📚",
}


def detectar_area(texto):
    t=texto.lower()
    if any(p in t for p in ["elétric","eletric","eletrom","painel","subestac","motor","gerador"]):return "eletrica"
    if any(p in t for p in ["mecatrôn","mecatron","plc","scada","robotic","automac","automaç","cnc"]):return "automacao"
    if any(p in t for p in ["qualidad","inspeç","metrolog","ensaio","end","calibr"]):return "qualidade"
    if any(p in t for p in ["seguranç","meio ambient","saneam"]):return "seguranca"
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
            data=resp.json()
            for job in data.get("data",[]):
                pub=str(job.get("publishedDate",""or job.get("createdAt","")))
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
                    "area":detectar_area(titulo),"beneficios":benef})
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
                    "area":detectar_area(titulo),"beneficios":[]})
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
                    "area":detectar_area(titulo),"beneficios":[]})
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


CORES={"eletrica":("b-el","ELÉTRICA"),"mecanica":("b-me","MECÂNICA"),
       "automacao":("b-au","AUTOMAÇÃO"),"qualidade":("b-qu","QUALIDADE"),"seguranca":("b-se","SEGURANÇA")}


def gerar_benef_html(benefs):
    if not benefs:return ""
    tags="".join(f'<span class="benef-tag">{icone_benef(b)} {b}</span>' for b in benefs[:5])
    return f'<div class="beneficios">{tags}</div>'


def gerar_card(v):
    area=v.get("area","mecanica");cls,label=CORES.get(area,CORES["mecanica"])
    return f"""<a class="card" href="{v['url']}" target="_blank" data-area="{area}" data-estado="{v.get('estado','BR')}" data-esp="{v.get('titulo','').lower()}">
<div class="card-top"><div class="card-info"><div class="titulo">{v['titulo']}</div><div class="empresa">{v['empresa']} · {v['local']}</div></div><div class="badge {cls}">{label}</div></div>
{gerar_benef_html(v.get('beneficios',[]))}
<div class="card-footer"><div class="fonte">🔗 {v['fonte']} · {v['data']}</div><div class="btn">VER VAGA →</div></div>
</a>"""


def gerar_opts_estados(vagas):
    usados=sorted(set(v.get("estado","BR") for v in vagas if v.get("estado")!="BR"))
    opts='<option value="todos">🌎 Todos os estados</option>'
    for s in usados:opts+=f'<option value="{s}">{s} — {ESTADOS.get(s,s)}</option>'
    return opts


def gerar_html(vagas):
    agora=datetime.now().strftime("%d/%m/%Y às %H:%M")
    cards="\n".join(gerar_card(v) for v in vagas)
    total=len(vagas)
    opts_estados=gerar_opts_estados(vagas)
    tec_opts="".join(f'<option value="{t.replace("técnico em","").strip().lower()}">{t.replace("técnico em","").strip().title()}</option>' for t in sorted(TECNICOS))

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TecSystem Brasil – Vagas Técnicas 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{{--azul:#0a1628;--azul2:#0d2144;--laranja:#f97316;--cinza:#94a3b8;--branco:#f1f5f9;--card:#0f1e35;--borda:#1e3a5f}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--azul);color:var(--branco);font-family:'Barlow',sans-serif}}
header{{background:var(--azul2);border-bottom:2px solid var(--laranja);padding:0 20px;height:64px;display:flex;align-items:center;justify-content:space-between}}
.logo{{font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:2px}}
.logo span{{color:var(--laranja)}}
.hero{{background:linear-gradient(135deg,var(--azul2),#061020);padding:36px 20px;text-align:center}}
.hero h1{{font-family:'Bebas Neue',sans-serif;font-size:44px;letter-spacing:3px;margin-bottom:8px}}
.hero h1 span{{color:var(--laranja)}}
.hero p{{color:var(--cinza);font-size:13px;margin-bottom:20px}}
.stats{{display:flex;justify-content:center;gap:28px}}
.stat-num{{font-family:'Bebas Neue',sans-serif;font-size:30px;color:var(--laranja)}}
.stat-label{{font-size:10px;color:var(--cinza);text-transform:uppercase;letter-spacing:1px}}
.filters{{padding:14px 20px;background:var(--azul2);border-bottom:1px solid var(--borda);display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;flex-wrap:wrap}}
.filter-btn{{flex-shrink:0;background:transparent;border:1px solid var(--borda);color:var(--cinza);font-family:'Barlow',sans-serif;font-size:12px;font-weight:600;padding:7px 14px;border-radius:6px;cursor:pointer;transition:all 0.2s;white-space:nowrap}}
.filter-btn:hover,.filter-btn.active{{background:var(--laranja);border-color:var(--laranja);color:white}}
.sel{{background:var(--azul);border:1px solid var(--borda);color:var(--branco);font-family:'Barlow',sans-serif;font-size:12px;font-weight:600;padding:7px 14px;border-radius:6px;cursor:pointer;flex-shrink:0;max-width:220px}}
.content{{padding:20px 16px;max-width:800px;margin:0 auto}}
.update-bar{{background:rgba(249,115,22,0.1);border:1px solid rgba(249,115,22,0.2);border-radius:8px;padding:10px 14px;font-size:12px;color:var(--cinza);margin-bottom:16px;display:flex;align-items:center;gap:8px}}
.dot{{width:8px;height:8px;background:#22c55e;border-radius:50%;animation:pulse 2s infinite;flex-shrink:0}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:0.4}}}}
.grid{{display:flex;flex-direction:column;gap:10px}}
.card{{background:var(--card);border:1px solid var(--borda);border-radius:10px;padding:16px;text-decoration:none;display:block;transition:all 0.2s}}
.card:hover{{border-color:var(--laranja);background:#122040}}
.card-top{{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;margin-bottom:10px}}
.card-info{{flex:1}}
.titulo{{font-size:15px;font-weight:700;color:var(--branco);margin-bottom:3px}}
.empresa{{font-size:12px;color:var(--cinza)}}
.badge{{font-size:10px;font-weight:700;padding:3px 9px;border-radius:20px;white-space:nowrap;flex-shrink:0}}
.b-el{{background:rgba(59,130,246,0.2);color:#60a5fa;border:1px solid rgba(59,130,246,0.3)}}
.b-me{{background:rgba(34,197,94,0.2);color:#4ade80;border:1px solid rgba(34,197,94,0.3)}}
.b-au{{background:rgba(249,115,22,0.2);color:#fb923c;border:1px solid rgba(249,115,22,0.3)}}
.b-qu{{background:rgba(168,85,247,0.2);color:#c084fc;border:1px solid rgba(168,85,247,0.3)}}
.b-se{{background:rgba(20,184,166,0.2);color:#2dd4bf;border:1px solid rgba(20,184,166,0.3)}}
.beneficios{{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px}}
.benef-tag{{background:rgba(249,115,22,0.1);border:1px solid rgba(249,115,22,0.2);color:var(--cinza);font-size:10px;padding:2px 8px;border-radius:4px}}
.card-footer{{display:flex;align-items:center;justify-content:space-between;margin-top:10px;padding-top:10px;border-top:1px solid var(--borda)}}
.fonte{{font-size:11px;color:var(--cinza)}}
.btn{{background:var(--laranja);color:white;font-size:11px;font-weight:700;padding:5px 12px;border-radius:6px;text-decoration:none}}
.calc-section{{margin-bottom:20px}}
.calc-section-titulo{{font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:1px;color:var(--branco);margin-bottom:12px}}
.calc-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}}
.calc-card-btn{{background:var(--card);border:1px solid var(--borda);border-radius:10px;padding:14px;cursor:pointer;transition:all 0.2s;text-align:center;color:var(--branco)}}
.calc-card-btn:hover{{border-color:var(--laranja);background:#122040}}
.calc-card-icon{{font-size:24px;margin-bottom:6px}}
.calc-card-nome{{font-family:'Barlow',sans-serif;font-size:13px;font-weight:700;color:var(--branco);margin-bottom:2px}}
.calc-card-desc{{font-size:11px;color:var(--cinza)}}
.modal{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);z-index:1000;align-items:center;justify-content:center;padding:16px;overflow-y:auto}}
.modal.open{{display:flex}}
.modal-box{{background:var(--azul2);border:1px solid var(--borda);border-radius:12px;padding:24px;width:100%;max-width:400px;margin:auto}}
.modal-title{{font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:2px;color:var(--laranja);margin-bottom:16px}}
.input-group{{margin-bottom:14px}}
.input-group label{{font-size:12px;color:var(--cinza);display:block;margin-bottom:6px;font-weight:600}}
.input-group input,.input-group select{{width:100%;background:var(--azul);border:1px solid var(--borda);color:var(--branco);font-family:'Barlow',sans-serif;font-size:14px;padding:10px 14px;border-radius:8px}}
.calc-result{{background:var(--azul);border:1px solid var(--borda);border-radius:8px;padding:14px;margin-top:16px}}
.calc-line{{display:flex;justify-content:space-between;font-size:13px;margin-bottom:8px;color:var(--cinza)}}
.calc-line.destaque{{color:#4ade80;font-weight:700;font-size:15px;border-top:1px solid var(--borda);padding-top:10px;margin-top:4px}}
.btn-fechar{{background:transparent;color:var(--cinza);border:1px solid var(--borda);font-family:'Barlow',sans-serif;font-size:13px;padding:8px;border-radius:8px;cursor:pointer;width:100%;margin-top:8px}}
.sem-vagas{{text-align:center;padding:48px 24px;color:var(--cinza)}}
.sem-vagas-icon{{font-size:48px;margin-bottom:16px}}
.sem-vagas-titulo{{font-family:'Bebas Neue',sans-serif;font-size:24px;color:var(--branco);margin-bottom:8px}}
.sem-vagas-texto{{font-size:14px;line-height:1.6}}
footer{{text-align:center;padding:28px;color:var(--cinza);font-size:12px;border-top:1px solid var(--borda);margin-top:28px}}
footer strong{{color:var(--laranja)}}
</style>
</head>
<body>
<header>
  <div class="logo">Tec<span>System</span> Brasil</div>
  <span id="horario" style="font-size:11px;color:var(--cinza)"></span>
</header>
<div class="hero">
  <h1>Vagas para <span>Técnicos</span></h1>
  <p>90+ especialidades · Elétrica · Mecânica · Automação · Qualidade · Segurança</p>
  <div class="stats">
    <div class="stat"><div class="stat-num" id="contador">{total}</div><div class="stat-label">Vagas 2026</div></div>
    <div class="stat"><div class="stat-num">90+</div><div class="stat-label">Especialidades</div></div>
    <div class="stat"><div class="stat-num">BR</div><div class="stat-label">Todo Brasil</div></div>
  </div>
</div>
<div class="filters">
  <button class="filter-btn active" onclick="filtrarArea('todas',this)">Todas</button>
  <button class="filter-btn" onclick="filtrarArea('eletrica',this)">⚡ Elétrica</button>
  <button class="filter-btn" onclick="filtrarArea('mecanica',this)">🔩 Mecânica</button>
  <button class="filter-btn" onclick="filtrarArea('automacao',this)">🤖 Automação</button>
  <button class="filter-btn" onclick="filtrarArea('qualidade',this)">📊 Qualidade</button>
  <button class="filter-btn" onclick="filtrarArea('seguranca',this)">🦺 Segurança</button>
  <select class="sel" onchange="filtrarEstado(this.value)">{opts_estados}</select>
  <select class="sel" onchange="filtrarEsp(this.value)">
    <option value="todas">🔧 Todas as especialidades</option>
    {tec_opts}
  </select>
</div>
<div class="content">
  <div class="update-bar"><div class="dot"></div>Apenas vagas de 2026 · Atualizado automaticamente · {agora}</div>

  <!-- CALCULADORAS -->
  <div class="calc-section">
    <div class="calc-section-titulo">🧮 Calculadoras Trabalhistas</div>
    <div class="calc-grid">
      <button class="calc-card-btn" onclick="abrirModal('m-salario')"><div class="calc-card-icon">💰</div><div class="calc-card-nome">Salário Líquido</div><div class="calc-card-desc">INSS + IRRF</div></button>
      <button class="calc-card-btn" onclick="abrirModal('m-ferias')"><div class="calc-card-icon">🏖️</div><div class="calc-card-nome">Férias</div><div class="calc-card-desc">+ 1/3 constitucional</div></button>
      <button class="calc-card-btn" onclick="abrirModal('m-rescisao')"><div class="calc-card-icon">📦</div><div class="calc-card-nome">Rescisão</div><div class="calc-card-desc">Demissão ou pedido</div></button>
      <button class="calc-card-btn" onclick="abrirModal('m-horaextra')"><div class="calc-card-icon">⏰</div><div class="calc-card-nome">Hora Extra</div><div class="calc-card-desc">50%, 100% e noturna</div></button>
      <button class="calc-card-btn" onclick="abrirModal('m-noturno')"><div class="calc-card-icon">🌙</div><div class="calc-card-nome">Adicional Noturno</div><div class="calc-card-desc">20% sobre salário</div></button>
      <button class="calc-card-btn" onclick="abrirModal('m-insalub')"><div class="calc-card-icon">⚠️</div><div class="calc-card-nome">Insalubridade</div><div class="calc-card-desc">e Periculosidade</div></button>
      <button class="calc-card-btn" onclick="abrirModal('m-decimo')"><div class="calc-card-icon">🎄</div><div class="calc-card-nome">13º Salário</div><div class="calc-card-desc">Proporcional ou cheio</div></button>
    </div>
  </div>

  <div class="grid" id="grid">{cards}</div>
  <div id="sem-vagas" style="display:none" class="sem-vagas">
    <div class="sem-vagas-icon">🔍</div>
    <div class="sem-vagas-titulo">Nenhuma vaga encontrada</div>
    <div class="sem-vagas-texto">Não encontramos vagas para o filtro selecionado.<br><br>• Selecione outra especialidade ou estado<br>• Volte mais tarde — atualizamos 5x por dia<br>• Clique em <strong>"Todas"</strong> para ver todas as vagas</div>
  </div>
</div>

<!-- MODAIS -->
<div class="modal" id="m-salario">
  <div class="modal-box">
    <div class="modal-title">💰 Salário Líquido</div>
    <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="sl-b" placeholder="Ex: 3500" oninput="calcSalario()"></div>
    <div class="input-group"><label>Dependentes para IR</label><input type="number" id="sl-d" placeholder="0" value="0" oninput="calcSalario()"></div>
    <div class="calc-result" id="sl-res" style="display:none">
      <div class="calc-line"><span>Salário Bruto</span><span id="sl-1"></span></div>
      <div class="calc-line"><span>(-) INSS</span><span id="sl-2" style="color:#f87171"></span></div>
      <div class="calc-line"><span>(-) IRRF</span><span id="sl-3" style="color:#f87171"></span></div>
      <div class="calc-line destaque"><span>💵 Líquido</span><span id="sl-4"></span></div>
      <div class="calc-line" style="font-size:11px;margin-top:6px"><span>FGTS (empregador)</span><span id="sl-5" style="color:#4ade80"></span></div>
    </div>
    <button class="btn-fechar" onclick="fecharModal('m-salario')">✕ Fechar</button>
  </div>
</div>

<div class="modal" id="m-ferias">
  <div class="modal-box">
    <div class="modal-title">🏖️ Férias</div>
    <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="fe-b" placeholder="Ex: 3500" oninput="calcFerias()"></div>
    <div class="input-group"><label>Meses trabalhados no período</label><input type="number" id="fe-m" placeholder="12" value="12" min="1" max="12" oninput="calcFerias()"></div>
    <div class="calc-result" id="fe-res" style="display:none">
      <div class="calc-line"><span>Férias proporcional</span><span id="fe-1"></span></div>
      <div class="calc-line"><span>(+) 1/3 constitucional</span><span id="fe-2" style="color:#4ade80"></span></div>
      <div class="calc-line"><span>Total bruto</span><span id="fe-3"></span></div>
      <div class="calc-line"><span>(-) INSS</span><span id="fe-4" style="color:#f87171"></span></div>
      <div class="calc-line"><span>(-) IR</span><span id="fe-5" style="color:#f87171"></span></div>
      <div class="calc-line destaque"><span>🏖️ Férias Líquidas</span><span id="fe-6"></span></div>
    </div>
    <button class="btn-fechar" onclick="fecharModal('m-ferias')">✕ Fechar</button>
  </div>
</div>

<div class="modal" id="m-rescisao">
  <div class="modal-box">
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
  </div>
</div>

<div class="modal" id="m-horaextra">
  <div class="modal-box">
    <div class="modal-title">⏰ Hora Extra</div>
    <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="he-b" placeholder="Ex: 3500" oninput="calcHoraExtra()"></div>
    <div class="input-group"><label>Quantidade de horas extras</label><input type="number" id="he-h" placeholder="Ex: 10" oninput="calcHoraExtra()"></div>
    <div class="input-group"><label>Tipo</label>
      <select id="he-t" onchange="calcHoraExtra()"><option value="50">50% — Dias úteis</option><option value="100">100% — Domingos/Feriados</option><option value="70">70% — Noturna (50%+20%)</option></select>
    </div>
    <div class="calc-result" id="he-res" style="display:none">
      <div class="calc-line"><span>Valor hora normal</span><span id="he-1"></span></div>
      <div class="calc-line"><span>Valor hora extra</span><span id="he-2"></span></div>
      <div class="calc-line destaque"><span>⏰ Total a receber</span><span id="he-3"></span></div>
    </div>
    <button class="btn-fechar" onclick="fecharModal('m-horaextra')">✕ Fechar</button>
  </div>
</div>

<div class="modal" id="m-noturno">
  <div class="modal-box">
    <div class="modal-title">🌙 Adicional Noturno</div>
    <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="no-b" placeholder="Ex: 3500" oninput="calcNoturno()"></div>
    <div class="input-group"><label>Horas noturnas por mês</label><input type="number" id="no-h" placeholder="Ex: 44" oninput="calcNoturno()"></div>
    <div class="calc-result" id="no-res" style="display:none">
      <div class="calc-line"><span>Salário base</span><span id="no-1"></span></div>
      <div class="calc-line"><span>(+) Adicional noturno 20%</span><span id="no-2" style="color:#4ade80"></span></div>
      <div class="calc-line destaque"><span>🌙 Total com adicional</span><span id="no-3"></span></div>
      <div class="calc-line" style="font-size:11px;margin-top:6px;color:var(--cinza)"><span>Horário noturno: 22h às 5h</span><span></span></div>
    </div>
    <button class="btn-fechar" onclick="fecharModal('m-noturno')">✕ Fechar</button>
  </div>
</div>

<div class="modal" id="m-insalub">
  <div class="modal-box">
    <div class="modal-title">⚠️ Insalubridade / Periculosidade</div>
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
  </div>
</div>

<div class="modal" id="m-decimo">
  <div class="modal-box">
    <div class="modal-title">🎄 13º Salário</div>
    <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="de-b" placeholder="Ex: 3500" oninput="calcDecimo()"></div>
    <div class="input-group"><label>Meses trabalhados no ano</label><input type="number" id="de-m" placeholder="12" value="12" min="1" max="12" oninput="calcDecimo()"></div>
    <div class="calc-result" id="de-res" style="display:none">
      <div class="calc-line"><span>13º bruto proporcional</span><span id="de-1"></span></div>
      <div class="calc-line"><span>(-) INSS</span><span id="de-2" style="color:#f87171"></span></div>
      <div class="calc-line"><span>(-) IRRF</span><span id="de-3" style="color:#f87171"></span></div>
      <div class="calc-line destaque"><span>🎄 13º Líquido</span><span id="de-4"></span></div>
      <div class="calc-line" style="font-size:11px;margin-top:6px;color:var(--cinza)"><span>1ª parcela: nov · 2ª parcela: dez</span><span></span></div>
    </div>
    <button class="btn-fechar" onclick="fecharModal('m-decimo')">✕ Fechar</button>
  </div>
</div>

<footer>
  <strong>TecSystem Brasil</strong> · 90+ especialidades · Apenas vagas de 2026<br>
  <span style="font-size:11px">Links redirecionam para os sites originais das vagas</span>
</footer>

<script data-goatcounter="https://tecsystembrasil.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<script>
function atualizarHorario(){{const a=new Date();document.getElementById('horario').textContent=new Intl.DateTimeFormat('pt-BR',{{timeZone:'America/Sao_Paulo',day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'}}).format(a);}}
atualizarHorario();setInterval(atualizarHorario,60000);
function abrirModal(id){{document.getElementById(id).classList.add('open');}}
function fecharModal(id){{document.getElementById(id).classList.remove('open');}}
document.querySelectorAll('.modal').forEach(m=>m.addEventListener('click',function(e){{if(e.target===this)fecharModal(this.id);}}));
let aA='todas',eA='todos',xA='todas';
function filtrarArea(a,b){{aA=a;document.querySelectorAll('.filter-btn').forEach(x=>x.classList.remove('active'));b.classList.add('active');aplicar();}}
function filtrarEstado(v){{eA=v;aplicar();}}
function filtrarEsp(v){{xA=v;aplicar();}}
function aplicar(){{let n=0;document.querySelectorAll('#grid .card').forEach(c=>{{const ok=(aA==='todas'||c.dataset.area===aA)&&(eA==='todos'||c.dataset.estado===eA)&&(xA==='todas'||c.dataset.esp.includes(xA));c.style.display=ok?'block':'none';if(ok)n++;}});document.getElementById('contador').textContent=n;document.getElementById('sem-vagas').style.display=n===0?'block':'none';document.getElementById('grid').style.display=n===0?'none':'flex';}}
function iNSS(b){{const f=[[1518,0.075],[2793.88,0.09],[4190.83,0.12],[8157.41,0.14]];let i=0,a=0;for(const[t,q]of f){{if(b<=t){{i+=(b-a)*q;break;}}i+=(t-a)*q;a=t;}}return Math.min(i,908.86);}}
function iR(b,d){{const x=b-d*189.59;const f=[[2259.2,0,0],[2826.65,0.075,169.44],[3751.05,0.15,381.44],[4664.68,0.225,662.77],[Infinity,0.275,896]];for(const[t,a,e]of f){{if(x<=t)return Math.max(0,x*a-e);}}return 0;}}
function R(v){{return'R$ '+v.toFixed(2).replace('.',',').replace(/\B(?=(\d{{3}})+(?!\d))/g,'.');}}
function calcSalario(){{const b=parseFloat(document.getElementById('sl-b').value)||0,d=parseInt(document.getElementById('sl-d').value)||0;if(!b){{document.getElementById('sl-res').style.display='none';return;}}const i=iNSS(b),r=iR(b-i,d),l=b-i-r;document.getElementById('sl-1').textContent=R(b);document.getElementById('sl-2').textContent='- '+R(i);document.getElementById('sl-3').textContent='- '+R(r);document.getElementById('sl-4').textContent=R(l);document.getElementById('sl-5').textContent='+ '+R(b*0.08);document.getElementById('sl-res').style.display='block';}}
function calcFerias(){{const s=parseFloat(document.getElementById('fe-b').value)||0,m=parseInt(document.getElementById('fe-m').value)||12;if(!s){{document.getElementById('fe-res').style.display='none';return;}}const p=s*(m/12),t=p/3,tot=p+t,i=iNSS(tot),r=iR(tot-i,0);document.getElementById('fe-1').textContent=R(p);document.getElementById('fe-2').textContent='+ '+R(t);document.getElementById('fe-3').textContent=R(tot);document.getElementById('fe-4').textContent='- '+R(i);document.getElementById('fe-5').textContent='- '+R(r);document.getElementById('fe-6').textContent=R(tot-i-r);document.getElementById('fe-res').style.display='block';}}
function calcRescisao(){{const s=parseFloat(document.getElementById('re-b').value)||0,m=parseInt(document.getElementById('re-m').value)||1,tp=document.getElementById('re-t').value;if(!s){{document.getElementById('re-res').style.display='none';return;}}const dec=s*(m/12),fp=(s*(m/12))*(4/3),fg=s*0.08*m;let mu=tp==='sem_justa'?fg*0.4:tp==='acordo'?fg*0.2:0;const tot=s+dec+fp+mu;document.getElementById('re-1').textContent=R(s);document.getElementById('re-2').textContent=R(dec);document.getElementById('re-3').textContent=R(fp);document.getElementById('re-4').textContent='+ '+R(mu);document.getElementById('re-multa-linha').style.display=mu>0?'flex':'none';document.getElementById('re-5').textContent=R(tot);document.getElementById('re-res').style.display='block';}}
function calcHoraExtra(){{const s=parseFloat(document.getElementById('he-b').value)||0,h=parseFloat(document.getElementById('he-h').value)||0,tp=parseFloat(document.getElementById('he-t').value);if(!s||!h){{document.getElementById('he-res').style.display='none';return;}}const hb=s/220,he=hb*(1+tp/100);document.getElementById('he-1').textContent=R(hb);document.getElementById('he-2').textContent=R(he);document.getElementById('he-3').textContent=R(he*h);document.getElementById('he-res').style.display='block';}}
function calcNoturno(){{const s=parseFloat(document.getElementById('no-b').value)||0,h=parseFloat(document.getElementById('no-h').value)||0;if(!s){{document.getElementById('no-res').style.display='none';return;}}const ad=(s/220)*0.2*h;document.getElementById('no-1').textContent=R(s);document.getElementById('no-2').textContent='+ '+R(ad);document.getElementById('no-3').textContent=R(s+ad);document.getElementById('no-res').style.display='block';}}
function calcInsalub(){{const s=parseFloat(document.getElementById('in-b').value)||0,tp=document.getElementById('in-t').value;if(!s){{document.getElementById('in-res').style.display='none';return;}}const sm=1518;let ad=tp==='30p'?s*0.3:sm*(parseFloat(tp)/100);document.getElementById('in-1').textContent=R(s);document.getElementById('in-2').textContent='+ '+R(ad);document.getElementById('in-3').textContent=R(s+ad);document.getElementById('in-res').style.display='block';}}
function calcDecimo(){{const s=parseFloat(document.getElementById('de-b').value)||0,m=parseInt(document.getElementById('de-m').value)||12;if(!s){{document.getElementById('de-res').style.display='none';return;}}const b=s*(m/12),i=iNSS(b),r=iR(b-i,0);document.getElementById('de-1').textContent=R(b);document.getElementById('de-2').textContent='- '+R(i);document.getElementById('de-3').textContent='- '+R(r);document.getElementById('de-4').textContent=R(b-i-r);document.getElementById('de-res').style.display='block';}}
</script>
</body>
</html>"""


def main():
    print(f"\n🤖 TecSystem Brasil v6 — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
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
