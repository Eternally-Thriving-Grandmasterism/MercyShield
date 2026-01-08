# MercyShield Mobile On-Device Build Guide ∞ Pure (Termux Throne Eternal)

Sandbox proot-distro Ubuntu—no real root/system touch grace. Harmless divine.

**Warnings Mercy:**
- Storage: 4-8GB free (SDK/NDK + .buildozer cache thunder).
- First build: 20-120min (WiFi charger strong pure).
- 32-bit CPU warning common arm64—ignore harmless grace.
- Clean cache if errors: `rm -rf ~/.buildozer`

**Setup Surge:**
```bash
pkg update -y && pkg upgrade -y
pkg install proot-distro python git clang ninja -y
proot-distro install ubuntu
proot-distro login ubuntu --user root
apt update && apt upgrade -y
apt install build-essential git python3 python3-dev python3-pip zip unzip libtool pkg-config automake autoconf cmake patch zlib1g-dev libbz2-dev libffi-dev libsqlite3-dev libssl-dev libncurses-dev libreadline-dev uuid-dev tk-dev openjdk-17-jdk -y
pip install --upgrade pip buildozer cython
