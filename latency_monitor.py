import subprocess
import json
import time
import csv
import os
from datetime import datetime

MAP_ID_INGRESS = "325"
MAP_ID_EGRESS  = "330"
CSV_FILE = "latency_log.csv"

def get_map_dump(map_id):
    try:
        result = subprocess.run(
            ["bpftool", "map", "dump", "id", map_id, "-j"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True
        )
        entries = json.loads(result.stdout)
        output = {}
        for entry in entries:
            if "formatted" in entry and "key" in entry["formatted"] and "value" in entry["formatted"]:
                key = int(entry["formatted"]["key"])
                value = int(entry["formatted"]["value"])
                output[key] = value
        return output
    except Exception as e:
        print(f"Erro lendo mapa {map_id}: {e}")
        return {}

def ns_to_ms(ns):
    return ns / 1_000_000

# Verifica se o arquivo existe e está vazio para escrever cabeçalho
file_exists = os.path.exists(CSV_FILE)
file_empty = True
if file_exists:
    file_empty = os.path.getsize(CSV_FILE) == 0

with open(CSV_FILE, mode="a", newline="") as csvfile:
    writer = csv.writer(csvfile)
    if file_empty:
        writer.writerow(["timestamp_utc", "ip_key", "delta_ns", "delta_ms"])

print("IP_key".ljust(12), "delta_ns".ljust(15), "delta_ms")
print("-" * 40)

while True:
    ingress = get_map_dump(MAP_ID_INGRESS)
    egress  = get_map_dump(MAP_ID_EGRESS)

    with open(CSV_FILE, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for key in ingress:
            if key in egress:
                delta = egress[key] - ingress[key]
                delta_ms = ns_to_ms(delta)
                timestamp = datetime.utcnow().isoformat()
                print(f"{key:<12} {delta:<15} {delta_ms:.3f} ms")
                writer.writerow([timestamp, key, delta, f"{delta_ms:.3f}"])
    time.sleep(1)