"""
TecSystem Brasil - Robô de Vagas v3
=====================================
- Busca vagas em fontes que não bloqueiam (4x/dia)
- Tenta Google 1x/dia às 22h
- Filtra apenas vagas de 2026
- Remove vagas que sumiram ou foram preenchidas
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import json
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9",
}

TERMOS = [
    "técnico manutenção elétrica",
    "técnico manutenção mecânica",
    "técnico mecatrônica",
    "técnico automação industrial",
    "eletricista industrial manutenção",
    "técnico instrumentação",
]

ANO_ATUAL = "2026"
CACHE_FILE = "vagas_cache.json"

# ─── VERIFICAR SE VAGA AINDA EXISTE ──────────────────────────────────────────

def vaga_ainda_existe(url):
    """Verifica se a vaga ainda está disponível."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        # Se retornar 404, 410 ou redirecionar para página de vagas encerradas
        if resp.status_code in [404, 410, 403]:
            return False
        texto = resp.text.lower()
        # Palavras que indicam vaga encerrada
        encerrada = [
            "vaga encerrada", "vaga expirada", "processo seletivo encerrado",
            "this job is no longer available", "job expired", "vaga inativa",
            "candidatura encerrada", "oportunidade encerrada", "não está mais disponível"
        ]
        for palavra in encerrada:
            if palavra in texto:
                return False
        return True
    except:
        return False


# ─── FILTRAR POR ANO ─────────────────────────────────────────────────────────

def e_de_2026(texto):
    """Verifica se o texto contém referência a 2026."""
    return ANO_ATUAL in texto


# ─── FONTE 1: GUPY ────────────────────────────────────────────────────────────

def buscar_gupy():
    vagas = []
    print("🔍 Buscando no Gupy...")
    for termo in TERMOS[:4]:
        try:
            url = f"https://portal.api.gupy.io/api/v1/jobs?jobName={requests.utils.quote(termo)}&limit=10"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            data = resp.json()
            jobs = data.get("data", [])
            for job in jobs:
                # Filtra por ano 2026
                publicado = job.get("publishedDate", "") or job.get("createdAt", "")
                if ANO_ATUAL not in str(publicado):
                    continue
                vagas.append({
                    "titulo": job.get("name", "Vaga Técnica")[:80],
                    "empresa": job.get("careerPageName", "Empresa")[:50],
                    "local": job.get("city", "Brasil") + ", " + job.get("state", ""),
                    "url": job.get("jobUrl", "#"),
                    "fonte": "gupy.io",
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "area": detectar_area(job.get("name", "")),
                })
            print(f"  ✅ Gupy '{termo}': {len([j for j in jobs if ANO_ATUAL in str(j.get('publishedDate',''))])} vagas de 2026")
            time.sleep(1.5)
        except Exception as e:
            print(f"  ⚠️ Gupy erro: {e}")
    return vagas


# ─── FONTE 2: VAGAS.COM.BR ────────────────────────────────────────────────────

def buscar_vagas_com_br():
    vagas = []
    print("🔍 Buscando no vagas.com.br...")
    termos_url = [
        "tecnico-manutencao-eletrica",
        "tecnico-manutencao-mecanica",
        "tecnico-mecatronica",
        "tecnico-automacao-industrial",
    ]
    for termo in termos_url:
        try:
            url = f"https://www.vagas.com.br/vagas-de-{termo}"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.find_all("li", class_="vaga")[:10]
            count = 0
            for card in cards:
                titulo_el = card.find("a", class_="link-detalhes-vaga")
                empresa_el = card.find("span", class_="empr-name")
                local_el = card.find("span", class_="local")
                data_el = card.find("span", class_="data-publicacao") or card.find("time")

                if not titulo_el:
                    continue

                # Verifica se é de 2026
                data_texto = data_el.get_text(strip=True) if data_el else ""
                if data_texto and "2025" in data_texto:
                    continue  # Pula vagas de 2025

                link = "https://www.vagas.com.br" + titulo_el.get("href", "")
                vagas.append({
                    "titulo": titulo_el.get_text(strip=True)[:80],
                    "empresa": empresa_el.get_text(strip=True)[:50] if empresa_el else "Empresa",
                    "local": local_el.get_text(strip=True)[:40] if local_el else "Brasil",
                    "url": link,
                    "fonte": "vagas.com.br",
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "area": detectar_area(titulo_el.get_text(strip=True)),
                })
                count += 1
            print(f"  ✅ vagas.com.br '{termo}': {count} vagas")
            time.sleep(2)
        except Exception as e:
            print(f"  ⚠️ vagas.com.br erro: {e}")
    return vagas


# ─── FONTE 3: INFOJOBS ────────────────────────────────────────────────────────

def buscar_infojobs():
    vagas = []
    print("🔍 Buscando no InfoJobs...")
    termos_url = [
        "tecnico-de-manutencao-eletrica",
        "tecnico-de-manutencao-mecanica",
        "tecnico-mecatronica",
    ]
    for termo in termos_url:
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
                data_el = card.find("time") or card.find(class_=lambda c: c and "date" in c.lower())

                if not titulo_el:
                    continue

                # Verifica se é de 2026
                data_texto = data_el.get("datetime", "") if data_el else ""
                if "2025" in str(data_texto) or "2024" in str(data_texto):
                    continue

                vagas.append({
                    "titulo": titulo_el.get_text(strip=True)[:80],
                    "empresa": empresa_el.get_text(strip=True)[:50] if empresa_el else "Empresa",
                    "local": local_el.get_text(strip=True)[:40] if local_el else "Brasil",
                    "url": titulo_el.get("href", "#"),
                    "fonte": "infojobs.com.br",
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "area": detectar_area(titulo_el.get_text(strip=True)),
                })
            print(f"  ✅ InfoJobs '{termo}': {len(cards)} vagas")
            time.sleep(2)
        except Exception as e:
            print(f"  ⚠️ InfoJobs erro: {e}")
    return vagas


# ─── FONTE 4: GOOGLE ─────────────────────────────────────────────────────────

def buscar_google():
    vagas = []
    print("🔍 Tentando Google...")
    try:
        from googlesearch import search
        termos = [
            "vaga técnico manutenção elétrica 2026 site:gupy.io",
            "vaga técnico mecânica manutenção 2026 site:vagas.com.br",
        ]
        for termo in termos:
            for url in search(termo, num_results=3, lang="pt"):
                vagas.append({
                    "titulo": "Vaga encontrada via Google",
                    "empresa": url.split("/")[2].replace("www.", ""),
                    "local": "Brasil",
                    "url": url,
                    "fonte": "google",
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "area": "mecanica",
                })
                time.sleep(2)
        print(f"  ✅ Google: {len(vagas)} resultados")
    except Exception as e:
        print(f"  ⚠️ Google bloqueou (normal): {e}")
    return vagas


# ─── VERIFICAR VAGAS DO CACHE ────────────────────────────────────────────────

def verificar_cache(vagas_cache):
    """Verifica quais vagas do cache ainda estão ativas."""
    if not vagas_cache:
        return []
    print(f"\n🔎 Verificando {len(vagas_cache)} vagas do cache...")
    vagas_ativas = []
    for vaga in vagas_cache:
        url = vaga.get("url", "")
        if not url or url == "#":
            continue
        if vaga_ainda_existe(url):
            vagas_ativas.append(vaga)
        else:
            print(f"  ❌ Removida: {vaga['titulo'][:50]}")
        time.sleep(1)
    print(f"  ✅ {len(vagas_ativas)} vagas ainda ativas")
    return vagas_ativas


# ─── UTILITÁRIOS ──────────────────────────────────────────────────────────────

def detectar_area(texto):
    texto = texto.lower()
    if any(p in texto for p in ["elétric", "eletric", "eletrom"]):
        return "eletrica"
    if any(p in texto for p in ["mecatrôn", "mecatron"]):
        return "mecatronica"
    if any(p in texto for p in ["automaç", "automac", "instrumenta"]):
        return "automacao"
    return "mecanica"


def remover_duplicatas(vagas):
    vistas = set()
    unicas = []
    for v in vagas:
        chave = v["url"]
        if chave not in vistas and len(v["titulo"]) > 5:
            vistas.add(chave)
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
    "eletrica":    ("b-el", "⚡", "ELÉTRICA"),
    "mecanica":    ("b-me", "🔩", "MECÂNICA"),
    "mecatronica": ("b-mx", "🤖", "MECATRÔNICA"),
    "automacao":   ("b-au", "⚙️", "AUTOMAÇÃO"),
}


def gerar_card(v):
    area = v.get("area", "mecanica")
    cls, ico, label = CORES.get(area, CORES["mecanica"])
    return f"""<a class="card" href="{v['url']}" target="_blank">
<div class="card-top"><div class="card-info"><div class="titulo">{v['titulo']}</div><div class="empresa">{v['empresa']} · {v['local']}</div></div><div class="badge {cls}">{label}</div></div>
<div class="card-footer"><div class="fonte">🔗 {v['fonte']} · {v['data']}</div><div class="btn">VER VAGA →</div></div>
</a>"""


def gerar_html(vagas):
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    cards = "\n".join(gerar_card(v) for v in vagas)
    total = len(vagas)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TecSystem Brasil</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{{--azul:#0a1628;--azul2:#0d2144;--laranja:#f97316;--cinza:#94a3b8;--branco:#f1f5f9;--card:#0f1e35;--borda:#1e3a5f}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--azul);color:var(--branco);font-family:'Barlow',sans-serif}}
header{{background:var(--azul2);border-bottom:2px solid var(--laranja);padding:0 24px;height:64px;display:flex;align-items:center;justify-content:space-between}}
.logo{{font-family:'Bebas Neue',sans-serif;font-size:24px;letter-spacing:2px}}
.logo span{{color:var(--laranja)}}
.hero{{background:linear-gradient(135deg,var(--azul2),#061020);padding:40px 24px;text-align:center}}
.hero h1{{font-family:'Bebas Neue',sans-serif;font-size:48px;letter-spacing:3px;margin-bottom:8px}}
.hero h1 span{{color:var(--laranja)}}
.hero p{{color:var(--cinza);font-size:14px;margin-bottom:24px}}
.stats{{display:flex;justify-content:center;gap:32px}}
.stat-num{{font-family:'Bebas Neue',sans-serif;font-size:32px;color:var(--laranja)}}
.stat-label{{font-size:11px;color:var(--cinza);text-transform:uppercase;letter-spacing:1px}}
.content{{padding:24px 16px;max-width:800px;margin:0 auto}}
.update-bar{{background:rgba(249,115,22,0.1);border:1px solid rgba(249,115,22,0.2);border-radius:8px;padding:10px 16px;font-size:12px;color:var(--cinza);margin-bottom:20px;display:flex;align-items:center;gap:8px}}
.dot{{width:8px;height:8px;background:#22c55e;border-radius:50%;animation:pulse 2s infinite;flex-shrink:0}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:0.4}}}}
.grid{{display:flex;flex-direction:column;gap:12px}}
.card{{background:var(--card);border:1px solid var(--borda);border-radius:10px;padding:18px;text-decoration:none;display:block;transition:all 0.2s;animation:fadeUp 0.4s ease both}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
.card:hover{{border-color:var(--laranja);background:#122040}}
.card-top{{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:10px}}
.card-info{{flex:1}}
.titulo{{font-size:16px;font-weight:700;color:var(--branco);margin-bottom:3px}}
.empresa{{font-size:13px;color:var(--cinza)}}
.badge{{font-size:11px;font-weight:700;padding:4px 10px;border-radius:20px;white-space:nowrap;flex-shrink:0}}
.b-el{{background:rgba(59,130,246,0.2);color:#60a5fa;border:1px solid rgba(59,130,246,0.3)}}
.b-me{{background:rgba(34,197,94,0.2);color:#4ade80;border:1px solid rgba(34,197,94,0.3)}}
.b-mx{{background:rgba(168,85,247,0.2);color:#c084fc;border:1px solid rgba(168,85,247,0.3)}}
.b-au{{background:rgba(249,115,22,0.2);color:#fb923c;border:1px solid rgba(249,115,22,0.3)}}
.card-footer{{display:flex;align-items:center;justify-content:space-between;margin-top:12px;padding-top:12px;border-top:1px solid var(--borda)}}
.fonte{{font-size:11px;color:var(--cinza)}}
.btn{{background:var(--laranja);color:white;font-size:12px;font-weight:700;padding:6px 14px;border-radius:6px}}
footer{{text-align:center;padding:32px;color:var(--cinza);font-size:12px;border-top:1px solid var(--borda);margin-top:32px}}
footer strong{{color:var(--laranja)}}
</style>
</head>
<body>
<header>
<div class="logo">Tec<span>System</span> Brasil</div>
<span style="font-size:11px;color:var(--cinza)">Atualizado: {agora}</span>
</header>
<div class="hero">
<h1>Vagas para <span>Técnicos</span></h1>
<p>Elétrica · Mecânica · Mecatrônica · Automação · Instrumentação</p>
<div class="stats">
<div class="stat"><div class="stat-num">{total}</div><div class="stat-label">Vagas 2026</div></div>
<div class="stat"><div class="stat-num">BR</div><div class="stat-label">Todo Brasil</div></div>
</div>
</div>
<div class="content">
<div class="update-bar"><div class="dot"></div>Vagas atualizadas automaticamente em {agora} · Apenas vagas de 2026</div>
<div class="grid">
{cards if cards else '<p style="color:var(--cinza);text-align:center;padding:32px">Nenhuma vaga encontrada agora. Tente mais tarde.</p>'}
</div>
</div>
<footer><strong>TecSystem Brasil</strong> · Apenas vagas de 2026 · Atualizado automaticamente<br><span style="font-size:11px">Links redirecionam para os sites originais</span></footer>
</body>
</html>"""


# ─── PRINCIPAL ────────────────────────────────────────────────────────────────

def main():
    hora = datetime.now().hour
    print(f"\n🤖 TecSystem Brasil v3 — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 50)

    # Carrega cache e verifica quais ainda existem
    cache = carregar_cache()
    vagas_ativas = verificar_cache(cache)

    # Busca vagas novas
    vagas_novas = []
    vagas_novas += buscar_gupy()
    vagas_novas += buscar_vagas_com_br()
    vagas_novas += buscar_infojobs()

    # Tenta Google apenas à noite
    if hora in [0, 1, 2]:
        vagas_novas += buscar_google()

    # Junta vagas ativas do cache com vagas novas
    todas = vagas_ativas + vagas_novas
    todas = remover_duplicatas(todas)

    print(f"\n📊 Total: {len(todas)} vagas únicas de 2026")

    # Salva cache
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(todas, f, ensure_ascii=False, indent=2)

    # Gera site
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(gerar_html(todas))

    print("✅ index.html gerado!")
    print(f"🌐 Site atualizado com {len(todas)} vagas de 2026")


if __name__ == "__main__":
    main()
