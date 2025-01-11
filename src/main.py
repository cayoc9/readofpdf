# Programa main
import os
import yaml
from crewai_tools import PDFSearchTool
from crewai import LLM, Crew, Process
from config import pdf_files, pdf_folder, solicitacoes, controles, restricoes, template
from config import create_agent_leitor, create_agent_revisor, leitor_task, revisor_task
from config import all_articles
import re

# Função para limpar e validar YAML
def clean_and_validate_yaml(yaml_string):
    # Remover caracteres extras ou formatação inesperada
    yaml_string = re.sub(r'```yaml\n|```', '', yaml_string.strip())

    # Adicionar aspas onde necessário (caso contenha caracteres especiais)
    def add_quotes(match):
        return f'{match.group(1)}: "{match.group(2)}"'
    
    yaml_string = re.sub(r'(^\s*\w+):\s*(.+)$', add_quotes, yaml_string, flags=re.MULTILINE)
    
    return yaml_string


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
                model="phi4",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="ollama", # or openai, ollama, ...
            config=dict(
                model="phi4",
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
  results = results.raw.replace("```yaml\n", "").replace("\n```", "")

  article_data = yaml.safe_load(results)
  all_articles.append(article_data)

final_output = {'artigos':  all_articles}

file_name = 'output.yaml'

with open(file_name, 'w') as file:
  yaml.dump(final_output, file, default_flow_style=False, allow_unicode=True)
print(f'Dados salvos em {file_name}')