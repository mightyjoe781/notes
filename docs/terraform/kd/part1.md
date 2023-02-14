### 1. Introduction

Terraform is written in Golang.
Terraform uses graph theory to plot relationships between resources.

HCL - Hashicorp configuration language.

IaC tools:

- AWS :: Cloudformation
- Azure :: Resource Manager
- GCP :: Deployment Manager
- Terraform

<hr>

### 2. Files in Terraform


files:

- provider.tf :: A provider in Terraform is a connection that allows Terraform to manage infrastructure using predefined interface
- resources.tf :: define the resource - represent things in real world
- variables.tf :: dynamic values - value set at runtime
- data-source.tf :: used to fetch data from a resource that is not managed by terraform
- outputs.tf :: outputs from provisioning

<hr>
### 3. Terraform State

NOTE: terraform.tfstate :: state according to terraform

`Terraform state :: terraform.tfstate`

- record of all resources that it has created
- it stores in local file terraform.tfstate
- the file also stores dependency order of the resources that have been created

<hr>

### 4. Resources

- allows you to define what you want to create in real world

**Resource Block**

- describes one or more infrastructure objects
ex: virtual network, compute instances, dns record

- declares a resource of a:
    + given type "aws_instance"
    + given name "my_instance"

ex:
    ```
    resource "aws_instance" "my_instance"{
            ami = "ami-1234qwerty"
            instance_type = "t2.micro"
        }
    ```

where::
    1. resource type  = aws_instance
    2. local resource name = my_instance
    3. argument name = ami, instance_type
    4. argument value =  ami-1234qwerty,t2.micro

**Implicit dependency in Resource Block**

- Terraform will automatically manage Implicit dependency by find reference objects and creating an Implicit ordering

ex:

```
resource "aws_eip" "my_eip"{
	vpc = "true"
}
```

    resource "aws_instance" "my_instance"{
        ami = "ami-1234qwerty"
        instance_type = "t2.micro"
        public_ip = aws_eip.my_eip.private_ip
    }

**Explicit dependency in Resource Block**

- is only required when resource relies on another resource behavior

ex:

````
resource "aws_s3_bucket" "example"{
		acl = "private"
}
````

    resource "aws_instance" "my_instance"{
        instance_type = "t2.micro"
        depends_on = [aws_s3_bucket.example]
    }

-----------------------

### 5. Terraform workflow/lifecycle

1. terraform init :: Prepare your working directory for other command
2. terraform plan :: show changes required by the current configuration
3. terraform apply :: create, update, or delete infrastructure
4. terraform destroy ::  destroy previously created infrastructure

----------------------

### 6. Terraform debugging/troubleshooting

- enable logging in terraform with `TF_LOG` environment variable
- presist logging output with `TF_LOG_PATH`

Values:
TF_LOG=TRACE :: Highest verbosity
TF_LOG=DEBUG
TF_LOG=INFO
TF_LOG=WARN
TF_LOG=ERROR :: lowest verbosity

ex:
    export TF_LOG=TRACE
    export TF_LOG_PATH=/logs/terraform.log


------------------------

### 7. Data Sources

- used to fetch data from a resource that is not managed by terraform 
- allows data to be fetched or computed from elsewhere in terraform configuration

ex:
    data "aws_ami" "example"{
        executable_users = ["self"]
        most_recent = true
        name_regex = "^myami-\\d{3}"
        owners = ["self"]

        filter {
            name="name"
            values = ["myami-*"]
        }
        filter {
            name="root-device-type"
            values=["ebs"]
        }
        filter {
            name="virtualization-type"
            values=["hvm"]
        }
    }

------------------------------

### 8. Variables in Terraform

- something set at runtime
- allows you to vary what terraform will do when passing in or using a dynamic value
- variable with undefined values will not directly result in ERROR
    NOTE: Terraform will ask you to supply a value **IMPORTANT** 
    ex:
        variable custom_var {}
- In version 0.12>=  :: var.instance_type declaration
- In version 0.11<=  :: ${var.instance_type} declaration

**3 types of variable types**

1. Simple variable types
    - String
    - Number
    - boolean

    ex:
        variable "aws_region"{
            type=string #type enforcement
            default="us-west-2"
        }
        variable "instance_count"{
            type=Number
            default=2
        }
        variable "enable_vpn_gateway"{
            type=bool
            default=false
        }


2. Collection Variable types (NOTE: all values of same type)
    - list :: [] 
    - map :: {k1=v1,k2=v2}
    - set :: an unordered collection of unique Values

    ex:
        variable "private_subnet_cidr_blocks"{
            type = list(string)
            default=[
                "10.0.101.0/24",
                "10.0.102.0/24",
                "10.0.103.0/24"
            ]
        }

        variable "resouce_tags"{
            type=map(string)
            default={
                project="project-alpha",
                environment="dev"
            }
        }


3. Structure Variable types
    - tuple :: ficed-length sequence of values of specified types - ["a",15,true]
    - object - A lookup table, matching a fixed set of keys to values of specified types

**Variable Precendence Order (Highest to lowest)**

1. -var or -var-file on command line
    ex:
        terraform apply -auto-approve \
        -var "aws_access_key=<KEY>" \
        -var "aws_secret_key="<KEY>"

2. *.auto.tfvars or *.auto.tfvars.json

3. terraform.tfvars
    ex:
        instance_type="t2.large"

4. variables.tf
    ex:
        variable "instance_type"{
            default="t2.micro"
        }

5. environment variables
    - can be used to set a variable
    - must be in format TF_VAR_name
      ex:
        .bashrc
        export TF_VAR_instance_type=t2.micro
        export TF_VAR_ami=ami-12345abc

-----------------------------

### 9. Splat Expressions

- The splat[*]
- the special splat[*] symbol iterates over all the elements of a given list to its left and accesses from each one the attribute name given on its right.

    ex:
    
    ````
    resource "aws_iam_user" "lb"{
      name="loadbalancer.${count.index}"
      count=3
      path="/system/"
    }
    ````
    
        output "arns"{
            value=aws_iam_user.lb[*].arn
        }

--------------------------------

### 10. Functions in Terraform

Built-in functions
1. Numeric
    abs/ceil/floor/log/max/min/parseint/pow/signum

2. String
    chomp/format/formatlist/indent/join/lower/regex/regexall/replace/split/strrev/substr/title/trim/trimprefix/trimsuffix/trimspace/upper

3. Collection 
    alltrue/anytrue/chunklist/coalesce/coalescelist/compact/concat/contains/distinct/element/flatten/index/keys/length/list/lookup/map/matchkeys/merge/one/range/reverse/setintersection/setproduct/setsubtract/setunion/slice/sort/sum/transpose/values/zipmap

4. Encoding
    base64decode/base64encode/base64gzip/csvdecode/jsondecode/jsonencode/textdecodebase64/textencodebase64/urlencode/yamldecode/yamlencode

5. Filesystem
    abspath/dirname/pathexpand/basename/file/fileexists/fileset/filebase64/templatefile

6. Date and Time 
    formatdate/timeadd/timestamp

7.Hash and crypto
    base64sha256/base64sha512/bcrypt/filebase64sha256/filebase64sha512/filemd5/filesha1/filesha256/filesha512/md5/rsadecrypt/sha1/sha256/sha512/uuid/uuidv5

8. IP network
    cidrhost/cidrnetmask/cidrsubnet/cidrsubnets

9. Type Conversion
    can/defaults/nonsensitive/sensitive/tobool/tolist/tomap/tonumber/toset/tostring/try/type

ex:
    - join :: produces a string by concatenating together all elements of a given list of strings with given delimeter
    - chomp :: removes newline characters at the end of a string
    - split :: produces a list by dividing string at all occurences of a given separator
    - max :: takes one ore more numbers and returns the greatest number from the set
    - slice :: extracts some consecutive elements from within a list

NOTE: User defined functions are not supported
NOTE: **IMPORTANT**
    - slice is NOT part of "string" function it is part of "Collection" function

--------------------------------
