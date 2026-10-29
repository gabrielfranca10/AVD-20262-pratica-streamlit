# Declaração de Uso de IA

**Nome:** Gabriel França  
**Data:** 27/10/2026 (Aula 21), 28/10/2026 (Aula 22) e 29/10/2026 (Aula 23)

## Ferramenta

Utilizei o Claude Code (Anthropic), com o modelo Claude Opus 5.5, integrado ao VS Code, como apoio durante o desenvolvimento do projeto.

## Prompt usado

**Aula 21:** enviei os slides da aula e o link do repositório-modelo para organizar a primeira entrega. Também utilizei o prompt disponível em [layout-skeleton-prompt.md](layout-skeleton-prompt.md) como referência para a estrutura inicial do `app.py`.

**Aula 22:** enviei os slides da Aula 22 e solicitei apoio para continuar os dashboards, seguindo o `ROTEIRO.md`, o `ALTAIR-CROSSFILTER.md` e as orientações de Streamlit (`developing-with-streamlit`). Conferi as métricas e testei o funcionamento dos filtros e gráficos durante a implementação.

**Aula 23:** enviei os slides da Aula 23 e pedi uma revisão dos dashboards e do repositório antes da publicação. Os ajustes foram conferidos com o aplicativo aberto no navegador. Fiz o deploy no Streamlit Community Cloud pela minha própria conta.

## O que foi aceito, modificado ou rejeitado e por quê

### Aula 21

- **Aceito:**
  - Estrutura inicial do `app.py`, com filtros na sidebar, áreas de correlação e distribuição e avisos para casos de borda.
  - Adaptação do notebook `notebooks/eda-com-downloads.ipynb` para ler os dados diretamente de `data/raw/`, mantendo o salvamento do dataset original em `data/raw/dataset.csv` e do tratado em `data/clean/dataset.csv`.
  - Rascunho do primeiro dashboard em `entregas/rascunho-dashboard1.png`.
- **Modificado:**
  - Preferi usar um `selectbox` para escolher a variável (com `Sales` como padrão) e apenas um slider de intervalo, em vez de vários sliders. Assim, a sidebar ficou mais simples e ocupou menos espaço.
- **Rejeitado:**
  - Nenhuma sugestão foi descartada nesta etapa.

### Aula 22

- **Aceito:**
  - Uso de `@st.cache_data` no `src/data_loader.py` para evitar leituras desnecessárias do CSV.
  - Configuração visual em `.streamlit/config.toml`, com temas claro e escuro, fonte Inter e cores próximas das que eu já utilizava na EDA.
  - Dashboard 1 em `src/dashboard1.py`, com heatmap de Spearman, histogramas e linha de mediana, além do tratamento de situações como seleção de poucas variáveis, intervalos sem pedidos e correlação indefinida.
  - Organização dos dois dashboards em abas no `app.py`, com filtros específicos para cada visualização.
  - Indicadores de pedidos, faturamento, ticket médio e taxa de problema. Antes de usar essas métricas no dashboard, conferi os cálculos em pandas e registrei as justificativas em `entregas/justificativa-metricas.md`.
  - Rascunho do segundo dashboard em `entregas/rascunho-dashboard2.png`, preparado antes da implementação.
  - Dashboard 2 em `src/dashboard2.py`, com KPIs, comparação com período anterior, gráfico por categoria com seleção cruzada, faixas de valor de `Sales` e taxa de problema por forma de pagamento.
- **Modificado:**
  - Não houve mudanças relevantes em relação à proposta desta aula.
- **Rejeitado:**
  - Nenhuma sugestão foi descartada nesta etapa.

### Aula 23

- **Aceito:**
  - Ajustes feitos após conferir o aplicativo no navegador: números no padrão brasileiro nos gráficos, nomes completos das variáveis no heatmap e melhorias nos rótulos e nas legendas.
  - Histograma de idade com uma barra para cada idade, para facilitar a identificação da anomalia aos 41 anos.
  - Exibição das taxas nas barras do gráfico de forma de pagamento e atualização da legenda das faixas de valor conforme os filtros aplicados.
  - Revisão da estrutura do repositório e atualização da versão mínima do Streamlit no `requirements.txt` para 1.66, utilizada nos testes.
  - Reorganização do README do projeto, incluindo descrição, principais análises, capturas de tela em `docs/img/`, tecnologias e estrutura das pastas.
- **Modificado:**
  - Não houve mudanças relevantes em relação à proposta desta aula.
- **Rejeitado:**
  - Nenhuma sugestão foi descartada nesta etapa.

## Considerações finais

A IA foi utilizada para apoiar a estruturação do código, a implementação dos componentes e a revisão do projeto. Ao longo das três aulas, acompanhei as entregas, conferi as métricas, testei as funcionalidades e fiz escolhas sobre os filtros e a apresentação dos dados. A publicação no Streamlit Community Cloud foi realizada por mim.
