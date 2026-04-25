# Tic-Tac-Toe

Tic-Tac-Toe is a famous 2 player game played on 3x3 board. Its deterministic game (easy to draw).

More on Game : https://en.wikipedia.org/wiki/Tic-tac-toe

## Requirements

**Given:**

- 3×3 grid, 2 players alternating turns
- Win condition: three symbols in a row, column, or diagonal
- Draw condition: all cells filled, no winner
- Validate moves - no overwriting a filled cell
- Display the board at any point

**Scope:** Service layer + a Demo class to drive it. No UI framework, no persistence.

## Class Design Walkthrough

### Step 1

These fall out naturally from the problem statement:

**`SymbolEnum`** - `X | O | EMPTY`. Using an enum (not raw strings) means invalid symbols are impossible to construct. `EMPTY` is necessary as the default cell state.

**`Cell`** - just a wrapper around `SymbolEnum`. The reason to have `Cell` as its own class rather than a raw `SymbolEnum` in a grid: it gives you a place to hang display logic (`__str__`) and, in extension, position metadata (row, col) without polluting `Board`.

**`Player`** - holds `name: str` and `symbol: SymbolEnum`. Symbol is fixed at construction; it never changes mid-game.

**`Board`** - owns the 2D grid of `Cell` objects. Three responsibilities:

- `_init_board()` - fill grid with `EMPTY` cells
- `place_symbol(row, col, symbol)` - validates the target cell is `EMPTY` before writing; raises on invalid move
- `print_board()` - required by spec
- `moves_cnt: int` - tracks total moves made; used by draw detection (when `moves_cnt == size²`, board is full)

`Board` knowing `moves_cnt` is a deliberate choice - the alternative is scanning the full grid for empties each time, which is wasteful. Counter is O(1).

![](assets/Pasted%20image%2020251207210625.png)

### Step 2

The interesting work is in how the game loop is structured. Two patterns are layered here.

## Pattern 1: State Pattern (for game lifecycle)

Three terminal/transient states: `InProgressState`, `WinnerState`, `DrawState`.

All implement `GameState`:

`Game` (the context class) holds `state: GameState` and delegates every move through it:

```python
def make_move(self, row: int, col: int) -> None:
    self.state.handle_move(self.curr_player, row, col)
```

Why State pattern here? Because what `handle_move` _means_ changes depending on current game status:

- `InProgressState.handle_move` → place the symbol, check win/draw, transition state
- `WinnerState.handle_move` → reject move, game is over
- `DrawState.handle_move` → reject move, game is over

Without State, `make_move` has a chain of `if game_over: return` guards. With State, each state is responsible for its own behaviour - adding a new state (e.g., `PausedState`) doesn't touch existing code.

**State transitions live in `InProgressState`**, not in `Game`. This is the key insight. After placing a symbol, `InProgressState` calls `game.win_strategy.check_winner(...)` and sets `game.state` to either `WinnerState` or `DrawState` if the game ends. `Game` never directly writes to `game.state` from its own methods.

---

## Pattern 2: Strategy Pattern (for win detection)

Three concrete strategies: `RowWinningStrategy`, `ColumnWinningStrategy`, `DiagonalWinningStrategy`.

All implement `WinningStrategy`:

`Game` holds `win_strategy: WinningStrategy`. Why one strategy at a time rather than all three? Because the design stores a single injected strategy - if you want to check all three, you'd wrap them in a `CompositeWinningStrategy` (same MacroCommand idea from the Command notes). 

The standard full-game check runs all three anyway, so composition is the right extension point, not adding more fields to `Game`.

**Why Strategy and not just methods on `Board`?** Putting `check_row_win()`, `check_col_win()` on `Board` violates SRP - `Board` is a data container, not a game-rules engine. Strategies let you swap rule sets entirely (e.g., a 5-in-a-row variant) without touching `Board` or `Game`.

![](assets/Pasted%20image%2020251207211942.png)

## The `Game` Context Class (full picture)

```
<<Game>>  — Context Class
──────────────────────────────────
player1, player2: Player
board: Board
curr_player: Player
winner: Player | None

state: GameState          ← State pattern hook
win_strategy: WinningStrategy  ← Strategy pattern hook

switch_curr_player()      ← toggles between player1/player2
check_winner() → bool     ← delegates to win_strategy
make_move(row, col):
    self.state.handle_move(self.curr_player, row, col)
```

`Game` never does game logic directly. It's pure delegation. The Demo class calls `game.make_move(row, col)` in a loop and the two patterns handle everything else.
## What's Missing / Not Covered (Intentionally)

- **`CompositeWinningStrategy`** - to check row + col + diagonal in one call, wrap all three in a composite. Straightforward extension, left as exercise.
- **N×N board** - `Board.size` is already a field; `WinningStrategy` implementations need to loop to `size`, not hardcode 3. Parameterisation is trivial once the structure is right.
- **Input parsing / Demo class** - just a `while True` loop prompting for row/col, calling `game.make_move()`, and breaking on `WinnerState` or `DrawState`.
- **Undo** - not a requirement here. If it were, this design would need the Command pattern layered on top (see Text Editor notes).

---

## Python Supplement

```python
from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Protocol


class Symbol(Enum):
    X = auto()
    O = auto()
    EMPTY = auto()


@dataclass
class Cell:
    symbol: Symbol = Symbol.EMPTY

    def is_empty(self) -> bool:
        return self.symbol == Symbol.EMPTY

    def __str__(self) -> str:
        return self.symbol.name[0] if self.symbol != Symbol.EMPTY else "."


@dataclass
class Player:
    name: str
    symbol: Symbol  # fixed at construction, never mutated


@dataclass
class Board:
    size: int
    moves_cnt: int = field(default=0, init=False)
    grid: list[list[Cell]] = field(init=False)

    def __post_init__(self) -> None:
        self.grid = [[Cell() for _ in range(self.size)] for _ in range(self.size)]

    def place_symbol(self, row: int, col: int, symbol: Symbol) -> None:
        """Validates and writes; caller catches ValueError on illegal move."""
        if not self.grid[row][col].is_empty():
            raise ValueError(f"Cell ({row},{col}) is already occupied.")
        self.grid[row][col].symbol = symbol
        self.moves_cnt += 1

    @property
    def is_full(self) -> bool:
        return self.moves_cnt == self.size * self.size

    def print_board(self) -> None:
        for row in self.grid:
            print(" | ".join(str(c) for c in row))


# ── Winning Strategy ──────────────────────────────────────────────────────────

class WinningStrategy(Protocol):
    def check_winner(self, player: Player, board: Board) -> bool: ...


class RowWinningStrategy:
    def check_winner(self, player: Player, board: Board) -> bool:
        return any(
            all(cell.symbol == player.symbol for cell in row)
            for row in board.grid
        )


class ColumnWinningStrategy:
    def check_winner(self, player: Player, board: Board) -> bool:
        return any(
            all(board.grid[r][c].symbol == player.symbol for r in range(board.size))
            for c in range(board.size)
        )


class DiagonalWinningStrategy:
    def check_winner(self, player: Player, board: Board) -> bool:
        n = board.size
        main = all(board.grid[i][i].symbol == player.symbol for i in range(n))
        anti = all(board.grid[i][n - 1 - i].symbol == player.symbol for i in range(n))
        return main or anti


# ── State Pattern ─────────────────────────────────────────────────────────────

class GameState(Protocol):
    def handle_move(self, game: Game, player: Player, row: int, col: int) -> None: ...


class InProgressState:
    def handle_move(self, game: Game, player: Player, row: int, col: int) -> None:
        game.board.place_symbol(row, col, player.symbol)
        # State transition logic lives HERE, not in Game
        if any(s.check_winner(player, game.board) for s in game.win_strategies):
            game.winner = player
            game.state = WinnerState()
        elif game.board.is_full:
            game.state = DrawState()
        else:
            game.switch_curr_player()


class WinnerState:
    def handle_move(self, game: Game, player: Player, row: int, col: int) -> None:
        raise RuntimeError(f"Game over — {game.winner.name} has already won.")


class DrawState:
    def handle_move(self, game: Game, player: Player, row: int, col: int) -> None:
        raise RuntimeError("Game over — it's a draw.")


# ── Game (Context) ────────────────────────────────────────────────────────────

@dataclass
class Game:
    player1: Player
    player2: Player
    board: Board
    win_strategies: list[WinningStrategy]  # composite approach — check all
    curr_player: Player = field(init=False)
    winner: Player | None = field(default=None, init=False)
    state: GameState = field(init=False)

    def __post_init__(self) -> None:
        self.curr_player = self.player1
        self.state = InProgressState()

    def make_move(self, row: int, col: int) -> None:
        """Single public API for the Demo class."""
        self.state.handle_move(self, self.curr_player, row, col)

    def switch_curr_player(self) -> None:
        self.curr_player = (
            self.player2 if self.curr_player == self.player1 else self.player1
        )

# Left as exercise: Demo class game loop, CompositeWinningStrategy wrapper,
# n×n board support (strategies already parameterise on board.size).
```

**Trickiest design decision - where do state transitions live?**

They live in `InProgressState.handle_move`, not in `Game.make_move`. `Game` doesn't know _when_ a game ends - it only knows _that_ a move was requested. The current state decides what that move means. If transitions lived in `Game`, you'd need `if isinstance(self.state, InProgressState)` checks, which defeats the entire point of the State pattern.

**Why `list[WinningStrategy]` on `Game` instead of a single strategy?**  
The diagram shows a single `win_strategy` field, which is correct for the pure Strategy pattern. In practice, you need to check all three - so either inject a `CompositeWinningStrategy` (cleanest) or hold a list and iterate (simpler, shown here). Both are valid; the list version trades a bit of pattern purity for reduced boilerplate.

---

## Further Reads & Exercises

### Directly Relevant

1. **"Design Patterns" - GoF, Chapter: State** - the intent section is short and precise; read it alongside the diagram.
2. **"Design Patterns" - GoF, Chapter: Strategy** - note how Strategy and State look identical structurally; the difference is purely in _who_ triggers the transition.
3. **Refactoring.Guru - State Pattern** - [https://refactoring.guru/design-patterns/state](https://refactoring.guru/design-patterns/state) - good comparison of State vs Strategy at the bottom.
4. **Refactoring.Guru - Strategy Pattern** - [https://refactoring.guru/design-patterns/strategy](https://refactoring.guru/design-patterns/strategy)
5. **Python `enum.Enum` docs** - [https://docs.python.org/3/library/enum.html](https://docs.python.org/3/library/enum.html) - specifically `auto()` and how `__str__` customisation works on enums.

### Exercises

**Easy** - Extend to a 4×4 board. What changes? What stays the same? (Should be almost nothing if the design is correct.)

**Medium** - Implement `CompositeWinningStrategy` that wraps `[RowWinningStrategy, ColumnWinningStrategy, DiagonalWinningStrategy]` and checks all three. Then make `Game.win_strategies` a single `WinningStrategy` again. Does the Game class get simpler?

**Hard (no right answer)** - Where should the "announce winner" / "announce draw" output live? Options: in `WinnerState.handle_move` (state announces itself), in `Game.make_move` after delegation (context inspects state), or in the Demo class (caller checks `game.winner`). Each has different coupling tradeoffs. Argue which boundary is cleanest and what changes if you later want to support a web API response instead of a print statement.

### Related LLD Problems

|Problem|What transfers|
|---|---|
|**Chess / Checkers**|Same State pattern for game lifecycle (`InProgress`, `Check`, `Checkmate`); WinningStrategy becomes `MoveValidator` per piece type. The Game context class structure is nearly identical.|
|**Vending Machine**|State pattern in its purest form — `IdleState`, `HasMoneyState`, `DispensingState`. No Strategy layer, but the context-delegates-to-state structure is identical.|
|**ATM Machine**|State pattern again (`CardInsertedState`, `PINEnteredState`, `TransactionState`). Good follow-up after Vending Machine — more states, more transitions, same skeleton.|

### Connection to HLD Problems

The State pattern maps directly to **finite state machines** in distributed systems design. In HLD, an order lifecycle (`PLACED → CONFIRMED → SHIPPED → DELIVERED → RETURNED`) is exactly this - each state defines what transitions are legal, and the order service is the context class. The difference is that in HLD, state transitions need to be persisted (usually as a status column + event log) and may be triggered by async events (webhooks, queues) rather than synchronous method calls. The class design here is the local, in-memory version of that same model.

The Strategy pattern maps to **pluggable rule engines** in HLD - pricing engines, fraud detection systems, recommendation algorithms. The pattern is identical: a context holds a reference to a strategy interface, and the concrete implementation is injected (or selected at runtime based on feature flags / tenant config).

Link : https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/tictactoe

