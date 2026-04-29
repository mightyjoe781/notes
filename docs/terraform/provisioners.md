# Provisioners

## What are Provisioners?

Provisioners run scripts or commands on a resource after it is created or before it is destroyed.

> **Use sparingly.** Provisioners are a last resort. For ongoing configuration management, prefer purpose-built tools like Ansible, Chef, or Puppet. Provisioners make Terraform less predictable and harder to reason about.

Provisioners live inside a `resource` block.

## local-exec

Runs a command on the **machine running Terraform** (not the target resource). Useful for triggering external scripts, notifications, or updating local records.

```hcl
resource "aws_instance" "my_instance" {
  ami           = data.aws_ami.app_ami.id
  instance_type = var.instance_type

  provisioner "local-exec" {
    command = "echo ${self.private_ip} >> private_ips.txt"
  }
}
```

Use `self` to reference attributes of the containing resource.

## remote-exec

Runs commands **on the target resource** over SSH or WinRM. Useful for bootstrapping software on a new instance.

Supported connection types:
- `ssh` - Linux/macOS instances
- `winrm` - Windows instances

```hcl
resource "aws_instance" "myec2" {
  ami                    = "ami-1234qwerty"
  instance_type          = "t2.micro"
  key_name               = "terraform-key-name"
  vpc_security_group_ids = [aws_security_group.allow_ssh.id]

  provisioner "remote-exec" {
    inline = [
      "sudo dnf install -y nginx",
      "sudo systemctl start nginx"
    ]

    connection {
      type        = "ssh"
      user        = "ec2-user"
      private_key = file("~/terraform.pem")
      host        = self.public_ip
    }
  }
}

resource "aws_security_group" "allow_ssh" {
  name = "allow_ssh"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Provisioner Types

| Provisioner | Description |
|-------------|-------------|
| `local-exec` | Run command locally on the Terraform host |
| `remote-exec` | Run commands on the remote resource |
| `file` | Copy files or directories to the remote resource |
| `null_resource` | Run provisioners without creating real infrastructure |

Deprecated provisioners (no longer recommended): `chef`, `puppet`, `habitat`, `salt-masterless`

## Timing: Creation vs Destroy

### Creation-Time (default)

Provisioner runs after the resource is created.

- If the provisioner fails, the resource is marked **tainted**
- A tainted resource will be destroyed and recreated on the next `terraform apply`

### Destroy-Time

Provisioner runs before the resource is destroyed. Add `when = destroy`.

```hcl
resource "aws_instance" "my_instance" {
  ami           = data.aws_ami.app_ami.id
  instance_type = var.instance_type

  provisioner "local-exec" {
    when    = destroy
    command = "echo ${self.private_ip} decommissioned >> audit.log"
  }
}
```

## Failure Behavior

Control what happens if a provisioner fails with `on_failure`:

| Value | Behavior |
|-------|----------|
| `fail` | Default. Raise error, stop apply, mark resource as tainted |
| `continue` | Log the error and continue |

```hcl
provisioner "local-exec" {
  command    = "some-script.sh"
  on_failure = continue
}
```
