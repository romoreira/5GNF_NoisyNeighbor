#include "fixup.h"
#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

#define DST_SENSOR bpf_htonl(0x08080808) // 8.8.8.8 em ordem de rede

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, __u32);   // dst_ip
    __type(value, __u64); // t2
    __uint(max_entries, 1024);
} flow_egress_map SEC(".maps");

SEC("classifier")
int mark_egress(struct __sk_buff *skb) {
    void *data = (void *)(long)skb->data;
    void *data_end = (void *)(long)skb->data_end;

    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end) return 0;
    if (bpf_ntohs(eth->h_proto) != ETH_P_IP) return 0;

    struct iphdr *ip = (void *)(eth + 1);
    if ((void *)(ip + 1) > data_end) return 0;

    // Só registra se o destino é 8.8.8.8
    if (ip->daddr == DST_SENSOR) {
        __u64 t2 = bpf_ktime_get_ns();
        __u32 key = ip->daddr; // chave é o destino (8.8.8.8)
        bpf_map_update_elem(&flow_egress_map, &key, &t2, BPF_ANY);
        bpf_printk("EGRESS: src=%x dst=%x\n", bpf_ntohl(ip->saddr), bpf_ntohl(ip->daddr));
    }

    return 0;
}

char _license[] SEC("license") = "GPL";
