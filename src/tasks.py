from crewai import Task

def leitor_task(agent_leitor):
    return Task(
        description="Leia o PDF e responda em YAML conforme solicitado.",
        expected_output="YAML com respostas extraídas.",
        agent=agent_leitor
    )

def revisor_task(agent_revisor):
    return Task(
        description="Revise o YAML gerado para garantir precisão e formato correto.",
        expected_output="YAML revisado conforme o modelo.",
        agent=agent_revisor
    )
