"""
TecSystem Brasil - Robô de Artigos v1
========================================
Busca notícias técnicas industriais de múltiplas fontes RSS.
Tem banco de artigos de reserva caso todas as fontes falhem.
Roda todo dia às 8h via GitHub Actions.
"""

import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time
import random
import re
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

ARTIGOS_FILE = "artigos.json"
MAX_ARTIGOS = 20  # máximo de artigos no site

# ─── FONTES RSS ───────────────────────────────────────────────────────────────

FONTES_RSS = [
    # Google News - termos técnicos industriais
    {
        "nome": "Google News - Manutenção Industrial",
        "url": "https://news.google.com/rss/search?q=manutenção+industrial+técnico&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Manutenção",
        "icone": "🔧",
    },
    {
        "nome": "Google News - Automação Industrial",
        "url": "https://news.google.com/rss/search?q=automação+industrial+técnico+PLC&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Automação",
        "icone": "🤖",
    },
    {
        "nome": "Google News - Mercado Técnico",
        "url": "https://news.google.com/rss/search?q=técnico+industrial+emprego+salário+2026&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Mercado",
        "icone": "📊",
    },
    {
        "nome": "Google News - NR Segurança",
        "url": "https://news.google.com/rss/search?q=NR10+NR35+NR12+segurança+trabalho+industrial&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Segurança",
        "icone": "🦺",
    },
    {
        "nome": "Google News - Elétrica Industrial",
        "url": "https://news.google.com/rss/search?q=elétrica+industrial+eletricista+técnico&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Elétrica",
        "icone": "⚡",
    },
    {
        "nome": "Google News - Refrigeração Industrial",
        "url": "https://news.google.com/rss/search?q=refrigeração+industrial+HVAC+técnico&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Refrigeração",
        "icone": "❄️",
    },
    {
        "nome": "Google News - Indústria 4.0",
        "url": "https://news.google.com/rss/search?q=indústria+4.0+técnico+robótica+CNC&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Tecnologia",
        "icone": "🏭",
    },
    {
        "nome": "Google News - Petróleo Gás",
        "url": "https://news.google.com/rss/search?q=petróleo+gás+técnico+offshore+manutenção&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "categoria": "Petróleo & Gás",
        "icone": "🛢️",
    },
]

# ─── BANCO DE ARTIGOS DE RESERVA ─────────────────────────────────────────────
# Usados quando todas as fontes online falham

ARTIGOS_RESERVA = [
    {
        "titulo": "Quanto ganha um Técnico em Manutenção Elétrica em 2026?",
        "resumo": "O técnico em manutenção elétrica é um dos profissionais mais requisitados na indústria brasileira. Em 2026, os salários variam de R$ 2.800 a R$ 6.500 dependendo da região, empresa e experiência. Em estados como São Paulo e Rio de Janeiro, os valores chegam a superar R$ 7.000 com adicionais de insalubridade e periculosidade. Certificações como NR10 e NR35 podem aumentar o salário em até 30%. Grandes empresas como Petrobras, Vale e WEG oferecem os melhores pacotes de benefícios para esses profissionais.",
        "categoria": "Salários",
        "icone": "⚡",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "NR10: Guia Completo para Técnicos Elétricos em 2026",
        "resumo": "A NR10 é obrigatória para todos os profissionais que trabalham com instalações elétricas no Brasil. Em 2026, o curso básico tem duração de 40 horas e o de segurança em eletricidade de 40 horas adicionais. O valor médio do curso varia de R$ 400 a R$ 1.200 dependendo da instituição. O SENAI oferece cursos credenciados em todo o Brasil com valores mais acessíveis. A validade é de 2 anos e a reciclagem é obrigatória. Técnicos com NR10 têm prioridade nas contratações e salários até 25% maiores.",
        "categoria": "Certificações",
        "icone": "📋",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Técnico em Automação Industrial: a profissão que mais cresce no Brasil",
        "resumo": "Com a expansão da Indústria 4.0, o técnico em automação industrial tornou-se um dos profissionais mais disputados do mercado. Empresas de todos os setores buscam profissionais com conhecimento em PLC, SCADA, CLP e redes industriais. Em 2026, a demanda cresceu 35% em relação ao ano anterior. Os salários médios variam de R$ 3.500 a R$ 8.000. Cursos técnicos do SENAI em automação industrial têm duração de 18 a 24 meses e garantem alta empregabilidade. Estados como São Paulo, Santa Catarina e Paraná concentram a maior parte das vagas.",
        "categoria": "Carreira",
        "icone": "🤖",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Melhores empresas para técnicos industriais em 2026",
        "resumo": "Algumas empresas se destacam pela remuneração e benefícios oferecidos aos técnicos industriais. Petrobras lidera o ranking com salários que chegam a R$ 12.000 para técnicos sêniores. Vale, WEG, Embraer, Bosch e Fiat também aparecem entre as melhores. Benefícios incluem plano de saúde, previdência privada, PLR e vale alimentação. Para concorrer a essas vagas, é fundamental ter curso técnico completo, certificações NR e experiência mínima de 2 anos. Fique de olho nas vagas abertas aqui no TecSystem Brasil.",
        "categoria": "Empresas",
        "icone": "🏭",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "NR12, NR33 e NR35: quais certificações valem mais para técnicos?",
        "resumo": "As normas regulamentadoras são fundamentais para a carreira técnica industrial. A NR12 (segurança em máquinas) é exigida em praticamente todas as indústrias de manufatura. A NR33 (espaços confinados) é obrigatória em refinarias, usinas e plantas químicas. A NR35 (trabalho em altura) é indispensável para técnicos de manutenção. Cada certificação pode adicionar de R$ 200 a R$ 500 ao salário mensal. O ideal é ter pelo menos 3 certificações NR para se destacar no mercado. O SENAI e diversas empresas privadas oferecem os cursos.",
        "categoria": "Certificações",
        "icone": "🦺",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Como passar na entrevista para técnico industrial em 2026",
        "resumo": "As entrevistas para técnicos industriais têm características específicas que todo candidato precisa conhecer. Além das perguntas comportamentais tradicionais, é comum haver testes técnicos práticos com leitura de esquemas elétricos, diagramas hidráulicos ou programação de CLP. Prepare-se para descrever situações reais de manutenção preventiva e corretiva que você já realizou. Chegue com seus certificados NR organizados. Pesquise sobre a empresa antes — conheça os equipamentos que ela opera. A pontualidade e apresentação são muito valorizadas no setor industrial.",
        "categoria": "Dicas",
        "icone": "💼",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Técnico em Refrigeração Industrial: mercado aquecido em 2026",
        "resumo": "O técnico em refrigeração industrial vive um momento de grande demanda no Brasil. Com o crescimento do setor alimentício, farmacêutico e de data centers, as oportunidades nunca foram tão grandes. Em 2026, há déficit de profissionais qualificados em HVAC e refrigeração industrial. Os salários variam de R$ 3.000 a R$ 7.000, com grandes empresas oferecendo até R$ 9.000 para especialistas em sistemas de amônia. O curso técnico tem duração de 18 meses e o SENAI oferece formações reconhecidas pelo mercado. Certificações em gases refrigerantes são um diferencial.",
        "categoria": "Mercado",
        "icone": "❄️",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Indústria 4.0: o que o técnico industrial precisa saber",
        "resumo": "A transformação digital chegou às fábricas e os técnicos industriais precisam se atualizar. Em 2026, conhecimentos em IoT industrial, manutenção preditiva com sensores, análise de vibração e sistemas SCADA são diferenciais competitivos. Empresas como Siemens, ABB e Rockwell Automation oferecem treinamentos especializados. Técnicos que dominam programação de PLC Siemens S7 e Allen Bradley têm salários até 40% maiores. O SENAI possui cursos de indústria 4.0 em parceria com as principais fabricantes de automação. Invista em qualificação para se destacar.",
        "categoria": "Tecnologia",
        "icone": "🔬",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Salário de Técnico em Mecatrônica por estado em 2026",
        "resumo": "O técnico em mecatrônica é um dos perfis mais versáteis da indústria, combinando conhecimentos de mecânica, elétrica e automação. Em São Paulo, o salário médio é de R$ 4.200. No Rio de Janeiro chega a R$ 3.900. Em Santa Catarina e Paraná, onde há forte presença do setor metal-mecânico, os valores chegam a R$ 4.800. Na Bahia, com as montadoras e o polo petroquímico, os salários variam de R$ 3.500 a R$ 5.500. O diferencial do mecatrônico é poder atuar em manutenção elétrica, mecânica e de sistemas automatizados simultaneamente.",
        "categoria": "Salários",
        "icone": "⚙️",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "PCM: Planejamento e Controle de Manutenção — o que é e como funciona",
        "resumo": "O PCM (Planejamento e Controle de Manutenção) é uma área estratégica nas indústrias modernas. O técnico em PCM é responsável por planejar, programar e controlar todas as atividades de manutenção da planta. Em 2026, a demanda por técnicos com conhecimento em SAP PM, Maximo e outros sistemas de gestão de manutenção cresceu 45%. Os salários variam de R$ 3.800 a R$ 7.500. Para atuar na área, além do curso técnico, é fundamental ter conhecimento em indicadores como MTBF, MTTR e disponibilidade de equipamentos. O SENAI e instituições privadas oferecem cursos específicos.",
        "categoria": "Carreira",
        "icone": "📊",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Concurso Petrobras 2026: tudo sobre as vagas para técnicos",
        "resumo": "A Petrobras é um dos empregadores mais desejados pelos técnicos industriais brasileiros. Em 2026, o concurso prevê aproximadamente 1.100 vagas para técnicos de manutenção nas áreas elétrica, mecânica, instrumentação e caldeiraria. Os salários iniciais chegam a R$ 9.500 com benefícios que incluem plano de saúde premium, previdência privada e PLR. Os requisitos incluem curso técnico completo na área e registro no conselho de classe. As provas são realizadas pela Cesgranrio e incluem conhecimentos específicos da área técnica. Fique atento ao edital.",
        "categoria": "Concursos",
        "icone": "🛢️",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Manutenção Preditiva: o futuro da manutenção industrial",
        "resumo": "A manutenção preditiva está revolucionando a indústria brasileira. Ao contrário da manutenção corretiva (consertar quando quebra) e preventiva (manutenção programada), a preditiva monitora o estado real dos equipamentos. Técnicas como análise de vibração, termografia, análise de óleo e ultrassom permitem prever falhas antes que ocorram. Em 2026, técnicos com certificação em análise de vibração (ISO Cat I e II) têm salários 35% acima da média. Empresas como Vale, CSN e Usiminas já operam com manutenção 100% preditiva em equipamentos críticos.",
        "categoria": "Tecnologia",
        "icone": "🔍",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Como montar um currículo de técnico industrial que chama atenção",
        "resumo": "Um bom currículo pode ser a diferença entre conseguir ou não uma entrevista. Para técnicos industriais, liste todas as certificações NR com data de validade. Destaque os equipamentos e sistemas que você já operou ou manteve. Mencione as empresas onde trabalhou e o porte delas. Coloque os softwares que domina (SAP, AutoCAD, WEG Motor Scan, etc). Use palavras-chave da área como preventiva, corretiva, MTBF, ordem de serviço. Mantenha o currículo em no máximo 2 páginas. Uma foto profissional aumenta em 40% as chances de ser chamado para entrevista.",
        "categoria": "Dicas",
        "icone": "📄",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Técnico em Soldagem: especialidade com alta demanda em 2026",
        "resumo": "O técnico em soldagem é um profissional altamente especializado e muito valorizado na indústria. Em 2026, há déficit de mais de 50.000 soldadores qualificados no Brasil, segundo a Associação Brasileira de Soldagem. Os salários variam de R$ 3.500 a R$ 9.000 dependendo do processo de soldagem dominado. Processos como TIG, MIG/MAG e soldagem subaquática têm as maiores remunerações. Certificações pela AWS (American Welding Society) ou ASME são grandes diferenciais. O setor de petróleo e gás, construção naval e indústria pesada são os maiores empregadores.",
        "categoria": "Mercado",
        "icone": "🔥",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Trabalho em turno: vantagens e desvantagens para técnicos industriais",
        "resumo": "Grande parte das vagas para técnicos industriais envolve trabalho em turnos rotativos ou fixos. Os regimes mais comuns são 12x36 (12 horas de trabalho por 36 de descanso), 2x2 e turno fixo noturno. O adicional noturno de 20% e horas extras podem aumentar significativamente o salário. No regime 12x36, o técnico trabalha em média 15 dias por mês, tendo mais tempo livre. É importante considerar os impactos na saúde e vida social antes de aceitar posições em turno. Use nossa calculadora de adicional noturno para calcular exatamente quanto você vai receber.",
        "categoria": "Dicas",
        "icone": "🌙",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "SENAI: os melhores cursos técnicos industriais para fazer em 2026",
        "resumo": "O SENAI é a principal instituição de formação técnica industrial do Brasil, com mais de 500 unidades espalhadas pelo país. Em 2026, os cursos mais procurados são: Automação Industrial, Eletrotécnica, Mecatrônica, Manutenção Industrial e Refrigeração. A duração varia de 18 a 24 meses para os cursos técnicos completos. Os valores são subsidiados pelo sistema S e muito inferiores às faculdades privadas. O SENAI também oferece cursos de curta duração em NRs, soldagem certificada e programação de CLP. A empregabilidade dos egressos do SENAI supera 85%.",
        "categoria": "Educação",
        "icone": "🎓",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Insalubridade e Periculosidade: técnicos industriais têm direito?",
        "resumo": "Muitos técnicos industriais têm direito a adicionais de insalubridade ou periculosidade mas não sabem disso. A insalubridade é devida quando o trabalho expõe o profissional a agentes nocivos acima dos limites de tolerância. Os percentuais são: mínimo (10% do salário mínimo), médio (20%) e máximo (40%). A periculosidade (30% sobre o salário) é devida para quem trabalha com inflamáveis, explosivos ou eletricidade em alta tensão. Técnicos elétricos que trabalham com tensões acima de 50V em corrente alternada geralmente têm direito à periculosidade. Use nossa calculadora para saber quanto você tem a receber.",
        "categoria": "Direitos",
        "icone": "⚠️",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Vale, Petrobras ou WEG: onde é melhor trabalhar como técnico?",
        "resumo": "Três das maiores empregadoras de técnicos industriais do Brasil têm perfis bem diferentes. A Petrobras oferece os maiores salários (R$ 9.000 a R$ 15.000) mas exige aprovação em concurso público rigoroso. A Vale tem salários de R$ 5.000 a R$ 10.000 com forte atuação na mineração e requer disponibilidade para trabalho em mina e turno. A WEG, gigante catarinense de motores elétricos, paga de R$ 3.500 a R$ 7.000 com excelente ambiente de trabalho e plano de carreira. Cada empresa tem sua cultura — pesquise qual combina mais com seu perfil antes de se candidatar.",
        "categoria": "Empresas",
        "icone": "🏆",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Técnico em Instrumentação: alta demanda no setor de petróleo e gás",
        "resumo": "O técnico em instrumentação industrial é especializado em calibração, manutenção e instalação de instrumentos de medição e controle. Em 2026, é um dos perfis mais escassos e valorizados da indústria. No setor de petróleo e gás, os salários chegam a R$ 12.000 com adicionais. A formação exige conhecimento em transmissores de pressão, temperatura, vazão e nível, além de válvulas de controle e sistemas de segurança instrumentada (SIS). Certificações pela ISA (International Society of Automation) são muito valorizadas. O SENAI oferece curso técnico em instrumentação industrial com duração de 20 meses.",
        "categoria": "Carreira",
        "icone": "📡",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
    {
        "titulo": "Como negociar salário em uma entrevista de emprego técnico",
        "resumo": "Negociar salário é uma habilidade que poucos técnicos dominam mas que pode fazer grande diferença na carreira. Primeiro, pesquise a faixa salarial para sua especialidade e região — use plataformas como Glassdoor e a calculadora do TecSystem Brasil. Nunca dê um número antes da empresa. Se perguntado, diga que está aberto a discutir com base no pacote completo. Considere todos os benefícios: plano de saúde, VT, VA, PLR e possibilidade de crescimento. Técnicos com certificações NR atualizadas têm mais poder de negociação. Uma contraproposta de 10 a 20% acima do oferecido é sempre razoável.",
        "categoria": "Dicas",
        "icone": "💰",
        "fonte": "TecSystem Brasil",
        "url": "#",
    },
]


# ─── FUNÇÕES DE BUSCA RSS ─────────────────────────────────────────────────────

def limpar_html(texto):
    """Remove tags HTML do texto."""
    if not texto:
        return ""
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()[:500]


def buscar_rss(fonte):
    """Busca artigos de uma fonte RSS."""
    artigos = []
    try:
        resp = requests.get(fonte["url"], headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"  ⚠️ {fonte['nome']}: HTTP {resp.status_code}")
            return []

        root = ET.fromstring(resp.content)
        items = root.findall(".//item")[:5]

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
            data_pub = data_el.text if data_el is not None else ""

            # Filtra só conteúdo relevante para área técnica
            palavras_chave = [
                "técnico", "industrial", "manutenção", "elétrica", "mecânica",
                "automação", "refrigeração", "soldagem", "caldeiraria", "instrumentação",
                "nr10", "nr12", "nr35", "senai", "petrobras", "vale", "weg",
                "plc", "scada", "cnc", "hvac", "insalubridade", "periculosidade",
            ]
            texto_check = (titulo + " " + resumo).lower()
            if not any(p in texto_check for p in palavras_chave):
                continue

            # Filtra notícias muito antigas (mais de 30 dias)
            try:
                from email.utils import parsedate_to_datetime
                data_obj = parsedate_to_datetime(data_pub)
                if (datetime.now(data_obj.tzinfo) - data_obj).days > 30:
                    continue
            except:
                pass

            if len(titulo) > 10:
                artigos.append({
                    "titulo": titulo[:120],
                    "resumo": resumo[:400] if resumo else "Clique para ler o artigo completo.",
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


# ─── PRINCIPAL ────────────────────────────────────────────────────────────────

def carregar_artigos_existentes():
    """Carrega artigos já salvos."""
    try:
        with open(ARTIGOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def remover_duplicatas_artigos(artigos):
    """Remove artigos duplicados por título."""
    vistos = set()
    unicos = []
    for a in artigos:
        chave = a["titulo"][:40].lower().strip()
        if chave not in vistos:
            vistos.add(chave)
            unicos.append(a)
    return unicos


def artigos_do_dia_reserva():
    """Seleciona artigos do banco de reserva de forma rotativa."""
    hoje = datetime.now().timetuple().tm_yday  # dia do ano (1-365)
    indice = hoje % len(ARTIGOS_RESERVA)
    # Pega 3 artigos rotacionando pelo dia do ano
    selecionados = []
    for i in range(3):
        idx = (indice + i) % len(ARTIGOS_RESERVA)
        artigo = ARTIGOS_RESERVA[idx].copy()
        artigo["data"] = datetime.now().strftime("%d/%m/%Y")
        artigo["origem"] = "reserva"
        selecionados.append(artigo)
    return selecionados


def main():
    print(f"\n📰 TecSystem Brasil - Robô de Artigos")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 50)

    # Carrega artigos existentes
    artigos_existentes = carregar_artigos_existentes()
    print(f"📚 Artigos existentes: {len(artigos_existentes)}")

    # Busca artigos novos de todas as fontes
    artigos_novos = []
    fontes_com_sucesso = 0

    for fonte in FONTES_RSS:
        print(f"\n🔍 Buscando: {fonte['nome']}...")
        artigos = buscar_rss(fonte)
        if artigos:
            artigos_novos.extend(artigos)
            fontes_com_sucesso += 1
        time.sleep(2)  # respeita os servidores

    print(f"\n📊 Fontes com sucesso: {fontes_com_sucesso}/{len(FONTES_RSS)}")
    print(f"📰 Artigos novos encontrados: {len(artigos_novos)}")

    # Se poucas fontes funcionaram, adiciona artigos de reserva
    if len(artigos_novos) < 3:
        print("⚠️ Poucas fontes online funcionaram. Usando banco de reserva...")
        artigos_novos.extend(artigos_do_dia_reserva())

    # Combina novos com existentes (novos primeiro)
    todos = artigos_novos + artigos_existentes

    # Remove duplicatas
    todos = remover_duplicatas_artigos(todos)

    # Mantém só os mais recentes
    todos = todos[:MAX_ARTIGOS]

    print(f"✅ Total de artigos: {len(todos)}")

    # Salva artigos
    with open(ARTIGOS_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

    print(f"💾 Artigos salvos em {ARTIGOS_FILE}")
    print("✅ Robô de artigos concluído!")


if __name__ == "__main__":
    main()
