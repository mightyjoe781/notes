
# CricBuzz Design

Assume that there are some providers in Stadium entering manually data/commentary, which is provided to CricBuzz GW and which needs to consumed by hundreds of services within CricBuzz.

You are tasked with Designing a solution for your ScoreBoard Service.

![](assets/Pasted%20image%2020251117222714.png)

- A Simple solution could be a pull based solution

![](assets/Pasted%20image%2020251117222747.png)

This wastes resources since consumers are continuously polling the source.

A direct improvement is to implement a new notification service which can send events to consumers saying them to consume the data.

![](assets/Pasted%20image%2020251117223307.png)

Example Code Snippets

```java
class CricketData {
    private LiveScoreBoard livescoreboard;
    private RunRateBoard runrateboard;
    private CommentaryBoard commentaryBoard;
    
    update() {
        this.livescoreboard.update(...);
        this.runrateboard.update(...);
        ....
    }
}
```

Above implementation has two big flaws (violates SOLID)

- OCP -> Addition of any new board will require modifying CricketData class.
- DIP -> all these classes could be represented using a simple polymorphic class & CricketData can depend on that abstraction.

![](assets/Pasted%20image%2020251117225232.png)

- This design seems to follow all the principles, yet there is an optimization we could do, since CricketEvent contains multiple data fields, we may not be interested in subscribing to every change, but some specific field.
- Some problem which could be asked, but not necessary
    - We don't have provision to have multiple producers
    - We don't have a provision to unsubscribe to the events

![](assets/Pasted%20image%2020251117230329.png)

- To solve multiple Producer we can modify sub class to maintain producer list in Subscriber class and create a Producer interface where multiple producers will be required to implement required methods

```java
// file - CommentaryBoardSub

CommentaryRepo _repo;
List<Producer> producers;

constructor(List<Producer> p) {
    this.producers = p;
    prod.subscribe(this);
}

update(CricketEvent ce) {
    prd.getCE.getCommentary()
    _repo.add(...)
}

```

