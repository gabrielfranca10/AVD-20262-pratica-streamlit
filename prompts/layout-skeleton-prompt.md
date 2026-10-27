# Template: rascunho de layout → esqueleto do app

Preencha cada bloco e envie à ferramenta de IA.

## Contexto

Sou aluno de Análise e Visualização de Dados (CESAR School, 2026.2), Aula 21 — Streamlit parte 1. O projeto é o Dashboard 1 (correlação + distribuição das variáveis quantitativas) a partir da minha EDA da Aula 11, feita sobre um dataset de e-commerce de eletrônicos e acessórios (`clean_final_data.csv`, ~49 mil pedidos de jan/2024 a jun/2026).

Estrutura do repositório: `app.py` na raiz, `src/data_loader.py` (função `load_data()`, lê `data/clean/dataset.csv`), notebooks em `notebooks/`, rascunhos em `entregas/`.

## Entrada

Rascunho anexado: `entregas/rascunho-dashboard1.png`.

Colunas do dataset tratado: `OrderID`, `CustomerID`, `OrderDate`, `ProductID`, `Quantity`, `Discount`, `PaymentMethod`, `Status`, `Age`, `City`, `SignupDate`, `CustomerSegment`, `ProductName`, `Category`, `UnitPrice`, `Sales`, `desfecho`, `cadastro_inconsistente`, `idade_41`, `produto_suspeito`, `Sales_log`, `faixa_etaria`.

Variáveis quantitativas (mesmas do `VARS_QUANT` da EDA): `Age`, `Quantity`, `Discount`, `UnitPrice`, `Sales`.

Perguntas que o dashboard deve responder: como as quantitativas se correlacionam entre si (Spearman, já que nenhuma é normal) e como cada uma se distribui; e se cortar os valores extremos (ex.: a cauda longa de `Sales`) muda essas relações.

Layout em texto: sidebar à esquerda com o seletor de variáveis e o filtro de intervalo; no topo da área principal, um contador de pedidos filtrados; abaixo, Correlação (heatmap) à esquerda e Distribuição (histogramas) à direita, lado a lado; no fim, um expander com a tabela filtrada.

## Restrições

- Só Streamlit; editar apenas `app.py`.
- Carregar os dados via `src/data_loader.py` (`load_data()`), sem caminho absoluto.
- Gerar só o esqueleto estrutural, sem os gráficos: usar placeholders (`st.info`) e `# TODO` onde entram o heatmap e os histogramas (Aula 22).
- Widgets mínimos: 1 seletor de variáveis (`st.multiselect`) e 1 filtro de intervalo (`st.slider` de faixa), ambos na sidebar.
- Tratar os casos de borda com aviso: menos de 2 variáveis na correlação, nenhuma variável ou nenhum pedido na distribuição.

## Formato de saída

Um único `app.py` completo, pronto para `streamlit run app.py`, com comentários curtos marcando cada seção do layout.
