import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")

st.title("📊 Análise Salarial de Profissionais de IA (2025-2026)")
st.write("Explore salários por cargo, país e nível de experiência")


# CARREGAR DADOS (CACHE)

@st.cache_data
def carregar_dados():
    df = pd.read_csv("ai_jobs_market_2025_2026.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = carregar_dados()
df = df.dropna()


# SIDEBAR (FILTROS)

st.sidebar.header("🔎 Filtros")

cargo = st.sidebar.multiselect(
    "Cargo",
    options=df["job_title"].unique(),
    default=df["job_title"].unique()
)

pais = st.sidebar.multiselect(
    "País",
    options=df["country"].unique(),
    default=df["country"].unique()
)

exp = st.sidebar.multiselect(
    "Experiência",
    options=df["experience_level"].unique(),
    default=df["experience_level"].unique()
)

# Filtro base
df_filtrado = df[
    (df["job_title"].isin(cargo)) &
    (df["country"].isin(pais)) &
    (df["experience_level"].isin(exp))
]
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com esses filtros")
    st.stop()

# Slider salário
sal_min, sal_max = st.sidebar.slider(
    "Faixa Salarial (USD)",
    int(df_filtrado["annual_salary_usd"].min()),
    int(df_filtrado["annual_salary_usd"].max()),
    (
        int(df_filtrado["annual_salary_usd"].min()),
        int(df_filtrado["annual_salary_usd"].max())
    )
)

df_filtrado = df_filtrado[
    (df_filtrado["annual_salary_usd"] >= sal_min) &
    (df_filtrado["annual_salary_usd"] <= sal_max)
]

# =========================
# VALIDAÇÃO
# =========================
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com esses filtros")
else:

    # =========================
    # MÉTRICAS
    # =========================
    st.subheader("📊 Resumo Geral")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Salário Médio", f"${int(df_filtrado['annual_salary_usd'].mean())}")
    col2.metric("📈 Salário Máximo", f"${int(df_filtrado['annual_salary_usd'].max())}")
    col3.metric("📊 Total de Vagas", len(df_filtrado))

    # =========================
    # GRÁFICO 1 - POR CARGO
    # =========================
    st.subheader("📌 Salário Médio por Cargo")

    media_cargo = df_filtrado.groupby("job_title")["annual_salary_usd"].mean().reset_index()
    media_cargo = media_cargo.sort_values("annual_salary_usd", ascending=False)

    fig1 = px.bar(
        media_cargo,
        x="job_title",
        y="annual_salary_usd",
        color="annual_salary_usd",
        title="Salário Médio por Cargo"
    )

    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

    # =========================
    # GRÁFICO 2 - POR PAÍS
    # =========================
    st.subheader("🌍 Salário Médio por País")

    media_pais = df_filtrado.groupby("country")["annual_salary_usd"].mean().reset_index()

    fig2 = px.bar(
        media_pais,
        x="country",
        y="annual_salary_usd",
        color="annual_salary_usd",
        title="Salário Médio por País"
    )

    st.plotly_chart(fig2, use_container_width=True)

    
    # TABELA
    
    st.subheader("📄 Dados Filtrados")
    st.dataframe(df_filtrado)

    
    # DOWNLOAD
    
    csv = df_filtrado.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Baixar dados filtrados",
        data=csv,
        file_name="dados_filtrados.csv",
        mime="text/csv"
    )
