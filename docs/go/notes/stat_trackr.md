### Website Status Tracker Application

This is an example of channels and parallelism in go.

Consider this code which goes through a list of websites and prints their status.

````go
package main

import (
	"fmt"
	"net/http"
)

func main() {

	links := []string{
		"http://google.com",
		"http://facebook.com",
		"http://stackoverflow.com",
		"http://golang.org",
		"http://amazon.com",
		"http://books.minetest.in",
	}
	for _, link := range links {
		checkLink(link)
	}
}

func checkLink(link string) {
	_, err := http.Get(link)  // <-- Blocking Call
	if err != nil {
		fmt.Println(link, "might be down!")
		return
	}
	fmt.Println(link, "is up!")
}
````

If we execute above program you will notice a delay in processing of each of links. Delay is present because go program waits for response from each of the website.

If we had 1000 such links, checking a website status might take a lot of time and to again check google.com might end up taking 1 hour. A website might go down and be back up in that timespace. We will fix program such that rather than serial checking of website it happens in parallel. Once a website is checked it keeps checking on.

#### Goroutine

Whenever we execute a program we basically execute a *main* goroutine. Main program executes line by line until it hits blocking function call and execution gets paused and waits for response to come back. We can create additional goroutines that will handle the blocking call so the main goroutine can keep on processing instead of getting blocked.

`go checkLink(link)` : go keyword is used to create a goroutine.

Go scheduler runs one routine until it finishes or makes a blocking call. It starts executing other goroutines in queue pausing the blocked goroutine. So its not actually parallelism instead Go scheduler smartly optimizing queues and running them Concurrently. By default go uses only one core.

In case of multiple CPU cores Go scheduler can easily spawn goroutines parallely. 

*Concurrency is not Parallelism :P*

Concurrency : Multiple threads executing code. If one thread blocks, another is picked up and worked on. Smart scheduling.

Parallelism : (Only in case of multiple CPU cores) Multiple threads executed at the exact same time. Requires multiple CPU’s.

Try adding go keyword to function and execute. Wait it doesn’t output anything :) ??? What happened is that multiple child goroutines were spawned by main goroutine but those all couldn’t complete but main goroutines reached the end and exited killing child goroutines. So we will need to make main goroutine to wait for response to come back from child goroutines.

#### Channels

Only way to communicate between goroutines. We can send messages to channels which becomes automatically gets sent to all the running goroutines that are running on machine and have access to that channel.

Channels are typed and the data shared by channel must be of same type.

```go
c := make(chan string)
```

Note we will need to pass in the channel to all the goroutines that we want to have to access to channel.

#### Sending Data through Channels

- channel<-5 : sends value 5 into the channel
- myNumber <- channel : wait for a value to be sent into the channel. When we get one, assign the value to `myNumber`
- fmt.Println(<-channel) : wait for a value to be sent into the channel. When we get one, we immediately log it out.

We will need for this application purpose all the goroutines to exit, so we will need to wait for all n channels for n websites.

Current Solution :

````go
package main

import (
	"fmt"
	"net/http"
)

func main() {

	links := []string{
		"http://google.com",
		"http://facebook.com",
		"http://stackoverflow.com",
		"http://golang.org",
		"http://amazon.com",
		"http://books.minetest.in",
	}

	c := make(chan string)

	for _, link := range links {
		go checkLink(link, c)
	}

	for i := 0; i < len(links); i++ {
		fmt.Println(<-c) // Note this stops and waits on first execution
	}

}

func checkLink(link string, c chan string) {
	_, err := http.Get(link)
	if err != nil {
		fmt.Println(link, "might be down!")
		c <- "might be down"
		return
	}
	fmt.Println(link, "is up!")
	c <- "It is up"
}
````

#### Modification

Now we are going to design Website Tracker to track website continuously. We can do easily that by sending `c<-link` in checkLink. And change line 26 to `go checkLink(<-c,c)`. This makes channel loop infinitely.

````go
for {
  go checkLink(<-c,c)
}
````

It may look like infinite loop but there is may be some delay and notice how sites go out of order because of different latency. But pinging a site so many times continously might be bad, lets fix this issue.

We will also fix above for loop with a stylistic fix, exactly same as above code.

````go
for l := range c { // waits for channel to return a val and assign to l
  go checkLink(l,c)
}
````

Time fix : Try :P

````go
for l := range c {
  time.Sleep(5 * time.Second) // This is wrong it blocks each channel by 5 sec, they are not lost but gets queued up !!
  go checkLink(l,c)
}
````

Actual fix using function literal. Attempt2 : why it keeps printing same website :P

````go
for l := range c {
  go func() {
    time.Sleep(5 * time.Second)
    go checkLink(l,c)
  }()
}
````

Complete Fixed and patched

````go
for l := range c {
  go func(link string) {
    time.Sleep(5 * time.Second)
    go checkLink(link,c)
  }(l) // always pass a copy of l to function literal, if not then l might changed by the time it gets picked up by checkLink(l,c) :P
}
````

