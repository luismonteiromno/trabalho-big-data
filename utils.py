import pandas as pd

# Corrigir vírgulas e converter para float
def converter_colunas(df):
    df["DY"] = pd.to_numeric(df["DY"].astype(str).str.replace(",", "."), errors="coerce")
    if "Liquidez" in df.columns:
        df["Liquidez"] = pd.to_numeric(df["Liquidez"].astype(str).str.replace(".", "").str.replace(",", "."), errors="coerce")
    if "Preço" in df.columns:
        df["Preço"] = pd.to_numeric(df["Preço"].astype(str).str.replace(",", "."), errors="coerce")
    return df

# Formato de porcentagem no eixo Y
def formatar_percentual(x, pos):
    return f'{x:.1f}%'
