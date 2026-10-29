# [IA] Claude Code (Claude Opus 5.5) – estrutura do app e abas dos dois dashboards (esqueleto da Aula 21 gerado a partir do rascunho, abas na Aula 22)
import streamlit as st

from src import dashboard1, dashboard2
from src.data_loader import load_data

st.set_page_config(
    page_title="Dashboards | E-commerce de Eletrônicos",
    page_icon=":material/monitoring:",
    layout="wide",
)

df = load_data()

# Uma aba por dashboard. Com on_change="rerun" só a aba aberta é executada,
# então a sidebar mostra apenas os filtros do dashboard que está na tela.
aba_d1, aba_d2 = st.tabs(
    [":material/scatter_plot: Dashboard 1 — Correlação e distribuição", ":material/speed: Dashboard 2 — KPIs"],
    key="aba",
    on_change="rerun",
)

if aba_d1.open:
    with aba_d1:
        dashboard1.render(df)

if aba_d2.open:
    with aba_d2:
        dashboard2.render(df)
