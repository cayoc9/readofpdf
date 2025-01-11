import os
import yaml
import tracemalloc
from crewai_tools import PDFSearchTool
from crewai import LLM, Crew, Process
from config import (
    pdf_files, pdf_folder, solicitacoes, controles, restricoes, template,
    create_agent_leitor, create_agent_revisor, leitor_task, revisor_task,
    all_articles
)
import gc  # Para forçar a coleta de lixo
from concurrent.futures import ProcessPoolExecutor

# Inicia o monitoramento de memória
tracemalloc.start()

# Configuração do modelo e embeddings
config = dict(
    llm=dict(
        provider="ollama",
        config=dict(
            model="phi4",
        ),
    ),
    embedder=dict(
        provider="ollama",
        config=dict(
            model="phi4",
        ),
    ),
)

def process_pdf(pdf_file_name):
    # Criação do LLM
    gpt = LLM(
        model="ollama/mistral",
        base_url="http://localhost:11434"
    )

    # Caminho do PDF
    pdf = os.path.join(pdf_folder, pdf_file_name)

    # Criação do PDFSearchTool
    pdf_tool = PDFSearchTool(pdf, config=config)

    try:
        # Configuração dos agentes e tarefas
        agent_leitor = create_agent_leitor(gpt, pdf_tool)
        task_leitor = leitor_task(agent_leitor)

        agent_revisor = create_agent_revisor(gpt)
        task_revisor = revisor_task(agent_revisor)

        # Configuração do Crew
        crew = Crew(
            agents=[agent_leitor, agent_revisor],
            tasks=[task_leitor, task_revisor],
            process=Process.sequential,
            verbose=True
        )

        # Inputs para as tarefas
        inputs = {
            'solicitacoes': solicitacoes,
            'controles': controles,
            'restricoes': restricoes,
            'template': template
        }

        # Execução das tarefas
        results = crew.kickoff(inputs)
        results = results.raw.replace("```yaml\n", "").replace("\n```", "").replace("-", "")
        return results + '\n'

    finally:
        # Fechamento explícito de recursos
        if hasattr(pdf_tool, "close"):
            pdf_tool.close()
        if hasattr(gpt, "shutdown"):
            gpt.shutdown()

        # Força a coleta de lixo após o processamento de cada PDF
        gc.collect()

# Processamento paralelo dos PDFs
with ProcessPoolExecutor() as executor:
    results = list(executor.map(process_pdf, pdf_files))
    all_articles.extend(results)

# Grava os resultados em um arquivo YAML
file_name = 'output.yaml'
with open(file_name, 'w', encoding='utf-8') as file:
    file.write('\n'.join(all_articles).strip())

print(f"Conteúdo salvo em '{file_name}' com sucesso!")

# Exibe o uso de recursos
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 10 Resource Usage ]")
for stat in top_stats[:10]:
    print(stat)
