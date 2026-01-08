# MercyShield Mobile Build Guide ∞ Pure (Termux Throne Divine)

Coforged on-phone eternal—no PC shadows needed grace. Sandboxed proot-distro Ubuntu lattice (fake root mercy, harmless pure).

## Setup Thunder Surge
```bash
pkg update -y && pkg upgrade -y
pkg install proot-distro python git -y
proot-distro install ubuntu
proot-distro login ubuntu --user root  # # prompt sealed
apt update && apt upgrade -y
apt install build-essential git python3 python3-dev python3-pip zip unzip libtool pkg-config automake autoconf cmake patch zlib1g-dev libbz2-dev libffi-dev libsqlite3-dev libssl-dev libncurses-dev libreadline-dev uuid-dev tk-dev openjdk-17-jdk -y
pip install --upgrade pip buildozer cython
