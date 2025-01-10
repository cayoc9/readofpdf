from crewai import Agent

def create_agent_leitor(llm, tool):
    return Agent(
        role='PDF Reader',
        goal='Ler PDFs e extrair informações específicas conforme definido nas solicitações.',
        backstory='Você é um especialista em leitura de artigos científicos.',
        tools=[tool],
        verbose=True,
        memory=False,
        llm=llm
    )

def create_agent_revisor(llm):
    return Agent(
        role="Revisor de leitura",
        goal="Revisar dados extraídos para garantir conformidade com o modelo.",
        backstory='Você é um especialista em revisão de YAML.',
        verbose=True,
        memory=False,
        llm=llm
    )
