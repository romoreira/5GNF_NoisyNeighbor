# ⚙️ PREREQUISITES (run once)

apt update
apt install -y clang llvm linux-tools-$(uname -r) linux-cloud-tools-$(uname -r)
mkdir -p headers

# minimal headers for compiling
echo -e '#define TC_ACT_OK 0\n#define ETH_P_IP 0x0800' > headers/fixup.h
bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h

# 🛠️ COMPILE BPF PROGRAM (e.g., egress_latency_bpf.c)

clang -O2 -g -target bpf -c egress_latency_bpf.c -o egress_latency_bpf.o \
  -I. -I./headers

# 📌 LOAD BPF PROGRAM

bpftool prog load egress_latency_bpf.o /sys/fs/bpf/egress_latency_bpf type classifier

# 🔗 ATTACH TO eth0 INTERFACE (egress)

tc qdisc add dev eth0 clsact 2>/dev/null || true
tc filter add dev eth0 egress bpf da pinned /sys/fs/bpf/egress_latency_bpf

# 🔎 CHECK KERNEL LOG FOR LATENCY OUTPUT

journalctl -k | grep latency_ns
