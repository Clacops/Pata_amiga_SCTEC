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
print("Conexão estabelecida com sucesso para a P5c!")

# Consulta SQL oficial da P5c
query = """
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
WHERE qt_itens IS NULL OR qt_itens = 0 OR vl_liquido IS NULL OR vl_liquido = 0;
"""

df = pd.read_sql(query, engine)

print("\n--- Resultado da P5c (Auditoria de Qualidade / Resíduos) ---")
print(df.to_string(index=False))

# Diretório dinâmico na pasta p5c
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

# Salvando a tabela em CSV
csv_path = os.path.join(output_dir, "tabela_auditoria_residuos_p5c.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"\nTabela salva com sucesso em CSV: {csv_path}")

# --- GRÁFICO DE BARRAS HORIZONTAIS COM MESMA COR E DESTAQUE DE VALORES BAIXOS ---
fig, ax = plt.subplots(figsize=(11, 5))

# Mesma cor sólida para todas as barras (ex: Azul corporativo elegante)
cor_unica = "#4C72B0"

bars = ax.barh(
    df["indicador"],
    df["total_registros"],
    color=cor_unica,
    alpha=0.85,
    edgecolor="black",
    linewidth=0.8,
    height=0.5
)

# Adicionando os valores numéricos exatamente ao lado de cada barra com destaque
max_val = max(df["total_registros"]) if max(df["total_registros"]) > 0 else 10
for bar in bars:
    width = bar.get_width()
    # Se o valor for muito pequeno (ex: 3), garantimos um deslocamento mínimo para o texto não ficar colado
    offset = max_val * 0.02
    ax.text(
        width + offset,
        bar.get_y() + bar.get_height() / 2,
        f"{int(width):,}",
        va="center",
        ha="left",
        fontsize=10,
        fontweight="bold",
        color="#333333"
    )

ax.set_xlabel("Total de Registros Anômalos / Resíduos", fontweight="bold", fontsize=11)
ax.set_title("P5c: Auditoria de Qualidade de Dados (Resíduos e Inconsistências)", pad=20, fontsize=13, fontweight="bold")
ax.grid(True, linestyle=":", alpha=0.5, axis="x")

# Expandimos um pouco o limite do eixo X para dar espaço aos rótulos numéricos sem cortar
ax.set_xlim(0, max_val * 1.15)

plt.tight_layout()
img_path = os.path.join(output_dir, "grafico_auditoria_residuos_p5c.png")
plt.savefig(img_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Gráfico de auditoria customizado salvo com sucesso na pasta P5c!")