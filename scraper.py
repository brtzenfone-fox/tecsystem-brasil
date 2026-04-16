"""
TecSystem Brasil - Robô de Vagas v5
=====================================
- 90+ tipos de técnicos industriais
- Extrai benefícios das vagas do Gupy
- Filtro por especialidade, estado e área
- Calculadora de salário líquido
- Filtra só vagas de 2026
- Remove vagas encerradas automaticamente
- Mensagem amigável quando não há vagas
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9",
}

TECNICOS = [
    "técnico em refrigeração industrial",
    "técnico em elétrica industrial",
    "técnico em eletrotécnica",
    "técnico em eletrônica industrial",
    "técnico em automação industrial",
    "técnico em mecatrônica",
    "técnico em mecânica industrial",
    "técnico em manutenção industrial",
    "técnico em manutenção mecânica",
    "técnico em manutenção elétrica",
    "técnico em manutenção eletromecânica",
    "técnico em instrumentação industrial",
    "técnico em processos industriais",
    "técnico em química industrial",
    "técnico em petroquímica",
    "técnico em metalurgia",
    "técnico em soldagem",
    "técnico em caldeiraria",
    "técnico em tubulação industrial",
    "técnico em hidráulica industrial",
    "técnico em pneumática",
    "técnico em utilidades industriais",
    "técnico em caldeiras",
    "técnico em vapor e utilidades",
    "técnico em ar comprimido",
    "técnico em HVAC",
    "técnico em climatização",
    "técnico em comando elétrico",
    "técnico em painéis elétricos",
    "técnico em PLC",
    "técnico em SCADA",
    "técnico em robótica industrial",
    "técnico em CNC",
    "técnico em usinagem",
    "técnico em ferramentaria",
    "técnico em produção industrial",
    "técnico em controle de qualidade",
    "técnico em inspeção de qualidade",
    "técnico em ensaios não destrutivos",
    "técnico em metrologia",
    "técnico em segurança do trabalho",
    "técnico em meio ambiente",
    "técnico em saneamento industrial",
    "técnico em logística industrial",
    "técnico em manutenção preditiva",
    "técnico em manutenção preventiva",
    "técnico em manutenção corretiva",
    "técnico em vibração",
    "técnico em análise de óleo",
    "técnico em lubrificação industrial",
    "técnico em motores elétricos",
    "técnico em geradores",
    "técnico em subestações",
    "técnico em energia",
    "técnico em telecomunicações industriais",
    "técnico em redes industriais",
    "técnico em automação predial",
    "técnico em alimentos",
    "técnico em laticínios",
    "técnico em biotecnologia industrial",
    "técnico em papel e celulose",
    "técnico em mineração",
    "técnico em siderurgia",
    "técnico em plástico",
    "técnico em borracha",
    "técnico em cerâmica",
    "técnico em têxtil",
    "técnico em embalagens",
    "técnico em farmacêutica",
    "técnico em cosméticos",
    "técnico em laboratório industrial",
    "técnico em operação de máquinas",
    "técnico em comissionamento",
    "técnico em assistência técnica industrial",
    "técnico em manutenção de compressores",
    "técnico em bombas industriais",
    "técnico em válvulas industriais",
    "técnico em torres de resfriamento",
    "técnico em tratamento de água",
    "técnico em efluentes industriais",
    "técnico em gás industrial",
    "técnico em combustão industrial",
    "técnico em fornos industriais",
    "técnico em instalações industriais",
    "técnico em montagem industrial",
    "técnico em planejamento de manutenção",
    "técnico em PCM",
    "técnico em confiabilidade industrial",
]

# Palavras-chave de benefícios para detectar
PALAVRAS_BENEFICIOS = [
    "vale transporte", "vale refeição", "vale alimentação",
    "plano médico", "plano de saúde", "assistência médica",
    "plano odontológico", "assistência odontológica",
    "seguro de vida", "previdência privada",
    "participação nos lucros", "plr", "ppr",
    "gympass", "total pass", "academia",
    "home office", "trabalho remoto", "híbrido",
    "clt", "pj", "cnpj",
    "13º salário", "férias",
    "fgts", "inss",
    "auxílio creche", "auxílio educação", "bolsa estudo",
    "convênio médico", "convênio odontológico",
    "cesta básica", "ticket",
]

PALAVRAS_DESCARTAR = [
    "banco de talentos", "banco de talento",
    "encerrad", "finalizad", "expirad", "inativ", "cancelad",
    "processo seletivo encerrado", "vaga encerrada",
    "não está mais disponível", "job expired",
    "talentos 2024", "talentos 2025", "2023", "2024",
]

ANO_ATUAL = "2026"
CACHE_FILE = "vagas_cache.json"

ESTADOS = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas",
    "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
    "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
    "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina",
    "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins",
}


# ─── EXTRAÇÃO DE BENEFÍCIOS ───────────────────────────────────────────────────

def extrair_beneficios_gupy(job_id, company_slug):
    """Tenta extrair benefícios da API do Gupy."""
    try:
        url = f"https://{company_slug}.gupy.io/api/v1/jobs/{job_id}"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return []
        data = resp.json()
        beneficios = []

        # Tenta pegar benefícios direto da API
        benefits_field = data.get("benefits", []) or data.get("beneficios", [])
        if benefits_field and isinstance(benefits_field, list):
            for b in benefits_field[:6]:
                if isinstance(b, dict):
                    nome = b.get("name", "") or b.get("nome", "")
                    if nome:
                        beneficios.append(nome[:30])
                elif isinstance(b, str):
                    beneficios.append(b[:30])
            if beneficios:
                return beneficios

        # Se não achou na API, tenta extrair do texto da vaga
        descricao = data.get("description", "") or data.get("descricao", "")
        if descricao:
            texto_lower = descricao.lower()
            for palavra in PALAVRAS_BENEFICIOS:
                if palavra in texto_lower:
                    beneficios.append(palavra.title())
            return beneficios[:6]

    except Exception as e:
        pass
    return []


def extrair_beneficios_pagina(url):
    """Extrai benefícios de uma página de vaga genérica."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
        texto = soup.get_text().lower()
        beneficios = []
        for palavra in PALAVRAS_BENEFICIOS:
            if palavra in texto:
                beneficios.append(palavra.title())
        return beneficios[:6]
    except:
        return []


# ─── UTILITÁRIOS ──────────────────────────────────────────────────────────────

def detectar_area(texto):
    texto = texto.lower()
    if any(p in texto for p in ["elétric", "eletric", "eletrom", "painel", "subestac", "motor", "gerador"]):
        return "eletrica"
    if any(p in texto for p in ["mecatrôn", "mecatron", "plc", "scada", "robotic", "automac", "automaç", "cnc"]):
        return "automacao"
    if any(p in texto for p in ["qualidad", "inspeç", "metrolog", "ensaio", "end", "calibr"]):
        return "qualidade"
    if any(p in texto for p in ["seguranç", "meio ambient", "saneam"]):
        return "seguranca"
    return "mecanica"


def detectar_estado(texto):
    texto_upper = texto.upper()
    for sigla, nome in ESTADOS.items():
        if f", {sigla}" in texto or nome.upper() in texto_upper:
            return sigla
    return "BR"


def titulo_valido(titulo):
    titulo_lower = titulo.lower()
    for palavra in PALAVRAS_DESCARTAR:
        if palavra in titulo_lower:
            return False
    return True


# ─── FONTES ───────────────────────────────────────────────────────────────────

def buscar_gupy():
    vagas = []
    print("🔍 Buscando no Gupy...")
    for termo in TECNICOS[:25]:
        try:
            url = f"https://portal.api.gupy.io/api/v1/jobs?jobName={requests.utils.quote(termo)}&limit=5"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            data = resp.json()
            jobs = data.get("data", [])
            for job in jobs:
                publicado = str(job.get("publishedDate", "") or job.get("createdAt", ""))
                if ANO_ATUAL not in publicado:
                    continue
                titulo = job.get("name", "")[:80]
                if not titulo_valido(titulo):
                    continue
                local = f"{job.get('city', 'Brasil')}, {job.get('state', '')}"

                # Tenta extrair benefícios
                beneficios = []
                try:
                    job_url = job.get("jobUrl", "")
                    benefits_raw = job.get("benefits", [])
                    if benefits_raw:
                        for b in benefits_raw[:6]:
                            if isinstance(b, dict):
                                nome = b.get("name", "")
                                if nome:
                                    beneficios.append(nome[:30])
                            elif isinstance(b, str):
                                beneficios.append(b[:30])
                except:
                    pass

                vagas.append({
                    "titulo": titulo,
                    "empresa": job.get("careerPageName", "Empresa")[:50],
                    "local": local,
                    "estado": detectar_estado(local),
                    "url": job.get("jobUrl", "#"),
                    "fonte": "gupy.io",
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "area": detectar_area(titulo),
                    "beneficios": beneficios,
                })
            time.sleep(1.0)
        except Exception as e:
            print(f"  ⚠️ Gupy erro: {e}")
    print(f"  ✅ Gupy: {len(vagas)} vagas")
    return vagas


def buscar_vagas_com_br():
    vagas = []
    print("🔍 Buscando no vagas.com.br...")
    termos_url = [
        "tecnico-manutencao-eletrica", "tecnico-manutencao-mecanica",
        "tecnico-mecatronica", "tecnico-automacao-industrial",
        "tecnico-instrumentacao", "tecnico-soldagem",
        "tecnico-caldeiraria", "tecnico-seguranca-trabalho",
        "tecnico-qualidade", "tecnico-refrigeracao",
    ]
    for termo in termos_url:
        try:
            url = f"https://www.vagas.com.br/vagas-de-{termo}"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.find_all("li", class_="vaga")[:8]
            for card in cards:
                titulo_el = card.find("a", class_="link-detalhes-vaga")
                empresa_el = card.find("span", class_="empr-name")
                local_el = card.find("span", class_="local")
                data_el = card.find("span", class_="data-publicacao") or card.find("time")
                if not titulo_el:
                    continue
                titulo = titulo_el.get_text(strip=True)[:80]
                if not titulo_valido(titulo):
                    continue
                data_texto = data_el.get_text(strip=True) if data_el else ""
                if "2025" in data_texto or "2024" in data_texto:
                    continue
                local = local_el.get_text(strip=True)[:40] if local_el else "Brasil"
                link = "https://www.vagas.com.br" + titulo_el.get("href", "")

                # Tenta extrair benefícios da listagem
                beneficios = []
                try:
                    benef_el = card.find(class_=lambda c: c and "beneficio" in c.lower())
                    if benef_el:
                        for b in benef_el.find_all("span")[:6]:
                            texto_b = b.get_text(strip=True)
                            if texto_b:
                                beneficios.append(texto_b[:30])
                except:
                    pass

                vagas.append({
                    "titulo": titulo,
                    "empresa": empresa_el.get_text(strip=True)[:50] if empresa_el else "Empresa",
                    "local": local,
                    "estado": detectar_estado(local),
                    "url": link,
                    "fonte": "vagas.com.br",
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "area": detectar_area(titulo),
                    "beneficios": beneficios,
                })
            time.sleep(1.5)
        except Exception as e:
            print(f"  ⚠️ vagas.com.br erro: {e}")
    print(f"  ✅ vagas.com.br: {len(vagas)} vagas")
    return vagas


def buscar_infojobs():
    vagas = []
    print("🔍 Buscando no InfoJobs...")
    termos = [
        "tecnico-de-manutencao-eletrica", "tecnico-de-manutencao-mecanica",
        "tecnico-mecatronica", "tecnico-instrumentacao",
    ]
    for termo in termos:
        try:
            url = f"https://www.infojobs.com.br/empregos/{termo}/"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.find_all("div", class_="ij-offercard")[:5]
            for card in cards:
                titulo_el = card.find("a", class_="ij-offercard-title")
                empresa_el = card.find("span", class_="ij-offercard-company")
                local_el = card.find("span", class_="ij-offercard-location")
                if not titulo_el:
                    continue
                titulo = titulo_el.get_text(strip=True)[:80]
                if not titulo_valido(titulo):
                    continue
                local = local_el.get_text(strip=True)[:40] if local_el else "Brasil"
                vagas.append({
                    "titulo": titulo,
                    "empresa": empresa_el.get_text(strip=True)[:50] if empresa_el else "Empresa",
                    "local": local,
                    "estado": detectar_estado(local),
                    "url": titulo_el.get("href", "#"),
                    "fonte": "infojobs.com.br",
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "area": detectar_area(titulo),
                    "beneficios": [],
                })
            time.sleep(1.5)
        except Exception as e:
            print(f"  ⚠️ InfoJobs erro: {e}")
    print(f"  ✅ InfoJobs: {len(vagas)} vagas")
    return vagas


def verificar_cache(vagas_cache):
    if not vagas_cache:
        return []
    print(f"\n🔎 Verificando {len(vagas_cache)} vagas do cache...")
    vagas_ativas = []
    for vaga in vagas_cache:
        if not titulo_valido(vaga.get("titulo", "")):
            continue
        try:
            resp = requests.get(vaga["url"], headers=HEADERS, timeout=8)
            if resp.status_code in [404, 410]:
                print(f"  ❌ Removida: {vaga['titulo'][:40]}")
                continue
            texto = resp.text.lower()
            if any(p in texto for p in ["vaga encerrada", "job expired", "não está mais disponível"]):
                print(f"  ❌ Encerrada: {vaga['titulo'][:40]}")
                continue
        except:
            pass
        # Garante que o campo beneficios existe
        if "beneficios" not in vaga:
            vaga["beneficios"] = []
        vagas_ativas.append(vaga)
        time.sleep(0.3)
    print(f"  ✅ {len(vagas_ativas)} vagas ativas")
    return vagas_ativas


def remover_duplicatas(vagas):
    vistas = set()
    unicas = []
    for v in vagas:
        if v["url"] not in vistas and len(v["titulo"]) > 5:
            vistas.add(v["url"])
            unicas.append(v)
    return unicas


def carregar_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


# ─── GERADOR HTML ─────────────────────────────────────────────────────────────

CORES = {
    "eletrica":  ("b-el", "ELÉTRICA"),
    "mecanica":  ("b-me", "MECÂNICA"),
    "automacao": ("b-au", "AUTOMAÇÃO"),
    "qualidade": ("b-qu", "QUALIDADE"),
    "seguranca": ("b-se", "SEGURANÇA"),
}

ICONES_BENEFICIOS = {
    "vale transporte": "🚌",
    "vale refeição": "🍽️",
    "vale alimentação": "🛒",
    "plano médico": "🏥",
    "plano de saúde": "🏥",
    "assistência médica": "🏥",
    "convênio médico": "🏥",
    "plano odontológico": "🦷",
    "assistência odontológica": "🦷",
    "convênio odontológico": "🦷",
    "seguro de vida": "🛡️",
    "previdência privada": "💰",
    "participação nos lucros": "💵",
    "plr": "💵",
    "gympass": "💪",
    "total pass": "💪",
    "academia": "💪",
    "home office": "🏠",
    "trabalho remoto": "🏠",
    "híbrido": "🔄",
    "cesta básica": "🧺",
    "auxílio educação": "📚",
    "bolsa estudo": "📚",
}


def icone_beneficio(b):
    b_lower = b.lower()
    for chave, icone in ICONES_BENEFICIOS.items():
        if chave in b_lower:
            return icone
    return "✅"


def gerar_beneficios_html(beneficios):
    if not beneficios:
        return ""
    tags = ""
    for b in beneficios[:5]:
        icone = icone_beneficio(b)
        tags += f'<span class="benef-tag">{icone} {b}</span>'
    return f'<div class="beneficios">{tags}</div>'


def gerar_card(v):
    area = v.get("area", "mecanica")
    cls, label = CORES.get(area, CORES["mecanica"])
    estado = v.get("estado", "BR")
    esp = v.get("titulo", "").lower()
    beneficios = v.get("beneficios", [])
    beneficios_html = gerar_beneficios_html(beneficios)

    return f"""<a class="card" href="{v['url']}" target="_blank" data-area="{area}" data-estado="{estado}" data-esp="{esp}">
<div class="card-top">
  <div class="card-info">
    <div class="titulo">{v['titulo']}</div>
    <div class="empresa">{v['empresa']} · {v['local']}</div>
  </div>
  <div class="badge {cls}">{label}</div>
</div>
{beneficios_html}
<div class="card-footer">
  <div class="fonte">🔗 {v['fonte']} · {v['data']}</div>
  <div class="btn">VER VAGA →</div>
</div>
</a>"""


def gerar_opcoes_estados(vagas):
    estados_usados = sorted(set(v.get("estado", "BR") for v in vagas if v.get("estado") != "BR"))
    opts = '<option value="todos">🌎 Todos os estados</option>'
    for s in estados_usados:
        opts += f'<option value="{s}">{s} — {ESTADOS.get(s, s)}</option>'
    return opts


def gerar_html(vagas):
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    cards = "\n".join(gerar_card(v) for v in vagas)
    total = len(vagas)
    opts_estados = gerar_opcoes_estados(vagas)

    tecnicos_options = ""
    for tec in sorted(TECNICOS):
        label = tec.replace("técnico em ", "").title()
        value = tec.replace("técnico em ", "").lower()
        tecnicos_options += f'<option value="{value}">{label}</option>'

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
.calc-btn{{background:var(--laranja);color:white;border:none;font-family:'Bebas Neue',sans-serif;font-size:18px;letter-spacing:1px;padding:12px 20px;border-radius:8px;cursor:pointer;margin-bottom:20px;width:100%}}
.modal{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);z-index:1000;align-items:center;justify-content:center;padding:16px}}
.modal.open{{display:flex}}
.modal-box{{background:var(--azul2);border:1px solid var(--borda);border-radius:12px;padding:24px;width:100%;max-width:400px}}
.modal-title{{font-family:'Bebas Neue',sans-serif;font-size:24px;letter-spacing:2px;color:var(--laranja);margin-bottom:16px}}
.input-group{{margin-bottom:14px}}
.input-group label{{font-size:12px;color:var(--cinza);display:block;margin-bottom:6px;font-weight:600}}
.input-group input{{width:100%;background:var(--azul);border:1px solid var(--borda);color:var(--branco);font-family:'Barlow',sans-serif;font-size:15px;padding:10px 14px;border-radius:8px}}
.calc-result{{background:var(--azul);border:1px solid var(--borda);border-radius:8px;padding:14px;margin-top:16px}}
.calc-line{{display:flex;justify-content:space-between;font-size:13px;margin-bottom:8px;color:var(--cinza)}}
.calc-line.destaque{{color:#4ade80;font-weight:700;font-size:16px;border-top:1px solid var(--borda);padding-top:10px;margin-top:4px}}
.btn-fechar{{background:transparent;color:var(--cinza);border:1px solid var(--borda);font-family:'Barlow',sans-serif;font-size:13px;padding:8px;border-radius:8px;cursor:pointer;width:100%;margin-top:8px}}
.sem-vagas{{text-align:center;padding:48px 24px;color:var(--cinza)}}
.sem-vagas-icon{{font-size:48px;margin-bottom:16px}}
.sem-vagas-titulo{{font-family:'Bebas Neue',sans-serif;font-size:24px;color:var(--branco);margin-bottom:8px;letter-spacing:1px}}
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
    {tecnicos_options}
  </select>
</div>
<div class="content">
  <div class="update-bar"><div class="dot"></div>Apenas vagas de 2026 · Atualizado automaticamente · {agora}</div>
  <button class="calc-btn" onclick="document.getElementById('modal').classList.add('open')">🧮 CALCULADORA DE SALÁRIO LÍQUIDO</button>
  <div class="grid" id="grid">{cards}</div>
  <div id="sem-vagas" style="display:none" class="sem-vagas">
    <div class="sem-vagas-icon">🔍</div>
    <div class="sem-vagas-titulo">Nenhuma vaga encontrada</div>
    <div class="sem-vagas-texto">
      Não encontramos vagas para o filtro selecionado no momento.<br><br>
      <strong>O que você pode fazer:</strong><br>
      • Selecione outra especialidade ou estado<br>
      • Volte mais tarde — o robô atualiza 5x por dia<br>
      • Clique em <strong>"Todas"</strong> para ver todas as vagas disponíveis
    </div>
  </div>
</div>
<div class="modal" id="modal">
  <div class="modal-box">
    <div class="modal-title">💰 Calculadora de Salário</div>
    <div class="input-group"><label>Salário Bruto (R$)</label><input type="number" id="salario" placeholder="Ex: 3500" oninput="calcular()"></div>
    <div class="input-group"><label>Número de dependentes (para IR)</label><input type="number" id="dependentes" placeholder="0" value="0" oninput="calcular()"></div>
    <div class="calc-result" id="resultado" style="display:none">
      <div class="calc-line"><span>Salário Bruto</span><span id="r-bruto"></span></div>
      <div class="calc-line"><span>(-) INSS</span><span id="r-inss" style="color:#f87171"></span></div>
      <div class="calc-line"><span>(-) IRRF</span><span id="r-ir" style="color:#f87171"></span></div>
      <div class="calc-line destaque"><span>💵 Salário Líquido</span><span id="r-liquido"></span></div>
      <div class="calc-line" style="margin-top:8px;font-size:11px"><span>FGTS depositado pelo empregador</span><span id="r-fgts" style="color:#4ade80"></span></div>
    </div>
    <button class="btn-fechar" onclick="document.getElementById('modal').classList.remove('open')">✕ Fechar</button>
  </div>
</div>
<footer>
  <strong>TecSystem Brasil</strong> · 90+ especialidades · Apenas vagas de 2026<br>
  <span style="font-size:11px">Links redirecionam para os sites originais das vagas</span>
</footer>
<script>
function atualizarHorario(){{const a=new Date();document.getElementById('horario').textContent=new Intl.DateTimeFormat('pt-BR',{{timeZone:'America/Sao_Paulo',day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'}}).format(a);}}
atualizarHorario();setInterval(atualizarHorario,60000);
let areaAtiva='todas',estadoAtivo='todos',espAtiva='todas';
function filtrarArea(a,b){{areaAtiva=a;document.querySelectorAll('.filter-btn').forEach(x=>x.classList.remove('active'));b.classList.add('active');aplicar();}}
function filtrarEstado(v){{estadoAtivo=v;aplicar();}}
function filtrarEsp(v){{espAtiva=v;aplicar();}}
function aplicar(){{
  let n=0;
  document.querySelectorAll('#grid .card').forEach(c=>{{
    const ok=(areaAtiva==='todas'||c.dataset.area===areaAtiva)&&(estadoAtivo==='todos'||c.dataset.estado===estadoAtivo)&&(espAtiva==='todas'||c.dataset.esp.includes(espAtiva));
    c.style.display=ok?'block':'none';
    if(ok)n++;
  }});
  document.getElementById('contador').textContent=n;
  document.getElementById('sem-vagas').style.display=n===0?'block':'none';
  document.getElementById('grid').style.display=n===0?'none':'flex';
}}
function calcularINSS(b){{const f=[[1518.00,0.075],[2793.88,0.09],[4190.83,0.12],[8157.41,0.14]];let i=0,a=0;for(const[t,q]of f){{if(b<=t){{i+=(b-a)*q;break;}}i+=(t-a)*q;a=t;}}return Math.min(i,908.86);}}
function calcularIR(b,d){{const x=b-d*189.59;const f=[[2259.20,0,0],[2826.65,0.075,169.44],[3751.05,0.15,381.44],[4664.68,0.225,662.77],[Infinity,0.275,896.00]];for(const[t,a,e]of f){{if(x<=t)return Math.max(0,x*a-e);}}return 0;}}
function fmt(v){{return'R$ '+v.toFixed(2).replace('.',',').replace(/\B(?=(\d{{3}})+(?!\d))/g,'.');}}
function calcular(){{const b=parseFloat(document.getElementById('salario').value)||0;const d=parseInt(document.getElementById('dependentes').value)||0;if(b<=0){{document.getElementById('resultado').style.display='none';return;}}const i=calcularINSS(b);const r=calcularIR(b-i,d);const l=b-i-r;document.getElementById('r-bruto').textContent=fmt(b);document.getElementById('r-inss').textContent='- '+fmt(i);document.getElementById('r-ir').textContent='- '+fmt(r);document.getElementById('r-liquido').textContent=fmt(l);document.getElementById('r-fgts').textContent='+ '+fmt(b*0.08);document.getElementById('resultado').style.display='block';}}
</script> 
<script data-goatcounter="https://tecsystembrasil.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>"""


def main():
    print(f"\n🤖 TecSystem Brasil v5 — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 50)

    cache = carregar_cache()
    vagas_ativas = verificar_cache(cache)

    vagas_novas = []
    vagas_novas += buscar_gupy()
    vagas_novas += buscar_vagas_com_br()
    vagas_novas += buscar_infojobs()

    todas = vagas_ativas + vagas_novas
    todas = remover_duplicatas(todas)

    print(f"\n📊 Total: {len(todas)} vagas únicas de 2026")

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(todas, f, ensure_ascii=False, indent=2)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(gerar_html(todas))

    print(f"✅ Site atualizado com {len(todas)} vagas!")


if __name__ == "__main__":
    main()
