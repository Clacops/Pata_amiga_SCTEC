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
print("Conexão estabelecida com sucesso para a P5c (Auditoria Final)!")

# 1. Consulta SQL para alimentar o DataFrame df
query_auditoria = """
WITH auditoria AS (
    SELECT 
        'Pedidos sem loja identificada' AS indicador, 
        COUNT(*) AS total_registros
    FROM fato_pedido 
    WHERE sk_loja = -1 

    UNION ALL

    SELECT 
        'Entregas não concluídas' AS indicador, 
        COUNT(*) AS total_registros
    FROM fato_pedido 
    WHERE dias_total_ate_entrega IS NULL

    UNION ALL

    SELECT 
        'Itens ou valores em branco/zerados' AS indicador, 
        COUNT(*) AS total_registros
    FROM fato_pedido 
    WHERE qt_itens IS NULL OR qt_itens = 0 OR vl_liquido IS NULL OR vl_liquido = 0
)
SELECT 
    indicador,
    total_registros,
    ROUND(100.0 * total_registros / (SELECT COUNT(*) FROM fato_pedido), 2) AS percentual
FROM auditoria;
"""

df = pd.read_sql(query_auditoria, engine)
print("Dados carregados com sucesso:")
print(df)

# Define a pasta de saída baseada no diretório atual do script
output_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Filtragem e ordenação para o gráfico de barras horizontais
df_grafico = df[df["indicador"] != "Total Geral de Pedidos (Base)"].copy()
df_grafico = df_grafico.sort_values(by="total_registros", ascending=True)

fig, ax = plt.subplots(figsize=(11, 5))
cor_unica = "#4C72B0"

bars = ax.barh(
    df_grafico["indicador"],
    df_grafico["total_registros"],
    color=cor_unica,
    alpha=0.85,
    edgecolor="black",
    linewidth=0.8,
    height=0.48
)

# Rótulos detalhados ao lado de cada barra
max_val = max(df_grafico["total_registros"]) if not df_grafico.empty and max(df_grafico["total_registros"]) > 0 else 10
for bar, pct in zip(bars, df_grafico["percentual"]):
    width = bar.get_width()
    offset = max_val * 0.02
    texto_rotulo = f"{int(width):,} ({pct:.2f}%)"
    ax.text(
        width + offset,
        bar.get_y() + bar.get_height() / 2,
        texto_rotulo,
        va="center",
        ha="left",
        fontsize=10,
        fontweight="bold",
        color="#333333"
    )

ax.set_xlabel("Total de Registros Anômalos", fontweight="bold", fontsize=11)
ax.set_title("P5c: Auditoria de Qualidade de Dados (Resíduos por Categoria)", pad=20, fontsize=13, fontweight="bold")
ax.grid(True, linestyle=":", alpha=0.5, axis="x")

# Margem de segurança para os rótulos não cortarem na direita
ax.set_xlim(0, max_val * 1.30)

plt.tight_layout()
img_path = os.path.join(output_dir, "grafico_auditoria_residuos_p5c.png")
plt.savefig(img_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Gráfico de auditoria gerado e salvo com sucesso em: {img_path}")