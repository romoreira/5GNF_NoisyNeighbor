import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Ensure output directory exists
os.makedirs('results_and_graphs', exist_ok=True)
df = pd.read_csv('data.csv')

window_size = 5
df['UPF CPU MA'] = df['UPF CPU'].rolling(window=window_size, min_periods=1, center=True).mean()

# === 1. N3 Packets Graph ===
fig, ax = plt.subplots(figsize=(4.5,3))
ln1 = ax.plot(df['Time'], df['N3 Packets'], marker='o', color='#1f77b4', markersize=4, label='N3 Packets')
#ax.set_xlabel('Time', fontsize=14)
ax.set_ylabel('N3 Packets', fontsize=14)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
#ax.set_title('N3 Packets', fontsize=14, pad=8)
leg = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=1, frameon=False, fontsize=12)
plt.tight_layout(rect=[0,0,1,0.93])
plt.savefig('results_and_graphs/n3_packets_acm.pdf', dpi=300)
plt.close()

# === 2. Throughput × UPF CPU Graph ===
fig, ax1 = plt.subplots(figsize=(4.5,3))
ln1 = ax1.plot(df['Time'], df['Throughput'], marker='s', color='#ff7f0e', markersize=4, label='Throughput')
#ax1.set_xlabel('Time', fontsize=14)
ax1.set_ylabel('Throughput (Mbps)', fontsize=14, color='#ff7f0e')
ax1.tick_params(axis='y', labelcolor='#ff7f0e', labelsize=12)
ax1.tick_params(axis='x', labelsize=12)

ax2 = ax1.twinx()
ln2 = ax2.plot(df['Time'], df['UPF CPU MA'], color='#d62728', linewidth=2, label='UPF CPU (MA)')
ax2.set_ylabel('UPF CPU (%)', fontsize=14, color='#d62728')
ax2.tick_params(axis='y', labelcolor='#d62728', labelsize=12)

# Legend below the plot, single line, clear style
lines = ln1 + ln2
labels = [l.get_label() for l in lines]
leg = ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=False, fontsize=12)

#ax1.set_title('Throughput × UPF CPU', fontsize=14, pad=8)
plt.tight_layout(rect=[0,0,1,0.93])
plt.savefig('results_and_graphs/throughput_upfcpu_acm.pdf', dpi=300)
plt.close()

print('Saved as results_and_graphs/n3_packets_acm.pdf and throughput_upfcpu_acm.pdf')
