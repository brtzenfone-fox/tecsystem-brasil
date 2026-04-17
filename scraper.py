“””
TecVagas - Robô de Vagas v11
Design LIGHT (branco/claro) - Manrope + Inter
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
“tecnico em manutencao eletrica”,“tecnico em eletrica industrial”,
“tecnico em eletrotecnica”,“tecnico em eletromecanica”,
“tecnico em eletronica industrial”,“tecnico em paineis eletricos”,
“tecnico em comando eletrico”,“tecnico em motores eletricos”,
“tecnico em subestacoes eletricas”,“tecnico em geradores”,
“tecnico em manutencao mecanica”,“tecnico em mecanica industrial”,
“tecnico em hidraulica industrial”,“tecnico em pneumatica industrial”,
“tecnico em bombas industriais”,“tecnico em compressores industriais”,
“tecnico em valvulas industriais”,“tecnico em lubrificacao industrial”,
“tecnico em soldagem industrial”,“tecnico em caldeiraria”,
“tecnico em tubulacao industrial”,“tecnico em usinagem”,“tecnico em CNC”,
“tecnico em mecatronica”,“tecnico em manutencao eletromecanica”,
“tecnico em manutencao industrial”,“tecnico em automacao industrial”,
“tecnico em PLC”,“tecnico em SCADA”,“tecnico em robotica industrial”,
“tecnico em instrumentacao industrial”,“tecnico em redes industriais”,
“tecnico em refrigeracao industrial”,“tecnico em HVAC”,
“tecnico em climatizacao industrial”,“tecnico em caldeiras industriais”,
“tecnico em vapor industrial”,“tecnico em ar comprimido industrial”,
“tecnico em tratamento de agua industrial”,“tecnico em utilidades industriais”,
“tecnico em manutencao preditiva”,“tecnico em manutencao preventiva”,
“tecnico em manutencao corretiva”,“tecnico em vibracao industrial”,
“tecnico em analise de oleo”,“tecnico em PCM”,
“tecnico em confiabilidade industrial”,“tecnico em planejamento de manutencao”,
“tecnico em controle de qualidade industrial”,“tecnico em inspecao de qualidade”,
“tecnico em ensaios nao destrutivos”,“tecnico em metrologia industrial”,
“tecnico em seguranca do trabalho industrial”,“tecnico em processos industriais”,
“tecnico em montagem industrial”,“tecnico em metalurgia”,
“tecnico em siderurgia”,“tecnico em mineracao”,“tecnico em petroquimica”,
“tecnico em gas industrial”,“tecnico em instalacoes industriais”,
]

PALAVRAS_DESCARTAR = [
“banco de talentos”,“encerrad”,“finalizad”,“expirad”,“inativ”,“cancelad”,
“vaga encerrada”,“nao esta mais disponivel”,“job expired”,“2024”,“2023”,
]

ANO_ATUAL = “2026”
CACHE_FILE = “vagas_cache.json”
ARTIGOS_FILE = “artigos.json”

ESTADOS_LISTA = [
(“AC”,“Acre”),(“AL”,“Alagoas”),(“AP”,“Amapa”),(“AM”,“Amazonas”),
(“BA”,“Bahia”),(“CE”,“Ceara”),(“DF”,“Distrito Federal”),(“ES”,“Espirito Santo”),
(“GO”,“Goias”),(“MA”,“Maranhao”),(“MT”,“Mato Grosso”),(“MS”,“Mato Grosso do Sul”),
(“MG”,“Minas Gerais”),(“PA”,“Para”),(“PB”,“Paraiba”),(“PR”,“Parana”),
(“PE”,“Pernambuco”),(“PI”,“Piaui”),(“RJ”,“Rio de Janeiro”),(“RN”,“Rio Grande do Norte”),
(“RS”,“Rio Grande do Sul”),(“RO”,“Rondonia”),(“RR”,“Roraima”),(“SC”,“Santa Catarina”),
(“SP”,“Sao Paulo”),(“SE”,“Sergipe”),(“TO”,“Tocantins”),
]
ESTADOS = {s:n for s,n in ESTADOS_LISTA}

CIDADES_ESTADO = {
“sao paulo”:“SP”,“campinas”:“SP”,“santos”:“SP”,“sorocaba”:“SP”,“jundiai”:“SP”,
“rio de janeiro”:“RJ”,“niteroi”:“RJ”,“macae”:“RJ”,
“belo horizonte”:“MG”,“contagem”:“MG”,“betim”:“MG”,“uberlandia”:“MG”,
“curitiba”:“PR”,“londrina”:“PR”,“maringa”:“PR”,
“porto alegre”:“RS”,“caxias do sul”:“RS”,“canoas”:“RS”,
“florianopolis”:“SC”,“joinville”:“SC”,“blumenau”:“SC”,
“salvador”:“BA”,“camacari”:“BA”,“feira de santana”:“BA”,
“recife”:“PE”,“caruaru”:“PE”,“fortaleza”:“CE”,“manaus”:“AM”,
“belem”:“PA”,“parauapebas”:“PA”,“goiania”:“GO”,“brasilia”:“DF”,
“vitoria”:“ES”,“vila velha”:“ES”,“serra”:“ES”,“cariacica”:“ES”,
“maceio”:“AL”,“natal”:“RN”,“joao pessoa”:“PB”,“teresina”:“PI”,
“sao luis”:“MA”,“porto velho”:“RO”,“cuiaba”:“MT”,“campo grande”:“MS”,
“macapa”:“AP”,“boa vista”:“RR”,“palmas”:“TO”,“aracaju”:“SE”,
}

ARTIGOS_PADRAO = [
{“titulo”:“A IA vai acabar com o emprego de tecnicos industriais?”,“resumo”:“A inteligencia artificial esta transformando a industria, mas os dados mostram que tecnicos sao dos profissionais mais resistentes a automacao.”,“conteudo”:“A pergunta que mais assusta trabalhadores da industria em 2026: a IA vai tirar meu emprego?\n\nA resposta curta e: nao para tecnicos industriais. E os dados comprovam isso.\n\n**Por que tecnicos industriais sao dificeis de substituir?**\n\nA automacao funciona bem para tarefas repetitivas. O trabalho de um tecnico industrial e exatamente o oposto disso.\n\nQuando uma bomba quebra as 3h da manha, nao e um algoritmo que vai trocar o selo. Quando um CLP apresenta falha intermitente, nao e uma tela que vai resolver no campo.\n\n**Os numeros:**\nSegundo o Forum Economico Mundial, 85 milhoes de empregos serao substituidos pela automacao ate 2025, mas 97 milhoes de novos empregos surgirao. Grande parte em manutencao e operacao de sistemas automatizados.\n\nNo Brasil, o deficit de tecnicos industriais qualificados ja chega a 400 mil profissionais, segundo o SENAI.”,“categoria”:“IA & Futuro”,“icone”:“🤖”,“fonte”:“TecVagas”,“url”:”#”,“data”:datetime.now().strftime(”%d/%m/%Y”)},
{“titulo”:“Quanto ganha um Tecnico em Manutencao Eletrica em 2026?”,“resumo”:“Salarios variam de R$ 2.800 a R$ 6.500 dependendo da regiao e experiencia.”,“conteudo”:“O tecnico em manutencao eletrica e um dos profissionais mais requisitados na industria brasileira em 2026.\n\n**Faixa salarial por nivel:**\n• Junior (0-2 anos): R$ 2.800 a R$ 3.500\n• Pleno (2-5 anos): R$ 3.500 a R$ 5.000\n• Senior (5+ anos): R$ 5.000 a R$ 6.500\n• Especialista: ate R$ 8.000\n\n**O que aumenta o salario:**\n• NR10 atualizado: +15 a 25%\n• NR35 (trabalho em altura): +10%\n• Periculosidade (eletricidade): +30% sobre o salario\n• Insalubridade: +10 a 40% sobre o salario minimo\n• Turno noturno: +20% adicional”,“categoria”:“Salarios”,“icone”:“⚡”,“fonte”:“TecVagas”,“url”:”#”,“data”:datetime.now().strftime(”%d/%m/%Y”)},
{“titulo”:“NR10: Guia Completo para Tecnicos Eletricos em 2026”,“resumo”:“A NR10 e obrigatoria para profissionais que trabalham com instalacoes eletricas.”,“conteudo”:“A NR10 e obrigatoria para qualquer profissional que trabalhe com sistemas eletricos no Brasil.\n\n**Tipos de curso:**\n• NR10 Basico: 40 horas\n• NR10 SEP: 40 horas adicionais (alta tensao)\n• Total: 80 horas para habilitacao completa\n\n**Validade:** 2 anos\n\n**Custo medio:**\n• SENAI: R$ 300 a R$ 600\n• Empresas privadas: R$ 600 a R$ 1.500\n• Reciclagem: R$ 150 a R$ 400\n\n**Impacto no salario:** +20 a 25% em media”,“categoria”:“Certificacoes”,“icone”:“📋”,“fonte”:“TecVagas”,“url”:”#”,“data”:datetime.now().strftime(”%d/%m/%Y”)},
{“titulo”:“Tecnico em Automacao: a profissao que mais cresce no Brasil”,“resumo”:“Com a Industria 4.0, tecnicos em PLC e SCADA sao os mais disputados.”,“conteudo”:“A automacao industrial esta criando uma enorme demanda por tecnicos qualificados.\n\n**O que o tecnico em automacao faz:**\n• Programacao e manutencao de CLPs\n• Configuracao de sistemas SCADA\n• Manutencao de robos industriais\n• Redes industriais (Profibus, Profinet)\n\n**Plataformas mais valorizadas:**\n• Siemens S7 (TIA Portal)\n• Allen Bradley (Studio 5000)\n• Schneider (EcoStruxure)\n• ABB - robotica\n\n**Salarios:**\n• Junior: R$ 3.000 a R$ 4.500\n• Pleno: R$ 4.500 a R$ 6.500\n• Senior: R$ 6.500 a R$ 9.000\n• Especialista: ate R$ 12.000”,“categoria”:“Carreira”,“icone”:“🤖”,“fonte”:“TecVagas”,“url”:”#”,“data”:datetime.now().strftime(”%d/%m/%Y”)},
{“titulo”:“Melhores empresas para tecnicos industriais em 2026”,“resumo”:“Petrobras, Vale, WEG, Embraer e Bosch oferecem os melhores pacotes.”,“conteudo”:“Algumas empresas se destacam pela remuneracao e beneficios para tecnicos industriais.\n\n**Petrobras**\n• Salario: R$ 9.000 a R$ 15.000\n• Acesso via concurso publico\n\n**Vale**\n• Salario: R$ 5.000 a R$ 10.000\n• Forte em MG, PA e ES\n\n**WEG**\n• Salario: R$ 3.500 a R$ 7.000\n• Base em Jaragua do Sul (SC)\n\n**Embraer**\n• Salario: R$ 4.000 a R$ 8.000\n• Sao Jose dos Campos (SP)\n\n**Bosch**\n• Salario: R$ 4.000 a R$ 7.500\n• Campinas e Curitiba”,“categoria”:“Empresas”,“icone”:“🏭”,“fonte”:“TecVagas”,“url”:”#”,“data”:datetime.now().strftime(”%d/%m/%Y”)},
{“titulo”:“Empregos manuais que a IA nunca vai substituir”,“resumo”:“Profissoes com trabalho fisico complexo e raciocinio situacional sao as mais seguras.”,“conteudo”:“A onda de automacao tem um ponto cego: o trabalho fisico especializado.\n\n**Profissoes mais seguras segundo pesquisadores:**\n\n• Tecnico em Manutencao Industrial - risco 2%\n• Tecnico Eletricista Industrial - risco 3%\n• Tecnico em Refrigeracao/HVAC - risco 4%\n• Tecnico em Automacao/PLC - risco 1%\n\n**O que fazer para se proteger:**\n• Especialize-se em equipamentos de alta complexidade\n• Aprenda a interpretar dados de sistemas de monitoramento\n• Adicione certificacoes NR ao seu curriculo\n• Desenvolva habilidade em manutencao preditiva\n\nO tecnico industrial do futuro nao compete com a IA - ele a opera, a programa e a mantem funcionando.”,“categoria”:“IA & Futuro”,“icone”:“🛡️”,“fonte”:“TecVagas”,“url”:”#”,“data”:datetime.now().strftime(”%d/%m/%Y”)},
]

def detectar_area(t):
t=t.lower()
if any(p in t for p in [“eletric”,“eletrom”,“painel”,“subestac”,“motor”,“gerador”]):return “eletrica”
if any(p in t for p in [“mecatron”,“plc”,“scada”,“robotic”,“automac”,“cnc”,“instrumenta”]):return “automacao”
if any(p in t for p in [“qualidad”,“inspec”,“metrolog”,“ensaio”,“calibr”]):return “qualidade”
if any(p in t for p in [“seguranc”,“meio ambient”]):return “seguranca”
if any(p in t for p in [“refriger”,“hvac”,“climatiz”,“ar condiciona”]):return “refrigeracao”
return “mecanica”

def detectar_estado(local_str):
if not local_str:
return None
texto = local_str.strip()
texto_lower = texto.lower()
m = re.search(r’\b([A-Z]{2})\s*$’, texto)
if m and m.group(1) in ESTADOS:
return m.group(1)
for sigla, nome in ESTADOS.items():
if nome.lower() in texto_lower:
return sigla
for cidade, sigla in CIDADES_ESTADO.items():
if cidade in texto_lower:
return sigla
return None

def titulo_valido(t):
return not any(p in t.lower() for p in PALAVRAS_DESCARTAR)

def normalizar_titulo(titulo):
titulo = re.sub(r’([a-z])([A-Z])’, r’\1 \2’, titulo)
titulo = re.sub(r’([a-zA-Z])(\d)’, r’\1 \2’, titulo)
titulo = re.sub(r’(\d)([a-zA-Z])’, r’\1 \2’, titulo)
for sufixo in [‘Jr’,‘Sr’,‘Pleno’,‘Junior’,‘Senior’,‘Trainee’]:
titulo = re.sub(rf’(?<=[a-z])({sufixo})\b’, rf’ \1’, titulo)
titulo = re.sub(r’\s*-\s*’, ’ - ‘, titulo)
titulo = re.sub(r’\s+’, ’ ’, titulo)
return titulo.strip()

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
if linha.startswith(’•’) or linha.startswith(‘✅’) or linha.startswith(‘❌’):
html += f’<p style="margin:4px 0;padding-left:4px">{linha}</p>’
else:
html += f’<p style="margin:8px 0">{linha}</p>’
return html

def buscar_gupy():
vagas=[]
print(“Buscando no Gupy…”)
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
vagas.append({“titulo”:titulo,“empresa”:job.get(“careerPageName”,“Empresa”)[:50],
“local”:local_display,“estado”:estado or “BR”,“url”:job.get(“jobUrl”,”#”),
“fonte”:“gupy.io”,“data”:datetime.now().strftime(”%d/%m/%Y”),
“area”:detectar_area(titulo),“beneficios”:[],“salario”:“A combinar”,“escala”:“CLT”})
time.sleep(1.0)
except Exception as e:print(f”  Gupy: {e}”)
print(f”  Gupy: {len(vagas)} vagas”)
return vagas

def buscar_vagas_com_br():
vagas=[]
print(“Buscando no vagas.com.br…”)
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
vagas.append({“titulo”:titulo,“empresa”:ee.get_text(strip=True)[:50] if ee else “Empresa”,
“local”:local_raw[:40] if local_raw else “Brasil”,“estado”:estado or “BR”,
“url”:“https://www.vagas.com.br”+te.get(“href”,””),
“fonte”:“vagas.com.br”,“data”:datetime.now().strftime(”%d/%m/%Y”),
“area”:detectar_area(titulo),“beneficios”:[],“salario”:“A combinar”,“escala”:“CLT”})
time.sleep(1.5)
except Exception as e:print(f”  vagas.com.br: {e}”)
print(f”  vagas.com.br: {len(vagas)} vagas”)
return vagas

def verificar_cache(cache):
if not cache:return []
print(f”\nVerificando {len(cache)} vagas…”)
ativas=[]
for v in cache:
if not titulo_valido(v.get(“titulo”,””)):continue
try:
r=requests.get(v[“url”],headers=HEADERS,timeout=8)
if r.status_code in[404,410]:continue
if any(p in r.text.lower() for p in [“vaga encerrada”,“job expired”]):continue
except:pass
if “beneficios” not in v:v[“beneficios”]=[]
if “salario” not in v:v[“salario”]=“A combinar”
if “escala” not in v:v[“escala”]=“CLT”
if v.get(“estado”) in [“BR”,””] and v.get(“local”):
novo=detectar_estado(v[“local”])
if novo:v[“estado”]=novo
v[“titulo”]=normalizar_titulo(v.get(“titulo”,””))
ativas.append(v)
time.sleep(0.3)
print(f”  {len(ativas)} ativas”)
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

AREA_CONFIG = {
“eletrica”:{“cls”:“tag-el”,“label”:“Eletrica”,“ico”:“⚡”,“cor”:”#1d4ed8”},
“mecanica”:{“cls”:“tag-me”,“label”:“Mecanica”,“ico”:“🔩”,“cor”:”#15803d”},
“automacao”:{“cls”:“tag-au”,“label”:“Automacao”,“ico”:“🤖”,“cor”:”#ea580c”},
“qualidade”:{“cls”:“tag-qu”,“label”:“Qualidade”,“ico”:“📊”,“cor”:”#7c3aed”},
“seguranca”:{“cls”:“tag-se”,“label”:“Seguranca”,“ico”:“🦺”,“cor”:”#0f766e”},
“refrigeracao”:{“cls”:“tag-rf”,“label”:“Refrigeracao”,“ico”:“❄️”,“cor”:”#2563eb”},
}

def gerar_card_vaga(v, idx=0):
area=v.get(“area”,“mecanica”)
cfg=AREA_CONFIG.get(area,AREA_CONFIG[“mecanica”])
salario=v.get(“salario”,“A combinar”)
escala=v.get(“escala”,“CLT”)
wpp=f”https://wa.me/?text=*{v[‘titulo’]}*%0A{v[‘empresa’]}%0A{v[‘local’]}%0A%0A{v[‘url’]}%0A%0A_Via TecVagas_”
return f’’’<article class="job-card" style="animation-delay:{idx*0.04}s" data-area="{area}" data-estado="{v.get('estado','BR')}" data-busca="{v.get('titulo','').lower()} {v.get('empresa','').lower()} {v.get('local','').lower()}">

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
    <div class="card-actions">
      <a class="btn-wpp" href="{wpp}" target="_blank" onclick="event.stopPropagation()">📲 WhatsApp</a>
      <a class="btn-ver" href="{v['url']}" target="_blank">Ver vaga →</a>
    </div>
  </div>
</article>'''

def gerar_card_artigo(a, idx=0):
conteudo_html = formatar_conteudo(a.get(“conteudo”,””)) or f’<p>{a.get(“resumo”,””)}</p>’
return f’’’<div class="article-card" onclick="openArticle({idx})">

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

def gerar_html(vagas, artigos):
agora=datetime.now().strftime(”%d/%m/%Y as %H:%M”)
cards_vagas=”\n”.join(gerar_card_vaga(v,i) for i,v in enumerate(vagas))
cards_artigos=”\n”.join(gerar_card_artigo(a,i) for i,a in enumerate(artigos))
total=len(vagas)
por_estado={}
for v in vagas:
e=v.get(“estado”,“BR”)
if e and e!=“BR”:por_estado[e]=por_estado.get(e,0)+1
estados_opts=’<option value="todos">Todos os estados</option>’
for s,n in ESTADOS_LISTA:
c=por_estado.get(s,0)
label=f”{n} ({c})” if c>0 else n
estados_opts+=f’<option value="{s}">{s} - {label}</option>’

```
return '''<!DOCTYPE html>
```

<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TecVagas - Vagas para Tecnicos Industriais 2026</title>
<meta name="description" content="As melhores vagas para tecnicos industriais do Brasil.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}
:root{
  --bg:#f6f8fc;--surface:#ffffff;--surface-2:#f1f5fb;--surface-3:#e9eef7;
  --line:#dbe4f0;--line-2:#c7d4e5;
  --text:#0f172a;--text-2:#334155;--muted:#64748b;--muted-2:#94a3b8;
  --navy:#0b1f3a;--navy-2:#102a4c;--navy-3:#16355f;
  --blue:#1d4ed8;--blue-2:#2563eb;--blue-3:#3b82f6;--blue-soft:#eff6ff;
  --green:#16a34a;--green-soft:#f0fdf4;--orange:#ea580c;--orange-soft:#fff7ed;
  --purple:#7c3aed;--purple-soft:#f5f3ff;--teal:#0f766e;--teal-soft:#f0fdfa;
  --yellow:#ca8a04;--yellow-soft:#fefce8;
  --shadow-sm:0 4px 16px rgba(15,23,42,.05);
  --shadow-md:0 10px 30px rgba(15,23,42,.08);
  --shadow-lg:0 22px 60px rgba(15,23,42,.10);
  --r:8px;--r2:14px;--r3:22px;
}
html{scroll-behavior:smooth}
body{background:radial-gradient(circle at top left,rgba(37,99,235,.05),transparent 30%),radial-gradient(circle at top right,rgba(11,31,58,.06),transparent 28%),var(--bg);color:var(--text);font-family:Inter,sans-serif;font-size:15px;line-height:1.6;overflow-x:hidden}
::-webkit-scrollbar{width:8px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:999px}
nav{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.92);backdrop-filter:blur(18px);border-bottom:1px solid rgba(15,23,42,.06);padding:0 22px;height:72px;display:flex;align-items:center;justify-content:space-between}
.nav-logo{font-family:Manrope,sans-serif;font-size:18px;font-weight:800;letter-spacing:-.3px;display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--navy)}
.nav-dot{width:9px;height:9px;background:var(--blue-2);border-radius:50%;box-shadow:0 0 0 6px rgba(37,99,235,.10);animation:blink 2s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.45}}
.nav-right{display:flex;align-items:center;gap:10px}
#nav-clock{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
.nav-badge{font-size:11px;font-weight:700;background:var(--blue-soft);color:var(--blue-2);border:1px solid rgba(37,99,235,.14);padding:6px 12px;border-radius:999px}
.hero{position:relative;overflow:hidden;padding:86px 24px 66px;text-align:center;background:radial-gradient(circle at 50% -20%,rgba(37,99,235,.20),transparent 45%),linear-gradient(180deg,#fff 0%,#f7faff 100%);border-bottom:1px solid rgba(15,23,42,.05)}
.hero-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(15,23,42,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(15,23,42,.03) 1px,transparent 1px);background-size:56px 56px;mask-image:radial-gradient(ellipse 100% 85% at 50% 0%,black 0%,transparent 78%)}
.hero-glow{position:absolute;top:-40px;left:50%;transform:translateX(-50%);width:900px;height:340px;background:radial-gradient(circle,rgba(29,78,216,.18),transparent 62%);pointer-events:none}
.hero-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--blue-2);margin-bottom:18px;background:rgba(255,255,255,.78);border:1px solid rgba(37,99,235,.12);padding:8px 14px;border-radius:999px;box-shadow:var(--shadow-sm)}
.hero h1{font-family:Manrope,sans-serif;font-size:clamp(36px,8vw,70px);font-weight:800;line-height:1.02;letter-spacing:-2.4px;color:var(--navy);margin-bottom:18px;max-width:820px;margin-left:auto;margin-right:auto}
.hero h1 .accent{color:var(--blue-2)}
.hero-sub{font-size:17px;color:var(--text-2);font-weight:500;max-width:650px;margin:0 auto;line-height:1.7}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;max-width:1120px;margin:24px auto 0;padding:0 18px 10px}
.metric{background:var(--surface);border:1px solid rgba(15,23,42,.06);border-radius:18px;padding:22px 16px;text-align:center;position:relative;overflow:hidden;box-shadow:var(--shadow-sm)}
.metric::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,var(--navy),var(--blue-2),#60a5fa)}
.metric-num{font-family:Manrope,sans-serif;font-size:30px;font-weight:800;color:var(--navy);line-height:1;margin-bottom:6px;letter-spacing:-1px}
.metric-label{font-size:11px;color:var(--muted);font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.filters-section{background:transparent;max-width:1120px;margin:14px auto 0;padding:14px 18px 4px}
.filters-search{position:relative;margin-bottom:12px}
.filters-search input{width:100%;background:var(--surface);border:1px solid var(--line);color:var(--text);font-family:Inter,sans-serif;font-size:14px;padding:15px 16px 15px 46px;border-radius:16px;outline:none;transition:border .2s,box-shadow .2s;box-shadow:var(--shadow-sm)}
.filters-search input::placeholder{color:var(--muted)}
.filters-search input:focus{border-color:rgba(37,99,235,.35);box-shadow:0 0 0 4px rgba(37,99,235,.10)}
.s-ico{position:absolute;left:16px;top:50%;transform:translateY(-50%);color:var(--blue-2);font-size:16px;pointer-events:none}
.f-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}
.f-row:last-child{margin-bottom:0}
.f-lbl{font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:8px;display:block}
.chip{flex-shrink:0;background:var(--surface);border:1px solid var(--line);color:var(--text-2);font-family:Inter,sans-serif;font-size:12px;font-weight:600;padding:8px 14px;border-radius:999px;cursor:pointer;transition:all .18s;white-space:nowrap;box-shadow:var(--shadow-sm)}
.chip:hover{border-color:rgba(37,99,235,.22);color:var(--blue-2);transform:translateY(-1px)}
.chip.active{background:var(--navy);border-color:var(--navy);color:#fff}
.f-sel{background:var(--surface);border:1px solid var(--line);color:var(--text);font-family:Inter,sans-serif;font-size:12px;padding:8px 13px;border-radius:999px;cursor:pointer;flex-shrink:0;outline:none;box-shadow:var(--shadow-sm)}
.trust-bar{max-width:1120px;margin:12px auto 0;background:linear-gradient(90deg,rgba(37,99,235,.05),rgba(11,31,58,.06));border:1px solid rgba(37,99,235,.10);border-radius:16px;padding:11px 16px;display:flex;align-items:center;gap:10px;font-size:12px;color:var(--text-2)}
.trust-dot{width:8px;height:8px;background:var(--green);border-radius:50%;flex-shrink:0;box-shadow:0 0 0 6px rgba(22,163,74,.12)}
.page{padding:28px 18px 56px;max-width:1120px;margin:0 auto}
.sec-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;margin-top:34px}
.sec-title{font-family:Manrope,sans-serif;font-size:18px;font-weight:800;color:var(--navy);display:flex;align-items:center;gap:10px;letter-spacing:-.3px}
.sec-count{font-size:11px;color:var(--blue-2);background:var(--blue-soft);border:1px solid rgba(37,99,235,.14);padding:6px 12px;border-radius:999px;font-weight:700}
.calc-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.calc-item{background:var(--surface);border:1px solid rgba(15,23,42,.06);border-radius:18px;padding:16px;display:flex;align-items:center;gap:12px;cursor:pointer;transition:all .2s;text-align:left;color:var(--text);box-shadow:var(--shadow-sm)}
.calc-item:hover{border-color:rgba(37,99,235,.18);transform:translateY(-2px);box-shadow:var(--shadow-md)}
.calc-emoji{font-size:22px;flex-shrink:0}
.calc-name{font-size:14px;font-weight:700;margin-bottom:2px;color:var(--navy)}
.calc-hint{font-size:11px;color:var(--muted)}
.articles-grid{display:flex;flex-direction:column;gap:12px}
.article-card{background:var(--surface);border:1px solid rgba(15,23,42,.06);border-radius:18px;padding:16px;display:flex;gap:14px;transition:all .2s;cursor:pointer;box-shadow:var(--shadow-sm)}
.article-card:hover{border-color:rgba(37,99,235,.16);transform:translateY(-2px);box-shadow:var(--shadow-md)}
.article-icon{font-size:24px;flex-shrink:0;margin-top:2px}
.article-content{flex:1;min-width:0}
.article-cat{font-size:10px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--blue-2);margin-bottom:4px}
.article-title{font-size:15px;font-weight:800;color:var(--navy);margin-bottom:5px;line-height:1.35}
.article-excerpt{font-size:13px;color:var(--text-2);line-height:1.55;margin-bottom:8px}
.article-footer{display:flex;align-items:center;justify-content:space-between;gap:8px}
.article-source{font-size:11px;color:var(--muted)}
.article-cta{font-size:12px;color:var(--blue-2);font-weight:800}
.newsletter{background:linear-gradient(135deg,#fff,#f5f9ff);border:1px solid rgba(37,99,235,.10);border-radius:22px;padding:24px 20px;margin-bottom:4px;position:relative;overflow:hidden;box-shadow:var(--shadow-md)}
.newsletter::before{content:'';position:absolute;top:0;left:0;right:0;height:5px;background:linear-gradient(90deg,var(--navy),var(--blue-2),#60a5fa)}
.nl-title{font-family:Manrope,sans-serif;font-size:20px;font-weight:800;margin-bottom:5px;color:var(--navy)}
.nl-title span{color:var(--blue-2)}
.nl-desc{font-size:13px;color:var(--text-2);margin-bottom:16px}
.nl-form{display:flex;gap:10px;flex-wrap:wrap}
.nl-input{flex:1;min-width:180px;background:#fff;border:1px solid var(--line);color:var(--text);font-family:Inter,sans-serif;font-size:14px;padding:12px 14px;border-radius:14px;outline:none}
.nl-input:focus{border-color:rgba(37,99,235,.35);box-shadow:0 0 0 4px rgba(37,99,235,.10)}
.nl-btn{background:var(--navy);color:#fff;border:none;font-family:Inter,sans-serif;font-size:14px;font-weight:700;padding:12px 18px;border-radius:14px;cursor:pointer;white-space:nowrap}
.nl-btn:hover{background:var(--navy-2)}
.nl-ok{display:none;color:var(--green);font-size:12px;margin-top:8px;font-weight:700}
.jobs-list{display:flex;flex-direction:column;gap:14px}
.job-card{background:var(--surface);border:1px solid rgba(15,23,42,.06);border-radius:22px;overflow:hidden;transition:all .22s;animation:fadeUp .35s ease both;position:relative;box-shadow:var(--shadow-sm)}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.job-card:hover{border-color:rgba(37,99,235,.16);transform:translateY(-3px);box-shadow:var(--shadow-lg)}
.card-accent{position:absolute;left:0;top:0;bottom:0;width:5px;border-radius:22px 0 0 22px}
.card-body{padding:20px 20px 18px 24px}
.card-top{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:12px}
.card-main{flex:1;min-width:0}
.card-tag{display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;padding:5px 10px;border-radius:999px;margin-bottom:8px}
.tag-el{background:#eff6ff;color:#1d4ed8;border:1px solid rgba(37,99,235,.12)}
.tag-me{background:#f0fdf4;color:#15803d;border:1px solid rgba(22,163,74,.12)}
.tag-au{background:#fff7ed;color:#ea580c;border:1px solid rgba(234,88,12,.12)}
.tag-qu{background:#f5f3ff;color:#7c3aed;border:1px solid rgba(124,58,237,.12)}
.tag-se{background:#f0fdfa;color:#0f766e;border:1px solid rgba(15,118,110,.12)}
.tag-rf{background:#eff6ff;color:#2563eb;border:1px solid rgba(37,99,235,.12)}
.card-title{font-family:Manrope,sans-serif;font-size:20px;font-weight:800;color:var(--navy);line-height:1.25;margin-bottom:4px;letter-spacing:-.4px}
.card-company{font-size:13px;color:var(--text-2);font-weight:600}
.card-badge-verified{flex-shrink:0;font-size:11px;font-weight:800;color:var(--green);background:var(--green-soft);border:1px solid rgba(22,163,74,.12);padding:6px 10px;border-radius:999px;white-space:nowrap}
.card-info-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.info-chip{font-size:11px;color:var(--text-2);background:var(--surface-2);border:1px solid var(--line);padding:6px 10px;border-radius:999px;font-weight:600}
.card-actions{display:flex;gap:8px;padding-top:14px;border-top:1px solid rgba(15,23,42,.06)}
.btn-wpp{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:700;color:var(--green);background:var(--green-soft);border:1px solid rgba(22,163,74,.14);padding:10px 14px;border-radius:14px;text-decoration:none;transition:all .2s}
.btn-wpp:hover{background:#e8faef}
.btn-ver{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:700;color:#fff;background:linear-gradient(135deg,var(--navy),var(--blue-2));padding:10px 16px;border-radius:14px;text-decoration:none;transition:all .2s;margin-left:auto;box-shadow:0 10px 24px rgba(29,78,216,.18)}
.btn-ver:hover{transform:translateY(-1px)}
.empty-state{text-align:center;padding:56px 20px;display:none}
.page[data-searching] .calc-section,.page[data-searching] .articles-section,.page[data-searching] .newsletter{display:none!important}
.empty-icon{font-size:46px;margin-bottom:14px;opacity:.5}
.empty-title{font-family:Manrope,sans-serif;font-size:20px;font-weight:800;margin-bottom:8px;color:var(--navy)}
.empty-text{font-size:14px;color:var(--muted);line-height:1.7;margin-bottom:20px}
.empty-btn{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:700;color:var(--blue-2);background:var(--blue-soft);border:1px solid rgba(37,99,235,.14);padding:10px 18px;border-radius:999px;cursor:pointer;transition:all .2s}
.empty-btn:hover{background:#dbeafe}
.modal{display:none;position:fixed;inset:0;background:rgba(15,23,42,.45);z-index:1000;align-items:center;justify-content:center;padding:16px;backdrop-filter:blur(7px);overflow-y:auto}
.modal.open{display:flex}
.modal-box{background:var(--surface);border:1px solid rgba(15,23,42,.06);border-radius:24px;padding:24px;width:100%;max-width:420px;margin:auto;position:relative;box-shadow:var(--shadow-lg)}
.modal-box::before{content:'';position:absolute;top:0;left:0;right:0;height:5px;background:linear-gradient(90deg,var(--navy),var(--blue-2),#60a5fa);border-radius:24px 24px 0 0}
.modal-article{max-width:660px;max-height:86vh;overflow-y:auto}
.modal-article-cat{font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--blue-2);margin-bottom:10px}
.modal-article-title{font-family:Manrope,sans-serif;font-size:28px;font-weight:800;line-height:1.15;margin-bottom:10px;letter-spacing:-.6px;color:var(--navy)}
.modal-article-meta{font-size:12px;color:var(--muted);margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid rgba(15,23,42,.06)}
.modal-article-body{font-size:15px;color:var(--text-2);line-height:1.78;margin-bottom:20px}
.modal-article-body strong{color:var(--navy);font-weight:800}
.modal-title{font-family:Manrope,sans-serif;font-size:20px;font-weight:800;color:var(--navy);margin-bottom:16px}
.modal-field{margin-bottom:13px}
.modal-label{font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);display:block;margin-bottom:6px}
.modal-input,.modal-select{width:100%;background:#fff;border:1px solid var(--line);color:var(--text);font-family:Inter,sans-serif;font-size:14px;padding:11px 13px;border-radius:14px;outline:none;transition:border .2s,box-shadow .2s}
.modal-input:focus,.modal-select:focus{border-color:rgba(37,99,235,.35);box-shadow:0 0 0 4px rgba(37,99,235,.10)}
.calc-result{background:var(--surface-2);border:1px solid var(--line);border-radius:16px;padding:14px;margin-top:14px}
.result-row{display:flex;justify-content:space-between;font-size:13px;margin-bottom:8px;color:var(--text-2)}
.result-row.total{color:var(--navy);font-weight:800;font-size:16px;border-top:1px solid var(--line);padding-top:10px;margin-top:5px}
.btn-close{width:100%;margin-top:10px;background:#fff;color:var(--text-2);border:1px solid var(--line);font-family:Inter,sans-serif;font-size:13px;font-weight:700;padding:11px;border-radius:14px;cursor:pointer;transition:all .2s}
.btn-close:hover{border-color:var(--line-2);background:var(--surface-2)}
footer{border-top:1px solid rgba(15,23,42,.06);padding:30px 20px 34px;text-align:center;background:linear-gradient(180deg,rgba(255,255,255,0),rgba(255,255,255,.7))}
.footer-logo{font-family:Manrope,sans-serif;font-size:18px;font-weight:800;margin-bottom:8px;color:var(--navy)}
.footer-logo span{color:var(--blue-2)}
.footer-text{font-size:12px;color:var(--muted);line-height:1.8}
@media (max-width:860px){.metrics{grid-template-columns:repeat(2,1fr)}}
@media (max-width:640px){nav{height:66px;padding:0 16px}.hero{padding:72px 18px 52px}.hero h1{letter-spacing:-1.6px}.hero-sub{font-size:15px}.metrics{padding:0 14px 8px;gap:10px}.filters-section,.page{padding-left:14px;padding-right:14px}.calc-grid{grid-template-columns:1fr}.card-top{flex-direction:column}.card-badge-verified{align-self:flex-start}.card-actions{flex-wrap:wrap}.btn-ver{margin-left:0}.modal-box{padding:18px}.modal-article-title{font-size:22px}}
</style>
</head>
<body>

<nav>
  <a class="nav-logo" href="#">
    <div class="nav-dot"></div>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 44" height="28" style="display:block">
      <defs><linearGradient id="og" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#0b1f3a"/><stop offset="100%" style="stop-color:#2563eb"/></linearGradient></defs>
      <g transform="translate(20,22)">
        <circle cx="0" cy="0" r="10" fill="none" stroke="url(#og)" stroke-width="2.5"/>
        <circle cx="0" cy="0" r="5" fill="#fff" stroke="url(#og)" stroke-width="1"/>
        <circle cx="0" cy="-1.5" r="2.5" fill="url(#og)"/>
        <path d="M-2,-1.5 Q-2,2 0,5.5 Q2,2 2,-1.5 Z" fill="url(#og)"/>
      </g>
      <text x="38" y="30" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="22" fill="#0b1f3a" letter-spacing="-0.5">Tec</text>
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
  <div class="hero-eyebrow">🇧🇷 Vagas para tecnicos industriais · 2026</div>
  <h1>As melhores vagas<br>para <span class="accent">tecnicos industriais</span><br>do Brasil.</h1>
  <p class="hero-sub">Eletrica · Mecanica · Automacao · Refrigeracao<br>Vagas verificadas, atualizadas 5x por dia.</p>
</section>

<div class="metrics">
  <div class="metric"><div class="metric-num" id="m-vagas">''' + str(total) + '''</div><div class="metric-label">Vagas ativas</div></div>
  <div class="metric"><div class="metric-num">60+</div><div class="metric-label">Especialidades</div></div>
  <div class="metric"><div class="metric-num">5x</div><div class="metric-label">Atualizado/dia</div></div>
  <div class="metric"><div class="metric-num">27</div><div class="metric-label">Estados</div></div>
</div>

<div class="filters-section">
  <div class="filters-search">
    <span class="s-ico">🔍</span>
    <input type="text" id="s-inp" placeholder="Buscar por cargo, empresa ou cidade..." oninput="buscar(this.value)">
  </div>
  <span class="f-lbl">Area tecnica</span>
  <div class="f-row">
    <button class="chip active" onclick="fA('todas',this)">Todas</button>
    <button class="chip" onclick="fA('eletrica',this)">⚡ Eletrica</button>
    <button class="chip" onclick="fA('mecanica',this)">🔩 Mecanica</button>
    <button class="chip" onclick="fA('automacao',this)">🤖 Automacao</button>
    <button class="chip" onclick="fA('refrigeracao',this)">❄️ Refrigeracao</button>
    <button class="chip" onclick="fA('qualidade',this)">📊 Qualidade</button>
    <button class="chip" onclick="fA('seguranca',this)">🦺 Seguranca</button>
  </div>
  <span class="f-lbl">Estado</span>
  <div class="f-row">
    <select class="f-sel" onchange="fE(this.value)">''' + estados_opts + '''</select>
  </div>
</div>

<div class="trust-bar">
  <div class="trust-dot"></div>
  Vagas verificadas · Apenas 2026 · Encerradas removidas automaticamente · Atualizado em ''' + agora + '''
</div>

<div class="page">

  <div class="calc-section">
  <div class="sec-hdr"><div class="sec-title">🧮 Calculadoras Trabalhistas</div></div>
  <div class="calc-grid">
    <button class="calc-item" onclick="openModal('m-sal')"><div class="calc-emoji">💰</div><div><div class="calc-name">Salario Liquido</div><div class="calc-hint">INSS + IRRF 2026</div></div></button>
    <button class="calc-item" onclick="openModal('m-fer')"><div class="calc-emoji">🏖️</div><div><div class="calc-name">Ferias</div><div class="calc-hint">+ 1/3 constitucional</div></div></button>
    <button class="calc-item" onclick="openModal('m-res')"><div class="calc-emoji">📦</div><div><div class="calc-name">Rescisao</div><div class="calc-hint">Demissao ou pedido</div></div></button>
    <button class="calc-item" onclick="openModal('m-he')"><div class="calc-emoji">⏰</div><div><div class="calc-name">Hora Extra</div><div class="calc-hint">50%, 100% e noturna</div></div></button>
    <button class="calc-item" onclick="openModal('m-not')"><div class="calc-emoji">🌙</div><div><div class="calc-name">Adicional Noturno</div><div class="calc-hint">20% sobre salario</div></div></button>
    <button class="calc-item" onclick="openModal('m-ins')"><div class="calc-emoji">⚠️</div><div><div class="calc-name">Insalubridade</div><div class="calc-hint">e Periculosidade</div></div></button>
    <button class="calc-item" onclick="openModal('m-dec')"><div class="calc-emoji">🎄</div><div><div class="calc-name">13o Salario</div><div class="calc-hint">Proporcional ou cheio</div></div></button>
  </div>
  </div>

  <div class="articles-section">
  <div class="sec-hdr"><div class="sec-title">📰 Para Tecnicos</div><span class="sec-count">''' + str(len(artigos)) + ''' artigos</span></div>
  <div class="articles-grid">''' + cards_artigos + '''</div>
  </div>

  <div class="newsletter">
    <div class="nl-title">📧 Receba <span>vagas</span> no seu email</div>
    <div class="nl-desc">Toda semana as melhores vagas tecnicas. Gratis.</div>
    <div class="nl-form">
      <input class="nl-input" type="email" id="nl-e" placeholder="seu@email.com">
      <button class="nl-btn" onclick="newsletter()">Quero receber</button>
    </div>
    <div class="nl-ok" id="nl-ok">Cadastrado!</div>
  </div>

  <div class="sec-hdr" id="vagas"><div class="sec-title">🔧 Vagas Disponiveis</div><span class="sec-count" id="vc">''' + str(total) + ''' vagas</span></div>
  <div class="jobs-list" id="jl">''' + cards_vagas + '''</div>
  <div class="empty-state" id="es">
    <div class="empty-icon">🔍</div>
    <div class="empty-title">Nenhuma vaga encontrada</div>
    <div class="empty-text">Tente outra area, estado ou termo de busca.</div>
    <button class="empty-btn" onclick="resetF()">Ver todas as vagas</button>
  </div>

</div>

<div class="modal" id="m-sal"><div class="modal-box">
<div class="modal-title">💰 Salario Liquido</div>
<div class="modal-field"><label class="modal-label">Salario Bruto</label><input class="modal-input" type="number" id="s1" oninput="cS()"></div>
<div class="modal-field"><label class="modal-label">Dependentes</label><input class="modal-input" type="number" id="s2" value="0" oninput="cS()"></div>
<div class="calc-result" id="s-r" style="display:none">
<div class="result-row"><span>Bruto</span><span id="s-a"></span></div>
<div class="result-row"><span>(-) INSS</span><span id="s-b" style="color:#dc2626"></span></div>
<div class="result-row"><span>(-) IRRF</span><span id="s-c" style="color:#dc2626"></span></div>
<div class="result-row total"><span>Liquido</span><span id="s-d"></span></div>
</div>
<button class="btn-close" onclick="closeModal('m-sal')">Fechar</button>
</div></div>

<div class="modal" id="m-fer"><div class="modal-box">
<div class="modal-title">🏖️ Ferias</div>
<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="f1" oninput="cF()"></div>
<div class="modal-field"><label class="modal-label">Meses</label><input class="modal-input" type="number" id="f2" value="12" oninput="cF()"></div>
<div class="calc-result" id="f-r" style="display:none">
<div class="result-row"><span>Ferias</span><span id="f-a"></span></div>
<div class="result-row"><span>+ 1/3</span><span id="f-b" style="color:var(--green)"></span></div>
<div class="result-row total"><span>Liquido</span><span id="f-d"></span></div>
</div>
<button class="btn-close" onclick="closeModal('m-fer')">Fechar</button>
</div></div>

<div class="modal" id="m-res"><div class="modal-box">
<div class="modal-title">📦 Rescisao</div>
<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="r1" oninput="cR()"></div>
<div class="modal-field"><label class="modal-label">Meses</label><input class="modal-input" type="number" id="r2" oninput="cR()"></div>
<div class="modal-field"><label class="modal-label">Tipo</label>
<select class="modal-select" id="r3" onchange="cR()">
<option value="sj">Sem justa causa</option><option value="pd">Pedido</option><option value="ac">Acordo</option>
</select></div>
<div class="calc-result" id="r-r" style="display:none">
<div class="result-row"><span>Saldo</span><span id="r-a"></span></div>
<div class="result-row"><span>13o</span><span id="r-b"></span></div>
<div class="result-row"><span>Ferias</span><span id="r-c"></span></div>
<div class="result-row total"><span>Total</span><span id="r-e"></span></div>
</div>
<button class="btn-close" onclick="closeModal('m-res')">Fechar</button>
</div></div>

<div class="modal" id="m-he"><div class="modal-box">
<div class="modal-title">⏰ Hora Extra</div>
<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="h1" oninput="cHE()"></div>
<div class="modal-field"><label class="modal-label">Horas</label><input class="modal-input" type="number" id="h2" oninput="cHE()"></div>
<div class="modal-field"><label class="modal-label">Tipo</label>
<select class="modal-select" id="h3" onchange="cHE()">
<option value="50">50%</option><option value="100">100%</option><option value="70">70%</option>
</select></div>
<div class="calc-result" id="h-r" style="display:none">
<div class="result-row total"><span>Total</span><span id="h-c"></span></div>
</div>
<button class="btn-close" onclick="closeModal('m-he')">Fechar</button>
</div></div>

<div class="modal" id="m-not"><div class="modal-box">
<div class="modal-title">🌙 Adicional Noturno</div>
<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="n1" oninput="cN()"></div>
<div class="modal-field"><label class="modal-label">Horas/mes</label><input class="modal-input" type="number" id="n2" oninput="cN()"></div>
<div class="calc-result" id="n-r" style="display:none">
<div class="result-row total"><span>Total</span><span id="n-c"></span></div>
</div>
<button class="btn-close" onclick="closeModal('m-not')">Fechar</button>
</div></div>

<div class="modal" id="m-ins"><div class="modal-box">
<div class="modal-title">⚠️ Insalubridade</div>
<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="i1" oninput="cI()"></div>
<div class="modal-field"><label class="modal-label">Tipo</label>
<select class="modal-select" id="i2" onchange="cI()">
<option value="10">Min 10%</option><option value="20">Med 20%</option><option value="40">Max 40%</option><option value="30p">Periculosidade 30%</option>
</select></div>
<div class="calc-result" id="i-r" style="display:none">
<div class="result-row total"><span>Total</span><span id="i-c"></span></div>
</div>
<button class="btn-close" onclick="closeModal('m-ins')">Fechar</button>
</div></div>

<div class="modal" id="m-dec"><div class="modal-box">
<div class="modal-title">🎄 13o Salario</div>
<div class="modal-field"><label class="modal-label">Salario</label><input class="modal-input" type="number" id="d1" oninput="cD()"></div>
<div class="modal-field"><label class="modal-label">Meses</label><input class="modal-input" type="number" id="d2" value="12" oninput="cD()"></div>
<div class="calc-result" id="d-r" style="display:none">
<div class="result-row total"><span>Liquido</span><span id="d-c"></span></div>
</div>
<button class="btn-close" onclick="closeModal('m-dec')">Fechar</button>
</div></div>

<footer>
  <div class="footer-logo">Tec<span>Vagas</span></div>
  <div class="footer-text">Vagas tecnicas industriais verificadas · Apenas 2026 · Todo o Brasil<br>Atualizado automaticamente 5x por dia</div>
</footer>

<script data-goatcounter="https://tecvagas.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>

<script>
(function(){var el=document.getElementById('nav-clock');function t(){el.textContent=new Date().toLocaleTimeString('pt-BR',{timeZone:'America/Sao_Paulo',hour:'2-digit',minute:'2-digit'});}t();setInterval(t,1000);})();
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
function cD(){var b=G('d1'),m=GI('d2')||12;if(!b){SH('d-r',0);return;}var br=b*(m/12),i=IN(br),r=IR(br-i,0);S('d-c',R(br-i-r));SH('d-r',1);}
</script>

</body>
</html>'''

def main():
print(f”\nTecVagas v11 - {datetime.now().strftime(’%d/%m/%Y %H:%M’)}”)
print(”=”*50)
cache=carregar_cache()
vagas_ativas=verificar_cache(cache)
vagas_novas=buscar_gupy()+buscar_vagas_com_br()
todas=remover_duplicatas(vagas_ativas+vagas_novas)
artigos=carregar_artigos()
print(f”\n{len(todas)} vagas | {len(artigos)} artigos”)
with open(CACHE_FILE,“w”,encoding=“utf-8”) as f:json.dump(todas,f,ensure_ascii=False,indent=2)
with open(“index.html”,“w”,encoding=“utf-8”) as f:f.write(gerar_html(todas,artigos))
print(“Site atualizado!”)

if **name**==”**main**”:main()
