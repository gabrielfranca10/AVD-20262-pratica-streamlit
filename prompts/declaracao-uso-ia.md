# Declaração de Uso de IA

**Nome:** Gabriel França
**Data:** 27/10/2026 (Aula 21) e 28/10/2026 (Aula 22)

## Ferramenta

Claude Code (Anthropic), modelo Claude Opus 5.5, rodando no VS Code.

## Prompt usado

**Aula 21:** enviei os slides da aula e o link do repositório-modelo, e pedi para montar a entrega do dia. O prompt estruturado usado para gerar o esqueleto do `app.py` está em [layout-skeleton-prompt.md](layout-skeleton-prompt.md).

**Aula 22:** enviei os slides da Aula 22 e pedi para fazer a parte 2 (Dashboard 1 completo, identidade visual, métricas e Dashboard 2), seguindo o `ROTEIRO.md`, o `ALTAIR-CROSSFILTER.md` e as skills do Streamlit (`developing-with-streamlit`).

## O que foi aceito, modificado ou rejeitado e por quê

**Aula 21**

- **Aceito:**
  - Esqueleto do `app.py`: sidebar com `st.multiselect` (variáveis) + `st.selectbox` e `st.slider` de faixa (filtro de intervalo), colunas Correlação/Distribuição com placeholders, avisos para os casos de borda.
  - `notebooks/eda-com-downloads.ipynb`: minha EDA da Aula 11 com a carga trocada de upload do Colab para leitura de `data/raw/`, mais a seção final que salva o dataset original (`data/raw/dataset.csv`) e o tratado (`data/clean/dataset.csv`).
  - Rascunho digital do layout em `entregas/rascunho-dashboard1.png`.
- **Modificado:**
  - O filtro de intervalo virou um slider só, sobre a variável escolhida num selectbox (padrão `Sales`), em vez de um slider por variável, para manter a sidebar curta.
- **Rejeitado:**
  - Nada nesta aula.

**Aula 22**

- **Aceito:**
  - `@st.cache_data` no `src/data_loader.py`, para o CSV ser lido uma vez só.
  - Identidade visual em `.streamlit/config.toml` (temas claro e escuro, fonte Inter, paleta dos gráficos), com as cores derivadas da paleta que eu já usava na EDA (roxo escuro, rosado e vermelho de alerta).
  - Dashboard 1 completo em `src/dashboard1.py`, com Altair: heatmap de Spearman (triângulo inferior, como no notebook) e um histograma por variável selecionada, com a linha da mediana. Também trata os casos de borda: 0, 1 e 2+ variáveis, intervalo sem pedidos e variável constante no intervalo (correlação indefinida, mostrada como "—").
  - Abas (`st.tabs`) separando os dois dashboards no `app.py`. Só a aba aberta é executada, então a sidebar mostra apenas os filtros do dashboard que está na tela.
  - Métricas do Dashboard 2 (pedidos, faturamento, ticket médio e taxa de problema), validadas antes em pandas e justificadas em `entregas/justificativa-metricas.md`.
  - Rascunho digital do layout em `entregas/rascunho-dashboard2.png`, feito antes do código do Dashboard 2.
  - Dashboard 2 em `src/dashboard2.py`: KPIs com `st.metric` (delta vs. período anterior e minigráfico mensal), gráfico de barras agrupando `Category` com seleção cruzada (`on_select`) filtrando os KPIs e os outros gráficos, `Sales` discretizado em faixas e taxa de problema por forma de pagamento.
- **Modificado:**
  - Nada nesta aula.
- **Rejeitado:**
  - Nada nesta aula.
