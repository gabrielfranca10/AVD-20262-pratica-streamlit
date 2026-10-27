# Declaração de Uso de IA

**Nome:** Gabriel França
**Data:** 27/10/2026

## Ferramenta

Claude Code (Anthropic), modelo Claude Opus 5.5, rodando no VS Code.

## Prompt usado

**Aula 21:** enviei os slides da aula e o link do repositório-modelo, e pedi para montar a entrega do dia. O prompt estruturado usado para gerar o esqueleto do `app.py` está em [layout-skeleton-prompt.md](layout-skeleton-prompt.md).

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
