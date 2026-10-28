"""Dashboard 1: correlação (Spearman) e distribuição das variáveis quantitativas."""

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Variáveis quantitativas do estudo (mesma lista VARS_QUANT do notebook de EDA)
VARS_QUANT = ["Age", "Quantity", "Discount", "UnitPrice", "Sales"]

# Cores fixas que funcionam nos temas claro e escuro (as barras usam a cor do tema)
COR_MEDIANA = "#d1495b"
COR_TEXTO_ESCURO = "#2d223a"
# Escala divergente da correlação: vermelho (negativa) → claro (zero) → roxo (positiva)
ESCALA_CORRELACAO = alt.Scale(domain=[-1, 0, 1], range=["#b8323f", "#f4eef1", "#4b2e83"])


def heatmap_correlacao(df, variaveis):
    corr = df[variaveis].corr(method="spearman")

    # Só o triângulo inferior (com a diagonal), como no notebook: o superior repete os valores
    dados = pd.DataFrame(
        [
            {"linha": y, "coluna": x, "r": corr.loc[y, x]}
            for i, y in enumerate(variaveis)
            for x in variaveis[: i + 1]
        ]
    )
    # Variável constante no intervalo → correlação indefinida (NaN), mostrada como "—"
    dados["rotulo"] = dados["r"].map(lambda r: "—" if pd.isna(r) else f"{r:.2f}")

    base = alt.Chart(dados).encode(
        x=alt.X("coluna:N", sort=variaveis, title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("linha:N", sort=variaveis, title=None),
    )
    celulas = base.mark_rect(stroke="white", strokeWidth=1).encode(
        color=alt.Color("r:Q", scale=ESCALA_CORRELACAO, title="ρ"),
        tooltip=[
            alt.Tooltip("linha:N", title="Variável"),
            alt.Tooltip("coluna:N", title="com"),
            alt.Tooltip("rotulo:N", title="ρ de Spearman"),
        ],
    )
    rotulos = base.mark_text(fontSize=14, fontWeight=600).encode(
        text="rotulo:N",
        color=alt.condition("abs(datum.r) > 0.5", alt.value("white"), alt.value(COR_TEXTO_ESCURO)),
    )
    return (celulas + rotulos).properties(height=60 * len(variaveis) + 40), corr


def histograma(serie):
    nome = serie.name
    titulo = alt.Title(nome, subtitle=f"mediana {serie.median():g} · média {serie.mean():.1f}")

    # Mesma regra do notebook: até 12 valores distintos é tratada como discreta (uma barra por valor)
    if serie.nunique() <= 12:
        contagem = serie.value_counts().sort_index()
        dados = pd.DataFrame({"valor": contagem.index, "pedidos": contagem.values})
        return (
            alt.Chart(dados, title=titulo)
            .mark_bar()
            .encode(
                x=alt.X("valor:O", title=None, axis=alt.Axis(labelAngle=0)),
                y=alt.Y("pedidos:Q", title="Pedidos"),
                tooltip=[alt.Tooltip("valor:O", title=nome), alt.Tooltip("pedidos:Q", title="Pedidos", format=",")],
            )
            .properties(height=220)
        )

    # Contínua: agrega em 30 faixas no pandas e manda só as contagens para o gráfico (e não 49 mil linhas)
    contagens, bordas = np.histogram(serie, bins=30)
    dados = pd.DataFrame({"inicio": bordas[:-1], "fim": bordas[1:], "pedidos": contagens})
    barras = (
        alt.Chart(dados)
        .mark_bar()
        .encode(
            x=alt.X("inicio:Q", bin="binned", title=None),
            x2="fim:Q",
            y=alt.Y("pedidos:Q", title="Pedidos"),
            tooltip=[
                alt.Tooltip("inicio:Q", title="De", format=".1f"),
                alt.Tooltip("fim:Q", title="Até", format=".1f"),
                alt.Tooltip("pedidos:Q", title="Pedidos", format=","),
            ],
        )
    )
    mediana = (
        alt.Chart(pd.DataFrame({"mediana": [serie.median()]}))
        .mark_rule(color=COR_MEDIANA, strokeDash=[5, 3], strokeWidth=2)
        .encode(x="mediana:Q")
    )
    return (barras + mediana).properties(title=titulo, height=220)


def render(df):
    st.title("Correlação e distribuição das variáveis quantitativas")

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

    # Dashboard 1: correlação (heatmap) à esquerda, distribuição (histogramas) à direita
    col_correlacao, col_distribuicao = st.columns([1, 1.5], gap="large")

    with col_correlacao:
        st.subheader("Correlação (Spearman)")

        if len(variaveis) < 2:
            st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
        elif len(df_filtrado) < 3:
            st.warning("Poucos pedidos no intervalo escolhido para calcular a correlação.")
        else:
            grafico, corr = heatmap_correlacao(df_filtrado, variaveis)
            st.altair_chart(grafico, width="stretch", alt="Heatmap da correlação de Spearman")
            st.caption(
                "Spearman (por postos), como na EDA: as variáveis são assimétricas e com outliers. "
                "Perto de 1 ou −1 = relação forte; perto de 0 = relação fraca."
            )
            constantes = [v for v in variaveis if df_filtrado[v].nunique() <= 1]
            if constantes:
                st.info(
                    f"{', '.join(constantes)} tem um único valor no intervalo escolhido, "
                    "então a correlação dela fica indefinida (—)."
                )

    with col_distribuicao:
        st.subheader("Distribuição")

        if not variaveis:
            st.warning("Selecione pelo menos 1 variável para ver a distribuição.")
        elif df_filtrado.empty:
            st.warning("Nenhum pedido dentro do intervalo escolhido.")
        else:
            # Um histograma por variável selecionada, em grade de 2 colunas
            colunas = st.columns(2)
            for i, var in enumerate(variaveis):
                with colunas[i % 2]:
                    st.altair_chart(histograma(df_filtrado[var]), width="stretch", alt=f"Histograma de {var}")
            st.caption("Linha tracejada = mediana (só nas variáveis contínuas).")

    with st.expander("Ver dados filtrados"):
        st.dataframe(df_filtrado[variaveis], width="stretch")
