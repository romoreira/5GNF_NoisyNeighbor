#include "fixup.h"
#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

#define GTPU_PORT 2152
#define GTPU_HDR_LEN 8

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, __u32);   // IP interno (daddr)
    __type(value, __u64); // t1
    __uint(max_entries, 1024);
} flow_latency_map SEC(".maps");

SEC("classifier")
int store_teid(struct __sk_buff *skb) {
    void *data = (void *)(long)skb->data;
    void *data_end = (void *)(long)skb->data_end;

    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end) return 0;
    if (bpf_ntohs(eth->h_proto) != ETH_P_IP) return 0;

    struct iphdr *ip = (void *)(eth + 1);
    if ((void *)(ip + 1) > data_end) return 0;
    if (ip->protocol != IPPROTO_UDP) return 0;

    struct udphdr *udp = (void *)(ip + 1);
    if ((void *)(udp + 1) > data_end) return 0;
    if (bpf_ntohs(udp->dest) != GTPU_PORT) return 0;

    __u8 *gtp = (void *)(udp + 1);

    // Varre offsets possíveis logo após o header GTPU
    #pragma unroll
    for (int i = 0; i < 32; i++) {
        if (gtp + GTPU_HDR_LEN + i + 4 > (unsigned char *)data_end)
            break;
        __u8 b0 = *(gtp + GTPU_HDR_LEN + i + 0);
        __u8 b1 = *(gtp + GTPU_HDR_LEN + i + 1);
        __u8 b2 = *(gtp + GTPU_HDR_LEN + i + 2);
        __u8 b3 = *(gtp + GTPU_HDR_LEN + i + 3);

        // Máximo 2 argumentos por printk!
        bpf_printk("Offset=%d b0=%u\n", i, b0);
        bpf_printk("Offset=%d b1=%u\n", i, b1);
        bpf_printk("Offset=%d b2=%u\n", i, b2);
        bpf_printk("Offset=%d b3=%u\n", i, b3);

        if (b0 == 8 && b1 == 8 && b2 == 8 && b3 == 8) {
            bpf_printk("ACHOU 8.8.8.8 no offset %d\n", i);
            __u32 key = (b0 << 24) | (b1 << 16) | (b2 << 8) | b3;
            __u64 t1 = bpf_ktime_get_ns();
            bpf_map_update_elem(&flow_latency_map, &key, &t1, BPF_ANY);
        }
    }

    return 0;
}

char _license[] SEC("license") = "GPL";