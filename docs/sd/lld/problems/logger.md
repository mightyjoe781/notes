# Logging Framework

Every programming language has some kind of logging framework. In an ideal scenario, you might wonder: _why do we even need a logger at all?_

Can’t you just run `print` or `cout` statements and direct the output to stdout or a file?

Of course you **can** do that, but a logging framework tries to **standardize and unify** how logs are produced and managed. For example, imagine you’ve imported a library that makes network calls. You don’t want to see every single detail that the library prints — that would be a disaster. The library might give you a switch to toggle some of that output, but it would still be very difficult to control the _level_ and _verbosity_ of the logs in a consistent way.

A logging framework solves this by introducing concepts like **log levels**, **appenders**, and **formatters**. These let you control verbosity, decide where logs go, and structure them for log-analysis tools — all without scattering arbitrary print statements throughout your code.

The following LLD problem involves designing a basic replica of these features.

## Requirements

- The logging framework should support different log levels, such as DEBUG, INFO, WARNING, ERROR, and FATAL.
- It should allow logging messages with a timestamp, log level, and message content.
- The framework should support multiple output destinations, such as console, file, and database.
- It should provide a configuration mechanism to set the log level and output destination.
- The logging framework should be thread-safe to handle concurrent logging from multiple threads.
- It should be extensible to accommodate new log levels and output destinations in the future.

## Classes

- From the intro text we can easily see that we need log levels which could be Enum Levels for this. And a `Message` class representing a log message
- Log Appenders could have multiple target sources, so we define Log Appenders as a interface with multiple implementation for each target. e.g. ConsoleAppenders, Database Appenders, File Appenders.
- Log Formatters could also be defined as a interface for different sources, but here We can make a concrete class with user passing message format or else it takes a default format.
- Usually Logging classes have a concept of root logger, where all the logs are ultimately transfers and other classes use their identity logger. The advantage of this is that maybe we wanna no send every log to database, it allows us to filter logs for different sources and helps in defining entire logging framework.

Good Video explaining Logging Module in `python` : https://www.youtube.com/watch?v=9L77QExPmI0

## Class Diagrams

- Following Data Models are Essential for describing the dataclasses involved in defining a log.

![](assets/Pasted%20image%2020251212220433.png)


![](assets/Pasted%20image%2020251212221244.png)

![](assets/Pasted%20image%2020251212221542.png)

Example Code : https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/loggingframework