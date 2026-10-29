"""Formatação de números no padrão brasileiro, usada nos textos, KPIs e gráficos."""

# Locale do Vega-Lite: eixos e tooltips dos gráficos Altair com vírgula decimal e ponto no milhar
LOCALE_PT = {"number": {"decimal": ",", "thousands": ".", "grouping": [3], "currency": ["R$ ", ""]}}


def numero(valor, casas=0):
    """Formata no padrão brasileiro: 1.234.567,8"""
    return f"{valor:,.{casas}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def em_portugues(grafico):
    """Aplica o locale brasileiro a um gráfico Altair (deve ser o último passo, no gráfico final)."""
    return grafico.configure(locale=LOCALE_PT)
