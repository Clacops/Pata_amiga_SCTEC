import os
import matplotlib.pyplot as plt
import numpy as np
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
print("Conexão estabelecida com sucesso para a P3!")

# Consulta SQL da Pergunta 3 (Ticket médio com/sem desconto e share por canal)
query = """
SELECT 
    canal_pedido,
    ROUND(AVG(CASE WHEN houve_desconto = 1 THEN vl_liquido END), 2) AS ticket_com_desconto,
    ROUND(AVG(CASE WHEN houve_desconto = 0 THEN vl_liquido END), 2) AS ticket_sem_desconto,
    COUNT(sk_pedido) AS total_pedidos,
    SUM(houve_desconto) AS qtd_com_desconto,
    COUNT(sk_pedido) - SUM(houve_desconto) AS qtd_sem_desconto,
    SUM(vl_liquido) AS faturamento_canal,
    ROUND((SUM(vl_liquido) / (SELECT SUM(vl_liquido) FROM fato_pedido)) * 100.0, 2) AS share_faturamento_perc
FROM fato_pedido
GROUP BY canal_pedido
ORDER BY share_faturamento_perc DESC;
"""

df = pd.read_sql(query, engine)

print("\n--- Resultado da Pergunta 3 (Desconto e Representatividade por Canal) ---")
print(
    df[["canal_pedido", "ticket_com_desconto", "ticket_sem_desconto", "share_faturamento_perc"]].to_string(index=False)
)

# Diretório dinâmico na mesma pasta onde este script está salvo (anexos/p3)
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

# Salvando a tabela em CSV com utf-8-sig (compatível com Excel)
csv_path = os.path.join(output_dir, "tabela_desconto_canal_p3.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"\nTabela salva com sucesso em CSV: {csv_path}")

# --- GERANDO O GRÁFICO DE BARRAS AGRUPADAS (Ticket Médio: Com vs Sem Desconto) ---
fig, ax = plt.subplots(figsize=(10, 5))

x = np.arange(len(df["canal_pedido"]))
width = 0.35

rects1 = ax.bar(x - width/2, df["ticket_com_desconto"], width, label="Com Desconto", color="#4C72B0", alpha=0.85)
rects2 = ax.bar(x + width/2, df["ticket_sem_desconto"], width, label="Sem Desconto", color="#55A868", alpha=0.85)

ax.set_ylabel("Ticket Médio Líquido (R$)", fontweight="bold")
ax.set_xlabel("Canal de Pedido", fontweight="bold")
ax.set_title("Comparativo de Ticket Médio: Com vs Sem Desconto por Canal (P3)", pad=20, fontsize=12, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(df["canal_pedido"])
ax.legend()

plt.tight_layout()

img_path = os.path.join(output_dir, "grafico_desconto_canal_p3.png")
plt.savefig(img_path, dpi=300, bbox_inches="tight")
plt.show()
print(f"Gráfico salvo em: {img_path}")