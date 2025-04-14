import streamlit as st
import pandas as pd
import plotly.express as px

# Simulando dados fictícios
def gerar_dados():
    data = {
        'Aluno': [f'Aluno {i}' for i in range(1, 101)],
        'Nota Português': pd.np.random.randint(0, 11, 100),
        'Nota Matemática': pd.np.random.randint(0, 11, 100),
        'Nota Ciências': pd.np.random.randint(0, 11, 100),
        'Escola': pd.np.random.choice(['Escola A', 'Escola B', 'Escola C'], 100),
        'Tipo de Escola': pd.np.random.choice(['Urbana', 'Rural', 'Estadual'], 100)
    }
    df = pd.DataFrame(data)
    return df

# Inicializa dados
df = gerar_dados()

# Layout
st.set_page_config(page_title="Dashboard Educacional de Oriximiná", layout="wide")
st.title("📊 Dashboard Educacional de Oriximiná")

# Sidebar - Filtros
tipo_escola = st.sidebar.selectbox("Tipo de escola", ["Todas"] + sorted(df["Tipo de Escola"].unique().tolist()))
if tipo_escola != "Todas":
    df = df[df["Tipo de Escola"] == tipo_escola]

escola = st.sidebar.selectbox("Escola", ["Todas"] + sorted(df["Escola"].unique().tolist()))
if escola != "Todas":
    df = df[df["Escola"] == escola]

# Abas
aba1, aba2, aba3 = st.tabs(["📈 Visão Geral", "📚 Notas por Disciplina", "🏅 Alunos Destaque"])

with aba1:
    st.subheader("📌 Distribuição das Notas por Escola")
    media_por_escola = df.groupby("Escola")[["Nota Português", "Nota Matemática", "Nota Ciências"]].mean().reset_index()
    fig_bar = px.bar(media_por_escola, x="Escola", y=["Nota Português", "Nota Matemática", "Nota Ciências"], barmode="group")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("✅ Aprovação x Reprovação")
    df["Aprovado"] = df[["Nota Português", "Nota Matemática", "Nota Ciências"]].mean(axis=1) >= 6
    aprovados = df["Aprovado"].value_counts()
    fig_pie = px.pie(names=aprovados.index.map({True: "Aprovados", False: "Reprovados"}), values=aprovados.values)
    st.plotly_chart(fig_pie, use_container_width=True)

with aba2:
    st.subheader("📚 Médias por Disciplina")
    medias = df[["Nota Português", "Nota Matemática", "Nota Ciências"]].mean()
    st.write(medias)

    st.subheader("📊 Gráfico de Médias por Disciplina")
    fig = px.line(x=medias.index, y=medias.values, markers=True, labels={'x': 'Disciplina', 'y': 'Média'})
    st.plotly_chart(fig, use_container_width=True)

with aba3:
    st.subheader("🏅 Alunos Nota 10")
    nota10 = df[(df["Nota Português"] == 10) | (df["Nota Matemática"] == 10) | (df["Nota Ciências"] == 10)]
    st.dataframe(nota10[["Aluno", "Escola", "Tipo de Escola", "Nota Português", "Nota Matemática", "Nota Ciências"]])

    st.subheader("🏆 Ranking por Média Geral")
    df["Média Geral"] = df[["Nota Português", "Nota Matemática", "Nota Ciências"]].mean(axis=1)
    ranking = df.sort_values(by="Média Geral", ascending=False).head(10)
    st.dataframe(ranking[["Aluno", "Escola", "Média Geral"]])
