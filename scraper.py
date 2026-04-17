# “””
TecVagas - Robô de Vagas v10.2

- Design inspirado no Notion (dark hero + light sections)
- Mapa de calor do Brasil por vagas
- Gráfico de áreas mais procuradas
- Todos os 27 estados fixos no filtro
- Detecção de estado corrigida
- Normalização de títulos
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

# Todos os 27 estados ordenados

ESTADOS_LISTA = [
(“AC”,“Acre”),(“AL”,“Alagoas”),(“AP”,“Amapá”),(“AM”,“Amazonas”),
(“BA”,“Bahia”),(“CE”,“Ceará”),(“DF”,“Distrito Federal”),(“ES”,“Espírito Santo”),
(“GO”,“Goiás”),(“MA”,“Maranhão”),(“MT”,“Mato Grosso”),(“MS”,“Mato Grosso do Sul”),
(“MG”,“Minas Gerais”),(“PA”,“Pará”),(“PB”,“Paraíba”),(“PR”,“Paraná”),
(“PE”,“Pernambuco”),(“PI”,“Piauí”),(“RJ”,“Rio de Janeiro”),(“RN”,“Rio Grande do Norte”),
(“RS”,“Rio Grande do Sul”),(“RO”,“Rondônia”),(“RR”,“Roraima”),(“SC”,“Santa Catarina”),
(“SP”,“São Paulo”),(“SE”,“Sergipe”),(“TO”,“Tocantins”),
]
ESTADOS = {s:n for s,n in ESTADOS_LISTA}

# Cidades conhecidas → estado

CIDADES_ESTADO = {
“são paulo”:“SP”,“sp”:“SP”,“campinas”:“SP”,“santos”:“SP”,“sorocaba”:“SP”,
“ribeirão preto”:“SP”,“guarulhos”:“SP”,“são bernardo”:“SP”,“abc”:“SP”,
“rio de janeiro”:“RJ”,“rj”:“RJ”,“niterói”:“RJ”,“duque de caxias”:“RJ”,
“belo horizonte”:“MG”,“mg”:“MG”,“uberlândia”:“MG”,“contagem”:“MG”,“betim”:“MG”,
“curitiba”:“PR”,“pr”:“PR”,“londrina”:“PR”,“maringá”:“PR”,“araucária”:“PR”,
“porto alegre”:“RS”,“rs”:“RS”,“caxias do sul”:“RS”,“canoas”:“RS”,
“florianópolis”:“SC”,“sc”:“SC”,“joinville”:“SC”,“blumenau”:“SC”,“itajaí”:“SC”,
“salvador”:“BA”,“ba”:“BA”,“camaçari”:“BA”,“feira de santana”:“BA”,
“recife”:“PE”,“pe”:“PE”,“caruaru”:“PE”,“suape”:“PE”,
“fortaleza”:“CE”,“ce”:“CE”,“maracanaú”:“CE”,
“manaus”:“AM”,“am”:“AM”,
“belém”:“PA”,“pa”:“PA”,“parauapebas”:“PA”,“marabá”:“PA”,
“goiânia”:“GO”,“go”:“GO”,“anápolis”:“GO”,
“brasília”:“DF”,“df”:“DF”,
“vitória”:“ES”,“es”:“ES”,“vila velha”:“ES”,“serra”:“ES”,“cariacica”:“ES”,
“maceió”:“AL”,“al”:“AL”,
“natal”:“RN”,“rn”:“RN”,
“joão pessoa”:“PB”,“pb”:“PB”,
“teresina”:“PI”,“pi”:“PI”,
“são luís”:“MA”,“ma”:“MA”,
“porto velho”:“RO”,“ro”:“RO”,
“cuiabá”:“MT”,“mt”:“MT”,
“campo grande”:“MS”,“ms”:“MS”,
“macapá”:“AP”,“ap”:“AP”,
“boa vista”:“RR”,“rr”:“RR”,
“palmas”:“TO”,“to”:“TO”,
“aracaju”:“SE”,“se”:“SE”,
“porto seguro”:“BA”,“ilhéus”:“BA”,
“rio grande”:“RS”,“pelotas”:“RS”,
“caxias do sul”:“RS”,“novo hamburgo”:“RS”,
“chapecó”:“SC”,“criciúma”:“SC”,
“são josé dos campos”:“SP”,“são carlos”:“SP”,“piracicaba”:“SP”,
“jundiaí”:“SP”,“taubaté”:“SP”,“bauru”:“SP”,
“americana”:“SP”,“limeira”:“SP”,“indaiatuba”:“SP”,
“macaé”:“RJ”,“campos dos goytacazes”:“RJ”,“volta redonda”:“RJ”,
“juiz de fora”:“MG”,“ipatinga”:“MG”,“montes claros”:“MG”,
“itabira”:“MG”,“sete lagoas”:“MG”,“poços de caldas”:“MG”,
“angra dos reis”:“RJ”,“resende”:“RJ”,
“paulínia”:“SP”,“cubatão”:“SP”,
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

ARTIGOS_PADRAO = [
{“titulo”:“A IA vai acabar com o emprego de técnicos industriais?”,“resumo”:“A inteligência artificial está transformando a indústria, mas os dados mostram que técnicos industriais são dos profissionais mais resistentes à automação.”,“conteudo”:””,“categoria”:“IA & Futuro”,“icone”:“🤖”,“fonte”:“TecVagas”,“url”:”#”,“data”:datetime.now().strftime(”%d/%m/%Y”)},
{“titulo”:“Empregos manuais que a IA nunca vai substituir”,“resumo”:“Especialistas apontam que profissões com trabalho físico complexo e raciocínio situacional são as mais seguras diante da automação.”,“conteudo”:””,“categoria”:“IA & Futuro”,“icone”:“🛡️”,“fonte”:“TecVagas”,“url”:”#”,“data”:datetime.now().strftime(”%d/%m/%Y”)},
{“titulo”:“Quanto ganha um Técnico em Manutenção Elétrica em 2026?”,“resumo”:“Salários variam de R$ 2.800 a R$ 6.500. Certificações como NR10 e NR35 podem aumentar em até 30%.”,“conteudo”:””,“categoria”:“Salários”,“icone”:“⚡”,“fonte”:“TecVagas”,“url”:”#”,“data”:datetime.now().strftime(”%d/%m/%Y”)},
{“titulo”:“NR10: Guia Completo para Técnicos Elétricos em 2026”,“resumo”:“A NR10 é obrigatória para trabalhos com instalações elétricas. Curso básico tem 40 horas e validade de 2 anos.”,“conteudo”:””,“categoria”:“Certificações”,“icone”:“📋”,“fonte”:“TecVagas”,“url”:”#”,“data”:datetime.now().strftime(”%d/%m/%Y”)},
{“titulo”:“O técnico industrial que aprender IA vai ganhar o dobro”,“resumo”:“Profissionais que combinam habilidades técnicas com conhecimento em automação e dados recebem propostas 80% acima da média.”,“conteudo”:””,“categoria”:“IA & Futuro”,“icone”:“🚀”,“fonte”:“TecVagas”,“url”:”#”,“data”:datetime.now().strftime(”%d/%m/%Y”)},
{“titulo”:“Melhores empresas para técnicos industriais em 2026”,“resumo”:“Petrobras, Vale, WEG, Embraer e Bosch oferecem os melhores salários e pacotes de benefícios.”,“conteudo”:””,“categoria”:“Empresas”,“icone”:“🏭”,“fonte”:“TecVagas”,“url”:”#”,“data”:datetime.now().strftime(”%d/%m/%Y”)},
]

def detectar_area(texto):
t=texto.lower()
if any(p in t for p in [“elétric”,“eletric”,“eletrom”,“painel”,“subestac”,“motor”,“gerador”]):return “eletrica”
if any(p in t for p in [“mecatrôn”,“mecatron”,“plc”,“scada”,“robotic”,“automac”,“automaç”,“cnc”,“instrumenta”]):return “automacao”
if any(p in t for p in [“qualidad”,“inspeç”,“metrolog”,“ensaio”,“calibr”]):return “qualidade”
if any(p in t for p in [“seguranç”,“meio ambient”]):return “seguranca”
if any(p in t for p in [“refriger”,“hvac”,“climatiz”,“ar condiciona”]):return “refrigeracao”
return “mecanica”

def detectar_estado(local_str):
“”“Detecta estado de forma robusta a partir de string de localização.”””
if not local_str:
return None
texto = local_str.strip()
texto_lower = texto.lower()

```
# 1. Tenta sigla no final: "Cidade, SP" ou "Cidade - SP"
m = re.search(r'\b([A-Z]{2})\s*$', texto)
if m:
    sigla = m.group(1)
    if sigla in ESTADOS:
        return sigla

# 2. Tenta nome completo do estado
for sigla, nome in ESTADOS.items():
    if nome.lower() in texto_lower:
        return sigla

# 3. Tenta cidade conhecida
for cidade, sigla in CIDADES_ESTADO.items():
    if cidade in texto_lower:
        return sigla

# 4. Tenta sigla sozinha no texto: ", SP," ou "- SP -"
m2 = re.search(r'[,\-\s]([A-Z]{2})[,\-\s]', " " + texto + " ")
if m2:
    sigla = m2.group(1)
    if sigla in ESTADOS:
        return sigla

return None
```

def titulo_valido(titulo):
return not any(p in titulo.lower() for p in PALAVRAS_DESCARTAR)

def normalizar_titulo(titulo):
titulo = re.sub(r’([a-záéíóúàãõâêîôûç])([A-ZÁÉÍÓÚÀÃÕÂÊÎÔÛÇ])’, r’\1 \2’, titulo)
titulo = re.sub(r’([a-zA-ZáéíóúàãõâêîôûçÁÉÍÓÚÀÃÕÂÊÎÔÛÇ])(\d)’, r’\1 \2’, titulo)
titulo = re.sub(r’(\d)([a-zA-ZáéíóúàãõâêîôûçÁÉÍÓÚÀÃÕÂÊÎÔÛÇ])’, r’\1 \2’, titulo)
for sufixo in [‘Jr’,‘Sr’,‘Pleno’,‘Junior’,‘Senior’,‘Sênior’,‘Trainee’,‘Júnior’]:
titulo = re.sub(rf’(?<=[a-záéíóúàãõâêîôûç])({sufixo})\b’, rf’ \1’, titulo)
titulo = re.sub(r’\s*-\s*’, ’ - ‘, titulo)
titulo = re.sub(r’\s+’, ’ ’, titulo)
return titulo.strip()

def icone_benef(b):
bl=b.lower()
for k,v in ICONES_BENEFICIOS.items():
if k in bl:return v
return “✅”

def formatar_conteudo(texto):
if not texto:
return “”
linhas = texto.strip().split(’\n’)
html = ‘’
for linha in linhas:
linha = linha.strip()
if not linha:
html += ‘<div style="height:8px"></div>’
continue
linha = re.sub(r’**(.*?)**’, r’<strong>\1</strong>’, linha)
if any(linha.startswith(x) for x in [’•’,‘✅’,‘❌’,‘🎯’,‘🥇’,‘🥈’,‘🥉’,‘📡’,‘🖥️’,‘📊’,‘🔌’,‘🔧’,‘⚡’,‘❄️’,‘🤖’,‘🔩’,‘🦾’,‘🚀’,‘🛡️’]):
html += f’<p style="margin:4px 0;padding-left:4px;color:#374151">{linha}</p>’
else:
html += f’<p style="margin:8px 0;color:#374151">{linha}</p>’
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
cidade=job.get(“city”,””) or “”
estado_api=job.get(“state”,””) or “”
local_str=f”{cidade}, {estado_api}”.strip(”, “)
estado=detectar_estado(local_str) or detectar_estado(estado_api) or detectar_estado(cidade)
local_display=f”{cidade}, {estado}” if cidade and estado else (cidade or estado or “Brasil”)
benef=[]
for b in job.get(“benefits”,[])[:5]:
if isinstance(b,dict) and b.get(“name”):benef.append(b[“name”][:30])
elif isinstance(b,str):benef.append(b[:30])
vagas.append({
“titulo”:titulo,
“empresa”:job.get(“careerPageName”,“Empresa”)[:50],
“local”:local_display,
“estado”:estado or “BR”,
“url”:job.get(“jobUrl”,”#”),
“fonte”:“gupy.io”,
“data”:datetime.now().strftime(”%d/%m/%Y”),
“area”:detectar_area(titulo),
“beneficios”:benef,
“salario”:“A combinar”,
“escala”:“CLT”,
})
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
local_raw=le.get_text(strip=True)[:60] if le else “”
estado=detectar_estado(local_raw)
local_display=local_raw[:40] if local_raw else “Brasil”
vagas.append({
“titulo”:titulo,
“empresa”:ee.get_text(strip=True)[:50] if ee else “Empresa”,
“local”:local_display,
“estado”:estado or “BR”,
“url”:“https://www.vagas.com.br”+te.get(“href”,””),
“fonte”:“vagas.com.br”,
“data”:datetime.now().strftime(”%d/%m/%Y”),
“area”:detectar_area(titulo),
“beneficios”:[],
“salario”:“A combinar”,
“escala”:“CLT”,
})
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
local_raw=le.get_text(strip=True)[:60] if le else “”
estado=detectar_estado(local_raw)
vagas.append({
“titulo”:titulo,
“empresa”:ee.get_text(strip=True)[:50] if ee else “Empresa”,
“local”:local_raw[:40] if local_raw else “Brasil”,
“estado”:estado or “BR”,
“url”:te.get(“href”,”#”),
“fonte”:“infojobs.com.br”,
“data”:datetime.now().strftime(”%d/%m/%Y”),
“area”:detectar_area(titulo),
“beneficios”:[],
“salario”:“A combinar”,
“escala”:“CLT”,
})
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
# Remigra estado se ainda for BR genérico
if v.get(“estado”) in [“BR”,””] and v.get(“local”):
novo_estado=detectar_estado(v[“local”])
if novo_estado:
v[“estado”]=novo_estado
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
try:
with open(ARTIGOS_FILE,“r”,encoding=“utf-8”) as f:
a=json.load(f)
if a:return a[:6]
except:pass
return ARTIGOS_PADRAO

def calcular_stats(vagas):
“”“Calcula estatísticas para o mapa e gráfico.”””
por_estado={}
por_area={}
for v in vagas:
e=v.get(“estado”,“BR”)
if e and e != “BR”:
por_estado[e]=por_estado.get(e,0)+1
a=v.get(“area”,“mecanica”)
por_area[a]=por_area.get(a,0)+1
return por_estado, por_area

AREA_CONFIG = {
“eletrica”:     {“cls”:“tag-el”,“label”:“Elétrica”,“ico”:“⚡”,“cor”:”#3b82f6”},
“mecanica”:     {“cls”:“tag-me”,“label”:“Mecânica”,“ico”:“🔩”,“cor”:”#22c55e”},
“automacao”:    {“cls”:“tag-au”,“label”:“Automação”,“ico”:“🤖”,“cor”:”#f97316”},
“qualidade”:    {“cls”:“tag-qu”,“label”:“Qualidade”,“ico”:“📊”,“cor”:”#a855f7”},
“seguranca”:    {“cls”:“tag-se”,“label”:“Segurança”,“ico”:“🦺”,“cor”:”#14b8a6”},
“refrigeracao”: {“cls”:“tag-rf”,“label”:“Refrigeração”,“ico”:“❄️”,“cor”:”#60a5fa”},
}

AREA_NOMES = {
“eletrica”:“Elétrica”,“mecanica”:“Mecânica”,“automacao”:“Automação”,
“qualidade”:“Qualidade”,“seguranca”:“Segurança”,“refrigeracao”:“Refrigeração”,
}

def gerar_card_vaga(v, idx=0):
area=v.get(“area”,“mecanica”)
cfg=AREA_CONFIG.get(area,AREA_CONFIG[“mecanica”])
estado=v.get(“estado”,“BR”)
estado_nome=ESTADOS.get(estado,estado) if estado!=“BR” else “Brasil”
salario=v.get(“salario”,“A combinar”)
escala=v.get(“escala”,“CLT”)
benefs=v.get(“beneficios”,[])
benef_html=””
if benefs:
tags=””.join(f’<span class="benef-chip">{icone_benef(b)} {b}</span>’ for b in benefs[:3])
benef_html=f’<div class="card-benefits">{tags}</div>’
wpp=f”https://wa.me/?text=🔧 *{v[‘titulo’]}*%0A🏭 {v[‘empresa’]}%0A📍 {v[‘local’]}%0A%0A👉 {v[‘url’]}%0A%0A_Via TecVagas_”
delay=f”animation-delay:{idx*0.04}s”
local_display = v[‘local’] if v[‘local’] and v[‘local’] != ‘Brasil’ else estado_nome
return f”””<article class="job-card" style="{delay}" data-area="{area}" data-estado="{estado}" data-busca="{v.get('titulo','').lower()} {v.get('empresa','').lower()} {v.get('local','').lower()}">

  <div class="card-inner">
    <div class="card-top">
      <div class="card-left">
        <span class="card-area-badge {cfg['cls']}">{cfg['ico']} {cfg['label']}</span>
        <h3 class="card-title">{v['titulo']}</h3>
        <p class="card-company">{v['empresa']}</p>
      </div>
      <span class="card-link-badge">🔗 Link ativo</span>
    </div>
    <div class="card-chips">
      <span class="chip-info">📍 {local_display}</span>
      <span class="chip-info">💰 {salario}</span>
      <span class="chip-info">📋 {escala}</span>
      <span class="chip-info muted">🗓 {v['data']}</span>
    </div>
    {benef_html}
    <div class="card-footer-actions">
      <a class="btn-wpp" href="{wpp}" target="_blank" onclick="event.stopPropagation()">📲 Compartilhar</a>
      <a class="btn-apply" href="{v['url']}" target="_blank">Ver vaga →</a>
    </div>
  </div>
</article>"""

def gerar_card_artigo(a, idx=0):
has_url = a.get(“url”,”#”) != “#”
conteudo = a.get(“conteudo”,””)
conteudo_html = formatar_conteudo(conteudo) if conteudo else f’<p style="color:#374151">{a.get(“resumo”,””)}</p>’
return f”””<div class="article-row" onclick="openArticle({idx})">

  <div class="article-row-icon">{a['icone']}</div>
  <div class="article-row-body">
    <span class="article-row-cat">{a['categoria']}</span>
    <p class="article-row-title">{a['titulo']}</p>
    <p class="article-row-src">{a.get('fonte','TecVagas')} · {a.get('data','')}</p>
  </div>
  <svg class="article-row-arrow" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
</div>
<div class="modal" id="article-{idx}">
  <div class="modal-box modal-article">
    <div class="modal-art-cat">{a['icone']} {a['categoria']}</div>
    <h2 class="modal-art-title">{a['titulo']}</h2>
    <p class="modal-art-meta">{a.get('fonte','TecVagas')} · {a.get('data','')}</p>
    <div class="modal-art-body">{conteudo_html}</div>
    {'<a class="modal-art-link" href="'+a['url']+'" target="_blank">Ler artigo completo →</a>' if has_url else ''}
    <button class="btn-modal-close" onclick="closeModal(\'article-{idx}\')">Fechar</button>
  </div>
</div>"""

def gerar_mapa_calor(por_estado, total):
“”“Gera mapa SVG simplificado do Brasil com calor por vagas.”””
# Posições aproximadas dos estados no mapa (x%, y%)
POSICOES = {
“AM”:(28,22),“PA”:(42,22),“MT”:(38,42),“BA”:(58,40),“MG”:(55,52),
“SP”:(50,60),“RJ”:(57,60),“RS”:(44,72),“PR”:(47,65),“SC”:(47,69),
“GO”:(47,48),“MS”:(43,55),“PE”:(68,32),“CE”:(67,24),“MA”:(57,22),
“PI”:(61,28),“RN”:(72,26),“PB”:(71,30),“AL”:(70,36),“SE”:(68,39),
“ES”:(61,55),“RO”:(30,35),“AC”:(22,35),“RR”:(32,12),“AP”:(45,12),
“TO”:(50,34),“DF”:(50,47),
}
max_vagas = max(por_estado.values()) if por_estado else 1

```
dots = ""
for sigla, (px, py) in POSICOES.items():
    count = por_estado.get(sigla, 0)
    if count == 0:
        dots += f'<circle cx="{px}%" cy="{py}%" r="5" fill="rgba(255,255,255,0.15)" />'
        dots += f'<text x="{px}%" y="{py+1.2}%" text-anchor="middle" font-size="7" fill="rgba(255,255,255,0.3)">{sigla}</text>'
    else:
        intensity = count / max_vagas
        r = 6 + int(intensity * 14)
        if intensity > 0.7:
            color = "#f97316"
        elif intensity > 0.4:
            color = "#fbbf24"
        else:
            color = "#3b82f6"
        opacity = 0.5 + intensity * 0.5
        dots += f'<circle cx="{px}%" cy="{py}%" r="{r}" fill="{color}" opacity="{opacity:.2f}" />'
        dots += f'<text x="{px}%" y="{py+0.8}%" text-anchor="middle" font-size="8" fill="white" font-weight="bold">{sigla}</text>'
        dots += f'<text x="{px}%" y="{py+2.5}%" text-anchor="middle" font-size="7" fill="rgba(255,255,255,0.8)">{count}</text>'

return f"""<svg viewBox="0 0 100 90" width="100%" style="max-height:280px">
```

  <rect width="100" height="90" fill="transparent"/>
  {dots}
</svg>"""

def gerar_grafico_areas(por_area, total):
“”“Gera gráfico de barras horizontal das áreas.”””
if not por_area or total == 0:
return “<p style='color:#6b7280;font-size:13px'>Aguardando dados…</p>”

```
CORES_AREA = {
    "eletrica":"#3b82f6","mecanica":"#22c55e","automacao":"#f97316",
    "qualidade":"#a855f7","seguranca":"#14b8a6","refrigeracao":"#60a5fa",
}

ordenado = sorted(por_area.items(), key=lambda x: x[1], reverse=True)
max_val = ordenado[0][1] if ordenado else 1
bars = ""
for area, count in ordenado:
    pct = int((count / max_val) * 100)
    cor = CORES_AREA.get(area, "#6b7280")
    nome = AREA_NOMES.get(area, area.title())
    ico = AREA_CONFIG.get(area, {}).get("ico", "")
    bars += f"""<div style="margin-bottom:10px">
```

  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
    <span style="font-size:13px;color:#111827;font-weight:500">{ico} {nome}</span>
    <span style="font-size:12px;color:#6b7280;font-weight:600">{count} vagas</span>
  </div>
  <div style="background:#f3f4f6;border-radius:4px;height:8px;overflow:hidden">
    <div style="width:{pct}%;height:100%;background:{cor};border-radius:4px;transition:width 0.8s ease"></div>
  </div>
</div>"""
    return bars

def gerar_html(vagas, artigos):
agora = datetime.now().strftime(”%d/%m/%Y às %H:%M”)
total = len(vagas)
por_estado, por_area = calcular_stats(vagas)

```
cards_vagas = "\n".join(gerar_card_vaga(v,i) for i,v in enumerate(vagas))
cards_artigos = "\n".join(gerar_card_artigo(a,i) for i,a in enumerate(artigos))
mapa_svg = gerar_mapa_calor(por_estado, total)
grafico_areas = gerar_grafico_areas(por_area, total)

# Filtro: todos os 27 estados fixos
estados_opts = '<option value="todos">Todos os estados</option>'
for sigla, nome in ESTADOS_LISTA:
    count = por_estado.get(sigla, 0)
    label = f"{nome} ({count})" if count > 0 else nome
    estados_opts += f'<option value="{sigla}">{sigla} — {label}</option>'

tec_opts = "".join(
    f'<option value="{t.replace("técnico em","").strip().lower()}">{t.replace("técnico em","").strip().title()}</option>'
    for t in sorted(TECNICOS)
)

return f"""<!DOCTYPE html>
```

<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TecVagas — Vagas para Técnicos Industriais 2026</title>
<meta name="description" content="As melhores vagas para técnicos industriais do Brasil. Elétrica, Mecânica, Automação, Refrigeração, PLC, SCADA, HVAC e mais.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
/* ── RESET ── */
*{{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}}
:root{{
  --dark:#0f1117;
  --dark2:#151821;
  --dark3:#1c2033;
  --orange:#f97316;
  --orange2:#fb923c;
  --blue:#3b82f6;
  --green:#22c55e;
  --white:#ffffff;
  --gray50:#f9fafb;
  --gray100:#f3f4f6;
  --gray200:#e5e7eb;
  --gray400:#9ca3af;
  --gray600:#4b5563;
  --gray700:#374151;
  --gray900:#111827;
  --r:8px;--r2:12px;--r3:16px;
}}
html{{scroll-behavior:smooth}}
body{{background:var(--dark);color:var(--white);font-family:'Inter',sans-serif;font-size:15px;line-height:1.5;overflow-x:hidden}}
::-webkit-scrollbar{{width:4px}}
::-webkit-scrollbar-track{{background:var(--dark)}}
::-webkit-scrollbar-thumb{{background:#333;border-radius:2px}}

/* ── NAV ── */
nav{{
position:sticky;top:0;z-index:200;
background:rgba(15,17,23,0.92);
backdrop-filter:blur(24px);
border-bottom:1px solid rgba(255,255,255,0.06);
padding:0 20px;height:52px;
display:flex;align-items:center;justify-content:space-between;
}}
.nav-brand{{
display:flex;align-items:center;gap:8px;
font-size:15px;font-weight:700;letter-spacing:-.3px;
text-decoration:none;color:var(–white);
}}
.nav-pulse{{
width:7px;height:7px;background:var(–orange);
border-radius:50%;
box-shadow:0 0 0 0 rgba(249,115,22,.4);
animation:navpulse 2s infinite;
}}
@keyframes navpulse{{
0%{{box-shadow:0 0 0 0 rgba(249,115,22,.4)}}
70%{{box-shadow:0 0 0 8px rgba(249,115,22,0)}}
100%{{box-shadow:0 0 0 0 rgba(249,115,22,0)}}
}}
.nav-time{{font-size:12px;color:rgba(255,255,255,.35);font-variant-numeric:tabular-nums}}

/* ── HERO ── */
.hero{{
background:var(–dark);
padding:72px 24px 64px;
position:relative;overflow:hidden;
}}
.hero-noise{{
position:absolute;inset:0;
background-image:url(“data:image/svg+xml,%3Csvg viewBox=‘0 0 256 256’ xmlns=‘http://www.w3.org/2000/svg’%3E%3Cfilter id=‘noise’%3E%3CfeTurbulence type=‘fractalNoise’ baseFrequency=‘0.9’ numOctaves=‘4’ stitchTiles=‘stitch’/%3E%3C/filter%3E%3Crect width=‘100%25’ height=‘100%25’ filter=‘url(%23noise)’ opacity=‘0.03’/%3E%3C/svg%3E”);
pointer-events:none;
}}
.hero-orb{{
position:absolute;top:-80px;left:50%;transform:translateX(-50%);
width:500px;height:500px;
background:radial-gradient(circle,rgba(249,115,22,.08) 0%,rgba(249,115,22,.03) 40%,transparent 70%);
pointer-events:none;
}}
.hero-label{{
display:inline-flex;align-items:center;gap:6px;
font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;
color:rgba(249,115,22,.9);
margin-bottom:24px;
}}
.hero h1{{
font-size:clamp(36px,9vw,68px);
font-weight:800;
line-height:1.04;
letter-spacing:-2.5px;
color:#ffffff;
margin-bottom:20px;
max-width:640px;
}}
.hero h1 .hl{{
background:linear-gradient(90deg,#f97316,#fb923c);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
background-clip:text;
}}
.hero-desc{{
font-size:16px;
color:rgba(255,255,255,.42);
font-weight:400;
max-width:400px;
line-height:1.65;
letter-spacing:-.1px;
}}

/* ── MÉTRICAS ── */
.metrics-bar{{
display:grid;grid-template-columns:repeat(4,1fr);
background:var(–dark2);
border-top:1px solid rgba(255,255,255,.06);
border-bottom:1px solid rgba(255,255,255,.06);
}}
.metric-cell{{
padding:18px 12px;text-align:center;
border-right:1px solid rgba(255,255,255,.06);
position:relative;
}}
.metric-cell:last-child{{border-right:none}}
.metric-cell::after{{
content:’’;position:absolute;bottom:0;left:20%;right:20%;height:2px;
background:var(–orange);opacity:0;border-radius:2px;
transition:opacity .3s;
}}
.metric-cell:hover::after{{opacity:.6}}
.metric-val{{
font-size:24px;font-weight:800;color:var(–orange);
line-height:1;margin-bottom:3px;letter-spacing:-1px;
}}
.metric-lbl{{font-size:10px;color:rgba(255,255,255,.3);font-weight:500;letter-spacing:.5px;text-transform:uppercase}}

/* ── FILTROS ── */
.filters-wrap{{
background:var(–dark2);
border-bottom:1px solid rgba(255,255,255,.06);
padding:14px 20px;
}}
.search-box{{position:relative;margin-bottom:12px}}
.search-box input{{
width:100%;
background:rgba(255,255,255,.05);
border:1px solid rgba(255,255,255,.1);
border-radius:var(–r2);
color:var(–white);
font-family:‘Inter’,sans-serif;font-size:14px;font-weight:400;
padding:11px 16px 11px 44px;
outline:none;
transition:border .2s,box-shadow .2s;
}}
.search-box input::placeholder{{color:rgba(255,255,255,.25)}}
.search-box input:focus{{
border-color:rgba(249,115,22,.5);
box-shadow:0 0 0 3px rgba(249,115,22,.08);
}}
.search-icon{{
position:absolute;left:14px;top:50%;transform:translateY(-50%);
color:rgba(255,255,255,.25);font-size:16px;pointer-events:none;
}}
.f-lbl{{
font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;
color:rgba(255,255,255,.25);margin-bottom:8px;display:block;
}}
.chips-row{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}}
.chip{{
background:rgba(255,255,255,.05);
border:1px solid rgba(255,255,255,.1);
color:rgba(255,255,255,.55);
font-family:‘Inter’,sans-serif;font-size:12px;font-weight:500;
padding:5px 13px;border-radius:20px;
cursor:pointer;transition:all .15s;white-space:nowrap;
}}
.chip:hover{{border-color:rgba(249,115,22,.4);color:var(–orange)}}
.chip.on{{background:rgba(249,115,22,.12);border-color:rgba(249,115,22,.4);color:var(–orange);font-weight:600}}
.f-sel{{
background:rgba(255,255,255,.05);
border:1px solid rgba(255,255,255,.1);
color:var(–white);
font-family:‘Inter’,sans-serif;font-size:12px;
padding:5px 13px;border-radius:20px;
cursor:pointer;outline:none;flex-shrink:0;
max-width:200px;
}}

/* ── TRUST BAR ── */
.trust{{
background:rgba(34,197,94,.04);
border-bottom:1px solid rgba(34,197,94,.1);
padding:7px 20px;
display:flex;align-items:center;gap:8px;
font-size:11px;color:rgba(255,255,255,.35);
}}
.trust-dot{{
width:6px;height:6px;background:var(–green);
border-radius:50%;flex-shrink:0;
animation:trustanim 2s ease-in-out infinite;
}}
@keyframes trustanim{{
0%,100%{{opacity:1;box-shadow:0 0 0 0 rgba(34,197,94,.5)}}
50%{{opacity:.7;box-shadow:0 0 0 5px rgba(34,197,94,0)}}
}}

/* ── SEÇÕES LIGHT ── */
.light-section{{
background:var(–gray50);
padding:32px 20px;
border-bottom:1px solid var(–gray200);
}}
.light-section + .light-section{{border-top:none}}
.section-label{{
font-size:12px;font-weight:600;color:var(–gray400);
letter-spacing:.5px;text-transform:uppercase;margin-bottom:6px;
}}
.section-heading{{
font-size:24px;font-weight:800;color:var(–gray900);
letter-spacing:-1px;line-height:1.1;margin-bottom:20px;
}}

/* ── STATS CARDS ── */
.stats-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.stat-card{{
background:var(–white);
border:1px solid var(–gray200);
border-radius:var(–r2);
padding:16px;
box-shadow:0 1px 3px rgba(0,0,0,.06);
}}
.stat-card-title{{
font-size:12px;font-weight:600;color:var(–gray400);
letter-spacing:.3px;text-transform:uppercase;margin-bottom:12px;
display:flex;align-items:center;gap:6px;
}}
.map-wrap{{
background:var(–dark3);
border-radius:var(–r);
padding:8px;
margin-top:4px;
}}

/* ── CALCULADORAS ── */
.calc-list{{display:flex;flex-direction:column;gap:8px}}
.calc-row{{
background:var(–white);
border:1px solid var(–gray200);
border-radius:var(–r2);
padding:14px 16px;
display:flex;align-items:center;gap:12px;
cursor:pointer;transition:all .15s;
box-shadow:0 1px 2px rgba(0,0,0,.04);
}}
.calc-row:hover{{
border-color:var(–gray400);
box-shadow:0 2px 8px rgba(0,0,0,.08);
transform:translateY(-1px);
}}
.calc-row-icon{{font-size:20px;flex-shrink:0}}
.calc-row-name{{font-size:14px;font-weight:600;color:var(–gray900)}}
.calc-row-hint{{font-size:11px;color:var(–gray400);margin-top:1px}}
.calc-row-arrow{{margin-left:auto;color:var(–gray400)}}

/* ── ARTIGOS ── */
.article-row{{
background:var(–white);
border:1px solid var(–gray200);
border-radius:var(–r2);
padding:14px 16px;
display:flex;align-items:center;gap:12px;
cursor:pointer;transition:all .15s;
box-shadow:0 1px 2px rgba(0,0,0,.04);
margin-bottom:8px;
text-decoration:none;color:var(–gray900);
}}
.article-row:hover{{
border-color:var(–gray400);
box-shadow:0 2px 8px rgba(0,0,0,.08);
transform:translateY(-1px);
}}
.article-row-icon{{font-size:22px;flex-shrink:0}}
.article-row-body{{flex:1;min-width:0}}
.article-row-cat{{
font-size:10px;font-weight:600;color:var(–orange);
letter-spacing:1px;text-transform:uppercase;margin-bottom:3px;
display:block;
}}
.article-row-title{{font-size:14px;font-weight:600;color:var(–gray900);line-height:1.35;margin-bottom:2px}}
.article-row-src{{font-size:11px;color:var(–gray400)}}
.article-row-arrow{{color:var(–gray400);flex-shrink:0}}

/* ── NEWSLETTER ── */
.newsletter-wrap{{
background:var(–dark);
padding:32px 20px;
border-top:1px solid rgba(255,255,255,.06);
}}
.nl-eyebrow{{
font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;
color:var(–orange);margin-bottom:8px;
}}
.nl-heading{{
font-size:22px;font-weight:800;letter-spacing:-.5px;
color:var(–white);margin-bottom:6px;
}}
.nl-desc{{font-size:13px;color:rgba(255,255,255,.4);margin-bottom:16px}}
.nl-form{{display:flex;gap:8px;flex-wrap:wrap}}
.nl-input{{
flex:1;min-width:180px;
background:rgba(255,255,255,.06);
border:1px solid rgba(255,255,255,.12);
color:var(–white);font-family:‘Inter’,sans-serif;font-size:14px;
padding:11px 14px;border-radius:var(–r2);outline:none;
transition:border .2s;
}}
.nl-input:focus{{border-color:rgba(249,115,22,.5)}}
.nl-btn{{
background:var(–orange);color:white;border:none;
font-family:‘Inter’,sans-serif;font-size:13px;font-weight:600;
padding:11px 20px;border-radius:var(–r2);cursor:pointer;
white-space:nowrap;transition:background .2s;
}}
.nl-btn:hover{{background:#ea6c0a}}
.nl-ok{{display:none;color:var(–green);font-size:13px;margin-top:8px;font-weight:500}}

/* ── VAGAS ── */
.jobs-section{{
background:var(–gray50);
padding:32px 20px 48px;
}}
.jobs-header{{
display:flex;align-items:center;justify-content:space-between;
margin-bottom:16px;
}}
.jobs-heading{{
font-size:22px;font-weight:800;color:var(–gray900);letter-spacing:-.5px;
}}
.jobs-count{{
font-size:12px;color:var(–gray400);
background:var(–white);border:1px solid var(–gray200);
padding:4px 12px;border-radius:20px;
}}
.jobs-list{{display:flex;flex-direction:column;gap:10px}}
.job-card{{
background:var(–white);
border:1px solid var(–gray200);
border-radius:var(–r2);
box-shadow:0 1px 3px rgba(0,0,0,.06);
transition:all .2s;
animation:rise .35s ease both;
overflow:hidden;
}}
@keyframes rise{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:translateY(0)}}}}
.job-card:hover{{
border-color:var(–gray400);
box-shadow:0 4px 16px rgba(0,0,0,.1);
transform:translateY(-2px);
}}
.card-inner{{padding:16px}}
.card-top{{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:10px}}
.card-left{{flex:1;min-width:0}}
.card-area-badge{{
display:inline-flex;align-items:center;gap:4px;
font-size:10px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;
padding:2px 9px;border-radius:20px;margin-bottom:6px;
}}
.tag-el{{background:rgba(59,130,246,.1);color:#2563eb;border:1px solid rgba(59,130,246,.2)}}
.tag-me{{background:rgba(34,197,94,.1);color:#16a34a;border:1px solid rgba(34,197,94,.2)}}
.tag-au{{background:rgba(249,115,22,.1);color:#ea580c;border:1px solid rgba(249,115,22,.2)}}
.tag-qu{{background:rgba(168,85,247,.1);color:#9333ea;border:1px solid rgba(168,85,247,.2)}}
.tag-se{{background:rgba(20,184,166,.1);color:#0d9488;border:1px solid rgba(20,184,166,.2)}}
.tag-rf{{background:rgba(59,130,246,.1);color:#1d4ed8;border:1px solid rgba(59,130,246,.15)}}
.card-title{{font-size:15px;font-weight:700;color:var(–gray900);line-height:1.3;margin-bottom:3px;letter-spacing:-.2px}}
.card-company{{font-size:12px;color:var(–gray400);font-weight:400}}
.card-link-badge{{
flex-shrink:0;font-size:10px;font-weight:600;
color:#16a34a;background:rgba(34,197,94,.08);
border:1px solid rgba(34,197,94,.2);
padding:2px 8px;border-radius:20px;white-space:nowrap;
}}
.card-chips{{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px}}
.chip-info{{
font-size:11px;color:var(–gray600);
background:var(–gray100);border:1px solid var(–gray200);
padding:2px 8px;border-radius:var(–r);
}}
.chip-info.muted{{color:var(–gray400)}}
.card-benefits{{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px}}
.benef-chip{{
font-size:10px;color:#92400e;
background:#fef3c7;border:1px solid #fde68a;
padding:2px 7px;border-radius:var(–r);
}}
.card-footer-actions{{
display:flex;gap:8px;
padding-top:10px;border-top:1px solid var(–gray100);
}}
.btn-wpp{{
display:inline-flex;align-items:center;gap:5px;
font-size:12px;font-weight:500;
color:#16a34a;background:rgba(34,197,94,.06);
border:1px solid rgba(34,197,94,.2);
padding:7px 14px;border-radius:var(–r2);
text-decoration:none;transition:all .2s;
}}
.btn-wpp:hover{{background:rgba(34,197,94,.12)}}
.btn-apply{{
display:inline-flex;align-items:center;gap:5px;
font-size:12px;font-weight:600;
color:white;background:var(–gray900);
padding:7px 16px;border-radius:var(–r2);
text-decoration:none;transition:all .2s;margin-left:auto;
}}
.btn-apply:hover{{background:var(–gray700)}}

/* ── EMPTY STATE ── */
.empty{{text-align:center;padding:48px 20px;display:none;background:var(–gray50)}}
.empty-ico{{font-size:40px;margin-bottom:12px;opacity:.4}}
.empty-title{{font-size:18px;font-weight:700;color:var(–gray900);margin-bottom:6px}}
.empty-text{{font-size:13px;color:var(–gray400);line-height:1.6;margin-bottom:16px}}
.empty-reset{{
display:inline-flex;align-items:center;gap:6px;
font-size:13px;font-weight:600;color:var(–orange);
background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);
padding:8px 18px;border-radius:20px;cursor:pointer;transition:all .2s;
}}
.empty-reset:hover{{background:rgba(249,115,22,.15)}}

/* ── MODAIS ── */
.modal{{
display:none;position:fixed;inset:0;
background:rgba(0,0,0,.7);z-index:500;
align-items:center;justify-content:center;
padding:16px;backdrop-filter:blur(6px);
overflow-y:auto;
}}
.modal.open{{display:flex}}
.modal-box{{
background:var(–white);
border-radius:var(–r3);
padding:24px;width:100%;max-width:420px;margin:auto;
position:relative;
box-shadow:0 24px 60px rgba(0,0,0,.3);
}}
.modal-article{{max-width:560px;max-height:88vh;overflow-y:auto}}
.modal-art-cat{{font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(–orange);margin-bottom:10px}}
.modal-art-title{{font-size:20px;font-weight:800;color:var(–gray900);line-height:1.2;margin-bottom:8px;letter-spacing:-.5px}}
.modal-art-meta{{font-size:11px;color:var(–gray400);margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid var(–gray200)}}
.modal-art-body{{font-size:14px;line-height:1.7;margin-bottom:20px}}
.modal-art-link{{
display:inline-flex;align-items:center;gap:6px;
font-size:13px;font-weight:600;color:var(–orange);
background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);
padding:8px 16px;border-radius:var(–r2);text-decoration:none;
margin-bottom:12px;transition:all .2s;
}}
.modal-art-link:hover{{background:rgba(249,115,22,.15)}}
.modal-title{{font-size:16px;font-weight:700;color:var(–gray900);margin-bottom:14px}}
.modal-field{{margin-bottom:12px}}
.modal-label{{font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:var(–gray400);display:block;margin-bottom:5px}}
.modal-input,.modal-select{{
width:100%;background:var(–gray50);border:1px solid var(–gray200);
color:var(–gray900);font-family:‘Inter’,sans-serif;font-size:14px;
padding:10px 12px;border-radius:var(–r2);outline:none;
transition:border .2s;
}}
.modal-input:focus,.modal-select:focus{{border-color:var(–orange);box-shadow:0 0 0 3px rgba(249,115,22,.08)}}
.calc-result{{background:var(–gray50);border:1px solid var(–gray200);border-radius:var(–r2);padding:14px;margin-top:14px}}
.result-row{{display:flex;justify-content:space-between;font-size:13px;margin-bottom:7px;color:var(–gray600)}}
.result-row.total{{color:#16a34a;font-weight:700;font-size:15px;border-top:1px solid var(–gray200);padding-top:9px;margin-top:3px}}
.btn-modal-close{{
width:100%;margin-top:8px;
background:transparent;color:var(–gray400);
border:1px solid var(–gray200);
font-family:‘Inter’,sans-serif;font-size:13px;
padding:9px;border-radius:var(–r2);cursor:pointer;transition:all .2s;
}}
.btn-modal-close:hover{{border-color:var(–gray400);color:var(–gray700)}}

/* ── FOOTER ── */
footer{{
background:var(–dark);
border-top:1px solid rgba(255,255,255,.06);
padding:28px 20px;text-align:center;
}}
.footer-brand{{font-size:15px;font-weight:700;letter-spacing:-.3px;margin-bottom:6px}}
.footer-brand span{{color:var(–orange)}}
.footer-text{{font-size:11px;color:rgba(255,255,255,.25);line-height:1.8}}

/* ── SEARCH MODE ── */
.page[data-searching] .calc-section,
.page[data-searching] .articles-section,
.page[data-searching] .newsletter-wrap,
.page[data-searching] .stats-section{{display:none!important}}
</style>

</head>
<body>

<!-- NAV -->

<nav>
  <a class="nav-brand" href="#">
    <div class="nav-pulse"></div>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 44" height="28" style="display:block">
      <defs>
        <linearGradient id="og" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#f97316"/>
          <stop offset="100%" style="stop-color:#fb923c"/>
        </linearGradient>
      </defs>
      <!-- Engrenagem -->
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
      <!-- Tec -->
      <text x="38" y="30" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="22" fill="#ffffff" letter-spacing="-0.5">Tec</text>
      <!-- Vagas -->
      <text x="80" y="30" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="22" fill="url(#og)" letter-spacing="-0.5">Vagas</text>
    </svg>
  </a>
  <span class="nav-time" id="nav-clock"></span>
</nav>

<!-- HERO -->

<section class="hero">
  <div class="hero-noise"></div>
  <div class="hero-orb"></div>
  <div class="hero-label">🇧🇷 Vagas técnicas industriais · 2026</div>
  <h1>As melhores vagas para <span class="hl">técnicos industriais</span> do Brasil.</h1>
  <p class="hero-desc">Elétrica · Mecânica · Automação · Refrigeração · PLC · SCADA · HVAC. Atualizado 5× por dia.</p>
</section>

<!-- MÉTRICAS -->

<div class="metrics-bar">
  <div class="metric-cell"><div class="metric-val" id="m-total">{total}</div><div class="metric-lbl">Vagas ativas</div></div>
  <div class="metric-cell"><div class="metric-val">60+</div><div class="metric-lbl">Especialidades</div></div>
  <div class="metric-cell"><div class="metric-val">5×</div><div class="metric-lbl">Por dia</div></div>
  <div class="metric-cell"><div class="metric-val">27</div><div class="metric-lbl">Estados</div></div>
</div>

<!-- FILTROS -->

<div class="filters-wrap">
  <div class="search-box">
    <span class="search-icon">🔍</span>
    <input type="text" id="s-inp" placeholder="Buscar por cargo, empresa ou cidade..." oninput="doSearch(this.value)">
  </div>
  <span class="f-lbl">Área técnica</span>
  <div class="chips-row">
    <button class="chip on" onclick="fArea('todas',this)">Todas</button>
    <button class="chip" onclick="fArea('eletrica',this)">⚡ Elétrica</button>
    <button class="chip" onclick="fArea('mecanica',this)">🔩 Mecânica</button>
    <button class="chip" onclick="fArea('automacao',this)">🤖 Automação</button>
    <button class="chip" onclick="fArea('refrigeracao',this)">❄️ Refrigeração</button>
    <button class="chip" onclick="fArea('qualidade',this)">📊 Qualidade</button>
    <button class="chip" onclick="fArea('seguranca',this)">🦺 Segurança</button>
  </div>
  <span class="f-lbl">Estado</span>
  <div class="chips-row">
    <select class="f-sel" onchange="fEstado(this.value)">{estados_opts}</select>
  </div>
</div>

<!-- TRUST -->

<div class="trust">
  <div class="trust-dot"></div>
  Vagas com link ativo · Apenas 2026 · Encerradas removidas automaticamente · {agora}
</div>

<!-- PÁGINA -->

<div class="page" id="page">

  <!-- STATS -->

  <div class="stats-section light-section">
    <div class="section-label">Panorama do mercado</div>
    <div class="section-heading">Onde estão as vagas.</div>
    <div class="stats-grid">
      <div class="stat-card" style="grid-column:1/-1">
        <div class="stat-card-title">🗺️ Vagas por estado</div>
        <div class="map-wrap">{mapa_svg}</div>
        <div style="display:flex;gap:12px;margin-top:10px;flex-wrap:wrap">
          <span style="font-size:11px;color:#6b7280;display:flex;align-items:center;gap:4px"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#f97316"></span> Alta demanda</span>
          <span style="font-size:11px;color:#6b7280;display:flex;align-items:center;gap:4px"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#fbbf24"></span> Média demanda</span>
          <span style="font-size:11px;color:#6b7280;display:flex;align-items:center;gap:4px"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#3b82f6"></span> Baixa demanda</span>
        </div>
      </div>
      <div class="stat-card" style="grid-column:1/-1">
        <div class="stat-card-title">📊 Áreas mais demandadas</div>
        {grafico_areas}
      </div>
    </div>
  </div>

  <!-- CALCULADORAS -->

  <div class="calc-section light-section">
    <div class="section-label">Ferramentas</div>
    <div class="section-heading">Calculadoras trabalhistas.</div>
    <div class="calc-list">
      <div class="calc-row" onclick="openModal('m-sal')"><div class="calc-row-icon">💰</div><div><div class="calc-row-name">Salário Líquido</div><div class="calc-row-hint">INSS + IRRF 2026</div></div><svg class="calc-row-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
      <div class="calc-row" onclick="openModal('m-fer')"><div class="calc-row-icon">🏖️</div><div><div class="calc-row-name">Férias</div><div class="calc-row-hint">+ 1/3 constitucional</div></div><svg class="calc-row-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
      <div class="calc-row" onclick="openModal('m-res')"><div class="calc-row-icon">📦</div><div><div class="calc-row-name">Rescisão</div><div class="calc-row-hint">Demissão ou pedido</div></div><svg class="calc-row-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
      <div class="calc-row" onclick="openModal('m-he')"><div class="calc-row-icon">⏰</div><div><div class="calc-row-name">Hora Extra</div><div class="calc-row-hint">50%, 100% e noturna</div></div><svg class="calc-row-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
      <div class="calc-row" onclick="openModal('m-not')"><div class="calc-row-icon">🌙</div><div><div class="calc-row-name">Adicional Noturno</div><div class="calc-row-hint">20% sobre salário</div></div><svg class="calc-row-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
      <div class="calc-row" onclick="openModal('m-ins')"><div class="calc-row-icon">⚠️</div><div><div class="calc-row-name">Insalubridade</div><div class="calc-row-hint">e Periculosidade</div></div><svg class="calc-row-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
      <div class="calc-row" onclick="openModal('m-dec')"><div class="calc-row-icon">🎄</div><div><div class="calc-row-name">13º Salário</div><div class="calc-row-hint">Proporcional ou cheio</div></div><svg class="calc-row-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
    </div>
  </div>

  <!-- ARTIGOS -->

  <div class="articles-section light-section">
    <div class="section-label">Para técnicos</div>
    <div class="section-heading">Carreira & mercado.</div>
    {cards_artigos}
  </div>

  <!-- NEWSLETTER -->

  <div class="newsletter-wrap">
    <div class="nl-eyebrow">📧 Newsletter gratuita</div>
    <div class="nl-heading">Vagas toda semana<br>no seu email.</div>
    <div class="nl-desc">As melhores vagas técnicas direto na caixa de entrada. Grátis.</div>
    <div class="nl-form">
      <input class="nl-input" type="email" id="nl-e" placeholder="seu@email.com">
      <button class="nl-btn" onclick="newsletter()">Quero receber</button>
    </div>
    <div class="nl-ok" id="nl-ok">✓ Cadastrado! Você receberá as vagas em breve.</div>
  </div>

  <!-- VAGAS -->

  <div class="jobs-section" id="vagas">
    <div class="jobs-header">
      <div class="jobs-heading">Vagas disponíveis.</div>
      <span class="jobs-count" id="jobs-count">{total} vagas</span>
    </div>
    <div class="jobs-list" id="jl">{cards_vagas}</div>
    <div class="empty" id="es">
      <div class="empty-ico">🔍</div>
      <div class="empty-title">Nenhuma vaga encontrada</div>
      <div class="empty-text">Tente outra área, estado ou termo de busca.<br>Atualizamos 5× por dia com novas vagas.</div>
      <button class="empty-reset" onclick="resetAll()">← Ver todas as vagas</button>
    </div>
  </div>

</div><!-- /page -->

<!-- MODAIS CALCULADORAS -->

<div class="modal" id="m-sal"><div class="modal-box">
  <div class="modal-title">💰 Salário Líquido</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="s1" placeholder="Ex: 3500" oninput="cS()"></div>
  <div class="modal-field"><label class="modal-label">Dependentes para IR</label><input class="modal-input" type="number" id="s2" value="0" oninput="cS()"></div>
  <div class="calc-result" id="s-r" style="display:none">
    <div class="result-row"><span>Salário Bruto</span><span id="s-a"></span></div>
    <div class="result-row"><span>(-) INSS</span><span id="s-b" style="color:#dc2626"></span></div>
    <div class="result-row"><span>(-) IRRF</span><span id="s-c" style="color:#dc2626"></span></div>
    <div class="result-row total"><span>💵 Salário Líquido</span><span id="s-d"></span></div>
    <div class="result-row" style="font-size:11px;margin-top:3px"><span>FGTS (empregador)</span><span id="s-e" style="color:#16a34a"></span></div>
  </div>
  <button class="btn-modal-close" onclick="closeModal('m-sal')">Fechar</button>
</div></div>

<div class="modal" id="m-fer"><div class="modal-box">
  <div class="modal-title">🏖️ Férias</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="f1" placeholder="Ex: 3500" oninput="cF()"></div>
  <div class="modal-field"><label class="modal-label">Meses trabalhados</label><input class="modal-input" type="number" id="f2" value="12" min="1" max="12" oninput="cF()"></div>
  <div class="calc-result" id="f-r" style="display:none">
    <div class="result-row"><span>Férias proporcional</span><span id="f-a"></span></div>
    <div class="result-row"><span>(+) 1/3 constitucional</span><span id="f-b" style="color:#16a34a"></span></div>
    <div class="result-row"><span>(-) INSS + IR</span><span id="f-c" style="color:#dc2626"></span></div>
    <div class="result-row total"><span>🏖️ Férias Líquidas</span><span id="f-d"></span></div>
  </div>
  <button class="btn-modal-close" onclick="closeModal('m-fer')">Fechar</button>
</div></div>

<div class="modal" id="m-res"><div class="modal-box">
  <div class="modal-title">📦 Rescisão</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="r1" placeholder="Ex: 3500" oninput="cR()"></div>
  <div class="modal-field"><label class="modal-label">Meses trabalhados no ano</label><input class="modal-input" type="number" id="r2" placeholder="Ex: 6" min="1" max="12" oninput="cR()"></div>
  <div class="modal-field"><label class="modal-label">Tipo de rescisão</label>
    <select class="modal-select" id="r3" onchange="cR()">
      <option value="sj">Demissão sem justa causa</option>
      <option value="pd">Pedido de demissão</option>
      <option value="ac">Acordo (distrato)</option>
    </select>
  </div>
  <div class="calc-result" id="r-r" style="display:none">
    <div class="result-row"><span>Saldo de salário</span><span id="r-a"></span></div>
    <div class="result-row"><span>13º proporcional</span><span id="r-b"></span></div>
    <div class="result-row"><span>Férias + 1/3</span><span id="r-c"></span></div>
    <div class="result-row" id="r-ml" style="display:none"><span>Multa FGTS</span><span id="r-d" style="color:#16a34a"></span></div>
    <div class="result-row total"><span>📦 Total Rescisão</span><span id="r-e"></span></div>
  </div>
  <button class="btn-modal-close" onclick="closeModal('m-res')">Fechar</button>
</div></div>

<div class="modal" id="m-he"><div class="modal-box">
  <div class="modal-title">⏰ Hora Extra</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="h1" placeholder="Ex: 3500" oninput="cHE()"></div>
  <div class="modal-field"><label class="modal-label">Horas extras</label><input class="modal-input" type="number" id="h2" placeholder="Ex: 10" oninput="cHE()"></div>
  <div class="modal-field"><label class="modal-label">Tipo</label>
    <select class="modal-select" id="h3" onchange="cHE()">
      <option value="50">50% — Dias úteis</option>
      <option value="100">100% — Dom/Feriados</option>
      <option value="70">70% — Noturna</option>
    </select>
  </div>
  <div class="calc-result" id="h-r" style="display:none">
    <div class="result-row"><span>Valor hora normal</span><span id="h-a"></span></div>
    <div class="result-row"><span>Valor hora extra</span><span id="h-b"></span></div>
    <div class="result-row total"><span>⏰ Total a receber</span><span id="h-c"></span></div>
  </div>
  <button class="btn-modal-close" onclick="closeModal('m-he')">Fechar</button>
</div></div>

<div class="modal" id="m-not"><div class="modal-box">
  <div class="modal-title">🌙 Adicional Noturno</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="n1" placeholder="Ex: 3500" oninput="cN()"></div>
  <div class="modal-field"><label class="modal-label">Horas noturnas por mês</label><input class="modal-input" type="number" id="n2" placeholder="Ex: 44" oninput="cN()"></div>
  <div class="calc-result" id="n-r" style="display:none">
    <div class="result-row"><span>Salário base</span><span id="n-a"></span></div>
    <div class="result-row"><span>(+) Adicional 20%</span><span id="n-b" style="color:#16a34a"></span></div>
    <div class="result-row total"><span>🌙 Total com adicional</span><span id="n-c"></span></div>
  </div>
  <button class="btn-modal-close" onclick="closeModal('m-not')">Fechar</button>
</div></div>

<div class="modal" id="m-ins"><div class="modal-box">
  <div class="modal-title">⚠️ Insalubridade</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="i1" placeholder="Ex: 3500" oninput="cI()"></div>
  <div class="modal-field"><label class="modal-label">Tipo de adicional</label>
    <select class="modal-select" id="i2" onchange="cI()">
      <option value="10">Insalubridade Mínima 10% SM</option>
      <option value="20">Insalubridade Média 20% SM</option>
      <option value="40">Insalubridade Máxima 40% SM</option>
      <option value="30p">Periculosidade 30% salário</option>
    </select>
  </div>
  <div class="calc-result" id="i-r" style="display:none">
    <div class="result-row"><span>Salário base</span><span id="i-a"></span></div>
    <div class="result-row"><span>(+) Adicional</span><span id="i-b" style="color:#16a34a"></span></div>
    <div class="result-row total"><span>⚠️ Total</span><span id="i-c"></span></div>
    <div class="result-row" style="font-size:10px;margin-top:3px;color:#9ca3af"><span>Salário mínimo 2026: R$ 1.518,00</span><span></span></div>
  </div>
  <button class="btn-modal-close" onclick="closeModal('m-ins')">Fechar</button>
</div></div>

<div class="modal" id="m-dec"><div class="modal-box">
  <div class="modal-title">🎄 13º Salário</div>
  <div class="modal-field"><label class="modal-label">Salário Bruto (R$)</label><input class="modal-input" type="number" id="d1" placeholder="Ex: 3500" oninput="cD()"></div>
  <div class="modal-field"><label class="modal-label">Meses trabalhados</label><input class="modal-input" type="number" id="d2" value="12" min="1" max="12" oninput="cD()"></div>
  <div class="calc-result" id="d-r" style="display:none">
    <div class="result-row"><span>13º bruto proporcional</span><span id="d-a"></span></div>
    <div class="result-row"><span>(-) INSS + IR</span><span id="d-b" style="color:#dc2626"></span></div>
    <div class="result-row total"><span>🎄 13º Líquido</span><span id="d-c"></span></div>
  </div>
  <button class="btn-modal-close" onclick="closeModal('m-dec')">Fechar</button>
</div></div>

<footer>
  <div class="footer-brand" style="margin-bottom:8px">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 44" height="30" style="display:inline-block">
      <defs><linearGradient id="og2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#f97316"/><stop offset="100%" style="stop-color:#fb923c"/></linearGradient></defs>
      <g transform="translate(20,22)">
        <path d="M0,-14 L2,-10 L-2,-10 Z" fill="url(#og2)"/>
        <path d="M9.9,-9.9 L7.5,-6.5 L10.5,-5 Z" fill="url(#og2)"/>
        <path d="M14,0 L10,-1.5 L10,1.5 Z" fill="url(#og2)"/>
        <path d="M9.9,9.9 L6.5,7.5 L5,10.5 Z" fill="url(#og2)"/>
        <path d="M0,14 L2,10 L-2,10 Z" fill="url(#og2)"/>
        <path d="M-9.9,9.9 L-7.5,6.5 L-10.5,5 Z" fill="url(#og2)"/>
        <path d="M-14,0 L-10,-1.5 L-10,1.5 Z" fill="url(#og2)"/>
        <path d="M-9.9,-9.9 L-6.5,-7.5 L-5,-10.5 Z" fill="url(#og2)"/>
        <circle cx="0" cy="0" r="10" fill="none" stroke="url(#og2)" stroke-width="2.5"/>
        <circle cx="0" cy="0" r="5" fill="#0f0f1a" stroke="url(#og2)" stroke-width="1"/>
        <circle cx="0" cy="-1.5" r="2.5" fill="url(#og2)"/>
        <path d="M-2,-1.5 Q-2,2 0,5.5 Q2,2 2,-1.5 Z" fill="url(#og2)"/>
        <circle cx="0" cy="-1.5" r="1" fill="#0f0f1a"/>
      </g>
      <text x="38" y="30" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="22" fill="#ffffff" letter-spacing="-0.5">Tec</text>
      <text x="80" y="30" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="22" fill="url(#og2)" letter-spacing="-0.5">Vagas</text>
    </svg>
  </div>
  <div class="footer-text">
    Vagas técnicas industriais com link ativo · Apenas 2026 · Todo o Brasil<br>
    Atualizado automaticamente 5× por dia · Links redirecionam para os sites originais
  </div>
</footer>

<script data-goatcounter="https://tecvagas.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>

<script>
// RELÓGIO
(function(){{
  const el=document.getElementById('nav-clock');
  function t(){{el.textContent=new Date().toLocaleTimeString('pt-BR',{{timeZone:'America/Sao_Paulo',hour:'2-digit',minute:'2-digit'}});}}
  t();setInterval(t,1000);
}})();

// MODAIS
function openModal(id){{document.getElementById(id).classList.add('open');document.body.style.overflow='hidden';}}
function closeModal(id){{document.getElementById(id).classList.remove('open');document.body.style.overflow='';}}
function openArticle(i){{openModal('article-'+i);}}
document.querySelectorAll('.modal').forEach(m=>m.addEventListener('click',e=>{{if(e.target===m)closeModal(m.id);}})  );
document.addEventListener('keydown',e=>{{if(e.key==='Escape')document.querySelectorAll('.modal.open').forEach(m=>closeModal(m.id));}});

// FILTROS
let _a='todas',_e='todos',_b='';
const page=document.getElementById('page');

function fArea(a,btn){{
  _a=a;
  document.querySelectorAll('.chip').forEach(x=>x.classList.remove('on'));
  btn.classList.add('on');
  render();
}}
function fEstado(v){{_e=v;render();}}
function doSearch(v){{
  _b=v.toLowerCase().trim();
  page.toggleAttribute('data-searching',_b.length>0);
  if(_b.length>0) document.getElementById('vagas').scrollIntoView({{behavior:'smooth',block:'start'}});
  render();
}}
function resetAll(){{
  _a='todas';_e='todos';_b='';
  document.getElementById('s-inp').value='';
  document.querySelectorAll('.chip').forEach(x=>x.classList.remove('on'));
  document.querySelector('.chip').classList.add('on');
  document.querySelectorAll('.f-sel').forEach(s=>s.selectedIndex=0);
  page.removeAttribute('data-searching');
  render();
}}
function render(){{
  let n=0;
  document.querySelectorAll('#jl .job-card').forEach(c=>{{
    const ok=
      (_a==='todas'||c.dataset.area===_a)&&
      (_e==='todos'||c.dataset.estado===_e)&&
      (_b===''||c.dataset.busca.includes(_b));
    c.style.display=ok?'block':'none';
    if(ok)n++;
  }});
  document.getElementById('jobs-count').textContent=n+' vagas';
  document.getElementById('m-total').textContent=n;
  document.getElementById('es').style.display=n===0?'block':'none';
  document.getElementById('jl').style.display=n===0?'none':'flex';
}}

// NEWSLETTER
function newsletter(){{
  const e=document.getElementById('nl-e').value;
  if(!e||!e.includes('@')){{alert('Digite um email válido!');return;}}
  fetch('https://formsubmit.co/ajax/tecvagas@gmail.com',{{
    method:'POST',
    headers:{{'Content-Type':'application/json','Accept':'application/json'}},
    body:JSON.stringify({{email:e,_subject:'Newsletter TecVagas'}})
  }}).catch(()=>{{}});
  document.getElementById('nl-ok').style.display='block';
  document.getElementById('nl-e').value='';
}}

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
print(f”\n🤖 TecVagas v10.2 — {datetime.now().strftime(’%d/%m/%Y %H:%M’)}”)
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
