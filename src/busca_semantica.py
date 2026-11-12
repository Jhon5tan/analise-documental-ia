import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

# Carrega os dados do CSV com as proposicoes (ementas) do dataset
df = pd.read_csv("data/proposicoes.csv")

# Carrega o modelo de embeddings.
# Este modelo especifico entende varios idiomas, incluindo portugues.
print("Carregando modelo de embeddings (Isso pode demorar um pouco na primeira vez)...")
modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Cria (ou abre, se ja existir) um banco de dados Chroma salvo em disco,
# na pasta "chroma_db" dentro do projeto
cliente_chroma = chromadb.PersistentClient(path="data/chroma_db")

# Cria (ou abre) uma "colecao" dentro do Chroma para armazenar os embeddings das ementas
colecao = cliente_chroma.get_or_create_collection(name="proposicoes")

print(f"Gerando embeddings para {len(df)} ementas...")

# Gera o embedding de cada ementa de uma vez
ementas = df["ementa"].astype(str).tolist()
embeddings = modelo.encode(ementas, show_progress_bar=True)

# Adiciona tudo no Chroma: cada item precisa de um id unico,
# o texto original, e o embedding correspondente
ids = df["id"].astype(str).tolist()

colecao.upsert(
    ids=ids,
    documents=ementas,
    embeddings=embeddings.tolist(),
)

print("Pronto! Embeddings gerados e salvos no Chroma.")
print("Total de itens na colecao:", colecao.count())