"""Dashboard 2: KPIs de vendas e de problemas nos pedidos.

As métricas e o motivo de cada uma estão em entregas/justificativa-metricas.md.
"""

import altair as alt
import pandas as pd
import streamlit as st

from src.formatacao import em_portugues, numero

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
SEGMENTOS = ["New", "Regular", "VIP"]

# Discretização de Sales (valor do pedido) em faixas fáceis de ler
FAIXAS_VALOR = [0, 20, 50, 100, 300, float("inf")]
ROTULOS_FAIXAS = ["até 20", "21–50", "51–100", "101–300", "acima de 300"]

# Cores fixas que funcionam nos temas claro e escuro (as barras comuns usam a cor do tema)
COR_ALERTA = "#d1495b"
COR_REFERENCIA = "#9a8c98"


def nome_mes(periodo):
    return f"{MESES[periodo.month - 1]}/{str(periodo.year)[2:]}"


def variacao(atual, anterior):
    if anterior is None or pd.isna(anterior) or anterior == 0:
        return None
    return f"{(atual - anterior) / anterior:+.1%}".replace(".", ",")


def calcula_kpis(dados):
    if dados.empty:
        return None
    return {
        "pedidos": len(dados),
        "faturamento": dados["Sales"].sum(),
        "ticket": dados["Sales"].mean(),
        "taxa_problema": dados["desfecho"].eq("Problema").mean(),
    }


def mostra_kpis(dados, dados_anterior, descricao_anterior):
    atual = calcula_kpis(dados)
    anterior = calcula_kpis(dados_anterior)

    # Minigráficos: a mesma métrica mês a mês dentro do período escolhido
    mensal = dados.groupby("mes").agg(
        pedidos=("OrderID", "size"),
        faturamento=("Sales", "sum"),
        ticket=("Sales", "mean"),
        taxa_problema=("desfecho", lambda s: s.eq("Problema").mean()),
    )

    def delta(chave):
        return variacao(atual[chave], anterior[chave]) if anterior else None

    # Taxa de problema: a diferença em pontos percentuais (p.p.) é mais clara que "% de %"
    delta_taxa = None
    if anterior:
        delta_taxa = f"{(atual['taxa_problema'] - anterior['taxa_problema']) * 100:+.1f} p.p.".replace(".", ",", 1)

    descricao = descricao_anterior if anterior else None
    with st.container(horizontal=True):
        st.metric(
            "Pedidos",
            numero(atual["pedidos"]),
            delta("pedidos"),
            delta_description=descricao,
            chart_data=mensal["pedidos"].tolist(),
            chart_type="bar",
            border=True,
            help="Quantidade de pedidos no período e nos filtros escolhidos.",
        )
        st.metric(
            "Faturamento",
            numero(atual["faturamento"]),
            delta("faturamento"),
            delta_description=descricao,
            chart_data=mensal["faturamento"].tolist(),
            chart_type="bar",
            border=True,
            help="Soma de Sales (valor dos pedidos), incluindo cancelados e devolvidos.",
        )
        st.metric(
            "Ticket médio",
            numero(atual["ticket"], 1),
            delta("ticket"),
            delta_description=descricao,
            chart_data=mensal["ticket"].tolist(),
            chart_type="line",
            border=True,
            help="Valor médio por pedido (média de Sales).",
        )
        st.metric(
            "Taxa de problema",
            f"{atual['taxa_problema']:.1%}".replace(".", ","),
            delta_taxa,
            delta_color="inverse",
            delta_description=descricao,
            chart_data=mensal["taxa_problema"].tolist(),
            chart_type="line",
            border=True,
            help="% de pedidos cancelados ou devolvidos (desfecho = Problema). Subir é ruim.",
        )


def grafico_categorias(dados):
    por_categoria = (
        dados.groupby("Category")
        .agg(faturamento=("Sales", "sum"), pedidos=("OrderID", "size"))
        .reset_index()
    )
    clique = alt.selection_point(name="categoria", fields=["Category"])
    return em_portugues(
        alt.Chart(por_categoria)
        .mark_bar()
        .encode(
            x=alt.X("faturamento:Q", title="Faturamento"),
            y=alt.Y("Category:N", sort="-x", title=None),
            opacity=alt.condition(clique, alt.value(1), alt.value(0.3)),
            tooltip=[
                alt.Tooltip("Category:N", title="Categoria"),
                alt.Tooltip("faturamento:Q", title="Faturamento", format=",.0f"),
                alt.Tooltip("pedidos:Q", title="Pedidos", format=","),
            ],
        )
        .add_params(clique)
        .properties(height=280)
    )


def grafico_faixas(dados):
    faixas = pd.cut(dados["Sales"], FAIXAS_VALOR, labels=ROTULOS_FAIXAS)
    contagem = faixas.value_counts().reindex(ROTULOS_FAIXAS, fill_value=0)
    por_faixa = pd.DataFrame({"faixa": ROTULOS_FAIXAS, "pedidos": contagem.values})
    por_faixa["percentual"] = por_faixa["pedidos"] / por_faixa["pedidos"].sum()
    return em_portugues(
        alt.Chart(por_faixa)
        .mark_bar()
        .encode(
            x=alt.X("faixa:N", sort=ROTULOS_FAIXAS, title="Valor do pedido (Sales)", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("pedidos:Q", title="Pedidos"),
            tooltip=[
                alt.Tooltip("faixa:N", title="Faixa"),
                alt.Tooltip("pedidos:Q", title="Pedidos", format=","),
                alt.Tooltip("percentual:Q", title="% dos pedidos", format=".1%"),
            ],
        )
        .properties(height=280)
    )


def grafico_pagamento(dados):
    por_pagamento = (
        dados.groupby("PaymentMethod")
        .agg(taxa=("desfecho", lambda s: s.eq("Problema").mean()), pedidos=("OrderID", "size"))
        .reset_index()
        .sort_values("taxa", ascending=False)
    )
    base = alt.Chart(por_pagamento).encode(
        # tickMinStep evita rótulos repetidos no eixo (0%, 1%, 1%, 2%...)
        x=alt.X("taxa:Q", title="Taxa de problema", axis=alt.Axis(format=".0%", tickMinStep=0.01)),
        # Ordem fixa (maior taxa no topo): com sort="-x" as camadas barra + texto geram aviso de ordem conflitante
        y=alt.Y("PaymentMethod:N", sort=por_pagamento["PaymentMethod"].tolist(), title=None),
        tooltip=[
            alt.Tooltip("PaymentMethod:N", title="Pagamento"),
            alt.Tooltip("taxa:Q", title="Taxa de problema", format=".1%"),
            alt.Tooltip("pedidos:Q", title="Pedidos", format=","),
        ],
    )
    # Rótulo dentro da barra, no início, para a linha da taxa geral (perto do fim das barras) não passar por cima
    rotulos = base.mark_text(align="left", dx=8, color="white", fontWeight=600).encode(
        x=alt.datum(0), text=alt.Text("taxa:Q", format=".1%")
    )
    barras = base.mark_bar(color=COR_ALERTA) + rotulos
    taxa_geral = dados["desfecho"].eq("Problema").mean()
    referencia = (
        alt.Chart(pd.DataFrame({"taxa": [taxa_geral]}))
        .mark_rule(color=COR_REFERENCIA, strokeDash=[5, 3], strokeWidth=2)
        .encode(x="taxa:Q", tooltip=[alt.Tooltip("taxa:Q", title="Taxa geral", format=".1%")])
    )
    return em_portugues((barras + referencia).properties(height=200))


def render(df):
    st.title("KPIs de vendas e de problemas nos pedidos")

    df = df.assign(mes=df["OrderDate"].dt.to_period("M"))
    meses = sorted(df["mes"].unique())

    # persist_state="page": os filtros continuam como estavam ao voltar da aba do Dashboard 1
    with st.sidebar:
        st.header("Filtros")
        inicio, fim = st.select_slider(
            "Período",
            options=meses,
            value=(meses[-12], meses[-1]),  # padrão: últimos 12 meses
            format_func=nome_mes,
            help="Os deltas dos KPIs comparam com o período anterior de mesmo tamanho.",
            key="d2_periodo",
            persist_state="page",
        )
        segmentos = st.pills(
            "Segmento de cliente",
            SEGMENTOS,
            selection_mode="multi",
            default=SEGMENTOS,
            key="d2_segmentos",
            persist_state="page",
        )

    if not segmentos:
        st.warning("Selecione pelo menos 1 segmento de cliente.")
        return

    # Período anterior com o mesmo número de meses, logo antes do início escolhido
    n_meses = (fim - inicio).n + 1
    inicio_anterior, fim_anterior = inicio - n_meses, inicio - 1

    do_segmento = df[df["CustomerSegment"].isin(segmentos)]
    df_periodo = do_segmento[do_segmento["mes"].between(inicio, fim)]
    df_anterior = do_segmento[do_segmento["mes"].between(inicio_anterior, fim_anterior)]

    st.caption(
        f"{nome_mes(inicio)} a {nome_mes(fim)} ({n_meses} {'mês' if n_meses == 1 else 'meses'}) · "
        f"segmentos: {', '.join(segmentos)}"
    )

    if df_periodo.empty:
        st.warning("Nenhum pedido no período e segmentos escolhidos.")
        return

    # Os KPIs ficam no topo, mas dependem do clique no gráfico de categorias (desenhado depois)
    area_kpis = st.container()

    col_categoria, col_faixa = st.columns(2)
    with col_categoria:
        with st.container(border=True):
            st.subheader("Faturamento por categoria")
            evento = st.altair_chart(
                grafico_categorias(df_periodo),
                key="clique_categoria",
                on_select="rerun",
                width="stretch",
                alt="Faturamento por categoria de produto",
            )
            st.caption("Clique numa barra para filtrar o painel (shift + clique seleciona várias).")

    # Seleção cruzada: o clique numa categoria filtra os KPIs e os outros gráficos
    categorias = [item["Category"] for item in evento.selection.get("categoria", [])]
    if categorias:
        df_periodo = df_periodo[df_periodo["Category"].isin(categorias)]
        df_anterior = df_anterior[df_anterior["Category"].isin(categorias)]

    # Ex.: categoria clicada e depois o período mudou para meses sem pedidos dela
    if df_periodo.empty:
        area_kpis.warning("Nenhum pedido da categoria selecionada neste período. Clique numa área vazia do gráfico para limpar.")
        return

    with area_kpis:
        if categorias:
            st.caption(f"Filtrando pela categoria: {', '.join(categorias)}. Clique numa área vazia do gráfico para limpar.")
        descricao_anterior = f"vs. {nome_mes(inicio_anterior)}–{nome_mes(fim_anterior)}"
        if df_anterior.empty:
            st.caption("Sem pedidos no período anterior equivalente, então os KPIs aparecem sem comparação.")
        mostra_kpis(df_periodo, df_anterior, descricao_anterior)

    with col_faixa:
        with st.container(border=True):
            st.subheader("Pedidos por faixa de valor")
            st.altair_chart(grafico_faixas(df_periodo), width="stretch", alt="Pedidos por faixa de valor do pedido")
            ate_50 = df_periodo["Sales"].le(50).mean()
            st.caption(f"Sales em faixas: {ate_50:.0%} dos pedidos do filtro atual são de até 50.")

    with st.container(border=True):
        st.subheader("Taxa de problema por forma de pagamento")
        st.altair_chart(grafico_pagamento(df_periodo), width="stretch", alt="Taxa de problema por forma de pagamento")
        st.caption("Linha tracejada = taxa de problema geral do filtro atual.")
