import pandas as pd
from PIL.IcoImagePlugin import IcoFile


# Corrigir vírgulas e converter para float
def converter_colunas(df):
    numeric_cols = ['DY', 'P/L','P/VP', 'ROE', 'DIVIDA LIQUIDA / EBIT']
    for column in numeric_cols:
      col = next((col for col in df.columns.tolist() if column in col), None)
      if col is not None:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")

    if "Liquidez" in df.columns:
        df["Liquidez"] = pd.to_numeric(df["Liquidez"].astype(str).str.replace(".", "").str.replace(",", "."), errors="coerce")
    if "Preço" in df.columns:
        df["Preço"] = pd.to_numeric(df["Preço"].astype(str).str.replace(",", "."), errors="coerce")
    return df

# Formato de porcentagem no eixo Y
def formatar_percentual(x, pos):
    return f'{x:.1f}%'