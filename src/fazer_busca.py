import chromadb
from sentence_transformers import SentenceTransformer

# 1. Carrega o mesmo modelo e conecta ao banco já criado
print("Carregando modelo e conectando ao banco de dados...")
modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
cliente_chroma = chromadb.PersistentClient(path="data/chroma_db")
colecao = cliente_chroma.get_collection(name="proposicoes")

# 2. Define a pergunta do usuário (pode testar outros temas)
pergunta = "projetos de lei sobre educação, escolas e universidades"
print(f"\nBuscando por: '{pergunta}'\n")
embedding_pergunta = modelo.encode([pergunta])

# 3. Realiza a busca semântica retornando os 3 resultados mais próximos
resultados = colecao.query(
    query_embeddings=embedding_pergunta.tolist(),
    n_results=3
)

# 4. Exibe os resultados
for i in range(len(resultados['ids'][0])):
    id_doc = resultados['ids'][0][i]
    documento = resultados['documents'][0][i]
    distancia = resultados['distances'][0][i]
    
    print(f"--- Resultado {i+1} (ID: {id_doc}) ---")
    print(f"Distância (menor = mais próximo): {distancia:.4f}")
    print(f"Ementa: {documento}\n")