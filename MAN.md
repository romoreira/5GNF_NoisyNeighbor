
# ====== Preparação inicial (uma vez só) ======

# 1. Instale dependências essenciais
apt update
apt install -y clang llvm linux-tools-$(uname -r) linux-cloud-tools-$(uname -r) bpftool

# 2. Crie pasta para headers mínimos e arquivos auxiliares
mkdir -p headers

# 3. Gere arquivo fixup.h com definições mínimas necessárias
echo -e '#define TC_ACT_OK 0\n#define ETH_P_IP 0x0800' > headers/fixup.h

# 4. Gere o arquivo vmlinux.h a partir da BTF do kernel
bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h


# ======= N3 (Ingress) =======

# 1. Compile o programa BPF para ingress (n3)
clang -O2 -g -target bpf -c ingress_store_teid.c -o ingress_store_teid.o -I. -I./headers

# 2. Remova filtros e objetos antigos da n3 (limpeza)
tc filter delete dev n3 ingress 2>/dev/null || true
tc qdisc del dev n3 clsact 2>/dev/null || true
rm -f /sys/fs/bpf/ingress_store_teid

# 3. Adicione qdisc clsact na interface n3
tc qdisc add dev n3 clsact 2>/dev/null || true

# 4. Carregue e "pinna" o programa BPF na FS BPF
bpftool prog load ingress_store_teid.o /sys/fs/bpf/ingress_store_teid type classifier

# 5. Anexe o programa à interface n3 no ingress
tc filter add dev n3 ingress bpf da pinned /sys/fs/bpf/ingress_store_teid

# ===========================


# ======= ETH0 (Egress) =======

# 1. Compile o programa BPF para egress (eth0)
clang -O2 -g -target bpf -c egress_store_sensor.c -o egress_store_sensor.o -I. -I./headers

# 2. Remova filtros e objetos antigos da eth0 (limpeza)
tc filter delete dev eth0 egress 2>/dev/null || true
tc qdisc del dev eth0 clsact 2>/dev/null || true
rm -f /sys/fs/bpf/egress_store_sensor

# 3. Adicione qdisc clsact na interface eth0
tc qdisc add dev eth0 clsact 2>/dev/null || true

# 4. Carregue e "pinna" o programa BPF na FS BPF
bpftool prog load egress_store_sensor.o /sys/fs/bpf/egress_store_sensor type classifier

# 5. Anexe o programa à interface eth0 no egress
tc filter add dev eth0 egress bpf da pinned /sys/fs/bpf/egress_store_sensor

# ===========================
