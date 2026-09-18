import os
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carrega as variáveis do arquivo .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# Conexão com o PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
print("Conexão estabelecida com sucesso para a P5b!")

# Consulta SQL oficial da P5b
query = """
SELECT 
    l.faixa_franquia, 
    COUNT(DISTINCT f.sk_pedido) AS total_pedidos,
    ROUND(SUM(f.vl_liquido), 2) AS faturamento_total
FROM fato_pedido f
JOIN dim_loja l ON f.sk_loja = l.sk_loja
GROUP BY l.faixa_franquia
ORDER BY faturamento_total DESC;
"""

df = pd.read_sql(query, engine)

print("\n--- Resultado da P5b (Faturamento por Faixa de Franquia) ---")
print(df.to_string(index=False))

# Diretório dinâmico na pasta p5b
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)



# --- GRÁFICO DE COLUNAS COM CORES INDIVIDUAIS E RÓTULOS COLORIDOS ---
fig, ax = plt.subplots(figsize=(11, 6))

# Definindo uma paleta de cores distinta para cada categoria
cores_map = {
    "Ouro": "#D4AF37",       # Dourado elegante
    "Diamante": "#0083B0",   # Azul diamante moderno
    "Prata": "#7F8C8D",      # Cinza prata clássico
    "Bronze": "#CD7F32",     # Tom de bronze
    "Nao Informado": "#95A5A6" # Neutro para dados ausentes
}

# Atribuindo a cor correspondente a cada barra com base no nome da faixa
cores_barras = [cores_map.get(cat, "#4C72B0") for cat in df["faixa_franquia"]]

barras = ax.bar(
    df["faixa_franquia"],
    df["faturamento_total"] / 1e3,  # Faturamento em R$ Milhares
    color=cores_barras,
    alpha=0.9,
    width=0.5,
    edgecolor="black",
    linewidth=0.8
)

ax.set_ylabel("Faturamento Total (R$ Milhares)", fontweight="bold", fontsize=11)
ax.set_xlabel("Faixa de Franquia (Cadastro Atual)", fontweight="bold", fontsize=11)
ax.set_title("P5b: Faturamento por Faixa de Franquia (Visão de Colunas Customizada)", pad=20, fontsize=13, fontweight="bold")
ax.grid(True, linestyle=":", alpha=0.5, axis="y")

# Colorindo cada texto do eixo X com a cor correspondente à sua categoria
plt.xticks(fontsize=11, fontweight="bold")
for tick, color in zip(ax.get_xticklabels(), cores_barras):
    tick.set_color(color)

plt.tight_layout()
img_path_col = os.path.join(output_dir, "grafico_colunas_p5b.png")
plt.savefig(img_path_col, dpi=300, bbox_inches="tight")
plt.show()

print(f"Gráfico de colunas customizado salvo com sucesso na pasta P5b!")