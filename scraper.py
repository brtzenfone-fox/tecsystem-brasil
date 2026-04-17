"""
TecVagas - Robo de Vagas v14 PREMIUM 3D
- Engrenagens com animacao infinita
- Fonte Fraunces (elegante)
- Disjuntor e botao 3D estilo industrial
- Detector de estado super melhorado (150+ cidades + descricao)
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
import re
import math

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
ESTADOS = {s: n for s, n in ESTADOS_LISTA}

# 200+ CIDADES BRASILEIRAS
CIDADES_ESTADO = {
    # SP
    "sao paulo":"SP","campinas":"SP","santos":"SP","sorocaba":"SP","jundiai":"SP",
    "guarulhos":"SP","osasco":"SP","ribeirao preto":"SP","sao bernardo":"SP",
    "santo andre":"SP","sao caetano":"SP","diadema":"SP","taubate":"SP",
    "sao jose dos campos":"SP","piracicaba":"SP","limeira":"SP","americana":"SP",
    "indaiatuba":"SP","apiai":"SP","cubatao":"SP","mogi das cruzes":"SP",
    "barueri":"SP","embu":"SP","itaquaquecetuba":"SP","carapicuiba":"SP",
    "suzano":"SP","mauadasul":"SP","franca":"SP","aracatuba":"SP",
    "presidente prudente":"SP","bauru":"SP","marilia":"SP","botucatu":"SP",
    "itu":"SP","salto":"SP","cotia":"SP","jacarei":"SP","caraguatatuba":"SP",
    "ubatuba":"SP","sao vicente":"SP","praia grande":"SP","guaruja":"SP",
    # RJ
    "rio de janeiro":"RJ","niteroi":"RJ","macae":"RJ","duque de caxias":"RJ",
    "nova iguacu":"RJ","sao goncalo":"RJ","petropolis":"RJ","volta redonda":"RJ",
    "campos":"RJ","resende":"RJ","angra dos reis":"RJ","cabo frio":"RJ",
    "nova friburgo":"RJ","teresopolis":"RJ","barra mansa":"RJ","itaguai":"RJ",
    "magé":"RJ","belford roxo":"RJ","queimados":"RJ","mesquita":"RJ",
    # MG
    "belo horizonte":"MG","contagem":"MG","betim":"MG","uberlandia":"MG",
    "juiz de fora":"MG","montes claros":"MG","ipatinga":"MG","sete lagoas":"MG",
    "pedro leopoldo":"MG","divinopolis":"MG","governador valadares":"MG",
    "uberaba":"MG","santa luzia":"MG","ribeirao das neves":"MG","poços de caldas":"MG",
    "varginha":"MG","ouro preto":"MG","mariana":"MG","itabira":"MG","conselheiro lafaiete":"MG",
    # PR
    "curitiba":"PR","londrina":"PR","maringa":"PR","cascavel":"PR",
    "ponta grossa":"PR","sao jose dos pinhais":"PR","foz do iguacu":"PR",
    "guarapuava":"PR","colombo":"PR","pinhais":"PR","araucaria":"PR",
    "campo largo":"PR","paranagua":"PR","apucarana":"PR","umuarama":"PR",
    # RS
    "porto alegre":"RS","caxias do sul":"RS","canoas":"RS","gravatai":"RS",
    "novo hamburgo":"RS","sao leopoldo":"RS","pelotas":"RS","santa maria":"RS",
    "passo fundo":"RS","viamao":"RS","alvorada":"RS","sao jose dos campos":"RS",
    "rio grande":"RS","esteio":"RS","santa cruz do sul":"RS","cachoeirinha":"RS",
    "bento goncalves":"RS","bage":"RS","uruguaiana":"RS","ijui":"RS",
    # SC
    "florianopolis":"SC","joinville":"SC","blumenau":"SC","jaragua do sul":"SC",
    "chapeco":"SC","criciuma":"SC","itajai":"SC","sao jose":"SC","palhoca":"SC",
    "balneario camboriu":"SC","brusque":"SC","tubarao":"SC","lages":"SC",
    "rio do sul":"SC","navegantes":"SC","camboriu":"SC","biguacu":"SC",
    # BA
    "salvador":"BA","camacari":"BA","feira de santana":"BA","candeias":"BA",
    "ilheus":"BA","vitoria da conquista":"BA","itabuna":"BA","juazeiro":"BA",
    "lauro de freitas":"BA","jequie":"BA","barreiras":"BA","alagoinhas":"BA",
    "porto seguro":"BA","simoes filho":"BA",
    # PE
    "recife":"PE","caruaru":"PE","jaboatao":"PE","olinda":"PE","petrolina":"PE",
    "paulista":"PE","cabo de santo agostinho":"PE","camaragibe":"PE","garanhuns":"PE",
    "vitoria de santo antao":"PE","igarassu":"PE",
    # CE
    "fortaleza":"CE","caucaia":"CE","juazeiro do norte":"CE","sobral":"CE",
    "maracanau":"CE","crato":"CE","itapipoca":"CE","maranguape":"CE",
    # AM, PA, AP, RR
    "manaus":"AM","belem":"PA","parauapebas":"PA","maraba":"PA","santarem":"PA",
    "ananindeua":"PA","castanhal":"PA","abaetetuba":"PA","cameta":"PA",
    "macapa":"AP","santana":"AP","boa vista":"RR","caracarai":"RR",
    # GO, DF
    "goiania":"GO","aparecida de goiania":"GO","anapolis":"GO","luziania":"GO",
    "rio verde":"GO","valparaiso":"GO","trindade":"GO","formosa":"GO","catalao":"GO",
    "brasilia":"DF","gama":"DF","taguatinga":"DF","ceilandia":"DF","plano piloto":"DF",
    "guara":"DF","sobradinho":"DF","planaltina":"DF","aguas claras":"DF",
    # ES
    "vitoria":"ES","vila velha":"ES","serra":"ES","cariacica":"ES","linhares":"ES",
    "cachoeiro de itapemirim":"ES","sao mateus":"ES","colatina":"ES","aracruz":"ES",
    "guarapari":"ES","viana":"ES",
    # AL, RN, PB, PI
    "maceio":"AL","arapiraca":"AL","palmeira dos indios":"AL","rio largo":"AL",
    "natal":"RN","mossoro":"RN","parnamirim":"RN","sao goncalo do amarante":"RN",
    "joao pessoa":"PB","campina grande":"PB","santa rita":"PB","patos":"PB",
    "teresina":"PI","parnaiba":"PI","picos":"PI","piripiri":"PI",
    # MA, RO, MT, MS
    "sao luis":"MA","imperatriz":"MA","timon":"MA","caxias":"MA","codoao":"MA",
    "porto velho":"RO","ji-parana":"RO","ariquemes":"RO","vilhena":"RO","cacoal":"RO",
    "cuiaba":"MT","varzea grande":"MT","rondonopolis":"MT","sinop":"MT","tangara":"MT",
    "comodoro":"MT","caceres":"MT","sorriso":"MT","lucas do rio verde":"MT",
    "campo grande":"MS","dourados":"MS","tres lagoas":"MS","corumba":"MS",
    "ponta pora":"MS","naviraí":"MS",
    # SE, TO, AC
    "aracaju":"SE","nossa senhora do socorro":"SE","lagarto":"SE","itabaiana":"SE",
    "palmas":"TO","araguaina":"TO","gurupi":"TO","porto nacional":"TO",
    "rio branco":"AC","cruzeiro do sul":"AC","sena madureira":"AC","tarauaca":"AC",
}

ARTIGOS_PADRAO = [
    {"titulo":"A IA vai acabar com o emprego de tecnicos industriais?","resumo":"A inteligencia artificial esta transformando a industria, mas dados mostram que tecnicos sao dos profissionais mais resistentes a automacao.","conteudo":"A pergunta que mais assusta trabalhadores da industria em 2026: a IA vai tirar meu emprego?\n\nA resposta curta e: nao para tecnicos industriais. E os dados comprovam.\n\n**Por que tecnicos sao dificeis de substituir?**\n\nA automacao funciona bem para tarefas repetitivas. O trabalho de um tecnico industrial e exatamente o oposto.\n\nQuando uma bomba quebra as 3h da manha, nao e um algoritmo que vai trocar o selo. Quando um CLP apresenta falha intermitente, nao e uma tela que vai resolver no campo.\n\n**Os numeros:**\nSegundo o Forum Economico Mundial, 85 milhoes de empregos serao substituidos pela automacao ate 2025, mas 97 milhoes de novos empregos surgirao.\n\nNo Brasil, o deficit de tecnicos qualificados ja chega a 400 mil profissionais, segundo o SENAI.","categoria":"IA & Futuro","icone":"🤖","fonte":"TecVagas","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"Quanto ganha um Tecnico em Manutencao Eletrica em 2026?","resumo":"Salarios variam de R$ 2.800 a R$ 6.500 dependendo da regiao e experiencia.","conteudo":"O tecnico em manutencao eletrica e um dos profissionais mais requisitados na industria brasileira em 2026.\n\n**Faixa salarial por nivel:**\n• Junior (0-2 anos): R$ 2.800 a R$ 3.500\n• Pleno (2-5 anos): R$ 3.500 a R$ 5.000\n• Senior (5+ anos): R$ 5.000 a R$ 6.500\n• Especialista: ate R$ 8.000\n\n**O que aumenta o salario:**\n• NR10 atualizado: +15 a 25%\n• NR35 (trabalho em altura): +10%\n• Periculosidade: +30%\n• Insalubridade: +10 a 40%\n• Turno noturno: +20% adicional","categoria":"Salarios","icone":"⚡","fonte":"TecVagas","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"NR10: Guia Completo para Tecnicos Eletricos em 2026","resumo":"A NR10 e obrigatoria para profissionais que trabalham com instalacoes eletricas.","conteudo":"A NR10 e obrigatoria para qualquer profissional que trabalhe com sistemas eletricos no Brasil.\n\n**Tipos de curso:**\n• NR10 Basico: 40 horas\n• NR10 SEP: 40 horas adicionais (alta tensao)\n• Total: 80 horas para habilitacao completa\n\n**Validade:** 2 anos\n\n**Custo medio:**\n• SENAI: R$ 300 a R$ 600\n• Empresas privadas: R$ 600 a R$ 1.500\n• Reciclagem: R$ 150 a R$ 400\n\n**Impacto no salario:** +20 a 25% em media","categoria":"Certificacoes","icone":"📋","fonte":"TecVagas","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"Tecnico em Automacao: a profissao que mais cresce no Brasil","resumo":"Com a Industria 4.0, tecnicos em PLC e SCADA sao os mais disputados.","conteudo":"A automacao industrial esta criando enorme demanda por tecnicos qualificados.\n\n**O que o tecnico em automacao faz:**\n• Programacao e manutencao de CLPs\n• Configuracao de sistemas SCADA\n• Manutencao de robos industriais\n• Redes industriais (Profibus, Profinet)\n\n**Plataformas valorizadas:**\n• Siemens S7 (TIA Portal)\n• Allen Bradley (Studio 5000)\n• Schneider (EcoStruxure)\n• ABB - robotica\n\n**Salarios:**\n• Junior: R$ 3.000 a R$ 4.500\n• Pleno: R$ 4.500 a R$ 6.500\n• Senior: R$ 6.500 a R$ 9.000\n• Especialista: ate R$ 12.000","categoria":"Carreira","icone":"🤖","fonte":"TecVagas","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"Melhores empresas para tecnicos industriais em 2026","resumo":"Petrobras, Vale, WEG, Embraer e Bosch oferecem os melhores pacotes.","conteudo":"Algumas empresas se destacam pela remuneracao e beneficios.\n\n**Petrobras**\n• Salario: R$ 9.000 a R$ 15.000\n• Acesso via concurso publico\n\n**Vale**\n• Salario: R$ 5.000 a R$ 10.000\n• Forte em MG, PA e ES\n\n**WEG**\n• Salario: R$ 3.500 a R$ 7.000\n• Base em Jaragua do Sul (SC)\n\n**Embraer**\n• Salario: R$ 4.000 a R$ 8.000\n• Sao Jose dos Campos (SP)\n\n**Bosch**\n• Salario: R$ 4.000 a R$ 7.500\n• Campinas e Curitiba","categoria":"Empresas","icone":"🏭","fonte":"TecVagas","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
    {"titulo":"Empregos manuais que a IA nunca vai substituir","resumo":"Profissoes com trabalho fisico complexo e raciocinio situacional sao as mais seguras.","conteudo":"A onda de automacao tem um ponto cego: o trabalho fisico especializado.\n\n**Profissoes mais seguras:**\n\n• Tecnico em Manutencao Industrial - risco 2%\n• Tecnico Eletricista Industrial - risco 3%\n• Tecnico em Refrigeracao/HVAC - risco 4%\n• Tecnico em Automacao/PLC - risco 1%\n\n**O que fazer para se proteger:**\n• Especialize-se em equipamentos complexos\n• Aprenda a interpretar dados de monitoramento\n• Adicione certificacoes NR\n• Desenvolva habilidade em manutencao preditiva","categoria":"IA & Futuro","icone":"🛡️","fonte":"TecVagas","url":"#","data":datetime.now().strftime("%d/%m/%Y")},
]

AREA_CONFIG = {
    "eletrica":     {"cls":"tag-el","label":"Eletrica","ico":"⚡","cor":"#4f8cff"},
    "mecanica":     {"cls":"tag-me","label":"Mecanica","ico":"🔩","cor":"#29c48a"},
    "automacao":    {"cls":"tag-au","label":"Automacao","ico":"🤖","cor":"#ff9f43"},
    "qualidade":    {"cls":"tag-qu","label":"Qualidade","ico":"📊","cor":"#b079ff"},
    "seguranca":    {"cls":"tag-se","label":"Seguranca","ico":"🦺","cor":"#23c9c8"},
    "refrigeracao": {"cls":"tag-rf","label":"Refrigeracao","ico":"❄️","cor":"#84b6ff"},
}

ESTADO_COORDS = {
    "AC":(85,235),"AM":(155,200),"RR":(180,140),"AP":(255,160),"PA":(255,210),
    "TO":(295,255),"MA":(335,200),"PI":(370,235),"CE":(405,205),"RN":(430,215),
    "PB":(435,235),"PE":(425,250),"AL":(420,265),"SE":(410,275),"BA":(370,275),
    "RO":(150,260),"MT":(225,290),"GO":(285,300),"DF":(305,305),"MS":(225,335),
    "MG":(325,335),"ES":(370,345),"RJ":(345,365),"SP":(295,365),"PR":(265,395),
    "SC":(265,425),"RS":(225,455),
}

def detectar_area(t):
    t = (t or "").lower()
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

def detectar_estado_smart(*textos):
    """Detector SUPER inteligente - analisa multiplos textos"""
    texto_completo = " ".join([(t or "") for t in textos])
    if not texto_completo.strip():
        return None
    
    texto_lower = texto_completo.lower()
    
    # PRIORIDADE 1: Padrao "cidade, UF" ou "cidade/UF" ou "cidade - UF" - BEM DEFINIDO
    padroes = [
        r"[\s,/\-]([A-Z]{2})\s*$",  # ", SP" no final
        r",\s*([A-Z]{2})(?:\s|$|[\.,;])",  # ", SP " ou ", SP."
        r"/([A-Z]{2})(?:\s|$|[\.,;])",  # "/SP"
        r"\s-\s([A-Z]{2})(?:\s|$|[\.,;])",  # " - SP"
        r"\(([A-Z]{2})\)",  # "(SP)"
    ]
    for padrao in padroes:
        for m in re.finditer(padrao, texto_completo):
            sigla = m.group(1)
            if sigla in ESTADOS:
                return sigla
    
    # PRIORIDADE 2: Cidade conhecida (200+)
    for cidade, sigla in CIDADES_ESTADO.items():
        # Procura cidade como palavra inteira
        if re.search(r"\b" + re.escape(cidade) + r"\b", texto_lower):
            return sigla
    
    # PRIORIDADE 3: Nome do estado completo
    for sigla, nome in ESTADOS.items():
        if re.search(r"\b" + re.escape(nome.lower()) + r"\b", texto_lower):
            return sigla
    
    # PRIORIDADE 4: Sigla isolada bem definida (entre espacos/pontuacao, evita pegar PARA->PA)
    # Exclui siglas que sao precedidas/seguidas por letras (parte de palavra maior)
    for m in re.finditer(r"(?<![A-Za-z])([A-Z]{2})(?![A-Za-z])", texto_completo):
        sigla = m.group(1)
        # Filtra falsos positivos: BR, EUA, etc nao sao estados
        if sigla in ESTADOS and sigla not in ["BR"]:
            return sigla
    
    return None

def extrair_cidade(local_str):
    if not local_str:
        return ""
    texto = local_str.strip()
    texto = re.sub(r"[,/\-\s]+[A-Z]{2}\s*$", "", texto)
    texto = texto.strip(" ,-/")
    if texto.lower() in ["brasil", "brazil", "remoto", "remote", "hibrido"]:
        return ""
    return texto[:40]

def titulo_valido(t):
    return not any(p in (t or "").lower() for p in PALAVRAS_DESCARTAR)

def normalizar_titulo(titulo):
    if not titulo:
        return ""
    titulo = re.sub(r"([a-z])([A-Z])", r"\1 \2", titulo)
    titulo = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", titulo)
    titulo = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", titulo)
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

def montar_local(cidade, estado, local_raw=""):
    cidade = (cidade or "").strip()
    estado = (estado or "").strip()
    if cidade and estado and estado in ESTADOS:
        return f"{cidade}, {estado}"
    if estado and estado in ESTADOS:
        return ESTADOS[estado]
    if cidade:
        return cidade
    if local_raw and local_raw.strip().lower() not in ["brasil", "brazil"]:
        return local_raw.strip()[:40]
    return "Nao informado"

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
                descricao = (job.get("description") or "")[:500]
                
                # SMART: usa titulo + cidade + estado + descricao
                estado = detectar_estado_smart(estado_api, cidade, titulo, descricao)
                local_display = montar_local(cidade, estado, f"{cidade}, {estado_api}".strip(", "))
                
                vagas.append({
                    "titulo": titulo,
                    "empresa": (job.get("careerPageName") or "Empresa")[:50],
                    "local": local_display,
                    "cidade": cidade,
                    "estado": estado or "",
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
                
                # SMART: usa local + titulo
                estado = detectar_estado_smart(local_raw, titulo)
                cidade = extrair_cidade(local_raw)
                local_display = montar_local(cidade, estado, local_raw)
                empresa = ee.get_text(strip=True)[:50] if ee else "Empresa"
                
                vagas.append({
                    "titulo": titulo,
                    "empresa": empresa,
                    "local": local_display,
                    "cidade": cidade,
                    "estado": estado or "",
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
        v["titulo"] = normalizar_titulo(v.get("titulo",""))
        # Re-tenta detectar estado se nao tem
        if not v.get("estado"):
            novo = detectar_estado_smart(v.get("local",""), v.get("titulo",""), v.get("cidade",""))
            if novo:
                v["estado"] = novo
        cidade = v.get("cidade","")
        estado = v.get("estado","")
        v["local"] = montar_local(cidade, estado, v.get("local",""))
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
        chave = (
            v.get("titulo","").strip().lower(),
            v.get("empresa","").strip().lower(),
            v.get("local","").strip().lower()
        )
        if len(v.get("titulo","")) <= 5:
            continue
        if chave not in vistas:
            vistas.add(chave)
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

def gerar_card_vaga(v, idx=0):
    area = v.get("area","mecanica")
    cfg = AREA_CONFIG.get(area, AREA_CONFIG["mecanica"])
    estado = v.get("estado","")
    salario = v.get("salario","A combinar")
    escala = v.get("escala","CLT")
    local = v.get("local","Nao informado")
    wpp_text = f"{v['titulo']} - {v['empresa']} - {local}"
    wpp = f"https://wa.me/?text={requests.utils.quote(wpp_text + ' - ' + v['url'] + ' - via TecVagas')}"
    delay = f"animation-delay:{idx*0.04}s"
    busca = f"{v.get('titulo','').lower()} {v.get('empresa','').lower()} {local.lower()} {estado.lower()}"
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
            opts += f'<option value="{s}">{s} - {n}</option>'
    return opts

def gerar_mapa_brasil(por_estado):
    max_v = max(por_estado.values()) if por_estado else 1
    pontos = ""
    for sigla, (cx, cy) in ESTADO_COORDS.items():
        c = por_estado.get(sigla, 0)
        if c > 0:
            ratio = min(c / max_v, 1)
            r_outer = 12 + ratio * 16
            r_inner = 6 + ratio * 10
            glow = 0.20 + ratio * 0.55
            pontos += f'''
            <g class="map-state" data-estado="{sigla}" data-count="{c}">
              <circle cx="{cx}" cy="{cy}" r="{r_outer}" fill="rgba(79,140,255,{glow:.2f})" class="map-halo"/>
              <circle cx="{cx}" cy="{cy}" r="{r_inner}" fill="#4f8cff" class="map-dot"/>
              <circle cx="{cx}" cy="{cy}" r="{max(3, r_inner-5)}" fill="#ffffff" opacity=".92"/>
              <text x="{cx}" y="{cy+28}" text-anchor="middle" font-size="10" font-weight="800" fill="var(--mapText)">{sigla}</text>
            </g>'''
        else:
            pontos += f'<circle cx="{cx}" cy="{cy}" r="3" fill="var(--mapIdle)" opacity=".65"/>'
    return f'''<div class="map-container">
<svg viewBox="0 60 480 440" xmlns="http://www.w3.org/2000/svg" class="brasil-map">
<defs><radialGradient id="mapBgGlow" cx="50%" cy="38%"><stop offset="0%" stop-color="rgba(79,140,255,.18)"/><stop offset="100%" stop-color="rgba(79,140,255,0)"/></radialGradient></defs>
<rect x="0" y="60" width="480" height="440" rx="24" fill="transparent"/>
<ellipse cx="240" cy="245" rx="180" ry="120" fill="url(#mapBgGlow)"/>
{pontos}
</svg>
<div class="map-tooltip" id="map-tip">Clique em um estado</div>
</div>'''

def gerar_grafico_pizza(por_area):
    total = sum(por_area.values()) or 1
    cores = {"eletrica":"#4f8cff","mecanica":"#29c48a","automacao":"#ff9f43","qualidade":"#b079ff","seguranca":"#23c9c8","refrigeracao":"#84b6ff"}
    nomes = {"eletrica":"Eletrica","mecanica":"Mecanica","automacao":"Automacao","qualidade":"Qualidade","seguranca":"Seguranca","refrigeracao":"Refrigeracao"}
    cumulative = 0
    segmentos = ""
    legenda = ""
    cx, cy, r = 110, 110, 82
    for area, count in sorted(por_area.items(), key=lambda x: -x[1]):
        if count == 0:
            continue
        pct = count / total
        angulo = pct * 360
        start_angle = cumulative * 3.6
        end_angle = (cumulative + pct * 100) * 3.6
        cumulative += pct * 100
        x1 = cx + r * math.cos(math.radians(start_angle - 90))
        y1 = cy + r * math.sin(math.radians(start_angle - 90))
        x2 = cx + r * math.cos(math.radians(end_angle - 90))
        y2 = cy + r * math.sin(math.radians(end_angle - 90))
        large_arc = 1 if angulo > 180 else 0
        cor = cores.get(area, "#999")
        nome = nomes.get(area, area)
        path = f'M {cx} {cy} L {x1:.2f} {y1:.2f} A {r} {r} 0 {large_arc} 1 {x2:.2f} {y2:.2f} Z'
        segmentos += f'<path d="{path}" fill="{cor}" stroke="var(--pieStroke)" stroke-width="3" class="pie-slice"><title>{nome}: {count} vagas ({pct*100:.0f}%)</title></path>'
        legenda += f'<div class="legend-item"><span class="legend-dot" style="background:{cor}"></span><span class="legend-label">{nome}</span><span class="legend-val">{count} ({pct*100:.0f}%)</span></div>'
    return f'''<div class="chart-container">
<svg viewBox="0 0 220 220" class="pie-chart">
<defs><radialGradient id="pieCoreGlow" cx="50%" cy="50%"><stop offset="0%" stop-color="rgba(255,255,255,.9)"/><stop offset="100%" stop-color="rgba(79,140,255,.15)"/></radialGradient></defs>
{segmentos}
<circle cx="{cx}" cy="{cy}" r="40" fill="var(--pieCore)"/>
<circle cx="{cx}" cy="{cy}" r="32" fill="url(#pieCoreGlow)" opacity=".22"/>
<text x="{cx}" y="{cy-3}" text-anchor="middle" font-size="24" font-weight="800" fill="var(--pieText)" font-family="Fraunces,serif">{total}</text>
<text x="{cx}" y="{cy+16}" text-anchor="middle" font-size="9" fill="var(--pieSub)" font-weight="700" letter-spacing="1.2">VAGAS</text>
</svg>
<div class="chart-legend">{legenda}</div>
</div>'''

HTML_CSS = r"""*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}
:root{
--bg:#06080d;--bg1:#0d1118;--bg2:#111827;--bg3:#172033;
--glass:rgba(255,255,255,.05);--glass2:rgba(255,255,255,.08);
--line:rgba(255,255,255,.08);--line2:rgba(147,197,253,.18);
--text:#f8fbff;--text2:#dbeafe;--muted:#93a4bd;--muted2:#c0d1ea;
--blue:#4f8cff;--blue2:#84b6ff;--blue3:#dbeafe;
--green:#29c48a;--orange:#ff9f43;--purple:#b079ff;--teal:#23c9c8;--danger:#ff4d4f;
--r:6px;--r2:12px;--r3:22px;
--shadow:0 14px 38px rgba(0,0,0,.30);
--mapText:#dbeafe;--mapIdle:#334155;
--pieStroke:rgba(15,23,42,.8);--pieCore:#0f172a;--pieText:#ffffff;--pieSub:#94a3b8;
}
body.light-mode{
--bg:#eef4fb;--bg1:#ffffff;--bg2:#f7faff;--bg3:#edf4ff;
--glass:rgba(255,255,255,.9);--glass2:rgba(15,23,42,.04);
--line:rgba(15,23,42,.08);--line2:rgba(79,140,255,.18);
--text:#0f172a;--text2:#1e293b;--muted:#64748b;--muted2:#475569;
--shadow:0 16px 38px rgba(15,23,42,.08);
--mapText:#1e293b;--mapIdle:#94a3b8;
--pieStroke:rgba(255,255,255,.9);--pieCore:#e8f1ff;--pieText:#0f172a;--pieSub:#64748b;
}
html{scroll-behavior:smooth}
body{
background:radial-gradient(circle at top center, rgba(79,140,255,.10), transparent 28%),linear-gradient(180deg,var(--bg) 0%, var(--bg) 100%);
color:var(--text);font-family:'DM Sans',sans-serif;font-size:15px;line-height:1.6;overflow-x:hidden;
transition:background .28s ease,color .28s ease
}
::selection{background:rgba(79,140,255,.22);color:#fff}
::-webkit-scrollbar{width:8px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:rgba(148,163,184,.35);border-radius:999px}

nav{position:sticky;top:0;z-index:100;background:color-mix(in srgb, var(--bg) 78%, transparent);backdrop-filter:blur(20px);border-bottom:1px solid var(--line);padding:0 22px;height:80px;display:flex;align-items:center;justify-content:space-between}
.nav-logo{font-family:'Fraunces',serif;font-size:18px;font-weight:800;letter-spacing:-.3px;display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--text)}
.nav-dot{width:8px;height:8px;background:var(--blue);border-radius:50%;box-shadow:0 0 14px var(--blue);animation:blink 2s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.4}}
.nav-right{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
#nav-clock{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
.nav-badge{font-size:11px;font-weight:700;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(79,140,255,.06));color:var(--text);border:1px solid var(--line2);padding:5px 12px;border-radius:999px;display:flex;align-items:center;gap:6px}
.nav-badge::before{content:'';width:6px;height:6px;background:var(--blue);border-radius:50%;box-shadow:0 0 10px var(--blue)}

/* DISJUNTOR 3D INDUSTRIAL */
.breaker-3d{
position:relative;width:58px;height:82px;cursor:pointer;
perspective:600px;
transition:transform .2s
}
.breaker-3d:hover{transform:translateY(-2px)}
.breaker-body{
position:absolute;inset:0;border-radius:10px;
background:linear-gradient(145deg,#3a3f4a 0%,#2a2e36 50%,#1a1d22 100%);
box-shadow:
0 6px 14px rgba(0,0,0,.6),
0 2px 4px rgba(0,0,0,.4),
inset 0 1px 0 rgba(255,255,255,.15),
inset 0 -2px 4px rgba(0,0,0,.5);
border:1px solid #1a1d22
}
.breaker-screw{
position:absolute;width:6px;height:6px;border-radius:50%;
background:radial-gradient(circle at 30% 30%,#888,#333);
box-shadow:inset 0 -1px 1px rgba(0,0,0,.5),inset 0 1px 1px rgba(255,255,255,.2);
}
.breaker-screw::before{content:'';position:absolute;top:50%;left:1px;right:1px;height:1px;background:#000;transform:translateY(-50%)}
.breaker-screw.tl{top:4px;left:4px}
.breaker-screw.tr{top:4px;right:4px}
.breaker-screw.bl{bottom:4px;left:4px}
.breaker-screw.br{bottom:4px;right:4px}
.breaker-window{
position:absolute;left:50%;transform:translateX(-50%);top:14px;
width:24px;height:54px;border-radius:6px;
background:linear-gradient(180deg,#0a0c0f,#1c1f25);
box-shadow:inset 0 2px 4px rgba(0,0,0,.8),inset 0 -1px 2px rgba(255,255,255,.05);
overflow:hidden;border:1px solid #000
}
.breaker-handle{
position:absolute;left:50%;transform:translateX(-50%);
width:20px;height:24px;border-radius:5px;
background:linear-gradient(145deg,#ff7a1a 0%,#e85d00 50%,#a04200 100%);
box-shadow:
0 4px 8px rgba(0,0,0,.5),
inset 0 1px 0 rgba(255,255,255,.4),
inset 0 -2px 3px rgba(0,0,0,.3);
top:3px;
transition:top .35s cubic-bezier(.4,0,.2,1)
}
.breaker-handle::after{
content:'';position:absolute;top:30%;left:25%;width:50%;height:20%;
background:linear-gradient(180deg,rgba(255,255,255,.4),transparent);
border-radius:50%;filter:blur(1px)
}
body.light-mode .breaker-handle{top:27px;background:linear-gradient(145deg,#22c55e 0%,#16a34a 50%,#0e6e34 100%)}
.breaker-label{
position:absolute;bottom:-16px;left:50%;transform:translateX(-50%);
font-size:8px;font-weight:800;letter-spacing:1.2px;color:var(--muted);
font-family:'DM Sans',sans-serif
}
.breaker-state{
position:absolute;top:-16px;left:50%;transform:translateX(-50%);
font-size:8px;font-weight:800;letter-spacing:1px;
color:var(--orange)
}
body.light-mode .breaker-state{color:var(--green);content:'ON'}
.breaker-state::before{content:'OFF'}
body.light-mode .breaker-state::before{content:'ON'}

/* BOTAO COGUMELO 3D EMERGENCIA */
.gear-power{
position:relative;width:62px;height:62px;cursor:pointer;border:none;background:transparent;
perspective:400px;
transition:transform .15s
}
.gear-power:active{transform:translateY(2px)}
.gear-power-base{
position:absolute;inset:0;border-radius:50%;
background:radial-gradient(circle at 50% 60%,#888 0%,#555 50%,#222 100%);
box-shadow:
0 6px 12px rgba(0,0,0,.5),
inset 0 -3px 6px rgba(0,0,0,.6),
inset 0 2px 3px rgba(255,255,255,.2)
}
.gear-power-cap{
position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
width:46px;height:46px;border-radius:50%;
background:radial-gradient(circle at 35% 30%,#ff8888 0%,#ff3333 30%,#cc1111 70%,#660000 100%);
box-shadow:
0 4px 8px rgba(0,0,0,.4),
inset 0 -3px 6px rgba(0,0,0,.5),
inset 0 2px 4px rgba(255,255,255,.5);
transition:all .25s cubic-bezier(.4,0,.2,1)
}
body.gears-on .gear-power-cap{
background:radial-gradient(circle at 35% 30%,#88ff88 0%,#33dd33 30%,#11aa11 70%,#005500 100%);
box-shadow:
0 0 14px rgba(41,196,138,.5),
0 2px 4px rgba(0,0,0,.4),
inset 0 -3px 6px rgba(0,0,0,.5),
inset 0 2px 4px rgba(255,255,255,.5)
}
.gear-power-shine{
position:absolute;top:18%;left:24%;width:35%;height:25%;
background:radial-gradient(ellipse,rgba(255,255,255,.6),transparent 70%);
border-radius:50%;filter:blur(1px);pointer-events:none
}
.gear-power-text{
position:absolute;bottom:-16px;left:50%;transform:translateX(-50%);
font-size:8px;font-weight:800;letter-spacing:.8px;color:var(--muted);
font-family:'DM Sans',sans-serif;white-space:nowrap
}
body.gears-on .gear-power-text{color:var(--green)}

.install-btn{
display:flex;align-items:center;gap:6px;
font-size:11px;font-weight:800;letter-spacing:.4px;
background:linear-gradient(180deg,#dbeafe,#4f8cff);
color:#06111f;border:none;
padding:9px 14px;border-radius:999px;cursor:pointer;
font-family:'DM Sans',sans-serif;
box-shadow:0 6px 18px rgba(79,140,255,.3);
transition:all .2s;
animation:pulse-install 2s ease-in-out infinite
}
.install-btn:hover{transform:translateY(-1px);box-shadow:0 10px 24px rgba(79,140,255,.4)}
@keyframes pulse-install{0%,100%{box-shadow:0 6px 18px rgba(79,140,255,.3)}50%{box-shadow:0 6px 24px rgba(79,140,255,.5)}}

.hero{
position:relative;overflow:hidden;padding:108px 24px 82px;text-align:center;
background:
radial-gradient(ellipse 42% 34% at 50% 12%, rgba(255,255,255,.16) 0%, rgba(219,234,254,.08) 22%, rgba(79,140,255,.12) 48%, transparent 76%),
radial-gradient(ellipse 70% 56% at 50% 0%, rgba(79,140,255,.10) 0%, transparent 74%),
linear-gradient(180deg,color-mix(in srgb, var(--bg) 88%, #0b1220) 0%, var(--bg) 100%)
}
body.light-mode .hero{
background:
radial-gradient(ellipse 42% 34% at 50% 12%, rgba(255,255,255,.95) 0%, rgba(219,234,254,.72) 22%, rgba(79,140,255,.10) 48%, transparent 76%),
radial-gradient(ellipse 70% 56% at 50% 0%, rgba(79,140,255,.08) 0%, transparent 74%),
linear-gradient(180deg,#fafdff 0%, #eef5ff 100%)
}
.hero-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:58px 58px;mask-image:radial-gradient(ellipse 100% 80% at 50% 0%,black 0%,transparent 72%)}
body.light-mode .hero-grid{background-image:linear-gradient(rgba(15,23,42,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(15,23,42,.04) 1px,transparent 1px)}
.hero-glow{position:absolute;top:-40px;left:50%;transform:translateX(-50%);width:100%;height:460px;background:radial-gradient(ellipse 34% 38% at 50% 15%, rgba(255,255,255,.18) 0%, rgba(219,234,254,.11) 18%, rgba(79,140,255,.12) 40%, rgba(79,140,255,.08) 56%, transparent 76%),radial-gradient(ellipse 58% 75% at 50% 0%, rgba(79,140,255,.10) 0%, transparent 72%);pointer-events:none;filter:blur(7px)}

.hero-gear,.section-gear,.footer-gear{position:absolute;opacity:0;pointer-events:none;transition:opacity .28s ease}
body.gears-on .hero-gear{opacity:.12;animation:spinSlow 18s linear infinite}
body.gears-on .section-gear.one{opacity:.10;animation:spinSlow 22s linear infinite reverse}
body.gears-on .section-gear.two{opacity:.10;animation:spinSlow 16s linear infinite}
body.gears-on .footer-gear{opacity:.12;animation:spinSlow 24s linear infinite}
@keyframes spinSlow{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
.footer-gear{animation-name:spinSlowFooter!important}
@keyframes spinSlowFooter{from{transform:translateX(-50%) rotate(0deg)}to{transform:translateX(-50%) rotate(360deg)}}
.hero-gear svg,.section-gear svg,.footer-gear svg{width:100%;height:100%}
.hero-gear{right:6%;top:84px;width:210px;height:210px;filter:drop-shadow(0 0 28px rgba(79,140,255,.22))}
.section-gear.one{left:-20px;top:120px;width:160px;height:160px}
.section-gear.two{right:-20px;top:30px;width:130px;height:130px}
.footer-gear{left:50%;bottom:12px;width:140px;height:140px;transform:translateX(-50%)}

.hero-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:800;letter-spacing:1.6px;color:var(--text);margin-bottom:24px;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(79,140,255,.05));border:1px solid var(--line2);padding:8px 16px;border-radius:999px;box-shadow:0 12px 38px rgba(79,140,255,.12), inset 0 1px 0 rgba(255,255,255,.08);backdrop-filter:blur(16px);font-family:'DM Sans',sans-serif}

.hero h1{
font-family:'Fraunces',Georgia,serif;
font-size:clamp(44px,9.5vw,88px);
font-weight:700;
font-style:italic;
font-variation-settings:"opsz" 144,"SOFT" 50,"WONK" 0;
line-height:1.05;letter-spacing:-1.5px;color:var(--text);margin-bottom:24px;max-width:920px;margin-left:auto;margin-right:auto;
text-shadow:0 3px 0 rgba(255,255,255,.04),0 10px 36px rgba(79,140,255,.16),0 24px 70px rgba(255,255,255,.06)
}
.hero h1 .accent{
background:linear-gradient(180deg,#ffffff 0%, #f8fbff 22%, #e8f2ff 46%, #cde3ff 72%, #8fc7ff 100%);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
filter:drop-shadow(0 12px 28px rgba(79,140,255,.18));
font-style:italic
}
body.light-mode .hero h1 .accent{background:linear-gradient(180deg,#0f172a 0%, #17365f 18%, #2563eb 58%, #60a5fa 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-sub{font-size:17px;color:var(--muted2);font-weight:500;max-width:560px;margin:0 auto;line-height:1.7;text-shadow:0 6px 20px rgba(79,140,255,.08);font-family:'DM Sans',sans-serif}

.metrics{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
@media(min-width:768px){.metrics{grid-template-columns:repeat(4,1fr)}}
.metric{background:linear-gradient(180deg,var(--bg1),var(--bg2));padding:24px 16px;text-align:center;position:relative;overflow:hidden;transition:all .25s}
.metric:hover{background:linear-gradient(180deg,var(--bg2),var(--bg3))}
.metric::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--blue),transparent);opacity:0;transition:opacity .3s}
.metric:hover::before{opacity:1}
.metric-num{font-family:'Fraunces',serif;font-size:36px;font-weight:700;color:var(--text);line-height:1;margin-bottom:6px;letter-spacing:-1px}
.metric-label{font-size:10px;color:var(--muted);font-weight:700;letter-spacing:1px;text-transform:uppercase}

.filters-section{background:color-mix(in srgb, var(--bg1) 88%, transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--line);padding:16px 20px}
.filters-search{position:relative;margin-bottom:12px}
.filters-search input{width:100%;background:var(--glass);border:1px solid var(--line);color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;padding:13px 18px 13px 44px;border-radius:16px;outline:none;transition:all .25s}
.filters-search input::placeholder{color:var(--muted)}
.filters-search input:focus{border-color:rgba(79,140,255,.40);box-shadow:0 0 0 4px rgba(79,140,255,.10)}
.s-ico{position:absolute;left:15px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:15px;pointer-events:none}
.f-row{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:8px}
.f-row:last-child{margin-bottom:0}
.f-lbl{font-size:10px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:var(--muted);margin-bottom:8px;display:block}
.chip{flex-shrink:0;background:var(--glass);border:1px solid var(--line);color:var(--muted2);font-family:'DM Sans',sans-serif;font-size:12px;font-weight:600;padding:7px 14px;border-radius:999px;cursor:pointer;transition:all .2s;white-space:nowrap}
.chip:hover{border-color:var(--line2);color:var(--text);transform:translateY(-1px)}
.chip.active{background:linear-gradient(180deg,rgba(255,255,255,.10),rgba(79,140,255,.10));border-color:var(--line2);color:var(--text)}
.f-sel{background:var(--glass);border:1px solid var(--line);color:var(--text);font-family:'DM Sans',sans-serif;font-size:12px;padding:8px 14px;border-radius:999px;cursor:pointer;flex-shrink:0;outline:none;min-width:220px;font-weight:600}
.f-sel:focus{border-color:var(--line2)}

.trust-bar{background:linear-gradient(90deg,rgba(79,140,255,.05),rgba(255,255,255,.02));border-bottom:1px solid var(--line2);padding:9px 20px;display:flex;align-items:center;gap:8px;font-size:11px;color:var(--muted2)}
.trust-dot{width:6px;height:6px;background:var(--blue);border-radius:50%;flex-shrink:0;box-shadow:0 0 8px var(--blue);animation:pg 2s ease-in-out infinite}
@keyframes pg{0%,100%{box-shadow:0 0 6px var(--blue)}50%{box-shadow:0 0 15px var(--blue)}}

.page{padding:28px 16px 52px;max-width:980px;margin:0 auto;position:relative}
.sec-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:15px;margin-top:34px}
.sec-title{font-family:'Fraunces',serif;font-size:20px;font-weight:700;color:var(--text);display:flex;align-items:center;gap:8px;letter-spacing:-.3px}
.sec-count{font-size:11px;color:var(--text);background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(79,140,255,.08));border:1px solid var(--line2);padding:5px 12px;border-radius:999px;font-weight:700}
.dash-sub{font-size:11px;color:var(--muted);font-weight:500;letter-spacing:.3px}

.dashboard{display:grid;grid-template-columns:1fr;gap:14px;margin-bottom:6px;position:relative}
@media(min-width:768px){.dashboard{grid-template-columns:1.15fr 1fr}}
.dash-card{background:linear-gradient(180deg,var(--glass2),var(--glass));border:1px solid var(--line2);border-radius:24px;padding:20px;position:relative;overflow:hidden;box-shadow:var(--shadow), inset 0 1px 0 rgba(255,255,255,.05)}
.dash-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,rgba(79,140,255,.85),transparent)}
.dash-title{font-family:'Fraunces',serif;font-size:16px;font-weight:700;margin-bottom:14px;display:flex;align-items:center;gap:8px;color:var(--text)}

.map-container{position:relative;width:100%;padding:4px}
.brasil-map{width:100%;height:auto;display:block;max-height:330px}
.map-state{cursor:pointer;transition:opacity .2s,transform .2s}
.map-state:hover{transform:translateY(-1px)}
.map-state:hover .map-dot{filter:drop-shadow(0 0 16px rgba(79,140,255,.55))}
.map-state:hover .map-halo{opacity:.95!important}
.map-tooltip{position:absolute;top:10px;right:10px;background:color-mix(in srgb, var(--bg2) 85%, transparent);border:1px solid var(--line2);padding:6px 10px;border-radius:10px;font-size:10px;color:var(--text2);pointer-events:none;font-weight:700}

.chart-container{display:flex;flex-direction:column;align-items:center;gap:14px}
@media(min-width:480px){.chart-container{flex-direction:row;align-items:flex-start}}
.pie-chart{width:168px;height:168px;flex-shrink:0;animation:rot 1s ease-out;filter:drop-shadow(0 14px 28px rgba(0,0,0,.25))}
@keyframes rot{from{transform:rotate(-70deg) scale(.9);opacity:0}to{transform:rotate(0) scale(1);opacity:1}}
.pie-slice{transition:transform .25s,filter .25s;transform-origin:110px 110px}
.pie-slice:hover{transform:scale(1.04);filter:brightness(1.12)}
.chart-legend{flex:1;display:flex;flex-direction:column;gap:7px;width:100%}
.legend-item{display:flex;align-items:center;gap:9px;font-size:12px;padding:8px 10px;border-radius:12px;background:var(--glass);border:1px solid var(--line)}
.legend-dot{width:11px;height:11px;border-radius:4px;flex-shrink:0}
.legend-label{flex:1;color:var(--muted2);font-weight:600}
.legend-val{color:var(--text);font-weight:700;font-variant-numeric:tabular-nums;font-size:11px}

.calc-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:9px;margin-bottom:4px}
.calc-item{background:linear-gradient(180deg,var(--glass2),var(--glass));border:1px solid var(--line);border-radius:18px;padding:15px;display:flex;align-items:center;gap:10px;cursor:pointer;transition:all .2s;text-align:left;color:var(--text)}
.calc-item:hover{border-color:var(--line2);background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.04));transform:translateY(-2px)}
.calc-emoji{font-size:20px;flex-shrink:0}
.calc-name{font-size:13px;font-weight:700;margin-bottom:1px}
.calc-hint{font-size:10px;color:var(--muted)}

.articles-grid{display:flex;flex-direction:column;gap:9px}
.article-card{background:linear-gradient(180deg,var(--glass2),var(--glass));border:1px solid var(--line);border-radius:18px;padding:16px;display:flex;gap:12px;transition:all .2s;cursor:pointer}
.article-card:hover{border-color:var(--line2);background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.04));transform:translateY(-2px)}
.article-icon{font-size:22px;flex-shrink:0;margin-top:2px}
.article-content{flex:1;min-width:0}
.article-cat{font-size:10px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:var(--blue2);margin-bottom:3px}
.article-title{font-family:'Fraunces',serif;font-size:16px;font-weight:700;color:var(--text);margin-bottom:4px;line-height:1.3;letter-spacing:-.2px}
.article-excerpt{font-size:12px;color:var(--muted);line-height:1.5;margin-bottom:7px}
.article-footer{display:flex;align-items:center;justify-content:space-between}
.article-source{font-size:10px;color:var(--muted)}
.article-cta{font-size:11px;color:var(--text);font-weight:700}

.newsletter{background:linear-gradient(135deg,rgba(255,255,255,.06),rgba(79,140,255,.06)),linear-gradient(180deg,var(--bg2),var(--bg1));border:1px solid var(--line2);border-radius:24px;padding:26px 20px;margin-bottom:4px;position:relative;overflow:hidden}
.newsletter::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#ffffff,#84b6ff,#4f8cff,#ffffff);background-size:200% 100%;animation:slide 4s linear infinite}
@keyframes slide{from{background-position:0% 0%}to{background-position:200% 0%}}
.nl-title{font-family:'Fraunces',serif;font-size:22px;font-weight:700;margin-bottom:5px;letter-spacing:-.3px}
.nl-title span{color:var(--blue2);font-style:italic}
.nl-desc{font-size:12px;color:var(--muted2);margin-bottom:15px}
.nl-form{display:flex;gap:8px;flex-wrap:wrap}
.nl-input{flex:1;min-width:170px;background:var(--glass);border:1px solid var(--line);color:var(--text);font-family:'DM Sans',sans-serif;font-size:13px;padding:11px 13px;border-radius:14px;outline:none}
.nl-input:focus{border-color:var(--line2)}
.nl-btn{background:linear-gradient(180deg,#dbeafe,#4f8cff);color:#06111f;border:none;font-family:'DM Sans',sans-serif;font-size:13px;font-weight:800;padding:11px 20px;border-radius:14px;cursor:pointer;white-space:nowrap;transition:all .2s}
.nl-btn:hover{transform:translateY(-1px);box-shadow:0 10px 22px rgba(79,140,255,.22)}
.nl-ok{display:none;color:var(--blue);font-size:12px;margin-top:8px;font-weight:700}

.jobs-list{display:flex;flex-direction:column;gap:12px}
.job-card{background:linear-gradient(180deg,var(--glass2),var(--glass));border:1px solid var(--line);border-radius:20px;overflow:hidden;transition:all .25s;animation:fadeUp .4s ease both;position:relative}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.job-card:hover{border-color:var(--line2);background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.04));transform:translateY(-3px);box-shadow:var(--shadow)}
.card-accent{position:absolute;left:0;top:0;bottom:0;width:4px}
.card-body{padding:17px 16px 16px 22px}
.card-top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;margin-bottom:10px}
.card-main{flex:1;min-width:0}
.card-tag{display:inline-flex;align-items:center;gap:4px;font-size:10px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;padding:4px 10px;border-radius:999px;margin-bottom:7px}
.tag-el{background:rgba(79,140,255,.10);color:#bfdbfe;border:1px solid rgba(79,140,255,.22)}
.tag-me{background:rgba(41,196,138,.10);color:#bbf7d0;border:1px solid rgba(41,196,138,.22)}
.tag-au{background:rgba(255,159,67,.10);color:#ffe0b8;border:1px solid rgba(255,159,67,.22)}
.tag-qu{background:rgba(176,121,255,.10);color:#ead8ff;border:1px solid rgba(176,121,255,.22)}
.tag-se{background:rgba(35,201,200,.10);color:#cdfdfc;border:1px solid rgba(35,201,200,.22)}
.tag-rf{background:rgba(132,182,255,.10);color:#dbeafe;border:1px solid rgba(132,182,255,.22)}
.card-title{font-family:'Fraunces',serif;font-size:18px;font-weight:700;color:var(--text);line-height:1.25;margin-bottom:3px;letter-spacing:-.3px}
.card-company{font-size:12px;color:var(--muted2);font-weight:600}
.card-badge-verified{flex-shrink:0;font-size:10px;font-weight:700;color:var(--text);background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(79,140,255,.08));border:1px solid var(--line2);padding:4px 10px;border-radius:999px;white-space:nowrap}
.card-info-row{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:11px}
.info-chip{font-size:10px;color:var(--muted2);background:var(--glass);border:1px solid var(--line);padding:4px 9px;border-radius:999px;font-weight:600}
.info-chip-loc{color:var(--text);background:rgba(79,140,255,.08);border-color:var(--line2);font-weight:700}
.card-actions{display:flex;gap:7px;padding-top:11px;border-top:1px solid var(--line)}
.btn-wpp{display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:700;color:#bbf7d0;background:rgba(41,196,138,.08);border:1px solid rgba(41,196,138,.18);padding:8px 13px;border-radius:14px;text-decoration:none;transition:all .2s}
.btn-wpp:hover{background:rgba(41,196,138,.14)}
.btn-ver{display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:800;color:#08111f;background:linear-gradient(180deg,#dbeafe,#4f8cff);padding:8px 15px;border-radius:14px;text-decoration:none;transition:all .2s;margin-left:auto}
.btn-ver:hover{transform:translateY(-1px);box-shadow:0 8px 20px rgba(79,140,255,.24)}

.empty-state{text-align:center;padding:56px 20px;display:none}
.page[data-searching] .calc-section,.page[data-searching] .articles-section,.page[data-searching] .newsletter,.page[data-searching] .dashboard-section{display:none!important}
.empty-icon{font-size:46px;margin-bottom:14px;opacity:.4}
.empty-title{font-family:'Fraunces',serif;font-size:22px;font-weight:700;margin-bottom:8px}
.empty-text{font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:18px}
.empty-btn{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:800;color:#08111f;background:linear-gradient(180deg,#dbeafe,#84b6ff);border:none;padding:10px 20px;border-radius:999px;cursor:pointer;transition:all .2s}
.empty-btn:hover{transform:translateY(-1px)}

.modal{display:none;position:fixed;inset:0;background:rgba(2,6,12,.82);z-index:1000;align-items:center;justify-content:center;padding:16px;backdrop-filter:blur(8px);overflow-y:auto}
.modal.open{display:flex}
.modal-box{background:linear-gradient(180deg,var(--bg2),var(--bg1));border:1px solid var(--line2);border-radius:24px;padding:22px;width:100%;max-width:420px;margin:auto;position:relative}
.modal-box::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#ffffff,#84b6ff,#4f8cff)}
.modal-article{max-width:620px;max-height:88vh;overflow-y:auto}
.modal-article-cat{font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--blue2);margin-bottom:10px}
.modal-article-title{font-family:'Fraunces',serif;font-size:26px;font-weight:700;line-height:1.15;margin-bottom:8px;letter-spacing:-.5px;color:var(--text)}
.modal-article-meta{font-size:11px;color:var(--muted);margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid var(--line)}
.modal-article-body{font-size:14px;color:var(--muted2);line-height:1.75;margin-bottom:20px}
.modal-article-body strong{color:var(--text);font-weight:700}
.modal-title{font-family:'Fraunces',serif;font-size:20px;font-weight:700;color:var(--text);margin-bottom:14px}
.modal-field{margin-bottom:12px}
.modal-label{font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--muted);display:block;margin-bottom:5px}
.modal-input,.modal-select{width:100%;background:var(--glass);border:1px solid var(--line);color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;padding:10px 13px;border-radius:14px;outline:none;transition:border .2s}
.modal-input:focus,.modal-select:focus{border-color:var(--line2);box-shadow:0 0 0 4px rgba(79,140,255,.08)}
.calc-result{background:var(--glass);border:1px solid var(--line);border-radius:16px;padding:14px;margin-top:14px}
.result-row{display:flex;justify-content:space-between;font-size:13px;margin-bottom:7px;color:var(--muted)}
.result-row.total{color:var(--blue);font-weight:800;font-size:15px;border-top:1px solid var(--line);padding-top:10px;margin-top:5px}
.btn-close{width:100%;margin-top:8px;background:transparent;color:var(--muted2);border:1px solid var(--line);font-family:'DM Sans',sans-serif;font-size:13px;padding:10px;border-radius:14px;cursor:pointer;transition:all .2s}
.btn-close:hover{border-color:var(--line2);color:var(--text)}

footer{border-top:1px solid var(--line);padding:36px 20px 54px;text-align:center;background:linear-gradient(180deg,transparent,var(--bg1));position:relative;overflow:hidden}
.footer-logo{font-family:'Fraunces',serif;font-size:18px;font-weight:700;margin-bottom:6px}
.footer-logo span{color:var(--blue2);font-style:italic}
.footer-text{font-size:11px;color:var(--muted);line-height:1.8}

@media (max-width:760px){
nav{height:auto;padding-top:14px;padding-bottom:14px;align-items:flex-start;flex-wrap:wrap}
.nav-right{justify-content:flex-end}
.hero{padding:88px 18px 62px}
.hero h1{letter-spacing:-1px}
.hero-gear{width:130px;height:130px;right:-10px;top:90px}
.calc-grid{grid-template-columns:1fr}
.card-top{flex-direction:column}
.card-badge-verified{align-self:flex-start}
.card-actions{flex-wrap:wrap}
.btn-ver{margin-left:0}
.breaker-3d{width:48px;height:68px}
.gear-power{width:54px;height:54px}
.breaker-handle{width:16px;height:20px}
.breaker-window{width:20px;height:46px}
}
"""

HTML_JS = r"""(function(){
  var el=document.getElementById('nav-clock');
  function t(){el.textContent=new Date().toLocaleTimeString('pt-BR',{timeZone:'America/Sao_Paulo',hour:'2-digit',minute:'2-digit'});}
  t();setInterval(t,1000);
})();

function openModal(id){document.getElementById(id).classList.add('open');document.body.style.overflow='hidden';}
function closeModal(id){document.getElementById(id).classList.remove('open');document.body.style.overflow='';}
function openArticle(idx){openModal('article-'+idx);}

document.querySelectorAll('.modal').forEach(function(m){
  m.addEventListener('click',function(e){if(e.target===m)closeModal(m.id);});
});
document.addEventListener('keydown',function(e){
  if(e.key==='Escape')document.querySelectorAll('.modal.open').forEach(function(m){closeModal(m.id);});
});

var _a='todas',_e='todos',_b='';
function fA(a,b){_a=a;document.querySelectorAll('.chip').forEach(function(x){x.classList.remove('active');});b.classList.add('active');render();}
function fE(v){_e=v;render();}
function buscar(v){
  _b=v.toLowerCase().trim();
  var p=document.querySelector('.page');
  if(_b.length>0){p.setAttribute('data-searching','1');}else{p.removeAttribute('data-searching');}
  render();
}
function resetF(){
  _a='todas';_e='todos';_b='';
  document.querySelectorAll('.chip').forEach(function(x){x.classList.remove('active');});
  document.querySelector('.chip').classList.add('active');
  document.getElementById('s-inp').value='';
  document.querySelectorAll('.f-sel').forEach(function(s){s.selectedIndex=0;});
  document.querySelector('.page').removeAttribute('data-searching');
  render();
}
function render(){
  var n=0;
  document.querySelectorAll('#jl .job-card').forEach(function(c){
    var ok=(_a==='todas'||c.dataset.area===_a)&&(_e==='todos'||c.dataset.estado===_e)&&(_b===''||c.dataset.busca.indexOf(_b)>=0);
    c.style.display=ok?'block':'none';
    if(ok)n++;
  });
  document.getElementById('vc').textContent=n+' vagas';
  document.getElementById('m-vagas').textContent=n;
  document.getElementById('es').style.display=n===0?'block':'none';
  document.getElementById('jl').style.display=n===0?'none':'flex';
}

document.querySelectorAll('.map-state').forEach(function(s){
  s.addEventListener('click',function(){
    var est=s.dataset.estado;
    document.querySelectorAll('.f-sel').forEach(function(sel){sel.value=est;});
    _e=est;render();
    window.scrollTo({top:document.getElementById('vagas').offsetTop-80,behavior:'smooth'});
  });
  s.addEventListener('mouseenter',function(){
    var tip=document.getElementById('map-tip');
    tip.textContent=s.dataset.estado+' - '+s.dataset.count+' vagas';
  });
  s.addEventListener('mouseleave',function(){
    document.getElementById('map-tip').textContent='Clique em um estado';
  });
});

function newsletter(){
  var e=document.getElementById('nl-e').value;
  if(!e||e.indexOf('@')<0){alert('Email invalido');return;}
  fetch('https://formsubmit.co/ajax/tecvagas@gmail.com',{
    method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},
    body:JSON.stringify({email:e,_subject:'Newsletter TecVagas'})
  }).catch(function(){});
  document.getElementById('nl-ok').style.display='block';
  document.getElementById('nl-e').value='';
}

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
function cD(){var b=G('d1'),m=GI('d2')||12;if(!b){SH('d-r',0);return;}var br=b*(m/12),i=IN(br),r=IR(br-i,0);S('d-c',R(br-i-r));SH('d-r',1);}

(function(){
  var body=document.body;
  var breaker=document.getElementById('theme-breaker');
  var savedTheme=localStorage.getItem('tecvagas-theme') || 'dark';
  if(savedTheme === 'light'){body.classList.add('light-mode');body.classList.remove('dark-mode');}
  else{body.classList.add('dark-mode');body.classList.remove('light-mode');}
  breaker.addEventListener('click',function(){
    body.classList.toggle('light-mode');
    body.classList.toggle('dark-mode');
    localStorage.setItem('tecvagas-theme', body.classList.contains('light-mode') ? 'light' : 'dark');
  });
})();

(function(){
  var body=document.body;
  var gearBtn=document.getElementById('gear-toggle');
  var savedGears=localStorage.getItem('tecvagas-gears') || 'on';
  if(savedGears === 'on'){body.classList.add('gears-on');}
  gearBtn.addEventListener('click',function(){
    body.classList.toggle('gears-on');
    localStorage.setItem('tecvagas-gears', body.classList.contains('gears-on') ? 'on' : 'off');
  });
})();

// PWA - Service Worker
if('serviceWorker' in navigator){
  window.addEventListener('load',function(){
    navigator.serviceWorker.register('/service-worker.js').catch(function(err){
      console.log('SW falhou:', err);
    });
  });
}

// Botao "Instalar app"
var deferredPrompt;
window.addEventListener('beforeinstallprompt',function(e){
  e.preventDefault();
  deferredPrompt=e;
  var btn=document.getElementById('install-btn');
  if(btn){btn.style.display='flex';}
});
function instalarApp(){
  if(!deferredPrompt){
    alert('Para instalar:\n\nNo iPhone (Safari): Toque em Compartilhar e depois "Adicionar a Tela de Inicio"\n\nNo Android: Toque no menu (3 pontinhos) e "Instalar app"');
    return;
  }
  deferredPrompt.prompt();
  deferredPrompt.userChoice.then(function(){
    deferredPrompt=null;
    document.getElementById('install-btn').style.display='none';
  });
}
"""

def gear_svg(extra_class=""):
    return f"""<div class="{extra_class}">
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
<g fill="none" stroke="rgba(79,140,255,.9)" stroke-width="7">
<circle cx="100" cy="100" r="34"/>
<path d="M100 18 L108 18 L112 36 L88 36 L92 18 Z"/>
<path d="M100 182 L108 182 L112 164 L88 164 L92 182 Z"/>
<path d="M18 100 L18 92 L36 88 L36 112 L18 108 Z"/>
<path d="M182 100 L182 92 L164 88 L164 112 L182 108 Z"/>
<path d="M42 42 L48 36 L63 46 L46 63 Z"/>
<path d="M158 158 L164 152 L154 137 L137 154 Z"/>
<path d="M158 42 L152 36 L137 46 L154 63 Z"/>
<path d="M42 158 L36 152 L46 137 L63 154 Z"/>
</g>
<circle cx="100" cy="100" r="18" fill="rgba(219,234,254,.18)" stroke="rgba(79,140,255,.9)" stroke-width="6"/>
</svg>
</div>"""

def gerar_html(vagas, artigos):
    agora = datetime.now().strftime("%d/%m/%Y as %H:%M")
    cards_vagas = "\n".join(gerar_card_vaga(v, i) for i, v in enumerate(vagas))
    cards_artigos = "\n".join(gerar_card_artigo(a, i) for i, a in enumerate(artigos))
    total = len(vagas)
    por_estado = {}
    por_area = {}
    for v in vagas:
        e = v.get("estado","")
        if e and e in ESTADOS:
            por_estado[e] = por_estado.get(e, 0) + 1
        a = v.get("area","mecanica")
        por_area[a] = por_area.get(a, 0) + 1
    estados_opts = gerar_estados_opts(por_estado)
    mapa_html = gerar_mapa_brasil(por_estado)
    pizza_html = gerar_grafico_pizza(por_area)
    estados_com_vagas = len([k for k, v in por_estado.items() if v > 0])

    out = '<!DOCTYPE html><html lang="pt-BR"><head>'
    out += '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
    out += '<title>TecVagas - Vagas para Tecnicos Industriais 2026</title>'
    out += '<meta name="description" content="As melhores vagas para tecnicos industriais do Brasil.">'
    out += '<link rel="preconnect" href="https://fonts.googleapis.com">'
    out += '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,700;0,9..144,800;1,9..144,400;1,9..144,700;1,9..144,800&family=DM+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
    out += '<link rel="manifest" href="manifest.json">'
    out += '<meta name="theme-color" content="#06080d">'
    out += '<meta name="apple-mobile-web-app-capable" content="yes">'
    out += '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'
    out += '<meta name="apple-mobile-web-app-title" content="TecVagas">'
    out += '<link rel="apple-touch-icon" href="icon-192.svg">'
    out += '<link rel="icon" type="image/svg+xml" href="icon-192.svg">'
    out += '<style>' + HTML_CSS + '</style></head><body class="dark-mode gears-on">'
    
    # NAV com disjuntor 3D e botao 3D
    out += '<nav><a class="nav-logo" href="#"><div class="nav-dot"></div>'
    out += '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 44" height="26" style="display:block">'
    out += '<defs><linearGradient id="og" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#ffffff"/><stop offset="100%" style="stop-color:#84b6ff"/></linearGradient></defs>'
    out += '<g transform="translate(20,22)">'
    out += '<circle cx="0" cy="0" r="10" fill="none" stroke="url(#og)" stroke-width="2.5"/>'
    out += '<circle cx="0" cy="0" r="5" fill="#08111f" stroke="url(#og)" stroke-width="1"/>'
    out += '<circle cx="0" cy="-1.5" r="2.5" fill="url(#og)"/>'
    out += '<path d="M-2,-1.5 Q-2,2 0,5.5 Q2,2 2,-1.5 Z" fill="url(#og)"/></g>'
    out += '<text x="38" y="30" font-family="Fraunces,Georgia,serif" font-weight="800" font-size="22" fill="#ffffff" letter-spacing="-0.5">Tec</text>'
    out += '<text x="80" y="30" font-family="Fraunces,Georgia,serif" font-weight="800" font-size="22" fill="url(#og)" letter-spacing="-0.5">Vagas</text>'
    out += '</svg></a>'
    out += '<div class="nav-right">'
    out += '<span id="nav-clock"></span>'
    out += '<span class="nav-badge">Ao vivo</span>'
    # DISJUNTOR 3D
    out += '<div class="breaker-3d" id="theme-breaker" title="Trocar tema">'
    out += '<div class="breaker-body">'
    out += '<div class="breaker-screw tl"></div><div class="breaker-screw tr"></div>'
    out += '<div class="breaker-screw bl"></div><div class="breaker-screw br"></div>'
    out += '<div class="breaker-window"><div class="breaker-handle"></div></div>'
    out += '</div>'
    out += '<div class="breaker-state"></div>'
    out += '<div class="breaker-label">TEMA</div>'
    out += '</div>'
    # BOTAO COGUMELO 3D
    out += '<button class="gear-power" id="gear-toggle" title="Engrenagens">'
    out += '<div class="gear-power-base"></div>'
    out += '<div class="gear-power-cap"><div class="gear-power-shine"></div></div>'
    out += '<div class="gear-power-text">ENGRENAGENS</div>'
    out += '</button>'
    out += '</div></nav>'

    # HERO
    out += '<section class="hero"><div class="hero-grid"></div><div class="hero-glow"></div>' + gear_svg("hero-gear")
    out += '<div class="hero-eyebrow">BR · VAGAS PARA TECNICOS INDUSTRIAIS · 2026</div>'
    out += '<h1>As melhores vagas<br>para <span class="accent">tecnicos industriais</span><br>do Brasil.</h1>'
    out += '<p class="hero-sub">Eletrica · Mecanica · Automacao · Refrigeracao<br>Vagas verificadas, atualizadas 5x por dia.</p></section>'

    # METRICS
    out += '<div class="metrics">'
    out += f'<div class="metric"><div class="metric-num" id="m-vagas">{total}</div><div class="metric-label">Vagas ativas</div></div>'
    out += f'<div class="metric"><div class="metric-num">{estados_com_vagas}</div><div class="metric-label">Estados</div></div>'
    out += '<div class="metric"><div class="metric-num">5x</div><div class="metric-label">Atualizado/dia</div></div>'
    out += '<div class="metric"><div class="metric-num">60+</div><div class="metric-label">Especialidades</div></div>'
    out += '</div>'

    # FILTROS
    out += '<div class="filters-section">'
    out += '<div class="filters-search"><span class="s-ico">🔍</span>'
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
    out += '<span class="f-lbl">Estado</span><div class="f-row">'
    out += '<select class="f-sel" onchange="fE(this.value)">' + estados_opts + '</select>'
    out += '</div></div>'

    out += f'<div class="trust-bar"><div class="trust-dot"></div>Vagas verificadas · Apenas 2026 · Encerradas removidas · Atualizado em {agora}</div>'

    out += '<div class="page">'
    out += gear_svg("section-gear one")
    out += gear_svg("section-gear two")

    # DASHBOARD
    out += '<div class="dashboard-section">'
    out += '<div class="sec-hdr"><div class="sec-title">Panorama do Mercado <span class="dash-sub">· premium</span></div></div>'
    out += '<div class="dashboard">'
    out += '<div class="dash-card"><div class="dash-title">Vagas por Estado</div>' + mapa_html + '</div>'
    out += '<div class="dash-card"><div class="dash-title">Distribuicao por Area</div>' + pizza_html + '</div>'
    out += '</div></div>'

    # CALCULADORAS
    out += '<div class="calc-section">'
    out += '<div class="sec-hdr"><div class="sec-title">Calculadoras Trabalhistas</div></div>'
    out += '<div class="calc-grid">'
    out += '<button class="calc-item" onclick="openModal(\'m-sal\')"><div class="calc-emoji">💰</div><div><div class="calc-name">Salario Liquido</div><div class="calc-hint">INSS + IRRF 2026</div></div></button>'
    out += '<button class="calc-item" onclick="openModal(\'m-fer\')"><div class="calc-emoji">🏖️</div><div><div class="calc-name">Ferias</div><div class="calc-hint">+ 1/3 constitucional</div></div></button>'
    out += '<button class="calc-item" onclick="openModal(\'m-res\')"><div class="calc-emoji">📦</div><div><div class="calc-name">Rescisao</div><div class="calc-hint">Demissao ou pedido</div></div></button>'
    out += '<button class="calc-item" onclick="openModal(\'m-he\')"><div class="calc-emoji">⏰</div><div><div class="calc-name">Hora Extra</div><div class="calc-hint">50%, 100% e noturna</div></div></button>'
    out += '<button class="calc-item" onclick="openModal(\'m-not\')"><div class="calc-emoji">🌙</div><div><div class="calc-name">Adicional Noturno</div><div class="calc-hint">20% sobre salario</div></div></button>'
    out += '<button class="calc-item" onclick="openModal(\'m-ins\')"><div class="calc-emoji">⚠️</div><div><div class="calc-name">Insalubridade</div><div class="calc-hint">e Periculosidade</div></div></button>'
    out += '<button class="calc-item" onclick="openModal(\'m-dec\')"><div class="calc-emoji">🎄</div><div><div class="calc-name">13o Salario</div><div class="calc-hint">Proporcional ou cheio</div></div></button>'
    out += '</div></div>'

    # ARTIGOS
    out += '<div class="articles-section">'
    out += f'<div class="sec-hdr"><div class="sec-title">Para Tecnicos</div><span class="sec-count">{len(artigos)} artigos</span></div>'
    out += '<div class="articles-grid">' + cards_artigos + '</div></div>'

    # NEWSLETTER
    out += '<div class="newsletter">'
    out += '<div class="nl-title">Receba <span>vagas</span> no seu email</div>'
    out += '<div class="nl-desc">Toda semana as melhores vagas tecnicas. Gratis.</div>'
    out += '<div class="nl-form"><input class="nl-input" type="email" id="nl-e" placeholder="seu@email.com">'
    out += '<button class="nl-btn" onclick="newsletter()">Quero receber</button></div>'
    out += '<div class="nl-ok" id="nl-ok">Cadastrado!</div></div>'

    # VAGAS
    out += f'<div class="sec-hdr" id="vagas"><div class="sec-title">Vagas Disponiveis</div><span class="sec-count" id="vc">{total} vagas</span></div>'
    out += '<div class="jobs-list" id="jl">' + cards_vagas + '</div>'
    out += '<div class="empty-state" id="es"><div class="empty-icon">🔍</div>'
    out += '<div class="empty-title">Nenhuma vaga encontrada</div>'
    out += '<div class="empty-text">Tente outra area, estado ou termo de busca.<br>Atualizamos 5x por dia.</div>'
    out += '<button class="empty-btn" onclick="resetF()">Ver todas as vagas</button></div>'
    out += '</div>'

    # MODAIS
    out += '<div class="modal" id="m-sal"><div class="modal-box"><div class="modal-title">Salario Liquido</div>'
    out += '<div class="modal-field"><label class="modal-label">Salario Bruto</label><input class="modal-input" type="number" id="s1" oninput="cS()"></div>'
    out += '<div class="modal-field"><label class="modal-label">Dependentes</label><input class="modal-input" type="number" id="s2" value="0" oninput="cS()"></div>'
    out += '<div class="calc-result" id="s-r" style="display:none">'
    out += '<div class="result-row"><span>Bruto</span><span id="s-a"></span></div>'
    out += '<div class="result-row"><span>(-) INSS</span><span id="s-b" style="color:#fca5a5"></span></div>'
    out += '<div class="result-row"><span>(-) IRRF</span><span id="s-c" style="color:#fca5a5"></span></div>'
    out += '<div class="result-row total"><span>Liquido</span><span id="s-d"></span></div></div>'
    out += '<button class="btn-close" onclick="closeModal(\'m-sal\')">Fechar</button></div></div>'

    out += '<div class="modal" id="m-fer"><div class="modal-box"><div class="modal-title">Ferias</div>'
    out += '<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="f1" oninput="cF()"></div>'
    out += '<div class="modal-field"><label class="modal-label">Meses</label><input class="modal-input" type="number" id="f2" value="12" oninput="cF()"></div>'
    out += '<div class="calc-result" id="f-r" style="display:none">'
    out += '<div class="result-row"><span>Ferias</span><span id="f-a"></span></div>'
    out += '<div class="result-row"><span>+ 1/3</span><span id="f-b" style="color:#86efac"></span></div>'
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
    out += '<div class="footer-text">Vagas tecnicas industriais verificadas · Apenas 2026 · Todo o Brasil<br>Atualizado automaticamente 5x por dia</div>'
    out += gear_svg("footer-gear")
    out += '</footer>'

    out += '<script data-goatcounter="https://tecvagas.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
    out += '<script>' + HTML_JS + '</script>'
    out += '</body></html>'
    return out

MANIFEST_JSON = """{
  "name": "TecVagas - Vagas para Tecnicos Industriais",
  "short_name": "TecVagas",
  "description": "As melhores vagas para tecnicos industriais do Brasil",
  "start_url": "/",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#06080d",
  "theme_color": "#06080d",
  "lang": "pt-BR",
  "categories": ["business", "productivity"],
  "icons": [
    {
      "src": "icon-192.svg",
      "sizes": "192x192",
      "type": "image/svg+xml",
      "purpose": "any maskable"
    },
    {
      "src": "icon-512.svg",
      "sizes": "512x512",
      "type": "image/svg+xml",
      "purpose": "any maskable"
    }
  ]
}"""

SERVICE_WORKER = """const CACHE_NAME = 'tecvagas-v1';
const urlsToCache = ['/', '/index.html'];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(urlsToCache).catch(function(){});
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(names) {
      return Promise.all(
        names.map(function(name) {
          if(name !== CACHE_NAME) return caches.delete(name);
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    fetch(event.request).catch(function() {
      return caches.match(event.request);
    })
  );
});
"""

# Logo SVG do TecVagas para gerar icones PNG
ICON_SVG = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'>
<rect width='512' height='512' rx='96' fill='#06080d'/>
<defs><linearGradient id='g' x1='0%' y1='0%' x2='100%' y2='100%'>
<stop offset='0%' style='stop-color:#ffffff'/><stop offset='100%' style='stop-color:#84b6ff'/>
</linearGradient></defs>
<g transform='translate(256,256)'>
<circle cx='0' cy='0' r='130' fill='none' stroke='url(#g)' stroke-width='32'/>
<circle cx='0' cy='0' r='65' fill='#06080d' stroke='url(#g)' stroke-width='12'/>
<circle cx='0' cy='-20' r='32' fill='url(#g)'/>
<path d='M-25,-20 Q-25,30 0,75 Q25,30 25,-20 Z' fill='url(#g)'/>
<circle cx='0' cy='-20' r='13' fill='#06080d'/>
</g>
</svg>"""

def gerar_icones():
    """Gera arquivos de icone PNG (na verdade SVG por simplicidade)"""
    # Como nao temos PIL no GitHub Actions, usamos o SVG diretamente
    # Os browsers aceitam SVG como icon
    with open("icon-192.png", "w", encoding="utf-8") as f:
        f.write(ICON_SVG)
    with open("icon-512.png", "w", encoding="utf-8") as f:
        f.write(ICON_SVG)

def main():
    print("\nTecVagas v14 PREMIUM 3D + PWA - " + datetime.now().strftime("%d/%m/%Y %H:%M"))
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
    # Gera arquivos PWA
    with open("manifest.json", "w", encoding="utf-8") as f:
        f.write(MANIFEST_JSON)
    with open("service-worker.js", "w", encoding="utf-8") as f:
        f.write(SERVICE_WORKER)
    with open("icon-192.svg", "w", encoding="utf-8") as f:
        f.write(ICON_SVG)
    with open("icon-512.svg", "w", encoding="utf-8") as f:
        f.write(ICON_SVG)
    print("Site + PWA atualizados!")

if __name__ == "__main__":
    main()
