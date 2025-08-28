# 5GNF Noisy Neighbor – New Approach

This repository investigates the impact of "noisy neighbor" effects on 5G network slice isolation, focusing on per-packet GTP-U decapsulation overhead using eBPF/bpftrace instrumentation in the User Plane Function (UPF).

## Directory: `new_approach`

This directory contains scripts and guides to reproducibly measure per-packet decapsulation latency for a specific User Equipment (UE) IP, leveraging kernel probes via bpftrace.

### Contents

- [`latency.bt`](https://github.com/romoreira/5GNF_NoisyNeighbor/blob/main/new_approach/latency.bt):  
  bpftrace script to monitor and log the overhead of GTP-U decapsulation for a specific UE IP.  
- [`README.md`](https://github.com/romoreira/5GNF_NoisyNeighbor/blob/main/new_approach/README.md):  
  Step-by-step guide to installing bpftrace for running the instrumentation scripts.

---

## How to Reproduce

### 1. **Install bpftrace**

Follow the official or provided guide to install the correct version (v0.21.0):

```bash
wget https://github.com/bpftrace/bpftrace/releases/download/v0.21.0/bpftrace
chmod +x bpftrace
sudo mv bpftrace /usr/local/bin/
bpftrace --version
# Expected: bpftrace v0.21.0
```

See the [`new_approach/README.md`](https://github.com/romoreira/5GNF_NoisyNeighbor/blob/main/new_approach/README.md) for details.

### 2. **Configure the Measurement Script**

Edit [`latency.bt`](https://github.com/romoreira/5GNF_NoisyNeighbor/blob/main/new_approach/latency.bt) to set your target UE IP address:
- Find and update the section:
  ```c
  // Exemplo para 10.1.0.44
  $target_ip = (44 << 24) | (0 << 16) | (1 << 8) | 10;
  ```
  Change the values to match your UE IP in the format `(D << 24) | (C << 16) | (B << 8) | A`.

### 3. **Run the bpftrace Script**

```bash
sudo bpftrace new_approach/latency.bt
```

### 4. **Generate and Replay GTP-U Traffic**

- Set up your 5G testbed (e.g., Free5GC, Kubernetes environment as described in your paper).
- Generate GTP-U traffic with known TEIDs and QFIs, including the UE IP you configured in the script.
- The script will print lines like:

  ```
  UE IP: 10.1.0.44 | Decapsulation Overhead: 123456 ns
  ```

---

## Notes

- The script only reports decapsulation latency for the specified UE IP.
- For best reproducibility, pin the UPF container/process to a single CPU core and monitor system load as described in your evaluation setup.

## References

- See [`new_approach/README.md`](https://github.com/romoreira/5GNF_NoisyNeighbor/blob/main/new_approach/README.md) for the latest bpftrace installation instructions.
- For further details and context, refer to the main paper or [project documentation](https://github.com/romoreira/5GNF_NoisyNeighbor).

---

**More details and source code available in the [new_approach directory](https://github.com/romoreira/5GNF_NoisyNeighbor/tree/main/new_approach).**

*Note: This summary is based on the available files in the `new_approach` directory. [See more on GitHub.](https://github.com/romoreira/5GNF_NoisyNeighbor/tree/main/new_approach)*
