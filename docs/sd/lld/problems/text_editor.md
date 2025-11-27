# Design Text Editor

Requirements

- Type ~ Add text to our editor
- Undo ~ User can undo the last operation
- Delete ~ User can delete some text

Consideration :

- No need to take care of any UI
- Don't require any server, networking capabilities and storage db
- We need the kind of like just the service layer of app, we just need class implementation.

NOTE: We care about OOPs and Logical Correctness of the Editor

A simple design could be following but violates multiple SOLID principles

![](assets/Pasted%20image%2020251127115013.png)

It violates SRP and OCP principles. Ideally it should be open for extension and closed for modification.

![](assets/Pasted%20image%2020251127115247.png)

There could be multiple strategy to solve this problem, but due to Undo Functionality we want to use Command Design Pattern(similar to strategy).

Use Cases

- Undo/Redo
- Queue/Schedule Operations
- Decouple the sender and receiver
- Macro Commands (combining commands)

[Behavioural Pattern](../behavioural_patterns.md) ~ Command Design Pattern.

![](assets/Pasted%20image%2020251127120000.png)

And we will have a Sender/Receiver Classes as well

![](assets/Pasted%20image%2020251127120308.png)


So Exact Type Command Class would be 

```Java

class TypeCommand implements Command {
    private TextEditor editor;
    private String text;
    
    TypeCommand(...) {}
    public void execute() {
        editor.type(text);
    }
    public void undo(){}
}

```

Notice : How our editor is TV and remote is the Command Manager from above attached link text.

Example of Macro Commands

```Java

class MacroCommand implements Command {
    private Command[] cmd;
    MacroCommand() {...}
    public void execute() {
        for(Command c: cmd) c.execute();
    }
    public undo() {
        for(i = cmd.length - 1; i >= 0; i--)
            cmd[i].undo();    
    }
}
```