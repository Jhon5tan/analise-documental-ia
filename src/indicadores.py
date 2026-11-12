import pandas as pd

# Le o CSV coletado (a tabela de proposicoes no DataFrame do pandas)
df = pd.read_csv("data/proposicoes.csv")

print("Total de proposicoes:", len(df))
print()

# A coluna dataApresentacao vem como texto (string), tipo "2026-03-25T18:46"
# Converte para um tipo "data" de verdade, para o pandas entender meses/anos
df["dataApresentacao"] = pd.to_datetime(df["dataApresentacao"])

# Cria uma nova coluna so com o mes (numero de 1 a 12)
df["mes"] = df["dataApresentacao"].dt.month

# Indicador 1: agrupa a quantidade de PLs por mes
por_mes = df.groupby("mes").size()
print("PLs por mes:")
print(por_mes)
print()

# Indicador 2: os 10 dias com mais PLs apresentados (pode revelar padroes, tipo fim de ano legislativo)
df["dia"] = df["dataApresentacao"].dt.date
por_dia = df.groupby("dia").size().sort_values(ascending=False).head(10)
print("Top 10 dias com mais PLs:")
print(por_dia) 

# Investigando o pico de 17 de julho
pico = df[df["dia"] == pd.to_datetime("2026-07-17").date()]
print("Amostra de PLs do dia 17/07:")
print(pico[["numero", "ementa"]].head(10))

# TODO (Etapa 3): aqui entra a categorizacao das proposicoes por tema,
# feita com embeddings/PLN (sentence-transformers), unindo este CSV
# da Camara com a camada de IA do projeto.