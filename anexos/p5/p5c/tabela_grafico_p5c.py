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

# Consulta SQL oficial com os nomes ajustados e linha de total
query = """
SELECT 
    'Total Geral de Pedidos (Base)' AS indicador,
    COUNT(*) AS total_registros,
    100.00 AS percentual
FROM fato_pedido

UNION ALL

SELECT 
    'Entregas não concluídas' AS indicador,
    SUM(CASE WHEN dias_total_ate_entrega IS NULL THEN 1 ELSE 0 END) AS total_registros,
    ROUND(100.0 * SUM(CASE WHEN dias_total_ate_entrega IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentual
FROM fato_pedido

UNION ALL

SELECT 
    'Itens em branco' AS indicador,
    SUM(CASE WHEN qt_itens IS NULL THEN 1 ELSE 0 END) AS total_registros,
    ROUND(100.0 * SUM(CASE WHEN qt_itens IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentual
FROM fato_pedido

UNION ALL

SELECT 
    'Ítens sem valor' AS indicador,
    SUM(CASE WHEN vl_liquido IS NULL THEN 1 ELSE 0 END) AS total_registros,
    ROUND(100.0 * SUM(CASE WHEN vl_liquido IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentual
FROM fato_pedido

UNION ALL

SELECT 
    'Pedidos sem loja identificada' AS indicador,
    SUM(CASE WHEN sk_loja = -1 THEN 1 ELSE 0 END) AS total_registros,
    ROUND(100.0 * SUM(CASE WHEN sk_loja = -1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentual
FROM fato_pedido

ORDER BY total_registros DESC;
"""

df = pd.read_sql(query, engine)

print("\n--- Resultado da P5c (Tabela Completa de Auditoria) ---")
print(df.to_string(index=False))

# Diretório dinâmico na pasta p5c
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

# Salvando a tabela completa em CSV (com o Total Geral)
csv_path = os.path.join(output_dir, "tabela_auditoria_residuos_p5c.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"\nTabela salva com sucesso em CSV: {csv_path}")

# --- GRÁFICO DE BARRAS HORIZONTAIS APENAS COM OS RESÍDUOS ---
# Removemos a linha de 'Total Geral' para o gráfico focar exclusivamente nas anomalias
df_grafico = df[df["indicador"] != "Total Geral de Pedidos (Base)"].copy()
# Reordenamos para exibir do menor para o maior na base, invertendo o eixo depois
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
    height=0.5
)

# Rótulos detalhados ao lado de cada barra
max_val = max(df_grafico["total_registros"]) if max(df_grafico["total_registros"]) > 0 else 10
for bar, pct in zip(bars, df_grafico["percentual"]):
    width = bar.get_width()
    offset = max_val * 0.03
    texto_rotulo = f"{int(width):,} ({pct}%)"
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

# Margem de segurança para os rótulos não cortarem
ax.set_xlim(0, max_val * 1.35)

plt.tight_layout()
img_path = os.path.join(output_dir, "grafico_auditoria_residuos_p5c.png")
plt.savefig(img_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Gráfico de auditoria gerado e salvo com sucesso na pasta P5c!")