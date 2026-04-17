# “””
TecVagas - Robô de Vagas v10.1

- Artigos abrem em modal com texto completo
- Todos os artigos são legíveis no site
  “””

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
import re

HEADERS = {
“User-Agent”: “Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36”,
“Accept-Language”: “pt-BR,pt;q=0.9”,
}

TECNICOS = [
“técnico em manutenção elétrica”,“técnico em elétrica industrial”,
“técnico em eletrotécnica”,“técnico em eletromecânica”,
“técnico em eletrônica industrial”,“técnico em painéis elétricos”,
“técnico em comando elétrico”,“técnico em motores elétricos”,
“técnico em subestações elétricas”,“técnico em geradores”,
“técnico em manutenção mecânica”,“técnico em mecânica industrial”,
“técnico em hidráulica industrial”,“técnico em pneumática industrial”,
“técnico em bombas industriais”,“técnico em compressores industriais”,
“técnico em válvulas industriais”,“técnico em lubrificação industrial”,
“técnico em soldagem industrial”,“técnico em caldeiraria”,
“técnico em tubulação industrial”,“técnico em usinagem”,“técnico em CNC”,
“técnico em mecatrônica”,“técnico em manutenção eletromecânica”,
“técnico em manutenção industrial”,“técnico em automação industrial”,
“técnico em PLC”,“técnico em SCADA”,“técnico em robótica industrial”,
“técnico em instrumentação industrial”,“técnico em redes industriais”,
“técnico em refrigeração industrial”,“técnico em HVAC”,
“técnico em climatização industrial”,“técnico em caldeiras industriais”,
“técnico em vapor industrial”,“técnico em ar comprimido industrial”,
“técnico em tratamento de água industrial”,“técnico em utilidades industriais”,
“técnico em manutenção preditiva”,“técnico em manutenção preventiva”,
“técnico em manutenção corretiva”,“técnico em vibração industrial”,
“técnico em análise de óleo”,“técnico em PCM”,
“técnico em confiabilidade industrial”,“técnico em planejamento de manutenção”,
“técnico em controle de qualidade industrial”,“técnico em inspeção de qualidade”,
“técnico em ensaios não destrutivos”,“técnico em metrologia industrial”,
“técnico em segurança do trabalho industrial”,“técnico em processos industriais”,
“técnico em montagem industrial”,“técnico em metalurgia”,
“técnico em siderurgia”,“técnico em mineração”,“técnico em petroquímica”,
“técnico em gás industrial”,“técnico em instalações industriais”,
]

PALAVRAS_DESCARTAR = [
“banco de talentos”,“banco de talento”,“encerrad”,“finalizad”,
“expirad”,“inativ”,“cancelad”,“processo seletivo encerrado”,
“vaga encerrada”,“não está mais disponível”,“job expired”,
“talentos 2024”,“talentos 2025”,“2023”,“2024”,
]

ANO_ATUAL = “2026”
CACHE_FILE = “vagas_cache.json”
ARTIGOS_FILE = “artigos.json”

ESTADOS = {
“AC”:“Acre”,“AL”:“Alagoas”,“AP”:“Amapá”,“AM”:“Amazonas”,
“BA”:“Bahia”,“CE”:“Ceará”,“DF”:“Distrito Federal”,“ES”:“Espírito Santo”,
“GO”:“Goiás”,“MA”:“Maranhão”,“MT”:“Mato Grosso”,“MS”:“Mato Grosso do Sul”,
“MG”:“Minas Gerais”,“PA”:“Pará”,“PB”:“Paraíba”,“PR”:“Paraná”,
“PE”:“Pernambuco”,“PI”:“Piauí”,“RJ”:“Rio de Janeiro”,“RN”:“Rio Grande do Norte”,
“RS”:“Rio Grande do Sul”,“RO”:“Rondônia”,“RR”:“Roraima”,“SC”:“Santa Catarina”,
“SP”:“São Paulo”,“SE”:“Sergipe”,“TO”:“Tocantins”,
}

ICONES_BENEFICIOS = {
“vale transporte”:“🚌”,“vale refeição”:“🍽️”,“vale alimentação”:“🛒”,
“plano médico”:“🏥”,“plano de saúde”:“🏥”,“assistência médica”:“🏥”,
“convênio médico”:“🏥”,“plano odontológico”:“🦷”,“convênio odontológico”:“🦷”,
“seguro de vida”:“🛡️”,“previdência privada”:“💰”,“participação nos lucros”:“💵”,
“gympass”:“💪”,“total pass”:“💪”,“academia”:“💪”,
“home office”:“🏠”,“trabalho remoto”:“🏠”,“cesta básica”:“🧺”,
“auxílio educação”:“📚”,“bolsa estudo”:“📚”,
}

# Artigos completos do banco de reserva

ARTIGOS_COMPLETOS = [
{
“titulo”: “Quanto ganha um Técnico em Manutenção Elétrica em 2026?”,
“resumo”: “Salários variam de R$ 2.800 a R$ 6.500 dependendo da região e experiência.”,
“conteudo”: “”“O técnico em manutenção elétrica é um dos profissionais mais requisitados na indústria brasileira em 2026.

**Faixa salarial por nível:**
• Júnior (0-2 anos): R$ 2.800 a R$ 3.500
• Pleno (2-5 anos): R$ 3.500 a R$ 5.000
• Sênior (5+ anos): R$ 5.000 a R$ 6.500
• Especialista: até R$ 8.000

**Por estado:**
• São Paulo: R$ 3.200 a R$ 6.500
• Rio de Janeiro: R$ 3.000 a R$ 6.000
• Minas Gerais: R$ 2.800 a R$ 5.500
• Paraná / Santa Catarina: R$ 3.000 a R$ 5.800
• Bahia (polo petroquímico): R$ 3.500 a R$ 7.000
• Pará (mineração): R$ 3.800 a R$ 7.500

**O que aumenta o salário:**
• NR10 atualizado: +15 a 25%
• NR35 (trabalho em altura): +10%
• Periculosidade (eletricidade): +30% sobre o salário
• Insalubridade: +10 a 40% sobre o salário mínimo
• Turno noturno: +20% adicional

**Setores que pagam mais:**

1. Petróleo e Gás (Petrobras, Shell, Equinor)
1. Mineração (Vale, Anglo American)
1. Automotivo (Toyota, Volkswagen, Fiat)
1. Papel e Celulose (Suzano, Klabin)
1. Alimentos e Bebidas (Ambev, JBS, BRF)

**Dica:** Mantenha o NR10 sempre atualizado (validade 2 anos) e busque certificações em sistemas específicos como Siemens, ABB ou Schneider para se destacar no mercado.”””,
“categoria”: “Salários”,
“icone”: “⚡”,
“fonte”: “TecVagas”,
“url”: “#”,
“data”: datetime.now().strftime(”%d/%m/%Y”),
},
{
“titulo”: “NR10: Guia Completo para Técnicos Elétricos em 2026”,
“resumo”: “A NR10 é obrigatória para todos os profissionais que trabalham com instalações elétricas.”,
“conteudo”: “”“A NR10 (Segurança em Instalações e Serviços em Eletricidade) é obrigatória para qualquer profissional que trabalhe com sistemas elétricos no Brasil.

**Quem precisa?**
• Eletricistas industriais
• Técnicos em manutenção elétrica
• Técnicos eletromecânicos
• Instrumentistas que trabalham com elétrica
• Qualquer profissional que opera painéis elétricos

**Tipos de curso:**
• NR10 Básico: 40 horas — para trabalhos em baixa tensão
• NR10 SEP: 40 horas adicionais — para trabalhos em alta tensão e sistemas elétricos de potência
• Total: 80 horas para quem precisa das duas habilitações

**Validade:** 2 anos — após isso é obrigatória a reciclagem (8 horas mínimo)

**Onde fazer:**
• SENAI (mais acessível, em todo o Brasil)
• Empresas credenciadas pelo MTE
• Online (algumas modalidades são aceitas, verifique a credenciação)

**Custo médio:**
• SENAI: R$ 300 a R$ 600
• Empresas privadas: R$ 600 a R$ 1.500
• Reciclagem: R$ 150 a R$ 400

**O que o curso aborda:**
• Fundamentos de eletricidade
• Riscos elétricos e medidas de controle
• EPIs para trabalhos elétricos
• Procedimentos de bloqueio e etiquetagem (LOTO)
• Primeiros socorros para choque elétrico
• Normas ABNT aplicáveis

**Impacto no salário:** Técnicos com NR10 atualizado ganham em média 20-25% a mais que sem a certificação. Empresas grandes como Petrobras e Vale exigem NR10 como requisito mínimo para contratação.”””,
“categoria”: “Certificações”,
“icone”: “📋”,
“fonte”: “TecVagas”,
“url”: “#”,
“data”: datetime.now().strftime(”%d/%m/%Y”),
},
{
“titulo”: “Técnico em Automação: a profissão que mais cresce no Brasil”,
“resumo”: “Com a Indústria 4.0, técnicos em PLC e SCADA são os mais disputados.”,
“conteudo”: “”“A automação industrial está transformando as fábricas brasileiras e criando uma enorme demanda por técnicos qualificados.

**Por que está crescendo tanto?**
A Indústria 4.0 chegou ao Brasil. Empresas de todos os setores estão automatizando processos para reduzir custos e aumentar eficiência. Em 2026, a demanda por técnicos em automação cresceu 35% em relação ao ano anterior.

**O que o técnico em automação faz:**
• Programação e manutenção de CLPs (CLP Siemens, Allen Bradley, Schneider)
• Configuração de sistemas SCADA e IHM
• Manutenção de robôs industriais
• Redes industriais (Profibus, Profinet, DeviceNet, Ethernet/IP)
• Inversores de frequência e servo drives
• Instrumentação e sensores

**Plataformas mais valorizadas:**

1. Siemens S7 (TIA Portal) — mais demandado no Brasil
1. Allen Bradley (Studio 5000) — forte no setor automotivo
1. Schneider (EcoStruxure) — energia e predial
1. ABB — robótica e motion control
1. Rockwell Automation — indústria pesada

**Salários:**
• Júnior: R$ 3.000 a R$ 4.500
• Pleno: R$ 4.500 a R$ 6.500
• Sênior: R$ 6.500 a R$ 9.000
• Especialista em robótica/SCADA: R$ 8.000 a R$ 12.000

**Onde se qualificar:**
• SENAI — Automação Industrial (18-24 meses)
• Cursos online Siemens Academy
• Udemy (PLCs e SCADA)
• CEFET e IFs com graduação em Controle e Automação

**Dica de ouro:** Dominar o TIA Portal da Siemens abre portas em praticamente qualquer indústria brasileira. É a plataforma mais usada no país.”””,
“categoria”: “Carreira”,
“icone”: “🤖”,
“fonte”: “TecVagas”,
“url”: “#”,
“data”: datetime.now().strftime(”%d/%m/%Y”),
},
{
“titulo”: “Melhores empresas para técnicos industriais em 2026”,
“resumo”: “Petrobras, Vale, WEG, Embraer e Bosch oferecem os melhores pacotes.”,
“conteudo”: “”“Algumas empresas se destacam pela remuneração, benefícios e oportunidades de crescimento para técnicos industriais.

**🥇 Petrobras**
• Salário: R$ 9.000 a R$ 15.000
• Acesso via concurso público
• Benefícios: plano de saúde premium, previdência privada, PLR expressivo
• Desvantagem: processo seletivo muito concorrido

**🥈 Vale**
• Salário: R$ 5.000 a R$ 10.000
• Forte em Minas Gerais, Pará e Espírito Santo
• Escalas: trabalho em turno, regime de campo
• Benefícios: plano de saúde, VA/VR, PLR, ônibus fretado

**🥉 WEG**
• Salário: R$ 3.500 a R$ 7.000
• Base em Jaraguá do Sul (SC), mas com unidades em todo o Brasil
• Excelente ambiente de trabalho e plano de carreira
• Referência em motores elétricos e automação

**4. Embraer**
• Salário: R$ 4.000 a R$ 8.000
• Foco em São José dos Campos (SP)
• Alta tecnologia aeronáutica
• Exige inglês técnico

**5. Bosch**
• Salário: R$ 4.000 a R$ 7.500
• Presença em Campinas e Curitiba
• Padrões alemães de qualidade e segurança
• Ótimo programa de desenvolvimento

**6. Ambev / JBS / BRF**
• Salário: R$ 3.000 a R$ 6.000
• Muitas vagas em todo o Brasil
• Bom para iniciar carreira técnica
• Escalas 12x36 comuns

**Como se candidatar:**
• Petrobras: concurso via Cesgranrio
• Vale, WEG, Embraer, Bosch: processo seletivo via Gupy, LinkedIn e sites próprios
• Fique de olho nas vagas aqui no TecVagas!”””,
“categoria”: “Empresas”,
“icone”: “🏭”,
“fonte”: “TecVagas”,
“url”: “#”,
“data”: datetime.now().strftime(”%d/%m/%Y”),
},
{
“titulo”: “NR12, NR33 e NR35: quais certificações valem mais?”,
“resumo”: “Cada NR pode adicionar R$ 200 a R$ 500 ao salário mensal.”,
“conteudo”: “”“As Normas Regulamentadoras (NRs) são exigências legais para trabalhos com riscos específicos. Para técnicos industriais, algumas são mais importantes que outras.

**NR12 — Segurança em Máquinas e Equipamentos**
• Para quem: técnicos que trabalham com máquinas industriais
• Duração: 8 a 16 horas (dependendo da modalidade)
• Onde é mais exigida: metalurgia, plásticos, alimentício
• Impacto salarial: +R$ 150 a R$ 300/mês
• Validade: não tem prazo, mas é recomendável reciclar a cada 2 anos

**NR33 — Trabalho em Espaços Confinados**
• Para quem: técnicos que entram em tanques, silos, dutos, caldeiras
• Duração: 16 horas
• Onde é mais exigida: petroquímica, papel/celulose, refinarias, saneamento
• Impacto salarial: +R$ 200 a R$ 400/mês
• Validade: 1 ano

**NR35 — Trabalho em Altura**
• Para quem: técnicos que trabalham acima de 2 metros
• Duração: 8 horas
• Onde é mais exigida: construção industrial, manutenção de estruturas, telecom
• Impacto salarial: +R$ 150 a R$ 300/mês
• Validade: 2 anos

**NR10 — Eletricidade (já abordamos)**
• Impacto salarial: +20 a 25%
• Essencial para qualquer técnico elétrico

**Ranking de valor para técnicos industriais:**

1. NR10 (elétricos) — maior impacto salarial
1. NR33 — rara, muito valorizada
1. NR35 — muito comum, exigida em quase toda indústria
1. NR12 — importante para manufatura
1. NR13 (vasos de pressão) — específica para utilidades

**Dica:** Ter NR10 + NR33 + NR35 juntas pode agregar até R$ 800/mês ao salário base e abre portas nas maiores empresas do Brasil.”””,
“categoria”: “Certificações”,
“icone”: “🦺”,
“fonte”: “TecVagas”,
“url”: “#”,
“data”: datetime.now().strftime(”%d/%m/%Y”),
},
{
“titulo”: “Como passar na entrevista para técnico industrial”,
“resumo”: “Dicas práticas de recrutadores sobre o que as empresas avaliam.”,
“conteudo”: “”“A entrevista para técnico industrial tem características específicas que todo candidato precisa conhecer para se sair bem.

**Antes da entrevista:**

✅ Organize seus documentos
• Certificados NR com data de validade visível
• Diploma ou certificado do curso técnico
• Registro no CREA (se aplicável)
• Portfólio de equipamentos que já trabalhou

✅ Pesquise a empresa
• Que tipo de indústria é? Alimentícia, automotiva, petroquímica?
• Quais equipamentos provavelmente usam?
• Quantos funcionários tem? É grande ou média empresa?

✅ Revise conceitos técnicos básicos
• Leitura de esquemas elétricos e diagramas hidráulicos
• Equipamentos de medição (multímetro, alicate amperímetro)
• Ordens de serviço e CMMS (SAP PM, Maximo)

**Durante a entrevista:**

🎯 Perguntas técnicas comuns:
• “Como você realiza uma manutenção preventiva?”
• “Já trabalhou com análise de falhas? Como faz?”
• “Conhece o conceito de MTBF e MTTR?”
• “Qual sua experiência com CLP/PLC?”
• “Como procede ao encontrar um equipamento parado?”

🎯 Como responder bem:
Use a técnica STAR — Situação, Tarefa, Ação, Resultado. Dê exemplos reais de situações que você resolveu.

**Erros que eliminam candidatos:**
❌ Não saber validade dos certificados NR
❌ Não conhecer nenhum sistema de gestão de manutenção
❌ Chegar sem EPI (em algumas empresas pedem na visita à planta)
❌ Não saber ler um esquema elétrico básico

**Dica final:** Vista roupas sóbrias, chegue 10 minutos antes, leve todos os documentos organizados e demonstre proatividade. No setor industrial, pontualidade e organização são muito valorizadas.”””,
“categoria”: “Dicas”,
“icone”: “💼”,
“fonte”: “TecVagas”,
“url”: “#”,
“data”: datetime.now().strftime(”%d/%m/%Y”),
},
]

def detectar_area(texto):
t=texto.lower()
if any(p in t for p in [“elétric”,“eletric”,“eletrom”,“painel”,“subestac”,“motor”,“gerador”]):return “eletrica”
if any(p in t for p in [“mecatrôn”,“mecatron”,“plc”,“scada”,“robotic”,“automac”,“automaç”,“cnc”,“instrumenta”]):return “automacao”
if any(p in t for p in [“qualidad”,“inspeç”,“metrolog”,“ensaio”,“calibr”]):return “qualidade”
if any(p in t for p in [“seguranç”,“meio ambient”]):return “seguranca”
if any(p in t for p in [“refriger”,“hvac”,“climatiz”,“ar condiciona”]):return “refrigeracao”
return “mecanica”

def detectar_estado(texto):
tu=texto.upper()
for s,n in ESTADOS.items():
if f”, {s}” in texto or n.upper() in tu:return s
return “BR”

def titulo_valido(titulo):
return not any(p in titulo.lower() for p in PALAVRAS_DESCARTAR)

def normalizar_titulo(titulo):
“”“Corrige títulos colados vindos das fontes (ex: TécnicoManutençãoElétrica).”””
# Insere espaço entre minúscula e maiúscula coladas
titulo = re.sub(r’([a-záéíóúàãõâêîôûç])([A-ZÁÉÍÓÚÀÃÕÂÊÎÔÛÇ])’, r’\1 \2’, titulo)
# Insere espaço entre letra e número colados
titulo = re.sub(r’([a-zA-ZáéíóúàãõâêîôûçÁÉÍÓÚÀÃÕÂÊÎÔÛÇ])(\d)’, r’\1 \2’, titulo)
titulo = re.sub(r’(\d)([a-zA-ZáéíóúàãõâêîôûçÁÉÍÓÚÀÃÕÂÊÎÔÛÇ])’, r’\1 \2’, titulo)
# Corrige sufixos de nível colados
for sufixo in [‘Jr’, ‘Sr’, ‘Pleno’, ‘Junior’, ‘Senior’, ‘Sênior’, ‘Trainee’, ‘Júnior’]:
titulo = re.sub(rf’(?<=[a-záéíóúàãõâêîôûç])({sufixo})\b’, rf’ \1’, titulo)
# Normaliza hífens
titulo = re.sub(r’\s*-\s*’, ’ - ‘, titulo)
# Remove espaços duplos
titulo = re.sub(r’\s+’, ’ ’, titulo)
return titulo.strip()

def icone_benef(b):
bl=b.lower()
for k,v in ICONES_BENEFICIOS.items():
if k in bl:return v
return “✅”

def formatar_conteudo(texto):
“”“Formata o conteúdo do artigo para HTML.”””
linhas = texto.strip().split(’\n’)
html = ‘’
for linha in linhas:
linha = linha.strip()
if not linha:
html += ‘<br>’
continue
# Negrito com **texto**
linha = re.sub(r’**(.*?)**’, r’<strong>\1</strong>’, linha)
# Títulos com #
if linha.startswith(’**’) and linha.endswith(’**’):
html += f’<p style="margin:12px 0 6px;font-weight:700;color:#f0f0f5">{linha[2:-2]}</p>’
# Itens de lista
elif linha.startswith(’•’) or linha.startswith(‘✅’) or linha.startswith(‘❌’) or linha.startswith(‘🎯’) or linha.startswith(‘🥇’) or linha.startswith(‘🥈’) or linha.startswith(‘🥉’):
html += f’<p style="margin:4px 0;padding-left:4px">{linha}</p>’
# Texto normal
else:
html += f’<p style="margin:8px 0">{linha}</p>’
return html

def buscar_gupy():
vagas=[]
print(“🔍 Buscando no Gupy…”)
for termo in TECNICOS[:25]:
try:
url=f”https://portal.api.gupy.io/api/v1/jobs?jobName={requests.utils.quote(termo)}&limit=5”
resp=requests.get(url,headers=HEADERS,timeout=15)
if resp.status_code!=200:continue
for job in resp.json().get(“data”,[]):
pub=str(job.get(“publishedDate”,””) or job.get(“createdAt”,””))
if ANO_ATUAL not in pub:continue
titulo=normalizar_titulo(job.get(“name”,””)[:80])
if not titulo_valido(titulo):continue
local=f”{job.get(‘city’,‘Brasil’)}, {job.get(‘state’,’’)}”
benef=[]
for b in job.get(“benefits”,[])[:5]:
if isinstance(b,dict) and b.get(“name”):benef.append(b[“name”][:30])
elif isinstance(b,str):benef.append(b[:30])
vagas.append({“titulo”:titulo,“empresa”:job.get(“careerPageName”,“Empresa”)[:50],
“local”:local,“estado”:detectar_estado(local),“url”:job.get(“jobUrl”,”#”),
“fonte”:“gupy.io”,“data”:datetime.now().strftime(”%d/%m/%Y”),
“area”:detectar_area(titulo),“beneficios”:benef,“salario”:“A combinar”,“escala”:“CLT”})
time.sleep(1.0)
except Exception as e:print(f”  ⚠️ Gupy: {e}”)
print(f”  ✅ Gupy: {len(vagas)} vagas”)
return vagas

def buscar_vagas_com_br():
vagas=[]
print(“🔍 Buscando no vagas.com.br…”)
termos=[“tecnico-manutencao-eletrica”,“tecnico-manutencao-mecanica”,
“tecnico-mecatronica”,“tecnico-automacao-industrial”,
“tecnico-instrumentacao”,“tecnico-soldagem”,“tecnico-caldeiraria”,
“tecnico-seguranca-trabalho”,“tecnico-qualidade”,“tecnico-refrigeracao”]
for termo in termos:
try:
resp=requests.get(f”https://www.vagas.com.br/vagas-de-{termo}”,headers=HEADERS,timeout=15)
if resp.status_code!=200:continue
soup=BeautifulSoup(resp.text,“html.parser”)
for card in soup.find_all(“li”,class_=“vaga”)[:8]:
te=card.find(“a”,class_=“link-detalhes-vaga”)
ee=card.find(“span”,class_=“empr-name”)
le=card.find(“span”,class_=“local”)
de=card.find(“span”,class_=“data-publicacao”) or card.find(“time”)
if not te:continue
titulo=normalizar_titulo(te.get_text(strip=True)[:80])
if not titulo_valido(titulo):continue
dt=de.get_text(strip=True) if de else “”
if “2025” in dt or “2024” in dt:continue
local=le.get_text(strip=True)[:40] if le else “Brasil”
vagas.append({“titulo”:titulo,“empresa”:ee.get_text(strip=True)[:50] if ee else “Empresa”,
“local”:local,“estado”:detectar_estado(local),
“url”:“https://www.vagas.com.br”+te.get(“href”,””),
“fonte”:“vagas.com.br”,“data”:datetime.now().strftime(”%d/%m/%Y”),
“area”:detectar_area(titulo),“beneficios”:[],“salario”:“A combinar”,“escala”:“CLT”})
time.sleep(1.5)
except Exception as e:print(f”  ⚠️ vagas.com.br: {e}”)
print(f”  ✅ vagas.com.br: {len(vagas)} vagas”)
return vagas

def buscar_infojobs():
vagas=[]
print(“🔍 Buscando no InfoJobs…”)
for termo in [“tecnico-de-manutencao-eletrica”,“tecnico-de-manutencao-mecanica”,“tecnico-mecatronica”,“tecnico-instrumentacao”]:
try:
resp=requests.get(f”https://www.infojobs.com.br/empregos/{termo}/”,headers=HEADERS,timeout=15)
if resp.status_code!=200:continue
soup=BeautifulSoup(resp.text,“html.parser”)
for card in soup.find_all(“div”,class_=“ij-offercard”)[:5]:
te=card.find(“a”,class_=“ij-offercard-title”)
ee=card.find(“span”,class_=“ij-offercard-company”)
le=card.find(“span”,class_=“ij-offercard-location”)
if not te:continue
titulo=normalizar_titulo(te.get_text(strip=True)[:80])
if not titulo_valido(titulo):continue
local=le.get_text(strip=True)[:40] if le else “Brasil”
vagas.append({“titulo”:titulo,“empresa”:ee.get_text(strip=True)[:50] if ee else “Empresa”,
“local”:local,“estado”:detectar_estado(local),“url”:te.get(“href”,”#”),
“fonte”:“infojobs.com.br”,“data”:datetime.now().strftime(”%d/%m/%Y”),
“area”:detectar_area(titulo),“beneficios”:[],“salario”:“A combinar”,“escala”:“CLT”})
time.sleep(1.5)
except Exception as e:print(f”  ⚠️ InfoJobs: {e}”)
print(f”  ✅ InfoJobs: {len(vagas)} vagas”)
return vagas

def verificar_cache(cache):
if not cache:return []
print(f”\n🔎 Verificando {len(cache)} vagas…”)
ativas=[]
for v in cache:
if not titulo_valido(v.get(“titulo”,””)):continue
try:
r=requests.get(v[“url”],headers=HEADERS,timeout=8)
if r.status_code in[404,410]:continue
if any(p in r.text.lower() for p in [“vaga encerrada”,“job expired”,“não está mais disponível”]):continue
except:pass
if “beneficios” not in v:v[“beneficios”]=[]
if “salario” not in v:v[“salario”]=“A combinar”
if “escala” not in v:v[“escala”]=“CLT”
ativas.append(v)
time.sleep(0.3)
print(f”  ✅ {len(ativas)} vagas ativas”)
return ativas

def remover_duplicatas(vagas):
vistas=set();unicas=[]
for v in vagas:
if v[“url”] not in vistas and len(v[“titulo”])>5:
vistas.add(v[“url”]);unicas.append(v)
return unicas

def carregar_cache():
try:
with open(CACHE_FILE,“r”,encoding=“utf-8”) as f:return json.load(f)
except:return []

def carregar_artigos():
“”“Carrega artigos. Se vier do RSS com URL real, usa. Senão, usa banco completo.”””
artigos_finais = []
try:
with open(ARTIGOS_FILE,“r”,encoding=“utf-8”) as f:
artigos_rss = json.load(f)
# Usa artigos RSS que têm URL real
for a in artigos_rss[:6]:
if a.get(“url”,”#”) != “#”:
artigos_finais.append(a)
except:
pass

```
# Completa com artigos do banco de reserva (com conteúdo completo)
for a in ARTIGOS_COMPLETOS:
    if len(artigos_finais) >= 6:
        break
    # Não duplica
    titulos = [x["titulo"][:30] for x in artigos_finais]
    if a["titulo"][:30] not in titulos:
        artigos_finais.append(a)

return artigos_finais[:6]
```

AREA_CONFIG = {
“eletrica”:     {“cls”:“tag-el”,“label”:“Elétrica”,“ico”:“⚡”,“cor”:”#3b82f6”},
“mecanica”:     {“cls”:“tag-me”,“label”:“Mecânica”,“ico”:“🔩”,“cor”:”#22c55e”},
“automacao”:    {“cls”:“tag-au”,“label”:“Automação”,“ico”:“🤖”,“cor”:”#f97316”},
“qualidade”:    {“cls”:“tag-qu”,“label”:“Qualidade”,“ico”:“📊”,“cor”:”#a855f7”},
“seguranca”:    {“cls”:“tag-se”,“label”:“Segurança”,“ico”:“🦺”,“cor”:”#14b8a6”},
“refrigeracao”: {“cls”:“tag-rf”,“label”:“Refrigeração”,“ico”:“❄️”,“cor”:”#60a5fa”},
}

def gerar_card_vaga(v, idx=0):
area=v.get(“area”,“mecanica”)
cfg=AREA_CONFIG.get(area,AREA_CONFIG[“mecanica”])
estado=v.get(“estado”,“BR”)
salario=v.get(“salario”,“A combinar”)
escala=v.get(“escala”,“CLT”)
benefs=v.get(“beneficios”,[])
benef_html=””
if benefs:
tags=””.join(f’<span class="benef-chip">{icone_benef(b)} {b}</span>’ for b in benefs[:3])
benef_html=f’<div class="card-benefits">{tags}</div>’
wpp=f”https://wa.me/?text=🔧 *{v[‘titulo’]}*%0A🏭 {v[‘empresa’]}%0A📍 {v[‘local’]}%0A%0A👉 {v[‘url’]}%0A%0A_Via TecVagas_”
delay=f”animation-delay:{idx*0.05}s”
return f”””<article class="job-card" style="{delay}" data-area="{area}" data-estado="{estado}" data-esp="{v.get('titulo','').lower()}" data-busca="{v.get('titulo','').lower()} {v.get('empresa','').lower()} {v.get('local','').lower()}">

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
      <span class="info-chip">📍 {v['local']}</span>
      <span class="info-chip">💰 {salario}</span>
      <span class="info-chip">📋 {escala}</span>
      <span class="info-chip">🗓 {v['data']}</span>
    </div>
    {benef_html}
    <div class="card-actions">
      <a class="btn-wpp" href="{wpp}" target="_blank" onclick="event.stopPropagation()">📲 WhatsApp</a>
      <a class="btn-ver" href="{v['url']}" target="_blank">Ver vaga →</a>
    </div>
  </div>
</article>"""

def gerar_card_artigo(a, idx=0):
“”“Gera card de artigo que abre modal com conteúdo completo.”””
has_url = a.get(“url”,”#”) != “#”
conteudo = a.get(“conteudo”,””)
conteudo_html = formatar_conteudo(conteudo) if conteudo else f’<p>{a.get(“resumo”,””)}</p>’
# Escapa aspas para uso no JS
titulo_safe = a[‘titulo’].replace(”’”,”'”).replace(’”’,’"’)

```
return f"""<div class="article-card" onclick="openArticle({idx})">
```

  <div class="article-icon">{a['icone']}</div>
  <div class="article-content">
    <div class="article-cat">{a['categoria']}</div>
    <div class="article-title">{a['titulo']}</div>
    <div class="article-excerpt">{a['resumo']}</div>
    <div class="article-footer">
      <span class="article-source">{a.get('fonte','TecVagas')} · {a.get('data','')}</span>
      <span class="article-cta">{'Ler artigo →' if not has_url else 'Ler →'}</span>
    </div>
  </div>
</div>
<div class="modal" id="article-{idx}">
  <div class="modal-box modal-article">
    <div class="modal-article-cat">{a['icone']} {a['categoria']}</div>
    <h2 class="modal-article-title">{a['titulo']}</h2>
    <div class="modal-article-meta">{a.get('fonte','TecVagas')} · {a.get('data','')}</div>
    <div class="modal-article-body">{conteudo_html if conteudo_html else f"<p>{a.get('resumo','')}</p>"}</div>
    {'<a class="modal-article-link" href="'+a['url']+'" target="_blank">Ler artigo completo →</a>' if has_url else ''}
    <button class="btn-close" onclick="closeModal(\'article-{idx}\')">Fechar</button>
  </div>
</div>"""

def gerar_opts_estados(vagas):
usados=sorted(set(v.get(“estado”,“BR”) for v in vagas if v.get(“estado”)!=“BR”))
opts=’<option value="todos">Todos os estados</option>’
for s in usados:opts+=f’<option value="{s}">{s} — {ESTADOS.get(s,s)}</option>’
return opts

def gerar_html(vagas, artigos):
agora=datetime.now().strftime(”%d/%m/%Y às %H:%M”)
cards_vagas=”\n”.join(gerar_card_vaga(v,i) for i,v in enumerate(vagas))
cards_artigos=”\n”.join(gerar_card_artigo(a,i) for i,a in enumerate(artigos))
total=len(vagas)
opts_estados=gerar_opts_estados(vagas)
tec_opts=””.join(f’<option value=”{t.replace(“técnico em”,””).strip().lower()}”>{t.replace(“técnico em”,””).strip().title()}</option>’ for t in sorted(TECNICOS))

```
return f"""<!DOCTYPE html>
```

<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TecVagas — Vagas para Técnicos Industriais 2026</title>
<meta name="description" content="As melhores vagas para técnicos industriais do Brasil. Elétrica, Mecânica, Automação, Refrigeração, PLC, SCADA, HVAC e mais.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}}
:root{{
  --bg:#0A0A0F;--bg1:#111118;--bg2:#16161F;--bg3:#1C1C28;
  --border:#ffffff0f;--border2:#ffffff18;
  --text:#F0F0F5;--muted:#7B7B8F;--muted2:#A0A0B0;
  --orange:#F97316;--orange2:#FB923C;
  --blue:#3B82F6;--blue2:#60A5FA;
  --green:#22C55E;--yellow:#FBBF24;--purple:#A855F7;--teal:#14B8A6;
  --r:4px;--r2:8px;--r3:12px;
}}
html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;font-size:15px;line-height:1.6;overflow-x:hidden}}
::-webkit-scrollbar{{width:4px}}
::-webkit-scrollbar-track{{background:var(--bg)}}
::-webkit-scrollbar-thumb{{background:var(--border2);border-radius:2px}}
nav{{position:sticky;top:0;z-index:100;background:rgba(10,10,15,0.9);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);padding:0 20px;height:56px;display:flex;align-items:center;justify-content:space-between}}
.nav-logo{{font-family:'Syne',sans-serif;font-size:17px;font-weight:800;letter-spacing:.5px;display:flex;align-items:center;gap:8px;text-decoration:none;color:var(--text)}}
.nav-dot{{width:8px;height:8px;background:var(--orange);border-radius:50%;box-shadow:0 0 8px var(--orange);animation:blink 2s ease-in-out infinite}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.nav-right{{display:flex;align-items:center;gap:10px}}
#nav-clock{{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}}
.nav-badge{{font-size:11px;font-weight:600;background:rgba(249,115,22,.12);color:var(--orange);border:1px solid rgba(249,115,22,.2);padding:3px 10px;border-radius:20px}}
.hero{{
  position:relative;overflow:hidden;
  padding:96px 24px 80px;
  text-align:center;
  background:var(--bg);
}}
.hero-grid{{
  position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);
  background-size:64px 64px;
  mask-image:radial-gradient(ellipse 100% 80% at 50% 0%,black 0%,transparent 70%);
}}
.hero-glow{{
  position:absolute;top:0;left:50%;transform:translateX(-50%);
  width:100%;height:360px;
  background:radial-gradient(ellipse 60% 100% at 50% 0%,rgba(249,115,22,.07) 0%,transparent 100%);
  pointer-events:none;
}}
.hero-eyebrow{{
  display:inline-flex;align-items:center;gap:6px;
  font-size:12px;font-weight:500;letter-spacing:.5px;
  color:var(--orange);
  margin-bottom:20px;
}}
.hero h1{{
  font-family:'Syne',sans-serif;
  font-size:clamp(36px,9vw,72px);
  font-weight:800;
  line-height:1.05;
  letter-spacing:-2.5px;
  color:#ffffff;
  margin-bottom:20px;
  max-width:700px;
  margin-left:auto;margin-right:auto;
}}
.hero h1 .accent{{
  background:linear-gradient(90deg,var(--orange),#ff9a3c);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
}}
.hero-sub{{
  font-size:17px;
  color:rgba(255,255,255,.45);
  font-weight:400;
  max-width:420px;
  margin:0 auto;
  line-height:1.65;
  letter-spacing:-.1px;
}}
.hero-ctas{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-bottom:44px}}
.btn-hero{{display:inline-flex;align-items:center;gap:8px;font-family:'DM Sans',sans-serif;font-size:14px;font-weight:600;padding:11px 22px;border-radius:var(--r2);text-decoration:none;border:none;cursor:pointer;transition:all .2s}}
.btn-primary{{background:var(--orange);color:white}}
.btn-primary:hover{{background:#ea6c0a;transform:translateY(-1px);box-shadow:0 0 20px rgba(249,115,22,.3)}}
.btn-ghost-green{{background:rgba(255,255,255,.04);color:var(--green);border:1px solid rgba(34,197,94,.25)}}
.btn-ghost-green:hover{{background:rgba(34,197,94,.08)}}
.metrics{{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--border);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}}
.metric{{background:var(--bg1);padding:18px 16px;text-align:center;position:relative;overflow:hidden}}
.metric::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--orange),transparent);opacity:0;transition:opacity .3s}}
.metric:hover::before{{opacity:1}}
.metric-num{{font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:var(--orange);line-height:1;margin-bottom:4px;letter-spacing:-1px}}
.metric-label{{font-size:10px;color:var(--muted);font-weight:500;letter-spacing:.5px;text-transform:uppercase}}
.filters-section{{background:var(--bg1);border-bottom:1px solid var(--border);padding:14px 20px}}
.filters-search{{position:relative;margin-bottom:10px}}
.filters-search input{{width:100%;background:var(--bg2);border:1px solid var(--border2);color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;padding:10px 16px 10px 42px;border-radius:var(--r2);outline:none;transition:border .2s,box-shadow .2s}}
.filters-search input::placeholder{{color:var(--muted)}}
.filters-search input:focus{{border-color:var(--orange);box-shadow:0 0 0 3px rgba(249,115,22,.1)}}
.s-ico{{position:absolute;left:13px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:15px;pointer-events:none}}
.f-row{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}}
.f-row:last-child{{margin-bottom:0}}
.f-lbl{{font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:var(--muted);margin-bottom:7px;display:block}}
.chip{{flex-shrink:0;background:var(--bg2);border:1px solid var(--border2);color:var(--muted2);font-family:'DM Sans',sans-serif;font-size:12px;font-weight:500;padding:5px 13px;border-radius:20px;cursor:pointer;transition:all .15s;white-space:nowrap}}
.chip:hover{{border-color:var(--orange);color:var(--orange)}}
.chip.active{{background:rgba(249,115,22,.12);border-color:var(--orange);color:var(--orange);font-weight:600}}
.f-sel{{background:var(--bg2);border:1px solid var(--border2);color:var(--text);font-family:'DM Sans',sans-serif;font-size:12px;padding:5px 13px;border-radius:20px;cursor:pointer;flex-shrink:0;outline:none}}
.trust-bar{{background:rgba(34,197,94,.03);border-bottom:1px solid rgba(34,197,94,.1);padding:7px 20px;display:flex;align-items:center;gap:8px;font-size:11px;color:var(--muted2)}}
.trust-dot{{width:6px;height:6px;background:var(--green);border-radius:50%;flex-shrink:0;box-shadow:0 0 6px var(--green);animation:pg 2s ease-in-out infinite}}
@keyframes pg{{0%,100%{{box-shadow:0 0 6px var(--green)}}50%{{box-shadow:0 0 12px var(--green)}}}}
.page{{padding:24px 16px 48px;max-width:860px;margin:0 auto}}
.sec-hdr{{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;margin-top:28px}}
.sec-title{{font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:var(--text);display:flex;align-items:center;gap:8px}}
.sec-count{{font-size:11px;color:var(--muted);background:var(--bg2);border:1px solid var(--border);padding:3px 10px;border-radius:20px}}
.calc-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:4px}}
.calc-item{{background:var(--bg1);border:1px solid var(--border);border-radius:var(--r2);padding:13px 14px;display:flex;align-items:center;gap:10px;cursor:pointer;transition:all .2s;text-align:left;color:var(--text)}}
.calc-item:hover{{border-color:var(--orange);background:var(--bg2);transform:translateY(-1px)}}
.calc-emoji{{font-size:19px;flex-shrink:0}}
.calc-name{{font-size:13px;font-weight:600;margin-bottom:1px}}
.calc-hint{{font-size:10px;color:var(--muted)}}
.articles-grid{{display:flex;flex-direction:column;gap:8px;margin-bottom:4px}}
.article-card{{background:var(--bg1);border:1px solid var(--border);border-radius:var(--r2);padding:14px;display:flex;gap:12px;transition:all .2s;cursor:pointer}}
.article-card:hover{{border-color:var(--border2);background:var(--bg2)}}
.article-icon{{font-size:22px;flex-shrink:0;margin-top:2px}}
.article-content{{flex:1;min-width:0}}
.article-cat{{font-size:10px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--orange);margin-bottom:3px}}
.article-title{{font-size:14px;font-weight:600;color:var(--text);margin-bottom:3px;line-height:1.35}}
.article-excerpt{{font-size:12px;color:var(--muted);line-height:1.5;margin-bottom:6px}}
.article-footer{{display:flex;align-items:center;justify-content:space-between}}
.article-source{{font-size:10px;color:var(--muted)}}
.article-cta{{font-size:11px;color:var(--orange);font-weight:600}}
.newsletter{{background:linear-gradient(135deg,var(--bg2),var(--bg3));border:1px solid var(--border);border-radius:var(--r3);padding:22px 18px;margin-bottom:4px;position:relative;overflow:hidden}}
.newsletter::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--orange),var(--blue))}}
.nl-title{{font-family:'Syne',sans-serif;font-size:17px;font-weight:700;margin-bottom:5px}}
.nl-title span{{color:var(--orange)}}
.nl-desc{{font-size:12px;color:var(--muted2);margin-bottom:14px}}
.nl-form{{display:flex;gap:8px;flex-wrap:wrap}}
.nl-input{{flex:1;min-width:170px;background:var(--bg);border:1px solid var(--border2);color:var(--text);font-family:'DM Sans',sans-serif;font-size:13px;padding:9px 12px;border-radius:var(--r2);outline:none;transition:border .2s}}
.nl-input:focus{{border-color:var(--orange)}}
.nl-btn{{background:var(--orange);color:white;border:none;font-family:'DM Sans',sans-serif;font-size:13px;font-weight:600;padding:9px 18px;border-radius:var(--r2);cursor:pointer;white-space:nowrap}}
.nl-ok{{display:none;color:var(--green);font-size:12px;margin-top:8px;font-weight:500}}
.jobs-list{{display:flex;flex-direction:column;gap:10px}}
.job-card{{background:var(--bg1);border:1px solid var(--border);border-radius:var(--r2);overflow:hidden;transition:all .2s;animation:fadeUp .4s ease both;position:relative}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
.job-card:hover{{border-color:var(--border2);background:var(--bg2);transform:translateY(-2px);box-shadow:0 8px 32px rgba(0,0,0,.3)}}
.card-accent{{position:absolute;left:0;top:0;bottom:0;width:3px}}
.card-body{{padding:15px 15px 15px 20px}}
.card-top{{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;margin-bottom:10px}}
.card-main{{flex:1;min-width:0}}
.card-tag{{display:inline-flex;align-items:center;gap:4px;font-size:10px;font-weight:600;letter-spacing:.8px;text-transform:uppercase;padding:2px 9px;border-radius:20px;margin-bottom:5px}}
.tag-el{{background:rgba(59,130,246,.12);color:var(--blue2);border:1px solid rgba(59,130,246,.2)}}
.tag-me{{background:rgba(34,197,94,.12);color:#4ade80;border:1px solid rgba(34,197,94,.2)}}
.tag-au{{background:rgba(249,115,22,.12);color:var(--orange2);border:1px solid rgba(249,115,22,.2)}}
.tag-qu{{background:rgba(168,85,247,.12);color:#c084fc;border:1px solid rgba(168,85,247,.2)}}
.tag-se{{background:rgba(20,184,166,.12);color:#2dd4bf;border:1px solid rgba(20,184,166,.2)}}
.tag-rf{{background:rgba(96,165,250,.12);color:var(--blue2);border:1px solid rgba(96,165,250,.2)}}
.card-title{{font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:var(--text);line-height:1.3;margin-bottom:3px;letter-spacing:-.2px}}
.card-company{{font-size:12px;color:var(--muted2)}}
.card-badge-verified{{flex-shrink:0;font-size:10px;font-weight:600;color:var(--green);background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.2);padding:2px 8px;border-radius:20px;white-space:nowrap}}
.card-info-row{{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px}}
.info-chip{{font-size:10px;color:var(--muted2);background:var(--bg3);border:1px solid var(--border);padding:2px 8px;border-radius:var(--r)}}
.card-benefits{{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px}}
.benef-chip{{font-size:10px;color:var(--yellow);background:rgba(251,191,36,.06);border:1px solid rgba(251,191,36,.15);padding:2px 7px;border-radius:var(--r)}}
.card-actions{{display:flex;gap:7px;padding-top:10px;border-top:1px solid var(--border)}}
.btn-wpp{{display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:600;color:var(--green);background:rgba(34,197,94,.06);border:1px solid rgba(34,197,94,.2);padding:6px 13px;border-radius:var(--r2);text-decoration:none;transition:all .2s}}
.btn-wpp:hover{{background:rgba(34,197,94,.12)}}
.btn-ver{{display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:600;color:white;background:var(--orange);padding:6px 14px;border-radius:var(--r2);text-decoration:none;transition:all .2s;margin-left:auto}}
.btn-ver:hover{{background:#ea6c0a}}
.empty-state{{text-align:center;padding:48px 20px;display:none}}
/* Modo busca: esconde calculadoras, artigos e newsletter */
.page[data-searching] .calc-section,
.page[data-searching] .articles-section,
.page[data-searching] .newsletter{{display:none!important}}
.empty-icon{{font-size:44px;margin-bottom:14px;opacity:.4}}
.empty-title{{font-family:'Syne',sans-serif;font-size:18px;font-weight:700;margin-bottom:8px}}
.empty-text{{font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:18px}}
.empty-btn{{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:var(--orange);background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);padding:8px 18px;border-radius:20px;cursor:pointer;transition:all .2s}}
.empty-btn:hover{{background:rgba(249,115,22,.15)}}
.modal{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:1000;align-items:center;justify-content:center;padding:16px;backdrop-filter:blur(4px);overflow-y:auto}}
.modal.open{{display:flex}}
.modal-box{{background:var(--bg2);border:1px solid var(--border2);border-radius:var(--r3);padding:22px;width:100%;max-width:400px;margin:auto;position:relative}}
.modal-box::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--orange),var(--blue));border-radius:var(--r3) var(--r3) 0 0}}
.modal-article{{max-width:560px;max-height:85vh;overflow-y:auto}}
.modal-article-cat{{font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--orange);margin-bottom:10px}}
.modal-article-title{{font-family:'Syne',sans-serif;font-size:20px;font-weight:800;line-height:1.2;margin-bottom:8px;letter-spacing:-.3px}}
.modal-article-meta{{font-size:11px;color:var(--muted);margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid var(--border)}}
.modal-article-body{{font-size:14px;color:var(--muted2);line-height:1.7;margin-bottom:20px}}
.modal-article-body strong{{color:var(--text);font-weight:600}}
.modal-article-link{{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:var(--orange);background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);padding:8px 16px;border-radius:var(--r2);text-decoration:none;margin-bottom:12px;transition:all .2s}}
.modal-article-link:hover{{background:rgba(249,115,22,.15)}}
.modal-title{{font-family:'Syne',sans-serif;font-size:17px;font-weight:700;color:var(--orange);margin-bottom:14px}}
.modal-field{{margin-bottom:12px}}
.modal-label{{font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:var(--muted);display:block;margin-bottom:5px}}
.modal-input,.modal-select{{width:100%;background:var(--bg);border:1px solid var(--border2);color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;padding:9px 12px;border-radius:var(--r2);outline:none;transition:border .2s}}
.modal-input:focus,.modal-select:focus{{border-color:var(--orange);box-shadow:0 0 0 3px rgba(249,115,22,.1)}}
.calc-result{{background:var(--bg);border:1px solid var(--border);border-radius:var(--r2);padding:13px;margin-top:14px}}
.result-row{{display:flex;justify-content:space-between;font-size:13px;margin-bottom:7px;color:var(--muted)}}
.result-row.total{{color:var(--green);font-weight:700;font-size:15px;border-top:1px solid var(--border);padding-top:9px;margin-top:3px}}
.btn-close{{width:100%;margin-top:8px;background:transparent;color:var(--muted);border:1px solid var(--border);font-family:'DM Sans',sans-serif;font-size:13px;padding:8px;border-radius:var(--r2);cursor:pointer;transition:all .2s}}
.btn-close:hover{{border-color:var(--border2);color:var(--text)}}
footer{{border-top:1px solid var(--border);padding:24px 20px;text-align:center}}
.footer-logo{{font-family:'Syne',sans-serif;font-size:15px;font-weight:800;margin-bottom:6px}}
.footer-logo span{{color:var(--orange)}}
.footer-text{{font-size:11px;color:var(--muted);line-height:1.8}}
</style>
</head>
<body>

<nav>
  <a class="nav-logo" href="#">
    <div class="nav-dot"></div>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 44" height="26" style="display:block">
      <defs><linearGradient id="og" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#f97316"/><stop offset="100%" style="stop-color:#fb923c"/></linearGradient></defs>
      <g transform="translate(20,22)">
        <path d="M0,-14 L2,-10 L-2,-10 Z" fill="url(#og)"/>
        <path d="M9.9,-9.9 L7.5,-6.5 L10.5,-5 Z" fill="url(#og)"/>
        <path d="M14,0 L10,-1.5 L10,1.5 Z" fill="url(#og)"/>
        <path d="M9.9,9.9 L6.5,7.5 L5,10.5 Z" fill="url(#og)"/>
        <path d="M0,14 L2,10 L-2,10 Z" fill="url(#og)"/>
        <path d="M-9.9,9.9 L-7.5,6.5 L-10.5,5 Z" fill="url(#og)"/>
        <path d="M-14,0 L-10,-1.5 L-10,1.5 Z" fill="url(#og)"/>
        <path d="M-9.9,-9.9 L-6.5,-7.5 L-5,-10.5 Z" fill="url(#og)"/>
        <circle cx="0" cy="0" r="10" fill="none" stroke="url(#og)" stroke-width="2.5"/>
        <circle cx="0" cy="0" r="5" fill="#0f0f1a" stroke="url(#og)" stroke-width="1"/>
        <circle cx="0" cy="-1.5" r="2.5" fill="url(#og)"/>
        <path d="M-2,-1.5 Q-2,2 0,5.5 Q2,2 2,-1.5 Z" fill="url(#og)"/>
        <circle cx="0" cy="-1.5" r="1" fill="#0f0f1a"/>
      </g>
      <text x="38" y="30" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="22" fill="#ffffff" letter-spacing="-0.5">Tec</text>
      <text x="80" y="30" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="22" fill="url(#og)" letter-spacing="-0.5">Vagas</text>
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

  </div><!-- /calc-section -->

  <div class="articles-section">
  <div class="sec-hdr"><div class="sec-title">📰 Para Técnicos</div><span class="sec-count">{len(artigos)} artigos</span></div>
  <div class="articles-grid">{cards_artigos}</div>
  </div><!-- /articles-section -->

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
    <div class="result-row"><span>(-) INSS</span><span id="s-b" style="color:#f87171"></span></div>
    <div class="result-row"><span>(-) IRRF</span><span id="s-c" style="color:#f87171"></span></div>
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
    <div class="result-row"><span>(-) INSS + IR</span><span id="f-c" style="color:#f87171"></span></div>
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
    <div class="result-row"><span>(-) INSS + IR</span><span id="d-b" style="color:#f87171"></span></div>
    <div class="result-row total"><span>🎄 13º Líquido</span><span id="d-c"></span></div>
  </div>
  <button class="btn-close" onclick="closeModal('m-dec')">Fechar</button>
</div></div>

<footer>
  <div class="footer-logo">TecVagas</div>
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
document.querySelectorAll('.modal').forEach(m=>m.addEventListener('click',e=>{{if(e.target===m)closeModal(m.id);}})  );
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
function resetF(){{_a='todas';_e='todos';_x='todas';_b='';document.querySelectorAll('.chip').forEach(x=>x.classList.remove('active'));document.querySelector('.chip').classList.add('active');document.getElementById('s-inp').value='';document.querySelectorAll('.f-sel').forEach(s=>s.selectedIndex=0);
  document.querySelector('.page').removeAttribute('data-searching');
  render();
}}
function render(){{let n=0;document.querySelectorAll('#jl .job-card').forEach(c=>{{const ok=(_a==='todas'||c.dataset.area===_a)&&(_e==='todos'||c.dataset.estado===_e)&&(_x==='todas'||c.dataset.esp.includes(_x))&&(_b===''||c.dataset.busca.includes(_b));c.style.display=ok?'block':'none';if(ok)n++;}});document.getElementById('vc').textContent=n+' vagas';document.getElementById('m-vagas').textContent=n;document.getElementById('es').style.display=n===0?'block':'none';document.getElementById('jl').style.display=n===0?'none':'flex';}}

// NEWSLETTER
function newsletter(){{const e=document.getElementById('nl-e').value;if(!e||!e.includes('@')){{alert('Digite um email válido!');return;}}fetch('https://formsubmit.co/ajax/tecvagas@gmail.com',{{method:'POST',headers:{{'Content-Type':'application/json','Accept':'application/json'}},body:JSON.stringify({{email:e,_subject:'Newsletter TecVagas'}})}}).catch(()=>{{}});document.getElementById('nl-ok').style.display='block';document.getElementById('nl-e').value='';}}

// MATEMÁTICA
function IN(b){{const f=[[1518,.075],[2793.88,.09],[4190.83,.12],[8157.41,.14]];let i=0,a=0;for(const[t,q]of f){{if(b<=t){{i+=(b-a)*q;break;}}i+=(t-a)*q;a=t;}}return Math.min(i,908.86);}}
function IR(b,d){{const x=b-d*189.59;const f=[[2259.2,0,0],[2826.65,.075,169.44],[3751.05,.15,381.44],[4664.68,.225,662.77],[1/0,.275,896]];for(const[t,a,e]of f)if(x<=t)return Math.max(0,x*a-e);return 0;}}
function R(v){{return'R$ '+v.toFixed(2).replace('.',',').replace(/\B(?=(\d{{3}})+(?!\d))/g,'.');}}
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

def main():
print(f”\n🤖 TecVagas v10.1 — {datetime.now().strftime(’%d/%m/%Y %H:%M’)}”)
print(”=”*50)
cache=carregar_cache()
vagas_ativas=verificar_cache(cache)
vagas_novas=buscar_gupy()+buscar_vagas_com_br()+buscar_infojobs()
todas=remover_duplicatas(vagas_ativas+vagas_novas)
artigos=carregar_artigos()
print(f”\n📊 {len(todas)} vagas · {len(artigos)} artigos”)
with open(CACHE_FILE,“w”,encoding=“utf-8”) as f:json.dump(todas,f,ensure_ascii=False,indent=2)
with open(“index.html”,“w”,encoding=“utf-8”) as f:f.write(gerar_html(todas,artigos))
print(f”✅ Site atualizado!”)

if **name**==”**main**”:main()
