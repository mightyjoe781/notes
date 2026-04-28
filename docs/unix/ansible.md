# Ansible

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Agentless configuration management and automation. Push-based: runs tasks over SSH, no software needed on managed nodes.

### Key Concepts

| Concept | Description |
|---|---|
| Inventory | list of hosts to manage |
| Playbook | YAML file describing what to do |
| Task | single action (install package, copy file, start service) |
| Module | built-in function that performs a task (`apt`, `copy`, `service`) |
| Role | reusable collection of tasks, handlers, templates |
| Handler | task triggered by `notify`, runs once at end of play |
| Vault | encrypted secrets storage |

### Installation

```bash
sudo apt install ansible
pip install ansible                  # or via pip
ansible --version
```

### Inventory

```ini
# inventory.ini
[web]
web1.example.com
web2.example.com ansible_user=ubuntu ansible_port=2222

[db]
db1.example.com

[production:children]
web
db

[production:vars]
ansible_ssh_private_key_file=~/.ssh/deploy
```

```yaml
# inventory.yaml (alternative)
all:
  children:
    web:
      hosts:
        web1.example.com:
        web2.example.com:
    db:
      hosts:
        db1.example.com:
```

```bash
ansible -i inventory.ini all -m ping          # test connectivity
ansible -i inventory.ini web -m command -a "uptime"
```

### Playbook Structure

```yaml
- name: Configure web servers
  hosts: web
  become: true                       # run as root (sudo)
  vars:
    http_port: 80

  tasks:
  - name: Install Nginx
    apt:
      name: nginx
      state: present
      update_cache: true

  - name: Copy config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: restart nginx

  - name: Start and enable Nginx
    service:
      name: nginx
      state: started
      enabled: true

  handlers:
  - name: restart nginx
    service:
      name: nginx
      state: restarted
```

```bash
ansible-playbook -i inventory.ini site.yml
ansible-playbook -i inventory.ini site.yml --check  # dry run
ansible-playbook -i inventory.ini site.yml --diff    # show file diffs
ansible-playbook -i inventory.ini site.yml --tags "nginx"
ansible-playbook -i inventory.ini site.yml --limit web1.example.com
```

### Common Modules

```yaml
# apt / yum / dnf - package management
- apt: name=nginx state=present update_cache=true
- apt: name=nginx state=absent

# file - manage files and directories
- file: path=/opt/app state=directory owner=app mode="0755"

# copy - copy file to remote
- copy: src=files/app.conf dest=/etc/app/app.conf mode="0644"

# template - Jinja2 template
- template: src=templates/nginx.conf.j2 dest=/etc/nginx/nginx.conf

# command / shell - run commands
- command: /usr/bin/my-script.sh
- shell: "echo {{ message }} > /tmp/msg.txt"

# user - manage users
- user: name=deploy shell=/bin/bash groups=sudo append=true

# git - clone repository
- git: repo=https://github.com/org/app.git dest=/opt/app version=main

# systemd - manage services
- systemd: name=nginx state=restarted enabled=true daemon_reload=true

# lineinfile - manage lines in files
- lineinfile: path=/etc/hosts line="10.0.0.5 db.internal"
```

### Variables

```yaml
# In playbook
vars:
  db_host: "localhost"

# In vars file
- include_vars: vars/prod.yaml

# In inventory group_vars/web.yaml
# In inventory host_vars/web1.example.com.yaml

# Pass on command line
ansible-playbook site.yml -e "version=1.2.3"

# Variable precedence (highest wins): extra vars > task vars > block vars > play vars > host vars > group vars > defaults
```

### Ansible Vault

```bash
# Encrypt a file
ansible-vault encrypt secrets.yaml

# Edit encrypted file
ansible-vault edit secrets.yaml

# Use vault in playbook run
ansible-playbook site.yml --ask-vault-pass
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```

### Roles

```
roles/
  nginx/
    tasks/main.yaml
    handlers/main.yaml
    templates/nginx.conf.j2
    defaults/main.yaml     # overridable defaults
    vars/main.yaml         # non-overridable vars
    files/
    meta/main.yaml
```

```bash
ansible-galaxy init my_role          # scaffold a role
ansible-galaxy install geerlingguy.nginx  # install from Galaxy
```

### Tips

- Use `--check` (dry run) with `--diff` to preview changes before applying
- Break large playbooks into roles for reusability
- Use handlers for service restarts - they run once regardless of how many tasks notify them
- `when: ansible_os_family == "Debian"` for conditional tasks
- `serial: 1` on a play applies changes one host at a time (rolling update)

### See Also

- [Terraform](terraform.md) for provisioning infrastructure before configuration
- Also: Pulumi, Salt, Chef, Puppet, Fabric (Python-based)
