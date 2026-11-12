import pandas as pd
import streamlit as st
import plotly.express as px

# Configuracao da pagina (titulo na aba do navegador)
st.set_page_config(page_title="Proposicoes Legislativas 2026", layout="wide")

# Carrega e prepara os dados (mesma logica do indicadores.py)
# df = Dataframe do pandas com todas as proposicoes coletadas via API da Camara
df = pd.read_csv("data/proposicoes.csv")
df["dataApresentacao"] = pd.to_datetime(df["dataApresentacao"])
df["mes"] = df["dataApresentacao"].dt.month
df["dia"] = df["dataApresentacao"].dt.date

# Titulo e texto introdutorio na pagina
st.title("Dashboard de Projetos de Lei - Camara dos Deputados (2026)")
st.markdown("Analise dos projetos de lei (PL) apresentados em 2026, via API de Dados Abertos da Camara.")

# Metrica simples no topo (numero grande e chamativo)
st.metric("Total de PLs apresentados em 2026", len(df))

# Define uma lista para os nomes dos meses, para usar nos graficos
nomes_meses = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
}
# Define uma lista para os nomes dos meses por extenso, para usar na formatacao de datas
nomes_meses_completo = {
    1: "Janeiro", 2: "Fevereiro", 3: "Marco", 4: "Abril", 5: "Maio", 6: "Junho",
    7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

# Adiciona uma coluna com o nome do mes, para usar nos graficos
df["mes_nome"] = df["mes"].map(nomes_meses)

# Grafico 1: PLs por mes (agora com nomes em vez de numeros)
por_mes = df.groupby(["mes", "mes_nome"]).size().reset_index(name="quantidade")
por_mes = por_mes.sort_values("mes")  # garante a ordem Jan, Fev, Mar...
fig_mes = px.bar(por_mes, x="mes_nome", y="quantidade", title="PLs apresentados por mes")
fig_mes.update_xaxes(title="Mes")
st.plotly_chart(fig_mes, use_container_width=True)

# Grafico 2: Top 10 dias com mais PLs (horizontal, com data por extenso)
por_dia = df.groupby("dia").size().reset_index(name="quantidade")
por_dia = por_dia.sort_values("quantidade", ascending=False).head(10)

def formatar_data_extenso(data):
    mes_nome = nomes_meses_completo[data.month]
    return f"{data.day} de {mes_nome}"

por_dia["dia_formatado"] = por_dia["dia"].apply(formatar_data_extenso)
por_dia = por_dia.sort_values("quantidade", ascending=True)  # ascending p/ barra horizontal ficar com maior no topo

fig_dia = px.bar(por_dia, x="quantidade", y="dia_formatado", orientation="h",
                  title="Top 10 dias com mais PLs apresentados")
fig_dia.update_yaxes(title="Dia")
fig_dia.update_xaxes(title="Quantidade")
st.plotly_chart(fig_dia, use_container_width=True)