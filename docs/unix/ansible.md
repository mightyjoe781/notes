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

1. Create an Inventory File: Save this as `inventory.ini`

````ini
[webservers]
192.168.1.10
192.168.1.11

[dbservers]  
192.168.1.20
````

2. Test Connectivity

````bash
ansible all -i inventory.ini -m ping
````

3. Write Your First Playbook: Save as `webserver.yml`

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

4. Run the Playbook

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
