import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from utils import converter_colunas, formatar_percentual

# TODO - Fazer com que o gráfico retorne os 10 ativos mais seguros para os investidores iniciantes

# Estilo visual mais limpo
sns.set_style("whitegrid")
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10
})

# Carregar dados
fiis_df = pd.read_csv('fiis.csv', sep=';', low_memory=False)
acoes_df = pd.read_csv('acoes.csv', sep=';', low_memory=False)

# Verificar todas as colunas disponíveis
print("Colunas disponíveis no DataFrame:")
print(acoes_df.columns.tolist())
print(fiis_df.columns.tolist())

fiis_df = converter_colunas(fiis_df)
acoes_df = converter_colunas(acoes_df)
acoes_df_seguras = acoes_df

# Filtros
fiis_df = fiis_df[fiis_df["DY"].notnull() & (fiis_df["DY"] > 2)]
acoes_df = acoes_df[acoes_df["DY"].notnull() & (acoes_df["DY"] > 2)]

if "Liquidez" in fiis_df.columns:
    fiis_df = fiis_df[fiis_df["Liquidez"] > 100000]

if "Liquidez" in acoes_df.columns:
    acoes_df = acoes_df[acoes_df["Liquidez"] > 100000]

if "Preço" in fiis_df.columns:
    fiis_df = fiis_df[fiis_df["Preço"] < 100]

if "Preço" in acoes_df.columns:
    acoes_df = acoes_df[acoes_df["Preço"] < 100]

# Selecionar os top 10
top_fiis = fiis_df.nlargest(10, "DY")[["TICKER", "DY"]]
top_acoes = acoes_df.nlargest(10, "DY")[["TICKER", "DY"]]

# Plot
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle("Top 10 FIIs e Ações com Maiores Rendimentos de Dividendos", fontsize=18, fontweight='bold')

# Cores
cores_fiis = sns.color_palette("Blues_d", len(top_fiis))
cores_acoes = sns.color_palette("Greens_d", len(top_acoes))

# FIIs
bars1 = axes[0].bar(top_fiis["TICKER"], top_fiis["DY"], color=cores_fiis, edgecolor='black', linewidth=0.7)
axes[0].set_title("FIIs")
axes[0].set_ylabel("Rendimento de dividendos (%)")
axes[0].yaxis.set_major_formatter(FuncFormatter(formatar_percentual))
axes[0].grid(axis="y", linestyle="--", alpha=0.6)
axes[0].tick_params(axis='x', rotation=45)

# Rótulos nas barras
for bar in bars1:
    height = bar.get_height()
    axes[0].annotate(f'{height:.2f}%',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 5),
                     textcoords="offset points",
                     ha='center', va='bottom',
                     fontsize=9,
                     bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", lw=0.5))

# Ações
bars2 = axes[1].bar(top_acoes["TICKER"], top_acoes["DY"], color=cores_acoes, edgecolor='black', linewidth=0.7)
axes[1].set_title("Ações")
axes[1].set_ylabel("Rendimento de dividendos (%)")
axes[1].yaxis.set_major_formatter(FuncFormatter(formatar_percentual))
axes[1].grid(axis="y", linestyle="--", alpha=0.6)
axes[1].tick_params(axis='x', rotation=45)

# Rótulos nas barras
for bar in bars2:
    height = bar.get_height()
    axes[1].annotate(f'{height:.2f}%',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 5),
                     textcoords="offset points",
                     ha='center', va='bottom',
                     fontsize=9,
                     bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", lw=0.5))

# Ajustes finais
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.subplots_adjust(wspace=0.25)
plt.show()

# -----------------------------
#  Ações mais seguras
# -----------------------------
# Filtrar apenas ações com dados válidos
acoes_df_seguras = acoes_df_seguras.dropna(subset=['DY', 'P/L', 'P/VP', 'ROE', 'DIVIDA LIQUIDA / EBIT'])

# Critérios para ações seguras:
# 1. DY positivo (pagam dividendos)
# 2. P/L razoável (entre 5 e 20)
# 3. P/VP menor que 1.5 (não muito supervalorizada)
# 4. ROE positivo
# 5. Dívida Líquida/EBIT baixa (menor que 3)
acoes_seguras = acoes_df_seguras[
    (acoes_df_seguras['DY'] > 0) &
    (acoes_df_seguras['P/L'].between(5, 20)) &
    (acoes_df_seguras['P/VP'] < 1.5) &
    (acoes_df_seguras['ROE'] > 0) &
    (acoes_df_seguras['DIVIDA LIQUIDA / EBIT'].abs() < 3)
]

# Ordenar por uma combinação de fatores (DY alto, P/L moderado, P/VP baixo)
acoes_seguras['SCORE'] = (
    acoes_seguras['DY'] * 0.4 +
    (1 / acoes_seguras['P/L']) * 0.3 +
    (1 / acoes_seguras['P/VP']) * 0.2 +
    acoes_seguras['ROE'] * 0.1
)

# Selecionar as top 10
top_10_seguras = acoes_seguras.nlargest(10, 'SCORE')[['TICKER', 'DY', 'P/L', 'P/VP', 'ROE', 'DIVIDA LIQUIDA / EBIT', 'SCORE']]

# Plot
plt.figure(figsize=(14, 8))
sns.set_style("whitegrid")
plt.title("Top 10 Ações Mais Seguras para Investidores Iniciantes", fontsize=16, pad=20)

# Criar gráfico de barras
bars = plt.bar(top_10_seguras['TICKER'], top_10_seguras['SCORE'],
               color=sns.color_palette("Greens_d", len(top_10_seguras)),
               edgecolor='black', linewidth=0.7)

plt.ylabel("Score de Segurança", fontsize=12)
plt.xlabel("Ticker", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.6)

# Adicionar rótulos com DY 
for i, bar in enumerate(bars):
    height = bar.get_height()
    ticker = top_10_seguras.iloc[i]['TICKER']
    dy = top_10_seguras.iloc[i]['DY']
    plt.annotate(f'DY: {dy:.2f}%',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 5),
                 textcoords="offset points",
                 ha='center', va='bottom',
                 fontsize=9,
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", lw=0.5))

# Adicionar tabela com outros indicadores
col_labels = ['P/L', 'P/VP', 'ROE', 'Dívida/EBIT', 'Score']
table_data = top_10_seguras[['P/L', 'P/VP', 'ROE', 'DIVIDA LIQUIDA / EBIT', 'SCORE']].values
table = plt.table(
    cellText=table_data.round(2),
    rowLabels=top_10_seguras['TICKER'].values,
    colLabels=col_labels,
    cellLoc='center',
    loc='bottom',
    bbox=[0.1, -0.7, 0.8, 0.4]
)

# -----------------------------
#  FIIs mais seguros
# -----------------------------

print("\n📌 Colunas originais:")
print(fiis_df)

# Converter colunas numéricas corretamente
colunas_numericas_fiis = [
    'DY', 'P/VP', 'LIQUIDEZ MEDIA DIARIA', 'CAGR DIVIDENDOS 3 ANOS', 'PATRIMONIO'
]
for coluna in colunas_numericas_fiis:
    fiis_df[coluna] = (
        fiis_df[coluna]
        .astype(str)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
    )
    fiis_df[coluna] = pd.to_numeric(fiis_df[coluna], errors='coerce')


fiis_df_seguro = fiis_df.dropna(subset=colunas_numericas_fiis)

# Criar SCORE
fiis_df_seguro['SCORE'] = (
    fiis_df_seguro['DY'] * 0.4 +
    (1 / fiis_df_seguro['P/VP']) * 0.2 +
    fiis_df_seguro['CAGR DIVIDENDOS 3 ANOS'] * 0.2 +
    (fiis_df_seguro['LIQUIDEZ MEDIA DIARIA'] / 1_000_000) * 0.1 +
    (fiis_df_seguro['PATRIMONIO'] / 1_000_000_000) * 0.1
)

# Verificação final
if fiis_df_seguro.empty:
    print("❌ Nenhum FII passou pelos critérios aplicados. Ajuste os filtros ou revise os dados.")
else:
    # Selecionar os 10 melhores
    top_10_fiis_seguro = fiis_df_seguro.nlargest(10, 'SCORE')[[
        'TICKER', 'DY', 'P/VP', 'CAGR DIVIDENDOS 3 ANOS',
        'LIQUIDEZ MEDIA DIARIA', 'PATRIMONIO', 'SCORE'
    ]]

    print("\n📊 Top 10 FIIs mais seguros:")
    print(top_10_fiis_seguro)

    # Plot
    plt.figure(figsize=(14, 8))
    sns.set_style("whitegrid")
    plt.title("Top 10 FIIs Mais Seguros para Investidores Iniciantes", fontsize=16, pad=20)

    bars = plt.bar(top_10_fiis_seguro['TICKER'], top_10_fiis_seguro['SCORE'],
                   color=sns.color_palette("Blues_d", len(top_10_fiis_seguro)),
                   edgecolor='black', linewidth=0.7)

    plt.ylabel("Score de Segurança", fontsize=12)
    plt.xlabel("Ticker", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    # Anotar DY
    for i, bar in enumerate(bars):
        height = bar.get_height()
        dy = top_10_fiis_seguro.iloc[i]['DY']
        plt.annotate(f'DY: {dy:.2f}%',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 5),
                     textcoords="offset points",
                     ha='center', va='bottom',
                     fontsize=9,
                     bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", lw=0.5))

plt.subplots_adjust(bottom=0.4)
plt.tight_layout()
plt.show()

# Mostrar a tabela no console também
print("\nTop 10 Ações Mais Seguras:")
print(top_10_seguras.to_string(index=False))
print("\nTop 10 FIIs Mais Seguros:")
print(top_10_fiis_seguro.to_string(index=False))
