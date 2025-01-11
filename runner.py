import subprocess
import time

# Caminho para o arquivo Python que será executado
script_path = "src/main.py"

# Número de vezes que o script será executado
n = 5  

for i in range(n):
    print(f"Executando pela {i + 1}ª vez...")
    subprocess.run(["python3", script_path])  # Executa o script
    time.sleep(2)  # Pausa de 2 segundos (opcional)

print("Execuções concluídas.")
