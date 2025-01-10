import os
import yaml
from crewai import LLM, Crew
from utils import load_pdfs
from agents import create_agent_leitor, create_agent_revisor
from tasks import leitor_task, revisor_task
from config import solicitacoes, controles, restricoes, template
from crewai_tools import PDFSearchTool

# Carregar arquivos PDF
pdf_folder = r"PDFs"
pdf_files = load_pdfs(pdf_folder)

all_articles = []

for pdf_file_name in pdf_files:
    gpt = LLM(
        model="ollama/mistral",
        base_url="http://localhost:11434"
    )

    pdf = os.path.join(pdf_folder, pdf_file_name)

    # Criar ferramenta PDFSearchTool
    pdf_tool = PDFSearchTool(
        pdf,
        config=dict(
            llm=dict(
                provider="ollama",
                config=dict(model="mistral"),
            ),
            embedder=dict(
                provider="ollama",
                config=dict(model="mistral"),
            ),
        )
    )

    # Criar agentes e tarefas
    agent_leitor = create_agent_leitor(gpt, pdf_tool)
    task_leitor = leitor_task(agent_leitor)
    agent_revisor = create_agent_revisor(gpt)
    task_revisor = revisor_task(agent_revisor)

    # Configurar Crew
    crew = Crew(
        agents=[agent_leitor, agent_revisor],
        tasks=[task_leitor, task_revisor],
        process=Crew.Process.sequential,
        verbose=True
    )

    # Executar tarefas
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

# Salvar saída final
final_output = {'artigos': all_articles}
file_name = 'output.yaml'

with open(file_name, 'w') as file:
    yaml.dump(final_output, file, default_flow_style=False, allow_unicode=True)
print(f'Dados salvos em {file_name}')
