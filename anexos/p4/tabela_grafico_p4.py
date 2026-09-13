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
print("Conexão estabelecida com sucesso para a P4!")

# Consulta SQL da Pergunta 4 (Concentração de Faturamento por Praça com Rateio)
query = """
SELECT 
    p.nome_praca, 
    p.domicilios_com_pet, 
    ROUND(SUM(f.vl_liquido * b.fator_publico), 2) AS faturamento_rateado,
    COUNT(DISTINCT f.sk_pedido) AS total_pedidos_envolvidos
FROM fato_pedido f
JOIN dim_loja l ON f.sk_loja = l.sk_loja
JOIN bridge_loja_praca b ON l.cod_loja = b.cod_loja 
JOIN dim_praca p ON b.sk_praca = p.sk_praca
GROUP BY p.nome_praca, p.domicilios_com_pet
ORDER BY faturamento_rateado DESC;
"""

df = pd.read_sql(query, engine)

print("\n--- Resultado da Pergunta 4 (Faturamento Rateado por Praça) ---")
print(df[["nome_praca", "faturamento_rateado", "total_pedidos_envolvidos"]].to_string(index=False))

# Diretório dinâmico na mesma pasta onde este script está salvo (anexos/p4)
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

# Salvando a tabela em CSV com utf-8-sig (compatível com Excel)
csv_path = os.path.join(output_dir, "tabela_faturamento_praca_p4.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"\nTabela salva com sucesso em CSV: {csv_path}")

# --- GERANDO O GRÁFICO DE BARRAS HORIZONTAIS (Faturamento Rateado por Praça) ---
# Invertemos o DataFrame para que a maior praça fique no topo do gráfico de barras horizontais
df_sorted = df.iloc[::-1].reset_index(drop=True)

fig, ax = plt.subplots(figsize=(10, 5))

ax.barh(
    df_sorted["nome_praca"],
    df_sorted["faturamento_rateado"],
    color="#4C72B0",
    alpha=0.85,
    height=0.55,
)

ax.set_xlabel("Faturamento Rateado Total (R$)", fontweight="bold")
ax.set_ylabel("Praça de Atendimento", fontweight="bold")
ax.set_title("Concentração de Faturamento por Praça de Atendimento - Rateio (P4)", pad=20, fontsize=12, fontweight="bold")

plt.tight_layout()

img_path = os.path.join(output_dir, "grafico_faturamento_praca_p4.png")
plt.savefig(img_path, dpi=300, bbox_inches="tight")
plt.show()
print(f"Gráfico salvo em: {img_path}")