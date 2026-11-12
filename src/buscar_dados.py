# Importa as bibliotecas para ler API(requests) e interpretar dados(pandas)
import requests
import pandas as pd

# Aqui se conectar a url a url onde esta a API da Câmara
url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"

# Cada tupla eh (data inicio, data fim) de um espaco de ate 3 meses
periodos = [
    ("2026-01-01", "2026-03-31"),
    ("2026-04-01", "2026-06-30"),
    ("2026-07-01", "2026-09-30"),
    ("2026-10-01", "2026-11-11"),
]

todas_proposicoes = []

# Dicionario e seus pares chaves-valor
for inicio, fim in periodos:
    print(f"---- PERIODO {inicio} a {fim} ----")

    # Para o primeiro pedido de cada periodo, usamos os parametros normais
    parametros = {
        "siglaTipo": "PL",
        "dataApresentacaoInicio": inicio,
        "dataApresentacaoFim": fim,
        "itens": 100,
        "ordem": "DESC",    
        "ordenarPor": "id"
    }


    proxima_url = url
    proximos_parametros = parametros

    # Repete enquanto houver uma proxima pagina
    while proxima_url is not None:
        resposta = requests.get(proxima_url, params=proximos_parametros)
        dados = resposta.json()
        proposicoes_pagina = dados["dados"]

        print(f"  Pagina recebida: {len(proposicoes_pagina)} itens")
        todas_proposicoes.extend(proposicoes_pagina)

        # Procura o link "next" dentro da lista de links
        proxima_url = None
        for link in dados["links"]:
            if link["rel"] == "next":
                proxima_url = link["href"]

        # A partir da segunda pagina, a URL "next" ja vem com tudo embutido,
        # entao nao precisamos mais mandar parametros separados
        proximos_parametros = None


print("Total acumulado:", len(todas_proposicoes))

# Para toda proposicao apresenta o nome, numero e 80 carcteres do texo base
df = pd.DataFrame(todas_proposicoes)
print(df.shape)
print(df.columns)

df.to_csv("data/proposicoes.csv", index=False, encoding="utf-8-sig")
print("Arquivo salvo em data/proposicoes.csv")