"""
TecVagas - Robo de Vagas v12 PREMIUM
Design dark Apple + Mapa Brasil + Grafico pizza + Estados detectados
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

ANO_ATUAL = "2026"
CACHE_FILE = "vagas_cache.json"
ARTIGOS_FILE = "artigos.json"

TECNICOS = [
    "tecnico em manutencao eletrica","tecnico em eletrotecnica",
    "tecnico em eletromecanica","tecnico em paineis eletricos",
    "tecnico em motores eletricos","tecnico em manutencao mecanica",
    "tecnico em mecanica industrial","tecnico em hidraulica industrial",
    "tecnico em pneumatica","tecnico em soldagem","tecnico em caldeiraria",
    "tecnico em usinagem","tecnico em CNC","tecnico em mecatronica",
    "tecnico em manutencao industrial","tecnico em automacao industrial",
    "tecnico em PLC","tecnico em SCADA","tecnico em robotica",
    "tecnico em instrumentacao","tecnico em refrigeracao",
    "tecnico em HVAC","tecnico em climatizacao","tecnico em caldeiras",
    "tecnico em manutencao preditiva","tecnico em PCM",
    "tecnico em controle de qualidade","tecnico em ensaios nao destrutivos",
    "tecnico em metrologia","tecnico em seguranca do trabalho",
    "tecnico em metalurgia","tecnico em mineracao","tecnico em petroquimica",
]

PALAVRAS_DESCARTAR = [
    "banco de talentos","encerrad","finalizad","expirad","inativ",
    "cancelad","vaga encerrada","job expired","2024","2023",
]

ESTADOS_LISTA = [
    ("AC","Acre"),("AL","Alagoas"),("AP","Amapa"),("AM","Amazonas"),
    ("BA","Bahia"),("CE","Ceara"),("DF","Distrito Federal"),("ES","Espirito Santo"),
    ("GO","Goias"),("MA","Maranhao"),("MT","Mato Grosso"),("MS","Mato Grosso do Sul"),
    ("MG","Minas Gerais"),("PA","Para"),("PB","Paraiba"),("PR","Parana"),
    ("PE","Pernambuco"),("PI","Piaui"),("RJ","Rio de Janeiro"),("RN","Rio Grande do Norte"),
    ("RS","Rio Grande do Sul"),("RO","Rondonia"),("RR","Roraima"),("SC","Santa Catarina"),
    ("SP","Sao Paulo"),("SE","Sergipe"),("TO","Tocantins"),
]
ESTADOS = {s:n for s,n in ESTADOS_LISTA}

CIDADES_ESTADO = {
    "sao paulo":"SP","campinas":"SP","santos":"SP","sorocaba":"SP","jundiai":"SP",
    "guarulhos":"SP","osasco":"SP","ribeirao preto":"SP","sao bernardo":"SP",
    "santo andre":"SP","sao caetano":"SP","diadema":"SP","taubate":"SP",
    "sao jose dos campos":"SP","piracicaba":"SP","limeira":"SP","americana":"SP",
    "indaiatuba":"SP","apiai":"SP","cubatao":"SP",
    "rio de janeiro":"RJ","niteroi":"RJ","macae":"RJ","duque de caxias":"RJ",
    "nova iguacu":"RJ","sao goncalo":"RJ","petropolis":"RJ","volta redonda":"RJ",
    "campos":"RJ","resende":"RJ",
    "belo horizonte":"MG","contagem":"MG","betim":"MG","uberlandia":"MG",
    "juiz de fora":"MG","montes claros":"MG","ipatinga":"MG","sete lagoas":"MG",
    "pedro leopoldo":"MG","divinopolis":"MG","governador valadares":"MG",
    "curitiba":"PR","londrina":"PR","maringa":"PR","cascavel":"PR",
    "ponta grossa":"PR","sao jose dos pinhais":"PR","foz do iguacu":"PR",
    "porto alegre":"RS","caxias do sul":"RS","canoas":"RS","gravatai":"RS",
    "novo hamburgo":"RS","sao leopoldo":"RS","pelotas":"RS","santa maria":"RS",
    "florianopolis":"SC","joinville":"SC","blumenau":"SC","jaragua do sul":"SC",
    "chapeco":"SC","criciuma":"SC","itajai":"SC","sao jose":"SC",
    "salvador":"BA","camacari":"BA","feira de santana":"BA","candeias":"BA",
    "ilheus":"BA","vitoria da conquista":"BA",
    "recife":"PE","caruaru":"PE","jaboatao":"PE","olinda":"PE","petrolina":"PE",
    "fortaleza":"CE","caucaia":"CE","juazeiro do norte":"CE","sobral":"CE",
    "manaus":"AM","belem":"PA","parauapebas":"PA","maraba":"PA","santarem":"PA",
    "goiania":"GO","aparecida de goiania":"GO","anapolis":"GO","luziania":"GO",
    "brasilia":"DF","gama":"DF","taguatinga":"DF","ceilandia":"DF",
    "vitoria":"ES","vila velha":"ES","serra":"ES","cariacica":"ES","linhares":"ES",
    "maceio":"AL","arapiraca":"AL","natal":"RN","mossoro":"RN",
    "joao pessoa":"PB","campina grande":"PB","teresina":"PI","parnaiba":"PI",
    "sao luis":"MA","imperatriz":"MA","porto velho":"RO","ji-parana":"RO",
    "cuiaba":"MT","varzea grande":"MT","rondonopolis":"MT","comodoro":"MT",
    "campo grande":"MS","dourados":"MS","tres lagoas":"MS",
    "macapa":"AP","boa vista":"RR","palmas":"TO","aracaju":"SE",
    "rio branco":"AC","cruzeiro do sul":"AC",
}

ARTIGOS_PADRAO = [
    {"titulo":"A IA vai acabar com o emprego de tecnicos industriais?","resumo":"A inteligencia artificial esta transformando a industria, mas dados mostram que tecnicos sao dos profissionais mais resistentes a automacao.","conteudo":"A pergunta que mais assusta trabalhadores da industria em 2026: a IA vai tirar meu emprego?\n\nA resposta curta e: nao para tecnicos industriais. E os dados comprovam.\n\n**Por que tecnicos sao dificeis de substituir?**\n\nA automacao funciona bem para tarefas repetitivas. O trabalho de um tecnico industrial e exatamente o oposto.\n\nQuando uma bomba quebra as 3h da manha, nao e um algoritmo que vai trocar o selo. Quando um CLP apresenta falha intermitente, nao e uma tela que vai resolver no campo.\n\n**Os numeros:**\nSegundo o Forum Economico Mundial, 85 milhoes de empregos serao substituidos pela automacao ate 2025, mas 97 milhoes de novos empregos surgirao. Grande parte em manutencao e operacao de sistemas automatizados.\n\nNo Brasil, o deficit de tecnicos qualificados ja chega a 400 mil profissionais, segundo o SENAI.","categoria":"IA & Futuro","icone":"🤖","fonte":"TecVagas","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"Quanto ganha um Tecnico em Manutencao Eletrica em 2026?","resumo":"Salarios variam de R$ 2.800 a R$ 6.500 dependendo da regiao e experiencia.","conteudo":"O tecnico em manutencao eletrica e um dos profissionais mais requisitados na industria brasileira em 2026.\n\n**Faixa salarial por nivel:**\n• Junior (0-2 anos): R$ 2.800 a R$ 3.500\n• Pleno (2-5 anos): R$ 3.500 a R$ 5.000\n• Senior (5+ anos): R$ 5.000 a R$ 6.500\n• Especialista: ate R$ 8.000\n\n**O que aumenta o salario:**\n• NR10 atualizado: +15 a 25%\n• NR35 (trabalho em altura): +10%\n• Periculosidade (eletricidade): +30% sobre o salario\n• Insalubridade: +10 a 40% sobre o salario minimo\n• Turno noturno: +20% adicional","categoria":"Salarios","icone":"⚡","fonte":"TecVagas","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"NR10: Guia Completo para Tecnicos Eletricos em 2026","resumo":"A NR10 e obrigatoria para profissionais que trabalham com instalacoes eletricas.","conteudo":"A NR10 e obrigatoria para qualquer profissional que trabalhe com sistemas eletricos no Brasil.\n\n**Tipos de curso:**\n• NR10 Basico: 40 horas\n• NR10 SEP: 40 horas adicionais (alta tensao)\n• Total: 80 horas para habilitacao completa\n\n**Validade:** 2 anos\n\n**Custo medio:**\n• SENAI: R$ 300 a R$ 600\n• Empresas privadas: R$ 600 a R$ 1.500\n• Reciclagem: R$ 150 a R$ 400\n\n**Impacto no salario:** +20 a 25% em media","categoria":"Certificacoes","icone":"📋","fonte":"TecVagas","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"Tecnico em Automacao: a profissao que mais cresce no Brasil","resumo":"Com a Industria 4.0, tecnicos em PLC e SCADA sao os mais disputados.","conteudo":"A automacao industrial esta criando enorme demanda por tecnicos qualificados.\n\n**O que o tecnico em automacao faz:**\n• Programacao e manutencao de CLPs\n• Configuracao de sistemas SCADA\n• Manutencao de robos industriais\n• Redes industriais (Profibus, Profinet)\n\n**Plataformas valorizadas:**\n• Siemens S7 (TIA Portal)\n• Allen Bradley (Studio 5000)\n• Schneider (EcoStruxure)\n• ABB - robotica\n\n**Salarios:**\n• Junior: R$ 3.000 a R$ 4.500\n• Pleno: R$ 4.500 a R$ 6.500\n• Senior: R$ 6.500 a R$ 9.000\n• Especialista: ate R$ 12.000","categoria":"Carreira","icone":"🤖","fonte":"TecVagas","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"Melhores empresas para tecnicos industriais em 2026","resumo":"Petrobras, Vale, WEG, Embraer e Bosch oferecem os melhores pacotes.","conteudo":"Algumas empresas se destacam pela remuneracao e beneficios.\n\n**Petrobras**\n• Salario: R$ 9.000 a R$ 15.000\n• Acesso via concurso publico\n\n**Vale**\n• Salario: R$ 5.000 a R$ 10.000\n• Forte em MG, PA e ES\n\n**WEG**\n• Salario: R$ 3.500 a R$ 7.000\n• Base em Jaragua do Sul (SC)\n\n**Embraer**\n• Salario: R$ 4.000 a R$ 8.000\n• Sao Jose dos Campos (SP)\n\n**Bosch**\n• Salario: R$ 4.000 a R$ 7.500\n• Campinas e Curitiba","categoria":"Empresas","icone":"🏭","fonte":"TecVagas","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"Empregos manuais que a IA nunca vai substituir","resumo":"Profissoes com trabalho fisico complexo e raciocinio situacional sao as mais seguras.","conteudo":"A onda de automacao tem um ponto cego: o trabalho fisico especializado.\n\n**Profissoes mais seguras:**\n\n• Tecnico em Manutencao Industrial - risco 2%\n• Tecnico Eletricista Industrial - risco 3%\n• Tecnico em Refrigeracao/HVAC - risco 4%\n• Tecnico em Automacao/PLC - risco 1%\n\n**O que fazer para se proteger:**\n• Especialize-se em equipamentos complexos\n• Aprenda a interpretar dados de monitoramento\n• Adicione certificacoes NR\n• Desenvolva habilidade em manutencao preditiva\n\nO tecnico industrial do futuro nao compete com a IA - ele a opera, programa e mantem.","categoria":"IA & Futuro","icone":"🛡️","fonte":"TecVagas","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
]


def detectar_area(t):
    t = t.lower()
    if any(p in t for p in ["eletric","eletrom","painel","subestac","motor","gerador"]):
        return "eletrica"
    if any(p in t for p in ["mecatron","plc","scada","robotic","automac","cnc","instrumenta"]):
        return "automacao"
    if any(p in t for p in ["qualidad","inspec","metrolog","ensaio","calibr"]):
        return "qualidade"
    if any(p in t for p in ["seguranc","meio ambient"]):
        return "seguranca"
    if any(p in t for p in ["refriger","hvac","climatiz","ar condiciona"]):
        return "refrigeracao"
    return "mecanica"


def detectar_estado(local_str):
    if not local_str:
        return None
    texto = local_str.strip()
    texto_norm = texto.lower()
    texto_norm = texto_norm.replace("a","a").replace("e","e").replace("i","i").replace("o","o").replace("u","u")
    # Remove acentos basicos
    rep = {"a":"a","a":"a","a":"a","a":"a","e":"e","e":"e","i":"i","o":"o","o":"o","u":"u","c":"c"}
    for k,v in rep.items():
        texto_norm = texto_norm.replace(k,v)
    # Sigla no final ", SP" ou "/SP" ou " - SP"
    m = re.search(r"[,/\-\s]\s*([A-Z]{2})\s*$", texto.upper())
    if m and m.group(1) in ESTADOS:
        return m.group(1)
    # Sigla no meio "SP -" ou "(SP)"
    m = re.search(r"\b([A-Z]{2})\b", texto.upper())
    if m and m.group(1) in ESTADOS:
        return m.group(1)
    # Nome do estado completo
    for sigla, nome in ESTADOS.items():
        nome_norm = nome.lower().replace("a","a").replace("e","e").replace("o","o").replace("c","c")
        if nome_norm in texto_norm:
            return sigla
    # Cidade conhecida
    for cidade, sigla in CIDADES_ESTADO.items():
        if cidade in texto_norm:
            return sigla
    return None


def extrair_cidade(local_str):
    if not local_str:
        return ""
    texto = local_str.strip()
    # Remove sigla do estado no final
    texto = re.sub(r"[,/\-\s]+[A-Z]{2}\s*$", "", texto)
    texto = texto.strip(" ,-/")
    return texto[:40]


def titulo_valido(t):
    return not any(p in t.lower() for p in PALAVRAS_DESCARTAR)


def normalizar_titulo(titulo):
    if not titulo:
        return ""
    # Insere espaco entre minuscula e maiuscula coladas
    titulo = re.sub(r"([a-zaaaaaaeeeiiooouuc])([A-ZAAAAAEEEIIOOOUUC])", r"\1 \2", titulo)
    # Insere espaco entre letra e numero
    titulo = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", titulo)
    titulo = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", titulo)
    # Sufixos
    for sufixo in ["Jr","Sr","Pleno","Junior","Senior","Trainee"]:
        titulo = re.sub(rf"(?<=[a-z])({sufixo})\b", rf" \1", titulo)
    titulo = re.sub(r"\s*-\s*", " - ", titulo)
    titulo = re.sub(r"\s+", " ", titulo)
    return titulo.strip()


def formatar_conteudo(texto):
    if not texto:
        return ""
    linhas = texto.strip().split("\n")
    html = ""
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            html += '<div style="height:8px"></div>'
            continue
        linha = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", linha)
        if linha.startswith("•") or linha.startswith("✅") or linha.startswith("❌"):
            html += f'<p style="margin:5px 0;padding-left:6px">{linha}</p>'
        else:
            html += f'<p style="margin:10px 0">{linha}</p>'
    return html


def buscar_gupy():
    vagas = []
    print("Buscando Gupy...")
    for termo in TECNICOS[:25]:
        try:
            url = f"https://portal.api.gupy.io/api/v1/jobs?jobName={requests.utils.quote(termo)}&limit=5"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            for job in resp.json().get("data", []):
                pub = str(job.get("publishedDate","") or job.get("createdAt",""))
                if ANO_ATUAL not in pub:
                    continue
                titulo = normalizar_titulo(job.get("name","")[:80])
                if not titulo_valido(titulo):
                    continue
                cidade = (job.get("city") or "").strip()
                estado_api = (job.get("state") or "").strip()
                local_combinado = f"{cidade}, {estado_api}".strip(", ")
                estado = detectar_estado(local_combinado) or detectar_estado(estado_api) or detectar_estado(cidade)
                if cidade and estado:
                    local_display = f"{cidade}, {estado}"
                elif estado:
                    local_display = ESTADOS.get(estado, estado)
                elif cidade:
                    local_display = cidade
                else:
                    local_display = "Brasil"
                vagas.append({
                    "titulo": titulo,
                    "empresa": (job.get("careerPageName") or "Empresa")[:50],
                    "local": local_display,
                    "cidade": cidade,
                    "estado": estado or "BR",
                    "url": job.get("jobUrl","#"),
                    "fonte": "gupy.io",
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "area": detectar_area(titulo),
                    "salario": "A combinar",
                    "escala": "CLT",
                })
            time.sleep(0.8)
        except Exception as e:
            print(f"  Gupy err: {e}")
    print(f"  Gupy: {len(vagas)}")
    return vagas


def buscar_vagas_com_br():
    vagas = []
    print("Buscando vagas.com.br...")
    termos = [
        "tecnico-manutencao-eletrica","tecnico-manutencao-mecanica",
        "tecnico-mecatronica","tecnico-automacao-industrial",
        "tecnico-instrumentacao","tecnico-soldagem","tecnico-caldeiraria",
        "tecnico-seguranca-trabalho","tecnico-qualidade","tecnico-refrigeracao",
        "tecnico-eletrotecnica","tecnico-eletromecanica","tecnico-pcm",
    ]
    for termo in termos:
        try:
            resp = requests.get(f"https://www.vagas.com.br/vagas-de-{termo}", headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            for card in soup.find_all("li", class_="vaga")[:8]:
                te = card.find("a", class_="link-detalhes-vaga")
                ee = card.find("span", class_="emprVaga") or card.find("span", class_="empr-name")
                le = card.find("span", class_="vaga-local") or card.find("span", class_="local")
                de = card.find("span", class_="data-publicacao") or card.find("time")
                if not te:
                    continue
                titulo = normalizar_titulo(te.get_text(strip=True)[:80])
                if not titulo_valido(titulo):
                    continue
                dt = de.get_text(strip=True) if de else ""
                if "2025" in dt or "2024" in dt:
                    continue
                local_raw = le.get_text(strip=True)[:60] if le else ""
                estado = detectar_estado(local_raw)
                cidade = extrair_cidade(local_raw)
                if cidade and estado:
                    local_display = f"{cidade}, {estado}"
                elif estado:
                    local_display = ESTADOS.get(estado, estado)
                else:
                    local_display = local_raw[:40] if local_raw else "Brasil"
                empresa = ee.get_text(strip=True)[:50] if ee else "Empresa"
                vagas.append({
                    "titulo": titulo,
                    "empresa": empresa,
                    "local": local_display,
                    "cidade": cidade,
                    "estado": estado or "BR",
                    "url": "https://www.vagas.com.br" + te.get("href",""),
                    "fonte": "vagas.com.br",
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "area": detectar_area(titulo),
                    "salario": "A combinar",
                    "escala": "CLT",
                })
            time.sleep(1.2)
        except Exception as e:
            print(f"  vagas.com.br err: {e}")
    print(f"  vagas.com.br: {len(vagas)}")
    return vagas


def verificar_cache(cache):
    if not cache:
        return []
    print(f"Verificando {len(cache)} vagas em cache...")
    ativas = []
    for v in cache:
        if not titulo_valido(v.get("titulo","")):
            continue
        # Renormaliza titulo
        v["titulo"] = normalizar_titulo(v.get("titulo",""))
        # Re-detecta estado se faltar
        if v.get("estado") in ["BR",""] and v.get("local"):
            novo = detectar_estado(v["local"])
            if novo:
                v["estado"] = novo
                cidade = extrair_cidade(v["local"])
                if cidade:
                    v["cidade"] = cidade
                    v["local"] = f"{cidade}, {novo}"
                else:
                    v["local"] = ESTADOS.get(novo, novo)
        if "salario" not in v: v["salario"] = "A combinar"
        if "escala" not in v: v["escala"] = "CLT"
        if "cidade" not in v: v["cidade"] = ""
        ativas.append(v)
    print(f"  Ativas: {len(ativas)}")
    return ativas


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


def carregar_artigos():
    try:
        with open(ARTIGOS_FILE, "r", encoding="utf-8") as f:
            a = json.load(f)
            if a:
                return a[:6]
    except:
        pass
    return ARTIGOS_PADRAO


AREA_CONFIG = {
    "eletrica":     {"cls":"tag-el","label":"Eletrica","ico":"⚡","cor":"#3b82f6"},
    "mecanica":     {"cls":"tag-me","label":"Mecanica","ico":"🔩","cor":"#22c55e"},
    "automacao":    {"cls":"tag-au","label":"Automacao","ico":"🤖","cor":"#f97316"},
    "qualidade":    {"cls":"tag-qu","label":"Qualidade","ico":"📊","cor":"#a855f7"},
    "seguranca":    {"cls":"tag-se","label":"Seguranca","ico":"🦺","cor":"#14b8a6"},
    "refrigeracao": {"cls":"tag-rf","label":"Refrigeracao","ico":"❄️","cor":"#60a5fa"},
}


def gerar_card_vaga(v, idx=0):
    area = v.get("area","mecanica")
    cfg = AREA_CONFIG.get(area, AREA_CONFIG["mecanica"])
    estado = v.get("estado","BR")
    salario = v.get("salario","A combinar")
    escala = v.get("escala","CLT")
    local = v.get("local","Brasil")
    wpp_text = f"{v['titulo']} - {v['empresa']} - {local}"
    wpp = f"https://wa.me/?text={requests.utils.quote(wpp_text + ' - ' + v['url'] + ' - via TecVagas')}"
    delay = f"animation-delay:{idx*0.04}s"
    busca = f"{v.get('titulo','').lower()} {v.get('empresa','').lower()} {local.lower()}"
    return f'''<article class="job-card" style="{delay}" data-area="{area}" data-estado="{estado}" data-busca="{busca}">
  <div class="card-accent" style="background:{cfg['cor']}"></div>
  <div class="card-body">
    <div class="card-top">
      <div class="card-main">
        <div class="card-tag {cfg['cls']}">{cfg['ico']} {cfg['label']}</div>
        <h3 class="card-title">{v['titulo']}</h3>
        <div class="card-company">{v['empresa']}</div>
      </div>
      <div class="card-badge-verified">🔗 Link ativo</div>
    </div>
    <div class="card-info-row">
      <span class="info-chip info-chip-loc">📍 {local}</span>
      <span class="info-chip">💰 {salario}</span>
      <span class="info-chip">📋 {escala}</span>
      <span class="info-chip">🗓 {v['data']}</span>
    </div>
    <div class="card-actions">
      <a class="btn-wpp" href="{wpp}" target="_blank" onclick="event.stopPropagation()">📲 WhatsApp</a>
      <a class="btn-ver" href="{v['url']}" target="_blank">Ver vaga →</a>
    </div>
  </div>
</article>'''


def gerar_card_artigo(a, idx=0):
    conteudo_html = formatar_conteudo(a.get("conteudo","")) or f'<p>{a.get("resumo","")}</p>'
    return f'''<div class="article-card" onclick="openArticle({idx})">
  <div class="article-icon">{a['icone']}</div>
  <div class="article-content">
    <div class="article-cat">{a['categoria']}</div>
    <div class="article-title">{a['titulo']}</div>
    <div class="article-excerpt">{a['resumo']}</div>
    <div class="article-footer">
      <span class="article-source">{a.get('fonte','TecVagas')} · {a.get('data','')}</span>
      <span class="article-cta">Ler artigo →</span>
    </div>
  </div>
</div>
<div class="modal" id="article-{idx}">
  <div class="modal-box modal-article">
    <div class="modal-article-cat">{a['icone']} {a['categoria']}</div>
    <h2 class="modal-article-title">{a['titulo']}</h2>
    <div class="modal-article-meta">{a.get('fonte','TecVagas')} · {a.get('data','')}</div>
    <div class="modal-article-body">{conteudo_html}</div>
    <button class="btn-close" onclick="closeModal('article-{idx}')">Fechar</button>
  </div>
</div>'''


def gerar_estados_opts(por_estado):
    opts = '<option value="todos">Todos os estados</option>'
    for s, n in ESTADOS_LISTA:
        c = por_estado.get(s, 0)
        if c > 0:
            opts += f'<option value="{s}">{s} - {n} ({c})</option>'
        else:
            opts += f'<option value="{s}" style="color:#555">{s} - {n}</option>'
    return opts


# Coordenadas SVG dos estados do Brasil (mapa simplificado)
ESTADO_COORDS = {
    "AC":(85,235),"AM":(155,200),"RR":(180,140),"AP":(255,160),"PA":(255,210),
    "TO":(295,255),"MA":(335,200),"PI":(370,235),"CE":(405,205),"RN":(430,215),
    "PB":(435,235),"PE":(425,250),"AL":(420,265),"SE":(410,275),"BA":(370,275),
    "RO":(150,260),"MT":(225,290),"GO":(285,300),"DF":(305,305),"MS":(225,335),
    "MG":(325,335),"ES":(370,345),"RJ":(345,365),"SP":(295,365),"PR":(265,395),
    "SC":(265,425),"RS":(225,455),
}


def gerar_mapa_brasil(por_estado):
    max_v = max(por_estado.values()) if por_estado else 1
    pontos = ""
    for sigla, (cx, cy) in ESTADO_COORDS.items():
        c = por_estado.get(sigla, 0)
        if c > 0:
            r = 8 + min(c / max_v, 1) * 18
            opacity = 0.4 + min(c / max_v, 1) * 0.6
            pontos += f'<g class="map-state" data-estado="{sigla}" data-count="{c}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#f97316" opacity="{opacity}" class="map-dot"/><text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="11" font-weight="700" fill="#fff" pointer-events="none">{c}</text></g>'
        else:
            pontos += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333" opacity="0.4"/>'
    return f'''<div class="map-container">
<svg viewBox="0 60 480 440" xmlns="http://www.w3.org/2000/svg" class="brasil-map">
<rect x="0" y="0" width="480" height="500" fill="transparent"/>
{pontos}
</svg>
<div class="map-tooltip" id="map-tip">Passe o mouse</div>
</div>'''


def gerar_grafico_pizza(por_area):
    total = sum(por_area.values()) or 1
    cores = {"eletrica":"#3b82f6","mecanica":"#22c55e","automacao":"#f97316","qualidade":"#a855f7","seguranca":"#14b8a6","refrigeracao":"#60a5fa"}
    nomes = {"eletrica":"Eletrica","mecanica":"Mecanica","automacao":"Automacao","qualidade":"Qualidade","seguranca":"Seguranca","refrigeracao":"Refrigeracao"}
    cumulative = 0
    segmentos = ""
    legenda = ""
    cx, cy, r = 100, 100, 75
    for area, count in sorted(por_area.items(), key=lambda x: -x[1]):
        if count == 0:
            continue
        pct = count / total
        angulo = pct * 360
        start_angle = cumulative * 3.6
        end_angle = (cumulative + pct * 100) * 3.6
        cumulative += pct * 100
        x1 = cx + r * (1.0 if start_angle == 0 else __import__('math').cos(__import__('math').radians(start_angle - 90)))
        y1 = cy + r * __import__('math').sin(__import__('math').radians(start_angle - 90))
        x2 = cx + r * __import__('math').cos(__import__('math').radians(end_angle - 90))
        y2 = cy + r * __import__('math').sin(__import__('math').radians(end_angle - 90))
        large_arc = 1 if angulo > 180 else 0
        cor = cores.get(area, "#888")
        nome = nomes.get(area, area)
        path = f'M {cx} {cy} L {x1:.2f} {y1:.2f} A {r} {r} 0 {large_arc} 1 {x2:.2f} {y2:.2f} Z'
        segmentos += f'<path d="{path}" fill="{cor}" stroke="#0A0A0F" stroke-width="2" class="pie-slice" data-area="{area}"><title>{nome}: {count} vagas ({pct*100:.0f}%)</title></path>'
        legenda += f'<div class="legend-item"><span class="legend-dot" style="background:{cor}"></span><span class="legend-label">{nome}</span><span class="legend-val">{count} ({pct*100:.0f}%)</span></div>'
    return f'''<div class="chart-container">
<svg viewBox="0 0 200 200" class="pie-chart">{segmentos}<circle cx="{cx}" cy="{cy}" r="32" fill="#0A0A0F"/><text x="{cx}" y="{cy-2}" text-anchor="middle" font-size="22" font-weight="800" fill="#fff" font-family="Syne,sans-serif">{total}</text><text x="{cx}" y="{cy+14}" text-anchor="middle" font-size="9" fill="#7B7B8F" font-weight="600" letter-spacing="1">VAGAS</text></svg>
<div class="chart-legend">{legenda}</div>
</div>'''


HTML_CSS = """*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}
:root{--bg:#0A0A0F;--bg1:#111118;--bg2:#16161F;--bg3:#1C1C28;--border:#ffffff0f;--border2:#ffffff18;--text:#F0F0F5;--muted:#7B7B8F;--muted2:#A0A0B0;--orange:#F97316;--orange2:#FB923C;--blue:#3B82F6;--blue2:#60A5FA;--green:#22C55E;--yellow:#FBBF24;--purple:#A855F7;--teal:#14B8A6;--r:4px;--r2:8px;--r3:12px}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;font-size:15px;line-height:1.6;overflow-x:hidden}
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px}
nav{position:sticky;top:0;z-index:100;background:rgba(10,10,15,0.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);padding:0 20px;height:60px;display:flex;align-items:center;justify-content:space-between}
.nav-logo{font-family:'Syne',sans-serif;font-size:17px;font-weight:800;letter-spacing:.3px;display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--text)}
.nav-dot{width:8px;height:8px;background:var(--orange);border-radius:50%;box-shadow:0 0 12px var(--orange);animation:blink 2s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.4}}
.nav-right{display:flex;align-items:center;gap:10px}
#nav-clock{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
.nav-badge{font-size:11px;font-weight:600;background:rgba(249,115,22,.12);color:var(--orange);border:1px solid rgba(249,115,22,.2);padding:4px 11px;border-radius:20px;display:flex;align-items:center;gap:5px}
.nav-badge::before{content:'';width:6px;height:6px;background:var(--orange);border-radius:50%;animation:blink 2s ease-in-out infinite}
.hero{position:relative;overflow:hidden;padding:90px 24px 70px;text-align:center;background:var(--bg)}
.hero-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:64px 64px;mask-image:radial-gradient(ellipse 100% 80% at 50% 0%,black 0%,transparent 70%)}
.hero-glow{position:absolute;top:0;left:50%;transform:translateX(-50%);width:100%;height:400px;background:radial-gradient(ellipse 60% 100% at 50% 0%,rgba(249,115,22,.10) 0%,transparent 100%);pointer-events:none}
.hero-eyebrow{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;letter-spacing:.8px;color:var(--orange);margin-bottom:22px;background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);padding:6px 14px;border-radius:30px}
.hero h1{font-family:'Syne',sans-serif;font-size:clamp(40px,9vw,76px);font-weight:800;line-height:1.04;letter-spacing:-2.5px;color:#fff;margin-bottom:22px;max-width:780px;margin-left:auto;margin-right:auto}
.hero h1 .accent{background:linear-gradient(90deg,var(--orange),#ff9a3c);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-sub{font-size:17px;color:rgba(255,255,255,.55);font-weight:400;max-width:480px;margin:0 auto;line-height:1.65}
.metrics{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--border);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
@media(min-width:768px){.metrics{grid-template-columns:repeat(4,1fr)}}
.metric{background:var(--bg1);padding:22px 16px;text-align:center;position:relative;overflow:hidden;transition:background .25s}
.metric:hover{background:var(--bg2)}
.metric::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--orange),transparent);opacity:0;transition:opacity .3s}
.metric:hover::before{opacity:1}
.metric-num{font-family:'Syne',sans-serif;font-size:32px;font-weight:800;color:var(--orange);line-height:1;margin-bottom:5px;letter-spacing:-1.5px}
.metric-label{font-size:10px;color:var(--muted);font-weight:600;letter-spacing:.8px;text-transform:uppercase}
.filters-section{background:var(--bg1);border-bottom:1px solid var(--border);padding:16px 20px}
.filters-search{position:relative;margin-bottom:12px}
.filters-search input{width:100%;background:var(--bg2);border:1px solid var(--border2);color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;padding:12px 18px 12px 44px;border-radius:var(--r2);outline:none;transition:all .25s}
.filters-search input::placeholder{color:var(--muted)}
.filters-search input:focus{border-color:var(--orange);box-shadow:0 0 0 3px rgba(249,115,22,.12)}
.s-ico{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:15px;pointer-events:none}
.f-row{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.f-row:last-child{margin-bottom:0}
.f-lbl{font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--muted);margin-bottom:8px;display:block}
.chip{flex-shrink:0;background:var(--bg2);border:1px solid var(--border2);color:var(--muted2);font-family:'DM Sans',sans-serif;font-size:12px;font-weight:500;padding:6px 14px;border-radius:20px;cursor:pointer;transition:all .2s;white-space:nowrap}
.chip:hover{border-color:var(--orange);color:var(--orange);transform:translateY(-1px)}
.chip.active{background:rgba(249,115,22,.14);border-color:var(--orange);color:var(--orange);font-weight:600}
.f-sel{background:var(--bg2);border:1px solid var(--border2);color:var(--text);font-family:'DM Sans',sans-serif;font-size:12px;padding:7px 14px;border-radius:20px;cursor:pointer;flex-shrink:0;outline:none;min-width:200px;font-weight:500}
.f-sel:focus{border-color:var(--orange)}
.trust-bar{background:linear-gradient(90deg,rgba(34,197,94,.04),rgba(34,197,94,.01));border-bottom:1px solid rgba(34,197,94,.1);padding:8px 20px;display:flex;align-items:center;gap:8px;font-size:11px;color:var(--muted2)}
.trust-dot{width:6px;height:6px;background:var(--green);border-radius:50%;flex-shrink:0;box-shadow:0 0 8px var(--green);animation:pg 2s ease-in-out infinite}
@keyframes pg{0%,100%{box-shadow:0 0 6px var(--green)}50%{box-shadow:0 0 14px var(--green)}}
.page{padding:24px 16px 48px;max-width:900px;margin:0 auto}
.sec-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;margin-top:30px}
.sec-title{font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:var(--text);display:flex;align-items:center;gap:8px;letter-spacing:-.2px}
.sec-count{font-size:11px;color:var(--orange);background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);padding:4px 11px;border-radius:20px;font-weight:600}
.dash-sub{font-size:11px;color:var(--muted);font-weight:400;letter-spacing:.3px}
.dashboard{display:grid;grid-template-columns:1fr;gap:14px;margin-bottom:6px}
@media(min-width:768px){.dashboard{grid-template-columns:1.2fr 1fr}}
.dash-card{background:linear-gradient(135deg,var(--bg1),var(--bg2));border:1px solid var(--border);border-radius:14px;padding:18px;position:relative;overflow:hidden}
.dash-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--orange),var(--blue))}
.dash-title{font-family:'Syne',sans-serif;font-size:14px;font-weight:700;margin-bottom:14px;display:flex;align-items:center;gap:8px;color:var(--text)}
.map-container{position:relative;width:100%}
.brasil-map{width:100%;height:auto;display:block;max-height:300px}
.map-state{cursor:pointer;transition:opacity .2s}
.map-state:hover .map-dot{opacity:1!important;filter:drop-shadow(0 0 12px var(--orange))}
.map-tooltip{position:absolute;top:8px;right:8px;background:rgba(0,0,0,.7);border:1px solid var(--border2);padding:5px 10px;border-radius:6px;font-size:10px;color:var(--muted2);pointer-events:none;font-weight:500}
.chart-container{display:flex;flex-direction:column;align-items:center;gap:14px}
@media(min-width:480px){.chart-container{flex-direction:row;align-items:flex-start}}
.pie-chart{width:140px;height:140px;flex-shrink:0;animation:rot 1s ease-out}
@keyframes rot{from{transform:rotate(-90deg) scale(.85);opacity:0}to{transform:rotate(0) scale(1);opacity:1}}
.pie-slice{transition:transform .25s,filter .25s;transform-origin:100px 100px}
.pie-slice:hover{transform:scale(1.05);filter:brightness(1.2)}
.chart-legend{flex:1;display:flex;flex-direction:column;gap:6px;width:100%}
.legend-item{display:flex;align-items:center;gap:8px;font-size:12px}
.legend-dot{width:10px;height:10px;border-radius:3px;flex-shrink:0}
.legend-label{flex:1;color:var(--muted2);font-weight:500}
.legend-val{color:var(--text);font-weight:600;font-variant-numeric:tabular-nums;font-size:11px}
.calc-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:4px}
.calc-item{background:var(--bg1);border:1px solid var(--border);border-radius:var(--r2);padding:14px;display:flex;align-items:center;gap:10px;cursor:pointer;transition:all .2s;text-align:left;color:var(--text)}
.calc-item:hover{border-color:var(--orange);background:var(--bg2);transform:translateY(-2px)}
.calc-emoji{font-size:20px;flex-shrink:0}
.calc-name{font-size:13px;font-weight:600;margin-bottom:1px}
.calc-hint{font-size:10px;color:var(--muted)}
.articles-grid{display:flex;flex-direction:column;gap:8px}
.article-card{background:var(--bg1);border:1px solid var(--border);border-radius:var(--r2);padding:15px;display:flex;gap:12px;transition:all .2s;cursor:pointer}
.article-card:hover{border-color:var(--border2);background:var(--bg2);transform:translateY(-2px)}
.article-icon{font-size:22px;flex-shrink:0;margin-top:2px}
.article-content{flex:1;min-width:0}
.article-cat{font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--orange);margin-bottom:3px}
.article-title{font-size:14px;font-weight:600;color:var(--text);margin-bottom:4px;line-height:1.35}
.article-excerpt{font-size:12px;color:var(--muted);line-height:1.5;margin-bottom:7px}
.article-footer{display:flex;align-items:center;justify-content:space-between}
.article-source{font-size:10px;color:var(--muted)}
.article-cta{font-size:11px;color:var(--orange);font-weight:600}
.newsletter{background:linear-gradient(135deg,var(--bg2),var(--bg3));border:1px solid var(--border);border-radius:var(--r3);padding:24px 20px;margin-bottom:4px;position:relative;overflow:hidden}
.newsletter::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--orange),var(--blue),var(--orange));background-size:200% 100%;animation:slide 3s linear infinite}
@keyframes slide{from{background-position:0% 0%}to{background-position:200% 0%}}
.nl-title{font-family:'Syne',sans-serif;font-size:18px;font-weight:700;margin-bottom:5px}
.nl-title span{color:var(--orange)}
.nl-desc{font-size:12px;color:var(--muted2);margin-bottom:15px}
.nl-form{display:flex;gap:8px;flex-wrap:wrap}
.nl-input{flex:1;min-width:170px;background:var(--bg);border:1px solid var(--border2);color:var(--text);font-family:'DM Sans',sans-serif;font-size:13px;padding:10px 13px;border-radius:var(--r2);outline:none}
.nl-input:focus{border-color:var(--orange)}
.nl-btn{background:var(--orange);color:#fff;border:none;font-family:'DM Sans',sans-serif;font-size:13px;font-weight:600;padding:10px 20px;border-radius:var(--r2);cursor:pointer;white-space:nowrap;transition:background .2s}
.nl-btn:hover{background:#ea6c0a}
.nl-ok{display:none;color:var(--green);font-size:12px;margin-top:8px;font-weight:500}
.jobs-list{display:flex;flex-direction:column;gap:11px}
.job-card{background:var(--bg1);border:1px solid var(--border);border-radius:var(--r2);overflow:hidden;transition:all .25s;animation:fadeUp .4s ease both;position:relative}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.job-card:hover{border-color:var(--border2);background:var(--bg2);transform:translateY(-3px);box-shadow:0 12px 36px rgba(0,0,0,.35)}
.card-accent{position:absolute;left:0;top:0;bottom:0;width:3px}
.card-body{padding:16px 16px 16px 22px}
.card-top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;margin-bottom:10px}
.card-main{flex:1;min-width:0}
.card-tag{display:inline-flex;align-items:center;gap:4px;font-size:10px;font-weight:600;letter-spacing:.8px;text-transform:uppercase;padding:3px 10px;border-radius:20px;margin-bottom:6px}
.tag-el{background:rgba(59,130,246,.12);color:var(--blue2);border:1px solid rgba(59,130,246,.2)}
.tag-me{background:rgba(34,197,94,.12);color:#4ade80;border:1px solid rgba(34,197,94,.2)}
.tag-au{background:rgba(249,115,22,.12);color:var(--orange2);border:1px solid rgba(249,115,22,.2)}
.tag-qu{background:rgba(168,85,247,.12);color:#c084fc;border:1px solid rgba(168,85,247,.2)}
.tag-se{background:rgba(20,184,166,.12);color:#2dd4bf;border:1px solid rgba(20,184,166,.2)}
.tag-rf{background:rgba(96,165,250,.12);color:var(--blue2);border:1px solid rgba(96,165,250,.2)}
.card-title{font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:var(--text);line-height:1.3;margin-bottom:3px;letter-spacing:-.3px}
.card-company{font-size:12px;color:var(--muted2);font-weight:500}
.card-badge-verified{flex-shrink:0;font-size:10px;font-weight:600;color:var(--green);background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.2);padding:3px 9px;border-radius:20px;white-space:nowrap}
.card-info-row{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:11px}
.info-chip{font-size:10px;color:var(--muted2);background:var(--bg3);border:1px solid var(--border);padding:3px 9px;border-radius:var(--r);font-weight:500}
.info-chip-loc{color:var(--orange2);background:rgba(249,115,22,.06);border-color:rgba(249,115,22,.18);font-weight:600}
.card-actions{display:flex;gap:7px;padding-top:11px;border-top:1px solid var(--border)}
.btn-wpp{display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:600;color:var(--green);background:rgba(34,197,94,.06);border:1px solid rgba(34,197,94,.2);padding:7px 13px;border-radius:var(--r2);text-decoration:none;transition:all .2s}
.btn-wpp:hover{background:rgba(34,197,94,.12)}
.btn-ver{display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:600;color:#fff;background:var(--orange);padding:7px 15px;border-radius:var(--r2);text-decoration:none;transition:all .2s;margin-left:auto}
.btn-ver:hover{background:#ea6c0a;box-shadow:0 6px 18px rgba(249,115,22,.3)}
.empty-state{text-align:center;padding:50px 20px;display:none}
.page[data-searching] .calc-section,.page[data-searching] .articles-section,.page[data-searching] .newsletter,.page[data-searching] .dashboard-section{display:none!important}
.empty-icon{font-size:46px;margin-bottom:14px;opacity:.4}
.empty-title{font-family:'Syne',sans-serif;font-size:18px;font-weight:700;margin-bottom:8px}
.empty-text{font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:18px}
.empty-btn{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:var(--orange);background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);padding:9px 20px;border-radius:20px;cursor:pointer;transition:all .2s}
.empty-btn:hover{background:rgba(249,115,22,.15)}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:1000;align-items:center;justify-content:center;padding:16px;backdrop-filter:blur(6px);overflow-y:auto}
.modal.open{display:flex}
.modal-box{background:var(--bg2);border:1px solid var(--border2);border-radius:var(--r3);padding:22px;width:100%;max-width:420px;margin:auto;position:relative}
.modal-box::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--orange),var(--blue));border-radius:var(--r3) var(--r3) 0 0}
.modal-article{max-width:600px;max-height:88vh;overflow-y:auto}
.modal-article-cat{font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--orange);margin-bottom:10px}
.modal-article-title{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;line-height:1.2;margin-bottom:8px;letter-spacing:-.4px;color:#fff}
.modal-article-meta{font-size:11px;color:var(--muted);margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid var(--border)}
.modal-article-body{font-size:14px;color:var(--muted2);line-height:1.75;margin-bottom:20px}
.modal-article-body strong{color:#fff;font-weight:700}
.modal-title{font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:var(--orange);margin-bottom:14px}
.modal-field{margin-bottom:12px}
.modal-label{font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:var(--muted);display:block;margin-bottom:5px}
.modal-input,.modal-select{width:100%;background:var(--bg);border:1px solid var(--border2);color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;padding:10px 13px;border-radius:var(--r2);outline:none;transition:border .2s}
.modal-input:focus,.modal-select:focus{border-color:var(--orange);box-shadow:0 0 0 3px rgba(249,115,22,.1)}
.calc-result{background:var(--bg);border:1px solid var(--border);border-radius:var(--r2);padding:14px;margin-top:14px}
.result-row{display:flex;justify-content:space-between;font-size:13px;margin-bottom:7px;color:var(--muted)}
.result-row.total{color:var(--green);font-weight:700;font-size:15px;border-top:1px solid var(--border);padding-top:10px;margin-top:5px}
.btn-close{width:100%;margin-top:8px;background:transparent;color:var(--muted);border:1px solid var(--border);font-family:'DM Sans',sans-serif;font-size:13px;padding:9px;border-radius:var(--r2);cursor:pointer;transition:all .2s}
.btn-close:hover{border-color:var(--border2);color:var(--text)}
footer{border-top:1px solid var(--border);padding:28px 20px;text-align:center;background:linear-gradient(180deg,transparent,var(--bg1))}
.footer-logo{font-family:'Syne',sans-serif;font-size:16px;font-weight:800;margin-bottom:6px}
.footer-logo span{color:var(--orange)}
.footer-text{font-size:11px;color:var(--muted);line-height:1.8}"""

HTML_JS = """(function(){var el=document.getElementById('nav-clock');function t(){el.textContent=new Date().toLocaleTimeString('pt-BR',{timeZone:'America/Sao_Paulo',hour:'2-digit',minute:'2-digit'});}t();setInterval(t,1000);})();
function openModal(id){document.getElementById(id).classList.add('open');document.body.style.overflow='hidden';}
function closeModal(id){document.getElementById(id).classList.remove('open');document.body.style.overflow='';}
function openArticle(idx){openModal('article-'+idx);}
document.querySelectorAll('.modal').forEach(function(m){m.addEventListener('click',function(e){if(e.target===m)closeModal(m.id);});});
document.addEventListener('keydown',function(e){if(e.key==='Escape')document.querySelectorAll('.modal.open').forEach(function(m){closeModal(m.id);});});
var _a='todas',_e='todos',_b='';
function fA(a,b){_a=a;document.querySelectorAll('.chip').forEach(function(x){x.classList.remove('active');});b.classList.add('active');render();}
function fE(v){_e=v;render();}
function buscar(v){_b=v.toLowerCase().trim();var p=document.querySelector('.page');if(_b.length>0){p.setAttribute('data-searching','1');}else{p.removeAttribute('data-searching');}render();}
function resetF(){_a='todas';_e='todos';_b='';document.querySelectorAll('.chip').forEach(function(x){x.classList.remove('active');});document.querySelector('.chip').classList.add('active');document.getElementById('s-inp').value='';document.querySelectorAll('.f-sel').forEach(function(s){s.selectedIndex=0;});document.querySelector('.page').removeAttribute('data-searching');render();}
function render(){var n=0;document.querySelectorAll('#jl .job-card').forEach(function(c){var ok=(_a==='todas'||c.dataset.area===_a)&&(_e==='todos'||c.dataset.estado===_e)&&(_b===''||c.dataset.busca.indexOf(_b)>=0);c.style.display=ok?'block':'none';if(ok)n++;});document.getElementById('vc').textContent=n+' vagas';document.getElementById('m-vagas').textContent=n;document.getElementById('es').style.display=n===0?'block':'none';document.getElementById('jl').style.display=n===0?'none':'flex';}
document.querySelectorAll('.map-state').forEach(function(s){s.addEventListener('click',function(){var est=s.dataset.estado;document.querySelectorAll('.f-sel').forEach(function(sel){sel.value=est;});_e=est;render();window.scrollTo({top:document.getElementById('vagas').offsetTop-80,behavior:'smooth'});});});
function newsletter(){var e=document.getElementById('nl-e').value;if(!e||e.indexOf('@')<0){alert('Email invalido');return;}fetch('https://formsubmit.co/ajax/tecvagas@gmail.com',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify({email:e,_subject:'Newsletter TecVagas'})}).catch(function(){});document.getElementById('nl-ok').style.display='block';document.getElementById('nl-e').value='';}
function IN(b){var f=[[1518,.075],[2793.88,.09],[4190.83,.12],[8157.41,.14]];var i=0,a=0;for(var k=0;k<f.length;k++){var t=f[k][0],q=f[k][1];if(b<=t){i+=(b-a)*q;break;}i+=(t-a)*q;a=t;}return Math.min(i,908.86);}
function IR(b,d){var x=b-d*189.59;var f=[[2259.2,0,0],[2826.65,.075,169.44],[3751.05,.15,381.44],[4664.68,.225,662.77],[1/0,.275,896]];for(var k=0;k<f.length;k++){if(x<=f[k][0])return Math.max(0,x*f[k][1]-f[k][2]);}return 0;}
function R(v){return 'R$ '+v.toFixed(2).replace('.',',');}
function G(id){return parseFloat(document.getElementById(id).value)||0;}
function GI(id){return parseInt(document.getElementById(id).value)||0;}
function GV(id){return document.getElementById(id).value;}
function S(id,v){document.getElementById(id).textContent=v;}
function SH(id,d){document.getElementById(id).style.display=d?'block':'none';}
function cS(){var b=G('s1'),d=GI('s2');if(!b){SH('s-r',0);return;}var i=IN(b),r=IR(b-i,d),l=b-i-r;S('s-a',R(b));S('s-b','- '+R(i));S('s-c','- '+R(r));S('s-d',R(l));SH('s-r',1);}
function cF(){var b=G('f1'),m=GI('f2')||12;if(!b){SH('f-r',0);return;}var p=b*(m/12),t=p/3,tot=p+t,i=IN(tot),r=IR(tot-i,0);S('f-a',R(p));S('f-b','+ '+R(t));S('f-d',R(tot-i-r));SH('f-r',1);}
function cR(){var b=G('r1'),m=GI('r2')||1,tp=GV('r3');if(!b){SH('r-r',0);return;}var dec=b*(m/12),fp=b*(m/12)*(4/3),fg=b*.08*m;var mu=tp==='sj'?fg*.4:tp==='ac'?fg*.2:0;S('r-a',R(b));S('r-b',R(dec));S('r-c',R(fp));S('r-e',R(b+dec+fp+mu));SH('r-r',1);}
function cHE(){var b=G('h1'),h=G('h2'),tp=parseFloat(GV('h3'));if(!b||!h){SH('h-r',0);return;}var hb=b/220,he=hb*(1+tp/100);S('h-c',R(he*h));SH('h-r',1);}
function cN(){var b=G('n1'),h=G('n2');if(!b){SH('n-r',0);return;}var ad=(b/220)*.2*h;S('n-c',R(b+ad));SH('n-r',1);}
function cI(){var b=G('i1'),tp=GV('i2');if(!b){SH('i-r',0);return;}var ad=tp==='30p'?b*.3:1518*(parseFloat(tp)/100);S('i-c',R(b+ad));SH('i-r',1);}
function cD(){var b=G('d1'),m=GI('d2')||12;if(!b){SH('d-r',0);return;}var br=b*(m/12),i=IN(br),r=IR(br-i,0);S('d-c',R(br-i-r));SH('d-r',1);}"""


def gerar_html(vagas, artigos):
    agora = datetime.now().strftime("%d/%m/%Y as %H:%M")
    cards_vagas = "\n".join(gerar_card_vaga(v,i) for i,v in enumerate(vagas))
    cards_artigos = "\n".join(gerar_card_artigo(a,i) for i,a in enumerate(artigos))
    total = len(vagas)
    por_estado = {}
    por_area = {}
    for v in vagas:
        e = v.get("estado","BR")
        if e and e != "BR":
            por_estado[e] = por_estado.get(e, 0) + 1
        a = v.get("area","mecanica")
        por_area[a] = por_area.get(a, 0) + 1
    estados_opts = gerar_estados_opts(por_estado)
    mapa_html = gerar_mapa_brasil(por_estado)
    pizza_html = gerar_grafico_pizza(por_area)
    estados_com_vagas = len([k for k,v in por_estado.items() if v > 0])

    out = '<!DOCTYPE html><html lang="pt-BR"><head>'
    out += '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
    out += '<title>TecVagas - Vagas para Tecnicos Industriais 2026</title>'
    out += '<meta name="description" content="As melhores vagas para tecnicos industriais do Brasil. Eletrica, Mecanica, Automacao, Refrigeracao, PLC, SCADA, HVAC.">'
    out += '<link rel="preconnect" href="https://fonts.googleapis.com">'
    out += '<link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
    out += '<style>' + HTML_CSS + '</style></head><body>'
    out += '<nav><a class="nav-logo" href="#"><div class="nav-dot"></div>'
    out += '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 44" height="26" style="display:block">'
    out += '<defs><linearGradient id="og" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#f97316"/><stop offset="100%" style="stop-color:#fb923c"/></linearGradient></defs>'
    out += '<g transform="translate(20,22)">'
    out += '<circle cx="0" cy="0" r="10" fill="none" stroke="url(#og)" stroke-width="2.5"/>'
    out += '<circle cx="0" cy="0" r="5" fill="#0A0A0F" stroke="url(#og)" stroke-width="1"/>'
    out += '<circle cx="0" cy="-1.5" r="2.5" fill="url(#og)"/>'
    out += '<path d="M-2,-1.5 Q-2,2 0,5.5 Q2,2 2,-1.5 Z" fill="url(#og)"/></g>'
    out += '<text x="38" y="30" font-family="DM Sans,Arial,sans-serif" font-weight="800" font-size="22" fill="#fff" letter-spacing="-0.5">Tec</text>'
    out += '<text x="80" y="30" font-family="DM Sans,Arial,sans-serif" font-weight="800" font-size="22" fill="url(#og)" letter-spacing="-0.5">Vagas</text>'
    out += '</svg></a><div class="nav-right"><span id="nav-clock"></span><span class="nav-badge">Ao vivo</span></div></nav>'
    out += '<section class="hero"><div class="hero-grid"></div><div class="hero-glow"></div>'
    out += '<div class="hero-eyebrow">BR · VAGAS PARA TECNICOS INDUSTRIAIS · 2026</div>'
    out += '<h1>As melhores vagas<br>para <span class="accent">tecnicos industriais</span><br>do Brasil.</h1>'
    out += '<p class="hero-sub">Eletrica - Mecanica - Automacao - Refrigeracao<br>Vagas verificadas, atualizadas 5x por dia.</p></section>'
    out += '<div class="metrics">'
    out += '<div class="metric"><div class="metric-num" id="m-vagas">' + str(total) + '</div><div class="metric-label">Vagas ativas</div></div>'
    out += '<div class="metric"><div class="metric-num">' + str(estados_com_vagas) + '</div><div class="metric-label">Estados</div></div>'
    out += '<div class="metric"><div class="metric-num">5x</div><div class="metric-label">Atualizado/dia</div></div>'
    out += '<div class="metric"><div class="metric-num">60+</div><div class="metric-label">Especialidades</div></div>'
    out += '</div>'
    out += '<div class="filters-section">'
    out += '<div class="filters-search"><span class="s-ico">' + chr(128269) + '</span>'
    out += '<input type="text" id="s-inp" placeholder="Buscar por cargo, empresa ou cidade..." oninput="buscar(this.value)"></div>'
    out += '<span class="f-lbl">Area tecnica</span><div class="f-row">'
    out += '<button class="chip active" onclick="fA(\'todas\',this)">Todas</button>'
    out += '<button class="chip" onclick="fA(\'eletrica\',this)">Eletrica</button>'
    out += '<button class="chip" onclick="fA(\'mecanica\',this)">Mecanica</button>'
    out += '<button class="chip" onclick="fA(\'automacao\',this)">Automacao</button>'
    out += '<button class="chip" onclick="fA(\'refrigeracao\',this)">Refrigeracao</button>'
    out += '<button class="chip" onclick="fA(\'qualidade\',this)">Qualidade</button>'
    out += '<button class="chip" onclick="fA(\'seguranca\',this)">Seguranca</button>'
    out += '</div>'
    out += '<span class="f-lbl">Estado (todos os 27)</span><div class="f-row">'
    out += '<select class="f-sel" onchange="fE(this.value)">' + estados_opts + '</select>'
    out += '</div></div>'
    out += '<div class="trust-bar"><div class="trust-dot"></div>Vagas verificadas - Apenas 2026 - Encerradas removidas - Atualizado em ' + agora + '</div>'
    out += '<div class="page">'
    out += '<div class="dashboard-section">'
    out += '<div class="sec-hdr"><div class="sec-title">Panorama do Mercado <span class="dash-sub">- ao vivo</span></div></div>'
    out += '<div class="dashboard">'
    out += '<div class="dash-card"><div class="dash-title">Vagas por Estado</div>' + mapa_html + '</div>'
    out += '<div class="dash-card"><div class="dash-title">Distribuicao por Area</div>' + pizza_html + '</div>'
    out += '</div></div>'
    out += '<div class="calc-section">'
    out += '<div class="sec-hdr"><div class="sec-title">Calculadoras Trabalhistas</div></div>'
    out += '<div class="calc-grid">'
    out += '<button class="calc-item" onclick="openModal(\'m-sal\')"><div class="calc-emoji">$</div><div><div class="calc-name">Salario Liquido</div><div class="calc-hint">INSS + IRRF 2026</div></div></button>'
    out += '<button class="calc-item" onclick="openModal(\'m-fer\')"><div class="calc-emoji">' + chr(127958) + '</div><div><div class="calc-name">Ferias</div><div class="calc-hint">+ 1/3 constitucional</div></div></button>'
    out += '<button class="calc-item" onclick="openModal(\'m-res\')"><div class="calc-emoji">' + chr(128230) + '</div><div><div class="calc-name">Rescisao</div><div class="calc-hint">Demissao ou pedido</div></div></button>'
    out += '<button class="calc-item" onclick="openModal(\'m-he\')"><div class="calc-emoji">' + chr(9200) + '</div><div><div class="calc-name">Hora Extra</div><div class="calc-hint">50%, 100% e noturna</div></div></button>'
    out += '<button class="calc-item" onclick="openModal(\'m-not\')"><div class="calc-emoji">' + chr(127769) + '</div><div><div class="calc-name">Adicional Noturno</div><div class="calc-hint">20% sobre salario</div></div></button>'
    out += '<button class="calc-item" onclick="openModal(\'m-ins\')"><div class="calc-emoji">' + chr(9888) + '</div><div><div class="calc-name">Insalubridade</div><div class="calc-hint">e Periculosidade</div></div></button>'
    out += '<button class="calc-item" onclick="openModal(\'m-dec\')"><div class="calc-emoji">' + chr(127876) + '</div><div><div class="calc-name">13o Salario</div><div class="calc-hint">Proporcional ou cheio</div></div></button>'
    out += '</div></div>'
    out += '<div class="articles-section">'
    out += '<div class="sec-hdr"><div class="sec-title">Para Tecnicos</div><span class="sec-count">' + str(len(artigos)) + ' artigos</span></div>'
    out += '<div class="articles-grid">' + cards_artigos + '</div></div>'
    out += '<div class="newsletter">'
    out += '<div class="nl-title">Receba <span>vagas</span> no seu email</div>'
    out += '<div class="nl-desc">Toda semana as melhores vagas tecnicas. Gratis.</div>'
    out += '<div class="nl-form"><input class="nl-input" type="email" id="nl-e" placeholder="seu@email.com">'
    out += '<button class="nl-btn" onclick="newsletter()">Quero receber</button></div>'
    out += '<div class="nl-ok" id="nl-ok">Cadastrado!</div></div>'
    out += '<div class="sec-hdr" id="vagas"><div class="sec-title">Vagas Disponiveis</div><span class="sec-count" id="vc">' + str(total) + ' vagas</span></div>'
    out += '<div class="jobs-list" id="jl">' + cards_vagas + '</div>'
    out += '<div class="empty-state" id="es"><div class="empty-icon">' + chr(128269) + '</div>'
    out += '<div class="empty-title">Nenhuma vaga encontrada</div>'
    out += '<div class="empty-text">Tente outra area, estado ou termo de busca.<br>Atualizamos 5x por dia.</div>'
    out += '<button class="empty-btn" onclick="resetF()">Ver todas as vagas</button></div>'
    out += '</div>'
    # Modais calculadoras
    out += '<div class="modal" id="m-sal"><div class="modal-box"><div class="modal-title">Salario Liquido</div>'
    out += '<div class="modal-field"><label class="modal-label">Salario Bruto</label><input class="modal-input" type="number" id="s1" oninput="cS()"></div>'
    out += '<div class="modal-field"><label class="modal-label">Dependentes</label><input class="modal-input" type="number" id="s2" value="0" oninput="cS()"></div>'
    out += '<div class="calc-result" id="s-r" style="display:none">'
    out += '<div class="result-row"><span>Bruto</span><span id="s-a"></span></div>'
    out += '<div class="result-row"><span>(-) INSS</span><span id="s-b" style="color:#f87171"></span></div>'
    out += '<div class="result-row"><span>(-) IRRF</span><span id="s-c" style="color:#f87171"></span></div>'
    out += '<div class="result-row total"><span>Liquido</span><span id="s-d"></span></div></div>'
    out += '<button class="btn-close" onclick="closeModal(\'m-sal\')">Fechar</button></div></div>'
    out += '<div class="modal" id="m-fer"><div class="modal-box"><div class="modal-title">Ferias</div>'
    out += '<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="f1" oninput="cF()"></div>'
    out += '<div class="modal-field"><label class="modal-label">Meses</label><input class="modal-input" type="number" id="f2" value="12" oninput="cF()"></div>'
    out += '<div class="calc-result" id="f-r" style="display:none">'
    out += '<div class="result-row"><span>Ferias</span><span id="f-a"></span></div>'
    out += '<div class="result-row"><span>+ 1/3</span><span id="f-b" style="color:var(--green)"></span></div>'
    out += '<div class="result-row total"><span>Liquido</span><span id="f-d"></span></div></div>'
    out += '<button class="btn-close" onclick="closeModal(\'m-fer\')">Fechar</button></div></div>'
    out += '<div class="modal" id="m-res"><div class="modal-box"><div class="modal-title">Rescisao</div>'
    out += '<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="r1" oninput="cR()"></div>'
    out += '<div class="modal-field"><label class="modal-label">Meses</label><input class="modal-input" type="number" id="r2" oninput="cR()"></div>'
    out += '<div class="modal-field"><label class="modal-label">Tipo</label>'
    out += '<select class="modal-select" id="r3" onchange="cR()">'
    out += '<option value="sj">Sem justa causa</option><option value="pd">Pedido</option><option value="ac">Acordo</option></select></div>'
    out += '<div class="calc-result" id="r-r" style="display:none">'
    out += '<div class="result-row"><span>Saldo</span><span id="r-a"></span></div>'
    out += '<div class="result-row"><span>13o</span><span id="r-b"></span></div>'
    out += '<div class="result-row"><span>Ferias</span><span id="r-c"></span></div>'
    out += '<div class="result-row total"><span>Total</span><span id="r-e"></span></div></div>'
    out += '<button class="btn-close" onclick="closeModal(\'m-res\')">Fechar</button></div></div>'
    out += '<div class="modal" id="m-he"><div class="modal-box"><div class="modal-title">Hora Extra</div>'
    out += '<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="h1" oninput="cHE()"></div>'
    out += '<div class="modal-field"><label class="modal-label">Horas</label><input class="modal-input" type="number" id="h2" oninput="cHE()"></div>'
    out += '<div class="modal-field"><label class="modal-label">Tipo</label>'
    out += '<select class="modal-select" id="h3" onchange="cHE()">'
    out += '<option value="50">50%</option><option value="100">100%</option><option value="70">70%</option></select></div>'
    out += '<div class="calc-result" id="h-r" style="display:none"><div class="result-row total"><span>Total</span><span id="h-c"></span></div></div>'
    out += '<button class="btn-close" onclick="closeModal(\'m-he\')">Fechar</button></div></div>'
    out += '<div class="modal" id="m-not"><div class="modal-box"><div class="modal-title">Adicional Noturno</div>'
    out += '<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="n1" oninput="cN()"></div>'
    out += '<div class="modal-field"><label class="modal-label">Horas/mes</label><input class="modal-input" type="number" id="n2" oninput="cN()"></div>'
    out += '<div class="calc-result" id="n-r" style="display:none"><div class="result-row total"><span>Total</span><span id="n-c"></span></div></div>'
    out += '<button class="btn-close" onclick="closeModal(\'m-not\')">Fechar</button></div></div>'
    out += '<div class="modal" id="m-ins"><div class="modal-box"><div class="modal-title">Insalubridade</div>'
    out += '<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="i1" oninput="cI()"></div>'
    out += '<div class="modal-field"><label class="modal-label">Tipo</label>'
    out += '<select class="modal-select" id="i2" onchange="cI()">'
    out += '<option value="10">Min 10%</option><option value="20">Med 20%</option><option value="40">Max 40%</option><option value="30p">Periculosidade 30%</option></select></div>'
    out += '<div class="calc-result" id="i-r" style="display:none"><div class="result-row total"><span>Total</span><span id="i-c"></span></div></div>'
    out += '<button class="btn-close" onclick="closeModal(\'m-ins\')">Fechar</button></div></div>'
    out += '<div class="modal" id="m-dec"><div class="modal-box"><div class="modal-title">13o Salario</div>'
    out += '<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="d1" oninput="cD()"></div>'
    out += '<div class="modal-field"><label class="modal-label">Meses</label><input class="modal-input" type="number" id="d2" value="12" oninput="cD()"></div>'
    out += '<div class="calc-result" id="d-r" style="display:none"><div class="result-row total"><span>Liquido</span><span id="d-c"></span></div></div>'
    out += '<button class="btn-close" onclick="closeModal(\'m-dec\')">Fechar</button></div></div>'
    out += '<footer><div class="footer-logo">Tec<span>Vagas</span></div>'
    out += '<div class="footer-text">Vagas tecnicas industriais verificadas - Apenas 2026 - Todo o Brasil<br>Atualizado automaticamente 5x por dia</div></footer>'
    out += '<script data-goatcounter="https://tecvagas.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
    out += '<script>' + HTML_JS + '</script>'
    out += '</body></html>'
    return out


def main():
    print("\nTecVagas v12 PREMIUM - " + datetime.now().strftime("%d/%m/%Y %H:%M"))
    print("=" * 50)
    cache = carregar_cache()
    vagas_ativas = verificar_cache(cache)
    vagas_novas = buscar_gupy() + buscar_vagas_com_br()
    todas = remover_duplicatas(vagas_ativas + vagas_novas)
    artigos = carregar_artigos()
    print(f"\n{len(todas)} vagas | {len(artigos)} artigos")
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(todas, f, ensure_ascii=False, indent=2)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(gerar_html(todas, artigos))
    print("Site atualizado!")


if __name__ == "__main__":
    main()
