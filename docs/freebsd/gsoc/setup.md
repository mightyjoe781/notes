

# Setup

## Cloud VMs





## M1 Mac VMs

## Quick setup arm64-VM

````bash
# install packages 
pkg install git opensbi qemu-8.1.1 ntfy lua54 lua54-luarocks vim tmux

# lua packages
luarocks54 install posix luacheck

# clone the freebsd-src repo
git clone https://github.com/mightyjoe781/freebsd-src && cd freebsd-src

# make buildworld buildkernel
make -j `sysctl -n hw.ncpu` -DWITHOUT_SYSTEM_COMPILER buildworld buildkernel
make -j `sysctl -n hw.ncpu` TARGET=amd64 TARGET_ARCH=amd64 toolchain

# save mount script
mkdir -p ~/freebsd-src/tools/boot/bootloader_test
echo "mount -v -t nfs 192.168.64.1:/System/Volumes/Data/Users/smk/personal/gsoc/fbsd/tools/boot/bootloader_test /root/freebsd-src/tools/boot/bootloader_test" >> mount.sh
chmod +x mount.sh


# run a basic test
lua54 main.lua -a amd64:amd64 -f ufs -i gpt -e none
````





---

### Notes

amd64, arm64, riscv, armv7, powerpc/64

Running qemu with script
qemu-system-riscv64: Unable to find the RISC-V BIOS "/usr/local/share/opensbi/lp64/generic/firmware/fw_jump.elf"

- make toolchain

### Armv7

- Image is not there
- Mount Issues were there
- compressed.tgz for now its fine, later decide where to host the resources

### Open Items

- Explore python for running test parallel
- move towards CI side of things 

### powerpc & powerpc64

- finding correct Recipe 
- Powerpc64 with openfirmware

-----

115049 -- security code

