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
fiis_df = pd.read_csv('fiis.csv', sep=';')
acoes_df = pd.read_csv('acoes.csv', sep=';')


fiis_df = converter_colunas(fiis_df)
acoes_df = converter_colunas(acoes_df)

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
