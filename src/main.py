# Programa main
import os
import yaml
from crewai_tools import PDFSearchTool
from crewai import LLM, Crew, Process
from config import pdf_files, pdf_folder, solicitacoes, controles, restricoes, template
from config import create_agent_leitor, create_agent_revisor, leitor_task, revisor_task
from config import all_articles
import tracemalloc
tracemalloc.start()


for pdf_file_name in pdf_files:

  gpt = LLM(
    model="ollama/mistral",
    base_url="http://localhost:11434"
  )

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

  pdf = os.path.join(pdf_folder, pdf_file_name)

 # pdf_tool = PDFSearchTool(pdf)

  pdf_tool = PDFSearchTool(pdf, config=config)
  
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
  results = results.raw.replace("```yaml\n", "").replace("\n```", "").replace("-", "")
  all_articles.append(results + '\n')
  
file_name = 'output.yaml'

# Grava todos os artigos concatenados no arquivo.
with open(file_name, 'w', encoding='utf-8') as file:
    file.write('\n'.join(all_articles).strip()) 

print(f"Conteúdo salvo em '{file_name}' com sucesso!")

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 10 Resource Usage ]")
for stat in top_stats[:10]:
    print(stat)