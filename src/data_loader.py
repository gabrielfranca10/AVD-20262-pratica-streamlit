import pandas as pd
import streamlit as st


# Cache: o CSV é lido uma vez só e reaproveitado em todas as interações (cada clique reexecuta o app.py)
@st.cache_data
def load_data(path="data/clean/dataset.csv"):
    """Lê o dataset já tratado (exportado ao final do notebook de EDA)."""
    return pd.read_csv(path, parse_dates=["OrderDate", "SignupDate"])
