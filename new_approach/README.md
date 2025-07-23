# 🐝 bpftrace Installation Guide (v0.21.0)

This guide provides the easiest and most reliable way to install **bpftrace** on Linux systems (`x86_64` architecture), such as Ubuntu, using the precompiled binary.

---

## ✅ Requirements

- Linux system (`x86_64` architecture)
- Superuser privileges (`sudo`)

---

## 📦 Installation Steps

### 1️⃣ Download the Binary

Download the standalone executable directly from GitHub:

```bash
wget https://github.com/bpftrace/bpftrace/releases/download/v0.21.0/bpftrace
2️⃣ Make the File Executable
Set execution permissions:

bash
chmod +x bpftrace
3️⃣ Move to System PATH
Move the binary to /usr/local/bin so you can run it from any terminal:

bash
sudo mv bpftrace /usr/local/bin/
🔍 Verify the Installation
Check the installed version:

bash
bpftrace --version
Expected output:

bash
bpftrace v0.21.0