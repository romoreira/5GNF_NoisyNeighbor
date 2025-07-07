import os
import requests

# Diretório de destino
output_dir = "resources_stats"
os.makedirs(output_dir, exist_ok=True)

# Lista dos charts que você quer baixar
charts = [
    'net_packets_eth0',
    "net_n3",
    "net_packets_n3",
    'net_errors_n3',
    'net_drops_n3',
    'net_fifo_n3',
    'net_events_n3',
    'cpu',
    'pgfaults',
    'mem',
    'mem_usage',
    'mem_usage_limit',
    'io',
    'mem_utilization',
    'cpu_limit'
]

# Parâmetros fixos
base_url = "http://127.0.0.1:19999/api/v1/data"
uuid = "pode66752c1_4239_4c43_9459_b9290c1733f6"
container_id = "1a36f7e76f2abfbdbd500495001583060caa30d223ba1c9976cf253e22bc53e7"
after = 1751886858

before = 1751886931



for chart in charts:
    full_chart = f"cgroup_k8s_kubepods-slice_kubepods-burstable-slice_kubepods-burstable-{uuid}-slice_cri-containerd-{container_id}-scope.{chart}"
    params = {
        "chart": full_chart,
        "format": "csv",
        "after": after,
        "before": before
    }
    response = requests.get(base_url, params=params)  # <-- Aqui está o ajuste
    print(print(response.url))
    if response.status_code == 200:
        filepath = os.path.join(output_dir, f"{chart}.csv")
        with open(filepath, "w") as f:
            f.write(response.text)
        print(f"[✔] Saved {filepath}")
    else:
        print(f"[✘] Failed to fetch {chart} – HTTP {response.status_code}")