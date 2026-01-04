import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import plotly.express as px

## Configuração de logs
LOG_DIR = Path("app/logs")

## Carregar logs em um DataFrame
def load_logs():
    records = []
    # Se o diretório não existir, retorna DataFrame vazio
    if not LOG_DIR.exists():
        return pd.DataFrame()
    # Percorre todos os arquivos .log no diretório de logs
    for log_path in LOG_DIR.glob("*.log"):
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    records.append(record)
                except json.JSONDecodeError:
                    continue

    df = pd.DataFrame(records)
    # Converte timestamp para datetime
    if not df.empty and "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df

## Cache dos dados para melhorar performance
@st.cache_data(ttl=5)
def get_data():
    return load_logs()

## Configuração da página do Streamlit
st.set_page_config(layout="wide")
# Título e descrição do dashboard
st.markdown("""
<h1 style="
    text-align: center;
    font-weight: 600;
    letter-spacing: -0.5px;
    margin-bottom: 10px;
">
    📊 Dashboard - Monitoramento de Classificação de Mensagens
</h1>
<p style="
    text-align: center;
    color: #6b7280;
    font-size: 16px;
    margin-top: 0;
">
    Visão geral dos logs, volumes e distribuição temporal das mensagens por classificação
</p>
<hr style="margin-top: 25px; margin-bottom: 25px;">
""", unsafe_allow_html=True)
# Carrega os dados
df = get_data()
# Se não houver dados, exibe mensagem
if df.empty:
    st.warning("Nenhum dado disponível ainda.")
    st.stop()

## Filtros por tipo de classificação
selected_types = st.multiselect(
    "Filtrar por tipo de classificação:",
    options=sorted(df["classification"].unique()),
    default=sorted(df["classification"].unique())
)
# Aplica filtro
filtered_df = df[df["classification"].isin(selected_types)]
# Se o filtro não retornar dados, exibe mensagem
if filtered_df.empty:
    st.info("Nenhum dado para exibir.")
    st.stop()

## Tabela principal de logs
st.subheader("Mensagens Classificadas")
st.dataframe(
    filtered_df[["input_message", "classification", "department", "event", "timestamp"]],
    use_container_width=True
)

## Preparação de cores para gráficos
classifications = sorted(filtered_df["classification"].unique())
# Paleta suave de cores
SOFT_COLORS = [
    "#E57373",
    "#64B5F6",
    "#FFB74D",
    "#81C784",
]
# Mapeia cada classificação para uma cor
color_map = {
    cls: SOFT_COLORS[i % len(SOFT_COLORS)]
    for i, cls in enumerate(classifications)
}

## Gráficos de volume e distribuição percentual
col1, col2 = st.columns(2)
# Volume por classe (gráfico de barras)
with col1:
    st.markdown(
    "<h3 style='text-align: center;'>Volume de Mensagens por Classificação</h3>",
    unsafe_allow_html=True
    )
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    volume_df = filtered_df["classification"].value_counts()
    ax1.bar(
        volume_df.index,
        volume_df.values,
        color=[color_map[c] for c in volume_df.index]
    )
    # Ajustes visuais
    ax1.tick_params(axis="x", labelsize=8)
    ax1.tick_params(axis="y", labelsize=8)
    ax1.tick_params(axis="x", rotation=45)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_linewidth(0.5)
    ax1.spines["bottom"].set_linewidth(0.5)
    st.pyplot(fig1)

# Distribuição percentual (gráfico de pizza)
with col2:
    st.markdown(
    "<h3 style='text-align: center;'>Distribuição Percentual</h3>",
    unsafe_allow_html=True
    )

    fig2, ax2 = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax2.pie(
        volume_df.values,
        autopct="%1.1f%%",
        startangle=90,
        colors=[color_map[c] for c in volume_df.index]
    )
    ax2.axis("equal")

    # Legenda no canto superior esquerdo
    ax2.legend(
        wedges,
        volume_df.index,
        loc="upper left",
        bbox_to_anchor=(0.0, 1.0),
        frameon=False,
        fontsize=5.5
    )
    # Ajuste do tamanho da fonte dos percentuais
    for autotext in autotexts:
        autotext.set_fontsize(7)

    st.pyplot(fig2)

## Tabela dos setores (Resumo Operacional)
today = pd.Timestamp.now(tz=filtered_df["timestamp"].dt.tz).date()
# Filtra apenas mensagens do dia atual
df_today = filtered_df[
    filtered_df["timestamp"].dt.date == today
]
# Total de mensagens por setor
total_por_setor = (
    df_today
    .groupby("department")
    .size()
    .reset_index(name="Total de mensagens no dia")
)
# Última mensagem por setor
now = pd.Timestamp.now(tz=filtered_df["timestamp"].dt.tz)
ultima_msg = (
    df_today
    .groupby("department")["timestamp"]
    .max()
    .reset_index(name="ultima_mensagem")
)
# Calcula minutos desde a última mensagem
ultima_msg["Minutos desde última mensagem"] = (
    (now - ultima_msg["ultima_mensagem"])
    .dt.total_seconds() / 60
).round(1)

ultima_msg = ultima_msg.drop(columns=["ultima_mensagem"])

## Status baseado nos últimos 10 minutos
now = pd.Timestamp.now(tz=filtered_df["timestamp"].dt.tz)
window_start = now - pd.Timedelta(minutes=10)
df_last_10 = filtered_df[
    filtered_df["timestamp"] >= window_start
]

volume_10min = (
    df_last_10
    .groupby("department")
    .size()
    .reset_index(name="mensagens_ultimos_10min")
)

# Define status operacional
def status_setor(qtd):
    if qtd > 15:
        return "🔴 Alerta: alto volume"
    else:
        return "🟢 Normal"
    
volume_10min["Status (últimos 10 min)"] = volume_10min["mensagens_ultimos_10min"].apply(status_setor)
# Garante setores sem mensagens recentes
volume_10min = (
    total_por_setor[["department"]]
    .merge(volume_10min, on="department", how="left")
    .fillna({"mensagens_ultimos_10min": 0})
)
volume_10min["mensagens_ultimos_10min"] = volume_10min["mensagens_ultimos_10min"].astype(int)
volume_10min["Status (últimos 10 min)"] = volume_10min["mensagens_ultimos_10min"].apply(status_setor)

## Combina todas as métricas em uma tabela final
tabela_setores = (
    total_por_setor
    .merge(
        ultima_msg[["department", "Minutos desde última mensagem"]],
        on="department"
    )
    .merge(
        volume_10min[["department", "Status (últimos 10 min)"]],
        on="department"
    )
    .rename(columns={
        "department": "Setor encaminhado"
    })
    .sort_values("Total de mensagens no dia", ascending=False)
)

st.subheader("Encaminhamento por Setor (Resumo Operacional do Dia)")
st.dataframe(
    tabela_setores,
    use_container_width=True,
    hide_index=True
)

## Gráfico linha temporal (plotly)
st.markdown(
    "<h3 style='text-align: center;'>Distribuição Temporal das Mensagens por Classificação</h3>",
    unsafe_allow_html=True
)

# Agrupa mensagens por minuto
filtered_df["minute"] = filtered_df["timestamp"].dt.floor("min")

time_df = (
    filtered_df
    .groupby(["minute", "classification"])
    .size()
    .reset_index(name="count")
)

# Pivot para formato wide
pivot_df = time_df.pivot(
    index="minute",
    columns="classification",
    values="count"
)

# Cria eixo temporal completo (minuto a minuto)
full_range = pd.date_range(
    start=pivot_df.index.min(),
    end=pivot_df.index.max(),
    freq="1min"
)

# Reindexa para incluir minutos sem mensagens
pivot_df = (
    pivot_df
    .reindex(full_range)
    .fillna(0)
)

plot_df = pivot_df.reset_index().rename(columns={"index": "minute"})

# Gráfico de linhas com plotly
fig = px.line(
    plot_df,
    x="minute",
    y=plot_df.columns[1:], 
    markers=True
)

fig.update_layout(
    xaxis_title=None,
    yaxis_title=None,
    legend_title_text=None
)

st.plotly_chart(fig, use_container_width=True)

