import os
import yaml
from crewai import Agent, Task, Crew, Process
from langchain.chat_models import ChatOpenAI
from crewai_tools import PDFSearchTool
from dotenv import load_dotenv
from crewai import LLM

# carregar variavel de ambiente
#load_dotenv()
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Api chatgpt
#os.environ["OPENAI_API_KEY"] = 'sk-ESQVwjEmNpgyq30GFQpYFD_Pgmn9JZq52Dbo7nmFSWT3BlbkFJZOK7U42F_mqSUK8cbOeFjC6HfveDLI6voRZjK4tqIA'


# Carregar pasta de pdfs
pdf_folder = r"PDFs"
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

# Variaveis
all_articles = []

solicitacoes = """
\n<solicitacoes>\n
1 - OBJETIVOS - Identificação dos Objetivos: Realize uma anákise cuidadosa do conteúdo do trabalho para extrair os objetivos principais. Resuma esses objetivos em um paragráfo claro e conciso, capturando a essencia das metas e inteções do estudo.\n
2 - GAP - Identificação do GAP: Analise o conteúdo do trabalho para identificar o GAP científico que ele aborda, mesmo que não esteja explicitamente mencionado. Formule um paragráfo conciso, focando em destacar a questão central que o estudo procura resolver ou elucidar.\n
3 - METODOLOGIA - Extração Detalhada da Metodologia: Identificação e Descrição Detalhada da Metodologia. Proceda com uma análise minuciosa para identificar a metodologia utilizada. Detalhe cada aspecto da metodologia utilizada. Detalhe cada aspecto da metodolgia, incluindo o desenho de estudo, as técnicas e ferramentas empregadas.\n
4 - DATASET - Identifique os datasets usados no trabalho. Descreva-os brevemente em texto corrido, limitando-se a 40 palavras. Quero somente o nome dos dataset na mesma linha e separados por virgula. Se o dataset na mesma linha e separados por virgula. Se o dataset foi criado pelos autores escreve "OWN DATASET".\n
5 - RESULTADOS -  Escreva um parágrafo os resultados obtidos no estudo dando enfase a dados quantitativos, quero dados uméricos explicitamente. Nesse parágrafo também dê enfase a comparação ao melhor trabalho anterioe em relação ao trabalho proposto. Não use superlativos. Deixe o tom neutro e científico.\n
6 - LIMITAÇÕES - Produza um texto parafraseado sobre as limitações do trabalho.\n
7 - CONCLUSãO - Resuma as conclusões dos autores em relação ao trabalho.\n
8 - FUTURO - Extraia as Recomendações para a Pesquisa Futura: Aponte recomedações para futuras investigações baseadas nas conclusões do artigo.\n
9 - AVALIAÇÃO - Faça uma avaliação crítica ao trabalho. Não seja generalista faça uma crítica aprofundada.\n
</solicitacoes>\n
"""

controles = """
\n<controles>\n
NÍVEIS DE CONTROLE:\n
1. Entonação: Formal CIentífico.\n
2. Foco de Tópico: voce deve responder sempre com alto foco no texto do artigo científico.\n
3. Língua: Responda sempre em Português do Brasil como os Brasileiros costuman escrever testos científicos aderindo aos padrões de redação cientifica do país a não ser o que será especificado para não traduzir.\n
4. Controle de Sentimento: Neutro e científico. Evite superlativos como: inovador, revolucionario e etc.\n
5. Nível de originalidade: 10, onde 1 é pouco original e 10 é muito original. Em hipótese alguma copie frases do texto original.\n
6. Nível de Abstraçã: 1, onde 1 é muito concreto e real e 10 é muito abstrato e irreal.\n
7. Tempo Verbal: Escreva no passado.\n
</controles>\n
"""

restricoes = """
\n<restricoes>\n
O QUE NÃO DEVE SER TRADUZIDO DO INGLÊS PARA O PORTUGUES:\n
1. Termos técnicos em inglês amplamente aceitos e usados nos texto em português.\n
2. Nome de algoritimos de machine learning.\n
3. Métricas usadas no trabalho.\n
4. Nome dos datasets.\n
</restricoes>\n
"""

# Template YAML
template = """
\n<template>\n
artigo:\n
  - artigo: "nome do arquivo.pdf"\n
  - OBJETIVOS: "Objetivo geral e específicos"\n
  - GAP: "Gap científico"\n
  - METODOLOGIA: "Metodologia"\n
  - DATASET: "Datasets utilizados"\n
  - RESULTADOS: "Resultados do artigo"\n
  - LIMITAÇÕES: "Limitações do artigo"\n
  - CONCLUSÃO: "Conclusão do artigo"\n
  - FUTURO: "Recomendações para o futuro"\n
  - AVALIAÇÃO: "Avaliação do artigo"\n
</template>\n
"""

def create_agent_leitor(llm, tool):
  return Agent(
      role = 'PDF Reader',
      goal = 'Ler PDFs e extrair informações específicas conforme definido nas solicitações em <solicitacoes>.'
             'Gerar um YAML de acordo com modelo especificado em <template>. {solicitacoes} {template}.',
      backstory = "Você é um especialista em leitura e análise de artigos científicos."
                  "Sua missão é extrair informações cruciais, compreendo o contexto semântico completo dos artigos"
                  "Sua função é fundamental para avaliar a relevância dos artigos analisados "
                  "Ao responder às solicitações delimitadas por <solicitacoes></solicitacoes>, "
                  "Você deve levar em consideração as definições de controles em <controles></controles>"
                  "e as restrições em <restricoes></restricoes>"
                  "{solicitacoes} {template} {restricoes} {controles}",
      tools = [tool],
      verbose=True,
      memory=False,
      llm = llm
  )

def create_agent_revisor(llm):
  return Agent(
      role = "Revisor de leitura",

      goal = "Leia os dados extraídos pelo Agente Revisor e verifique se um YAML foi produzido "
             "de acordo com o template proposto em <template>"
             "com os dados solicitados em <solicitacoes> "
             "Com resultado do seu trabalho, você deve retornar um YAML "
             "revisando no mesmo formato do template proposto. {solicitacoes} {template}",

      backstory = "Você é um especialista em revisão de informações em YAML, "
                  "especialmente de resumos de artigos científicos."
                  "Sua função é garantir que os dados extraídos reflitam "
                  "com precisão as solicitações definidas em <solicitacoes> "
                  "e estejam formatadas conforme o template proposto em <template>. "
                  "Sua atenção aos detalhes assegura que os resultados finais "
                  "sejam precisos e conformes às expectativas. {solicitacoes} {template}",

      verbose = True,
      memory = False,
      llm = llm
  )

def leitor_task(agent_leitor):
  return Task(
      description = "Leia o PDF e responda em YAML às solicitações definidas em <solicitacoes> "
          "usando o modelo definido em <template>. "
          "{solicitacoes} {template}",
      expected_output = "YAML com as respostas às solicitações definidas em "
                        "<solicitacoes> usando o modelo definido em <template>. ",
      agent = agent_leitor

  )

def revisor_task(agent_revisor):
  return Task(
      description = "Revise o YAML produzido pelo agente leitor para garantir que ele esteja de acordo com o template defin "
                    "e contenha todas as informações solicitadas em <solicitacoes>. {solicitacoes} {template}",

      expected_output = "YAML revisado que esteja de acordo com o template definido em <template>"
                        "e contenha todas as informações solicitadas em <solicitacoes>. (solicitacoes) {template}",
      agent = agent_revisor
  )

# Programa main
import os
import yaml
from typing import List


for pdf_file_name in pdf_files:

  gpt = LLM(
    model="ollama/mistral",
    base_url="http://localhost:11434"
  )

  pdf = os.path.join(pdf_folder, pdf_file_name)

 # pdf_tool = PDFSearchTool(pdf)

  pdf_tool = PDFSearchTool(pdf,
    config=dict(
        llm=dict(
            provider="ollama", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="mistral",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="ollama", # or openai, ollama, ...
            config=dict(
                model="mistral",
                #task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)

  agent_leitor = create_agent_leitor(gpt, pdf_tool)
  task_leitor = leitor_task(agent_leitor)

  agent_revisor = create_agent_revisor(gpt)
  task_revisor = revisor_task(agent_revisor)

  crew = Crew(
      agents = [agent_leitor, agent_revisor],
      tasks = [task_leitor, task_revisor],
      process=Process.sequential,
      verbose=True
  )

  inputs = {
      'solicitacoes': solicitacoes,
      'controles': controles,
      'restricoes': restricoes,
      'template': template
  }

  results = crew.kickoff(inputs)
  print(f'Primeiro Resultado: {results} \n')
  results = results.raw.replace("```yaml\n", "").replace("\n```", "").replace("-", "")
  print(results)

  article_data = yaml.safe_load(results)
  all_articles.append(article_data)

final_output = {'artigos':  all_articles}

file_name = 'output.yaml'

with open(file_name, 'w') as file:
  yaml.dump(final_output, file, default_flow_style=False, allow_unicode=True)
print(f'Dados salvos em {file_name}')