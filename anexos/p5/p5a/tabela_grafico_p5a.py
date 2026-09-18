import os
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np

# Top 10 lojas ranqueadas por densidade decrescente
lojas = [
    "Rio dos Cedros",
    "Presidente Getúlio",
    "Ibirama",
    "Itapoá",
    "Santo Amaro da Imperatriz",
    "Taió",
    "Timbó",
    "Gaspar",
    "Otacílio Costa",
    "Ituporanga"
]

densidade = [41.87, 34.84, 32.07, 25.94, 23.71, 19.37, 17.86, 16.72, 15.86, 13.75]
dias = [14.24, 14.16, 15.39, 15.39, 15.88, 14.57, 7.70, 8.01, 15.61, 16.53]

# Inverte para posicionar a 1ª colocada (Rio dos Cedros) no topo vertical
lojas_inv = lojas[::-1]
densidade_inv = densidade[::-1]
dias_inv = dias[::-1]

fig, ax1 = plt.subplots(figsize=(12, 7.5))

# Margens calibradas para nomes extensos e eixos superior/inferior
plt.subplots_adjust(left=0.25, right=0.93, top=0.84, bottom=0.12)

y_pos = np.arange(len(lojas_inv))
cores_barras = ['#d90429' if d > 10 else '#2b5c8f' for d in dias_inv]

# Barras horizontais de densidade
bars = ax1.barh(y_pos, densidade_inv, color=cores_barras, alpha=0.85, height=0.55)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(lojas_inv, fontsize=10.5, fontweight='semibold')
ax1.set_xlabel("Densidade de Vendas (Itens por 1.000 Habitantes)", fontsize=11, fontweight='bold', color='#1d3557', labelpad=10)
ax1.set_xlim(0, 52)
ax1.grid(axis='x', linestyle='--', alpha=0.5)

# Eixo superior para os dias médios de entrega
ax2 = ax1.twiny()
ax2.plot(dias_inv, y_pos, color='#ff7b00', marker='o', linewidth=2.5, markersize=8)
ax2.set_xlabel("Tempo Médio de Entrega (Dias)", fontsize=11, fontweight='bold', color='#ff7b00', labelpad=12)
ax2.set_xlim(0, 22)
ax2.grid(False)

# Rótulo de densidade ao lado de cada barra
for idx, val in enumerate(densidade_inv):
    ax1.text(val + 0.8, idx, f"{val:.1f} itens", va='center', fontsize=9, fontweight='bold', color='#1d3557')

# Rótulo de dias de entrega acima de cada ponto laranja
for idx, dia in enumerate(dias_inv):
    ax2.annotate(f"{dia:.1f}d", (dia, idx), xytext=(0, 9), textcoords="offset points",
                 ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#c44e00')

# Título global centralizado
fig.suptitle("Top 10 Lojas por Densidade (P5A): Itens/1k Hab vs. Tempo de Entrega", 
             fontsize=13, fontweight='bold', y=0.96)

# Legenda posicionada em área neutra
p_azul = mpatches.Patch(color='#2b5c8f', label='Densidade (Entrega < 10 dias)')
p_verm = mpatches.Patch(color='#d90429', label='Densidade (Entrega > 10 dias)')
l_laranja = mlines.Line2D([], [], color='#ff7b00', marker='o', label='Tempo Médio Entrega (Dias)')
ax1.legend(handles=[p_azul, p_verm, l_laranja], loc='lower left', bbox_to_anchor=(0.58, 0.03), frameon=True, fontsize=9.2)

output_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(output_dir, "grafico_top10_densidade_p5a.png")
plt.savefig(img_path, dpi=300)
plt.show()

print(f"Gráfico Top 10 salvo com sucesso em: {img_path}")