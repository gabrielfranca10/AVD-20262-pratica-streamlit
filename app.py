import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Dashboard 1 — Correlação e Distribuição | E-commerce",
    layout="wide",
)

st.title("Correlação e Distribuição das Variáveis Quantitativas — E-commerce de Eletrônicos")

df = load_data()

# Variáveis quantitativas do estudo (mesma lista VARS_QUANT do notebook de EDA)
VARS_QUANT = ["Age", "Quantity", "Discount", "UnitPrice", "Sales"]

# Sidebar: filtros (variáveis + intervalo)
with st.sidebar:
    st.header("Filtros")

    variaveis = st.multiselect(
        "Variáveis quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT,
        help="Variáveis que entram na correlação e na distribuição.",
    )

    var_intervalo = st.selectbox(
        "Filtrar intervalo de",
        options=VARS_QUANT,
        index=VARS_QUANT.index("Sales"),
        help="Ex.: cortar os pedidos de valor extremo e ver se a correlação muda.",
    )

    # Todas as quantitativas do dataset são inteiras (ex.: 4.0), então o slider usa passo 1
    minimo, maximo = int(df[var_intervalo].min()), int(df[var_intervalo].max())
    inicio, fim = st.slider(
        f"Intervalo de {var_intervalo}",
        min_value=minimo,
        max_value=maximo,
        value=(minimo, maximo),
        step=1,
        key=f"intervalo_{var_intervalo}",
    )

# Mantém só os pedidos dentro do intervalo escolhido
df_filtrado = df[df[var_intervalo].between(inicio, fim)]

st.caption(f"{len(df_filtrado):,} de {len(df):,} pedidos dentro do intervalo escolhido.".replace(",", "."))

# Dashboard 1: correlação (heatmap) à esquerda, distribuição (histograma) à direita
col_correlacao, col_distribuicao = st.columns([1, 1.5])

with col_correlacao:
    st.subheader("Correlação (Spearman)")

    if len(variaveis) < 2:
        st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
    else:
        # TODO (Aula 22): heatmap da correlação de Spearman de df_filtrado[variaveis]
        st.info(f"Placeholder do heatmap — variáveis: {', '.join(variaveis)}")

with col_distribuicao:
    st.subheader("Distribuição")

    if not variaveis:
        st.warning("Selecione pelo menos 1 variável para ver a distribuição.")
    elif df_filtrado.empty:
        st.warning("Nenhum pedido dentro do intervalo escolhido.")
    else:
        # TODO (Aula 22): um histograma por variável selecionada
        st.info(f"Placeholder dos histogramas — {len(variaveis)} variável(is) selecionada(s)")

with st.expander("Ver dados filtrados"):
    st.dataframe(df_filtrado[variaveis], width="stretch")

# TODO: Dashboard 2 — KPIs (Aula 22)
