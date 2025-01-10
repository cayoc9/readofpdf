from OllamaMistralEmbedder import OllamaMistralEmbedder
from crewai_tools import PDFSearchTool

ollama = OllamaMistralEmbedder() 

pdf = PDFSearchTool(pdf="/home/wallace/Projects/'leitor de PDF - GPT - Old'/PDFs/Framework-for-Improving-Critical-Infrastructure-Cybersecurity.pdf", embedding_model=ollama)
