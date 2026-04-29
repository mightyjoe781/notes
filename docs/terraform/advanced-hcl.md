# Advanced HCL

## Built-in Functions

Terraform has a set of built-in functions. **User-defined functions are not supported.**

Call syntax: `function_name(arg1, arg2)`

### Numeric

`abs` `ceil` `floor` `log` `max` `min` `parseint` `pow` `signum`

```hcl
max(5, 12, 9)    # 12
min(5, 12, 9)    # 5
ceil(1.2)        # 2
floor(1.9)       # 1
```

### String

`chomp` `format` `formatlist` `indent` `join` `lower` `upper` `regex` `regexall` `replace` `split` `strrev` `substr` `title` `trim` `trimprefix` `trimsuffix` `trimspace`

```hcl
join(", ", ["a", "b", "c"])         # "a, b, c"
split(",", "a,b,c")                 # ["a", "b", "c"]
lower("HELLO")                      # "hello"
replace("hello world", "world", "terraform")  # "hello terraform"
chomp("hello\n")                    # "hello"
```

### Collection

`alltrue` `anytrue` `chunklist` `coalesce` `coalescelist` `compact` `concat` `contains` `distinct` `element` `flatten` `index` `keys` `length` `lookup` `map` `matchkeys` `merge` `one` `range` `reverse` `setintersection` `setproduct` `setsubtract` `setunion` `slice` `sort` `sum` `transpose` `values` `zipmap`

```hcl
length(["a", "b", "c"])             # 3
contains(["a", "b"], "a")           # true
merge({a=1}, {b=2})                 # {a=1, b=2}
flatten([[1,2],[3,4]])               # [1,2,3,4]
lookup({env="dev"}, "env", "prod")  # "dev"
```

> **Exam note:** `slice` is a **Collection** function, not a String function.

### Encoding

`base64decode` `base64encode` `base64gzip` `csvdecode` `jsondecode` `jsonencode` `textdecodebase64` `textencodebase64` `urlencode` `yamldecode` `yamlencode`

```hcl
jsonencode({name = "terraform"})    # "{\"name\":\"terraform\"}"
jsondecode("{\"name\":\"test\"}")   # {name = "test"}
base64encode("hello")               # "aGVsbG8="
```

### Filesystem

`abspath` `dirname` `pathexpand` `basename` `file` `fileexists` `fileset` `filebase64` `templatefile`

```hcl
file("~/.ssh/id_rsa.pub")           # reads file contents
fileexists("config.json")           # true/false
templatefile("init.sh.tpl", { name = "web" })
```

### Date and Time

`formatdate` `timeadd` `timestamp`

```hcl
timestamp()                         # current UTC time
timeadd(timestamp(), "24h")        # 24 hours from now
```

### Hash and Crypto

`base64sha256` `base64sha512` `bcrypt` `filebase64sha256` `filebase64sha512` `filemd5` `filesha1` `filesha256` `filesha512` `md5` `rsadecrypt` `sha1` `sha256` `sha512` `uuid` `uuidv5`

```hcl
md5("hello")
sha256("hello")
uuid()   # generates a new UUID each time (triggers re-apply)
```

### IP Network

`cidrhost` `cidrnetmask` `cidrsubnet` `cidrsubnets`

```hcl
cidrsubnet("10.0.0.0/16", 8, 1)    # "10.0.1.0/24"
cidrhost("10.0.1.0/24", 5)         # "10.0.1.5"
```

### Type Conversion

`can` `nonsensitive` `sensitive` `tobool` `tolist` `tomap` `tonumber` `toset` `tostring` `try` `type`

```hcl
tostring(42)       # "42"
tonumber("42")     # 42
tobool("true")     # true
toset(["a","a","b"])  # {"a","b"} (deduplicates)
```

## Conditional Expressions

Ternary syntax: `condition ? value_if_true : value_if_false`

```hcl
# use var.ami if provided, otherwise use the latest Ubuntu AMI
resource "aws_instance" "server" {
  ami           = var.ami != "" ? var.ami : data.aws_ami.default.id
  instance_type = var.instance_size
}
```

Common use with `count` to conditionally create a resource:

```hcl
resource "aws_eip" "pip" {
  count             = var.create_public_ip ? 1 : 0
  network_interface = aws_instance.server.primary_network_interface_id
  domain            = "vpc"
}
```

## count

`count` creates multiple instances of a resource. Use `count.index` (starts at 0) to give each instance a unique name.

```hcl
resource "aws_instance" "server" {
  count         = 4
  ami           = "ami-a1b2c3d4"
  instance_type = "t2.micro"

  tags = {
    Name = "Server ${count.index}"
    # creates: Server 0, Server 1, Server 2, Server 3
  }
}
```

Reference a specific instance: `aws_instance.server[0].id`  
Reference all instances: `aws_instance.server[*].id`

## for_each

`for_each` is preferred over `count` when working with maps or sets because it gives each instance a stable identity (key), not a numeric index.

```hcl
variable "servers" {
  default = {
    web = "t2.micro"
    api = "t2.small"
    db  = "t3.medium"
  }
}

resource "aws_instance" "server" {
  for_each      = var.servers
  ami           = "ami-a1b2c3d4"
  instance_type = each.value

  tags = {
    Name = each.key
  }
}
```

Reference: `aws_instance.server["web"].id`

## Dynamic Blocks

Dynamic blocks generate repeated nested blocks (like `ingress`, `ebs_block_device`) from a collection variable. This avoids repeating the same block multiple times.

```hcl
variable "ebs_volumes" {
  type = list(object({
    device_name = string
    volume_size = number
    volume_type = string
  }))
}

resource "aws_instance" "server" {
  ami           = "ami-0528a5175983e7f28"
  instance_type = "t2.micro"

  dynamic "ebs_block_device" {
    for_each = var.ebs_volumes
    content {
      device_name = ebs_block_device.value.device_name
      volume_size = ebs_block_device.value.volume_size
      volume_type = ebs_block_device.value.volume_type
    }
  }
}
```

The `content` block defines what each generated block looks like. Reference the current iteration value with `<block_label>.value`.
