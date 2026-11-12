# Importa as bibliotecas para ler API(requests) e interpretar dados(pandas)
import requests
import pandas as pd

# Aqui se conectar a url a url onde esta a API da Câmara
url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
# Dicionario e seus pares chaves-valor
parametros = {
    "siglaTipo": "PL",
    "itens": 20,
    "ordem": "DESC",
    "ordenarPor": "id"
}

# Request que busca os parametros definidos no dicionario
resposta = requests.get(url, params=parametros)

# 200, 404, 500, 429
print("Status da resposta:", resposta.status_code)

# Converte o JSON em "arquivo inteligivel" pelo python
dados = resposta.json()
proposicoes = dados["dados"]

# Para toda proposicao apresenta o nome, numero e 80 carcteres do texo base
for p in proposicoes:
    print(p["siglaTipo"], p["numero"], "-", p["ementa"][:80])

# Uso da pandas para processamento de dados
df = pd.DataFrame(proposicoes)
print(df.shape)       # mostra (linhas, colunas)
print(df.columns)     # mostra os nomes das colunas

df.to_csv("data/proposicoes.csv", index=False, encoding="utf-8-sig")
print("Arquivo salvo em data/proposicoes.csv")