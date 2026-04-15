import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import json

TERMOS_BUSCA = [
    "vaga técnico manutenção elétrica site:gupy.io",
    "vaga técnico manutenção mecânica site:gupy.io",
    "vaga técnico mecatrônica manutenção site:gupy.io",
    "vaga técnico automação industrial site:gupy.io",
    "vaga técnico manutenção elétrica site:vagas.com.br",
    "vaga técnico manutenção mecânica site:vagas.com.br",
    "vaga eletricista industrial manutenção site:infojobs.com.br",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def buscar_google(termo, max_resultados=5):
    try:
        from googlesearch import search
        urls = []
        for url in search(termo, num_results=max_resultados, lang="pt"):
            urls.append(url)
            time.sleep(random.uniform(1.5, 3.0))
        return urls
    except Exception as e:
        print(f"Erro: {e}")
        return []

def extrair_vaga(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        titulo = soup.find("h1")
        empresa = soup.find("h2")
        titulo_texto = titulo.get_text(strip=True)[:80] if titulo else "Vaga Técnica"
        empresa_texto = empresa.get_text(strip=True)[:50] if empresa else url.split("/")[2]
        return {
            "titulo": titulo_texto,
            "empresa": empresa_texto,
            "url": url,
            "fonte": url.split("/")[2].replace("www.",""),
            "data": datetime.now().strftime("%d/%m/%Y"),
            "area": detectar_area(titulo_texto),
        }
    except:
        return None

def detectar_area(texto):
    texto = texto.lower()
    if any(p in texto for p in ["elétric","eletric"]):
        return "eletrica"
    if any(p in texto for p in ["mecatrôn","mecatron"]):
        return "mecatronica"
    if any(p in texto for p in ["automaç","automac"]):
        return "automacao"
    return "mecanica"

def gerar_html(vagas):
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    cards = ""
    for v in vagas:
        cards += f"""
        <a class="card" href="{v['url']}" target="_blank">
          <div class="titulo">{v['titulo']}</div>
          <div class="empresa">{v['empresa']}</div>
          <div class="footer">{v['fonte']} · {v['data']}</div>
        </a>"""

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TecSystem Brasil</title>
<style>
  body {{ background:#0a1628; color:#f1f5f9; font-family:sans-serif; margin:0; }}
  header {{ background:#0d2144; border-bottom:2px solid #f97316; padding:16px 24px; }}
  h1 {{ font-size:22px; margin:0; }} h1 span {{ color:#f97316; }}
  .sub {{ color:#94a3b8; font-size:13px; margin-top:4px; }}
  .grid {{ padding:20px 16px; max-width:800px; margin:0 auto; display:flex; flex-direction:column; gap:12px; }}
  .card {{ background:#0f1e35; border:1px solid #1e3a5f; border-radius:10px; padding:16px; text-decoration:none; display:block; transition:all 0.2s; }}
  .card:hover {{ border-color:#f97316; }}
  .titulo {{ font-size:16px; font-weight:700; color:#f1f5f9; margin-bottom:4px; }}
  .empresa {{ font-size:13px; color:#94a3b8; }}
  .footer {{ font-size:11px; color:#475569; margin-top:10px; padding-top:10px; border-top:1px solid #1e3a5f; }}
  .update {{ background:rgba(249,115,22,0.1); border:1px solid rgba(249,115,22,0.2); border-radius:8px; padding:10px 16px; font-size:12px; color:#94a3b8; margin-bottom:16px; }}
</style>
</head>
<body>
<header>
  <h1>Tec<span>System</span> Brasil</h1>
  <div class="sub">Vagas técnicas de manutenção · Atualizado: {agora}</div>
</header>
<div class="grid">
  <div class="update">🟢 {len(vagas)} vagas encontradas automaticamente</div>
  {cards if cards else '<p style="color:#94a3b8;text-align:center;padding:32px;">Nenhuma vaga encontrada hoje.</p>'}
</div>
</body>
</html>"""

def main():
    print("🤖 TecSystem Brasil - Buscando vagas...")
    vagas = []
    urls_vistas = set()
    for termo in TERMOS_BUSCA:
        print(f"🔍 {termo[:50]}...")
        for url in buscar_google(termo, 3):
            if url in urls_vistas:
                continue
            urls_vistas.add(url)
            vaga = extrair_vaga(url)
            if vaga:
                vagas.append(vaga)
                print(f"  ✅ {vaga['titulo'][:50]}")
            time.sleep(random.uniform(1.0, 2.0))
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(gerar_html(vagas))
    print(f"\n✅ Pronto! {len(vagas)} vagas · index.html gerado")

if __name__ == "__main__":
    main()
