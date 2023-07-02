## Week 3

Timeline : 12 Jun

### Setup ntfy

`ntfy` is very useful notification application and its open-source. Using ntfy you can send notification via any push notification services like pushover.

- Purchase one-time pushover service at 5$.
- Setup ntfy.

````bash
sudo pkg install ntfy
````

I used my old `ntfy.yml` by sending it to server directly from my server. (Assuming that server has been setup properly locally in `conf` file.)

```bash
scp prismo:~/.config/ntfy/ntfy.yml gsoc:~/.config/ntfy/ntfy.yml
```

### Build FreeBSD Source Tree

Useful Resources : 

- https://klarasystems.com/articles/freebsd-developer-workstation-setup/

````bash
# Install my source tree
git clone git@github.com:mightyjoe781/freebsd-src.git --branch bootloader-smk fbsd-smk
cd fbsd-smk

# maybe you will need sudo for this
chown smk:smk /usr/src /usr/obj

# assuming ntfy is setup correctly lets build tree with env
ntfy done make -j `sysctl -n hw.ncpu` -DWITHOUT_SYSTEM_COMPILER buildworld buildkernel


# Warner wanted one kernel for arm64 for override
mkdir -p $HOME/stand-test-root/override/arm64-aarch64
sudo -E make installkernel DESTDIR=$HOME/stand-test-root/override/arm64-aarch64 TARGET=arm64
````

### Setup Development Workflow

- Following tooling seems to work fine for me these days. Its adapted from my own server to work in freebsd servers.

````bash
# my setup works for only bash for now
# first get my dotfiles
git clone https://github.com/mightyjoe781/.dotfiles

# install required tools
sudo pkg install stow tmux vim neovim

# go in .dotfiles
cd .dotfiles
# i think i changed this so i don't need this but doesn't hurt to copy
cp ~/.dotfiles/bash/.bashrc ~

# ignore pushd and popd errors in FreeBSD
chmod +x install
./install

# this should stow most of required stuff
# .bashrc.d way of setting up things i learned from ghoti :P
cp -r ~/.dotfiles/bash/.bashrc.d ~
cp ~/.dotfiles/vim/.vimrc ~

# Open vim and execute :PlugInstall
# need to work on making tmux working panels
````

### build.lua module progress

- There are two ways build.lua works atm, depending on linuxboot flag (wait did I ever decide how to enable it oops)
  - LinuxBoot
  - FreeBSD Boot
- This week FreeBSD Boot should be in atleast complete shape to keep up with timelines, Next week could take up configuring `test.lua` for running those FreeBSD trees using `qemu`
- Later that I can work on bringing the Linux Kernel Boot working (wait that reminds me of extra custom kernel warner hosted)
- 
- 

### ToDo

- This setup seems to have the VSCode Remote Extension working, but i do not wish to destroy my current jail following some random gist :P. but that is what jail is for (another smk shouts from corner lol) 
  https://gist.github.com/mateuszkwiatkowski/ce486d692b4cb18afc2c8c68dcfe8602
- Let’s try to focus on testing via qemu and completing the build script for this week.

