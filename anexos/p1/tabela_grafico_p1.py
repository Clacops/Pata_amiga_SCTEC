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

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
print("Conexão estabelecida com sucesso!")

# Consulta SQL da Pergunta 1 (Tempos de entrega por loja)
query = """
SELECT 
    l.nome_loja,
    ROUND(CAST(AVG(f.dias_integracao_separacao) AS NUMERIC), 2) AS media_integracao_separacao,
    ROUND(CAST(AVG(f.dias_separacao_nota) AS NUMERIC), 2) AS media_separacao_nota,
    ROUND(CAST(AVG(f.dias_nota_despacho) AS NUMERIC), 2) AS media_nota_despacho,
    ROUND(CAST(AVG(f.dias_despacho_entrega) AS NUMERIC), 2) AS media_despacho_entrega,
    ROUND(CAST(AVG(f.dias_total_ate_entrega) AS NUMERIC), 2) AS media_total_ate_entrega,
    COUNT(f.sk_pedido) AS total_pedidos_avaliados
FROM fato_pedido f
INNER JOIN dim_loja l ON f.sk_loja = l.sk_loja
GROUP BY l.nome_loja
ORDER BY media_total_ate_entrega DESC;
"""

df = pd.read_sql(query, engine)
print("\n--- Resultado da Pergunta 1 ---")
print(df.to_string(index=False))


# Garante que o diretório de saída seja o mesmo onde o script está localizado (anexos/p1)
output_dir = os.path.dirname(os.path.abspath(__file__))

##os.makedirs(output_dir, exist_ok=True)
##csv_path = os.path.join(output_dir, "tabela_tempos_entrega_p1.csv")
##df.to_csv(csv_path, index=False, encoding="utf-8-sig")
##print(f"\nTabela salva em: {csv_path}")

# Gerando o Gráfico e salvando no mesmo lugar
plt.figure(figsize=(10, 5))
plt.barh(df["nome_loja"], df["media_total_ate_entrega"], color="#4C72B0")
plt.xlabel("Média de Dias Totais até a Entrega")
plt.ylabel("Loja")
plt.title("Tempo Médio Total de Entrega por Loja (Pergunta 1)")
plt.gca().invert_yaxis()
plt.tight_layout()

img_path = os.path.join(output_dir, "grafico_tempos_entrega_p1.png")
plt.savefig(img_path, dpi=300, bbox_inches="tight")
plt.show()
print(f"Gráfico salvo em: {img_path}")