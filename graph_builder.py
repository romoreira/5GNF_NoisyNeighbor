import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Leia o CSV
df = pd.read_csv('data.csv')

# Parâmetro para média móvel (ex: janela de 5 pontos)
window_size = 5
df['UPF CPU MA'] = df['UPF CPU'].rolling(window=window_size, min_periods=1, center=True).mean()

fig, ax1 = plt.subplots(figsize=(8,5))

marker_size = 6

# Linhas principais
ax1.plot(df['Time'], df['N3 Packets'], label='N3 Packets', marker='o', markersize=marker_size, color='#1f77b4')
ax1.plot(df['Time'], df['Throughput'], label='Throughput', marker='s', markersize=marker_size, color='#ff7f0e')
ax1.set_xlabel('Time', fontsize=18)
ax1.set_ylabel('N3 Packets / Throughput', fontsize=18)
ax1.tick_params(axis='x', labelsize=18)
ax1.tick_params(axis='y', labelsize=18)

ax2 = ax1.twinx()
# Tira marker da média móvel para suavizar ainda mais
ax2.plot(df['Time'], df['UPF CPU MA'], color='#d62728', label='UPF CPU (mean)', linewidth=2)
ax2.set_ylabel('UPF CPU (moving average)', fontsize=18, color='#d62728')
ax2.tick_params(axis='y', labelcolor='#d62728', labelsize=18)
ax2.set_ylim(bottom=0, top=df['UPF CPU MA'].max() * 1.2)

# Legenda
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
leg = ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, 1.18), ncol=3, fontsize=15)
leg.get_frame().set_linewidth(0.0)

plt.title('Metrics Evolution over Time (UPF)', fontsize=18)
plt.tight_layout()
plt.savefig('results_and_graphs/graph_ma.pdf', dpi=300)
