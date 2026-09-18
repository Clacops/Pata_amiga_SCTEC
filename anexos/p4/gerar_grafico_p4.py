import os
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# 1. Dados consolidados da Tabela P4
pracas = [
    "Vale do Itajai", "Grande Florianópolis", "Norte Industrial", "Litoral Sul",
    "Litoral Norte", "Extremo Oeste", "Carbonífera", "Serra Catarinense",
    "Meio-Oeste", "Foz do Itajaí", "Planalto Norte", "Planalto Serrano"
]

faturamento_k = np.array([633.7, 283.5, 175.4, 137.1, 128.9, 98.4, 88.7, 80.5, 59.0, 46.7, 31.1, 29.3])
share_rede = np.array([35.34, 15.81, 9.78, 7.64, 7.19, 5.48, 4.95, 4.49, 3.29, 2.61, 1.73, 1.64])
receita_dom = np.array([4.28, 2.15, 1.83, 2.36, 2.11, 1.56, 1.32, 1.83, 1.16, 0.63, 0.94, 1.01])

# 2. Configuração do ambiente 3D
fig = plt.figure(figsize=(13, 8))
ax = fig.add_subplot(111, projection='3d')

# Mapa de cores baseado na receita por domicílio (eficiência)
norm = plt.Normalize(receita_dom.min(), receita_dom.max())
cmap = plt.cm.viridis
cores = cmap(norm(receita_dom))

# Dimensões geométricas das barras
dx = np.ones(len(pracas)) * 1.2
dy = np.ones(len(pracas)) * 0.15
dz = faturamento_k

# Renderização das barras tridimensionais
ax.bar3d(share_rede - dx/2, receita_dom - dy/2, np.zeros(len(pracas)), dx, dy, dz, 
         color=cores, alpha=0.9, edgecolor='black', linewidth=0.6)

# Anotações executivas de destaque (usando 'R\$' para escapar o cifrão)
ax.text(35.34, 4.28, 650, "Vale do Itajaí\n(Líder: R$ 4,28/dom)", fontsize=9, fontweight='bold', color='#1b4332')
ax.text(15.81, 2.15, 300, "Grande Florianópolis", fontsize=8.5, fontweight='bold', color='#1b4332')
ax.text(9.78, 1.83, 190, "Norte Industrial", fontsize=8, fontweight='bold')
ax.text(2.61, 0.63, 65, "Foz do Itajaí (Gargalo: R$ 0,63)", fontsize=8, fontweight='bold', color='#9d0208')

# Customização dos eixos com cifrões escapados (R\$)
ax.set_xlabel("Share da Rede (%)", fontsize=11, fontweight="bold", labelpad=12)
ax.set_ylabel(r"Receita / Domicílio (R\$)", fontsize=11, fontweight="bold", labelpad=12)
ax.set_zlabel(r"Faturamento Rateado (mil R\$)", fontsize=11, fontweight="bold", labelpad=12)

ax.set_xlim(0, 38)
ax.set_ylim(0.4, 4.6)
ax.set_zlim(0, 700)

# Ângulo de visualização tridimensional
ax.view_init(elev=24, azim=125)

# Título usando string raw com escape de cifrão: r"..." e R\$
plt.title(
    r"Concentração e Penetração por Praça (Visão 3D)" + "\n" +
    r"Volume Rateado (R\$) x Participação na Rede (%) x Eficiência por Domicílio (R\$)", 
    fontsize=12, fontweight="bold", pad=22
)

# Barra lateral com a graduação de eficiência
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, shrink=0.55, aspect=14, pad=0.08)
cbar.set_label(r"Receita / Domicílio (R\$)", fontsize=10, fontweight="bold")

# Salva dinamicamente na mesma pasta do script
output_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(output_dir, "grafico_3d_barras_pracas_p4.jpg")


# bbox_inches='tight' substitui o tight_layout() sem quebrar em projeções 3D
plt.savefig(img_path, dpi=300, bbox_inches='tight')
plt.show()
print(f"Gráfico 3D salvo com sucesso em: {img_path}")