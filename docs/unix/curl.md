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

