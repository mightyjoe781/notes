# Unix Notes - Part 1
Generated on: 2025-06-01 14:34:33
Topic: unix
This is part 1 of 1 parts

---

## File: unix/ansible.md

# Ansible

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

Automate IT infrastructure with ease

### Introduction

Ansible is an **automation tool** that helps you manage servers, deploy applications, and configure systems. It uses **YAML** for its playbooks, making it easy to read and write.

Key Features:

- **Agentless**: No software needed on managed nodes.
- **Idempotent**: Running the same playbook multiple times won’t break things.
- **Declarative**: You describe the desired state, and Ansible figures out how to get there.

### Installation

Install Ansible on your control machine

````bash
sudo apt update  
sudo apt install ansible  

# verify 
ansible --version
````

### Key Concepts

1. **Inventory**: A file that lists the servers (nodes) you want to manage.

   ````ini
   [webservers]  
   web1.example.com  
   web2.example.com  
   
   [dbservers]  
   db1.example.com  
   ````

2. **Playbooks**: YAML files that define tasks to be executed.

   ````yaml
   - hosts: webservers  
     tasks:  
       - name: Ensure Apache is installed  
         apt:  
           name: apache2  
           state: present  
   ````

3. **Modules**: Pre-built functions (e.g., `apt`, `copy`, `service`) to perform tasks.

4. **Ad-Hoc Commands**: One-liners for quick tasks.

````bash
ansible webservers -m ping
````

### Getting Started

* Create an Inventory File: Save this as `inventory.ini`

````ini
[webservers]
192.168.1.10
192.168.1.11

[dbservers]  
192.168.1.20
````

* Test Connectivity

````bash
ansible all -i inventory.ini -m ping
````

* Write Your First Playbook: Save as `webserver.yml`

````bash
- hosts: webservers  
  become: yes  # Run tasks as root  
  tasks:  
    - name: Install Apache  
      apt:  
        name: apache2  
        state: present  

    - name: Start Apache service  
      service:  
        name: apache2  
        state: started  
        enabled: yes  
````

* Run the Playbook

````bash
ansible-playbook -i inventory.ini webserver.yml
````

### Common Use Cases

#### Copy Files

````yaml
- name: Copy index.html  
  copy:  
    src: files/index.html  
    dest: /var/www/html/index.html  
````

#### Create Users

````yaml
- name: Add user 'deploy'  
  user:  
    name: deploy  
    shell: /bin/bash  
    groups: sudo  
    append: yes  
````

#### Install Packages

````yaml
- name: Install required packages  
  apt:  
    name:  
      - git  
      - curl  
      - unzip  
    state: present  
````

#### Restart Services

````yaml
- name: Restart Nginx  
  service:  
    name: nginx  
    state: restarted  
````

### Best Practices

#### 1. Organize Playbooks

* Use **roles** to group related tasks (e.g., `webserver`, `database`).
* Example structure:

````yaml
playbooks/  
├── inventory.ini  
├── webserver.yml  
└── roles/  
    └── webserver/  
        ├── tasks/  
        │   └── main.yml  
        ├── handlers/  
        │   └── main.yml  
        └── templates/  
            └── index.html.j2  
````

#### 2. Use Variables

* Define variables in `group_vars` or `host_vars`

````yaml
# group_vars/webservers.yml  
http_port: 80  
````

#### 3. Idemptotency

* Always check if a task idempotent. For Example

````yaml
- name: Ensure directory exists  
  file:  
    path: /var/www/html  
    state: directory  
````

#### 4. Error Handling

````yaml
- block:  
    - name: Try risky task  
      command: /bin/false  
  rescue:  
    - name: Handle failure  
      debug:  
        msg: "Task failed, but we're recovering!"  
````

### Troubleshooting

| Issue                   | Solution                                                 |
| ----------------------- | -------------------------------------------------------- |
| "SSH connection failed" | Check SSH keys and `ansible_user` in inventory.          |
| "Permission denied"     | Use `become: yes` to run tasks as root.                  |
| "Module not found"      | Ensure the module is installed (e.g., `apt` for Debian). |
|                         |                                                          |

### Pro Tips

* Dry Run: Test Playbooks without making changes

````bash
ansible-playbook --check webserver.yml  
````

* Tagging Tasks: Run specific tasks using tags

````yaml
- name: Install Apache  
  apt:  
    name: apache2  
    state: present  
  tags: install  
````

````bash
ansible-playbook webserver.yml --tags "install"  
````

* Use Vault for Secrets: Encrypt sensitive data

````bash
ansible-vault create secrets.yml  
````

### See Also

* [Ansible Documentation](https://docs.ansible.com/)
* [Ansible Galaxy](https://galaxy.ansible.com/) (pre-built roles)


---

## File: unix/cheat.md

# cheat.sh

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

Instant answers for commands, programming, and more

### What is cheat.sh ?

`cheat.sh` is a command-line cheat sheet that provides quick answers for

* Linux Commands (e.g. `tar`, `grep`, `awk`)
* Programming Languages (e.g. `Python`, `JavaScript`, `Go`)
* Tools (e.g. `Git`, `Docker`, `Kubernetes`)

It is accessible via `curl` or a browser, making it a go-to resource for quick help.

### Installation

No installation needed! Use `curl` to access it

````bash
curl cheat.sh
````

For a better experience, install the `cht.sh` wrapper

````bash
curl https://cht.sh/:cht.sh > ~/bin/cht.sh
chmod +x ~/bin/cht.sh
````

### Basic Usage

#### 1. Query a Command

````bash
curl cheat.sh/tar

# or to find a word
curl cheat.sh/tar | grep -C 3 "contents"
````

#### 2. Search for a Topic

````bash
curl cheat.sh/python/list+comprehension
````

3. #### Use the wrapper

With `cht.sh`, queries are simpler

````bash
cht.sh tar
cht.sh python list comprehension
````

### Examples

| Query Type         | Command                      | Output Description             |
| ------------------ | ---------------------------- | ------------------------------ |
| **Linux Commands** | `curl cheat.sh/grep`         | Examples of `grep` usage       |
| **Programming**    | `curl cheat.sh/python/split` | Python `str.split()` examples  |
| **Tools**          | `curl cheat.sh/git`          | Common Git commands            |
| **Error Messages** | `curl cheat.sh/curl+error+7` | Explanation for `curl error 7` |

#### Advanced Features

* Inline Queries: Use `:` to query directly in the terminal

````bash
cht.sh :help
cht.sh :list
````

* Multiple Queries: Combine Topics for detailed answers

```bash
cht.sh python+json+load
```

* Local Caching: Enable caching for faster responses

````bash
export CHEATSH_CACHE=~/.cheat.sh
mkdir -p $CHEATSH_CACHE
````

* Syntax Highlighting: Use `bat` or `pygmentize` for colored output

````bash
curl cheat.sh/python/functions | bat
````

### Integration with Editors

* Vim Integration

````bash
:nmap \c :!curl cheat.sh/<cword><CR>  
````

* VS Code: Install the `cheat.sh` plugin for quick access.

### Tmux Based cht.sh

````bash
#!/usr/bin/env bash

# put your languages, and chat commands in following files
selected=`cat ~/.tmux-cht-languages ~/.tmux-cht-command | fzf`
if [[ -z $selected ]]; then
    exit 0
fi

read -p "Enter Query: " query

if grep -qs "$selected" ~/.tmux-cht-languages; then
    query=`echo $query | tr ' ' '+'`
    tmux neww bash -c "echo \"curl cht.sh/$selected/$query/\" & curl cht.sh/$selected/$query & while [ : ]; do sleep 1; done"
else
    tmux neww bash -c "curl -s cht.sh/$selected~$query | less"
fi
````



---

## File: unix/compression.md

# tar/gzip/zstd

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

## tar (tape archive)

used to bundle files into a single archive

### Basic Usage

#### 1. Create and Archive

````bash
tar -cvf archive.tar file1 file2
````

* `-c`: create archive
* `-v`: verbose output
* `-f`: specify archive filename

#### 2. Extract an Archive

````bash
tar -xvf archive.tar
````

* `-x`: Extract files
* files are extracted into current directory by default

#### 3. List Archive Contents

````bash
tar -tvf archive.tar
````

### Common Scenarios

1. Extract to a Specific Directory

   ````bash
   tar -xvf archive.tar -C /path/to/dir
   ````

2. Create and archive from a Directory

   ````bash
   tar -cvf archive.tar /path/to/dir
   ````

3. Exclude file

   ````bash
   tar -cvf archive.tar --exclude="*.log" /path/to/dir
   ````

4. Extracting only `txt` files

   ````bash
   tar -xvf archive.tar --wildcards "*.txt"
   ````

5. Combine with `find` archive specific files

   ````bash
   find . -name "*.txt" | tar -cvf archive.tar -T -
   ````

## gzip

Compress files using `.gz` format

### Basic Usage

#### 1. Compress a file

````bash
gzip file.txt
````

#### 2. Decompress a file

````bash
gzip -d file.txt.gz
````

#### 3. Compress and Archive

````bash
tar -czvf archive.tar.gz file1 file2
````

#### 4. Extract `.tar.gz`

````bash
tar -xzvf archive.tar.gz
````

#### 5. View Compressed files without extraction

````bash
zcat file.txt.gz
````

* Use `gunzip` as an alias for `gzip -d`

## Zstd (Z Standard)

A modern compression tool with better speed and ratios

### Basic Usage

#### 1. Compress a File

````bash
zstd file.txt
````

#### 2. Decompress a File

````bash
zstd -d file.txt.zst
````

#### 3. Compress and Archive

````bash
tar -cvf archive.tar.zst --zstd file1 file2
````

#### 4. Extract `.tar.zst`

````bash
tar -xvf archive.tar.zst --zstd
````

You can adjust compression level : `zstd -19 file.txt`

Use `unzstd` as alias for `zstd -d`

### Comparison between gzip and zstd

| Tool   | Speed  | Compression Ratio | Common Use Cases           |
| ------ | ------ | ----------------- | -------------------------- |
| `gzip` | Medium | Good              | General-purpose            |
| `zstd` | Fast   | Excellent         | Modern systems, large data |

#### Notes

* take a look at `pigz` (parallel implementation of gzip)

---

## File: unix/cron.md

# cron

allows users to schedule the execution.

### Installation

````bash
sudo apt update && sudo apt install cron
sudo systemctl enable cron
````

Cron is mostly installed in all the systems and consists of two things

* `cron` or `crond` : daemon
* `crontab` : command interface for interacting with daemon

### Cron Syntax

````bash
*    *    *    *    *   /home/user/bin/somecommand.sh
|    |    |    |    |            |
|    |    |    |    |    Command or Script to execute
|    |    |    |    |
|    |    |    | Day of week(0-6 | Sun-Sat)
|    |    |    |
|    |    |  Month(1-12)
|    |    |
|    |  Day of Month(1-31)
|    |
|   Hour(0-23)
|
Min(0-59)
````

`*`: matches all values, so above script runs every minute

### Usage

* add crontab entry

````bash
crontab -e
````

NOTE: crontab entries do not source `~/.bashrc` so always use full script path and environment variable. Either hardcode or source in the executing script

NOTE: Make sure your script is executible

* cron logs

  ````bash
  tail -f /var/log/cron
  ````

  

### Example crons entries

* Use https://crontab.guru to validate your cron

If you want to run four times a day between Monday and Friday, you can use the *step operator* ( **/** ) and the *range operator* ( **-** ).

````bash
0 */6 * * Mon-Fri /home/user/somejob.sh
````

#### **Run Every Hour at Minute 15**

```
15 * * * * /path/to/script.sh 
```

#### **Run Every Day at 2 AM**

````bash
0 2 * * * /path/to/script.sh
````

#### **Run Every Sunday at 3 PM**

````bash
0 15 * * 0 /path/to/script.sh
````

#### **Run Every Month on the 1st at 4 AM**

````bash
0 4 1 * * /path/to/script.sh
````

### Advanced Features

#### Environment Variable

````bash
SHELL=/bin/bash  
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
* * * * * /path/to/script.sh
* * * * * /path/to/script.sh >> /var/log/script.log 2>&1
````

#### Special Strings

Use predefined schedules:

- `@reboot`: Run at startup.
- `@daily`: Run once a day.
- `@weekly`: Run once a week.
- `@monthly`: Run once a month.
- `@yearly`: Run once a year.

````bash
@daily /path/to/script.sh
````

### Pro Tips

**Use `cron.d` for System Jobs**: Place system-wide cron jobs in `/etc/cron.d/`

---

## File: unix/curl.md

# cURL/Wget

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

### Installation

````bash
apt update
apt install curl wget
````

## cURL

### Basic Commands

#### Download a file

````bash
curl -O https://example.com/file.txt
````

#### Send a GET Request

````bash
curl https://example.com/api
````

#### Send a POST Request

````bash
curl -X POST -d "param1=value1" https://example.com/api
````

#### Follow Redirects

````bash
curl -L https://example.com
````

#### Include Custom Headers

````bash
curl -H "Authorization: Bearer token" https://example.com/api
````

#### Save output to a File

````bash
curl -o output.txt https://example.com/file.txt
````

#### Upload a File

```bash
curl -F "file=@localfile.txt" https://example.com/upload
```

#### Use a Proxy for connection

````bash
curl -x http://proxy.example.com:8080 https://example.com
````

#### Use `curljson` alias

````bash
alias curljson='curl -H "Content-Type: application/json"'
curljson https://example.com
````

## Wget

### Basic Commands

#### Download a File

````bash
wget https://example.com/file.txt
````

#### Download in Background

````bash
wget -b https://example.com/file.txt
````

#### Resume a Download

````bash
wget -c https://example.com/file.txt 
````

#### Download Recursively

````bash
wget -r https://example.com
````

#### Limit Download Speed

````bash
wget --limit-rate=100k https://example.com/file.txt
````

#### Download with Auth

````bash
wget --user=username --password=password https://example.com/file.txt
````

#### Mirror a website

````bash
wget -mk https://example.com
````



---

## File: unix/docker.md

# Docker

 [:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guides](../docker/index.md)

### Installation

````bash
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
````

````bash
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
````

````bash
sudo apt install docker-ce docker-ce-cli containerd.io
````

````bash
# managing docker as non root user
$USER=smk
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker # refresh group

# test docker run hello-world
# NOTE : fix .docker dir due to previous root runs if you get config errors
sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "$HOME/.docker" -R
````

### Essential Commands

| Category       | Command                          | Description                 |
| -------------- | -------------------------------- | --------------------------- |
| **Containers** | `docker run -d -p 80:80 ngnix`   | Run Container in background |
|                | `docker stop <container>`        | Stop container              |
|                | `docker logs -f <container>`     | Follow logs                 |
| **Images**     | `docker build -t myapp:latest .` | Build from Dockerfile       |
|                | `docker pull ubuntu:22.04`       | Download image              |
|                | `docker image prune`             | Remove unused images        |
| **System**     | `docker ps -a`                   | List all containers         |
|                | `docker system df`               | Show disk usage             |
|                | `docker exec -it <id> bash`      | Enter running container     |

### Docker Compose Setup

Sample `docker-compose.yml`

````yaml
version: '3.8'  
services:  
  web:  
    image: nginx:alpine  
    ports:  
      - "80:80"  
    volumes:  
      - ./html:/usr/share/nginx/html  
  db:  
    image: postgres:15  
    environment:  
      POSTGRES_PASSWORD: example  
````

Run with:

````bash
docker compose up -d
````

#### Cleanup

````bash
docker system prune -a --volumes  # Remove all unused data  
````

#### Debugging

```bash
docker inspect <container>  # Show detailed config  
```

#### Security

````bash
docker scan nginx:alpine  # Vulnerability check
````

### Security Best Practices

* Avoid using `--privileged` flag
* Use non-root users in containers

````dockerfile
FROM alpine
RUN adduser -D appuser && chown appuser /app
USER appuser
````



* Limit Resources

````bash
docker run --memory=512m --cpus=1.5 myapp
````

### Resources

* [Docker Documentation](https://docs.docker.com/)
* [Best Practices Guide](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
* [Personal Notes](../docker/index.md)

### Installing Portainer


---

## File: unix/fail2ban.md

# fail2ban

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

### Installation

````bash
sudo apt update
sudo apt install fail2ban
````

````bash
# check fail2ban service
systemctl status fail2ban.service
````

### Setup

* Create a local configuration : `jail.local`

````bash
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
````

* Edit Configuration file `/etc/fail2ban/jail.local`

````ini
[DEFAULT]  
ignoreip = 127.0.0.1/8 192.168.1.0/24  
bantime = 600  
findtime = 600  
maxretry = 3 
````

* Enable Jails

````ini
[sshd]  
enabled = true  
````

````bash
systemctl enable fail2ban
````

### Commands

* Check Status

  ````bash
  fail2ban-client status
  ````

* Unban an IP

  ````bash
  fail2ban-client set sshd unbanip 192.168.1.100
  ````

* Ban an IP Manually

  ````bash
  fail2ban-client set sshd banip 192.168.1.100  
  ````

* Reload Configuration

  ````bash
  fail2ban-client reload
  ````

### Advanced Use-Cases

* Create a custom filter in `/etc/fail2ban/filter.d/`

  ````ini
  [custom-filter]  
  enabled = true  
  filter = custom-filter  
  action = iptables[name=Custom, port=http, protocol=tcp]  
  logpath = /var/log/custom.log  
  maxretry = 3  
  bantime = 600
  ````

* Email Notifications: Configure mail alerts in `jail.local`

  ````ini
  [DEFAULT]  
  destemail = admin@example.com  
  sender = fail2ban@example.com  
  action = %(action_mwl)s 
  ````

### Example Configurations

#### Securing MailCow Mailserver

Create a new filter : ` /etc/fail2ban/filter.d/mailcow.conf`

````ini
[Definition] 
failregex = LOGIN authenticator failed for .+ \[<HOST>\]:.* 
            NOQUEUE: reject: RCPT from \[<HOST>\].* Auth failure: 535 

````

Add `[mailcow]` jail in `/etc/fail2ban/jail.conf`

````ini
[mailcow] 
enabled = true 
port = smtp, submission, imap, imaps, pop3, pop3s 
filter = mailcow 
logpath = /opt/mailcow-dockerized/mailcow.conf 
maxretry = 3 
bantime = 3600
````

#### Securing Nextcloud with Fail2Ban

Create a new filter : ` /etc/fail2ban/filter.d/nextcloud.conf`

````ini
[Definition] 
failregex = Login failed.*REMOTE_ADDR=<HOST>
````

Add `[nextcloud]` jail in `/etc/fail2ban/jail.conf`

````ini
[nextcloud] 
enabled = true 
port = http, https 
filter = nextcloud 
logpath = /path/to/nextcloud.log 
maxretry = 3 
bantime = 3600
````

#### 

---

## File: unix/fzf.md

# fzf

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

A command-line fuzzy finder for filtering and selecting files, commands, and more.

### Installation

````bash
sudo apt install fzf  # Debian/Ubuntu
brew install fzf      # macOS
````

### Basic Usage

* Basic Files

````bash
fzf
````

* Search Command History

```bash
history | fzf
```

* Search and open files

````bash
vim $(fzf)
````

### Advanced Features

#### Preview Files

````bash
fzf --preview 'cat {}'
````

#### Multi-Select

````bash
fzf --multi
````

#### Integration with `cd`

````bash
cd $(find . -type d | fzf)
````

#### Other

* Use `Ctrl+T` to insert selected files into the command line
* Bind `fzf` to `Ctrl+R` for interactive history search

#### Example ZSH Functions

````bash
#!/usr/local/env zsh

# Open file
# fe [FUZZY PATTERN] - Open the selected file with the default editor
#   - Bypass fuzzy finder if there's only one match (--select-1)
#   - Exit if there's no match (--exit-0)
function fe {
  local files
  IFS=$'\n' files=($(fzf --query="$1" --multi --select-1 --exit-0))
  [[ -n "$files" ]] && ${EDITOR:-vim} "${files[@]}"
}

# fcd - cd to selected directory
function fcd {
  local dir
  dir=$(fd . "${1:-.}" --type=d | fzf --no-multi --layout=reverse --height=40%) &&
  cd "$dir"
}

# fcda - including hidden directories
function fcda {
  local dir
  dir=$(fd . "${1:-.}" --hidden --type=d | fzf --no-multi --layout=reverse --height=40%) &&
  cd "$dir"
}

# cdf - cd into the directory of the selected file
function cdf {
  local file
  local dir
  file=$(fzf --query "$1" --no-multi --layout=reverse --height=40%) && dir=$(dirname "$file") && cd "$dir"
}


# Tmux
function fta {
  local session
  session=$(tmux list-sessions -F "#{session_name}" | \
    fzf --layout=reverse --height=20% --query="$1" --select-1 --exit-0) &&
  tmux -CC attach -d -t "$session"
}
````

### Resources

* https://thevaluable.dev/practical-guide-fzf-example/


---

## File: unix/git.md

# Git

 [:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guide](../git/index.md)

### Installation

Install Git:

````bash
apt-get install git
````

### Configuration

Edit: `~/.gitconfig`

````ini
[user]  
    name = smk  
    email = smk@minetest.in  
[alias]  
    st = status -sb  
    lg = log --graph --abbrev-commit --decorate  
[core]  
    editor = vim  
````

### Common Workflows

Clone a repository

````bash
git clone https://github.com/user/repo.git
````

Create and push branch

````bash
git checkout -b feature  
git add .  
git commit -m "Add feature"  
git push -u origin feature  
````

### Pro Tips

1. **Rebase**: Squash commits with `git rebase -i HEAD~3`.
2. **Stash**: Temporarily save changes with `git stash`.
3. **Reflog**: Recover lost commits via `git reflog`.

### See Also

* [giteveryday(7)](https://man.freebsd.org/cgi/man.cgi?query=giteveryday)

---

## File: unix/gnu.md

# GNU Coreutils

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

Master file/text manipulation and system basics.

### Installation

Preinstalled on most Linux systems. Verify/update:

````bash
sudo apt update && sudo apt install coreutils
````

### Essential Commands

| Category | Command                     | Description                   |
| -------- | --------------------------- | ----------------------------- |
| File Ops | `cp -a`                     | archive-preserving copy       |
|          | `mv -i`                     | interactive rename (prompt)   |
|          | `rm -I`                     | Safe bulk delete (1 prompt)   |
| Text     | `grep -C 3 'text'`          | show 3 lines around match     |
|          | `sed -i 's/old/new/g' file` | in-place replace              |
|          | `awk '{print $1}'`          | print first column            |
| System   | `df -h`                     | Human-readable disk space     |
|          | `du -sh *`                  | directory sizes summary       |
| Search   | `find . -mtime -7`          | files modified in last 7 days |
|          | `locate -i pattern`         | case-insensitive file search  |
|          |                             |                               |

### Advanced Usage

* Bulk rename with `xargs` and `sed`:

````bash
ls *.txt | xargs -I {} sh -c 'mv {} $(echo {} | sed "s/.txt/.md/")'
````

* parallel processing with `parallel`

````bash
find . -name "*.log" | parallel -j 4 gzip
````

* Compare Directories

````bash
diff -qr dir1/ dir2/
````

### Configuration

Customize `ls` color `~/.bashrc`

````bash
export LS_COLORS="di=1;36:ln=35:*.zip=32"
alias ls="ls --color=auto"
````

Safe defaults `~/.bash_aliases`

````bash
alias cp="cp -i --preserve=all"  
alias rm="rm -I"  
````

#### Pro Tips

* **Dry Run** for destructive operations

````bash
rm -Iv *  # Interactive verbose
cp -anv src/ dest/  # No-clobber dry-run
````

* Timing command Executions

```bash
time grep -r "pattern" /large_dir  
```

* Split large files

````bash
split -b 100M bigfile.zip "bigfile_part_"  
````

### Troubleshooting

| Issues                     | Solution                                   |
| -------------------------- | ------------------------------------------ |
| "Permission denied"        | Use `sudo` or `chmod/chown`                |
| "Argument list too long"   | Use `xargs`: `find ... | xargs rm`         |
| Special chars in filenames | Use quotes or escape: `rm 'file$name.txt'` |
|                            |                                            |

#### See also

* `man coreutils`
* `info coreutils`
* [Coreutils Manual](https://www.gnu.org/software/coreutils/manual/)

---

## File: unix/index.md

---
hide:
  - navigation
  - toc
---
# Unix Tools

:octicons-arrow-left-24:{ .icon } [Back](../toc.md)

<div class="grid cards" markdown>

- __Terminal & Shell Tools__

  ---

  :simple-fishshell:{ .lg .middle } [Bash/Zsh/Fish](shell.md)
  
  :simple-git:{ .lg .middle } [Git](git.md)
  
  :material-ssh:{ .lg .middle } [SSH](ssh.md)
  
  :simple-tmux:{ .lg .middle } [Tmux](tmux.md)
  
  :simple-neovim:{ .lg .middle } [Vim](../vim/index.md)
  
  :simple-gnu:{ .lg .middle } [GNU Coreutils](gnu.md)
  
- __System & Monitoring__

    ---
    
    :fontawesome-solid-terminal:{ .lg .middle } [Systemd](systemd.md)

    :material-recycle-variant:{ .lg .middle } [Cron](cron.md)

    :simple-htop:{ .lg .middle } [Htop/Glances/Btop]

    :octicons-log-16:{ .lg .middle } [Logrotate]

    :material-sync:{ .lg .middle } [rsync](rsync.md)
  
- __Networking & Security__

    ---
    
    :simple-nginx:{ .lg .middle } [Nginx](nginx.md)

    :material-router:{ .lg .middle } [UFW](ufw.md)

    :octicons-terminal-16:{ .lg .middle } [Curl/Wget](curl.md)

    :simple-openssl:{ .lg .middle } [OpenSSL](openssl.md)

    :material-hammer:{ .lg .middle } [Fail2ban](fail2ban.md)
  
- __Development & DevOps__

  ---
  
  :simple-docker:{ .lg .middle } [Docker/Podman](docker.md)
  
  :simple-kubernetes:{ .lg .middle } [Kubernetes](kubernetes.md)
  
  :simple-terraform:{ .lg .middle } [Terraform](terraform.md)
  
  :simple-ansible:{ .lg .middle } [Ansible](ansible.md)
  
- __Productivity__

    ---
    
    :fontawesome-regular-face-dizzy:{ .lg .middle } [fzf](fzf.md)

    :octicons-terminal-16:{ .lg .middle } [ripgrep(rg)](ripgrep.md)

    :material-zip-box:{ .lg .middle } [tar/gzip/zstd](compression.md)

    :simple-cmake:{ .lg .middle } [Taskfile/Makefile](makefile.md)

    :material-information:{ .lg .middle } [tldr](tldr.md)

    :octicons-terminal-16:{ .lg .middle } [cheat.sh](cheat.md)

- __Databases__

    ---
    
    :simple-postgresql:{ .lg .middle } [PostgreSQL](postgresql.md)

    :simple-redis:{ .lg .middle } [Redis](redis.md)

    :simple-sqlite:{ .lg .middle } [sqlite](sqlite.md)

- __Miscellaneous__

    ---
    
    :material-file-document:{ .lg .middle } [Pandoc]

    :material-image:{ .lg .middle } [ImageMagick]

    :simple-ffmpeg:{ .lg .middle } [FFmpeg]

    :material-git:{ .lg .middle } [lazygit]
    
    

</div>


---

## File: unix/kubernetes.md

# Kubernetes

[:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guides](../kubernetes/index.md)

### Installation

Install `kubectl` and `minikube` for local testing

````bash
# kubectl  
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"  
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl  

# minikube  
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64  
sudo install minikube-linux-amd64 /usr/local/bin/minikube  
minikube start --driver=docker  
````

### Essential Commands

| Category        | Command                                    | Description           |
| --------------- | ------------------------------------------ | --------------------- |
| **Pods**        | `kubectl get pods -A`                      | List all pods         |
|                 | `kubectl describe pod <name>`              | Inspect pod details   |
| **Deployments** | `kubectl rollout status deploy/<name>`     | Check deployment      |
|                 | `kubectl scale deploy/<name> --replicas=3` | Scale replicas        |
| **Services**    | `kubectl expose deploy/<name> --port=80`   | Create service        |
| **Debugging**   | `kubectl logs <pod> -f`                    | Stream logs           |
|                 | `kubectl exec -it <pod> -- sh`             | Enter container shell |
|                 |                                            |                       |

Sample Deployment (`deploy.yml`)

````yaml
apiVersion: apps/v1  
kind: Deployment  
metadata:  
  name: nginx  
spec:  
  replicas: 3  
  selector:  
    matchLabels:  
      app: nginx  
  template:  
    metadata:  
      labels:  
        app: nginx  
    spec:  
      containers:  
      - name: nginx  
        image: nginx:alpine  
        ports:  
        - containerPort: 80  
````

Apply

````bash
kubectl apply -f deploy.yml
````

### Tips

* Context Switching

````bash
kubectl config use-context <cluster-name>
````

* port forwarding

````bash
kubectl port-forward svc/nginx 8080:80
````

* resources limits

````bash
resources:  
  limits:  
    memory: "512Mi"  
    cpu: "1"  
````

#### Security Best Practices

* Use `Role-Based Access Control(RBAC)`
* Enable `Netowrk Policies`
* Scan images with `Trivy`

````bash
trivy image nginx:alpine
````

### Resources

* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
* [Minikube Docs](https://minikube.sigs.k8s.io/docs/)
* [Personal Notes](../kubernetes/index.md)

---

## File: unix/makefile.md

# Makefile/Taskfile

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

Task automation tools

### Taskfile

A modern, YAML-based task runner designed to simplify Tasks

1. Create a Taskfile

   ````yaml
   version: '3'
   tasks:
     build:
       cmds:
         - echo "Building..."
   ````

2. Run a Task

   ````bash
   task build
   ````

#### Taskfile Syntax

````yaml
version: '3'  # Taskfile version  

tasks:  
  <task-name>:  
    desc: "Description of the task"  
    cmds:  
      - <command-1>  
      - <command-2>  
    deps:  
      - <dependent-task>  
    vars:  
      <var-name>: <value>  
````

#### Example Taskfile

````yaml
version: '3'  

tasks:  
  greet:  
    desc: "Greet the user"  
    vars:  
      NAME: "World"  
    cmds:  
      - echo "Hello, {{.NAME}}!"  
  clean:  
    desc: "Clean build artifacts"  
    cmds:  
      - echo "Cleaning..."  
  build:  
    desc: "Build the project"  
    deps: [clean]  
    cmds:  
      - echo "Building..."  
````

#### Taskfile Example Go

```yaml
version: '3'  

tasks:  
  fmt:  
    desc: "Format Go code"  
    cmds:  
      - go fmt ./...  
  vet:  
    desc: "Vet Go code"  
    cmds:  
      - go vet ./...  
  build:
    desc: "Build the project"  
    deps: [fmt, vet]
    env:  
      GO_VERSION: "1.20"
    cmds:  
      - go build -o bin/app . 
```

#### Including Other Taskfiles

````yaml
version: '3'  

includes:  
  dev: ./tasks/dev.yml  
  prod: ./tasks/prod.yml  
````

### Makefile

1. Create a Makefile

   ````makefile
   build:
   		echo "Building..."
   ````

2. Run a Make Target

   ````bash
   make build
   ````

#### Makefile Syntax

````makefile
targets: prerequisites
	command
	command
	command
````

#### Makefile Example C

````makefile
blah: blah.c	# build target only if blah.c changes
	cc blah.c -o blah
````

#### Makefile Example Go

````bash
.DEFAULT_GOAL := build

.PHONY:fmt vet build
fmt:
	go fmt ./...

vet: fmt
	go vet ./...

build: vet
	go build
````

### Resources

* [Make File Tutorial](https://makefiletutorial.com/)
* [Taskfile Documentation](https://taskfile.dev)

---

## File: unix/nginx.md

# nginx

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

### Installation

````bash
# dependencies
sudo apt install curl gnupg2 ca-certificates lsb-release debian-archive-keyring

# nginx signing key to verify installation
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null

# verify key
gpg --dry-run --quiet --no-keyring --import --import-options import-show /usr/share/keyrings/nginx-archive-keyring.gpg

# optional: add nginx stable to sources in apt repo
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
http://nginx.org/packages/debian `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list
    
# installing
sudo apt update
sudo apt install nginx
````

### Setup

Edit `/etc/nginx/nginx.conf`

````nginx
# add in http block
http {
  	# default options
  	...
    # modified options
    add_header X-Frame-Options "SAMEORIGIN";
    include /etc/nginx/sites-available/default;
    include /etc/nginx/conf.d/*.conf;
}

````

Create a `/etc/nginx/local/common.conf`

````nginx
#---------------------------------------------------------------------
# Start of "common.conf".

#---------------------------------------------------------------------
# SSL settings.

# The  "dhparam.pem" file is  created using a script  that is provided
# separately.

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_dhparam /etc/ssl/certs/dhparam.pem;
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;

#---------------------------------------------------------------------
# Strict Transport Security.

# If  you've  got a site  that needs to support  "http"  as opposed to
# "https", you'll need to set that site up differently.

    add_header Strict-Transport-Security max-age=15768000;

#---------------------------------------------------------------------
# PHP.

location ~ \.php8?$ {
    location ~ \..*/.*\.php8$ { return 404; }
    root $docdir;
    try_files $uri =404;
#   fastcgi_pass 127.0.0.1:9000;
    fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
    fastcgi_index index.php;
    fastcgi_param SCRIPT_FILENAME
    $document_root$fastcgi_script_name;
    include fastcgi_params;
}

#---------------------------------------------------------------------
# Misc. safety measures and/or tweaks.

location / {
    root $docdir;
    index index.php index.html index.htm;
}

location ~* ^.+.(jpg|jpeg|gif|css|png|js|ico|xml)$ {
    root $docdir;
    access_log off;
}

location ~ /\.ht {
    deny all;
}
# add other services like censys to stop them from scanning
if ($http_user_agent ~* (IndeedBot)) {
    return 403;
}

# if ($bad_referer) {
#     return 444;
# }

location ~ /.well-known {
    allow all;
}

# To allow POST on static pages
error_page 405 =200 $uri;

#---------------------------------------------------------------------
# End of "common.conf".
````

Create a default server blocks in 

````nginx
# Virtual Host configuration for example.com
#
# You can move that to a different file under sites-available/ and symlink that
# to sites-enabled/ to enable it.
#
server {
	listen 80;
	listen [::]:80;

	server_name example.com;

	root /var/www/example.com;
	index index.html;

	location / {
		try_files $uri $uri/ =404;
	}
}

server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;

    server_name _;

    ssl_certificate /etc/nginx/ssl/self-signed.crt;
    ssl_certificate_key /etc/nginx/ssl/self-signed.key;

    access_log /var/log/nginx/default_ssl_access.log;
    error_log /var/log/nginx/default_ssl_error.log;

    return 444;  # Drop the connection
}
````



Create `minetest.in.conf` in `/etc/nginx/conf.d/`

````nginx
# detect http[s]://www. access to server and redirect to http[s]://minetest.in
server {
    listen 80;
  	listen 443;
		# detect http[s]://www. access to server
    server_name ~^www\.minetest\.in$;

    access_log /var/log/nginx/minetest_access.log main ;
    error_log  /var/log/nginx/minetest_error.log  info ;

    ssl_certificate     /var/letse/smk/certificates/minetest.in.crt ;
    ssl_certificate_key /var/letse/smk/certificates/minetest.in.key ;
	
  	# forward to https
    return 301 $scheme://minetest.in$request_uri;
}
# handle http/https
server {
    listen 80;
    listen 443 ssl;
    server_name ~^minetest\.in$;

    access_log /var/log/nginx/minetest_access.log main ;
    error_log  /var/log/nginx/minetest_error.log  info ;

    ssl_certificate     /var/letse/smk/certificates/minetest.in.crt ;
    ssl_certificate_key /var/letse/smk/certificates/minetest.in.key ;

    location ^~ /.well-known/acme-challenge/ {
        default_type "text/plain";
        root /var/www/tmp;
        allow all;
    }

    location = /.well-known/acme-challenge/ {
        return 404;
    }

    set $docdir /var/www/minetest.in;
    include /etc/nginx/local/common.conf;
    root $docdir;
}
````

### Examples

#### Serving Static Content

````bash
server {
    location / {
        root /data/www;
    }

    location /images/ {
        root /data;
    }
}
````

#### Simple Proxy Server

````nginx
server {
    location / {
        proxy_pass http://localhost:8080/;
    }

    location ~ \.(gif|jpg|png)$ {
        root /data/images;
    }
}
````

#### Simple FastCGI Proxying

````bash
server {
    location / {
        fastcgi_pass  localhost:9000;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param QUERY_STRING    $query_string;
    }

    location ~ \.(gif|jpg|png)$ {
        root /data/images;
    }
}
````

### Resources

* https://nginx.org/en/docs/beginners_guide.html

* [Server Nginx Setup Guide 1](../server/nginx.md)
* [Server Nginx Setup Guide 2](../server/nginx2.md)

---

## File: unix/openssl.md

# OpenSSL

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

### Installation

````bash
sudo apt update
sudo apt install openssl
````

### Common Usage

#### Generate a Private Key

````bash
# RSA Key
openssl genpkey -algorithm RSA -out private.key

# EC Key
openssl ecparam -genkey -name secp384r1 -out ec.key
````

#### Generate a CSR (Certificate Signing Request)

````bash
openssl req -new -key private.key -out request.csr
````

#### Create a self-signed Certificate

````bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
````

#### Convert Certificate Formats

````bash
# PEM to DER
openssl x509 -in cert.pem -outform DER -out cert.der

# DER to PEM
openssl x509 -inform DER -in cert.der -out cert.pem
````

#### Verify a Certificate

````bash
# verify details
openssl x509 -in cert.pem -text -noout

# verify cert chain
openssl verify -CAfile ca.crt cert.pem
````

#### Encrypt and Decrypt Files

````bash
# encrypt a file
openssl enc -aes-256-cbc -salt -in file.txt -out file.enc

# decrypt a file
openssl enc -d -aes-256-cbc -in file.enc -out file.txt
````

### Advanced Usage

#### Create a PKCS#12 Bundle

````bash
# bundle cert and key
openssl pkcs12 -export -in cert.pem -inkey key.pem -out bundle.p12

# extract from pkcs#12
openssl pkcs12 -in bundle.p12 -out cert.pem -nodes
````

#### Generate DH (Diffie-Hellman) Params file

````bash
openssl dhparam -out dhparam.pem 2048
````

### Example

#### Block unwanted DNS resolution by port scanners

Issue a fake certificate with `example.com` to prevent Censys like services to resolve domain names from nginx-default redirects.

````bash
# 100 yrs self-signed valid certificate
sudo openssl req -x509 -nodes -days 36500 -newkey rsa:2048 \
  -keyout /etc/ssl/nginx/self-signed.key \
  -out /etc/ssl/nginx/self-signed.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN=example.com"
````

Edit `/etc/nginx/sites-available/default`

````nginx
## save following contents to /etc/nginx/sites-available/default
# this prevent domain name leak and default forwarding from ip
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
  
	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;
	server_name _;

	location / {
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		try_files $uri $uri/ =404;
	}
}

server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;

    server_name _;

    ssl_certificate /etc/nginx/ssl/self-signed.crt;
    ssl_certificate_key /etc/nginx/ssl/self-signed.key;

    access_log /var/log/nginx/default_ssl_access.log;
    error_log /var/log/nginx/default_ssl_error.log;

    return 444;  # Drop the connection
}
````

### Resources

* https://www.feistyduck.com/library/openssl-cookbook/

### Tips

* Automate Cert Generation : Use Scripts to automate CSR and certificate generation
* Use *Let’s Encrypt* : provides free SSL/TLS certificates
* Monitor Cert Expiry: Use tools like `certbot renew` or `cron` to automate renewal


---

## File: unix/postgresql.md

# PostgreSQL

[:octicons-arrow-left-24:{ .icon } Back](index.md)

### Installation

Debian/Ubuntu

````bash
sudo apt update
sudo apt install postgresql postgresql-contrib

# check service status
sudo systemctl status postgresql
````

macOS

````bash
brew install postgresql

# start the service
brew services start postgresql
````

### Setup

NOTE: Ideally you should not expose your database to public network.

Edit `pg_hba.conf` (usually located at `/etc/postgresql/<version>/main/pg_hba.conf`)

````bash
host    all             all             0.0.0.0/0               md5
````

Edit `postgresql.conf` to listen on all interfaces

````bash
listen_addresses = "*"
````

````bash
sudo systemctl restart postgresql
````

### Security

* Change default password

````bash
ALTER USER postgres WITH PASSWORD 'newpassword';
````

* Restrict Access: Use `pg_hba.conf` to control access

````bash
# Allow only specific IPs  
host    all             all             192.168.1.0/24          md5  
````

* Enable SSL: Edit `postgresql.conf`

````bash
ssl = on
ssl_cert_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem'  
ssl_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key'
````

* Audit Logging

````bash
log_statement = 'all'  
log_directory = 'pg_log'  
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
````

* Regular Backup: Use `pg_dump` for backup

````bash
pg_dump -U myuser -d mydb -f mydb_backup.sql
````



### Useful Commands

#### 1. Connecting to PostgreSQL

````postgresql
# login
psql -U username -d dbname

# switching database
\c dbname

# list databases
\l
````

#### 2. Managing a Database

````postgresql
# creation
CREATE DATABASE dbname;

# deletion
DROP DATABASE dbname;

# Backup a Database
pg_dump -U username -d dbname -f backup.sql

# Restoring a Backup
psql -U username -d dbname -f backup.sql
````

#### 3. Managing Tables

````postgresql
CREATE TABLE users (  
    id SERIAL PRIMARY KEY,  
    name TEXT NOT NULL,  
    email TEXT UNIQUE  
);  

# list tables
\dt

# describe a table
\d tablename

# delete a table
DROP TABLE tablename;
````

#### 4. Querying Data

````postgresql
SELECT * FROM users;  

SELECT * FROM users WHERE id = 1;  

SELECT * FROM users ORDER BY name ASC;  

SELECT * FROM users LIMIT 10;
````

#### 5. Inserting and Updating and Deleting Data

````postgresql
INSERT INTO users (name, email) VALUES ('John', 'john@example.com');

UPDATE users SET email = 'john.doe@example.com' WHERE id = 1;

DELETE FROM users WHERE id = 1;
````

#### 6. Indexes

````postgresql
CREATE INDEX idx_users_email ON users (email);

# list indices
\di

# dropping indices
DROP INDEX idx_users_email;
````

#### 7. User and Permission

````postgresql
# create a user
CREATE USER username WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE dbname TO username;
REVOKE ALL PRIVILEGES ON DATABASE dbname FROM username;

# list users
\du
````

#### 8. Troubleshooting

````postgresql
# check active connections
SELECT * FROM pg_stat_activity;  

# kill a connection
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid = 12345;

# check locks
SELECT * FROM pg_locks;
````

#### 9. Exporting and Importing Data

````postgresql
# export
\copy (SELECT * FROM users) TO 'users.csv' CSV HEADER;

# import 
\copy users FROM 'users.csv' CSV HEADER; 
````

#### 10. Transactions

````postgresql
BEGIN;  
UPDATE users SET email = 'new@example.com' WHERE id = 1;  
COMMIT; 
````

#### 11. Analyzing Query Performance

````postgresql
EXPLAIN ANALYZE SELECT * FROM users WHERE id = 1;
````



---

## File: unix/redis.md

# Redis

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

### Installation

Debain/Ubuntu

````bash
sudo apt update
sudo apt install redis-server

# check status
sudo systemctl status redis
````

macOS

````bash
brew install redis
brew service start redis
````

### Setup

#### Access Redis CLI : Connect to redis server

````bash
redis-cli
````

#### Test Connection

````bash
ping # server replies: PONG
````

#### Set and Get Data: storing and retrieving key-value pairs

````bash
SET mykey "Hello Redis"  
GET mykey 
````

#### Enabling Persistence

Edit `/etc/redis/redis.conf`

* For RDB (snapshotting)

````bash
save 900 1  # Save if 1 key changes in 900 seconds  
save 300 10 # Save if 10 keys change in 300 seconds
````

* For AOF (Append Only File)

````bash
appendonly yes  
appendfilename "appendonly.aof" 
````

Restart Redis

````bash
sudo systemctl restart redis
````

### Security

#### 1. Set a Password

Edit `/etc/redis/redis.conf`

````bash
requirepass yourpassword
````

````bash
sudo systemctl restart redis
````

````bash
# Authenticate in redis-cli
AUTH yourpassword
````

#### 2. Bind to Specific IP

Edit `/etc/redis/redis.conf`

````bash
bind 127.0.0.1
````

#### 3. Disable Dangerous Commands

````bash
rename-command FLUSHALL ""
````

#### 4. Enable Firewall

````bash
sudo ufw allow from 192.168.1.0/24 to any port 6379  
````

### Essential Commands

````bash
# set a key
SET mykey "Hello Redis"

# get a key
GET mykey

# delete a key
DEL mykey

# check if exists
EXISTS mykey
````

### Data Types

* Lists

  ````bash
  LPUSH mylist "item1"  
  RPUSH mylist "item2"  
  LRANGE mylist 0 -1  
  ````

* Sets

  ```bash
  SADD myset "item1"  
  SMEMBERS myset  
  ```

* Hashes

  ```bash
  HSET myhash field1 "value1"  
  HGET myhash field1 
  ```

* Sorted Sets

  ```bash
  ZADD myzset 1 "item1"  
  ZRANGE myzset 0 -1  
  ```

### Server Management

````bash
# flush all data
FLUSHALL

# get server info
INFO

# monitor commands
MONITOR
````

### Advanced Features

#### Pub/Sub Messaging

````bash
# publisher
PUBLISH mychannel "Hello"  

# sub
SUBSCRIBE mychannel
````

#### Transactions

Use `MULTI` and `EXEC` for atomic operations

````bash
MULTI  
SET key1 "value1"  
SET key2 "value2"  
EXEC  
````

#### Lua Scripting

````bash
EVAL "return redis.call('GET', 'mykey')" 0
````

### Troubleshooting

````bash
# view redis logs
sudo tail -f /var/log/redis/redis-server.log  

# test connection
redis-cli -h 127.0.0.1 -p 6379 ping  

# check memory usage
INFO memory
````

### Tips

````bash
# using redis as a cache
SET mykey "value" EX 60

# backup data using SAVE or BGSAVE to create snapshots
SAVE

# monitoring performance using redis-benchmark
redis-benchmark -n 100000 -c 50
````



---

## File: unix/ripgrep.md

# ripgrep

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

A faster, modern alternative to `grep`

### Installation

````bash
sudo apt install ripgrep
# brew install ripgrep
````

### Basic Usage

1. Search in Files

   ````bash
   rg "pattern"
   ````

2. Case-Insensitive Search

   ````bash
   rg -i "pattern"
   ````

3. Search in Specific File Types

   ````bash
   rg "pattern" -t py
   ````

4. Exclude Files/Directories

   ````bash
   rg "pattern" --glob '!node_modules'
   ````

5. JSON Output

   ````bash
   rg "pattern" --json
   ````

6. Replace Text

   ````bash
   rg "old" --replace "new"
   ````

### Combining `rg` with `fzf`

````bash
rg "pattern" | fzf
````



---

## File: unix/rsync.md

# rsync

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

### Installation

````bash
apt update
apt install rsync

# verify
rsync --version
````

### Basic Usage

#### Copy Files

````bash
rsync -av /src/ /dst/
# -a : archive mode
# -v : verbose
````

#### Dry Run

````bash
rsync -av --dry-run /source/ /destination/ 
````

#### Delete Extraneous Files

````bash
rsync -av --delete /source/ /destination/
````

#### Copy to Remote Server

````bash
rsync -av /source/ user@remote:/destination/
````

#### Copy from Remote Server

````bash
rsync -av user@remote:/source/ /destination/
````

#### Use SSH

````bash
rsync -av -e ssh /source/ user@remote:/destination/
````

### Exclude Files

````bash
rsync -av --exclude='*.log' /source/ /destination/
rsync -av --exclude={'*.log','*.tmp'} /source/ /destination/

# using exclude files
echo '*.log' > exclude.txt  
echo '*.tmp' >> exclude.txt  
rsync -av --exclude-from='exclude.txt' /source/ /destination/ 
````

### Tips

#### Automate Backups

````bash
# cron to schedule regular backups
0 2 * * * rsync -av /source/ /backup/ 
````

#### Use `--backup` for Versioning

````bash
# keep copies of overwritten files
rsync -av --backup --backup-dir=backup-$(date +%F) /source/ /destination/ 
````

#### Combine with Tar

````bash
# compress files before syncing
tar czf - /source/ | rsync -av -e ssh - user@remote:/destination/backup.tar.gz
````

### Example

#### rsync using ssh remote

````bash
#!/bin/sh
mkdocs build && rsync -avz --delete site/ smkroot:/var/www/notes/
exit 0
````



---

## File: unix/shell.md

# Bash/Zsh Shell Configuration

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

### Optimize terminal workflow

Installation (if required)

````bash
# Install Zsh  
sudo apt install zsh  

# Set Zsh as default shell  
chsh -s $(which zsh)  
````

### Configuration

Edit `~/.bashrc` or `~/.zshrc`

````bash
# Aliases
alias ll='ls -alh'
alias grep='grep --color=auto'

# Prompt customization
PS1='\[\033[1;32m\]\u@\h:\w\$ \[\033[0m\]'

# History settings
HISTSIZE=5000
HISTTIMEFORMAT="%F %T "
````

Apply Changes

````bash
source ~/.bashrc # or source ~/.zshrc
````

### Key Features

|  Command   |        Description        |
| :--------: | :-----------------------: |
|    `!!`    |    Rerun last command     |
|    `!$`    | last argument or prev cmd |
| `ctrl + r` |      search history       |
|   `cd -`   |    previous directory     |

#### Pro Tips

* Use `stow` to manage dotfiles:

````bash
mkdir ~/dotfiles && cd ~/dotfiles  
stow -t ~/ bash  
````

* Enable **autocompletion**

````bash
sudo apt install bash-completion
````

### smk’s dotfiles

````bash
# get the files
git clone https://github.com/mightyjoe781/.dotfiles

cd ~/.dotfiles
# validate install files, its a stow on array of folders

./install
````



---

## File: unix/sqlite.md

# SQLite3

[:octicons-arrow-left-24:{ .icon } Back](index.md)

### Installation

Debian/Ubuntu

````bash
sudo apt update
sudo apt install sqlite3
sqlite3 --version
````

macOS

````bash
# usually sqlite is preinstalled
sqlite3 --version
# or 
brew install sqlite
````

### Setup

````bash
# creating a database
sqlite3 mydb.db

# exit the sqlite shell
.exit

# import data from CSV
CREATE TABLE mytable (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);  
.mode csv  
.import data.csv mytable

# Export data to CSV
.headers on  
.mode csv  
.output data.csv  
SELECT * FROM mytable;  

````

### Security

#### File Permissions

SQLite databases are files. Use file system permissions to restrict access

````bash
chmod 600 mydb.db
````

#### Encryption

We can use extensions like SQLCipher for encryption

````bash
sqlcipher mydb.db
PRAGMA key = mysecretkey
````

#### Backup

````bash
sqlite3 mydb ".dump" > backup.sql
````

### Meta-Commands

````sqlite
# list tables
.tables

# describe a table
.schema users

# export data
.mode csv  
.output users.csv  
SELECT * FROM users;

# import data
.mode csv  
.import users.csv users  
````

### Advanced Features

#### Transaction

````bash
BEGIN;  
UPDATE users SET email = 'new@example.com' WHERE id = 1;  
COMMIT;  
````

#### Indexes

```bash
CREATE INDEX idx_users_email ON users (email);
```

#### Views

````bash
CREATE VIEW active_users AS SELECT * FROM users WHERE active = 1;
````

#### Triggers

Automate actions with triggers

````bash
CREATE TRIGGER update_timestamp AFTER UPDATE ON users  
BEGIN  
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;  
END;  
````

### Troubleshooting

````bash
# check database integrity
PRAGMA integrity_check

# recover data from `.dump` to recover data from a corrupted database
sqlite3 corrupted.db ".dump" | sqlite3 new.db

# debug queries
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'john@example.com';
````

### Tips

````bash
# use in-memory databases
sqlite3 :memory:

# backup automatically
sqlite3 mydb.db ".dump" | gzip > backup_$(date +%F).sql.gz

# optimizations
RAGMA journal_mode = WAL;  # Write-Ahead Logging  
PRAGMA synchronous = NORMAL;
````

### Resources

* https://www.sqlitetutorial.net

---

## File: unix/ssh.md

# SSH

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

Secure Shell (SSH) configuration for remote access and security.

***Warning:*** Always test SSH changes in a **second terminal** before disconnecting!

## Basic Configuration

Edit `/etc/ssh/sshd_config`

````bash
# Change default port
Port 23415
# Disable root login
PermitRootLogin no
# Allow specific users
AllowUsers smk deploy
# Key authentication only
PasswordAuthentication no
````

````bash
# Reload SSH
sudo systemctl reload ssh
````

## Key-Based Authentication

````bash
# Generate ED25519 key (client)
ssh-keygen -t ed25519 -C "smk@vps" -f ~/.ssh/vps_key

# Copy public key to server
ssh-copy-id -i ~/.ssh/vps_key.pub smk@your-server -p 23415

# SSH config shortcut (~/.ssh/config)
Host vps
  HostName your-server.com
  User smk
  Port 23415
  IdentityFile ~/.ssh/vps_key
  IdentitiesOnly yes
````

## Security Hardening

````bash
# Edit /etc/ssh/sshd_config
ClientAliveInterval 300
ClientAliveCountMax 2
MaxAuthTries 3
LoginGraceTime 1m
````

## Fail2Ban Setup

````bash
sudo apt install fail2ban
sudo cp /etc/fail2ban/jail.{conf,local}
````

Edit `/etc/fail2ban/jail.local`:

````bash
[sshd]
enabled = true
port = 23415
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 1h
ignoreip = 127.0.0.1/8
````

````bash
sudo systemctl restart fail2ban
````

## Useful Commands

````bash
# SSH tunnel
ssh -L 8080:localhost:80 vps

# SCP file transfer
scp -P 23415 file.txt vps:/path/

# Check active sessions
ss -tnp | grep 'ssh'
````

## Troubleshooting

````bash
# Check SSH status
sudo systemctl status ssh

# Test config syntax
sshd -t

# Verbose connection test
ssh -vvv vps

````



#### Reference: Full `~/.ssh/config` Setup

````yaml
Host *
Protocol 2
Compression no
StrictHostKeyChecking no
#-------- GIT COMMITS ----------
Host github gh github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

#-------- Proxy Example ---------
# Host smk.minetest.ca 1.1.1.1
    ProxyCommand ssh -xaqW%h:22195 minetest.in

# -------- Proxy SSH Example --------
Host bsdimp.com 1.1.1.1
    User smk
    HostName bsdimp.com
    Port 8798
    IdentityFile ~/.ssh/id_ed25519
    ProxyCommand ssh -xaqW%h:8792 minetest.in

# -------- remote ssh config --------
Host code
    HostName 1.1.1.1
    Port 22199
    User code
    IdentityFile ~/.ssh/smk.prvkey
    # useful for keeping vscode connected
    ServerAliveInterval 60
    ServerAliveCountMax 20
    # localhost forwarding settings
    ForwardAgent yes
    ExitOnForwardFailure no
    LogLevel QUIET
    LocalForward 3000 localhost:3000
    LocalForward 3001 localhost:3001
    LocalForward 4321 localhost:4321
    LocalForward 5000 localhost:5000
    LocalForward 8000 localhost:8000
    LocalForward 8385 localhost:8384

# ------------ Example SSH for FreeBSD ------
Host freebsd-vm
    HostName 192.168.69.3
    Port 22
    User smk
    IdentityFile /Users/smk/.ssh/id_ed25519
    RemoteCommand /compat/debian/bin/bash
    RequestTTY force
    SetEnv BASH_ENV=".bash_debian"

````



---

## File: unix/systemd.md

# systemd

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

Although some folks hate systemd :). I am more keen on solving my problem rather than getting into that debate. I still use init on my freeBSD instances.

Since I occasionally encounter system running systemd, I think there is no hard in getting familiar with it.

### Basic Commands

````bash
# start a service
sudo systemctl start servicename

# stop a service
sudo systemctl stop servicename

# restart a service
sudo systemctl restart servicename

# reload a service
sudo systemctl reload servicename

# enable a service
sudo systemctl enable servicename

# disable a service
sudo systemctl disable servicename

# check service status
sudo systemctl status servicename
````

#### Sytem Management

````bash
sudo systemctl reboot
sudo systemctl poweroff
sudo systemctl suspend
systemctl status
````

### Creating a Custom Service

Create `/etc/systemd/system/myservice.service`

````ini
[Unit]  
Description=My Custom Service  
After=network.target  

[Service]  
ExecStart=/usr/bin/myscript.sh  
Restart=on-failure  

[Install]  
WantedBy=multi-user.target  
````



````bash
# reload daemon
sudo systemctl daemon-reload
# enable the service
sudo systemctl start myservice  
sudo systemctl enable myservice
````

### Timers (Cron Alternatives)

Create a timer file : `/etc/systemd/system/mytimer.timer`

````ini
[Unit]  
Description=Run My Script Daily  

[Timer]  
OnCalendar=daily  
Persistent=true  

[Install]  
WantedBy=timers.target  
````

Create a Service File : `/etc/systemd/system/mytimer.service`

````ini
[Unit]  
Description=My Timer Service  

[Service]  
ExecStart=/usr/bin/myscript.sh
````

````bash
sudo systemctl enable mytimer.timer
sudo systemctl start mytimer.timer
````

### Debugging 

````bash
# view logs
journalctl -u servicename

# follow logs
journalctl -u servicename -f

# filter by time
journalctl --since "2023-10-01" --until "2023-10-02"
````

### Best Practies

* Limit Service Permissions: Use `User` and `Group` directives in service files

  ````ini
  [Service]  
  User=nobody  
  Group=nogroup
  ````

* Sandbox Services: Use `ProtectSystem` and `ProtectHome`

  ````ini
  [Service]  
  ProtectSystem=full  
  ProtectHome=true  
  ````

* Disable Unused services: `sudo systemctl disable servicename`

* Automate Service Restarts: Use `Restart=always` in service files

  ````ini
  [Service]  
  Restart=always  
  ````

* Identify rogue services during boottime: `systemd-analyze blame`

### Example Service to Send Pushover Notification on Server Reboot

Edit : `/etc/systemd/system/multi-user.target.wants/reboot_ntf.service`

````ini
[Unit]
Description=ntf reboot script
After=network-online.target
Wants=network-online.target
[Service]
ExecStart=/bin/bash -c 'sleep 2 && /usr/local/bin/ntf send -t REBOOT minetest.in just rebooted! > /var/log/reboot_ntf.log 2>&1'
Type=oneshot
RemainAfterExit=true
Environment=HOME=/root/
[Install]
WantedBy=multi-user.target
````



---

## File: unix/tar.md

# tar/gzip/zstd

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

## tar (tape archive)

used to bundle files into a single archive

### Basic Usage

#### 1. Create and Archive

````bash
tar -cvf archive.tar file1 file2
````

* `-c`: create archive
* `-v`: verbose output
* `-f`: specify archive filename

#### 2. Extract an Archive

````bash
tar -xvf archive.tar
````

* `-x`: Extract files
* files are extracted into current directory by default

#### 3. List Archive Contents

````bash
tar -tvf archive.tar
````

### Common Scenarios

1. Extract to a Specific Directory

   ````bash
   tar -xvf archive.tar -C /path/to/dir
   ````

2. Create and archive from a Directory

   ````bash
   tar -cvf archive.tar /path/to/dir
   ````

3. Exclude file

   ````bash
   tar -cvf archive.tar --exclude="*.log" /path/to/dir
   ````

4. Extracting only `txt` files

   ````bash
   tar -xvf archive.tar --wildcards "*.txt"
   ````

5. Combine with `find` archive specific files

   ````bash
   find . -name "*.txt" | tar -cvf archive.tar -T -
   ````

## gzip

Compress files using `.gz` format

### Basic Usage

#### 1. Compress a file

````bash
gzip file.txt
````

#### 2. Decompress a file

````bash
gzip -d file.txt.gz
````

#### 3. Compress and Archive

````bash
tar -czvf archive.tar.gz file1 file2
````

#### 4. Extract `.tar.gz`

````bash
tar -xzvf archive.tar.gz
````

#### 5. View Compressed files without extraction

````bash
zcat file.txt.gz
````

* Use `gunzip` as an alias for `gzip -d`

## Zstd (Z Standard)

A modern compression tool with better speed and ratios

### Basic Usage

#### 1. Compress a File

````bash
zstd file.txt
````

#### 2. Decompress a File

````bash
zstd -d file.txt.zst
````

#### 3. Compress and Archive

````bash
tar -cvf archive.tar.zst --zstd file1 file2
````

#### 4. Extract `.tar.zst`

````bash
tar -xvf archive.tar.zst --zstd
````

You can adjust compression level : `zstd -19 file.txt`

Use `unzstd` as alias for `zstd -d`

### Comparison between gzip and zstd

| Tool   | Speed  | Compression Ratio | Common Use Cases           |
| ------ | ------ | ----------------- | -------------------------- |
| `gzip` | Medium | Good              | General-purpose            |
| `zstd` | Fast   | Excellent         | Modern systems, large data |

#### Notes

* take a look at `pigz` (parallel implementation of gzip)

---

## File: unix/terraform.md

# Terraform 

[:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guides](../terraform/index.md)

Infrastructure as Code (IaC) for cloud provisioning.

### Installation

````bash
# Using apt  
sudo apt-get update && sudo apt-get install terraform  

# Manual install  
wget https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip  
unzip terraform_1.5.7_linux_amd64.zip && sudo mv terraform /usr/local/bin/  
````

### Commands

| Command                | Description                  |
| ---------------------- | ---------------------------- |
| `terraform init`       | Initialize working directory |
| `terraform plan`       | Preview changes              |
| `terraform apply`      | Apply configuration          |
| `terraform destroy`    | Delete infrastructure        |
| `terraform state list` | List managed resources       |

### Sample AWS EC2 Config

Example `main.tf`

````hcl
provider "aws" {  
  region = "us-west-2"  
}  

resource "aws_instance" "web" {  
  ami           = "ami-0c55b159cbfafe1f0"  
  instance_type = "t2.micro"  

  tags = {  
    Name = "Terraform-Web"  
  }  
}  
````

### State Management

* local state

````bash
terraform state pull > backup.tfstate  
````

* remote backend (s3)

````bash
terraform {  
  backend "s3" {  
    bucket = "my-tf-state"  
    key    = "prod/terraform.tfstate"  
    region = "us-east-1"  
  }  
}  
````

### Tips

* Variables

````hcl
variable "region" {  
  default = "us-west-2"  
}  
````

* Workspaces

````hcl
terraform workspace new dev  
````

* plan output

````hcl
terraform plan -out=tfplan  
terraform apply tfplan  
````

### Security

1. **Secret Management**:

   ```hcl
   data "aws_secretsmanager_secret" "db_pass" {  
     name = "prod/db"  
   }  
   ```

2. **Lock State**: Use S3/DynamoDB for state locking.

### Troubleshooting

| Issue                | Solution                        |      |
| -------------------- | ------------------------------- | ---- |
| "Provider not found" | Run `terraform init`            |      |
| "State locked"       | Manually remove `.tfstate.lock` |      |
| Plan/apply mismatch  | Use `-refresh=false` flag       |      |

### Resources

* [Terraform Registry](https://registry.terraform.io/)
* [AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

## File: unix/tldr.md

# tldr

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

Simplified man pages for quick reference

### Installation

````bash
sudo apt install tldr
# brew install tldr
````

### Basic Usage

````bash
tldr tar
# tldr fzf
````

````bash
tldr tldr	# understand usecases of tldr
````

### Example Uses

* with fzf

````bash
tldr --list | fzf | xargs tldr  # open fzf menu with all tldr cmds
````

* get a random command

````bash
tldr --list | shuf -n1 | xargs tldr  
````

---

## File: unix/tmux.md

# Tmux

 [:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guide](../tmux/index.md)

## Installation

````bash
sudo apt install tmux
````

### Configuration

Edit `~/.tmux.conf`

````bash
# Remap prefix to Ctrl-a  
unbind C-b  
set -g prefix C-a  

# Mouse support  
set -g mouse on  

# Split panes  
bind | split-window -h  
bind - split-window -v  

# Status bar  
set -g status-bg cyan  
````

* [Configuration Guide](../tmux/tmux2/ch2.md)
* [Example .conf](https://raw.githubusercontent.com/mightyjoe781/.dotfiles/refs/heads/master/tmux/.tmux.conf)

Reload Config

````bash
tmux source-file ~/.tmux.conf
````

### Key Workflows

| Command              | Workflow            |
| -------------------- | ------------------- |
| `tmux new -s <name>` | Start named Session |
| `Ctrl-a d`           | Detach Session      |
| `tmux ls`            | List Session        |
| `Ctrl-a c`           | New Window          |

#### Pro Tips

* Persist sessions with `tmux-resurrect`

````bash
git clone https://github.com/tmux-plugins/tmux-resurrect ~/.tmux/plugins/tmux-resurrect  
````

* Use `ssh-agent` in tmux for shared keys.
* https://tmuxcheatsheet.com/


---

## File: unix/ufw.md

# ufw

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

NOTE: Do not copy paste these commands except you understand each of them.

### Installation

````bash
apt -y install ufw
systemctl enable ufw
````

### Setup

````bash
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22195
ufw allow from <EDGE_NODE_IP> to any port 8000	# connect edge agents to portainer

ufw default reject incoming
ufw default allow outgoing
ufw default deny routed

ufw show added
ufw show listening
````

After reviewed. Activate your firewall

````bash
ufw --force enable
ufw status verbose
````

### Chain Default Action

````bash
ufw [--dry-run] default allow|deny|reject [incoming|outgoing|routed]
````

#### Safe Mode (Allow all chain)

````bash
ufw default allow incoming
ufw default allow outgoing
ufw default allow routed
````

#### Recommended

````bash
ufw default reject incoming
ufw default allow outgoing
ufw default deny routed	# drop forward chain
````

### Firewall Rules

#### Rule Syntax

````bash
ufw [rule]
  [delete] [insert NUM] [prepend]
  allow|deny|reject|limit
  [in|out [on INTERFACE]]
  [log|log-all]
  [proto PROTOCOL]
  [from ADDRESS [port PORT | app APPNAME ]]
  [to ADDRESS [port PORT | app APPNAME ]]
  [comment COMMENT]
````

#### Abbreviated allow syntax using Port/Protocol

````bash
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
````

#### Abbreviated allow syntax using Service Name

````bash
ufw allow ssh
ufw allow http
ufw allow https
````

Check service name from `/etc/services` and replace port/protocol with it.

````bash
cat /etc/services | head -35 | tail -10
````

#### Abbreviated allow syntax using UFW Application Profile

````bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
````

````bash
# check available app profiels
ufw app list

# app profile info
ufw app info <appname>

# app profiles directory : /etc/ufw/applications.d/
````

#### Full allow incoming connection syntax

````bash
## using port/protocol
ufw allow in proto tcp to any port 22## using service name
ufw allow in to any port ssh## using application profile
ufw allow in to any app OpenSSH
````

#### Allow incoming connection from specific source

- **Network Interface**: add `in on <interface>` after `ufw`
- **Source IP/CIDR**: add `from <IP/CIDR>` after `ufw allow`

````bash
## specific incoming interface
ufw allow in on eth0 proto tcp to any port 22
ufw allow in on eth0 to any port ssh## specific source ip
ufw allow from 192.168.1.0/24 proto tcp to any port 22
ufw allow from 172.16.1.10 proto tcp to any port 80
ufw allow from 172.16.1.10 proto tcp to any port 443## or both
ufw allow in on eth0 from 192.168.1.0/24 to any port 22
````

### Show Report

#### Report Syntax

````bash
ufw show raw
ufw show builtins|before-rules|user-rules|after-rules|logging-rules
ufw show listening
ufw show added
````

#### Show listening ports along with firewall rules

````bash
ufw show listening
````

NOTE: if some service doesn’t have any rules then default chain action is executed.

#### Show added rules

````bash
ufw show added
````

### Control your Firewall

- `ufw enable` — Activate ufw by adding all ufw iptables rules
- `ufw disable` — Remove all ufw iptables rules
- `ufw reload` — Reload config (e.g. `/etc/default/ufw` `/etc/ufw/*` )

### Status — Check UFW Status

Syntax: `ufw status [verbose|numbered]`

---

