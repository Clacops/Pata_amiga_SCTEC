import os
import matplotlib.pyplot as plt
import numpy as np
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
print("Conexão estabelecida com sucesso para a P5a!")

# Consulta SQL contemplando as dimensões e o filtro de corte acima da média
query = """
SELECT 
    l.nome_loja,
    p.nome_praca,
    p.domicilios_com_pet AS populacao_referencia,
    ROUND((SUM(f.qt_itens * b.fator_publico) * 1000.0) / NULLIF(p.domicilios_com_pet, 0), 2) AS itens_por_mil_habitantes,
    ROUND(AVG(f.dias_total_ate_entrega), 2) AS tempo_medio_entrega_dias
FROM fato_pedido f
JOIN dim_loja l ON f.sk_loja = l.sk_loja
JOIN bridge_loja_praca b ON l.cod_loja = b.cod_loja
JOIN dim_praca p ON b.sk_praca = p.sk_praca
GROUP BY l.nome_loja, p.nome_praca, p.domicilios_com_pet
HAVING AVG(f.dias_total_ate_entrega) > (
    SELECT AVG(f_sub.dias_total_ate_entrega) 
    FROM fato_pedido f_sub
)
ORDER BY itens_por_mil_habitantes DESC, tempo_medio_entrega_dias DESC;
"""

df = pd.read_sql(query, engine)

print("\n--- Resultado da P5a (Lojas Críticas: Densidade x Tempo x População) ---")
print(df.to_string(index=False))

# Diretório dinâmico na pasta p5a
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

# Salvando a tabela em CSV
csv_path = os.path.join(output_dir, "tabela_densidade_p5a.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"\nTabela salva com sucesso em CSV: {csv_path}")

# --- GERANDO O GRÁFICO DE BARRAS AGRUPADAS (DUO-BAR) ---
# Ordenamos de forma ascendente para que a maior densidade fique no topo do gráfico horizontal
df_sorted = df.sort_values("itens_por_mil_habitantes", ascending=True)

labels = df_sorted["nome_loja"] + " (" + df_sorted["nome_praca"] + ")"
x = np.arange(len(labels))
width = 0.35  # Largura das barras

altura_figura = max(8, len(df_sorted) * 0.4)
fig, ax1 = plt.subplots(figsize=(12, altura_figura))

# Como as escalas são diferentes (Itens/Mil Hab vs Dias), normalizamos ou usamos eixos separados.
# Para barras agrupadas limpas, criamos duas barras lado a lado. Como as ordens de grandeza são parecidas (~5 a 15), ficam ótimas juntas.
rects1 = ax1.barh(x - width/2, df_sorted["itens_por_mil_habitantes"], width, label="Itens por 1.000 Hab.", color="#4C72B0", alpha=0.85)
rects2 = ax1.barh(x + width/2, df_sorted["tempo_medio_entrega_dias"], width, label="Tempo Médio de Entrega (Dias)", color="#C44E52", alpha=0.85)

ax1.set_yticks(x)
ax1.set_yticklabels(labels, fontsize=9, fontweight="bold")
ax1.set_xlabel("Escala Comparativa (Valor Numérico)", fontweight="bold", fontsize=11)
ax1.set_title("Matriz de Decisão P5a: Comparativo de Densidade vs Prazo Logístico", pad=20, fontsize=13, fontweight="bold")
ax1.legend(loc="lower right")

ax1.grid(True, linestyle=":", alpha=0.5, axis="x")
plt.tight_layout()

img_path = os.path.join(output_dir, "grafico_barras_duplas_p5a.png")
plt.savefig(img_path, dpi=300, bbox_inches="tight")
plt.show()
print(f"Gráfico de barras duplas salvo em: {img_path}")