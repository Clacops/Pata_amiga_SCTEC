import os
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carrega as variáveis do arquivo .env de forma segura
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Conexão com o PostgreSQL local utilizando credenciais protegidas
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
print("Conexão estabelecida com sucesso para a P2!")

# Consulta SQL da Pergunta 2 (Faturamento e percentual por categoria padronizada)
query = """
SELECT 
    c.nome_categoria,
    SUM(f.vl_liquido) AS faturamento_categoria,
    ROUND(
        (SUM(f.vl_liquido) / (SELECT SUM(vl_liquido) FROM fato_pedido)) * 100.0, 2
    ) AS percentual_sobre_total
FROM fato_pedido f
INNER JOIN dim_categoria c ON f.sk_categoria = c.sk_categoria
GROUP BY c.nome_categoria
ORDER BY faturamento_categoria DESC;
"""

df = pd.read_sql(query, engine)

print("\n--- Resultado da Pergunta 2 (Concentração de Faturamento por Categoria) ---")
print(df.to_string(index=False))

# Diretório dinâmico na mesma pasta onde este script está salvo (anexos/p2)
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

# Salvando a tabela em CSV com utf-8-sig (compatível com Excel)
csv_path = os.path.join(output_dir, "tabela_faturamento_categoria_p2.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"\nTabela salva com sucesso em CSV: {csv_path}")

# --- GERANDO O GRÁFICO DUPLO (Faturamento + Percentual) ---
fig, ax1 = plt.subplots(figsize=(10, 5))

colors = [
    "#55A868" if cat != "Racao" else "#4C72B0" for cat in df["nome_categoria"]
]
bars = ax1.barh(
    df["nome_categoria"],
    df["faturamento_categoria"],
    color=colors,
    alpha=0.8,
    height=0.55,
)
ax1.set_xlabel("Faturamento Líquido Total (R$)", color="#333333", fontweight="bold")
ax1.set_ylabel("Categoria Padronizada", color="#333333", fontweight="bold")

ax2 = ax1.twiny()
ax2.plot(
    df["percentual_sobre_total"],
    df["nome_categoria"],
    color="#C44E52",
    marker="o",
    linewidth=2.5,
    markersize=8,
)
ax2.set_xlabel(
    "Percentual sobre o Total da Rede (%)", color="#C44E52", fontweight="bold"
)
ax2.set_xlim(0, 100)

plt.title(
    "Concentração de Faturamento por Categoria: Volume (R$) vs Share (%)",
    pad=20,
    fontsize=12,
    fontweight="bold",
)
plt.tight_layout()

img_path = os.path.join(output_dir, "grafico_faturamento_categoria_p2.png")
plt.savefig(img_path, dpi=300, bbox_inches="tight")
plt.show()
print(f"Gráfico salvo em: {img_path}")