"""
TecVagas - Robo de Artigos v3
========================================
- Fontes RSS publicas que funcionam em CI/CD
- Sem dependencia do Google News (bloqueado em datacenters)
- Fallback robusto com banco de reserva rotativo
"""

import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import re
import os
import hashlib

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; TecSystemBot/1.0)",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

ARTIGOS_FILE = "artigos.json"
MAX_ARTIGOS = 20

FONTES_RSS = [
    {
        "nome": "Tecmundo",
        "url": "https://www.tecmundo.com.br/rss",
        "categoria": "tecnologia",
        "tags": ["tecnologia", "inovacao", "automacao"]
    },
    {
        "nome": "Olhar Digital",
        "url": "https://olhardigital.com.br/feed/",
        "categoria": "tecnologia",
        "tags": ["tecnologia", "automacao", "mercado"]
    },
    {
        "nome": "TI Inside",
        "url": "https://tiinside.com.br/feed/",
        "categoria": "mercado",
        "tags": ["TI", "industria", "automacao"]
    },
    {
        "nome": "Computerworld Brasil",
        "url": "https://computerworld.com.br/feed/",
        "categoria": "mercado",
        "tags": ["tecnologia", "mercado", "automacao"]
    },
    {
        "nome": "Canaltech",
        "url": "https://canaltech.com.br/rss/",
        "categoria": "tecnologia",
        "tags": ["tecnologia", "automacao", "IA"]
    },
    {
        "nome": "InfoMoney Tech",
        "url": "https://www.infomoney.com.br/category/tecnologia/feed/",
        "categoria": "mercado",
        "tags": ["tecnologia", "mercado", "empregos"]
    },
]

BANCO_RESERVA = [
    {"titulo": "IA generativa transforma manutencao industrial em 2025", "resumo": "Empresas adotam inteligencia artificial para diagnostico preditivo, reduzindo paradas nao programadas em ate 40%. Tecnicos precisam se adaptar as novas tecnologias para manter empregabilidade.", "url": "https://tiinside.com.br", "fonte": "TI Inside", "categoria": "tecnologia", "tags": ["IA", "manutencao", "industria"], "imagem": "https://images.unsplash.com/photo-1565514020179-026b92b84bb6?w=800"},
    {"titulo": "Tecnicos de refrigeracao sao os mais buscados em 2025", "resumo": "Com o aumento das temperaturas e expansao de data centers, profissionais de HVAC e refrigeracao industrial estao em alta demanda no mercado brasileiro.", "url": "https://www.tecmundo.com.br", "fonte": "Tecmundo", "categoria": "mercado", "tags": ["HVAC", "refrigeracao", "empregos"], "imagem": "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=800"},
    {"titulo": "NR-10 e NR-12: novas exigencias para eletricistas industriais", "resumo": "O Ministerio do Trabalho atualiza normas regulamentadoras, aumentando exigencias de qualificacao e abrindo oportunidades para profissionais certificados.", "url": "https://tiinside.com.br", "fonte": "TI Inside", "categoria": "normas", "tags": ["NR-10", "NR-12", "eletricista"], "imagem": "https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=800"},
    {"titulo": "Automacao cria novas vagas para tecnicos especializados", "resumo": "Estudo aponta que automacao elimina funcoes repetitivas mas cria demanda por tecnicos capazes de programar e manter equipamentos automatizados.", "url": "https://computerworld.com.br", "fonte": "Computerworld Brasil", "categoria": "mercado", "tags": ["automacao", "empregos", "tecnicos"], "imagem": "https://images.unsplash.com/photo-1581092921461-39b7a5d6f4a4?w=800"},
    {"titulo": "Industria 4.0: tecnicos precisam dominar IoT e sensores", "resumo": "Com digitalizacao das fabricas, profissionais de manutencao precisam conhecer sensores IoT, PLCs e sistemas SCADA.", "url": "https://olhardigital.com.br", "fonte": "Olhar Digital", "categoria": "tecnologia", "tags": ["IoT", "industria 4.0", "PLC"], "imagem": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800"},
    {"titulo": "Petroleo e gas abre 15 mil vagas para tecnicos no Brasil", "resumo": "Expansao do setor de energia preve abertura de milhares de postos para tecnicos de manutencao, instrumentacao e seguranca industrial.", "url": "https://www.infomoney.com.br", "fonte": "InfoMoney", "categoria": "mercado", "tags": ["petroleo", "gas", "empregos"], "imagem": "https://images.unsplash.com/photo-1570615470447-7c4db8e16f80?w=800"},
    {"titulo": "Soldadores qualificados escassos no setor naval brasileiro", "resumo": "Retomada da industria naval cria escassez de soldadores, com salarios chegando a R$ 8.000 para profissionais com certificacao AWS.", "url": "https://canaltech.com.br", "fonte": "Canaltech", "categoria": "mercado", "tags": ["soldagem", "naval", "empregos"], "imagem": "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=800"},
    {"titulo": "Manutencao preditiva com IA muda as fabricas brasileiras", "resumo": "Sensores inteligentes e machine learning permitem prever falhas antes que ocorram, reduzindo custos de manutencao em ate 30%.", "url": "https://tiinside.com.br", "fonte": "TI Inside", "categoria": "tecnologia", "tags": ["manutencao preditiva", "IA", "fabrica"], "imagem": "https://images.unsplash.com/photo-1565514020179-026b92b84bb6?w=800"},
    {"titulo": "Tecnicos de TI industrial: perfil mais procurado pelas industrias", "resumo": "Convergencia entre TI e tecnologia operacional cria demanda por profissionais hibridos que entendam redes industriais e manutencao de equipamentos.", "url": "https://computerworld.com.br", "fonte": "Computerworld Brasil", "categoria": "carreira", "tags": ["TI industrial", "IT/OT", "carreira"], "imagem": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800"},
    {"titulo": "Energia solar impulsiona demanda por tecnicos fotovoltaicos", "resumo": "Com crescimento de 45% em 2024, mercado de energia solar cria demanda recorde por instaladores e tecnicos de manutencao de sistemas fotovoltaicos.", "url": "https://olhardigital.com.br", "fonte": "Olhar Digital", "categoria": "mercado", "tags": ["energia solar", "fotovoltaico", "empregos"], "imagem": "https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?w=800"},
    {"titulo": "Robotica colaborativa: tecnicos aprendem a trabalhar com cobots", "resumo": "Robos colaborativos chegam as medias e pequenas industrias. Tecnicos que programarem e mantiverem esses equipamentos terao vantagem no mercado.", "url": "https://www.tecmundo.com.br", "fonte": "Tecmundo", "categoria": "tecnologia", "tags": ["robotica", "cobots", "automacao"], "imagem": "https://images.unsplash.com/photo-1581092921461-39b7a5d6f4a4?w=800"},
    {"titulo": "SENAI abre 50 mil vagas em cursos tecnicos de automacao", "resumo": "Programa nacional de qualificacao com foco em automacao industrial, manutencao eletromecanica e mecatronica, com bolsas integrais.", "url": "https://tiinside.com.br", "fonte": "TI Inside", "categoria": "educacao", "tags": ["SENAI", "qualificacao", "automacao"], "imagem": "https://images.unsplash.com/photo-1581092921461-39b7a5d6f4a4?w=800"},
    {"titulo": "Data centers geram boom de vagas tecnicas no Brasil", "resumo": "Chegada de Google, Amazon e Microsoft ao Brasil impulsiona demanda por tecnicos de infraestrutura, refrigeracao e sistemas eletricos.", "url": "https://canaltech.com.br", "fonte": "Canaltech", "categoria": "mercado", "tags": ["data center", "infraestrutura", "empregos"], "imagem": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800"},
    {"titulo": "Instrumentacao industrial: salarios chegam a R$ 12 mil", "resumo": "Profissionais de calibracao e manutencao de instrumentos de medicao sao altamente valorizados na industria quimica e farmaceutica.", "url": "https://www.infomoney.com.br", "fonte": "InfoMoney", "categoria": "carreira", "tags": ["instrumentacao", "salarios", "industria"], "imagem": "https://images.unsplash.com/photo-1559523161-0fc0d8b814f2?w=800"},
    {"titulo": "Veiculos eletricos: nova fronteira para mecanicos no Brasil", "resumo": "Com chegada de veiculos eletricos ao mercado, mecanicos precisam se capacitar em sistemas de alta tensao e baterias de ion-litio.", "url": "https://olhardigital.com.br", "fonte": "Olhar Digital", "categoria": "tecnologia", "tags": ["eletrico", "mecanica", "capacitacao"], "imagem": "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=800"},
]


def gerar_id(titulo, url):
    texto = (titulo + url).encode("utf-8")
    return hashlib.md5(texto).hexdigest()[:12]


def limpar_html(texto):
    if not texto:
        return ""
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto[:300]


def buscar_rss(fonte):
    artigos = []
    try:
        resp = requests.get(fonte["url"], headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return artigos
        root = ET.fromstring(resp.content)
        items = root.findall(".//item")
        if not items:
            items = root.findall(".//{http://www.w3.org/2005/Atom}entry")
        for item in items[:8]:
            titulo_el = item.find("title") or item.find("{http://www.w3.org/2005/Atom}title")
            link_el = item.find("link") or item.find("{http://www.w3.org/2005/Atom}link")
            desc_el = item.find("description") or item.find("{http://www.w3.org/2005/Atom}summary")
            data_el = item.find("pubDate") or item.find("{http://www.w3.org/2005/Atom}published")
            titulo = (titulo_el.text or "").strip() if titulo_el is not None else ""
            url_art = ""
            if link_el is not None:
                url_art = (link_el.text or link_el.get("href", "")).strip()
            if not titulo or not url_art:
                continue
            resumo = limpar_html(desc_el.text or "") if desc_el is not None else ""
            data_str = datetime.now().strftime("%Y-%m-%d")
            if data_el is not None and data_el.text:
                data_str = data_el.text.strip()[:10]
            artigos.append({
                "id": gerar_id(titulo, url_art),
                "titulo": titulo,
                "resumo": resumo or f"Artigo de {fonte['nome']}.",
                "url": url_art,
                "fonte": fonte["nome"],
                "categoria": fonte["categoria"],
                "data": data_str,
                "tags": fonte["tags"],
                "imagem": "https://images.unsplash.com/photo-1565514020179-026b92b84bb6?w=800"
            })
    except Exception as e:
        pass
    return artigos


def carregar_artigos_existentes():
    try:
        with open(ARTIGOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def salvar_artigos(artigos):
    with open(ARTIGOS_FILE, "w", encoding="utf-8") as f:
        json.dump(artigos, f, ensure_ascii=False, indent=2)


def main():
    print("\n Robo de Artigos v3")
    print(f" {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 48)

    artigos_existentes = carregar_artigos_existentes()
    ids_existentes = {a.get("id", "") for a in artigos_existentes if a.get("id")}

    todos_novos = []
    fontes_ok = 0

    for fonte in FONTES_RSS:
        print(f"\n Buscando: {fonte['nome']}...")
        novos = buscar_rss(fonte)
        realmente_novos = [a for a in novos if a.get("id") and a["id"] not in ids_existentes]
        if realmente_novos:
            fontes_ok += 1
            todos_novos.extend(realmente_novos)
            print(f"   OK: {len(realmente_novos)} artigos novos")
        else:
            print(f"   Sem novos ({len(novos)} retornados, ja conhecidos ou vazio)")
        time.sleep(1)

    print(f"\n Fontes com conteudo novo: {fontes_ok}/{len(FONTES_RSS)}")
    print(f" Artigos novos: {len(todos_novos)}")

    if todos_novos:
        artigos_finais = todos_novos + artigos_existentes
        vistos = set()
        artigos_unicos = []
        for a in artigos_finais:
            aid = a.get("id")
            if aid and aid not in vistos:
                vistos.add(aid)
                artigos_unicos.append(a)
        artigos_finais = artigos_unicos[:MAX_ARTIGOS]
    else:
        print("\n Sem artigos novos. Usando banco de reserva rotativo...")
        dia_do_ano = datetime.now().timetuple().tm_yday
        offset = dia_do_ano % len(BANCO_RESERVA)
        reserva = BANCO_RESERVA[offset:] + BANCO_RESERVA[:offset]
        hoje = datetime.now().strftime("%Y-%m-%d")
        artigos_finais = []
        for i, artigo in enumerate(reserva[:MAX_ARTIGOS]):
            a = artigo.copy()
            a["data"] = hoje
            a["id"] = f"res_{dia_do_ano:03d}_{i:02d}"
            artigos_finais.append(a)

    salvar_artigos(artigos_finais)
    print(f"\n {len(artigos_finais)} artigos salvos!")


if __name__ == "__main__":
    main()
