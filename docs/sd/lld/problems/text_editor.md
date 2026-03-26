# Design Text Editor

## Requirements

- **Type** - append text to the editor
- **Delete** - remove `n` characters from the end
- **Undo** - reverse the last operation

**Scope:** Pure service layer. No UI, no persistence, no networking. OOP and logical correctness are what's being graded here.

## Why the Naive Design Fails

The `TextEditor` class (Image 1) doing `type()`, `delete()`, and `undo()` all by itself violates two SOLID principles:

- **SRP** - the editor is simultaneously the data store _and_ the operation executor _and_ the history manager.
- **OCP** - adding a new operation (e.g., `replace`, `format`) means modifying the existing class, not extending it.

The `undo()` method is the real culprit: it forces the editor to know _how to reverse every operation it can perform_, which means it grows linearly with each new operation added.

![](assets/Pasted%20image%2020251127115013.png)

It violates SRP and OCP principles. Ideally it should be open for extension and closed for modification.

## Design: Command Pattern

The fix is to extract each operation into its own **Command** object that knows both how to _execute_ and how to _undo_ itself. The editor stays dumb - it just holds state and exposes primitive mutations.

![](assets/Pasted%20image%2020251127115247.png)

The `CommandManager` is the remote. The `TextEditor` is the TV. The remote never needs to know how the TV processes a channel change - it just sends the signal.


Use Cases

- Undo/Redo
- Queue/Schedule Operations
- Decouple the sender and receiver
- Macro Commands (combining commands)

[Behavioural Pattern](../behavioural_patterns.md) ~ Command Design Pattern.

![](assets/Pasted%20image%2020251127120000.png)

And we will have a Sender/Receiver Classes as well

### CommandManager


![](assets/Pasted%20image%2020251127120308.png)

The stack is the entire undo mechanism. `undo()` doesn't need a switch-case or if-else chain - it just pops the last command and calls _its_ `undo()`. Polymorphism does the dispatch.

## Concrete Commands

### TypeCommand

```java
class TypeCommand implements Command {
    private TextEditor editor;
    private String text;

    TypeCommand(TextEditor editor, String text) { ... }

    public void execute() { editor.type(text); }
    public void undo()    { editor.delete(text.length()); }
}
```

`undo()` just deletes exactly as many characters as were typed. This works because `type()` is an append-only operation - no need to snapshot the whole buffer.

### DeleteCommand

```java
class DeleteCommand implements Command {
    private TextEditor editor;
    private int length;
    private String deleted; // captured at execute() time

    public void execute() {
        deleted = editor.getLastN(length); // snapshot before deletion
        editor.delete(length);
    }
    public void undo() { editor.type(deleted); }
}
```

**Key insight:** `DeleteCommand` must capture the deleted text at `execute()` time, not at construction time. The text to be deleted isn't known until the command runs - so `deleted` is state that lives on the command object, not a constructor parameter.

## MacroCommand

Combines multiple commands into one atomic unit. Useful for "paste formatted text", "find-and-replace all", etc.

```java
class MacroCommand implements Command {
    private Command[] cmds;

    public void execute() {
        for (Command c : cmds) c.execute();
    }
    public void undo() {
        // Reverse order — last command undone first
        for (int i = cmds.length - 1; i >= 0; i--)
            cmds[i].undo();
    }
}
```

Undo iterates in reverse. This is not optional - if you `type("hello")` then `delete(3)`, undoing in forward order would try to re-type before restoring the delete.

## Use Cases Where This Pattern Pays Off

| Use Case                 | How the pattern helps                                |
| ------------------------ | ---------------------------------------------------- |
| Undo / Redo              | Stack of commands; redo needs a second stack         |
| Queue / Schedule         | Commands are objects - serialisable, deferrable      |
| Macro commands           | Compose commands without touching the editor         |
| Decouple sender/receiver | `CommandManager` never imports `TextEditor` directly |

## What's Not Covered Here (Intentionally)

- **Redo** - needs a second stack (`redoStack`). On `undo()`, push the popped command onto redo. On `execute()`, clear the redo stack.
- **Cursor position** - `delete(int length)` is simplified as "delete last N chars". A real editor tracks a cursor; delete semantics become more complex.
- **Persistence / serialisation** - commands as objects make this tractable, but it's out of scope.

---
## Python Supplement

```python
from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass, field


class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...


class TextEditor:
    def __init__(self) -> None:
        self._text = ""

    def type(self, text: str) -> None:
        self._text += text

    def delete(self, length: int) -> None:
        self._text = self._text[:-length] if length else self._text

    def get_last_n(self, n: int) -> str:
        return self._text[-n:] if n else ""

    @property
    def text(self) -> str:
        return self._text


@dataclass
class TypeCommand:
    editor: TextEditor
    text: str

    def execute(self) -> None:
        self.editor.type(self.text)

    def undo(self) -> None:
        self.editor.delete(len(self.text))


@dataclass
class DeleteCommand:
    editor: TextEditor
    length: int
    _deleted: str = field(default="", init=False, repr=False)
    # _deleted captured at execute() time, not __init__ — editor state unknown before then

    def execute(self) -> None:
        self._deleted = self.editor.get_last_n(self.length)
        self.editor.delete(self.length)

    def undo(self) -> None:
        self.editor.type(self._deleted)


@dataclass
class MacroCommand:
    commands: list[Command]

    def execute(self) -> None:
        for cmd in self.commands:
            cmd.execute()

    def undo(self) -> None:
        for cmd in reversed(self.commands):  # reverse order is mandatory
            cmd.undo()


class CommandManager:
    def __init__(self) -> None:
        self._history: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo(self) -> None:
        if self._history:
            self._history.pop().undo()


# --- Trickiest design decision: where does _deleted live? ---
# It MUST be instance state on DeleteCommand, not a constructor arg.
# Reason: the text to delete is only known at execute() time.
# If you pass it at construction, you've read editor state too early
# (the editor may have changed between construction and execution).

# Usage
editor = TextEditor()
mgr = CommandManager()

mgr.execute(TypeCommand(editor, "hello "))
mgr.execute(TypeCommand(editor, "world"))
print(editor.text)   # "hello world"

mgr.undo()
print(editor.text)   # "hello "

mgr.execute(DeleteCommand(editor, 3))
print(editor.text)   # "hel"

mgr.undo()
print(editor.text)   # "hello "

# Left as exercise: redo stack, cursor-aware delete, command serialisation
```

> `Protocol` is used instead of `ABC` because Command objects don't share any base behaviour - structural subtyping is the right fit. `dataclass` over plain `__init__` because all fields are data, no logic in construction.

---

## Further Reads & Exercises

### Directly Relevant

1. **"Design Patterns" - GoF, Chapter: Command** - the canonical reference; the intent and motivation section is worth reading verbatim.
2. **Refactoring.Guru - Command Pattern** - [https://refactoring.guru/design-patterns/command](https://refactoring.guru/design-patterns/command) - good diagrams, Python examples included.
3. **Python `typing.Protocol` docs** - [https://docs.python.org/3/library/typing.html#typing.Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol) - understand structural vs nominal subtyping before defaulting to ABC.
4. **"Fluent Python" 2nd ed., Ch. 13** - covers Protocol and duck typing in depth, directly relevant to how Command is best expressed in Python.
5. **"Clean Architecture" - Uncle Bob, Ch. 7 (SRP)** - good grounding for _why_ the naive TextEditor design fails.

### Exercises

**Easy** - Implement a `ReplaceCommand` that replaces a substring at a given index. What state does it need to capture at `execute()` time?

**Medium** - Add a redo stack to `CommandManager`. What should happen to the redo stack when a _new_ command is executed after an undo? (Hint: think about what git does when you commit after a reset.)

**Hard (no right answer)** - Where should the undo history limit live? Options: on `CommandManager` (cap the stack at N), on `TextEditor` (it decides its own history depth), or injected as a policy object. Argue both sides of CommandManager-owned vs policy-object approaches. What changes if the commands are also being persisted to a database?

### Related LLD Problems

| Problem                           | What transfers                                                                                                            |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Undo/Redo in a Drawing App**    | Identical Command pattern; the challenge shifts to how you snapshot graphical state (pixel buffer vs. vector ops).        |
| **Job/Task Scheduler**            | Commands as first-class objects that can be queued, delayed, or retried - the `executeCommand()` call just gets deferred. |
| **Transaction Manager (Banking)** | MacroCommand maps directly to a transaction: all-or-nothing execution, reverse-order rollback on failure.                 |

### Connection to HLD Problems

The Command pattern at the class level is a microcosm of the **event sourcing** pattern at the system level. In HLD, instead of a `history_stack` of command objects, you have an **event log** (Kafka, Kinesis) where every state change is stored as an immutable event. 

- Replay = re-execute all events. 
- Undo = compensating transaction. 

The mental model is identical - the unit of storage is an _operation_, not a _snapshot_.