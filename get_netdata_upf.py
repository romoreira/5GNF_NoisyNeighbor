import os
import requests

from datetime import datetime, timezone

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
uuid = "poddf7376fb_a478_4be0_8ed3_4cc228b3a39c"
container_id = "3c4f2e26c8ea277d5269aacdc1fc134e7a00dfbea5f2b592673a9af89d91efff"


# string original
after = "Fri Jul 25 22:50:33 UTC 2025"
before = "Fri Jul 25 22:51:10 UTC 2025"

# converter para objeto datetime
dt = datetime.strptime(after, "%a %b %d %H:%M:%S %Z %Y")
# definir como UTC
dt = dt.replace(tzinfo=timezone.utc)
# converter para epoch
after = int(dt.timestamp())


# converter para objeto datetime
dt = datetime.strptime(before, "%a %b %d %H:%M:%S %Z %Y")
# definir como UTC
dt = dt.replace(tzinfo=timezone.utc)
# converter para epoch
before = int(dt.timestamp())


for chart in charts:
    full_chart = f"cgroup_k8s_kubepods-slice_kubepods-{uuid}-slice_cri-containerd-{container_id}-scope.{chart}"
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