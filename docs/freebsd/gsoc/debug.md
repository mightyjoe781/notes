# Debug Notes

## notes on script design



## nfs attach script

````bash
# notes - follow freebsd-m1 setup page
echo "mount -v -t nfs 192.168.64.1:/System/Volumes/Data/Users/smk/personal/gsoc/fbsd/tools/boot/bootloader_test /root/freebsd-src/tools/boot/bootloader_test" >> mount.sh
chmod +x mount.sh
# later configure to execute on bootup
````

- There is an issue when mounting entire freebsd-src from Mac. Seems like its attaching in a read-only mode which interferes with `buildworld`, `buildkernel` steps
- There is another issue while running `amd64` builds from `arm64` qemu running requires to build toolchain

````bash
# building toolchain
cd freebsd-src
# assumes buildworld and buildkernel is done
make -j `sysctl -n hw.ncpu` TARGET=amd64 TARGET_ARCH=amd64 toolchain
# optionally could use : toolchains to build everything
````



## notes on amd64

- really already been solved by warner

## notes on arm64

- Check nfs attach script section’s 2nd portion

## notes on riscv

default boot mode for my script is using opensbi

````bash
# install opensbi & optionally u-boot
pkg install opensbi u-boot-qemu-riscv64
````

## notes on armv7

This image is always released as IMG file, which could be tricky to handle in bootloader_tests script which is a lua script.

- Decided to convert `.img` into `.iso`

How do we get all the files ?

````bash
# uncompress the xz
xz -k FreeBSD-13.2-RELEASE-arm-armv7-GENERICSD.img.xz

# then create a virtual device with this uncompressed image
mdconfig -a -t vnode -f ~/cache/FreeBSD-13.2-RELEASE-arm-armv7-GENERICSD.img -u 0
# this should mount the virtual device as md0 & confirm it as
mdconfig -l
ls /dev/md0*		# output should be md0, md0s1, md0s2, md0s2a

# lets find out file-system of each of them
file FreeBSD-13.2-RELEASE-arm-armv7-GENERICSD.img
fstyp /dev/md0s2a			# this should be required ufs partition

# mounting
mount -t ufs /dev/md0s2a /mnt/armv7

# cleanup: unmount & delete virtual device
unmount /mnt/armv7
mdconfig -d -u 0

# reference
# discord discussions & https://gist.github.com/yzgyyang/4965d5673b5c79c644a695dd75fa8e05
# https://www.freebsddiary.org/iso-mount.php
# https://www.cs.ait.ac.th/~on/technotes/archives/2013/12/11/mount_a_file_system_image_in_freebsd/index.html
````

Creating ISO

````bash
# install cdutils
pkg install sysutils/cdrtools

# in qemu cd-writer needs to configured so rather let's write the folder into iso
mkisofs -o FreeBSD-13.2-RELEASE-arm-armv7-GENERICSD.iso /dev/md0s2a

# if not in qemu
cdrecord dev=md0 imagefile.iso

# reference : https://docs.freebsd.org/en/books/handbook/disks/#creating-cds
````

## notes on powerpc64

## notes on CI process

## notes on parallelisation of tests

## notes on python port
