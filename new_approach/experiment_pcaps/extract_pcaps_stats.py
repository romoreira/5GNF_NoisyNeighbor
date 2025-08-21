#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import math
import argparse
from collections import defaultdict

from scapy.all import PcapReader, UDP, TCP

# Tenta carregar RTP (fica em scapy.contrib)
# Caso não exista, o script ainda roda, apenas sem métricas de RTP.
try:
    from scapy.contrib.rtp import RTP
    HAS_RTP = True
except Exception:
    RTP = None
    HAS_RTP = False

# Mapas simples de clock por Payload Type (comum em RTP)
# 0=PCMU 8kHz, 8=PCMA 8kHz; demais (p.ex. dinâmicos de vídeo) assumimos 90kHz
def rtp_clockrate(pt: int) -> int:
    if pt in (0, 8):
        return 8000
    # fallback razoável para vídeo/dinâmicos
    return 90000

def analyze_pcap(path):
    total_pkts = 0
    total_bytes = 0
    udp_pkts = 0
    tcp_pkts = 0

    first_ts = None
    last_ts = None

    # Estruturas para RTP por fluxo (SSRC)
    # Para cada fluxo: últimos seq/arrival/rtp_ts e acumuladores de perda/jitter
    rtp_streams = {}
    rtp_total_pkts = 0
    rtp_total_lost = 0

    # Jitter RFC3550 por fluxo: J += (|D|-J)/16, com D = (Ta_diff - Ts_diff/clock)
    # Guardamos J por SSRC
    rtp_jitter = defaultdict(float)

    # Para cálculo de perda, precisamos rastrear seq anterior por SSRC
    # Usamos janela simples (sem reordenação avançada, mas cobre a maioria dos casos)
    # key = (ssrc, pt) apenas para estatística separada por PT se quiser evoluir depois
    rtp_last = {}  # key -> dict(seq, arrival, rtp_ts, clock)

    def pkt_len(pkt):
        # len(pkt) costuma funcionar; se necessário, tente bytes(pkt)
        try:
            return len(pkt)
        except Exception:
            try:
                return len(bytes(pkt))
            except Exception:
                return 0

    with PcapReader(path) as rd:
        for pkt in rd:
            try:
                ts = float(pkt.time)
            except Exception:
                # Se não tiver timestamp, ignora
                continue

            if first_ts is None:
                first_ts = ts
            last_ts = ts

            size = pkt_len(pkt)
            total_bytes += size
            total_pkts += 1

            if UDP in pkt:
                udp_pkts += 1
            elif TCP in pkt:
                tcp_pkts += 1

            # RTP (opcional)
            if HAS_RTP and UDP in pkt and pkt.haslayer(RTP):
                try:
                    rtp = pkt[RTP]
                    ssrc = int(rtp.ssrc)
                    pt = int(rtp.payload_type)
                    seq = int(rtp.sequence)
                    ts_rtp = int(rtp.timestamp)
                    clk = rtp_clockrate(pt)

                    key = (ssrc, pt)
                    prev = rtp_last.get(key)
                    rtp_total_pkts += 1

                    if prev:
                        # perda por gap de sequência (16 bits, considera wrap)
                        prev_seq = prev["seq"]
                        gap = (seq - prev_seq) & 0xFFFF
                        if gap > 1:
                            rtp_total_lost += (gap - 1)

                        # jitter RFC3550
                        Ta_diff = ts - prev["arrival"]
                        Ts_diff = (ts_rtp - prev["rtp_ts"]) / float(clk)
                        D = Ta_diff - Ts_diff
                        J = rtp_jitter[ssrc]
                        J = J + (abs(D) - J) / 16.0
                        rtp_jitter[ssrc] = J

                    # atualiza estado
                    rtp_last[key] = {"seq": seq, "arrival": ts, "rtp_ts": ts_rtp, "clock": clk}
                except Exception:
                    # Qualquer parse estranho -> ignora este pacote RTP
                    pass

    if total_pkts == 0 or first_ts is None or last_ts is None:
        return {
            "file": os.path.basename(path),
            "duration_s": 0.0,
            "packets": 0,
            "total_bytes": 0,
            "bps": 0.0,
            "pps": 0.0,
            "udp_pct": 0.0,
            "tcp_pct": 0.0,
            "rtp_pkts": 0,
            "rtp_streams": 0,
            "rtp_loss_pct": 0.0,
            "rtp_jitter_ms": 0.0,
        }

    duration = max(last_ts - first_ts, 1e-9)
    bps = (8.0 * total_bytes) / duration
    pps = total_pkts / duration
    udp_pct = 100.0 * udp_pkts / total_pkts
    tcp_pct = 100.0 * tcp_pkts / total_pkts

    # Agrega jitter médio (ms) entre os fluxos observados
    # Obs.: RFC3550 define J em unidades de tempo (seg), aqui convertemos p/ ms
    rtp_stream_count = len(set(ssrc for (ssrc, _pt) in rtp_last.keys()))
    if rtp_stream_count > 0:
        avg_jitter_ms = 1000.0 * (sum(rtp_jitter.values()) / rtp_stream_count)
    else:
        avg_jitter_ms = 0.0

    # Perda (%): lost / (received + lost)
    if rtp_total_pkts + rtp_total_lost > 0:
        rtp_loss_pct = 100.0 * (rtp_total_lost / float(rtp_total_pkts + rtp_total_lost))
    else:
        rtp_loss_pct = 0.0

    return {
        "file": os.path.basename(path),
        "duration_s": round(duration, 6),
        "packets": total_pkts,
        "total_bytes": total_bytes,
        "bps": round(bps, 3),
        "pps": round(pps, 6),
        "udp_pct": round(udp_pct, 3),
        "tcp_pct": round(tcp_pct, 3),
        "rtp_pkts": rtp_total_pkts,
        "rtp_streams": rtp_stream_count,
        "rtp_loss_pct": round(rtp_loss_pct, 3),
        "rtp_jitter_ms": round(avg_jitter_ms, 3),
    }

def analyze_directory(pcap_dir):
    rows = []
    for name in sorted(os.listdir(pcap_dir)):
        if not name.lower().endswith((".pcap", ".pcapng")):
            continue
        path = os.path.join(pcap_dir, name)
        try:
            stats = analyze_pcap(path)
            rows.append(stats)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            rows.append({
                "file": name,
                "duration_s": 0.0,
                "packets": 0,
                "total_bytes": 0,
                "bps": 0.0,
                "pps": 0.0,
                "udp_pct": 0.0,
                "tcp_pct": 0.0,
                "rtp_pkts": 0,
                "rtp_streams": 0,
                "rtp_loss_pct": 0.0,
                "rtp_jitter_ms": 0.0,
            })

    return rows

def main():
    parser = argparse.ArgumentParser(description="Estatísticas de PCAPs com Scapy (inclui RTP se disponível).")
    parser.add_argument("--dir", required=True, help="Diretório com arquivos .pcap/.pcapng")
    parser.add_argument("--out", default="pcap_stats.csv", help="Caminho do CSV de saída")
    args = parser.parse_args()

    rows = analyze_directory(args.dir)
    fieldnames = [
        "file","duration_s","packets","total_bytes","bps","pps",
        "udp_pct","tcp_pct","rtp_pkts","rtp_streams","rtp_loss_pct","rtp_jitter_ms"
    ]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"[ok] Estatísticas salvas em: {args.out}")

if __name__ == "__main__":
    main()
