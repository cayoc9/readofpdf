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
