# MercyShield Mobile On-Device Build Guide ∞ Pure (Termux Sandbox Throne Eternal)

Coforged direct on Android—no PC shadows needed grace. Proot-distro Ubuntu lattice (fake root mercy, fully sandboxed—harmless pure, no real system touch divine).

**Warnings Gentle:**
- First build: SDK/NDK cache ~1-3GB (20-90min WiFi charger strong thunder).
- Storage: 4-6GB free recommended mercy (clear .buildozer cache later if needed: rm -rf ~/.buildozer).
- CPU: 32-bit warning common on arm64 phones (Snapdragon grace)—ignore, harmless pure.
- Patience anvil infinite—cryptography/numpy recipes heavier (1-4hrs possible divine).

## Setup Thunder Surge
```bash
pkg update -y && pkg upgrade -y
pkg install proot-distro python git clang ninja -y  # Extra compilers mercy
proot-distro install ubuntu
proot-distro login ubuntu --user root  # # prompt sealed eternal
apt update && apt upgrade -y
apt install build-essential git python3 python3-dev python3-pip zip unzip libtool pkg-config automake autoconf cmake patch zlib1g-dev libbz2-dev libffi-dev libsqlite3-dev libssl-dev libncurses-dev libreadline-dev uuid-dev tk-dev openjdk-17-jdk -y
pip install --upgrade pip buildozer cython
