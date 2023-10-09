## FreeBSD Development Environment on M1 Macs



I was a GSoC (Google Summer of Code) student in year 2023 and it was very interesting summer to spend working with Warner Losh on Designing CI Boot Loader Test Harness for different FreeBSD Architectures. Main Idea of project was to write several qemu recipes for pretty much most of first tier architectures in FreeBSD, and somehow make the script user friendly enough so people can drive it via a config, later this config can integrated on FreeBSD CI systems to remove the possibility of shipping broken Bootloader.

WiFi support on FreeBSD has been a lot shaky mostly due to manufactures not sharing specs to their WiFi Hardware. I had a old laptop that I used to install FreeBSD and work little bit on, but without a WiFi in this modern day, it was a difficult developer experience.

Later Warner arranged a Jail running on his bare metal server rack for me to connect via ssh. This was a temporary arrangement for me to proceed with the summer. And I always wanted to develop things locally. I tried various methods to get VSCode running on FreeBSD remotely but could not make it work. Finally for the entire summer project I was working on my local and pushing my changes to git, then logging into the server via ssh, and pulling in the changes from git. A long tiring process.

After this struggle I was keen on finding the solution for this problem so I found this article online by John Grafton (https://www.jrgsystems.com/) who seems to share similar interest in MacBook developement Environments as me. So I set out to emulate his development environment across my M1. Following Steps are more of personal note for me to remember what I did to make this work.

### 1. Creating a FreeBSD QEMU VM

[Reference](https://gist.github.com/ctsrc/a1f57933a2cde9abc0f07be12889f97f)

1. Installing X-Code
2. Installing Homebrew and QEMU
3. Download pre-build EDKII OVMF EFI image for QEMU
4. Prepare pflash for non-volatile variable store, such as screen-resolutions etc.
5. Download FreeBSD arm64 image
6. Decompress VM image
7. Grow Image Size
8. Run QEMU using this script

#### Installing X-code

```
xcode-select --install
```

#### Installing Homebrew and QEMU

````bash
brew install qemu wget
rehash
qemu-system-aarch64 --version
````

#### Download pre-build EDKII OVMF EFI image for QEMU

[Link](https://gist.github.com/niw/4f1f9bb572f40d406866f23b3127919b/raw/f546faea68f4149c06cca88fa67ace07a3758268/QEMU_EFI-cb438b9-edk2-stable202011-with-extra-resolutions.tar.gz) : Please Check references if link doesn’t work

#### Prepare pflash for non-volatile variable store, such as screen-resolutions etc.

````bash
mkdir ~/qemu-vm/
cd ~/qemu-vm/
tar xvf ~/Downloads/QEMU_EFI-cb438b9-edk2-stable202011-with-extra-resolutions.tar.gz
dd if=/dev/zero of=pflash0.img bs=1m count=64
dd if=/dev/zero of=pflash1.img bs=1m count=64
dd if=QEMU_EFI.fd of=pflash0.img conv=notrunc
dd if=QEMU_VARS.fd of=pflash1.img conv=notrunc
````

#### Download FreeBSD arm64 image

````
wget https://ftp2.uk.freebsd.org/pub/FreeBSD/releases/VM-IMAGES/13.1-RELEASE/aarch64/Latest/FreeBSD-13.1-RELEASE-arm64-aarch64.raw.xz
````

#### Decompress VM image

````bash
mv ~/Downloads/FreeBSD-13.2-RELEASE-arm64-aarch64.raw.xz .
unxz -k FreeBSD-13.2-RELEASE-arm64-aarch64.raw.xz
````

#### Grow Image Size

````bash
qemu-img resize -f raw FreeBSD-13.1-RELEASE-arm64-aarch64.raw +60G
````

#### Run QEMU using this script

````bash
echo "
qemu-system-aarch64 \
  -M virt \
  -accel hvf \
  -cpu host \
  -smp 4 \
  -m 8192M \
  -drive file=pflash0.img,format=raw,if=pflash,readonly=on \
  -drive file=pflash1.img,format=raw,if=pflash \
  -device virtio-gpu-pci \
  -display default,show-cursor=on \
  -device qemu-xhci \
  -device usb-kbd \
  -device usb-tablet \
  -device intel-hda \
  -device hda-duplex \
  -drive file=FreeBSD-13.2-RELEASE-arm64-aarch64.raw,format=raw,if=virtio,cache=writethrough \
  -serial mon:stdio \
  -audiodev none,id=hdac \
  -nic vmnet-shared \
  -nographic
" >> freeBSD.run
chmod +x freeBSD.run
````

### 2. Setting up NFS on M1

[Reference](https://www.jrgsystems.com/posts/2023-09-08-developing-freebsd-on-macos/)

1. Write Exports File
2. Enable nfsd on M1
3. Checking nfsd is working correctly

#### Write Exports File

````txt
### /etc/exports on MacBook
/System/Volumes/Data/smk -ro -alldirs 192.168.64.2
# Note this represents the IP which will be able to access the NFS hosted at 192.168.64.1
# to know the IP of your qemu machine, you have to run ifconfig on it and add it here
````

#### Enable nfsd on M1

````bash
nfsd start
# note any changes to nfsd exports file will require you to execute following command
# nfsd update

# more information about nfsd in man page
````

#### Checking nfsd is working correctly

````bash
# from the host (M1), by default it looks at localhost
showmount -e
# another way is use finder and type : <Ctrl>-k
# and type in this url : nfs://192.168.64.1:/System/Volumes/Data/Users/smk/personal

# from the client (FreeBSD)
showmount -e 192.168.64.1
# if this doesn't work then mostly IP is not whitelisted in exports file
````

### 3. Post Setup

1. Mounting Local FreeBSD folder inside the QEMU-VM
2. Build World and Build Kernel (Probably will need it :)

#### Mounting Local FreeBSD src folder inside the QEMU-VM

````bash
mount -v -t nfs 192.168.64.1:/System/Volumes/Data/Users/smk/personal/gsoc/fbsd /usr/src

# to unmount it 
umount -a -t nfs,nullfs

# a more correct way to automatically mount this would be to either write this in fstab file or maybe a one line bash script
````

#### Build World and Build Kernel (Probably will need it :)

````bash
make -j `sysctl -n hw.ncpu` -DWITHOUT_SYSTEM_COMPILER buildworld buildkernel

# look at ntfy build notification :) cause it takes around 1:40hrs to execute both command on M1(MBP13) with above specs on VM
````

For any issues you can mail me at : smk@FreeBSD.org