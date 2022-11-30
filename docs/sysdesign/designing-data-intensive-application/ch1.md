## 1. Reliable, Scalable, and Maintainable Applications

- Many applications today are *data-intensive* rather than *compute-intensive*. CPU power rarely limits these application, bigger problems are usually 1. Amount of Data, 2. the complexity of data, 3. Rate at which data changes.
- A data intensive application is usually built from standard building blocks that commonly provide needed functionality e.g. *databases*, *caches*, *search indexes*, *stream processing*, *batch processing*.
- In real life scenario, each application has different requirements and we can’t simply utilise standard tools as a simple solution to those requirements.

### Thinking About Data Systems

- We think of *databases, queues, caches, etc* as being very different categories of tools. At core they maybe similar but can vary in terms of different performance characterstics and implementation. Yet we classify those tools under one umbrella *data systems*
- In recent years a lot of tools emerged to solve some specific problems and use cases and they don’t have a fine line of distinction in terms of use case. Ex : datastores that are also used as message queue (Redis), message queues with database reliability (Apache Kafka)
- Considering the demand of applications these days no one tool can be utilised to solve the problems, instead we use multiple tools together and just expose an API for entire system. You Sir technically have created a new, special purpose data system.
- There are many factors that affect design of a data system, but book will focus on 3 important factors.

### Reliability

- Expected Functioning, Fault Tolerant, Meets Load/Volume Performance Criteria, Prevent any unauthorized access and abuse.

- Reliable : Continues to work, even when things go wrong. (fault-tolerance mechanisms that prevent faults from causing failures) 
- Possibility of fault can’t be reduced to zero, so it becomes imperative to design a fault-tolerant system. See [Netflix Simian Army](https://netflixtechblog.com/the-netflix-simian-army-16e57fbab116)

#### Hardware Faults

- Hard disk have MTTF (mean time to failure) of about 10-50 yrs, so we can expect them to die randomly in a data center (contains 10k disks) everyday.
- Redundency is the one of solutions, e.g. RAID configs, dual power supplies, hot-swappable CPUs, and datacenters may have batteries and diesel for backup power. Basic Idea is to have a copy of resource that can take place in case of failure and can be backed up into a new system fairly quickly.
- One advantage is availability that comes from redundency and no downtime for upgrades (utilize rolling upgrades).

#### Software Errors

- Systematic Errors withing the system, and the worst part is its replicated across nodes and cause many more system failures than *uncorrelated hardware faults*
- Software faults could lie dormant for a long time until they are triggered by an unusual set of circumstances.Usually sofware is making some wrong assumption that is true most of times, except the one time it is false.
- There is no quick solution to problem of systematic faults in softwares. Lots of small things can help : think about assumptions and interactions in the system; thorough testing, process isolation; allowing process to crash and restart, measuring, monitoring, and analyzing system behavior in production.
- If system can poll itself for some output for some input then it can keep running and raise alerts in case of discrepancy.

#### Human Errors

- A major cause of outages is configuration error by operators while hardware faults(servers or network) played 10-25% of outages.
- Some ways to make systems 
  - Minimize opportunity for error. Well designed abstration, APIs and admin interfaces. However if the interfaces are too restrictive creative people try to find workaround it.
  - Decouple the places where people make most mistakes where they can cause failures
  - Test thoroughly at all levels, from unit tests to whole-system integration tests and manual tests.
  - Allow quick and easy recovery from human errors, to minimize impact of failure.
  - Set up detailed and clear monitoring, such as performance metrics and error rates (Telemetry)
  - Implement good management practices and training.

#### How important is Reliability ?

- In critical application reliability is most important.
- In “noncritical” application we have a responsibility to our users.
- We can trade reliability in order to reduce development cost(e.g., when developing a prototype product for an unproven market) or operation cost(narrow profit margin)

### Scalability