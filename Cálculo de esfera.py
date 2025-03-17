import math
import pandas as pd
import numpy as np
from google.colab import files

# Passo 1: Upload do arquivo CSV
print("Faça upload do arquivo 'arquivo_de_esfera.csv':")
uploaded = files.upload()

# Passo 2: Carregar os dados com o novo formato de cabeçalho
dados = pd.read_csv("arquivo_de_esfera")  # Lê o CSV <button class="citation-flag" data-index="5">

# Verifica se há valores ausentes ou não numéricos
print("\nPrimeiras linhas do arquivo:")
print(dados.head())

# Passo 3: Definir incerteza do paquímetro (ajuste conforme seu relatório)
DELTA_D_PAQUIMETRO = 0.01  # Incerteza do paquímetro (ex: 0.01 mm) [[rel_2_física_aplicada.pdf]]

# Passo 4: Funções de cálculo
def calcular_volume(r):
    """Calcula o volume da esfera: V = (4/3) * π * r³"""
    return (4 / 3) * math.pi * r**3

def calcular_erro_volume(d, delta_d):
    """Propaga a incerteza: ΔV = (πd²/2) * Δd"""
    return (math.pi * d**2 / 2) * delta_d

# Passo 5: Processar todas as esferas
resultados = []

for index, row in dados.iterrows():
    try:
        # Medições do paquímetro
        diametros_p = row[["paquímetro 1", "paquímetro 2", "paquímetro 3", "paquímetro 4", "paquímetro 5"]].values

        # Converter valores para float (caso estejam como string)
        diametros_p = [float(d.replace(',', '.')) if isinstance(d, str) else float(d) for d in diametros_p]

        # Cálculo do diâmetro médio e desvio padrão
        dp_medio = np.mean(diametros_p)  # Diâmetro médio
        dp_desvio_padrao = np.std(diametros_p)  # Desvio padrão

        # Cálculo do raio
        raio = dp_medio / 2

        # Cálculo do volume
        volume = calcular_volume(raio)

        # Cálculo da incerteza total (propagação de erro)
        erro_total = calcular_erro_volume(dp_medio, DELTA_D_PAQUIMETRO)

        resultados.append({
            "Esfera": row["Esferas"],  # Número da esfera
            "Diâmetro Médio (mm)": round(dp_medio, 4),
            "Desvio Padrão (mm)": round(dp_desvio_padrao, 4),
            "Incerteza Instrumento (mm)": DELTA_D_PAQUIMETRO,
            "Incerteza Total (mm³)": round(erro_total, 4),
            "Raio (mm)": round(raio, 4),
            "Volume (mm³)": round(volume, 4)
        })
    except Exception as e:
        print(f"Erro ao processar a esfera {row['Esferas']}: {e}")

# Passo 6: Exibir resultados
df_resultados = pd.DataFrame(resultados)
print("\nResultados Finais:")
print(df_resultados)