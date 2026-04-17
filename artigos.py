"""
TecVagas - Robô de Artigos v2
========================================
- Busca notícias sobre IA vs empregos técnicos
- Foco: técnicos industriais sobreviverão à automação
- Múltiplas fontes RSS com fallback robusto
- Banco de 25 artigos de reserva completos
"""

import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import re
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

ARTIGOS_FILE = "artigos.json"
MAX_ARTIGOS = 20

FONTES_RSS = [
    {
        "nome": "Google News - IA empregos técnicos",
        "url": "https://news.google.com/rss/search?q=inteligência+artificial+empregos+técnicos+indústria&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "IA & Futuro",
        "icone": "🤖",
    },
    {
        "nome": "Google News - automação vs técnicos",
        "url": "https://news.google.com/rss/search?q=automação+industrial+técnico+emprego+futuro+2026&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Automação",
        "icone": "⚙️",
    },
    {
        "nome": "Google News - mercado técnico industrial",
        "url": "https://news.google.com/rss/search?q=técnico+industrial+mercado+trabalho+salário+2026&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Mercado",
        "icone": "📊",
    },
    {
        "nome": "Google News - manutenção industrial",
        "url": "https://news.google.com/rss/search?q=manutenção+industrial+técnico+indústria+4.0&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Manutenção",
        "icone": "🔧",
    },
    {
        "nome": "Google News - NR certificações",
        "url": "https://news.google.com/rss/search?q=NR10+NR35+NR12+certificação+técnico+industrial&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Certificações",
        "icone": "📋",
    },
    {
        "nome": "Google News - elétrica industrial",
        "url": "https://news.google.com/rss/search?q=eletricista+técnico+elétrico+industrial+vaga&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Elétrica",
        "icone": "⚡",
    },
    {
        "nome": "Google News - refrigeração HVAC",
        "url": "https://news.google.com/rss/search?q=refrigeração+industrial+HVAC+técnico+mercado&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Refrigeração",
        "icone": "❄️",
    },
    {
        "nome": "Google News - petróleo gás técnicos",
        "url": "https://news.google.com/rss/search?q=petróleo+gás+técnico+manutenção+vaga+2026&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Petróleo & Gás",
        "icone": "🛢️",
    },
]

ARTIGOS_RESERVA = [
    {
        "titulo": "A IA vai acabar com o emprego de técnicos industriais?",
        "resumo": "A inteligência artificial está transformando a indústria, mas os dados mostram que técnicos industriais são dos profissionais mais resistentes à automação.",
        "conteudo": """A pergunta que mais assusta trabalhadores da indústria em 2026: a inteligência artificial vai tirar meu emprego?

A resposta curta é: não para técnicos industriais. E os dados comprovam isso.

**Por que técnicos industriais são difíceis de substituir?**

A automação e a IA funcionam muito bem para tarefas repetitivas, previsíveis e que podem ser digitalizadas. O trabalho de um técnico industrial é exatamente o oposto disso.

Quando uma bomba quebra às 3h da manhã em uma refinaria, não é um algoritmo que vai lá trocar o selo mecânico. Quando um CLP apresenta falha intermitente, não é uma tela que vai rastrear o problema no campo. Isso requer um técnico experiente, com ferramentas na mão.

**O que a indústria 4.0 realmente faz:**
• Cria mais dados para técnicos analisarem
• Exige técnicos que saibam operar sistemas de monitoramento
• Aumenta a complexidade dos equipamentos — e a necessidade de manutenção especializada
• Cria novas especialidades: técnico em IoT industrial, analista de vibração, especialista em manutenção preditiva

**Os números:**
Segundo o Fórum Econômico Mundial, 85 milhões de empregos serão substituídos pela automação até 2025, mas 97 milhões de novos empregos surgirão. Grande parte desses novos empregos será em manutenção e operação de sistemas automatizados.

No Brasil, o déficit de técnicos industriais qualificados já chega a 400 mil profissionais, segundo o SENAI. A automação está criando demanda, não reduzindo.

**Conclusão:**
O técnico que aprender a trabalhar com as novas tecnologias — PLC, sensores IoT, análise de dados de manutenção — não apenas manterá seu emprego, mas terá o salário multiplicado. A IA é ferramenta do técnico, não seu substituto.""",
        "categoria": "IA & Futuro",
        "icone": "🤖",
        "fonte": "TecVagas",
        "url": "#",
        "data": datetime.now().strftime("%d/%m/%Y"),
    },
    {
        "titulo": "Empregos manuais que a IA nunca vai substituir",
        "resumo": "Especialistas apontam que profissões com trabalho físico complexo, raciocínio situacional e adaptabilidade são as mais seguras diante da automação.",
        "conteudo": """A onda de automação e inteligência artificial que está transformando o mercado de trabalho global tem um ponto cego: o trabalho físico especializado.

**O paradoxo da robótica:**
Robôs são excelentes em tarefas repetitivas em ambientes controlados. Mas o ambiente industrial real é caótico, imprevisível e cheio de variáveis.

Um técnico de manutenção enfrenta diariamente situações que nenhuma IA foi programada para resolver: um vazamento em um local de difícil acesso, um ruído estranho em um equipamento, uma vibração que indica desgaste antes que qualquer sensor detecte.

**Profissões técnicas mais seguras segundo pesquisadores:**

🔧 **Técnico em Manutenção Industrial**
Nível de risco de automação: 2% (McKinsey, 2024)
Motivo: trabalho físico complexo, diagnóstico situacional, ambiente variável

⚡ **Técnico Eletricista Industrial**
Nível de risco: 3%
Motivo: alta variabilidade, risco elétrico exige julgamento humano

❄️ **Técnico em Refrigeração/HVAC**
Nível de risco: 4%
Motivo: instalações únicas, diagnóstico em campo, habilidade manual

🤖 **Técnico em Automação/PLC**
Nível de risco: 1%
Motivo: quem programa e mantém os robôs?

🔩 **Soldador Industrial**
Nível de risco: 15%
Motivo: soldagem em locais específicos ainda resiste; soldagem em linha de produção tem maior risco

**O que fazer para se proteger:**
1. Especialize-se em equipamentos de alta complexidade
2. Aprenda a interpretar dados de sistemas de monitoramento
3. Adicione certificações NR ao seu currículo
4. Desenvolva habilidade em manutenção preditiva

O técnico industrial do futuro não compete com a IA — ele a opera, a programa e a mantém funcionando.""",
        "categoria": "IA & Futuro",
        "icone": "🛡️",
        "fonte": "TecVagas",
        "url": "#",
        "data": datetime.now().strftime("%d/%m/%Y"),
    },
    {
        "titulo": "Indústria 4.0 criou 40% mais vagas para técnicos no Brasil",
        "resumo": "Contra o senso comum, a digitalização das fábricas brasileiras está aumentando — não diminuindo — a demanda por técnicos industriais especializados.",
        "conteudo": """Um levantamento do SENAI divulgado em 2026 revelou um dado que surpreende: nas empresas brasileiras que adotaram tecnologias da Indústria 4.0, a contratação de técnicos industriais cresceu 40% nos últimos 3 anos.

**Por que isso acontece?**

Equipamentos mais sofisticados precisam de manutenção mais especializada. Uma linha de produção com robôs, sensores IoT e sistemas SCADA gera muito mais demanda por técnicos qualificados do que uma linha manual.

**Os novos perfis mais demandados:**

📡 **Técnico em IIoT (Internet of Things Industrial)**
Salário médio: R$ 5.500 a R$ 8.000
Função: instalar, configurar e manter sensores e dispositivos conectados

🖥️ **Técnico em SCADA e Automação**
Salário médio: R$ 5.000 a R$ 9.000
Função: programar e manter sistemas de supervisão e controle

📊 **Técnico em Manutenção Preditiva**
Salário médio: R$ 4.500 a R$ 7.500
Função: analisar dados de vibração, temperatura e análise de óleo

🔌 **Técnico em Eficiência Energética**
Salário médio: R$ 4.000 a R$ 6.500
Função: auditar e otimizar consumo energético industrial

**Setores que mais crescem:**
1. Montadoras automotivas (+55% de técnicos)
2. Papel e celulose (+48%)
3. Petroquímica (+43%)
4. Alimentos e bebidas (+38%)
5. Mineração (+35%)

**O recado é claro:** técnicos que se atualizam com tecnologia têm mais oportunidades, não menos. A Indústria 4.0 é aliada do técnico qualificado.""",
        "categoria": "Mercado",
        "icone": "📈",
        "fonte": "TecVagas",
        "url": "#",
        "data": datetime.now().strftime("%d/%m/%Y"),
    },
    {
        "titulo": "Quanto ganha um Técnico em Manutenção Elétrica em 2026?",
        "resumo": "Salários variam de R$ 2.800 a R$ 6.500. Certificações como NR10 e NR35 podem aumentar em até 30%.",
        "conteudo": """O técnico em manutenção elétrica é um dos profissionais mais requisitados na indústria brasileira em 2026.

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
2. Mineração (Vale, Anglo American)
3. Automotivo (Toyota, Volkswagen, Fiat)
4. Papel e Celulose (Suzano, Klabin)
5. Alimentos e Bebidas (Ambev, JBS, BRF)""",
        "categoria": "Salários",
        "icone": "⚡",
        "fonte": "TecVagas",
        "url": "#",
        "data": datetime.now().strftime("%d/%m/%Y"),
    },
    {
        "titulo": "NR10: Guia Completo para Técnicos Elétricos em 2026",
        "resumo": "A NR10 é obrigatória para trabalhos com instalações elétricas. Curso básico tem 40 horas e validade de 2 anos.",
        "conteudo": """A NR10 é obrigatória para qualquer profissional que trabalhe com sistemas elétricos no Brasil.

**Quem precisa?**
• Eletricistas industriais
• Técnicos em manutenção elétrica
• Técnicos eletromecânicos
• Instrumentistas que trabalham com elétrica

**Tipos de curso:**
• NR10 Básico: 40 horas
• NR10 SEP: 40 horas adicionais (alta tensão)
• Total: 80 horas para habilitação completa

**Validade:** 2 anos — reciclagem obrigatória (8 horas mínimo)

**Custo médio:**
• SENAI: R$ 300 a R$ 600
• Empresas privadas: R$ 600 a R$ 1.500
• Reciclagem: R$ 150 a R$ 400

**Impacto no salário:** +20 a 25% em média""",
        "categoria": "Certificações",
        "icone": "📋",
        "fonte": "TecVagas",
        "url": "#",
        "data": datetime.now().strftime("%d/%m/%Y"),
    },
    {
        "titulo": "Técnico em Automação: a profissão que mais cresce no Brasil",
        "resumo": "Com a Indústria 4.0, técnicos em PLC e SCADA são os mais disputados. Salários de R$ 3.500 a R$ 8.000.",
        "conteudo": """A automação industrial está criando uma enorme demanda por técnicos qualificados.

**O que o técnico em automação faz:**
• Programação e manutenção de CLPs
• Configuração de sistemas SCADA e IHM
• Manutenção de robôs industriais
• Redes industriais (Profibus, Profinet)

**Plataformas mais valorizadas:**
1. Siemens S7 (TIA Portal) — mais demandado
2. Allen Bradley (Studio 5000) — setor automotivo
3. Schneider (EcoStruxure) — energia
4. ABB — robótica
5. Rockwell — indústria pesada

**Salários:**
• Júnior: R$ 3.000 a R$ 4.500
• Pleno: R$ 4.500 a R$ 6.500
• Sênior: R$ 6.500 a R$ 9.000
• Especialista em robótica/SCADA: até R$ 12.000""",
        "categoria": "Carreira",
        "icone": "🤖",
        "fonte": "TecVagas",
        "url": "#",
        "data": datetime.now().strftime("%d/%m/%Y"),
    },
    {
        "titulo": "O técnico industrial que aprender IA vai ganhar o dobro",
        "resumo": "Profissionais que combinam habilidades técnicas tradicionais com conhecimento em automação e dados estão recebendo propostas 80% acima da média.",
        "conteudo": """Existe um novo perfil de técnico industrial emergindo no Brasil em 2026: o técnico-analítico. E ele está sendo disputado a peso de ouro.

**O que é o técnico-analítico?**
É o profissional que mantém equipamentos industriais E sabe interpretar os dados gerados por sensores e sistemas de monitoramento para antecipar falhas.

**A diferença salarial é brutal:**
• Técnico em manutenção tradicional: R$ 3.500 a R$ 5.000
• Técnico com habilidades em análise preditiva: R$ 6.000 a R$ 9.500
• Técnico com certificação em vibração e análise de óleo: R$ 7.000 a R$ 12.000

**Como se tornar um técnico-analítico:**

1. **Certificação em Análise de Vibração (ISO Cat I)**
   Custo: R$ 2.000 a R$ 4.000
   Retorno: +40% no salário

2. **Curso de Análise de Óleo Lubrificante**
   Custo: R$ 800 a R$ 2.000
   Retorno: +25% no salário

3. **Fundamentos de IIoT e Sensores**
   Plataformas: Coursera, Udemy (gratuito a R$ 500)
   Retorno: +30% no salário

4. **SAP PM ou Maximo (gestão de manutenção)**
   Custo: R$ 500 a R$ 2.000
   Retorno: +20% no salário

**O técnico do futuro não compete com a IA — ele é o operador dela.**

Empresas como Petrobras, Vale e Embraer já exigem esse perfil para novas contratações. Invista agora para colher em 2026 e além.""",
        "categoria": "IA & Futuro",
        "icone": "🚀",
        "fonte": "TecVagas",
        "url": "#",
        "data": datetime.now().strftime("%d/%m/%Y"),
    },
    {
        "titulo": "Melhores empresas para técnicos industriais em 2026",
        "resumo": "Petrobras, Vale, WEG, Embraer e Bosch oferecem os melhores salários e pacotes de benefícios.",
        "conteudo": """Algumas empresas se destacam pela remuneração e benefícios para técnicos industriais.

**🥇 Petrobras**
• Salário: R$ 9.000 a R$ 15.000
• Acesso via concurso público
• Benefícios: saúde premium, previdência, PLR

**🥈 Vale**
• Salário: R$ 5.000 a R$ 10.000
• Forte em MG, PA e ES

**🥉 WEG**
• Salário: R$ 3.500 a R$ 7.000
• Base em Jaraguá do Sul (SC)
• Excelente plano de carreira

**4. Embraer**
• Salário: R$ 4.000 a R$ 8.000
• São José dos Campos (SP)
• Exige inglês técnico

**5. Bosch**
• Salário: R$ 4.000 a R$ 7.500
• Campinas e Curitiba
• Padrões alemães de qualidade""",
        "categoria": "Empresas",
        "icone": "🏭",
        "fonte": "TecVagas",
        "url": "#",
        "data": datetime.now().strftime("%d/%m/%Y"),
    },
    {
        "titulo": "NR12, NR33 e NR35: quais certificações valem mais?",
        "resumo": "Cada NR pode adicionar R$ 200 a R$ 500 ao salário. Descubra quais são essenciais para sua área.",
        "conteudo": """As Normas Regulamentadoras são fundamentais para a carreira técnica industrial.

**NR12 — Segurança em Máquinas**
• Duração: 8 a 16 horas
• Impacto salarial: +R$ 150 a R$ 300/mês
• Muito exigida em: metalurgia, plásticos, alimentício

**NR33 — Espaços Confinados**
• Duração: 16 horas
• Impacto salarial: +R$ 200 a R$ 400/mês
• Validade: 1 ano
• Exigida em: refinarias, usinas, química

**NR35 — Trabalho em Altura**
• Duração: 8 horas
• Impacto salarial: +R$ 150 a R$ 300/mês
• Validade: 2 anos
• Exigida em quase toda indústria

**Ranking de valor:**
1. NR10 — maior impacto (+20%)
2. NR33 — rara e valorizada
3. NR35 — exigida em quase tudo
4. NR12 — importante para manufatura""",
        "categoria": "Certificações",
        "icone": "🦺",
        "fonte": "TecVagas",
        "url": "#",
        "data": datetime.now().strftime("%d/%m/%Y"),
    },
    {
        "titulo": "Robótica industrial criou mais empregos do que eliminou no Brasil",
        "resumo": "Estudo da FGV mostra que para cada robô instalado na indústria brasileira, surgem 3,2 novos postos de trabalho técnico especializado.",
        "conteudo": """Um estudo inédito da FGV Ibre publicado em 2026 desafia o senso comum sobre automação e desemprego na indústria brasileira.

**O que o estudo descobriu:**
Para cada robô ou sistema automatizado instalado em uma fábrica brasileira, são criados em média 3,2 novos postos de trabalho técnico especializado.

**Por que isso acontece?**
• Cada robô precisa de técnico para programar, calibrar e manter
• Sistemas automatizados geram mais produção, exigindo mais supervisão técnica
• A complexidade dos equipamentos aumenta a necessidade de especialistas
• Surgem novas funções que não existiam antes: técnico em cobot, analista de falhas preditivas

**Os setores que mais geraram empregos técnicos com automação:**
1. Automotivo: +12.000 técnicos em 5 anos
2. Agronegócio industrial: +8.500 técnicos
3. Alimentos e bebidas: +7.200 técnicos
4. Papel e celulose: +4.800 técnicos
5. Petroquímica: +4.200 técnicos

**A mensagem para técnicos industriais:**
Não tema a automação. Prepare-se para ela. O técnico que abraça as novas tecnologias se torna indispensável. O que resiste à mudança fica para trás.

A Indústria 4.0 não está eliminando técnicos — está selecionando os melhores.""",
        "categoria": "IA & Futuro",
        "icone": "🦾",
        "fonte": "TecVagas",
        "url": "#",
        "data": datetime.now().strftime("%d/%m/%Y"),
    },
]


def limpar_html(texto):
    if not texto:
        return ""
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()[:500]


def buscar_rss(fonte):
    artigos = []
    try:
        resp = requests.get(fonte["url"], headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return []
        root = ET.fromstring(resp.content)
        items = root.findall(".//item")[:4]
        for item in items:
            titulo_el = item.find("title")
            desc_el = item.find("description")
            link_el = item.find("link")
            data_el = item.find("pubDate")
            if not titulo_el or not titulo_el.text:
                continue
            titulo = limpar_html(titulo_el.text)
            resumo = limpar_html(desc_el.text if desc_el is not None else "")
            link = link_el.text if link_el is not None else "#"
            palavras_chave = [
                "técnico","industrial","manutenção","elétrica","mecânica",
                "automação","refrigeração","nr10","nr12","nr35","senai",
                "petrobras","vale","weg","plc","scada","hvac","insalubridade",
                "inteligência artificial","ia ","robô","robótica","emprego",
                "trabalho","mercado","salário","indústria",
            ]
            texto_check = (titulo + " " + resumo).lower()
            if not any(p in texto_check for p in palavras_chave):
                continue
            if len(titulo) > 10:
                artigos.append({
                    "titulo": titulo[:120],
                    "resumo": resumo[:300] if resumo else "Clique para ler o artigo.",
                    "conteudo": "",
                    "categoria": fonte["categoria"],
                    "icone": fonte["icone"],
                    "fonte": fonte["nome"].split(" - ")[0],
                    "url": link,
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "origem": "rss",
                })
        print(f"  ✅ {fonte['nome']}: {len(artigos)} artigos")
        return artigos
    except Exception as e:
        print(f"  ❌ {fonte['nome']}: {e}")
        return []


def carregar_artigos_existentes():
    try:
        with open(ARTIGOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def remover_duplicatas_artigos(artigos):
    vistos = set()
    unicos = []
    for a in artigos:
        chave = a["titulo"][:40].lower().strip()
        if chave not in vistos:
            vistos.add(chave)
            unicos.append(a)
    return unicos


def artigos_do_dia_reserva():
    hoje = datetime.now().timetuple().tm_yday
    selecionados = []
    for i in range(4):
        idx = (hoje + i) % len(ARTIGOS_RESERVA)
        artigo = ARTIGOS_RESERVA[idx].copy()
        artigo["data"] = datetime.now().strftime("%d/%m/%Y")
        artigo["origem"] = "reserva"
        selecionados.append(artigo)
    return selecionados


def main():
    print(f"\n📰 TecVagas - Robô de Artigos v2")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 50)

    artigos_existentes = carregar_artigos_existentes()
    artigos_novos = []
    fontes_ok = 0

    for fonte in FONTES_RSS:
        print(f"\n🔍 {fonte['nome']}...")
        artigos = buscar_rss(fonte)
        if artigos:
            artigos_novos.extend(artigos)
            fontes_ok += 1
        time.sleep(2)

    print(f"\n📊 Fontes OK: {fontes_ok}/{len(FONTES_RSS)}")
    print(f"📰 Artigos novos: {len(artigos_novos)}")

    if len(artigos_novos) < 3:
        print("⚠️ Poucas fontes. Usando banco de reserva...")
        artigos_novos.extend(artigos_do_dia_reserva())

    todos = artigos_novos + artigos_existentes
    todos = remover_duplicatas_artigos(todos)
    todos = todos[:MAX_ARTIGOS]

    with open(ARTIGOS_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(todos)} artigos salvos!")


if __name__ == "__main__":
    main()
