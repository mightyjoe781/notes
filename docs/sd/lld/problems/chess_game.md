# Design Chess Game

## Requirements (Locked)

**In scope:**

- Console-based 2-player game, fully playable
- All basic chess rules: movement, capture, check detection
- Per-piece move logic (each piece knows its own valid moves)
- Turn management, input parsing, board display

**Out of scope (explicitly):**

- Castling, en passant, pawn promotion (nice-to-have, not required)
- Persistence, network/API layer
- Bot player (good-to-have)

**NFRs:** Modular, extensible, SOLID-compliant, running code.

---
## Class Decomposition

Three natural layers fall out of the problem:

**Models** - pure data, no game logic

```
Color (Enum): WHITE | BLACK
Position: row, col  ← value object, frozen
Piece (ABC): color, position, is_captured
  └── King, Queen, Rook, Bishop, Knight, Pawn
Board: 8×8 grid of Optional[Piece]
Player: name, color, pieces: list[Piece]
Move: from_pos, to_pos, piece, captured_piece | None
```

**Rules / Strategy layer** - the interesting design decisions

```
MoveValidator (Protocol)
  └── per-piece validators, or validation baked into Piece itself
CheckDetector: is_in_check(color, board) → bool
```

**Game orchestration**

```
Game (Context): board, player1, player2, current_turn, move_history
  - make_move(from, to)
  - switch_turn()
  - is_game_over() → bool
```

---

## Design Patterns

### 1. Strategy - per-piece move generation

Each piece needs different move logic. Two ways to model it:

**Option A - Method on Piece subclass** `piece.get_valid_moves(board) → list[Position]` Each subclass overrides. Simple, cohesive — the piece knows how it moves.

**Option B - External `MoveStrategy` per piece type** `KnightMoveStrategy.get_moves(piece, board)`. Follows SRP more strictly; easier to test strategies in isolation. More classes, more indirection.

For a chess LLD, **Option A is the standard choice** — move logic is intrinsic to the piece type and doesn't vary independently. Use Option B only if you need runtime-swappable move rules (e.g., custom chess variants).

### 2. Command Pattern - move history + undo

Every `make_move()` produces a `Move` object pushed onto a stack. `undo()` pops and reverses. This naturally gives you move history (required) and undo (nice-to-have) for free. Identical structure to the Text Editor problem.

### 3. State Pattern - game lifecycle

`GameState: IN_PROGRESS | CHECK | CHECKMATE | STALEMATE | DRAW`

`Game` holds `current_state: GameState`. After every move, `InProgressState` re-evaluates and transitions. Prevents moves being accepted after checkmate without if-else chains in `make_move()`. Same structure as the Tic-Tac-Toe problem.

### 4. Observer (optional) - event hooks

When a move is made, fire events: `OnCheck`, `OnCapture`, `OnGameOver`. Lets you attach a display layer or bot listener without coupling it to game logic. Useful if bot player is added later.

---

## The Hard Parts (worth noting before implementation)

**Check validation** is expensive naively - after every candidate move, simulate it, rebuild attack maps, check if own king is in check. You need `Board.clone()` for this.

**Pawn is the hardest piece** - moves forward, captures diagonally, different on first move (2 squares). Even without en passant it's the most conditional piece.

**Input parsing** - standard algebraic notation `e2 e4` or `e2-e4`. Parse to `Position(row, col)`. Validate before passing to game logic.

**Stalemate vs Checkmate** - both mean no legal moves; the difference is whether the king is currently in check. Must be distinguished correctly for game-over detection.
## Connection to HLD / Other Problems

The **Command + State** combination here is the same stack as Tic-Tac-Toe (State) and Text Editor (Command). Once you've internalised both, chess is just a harder instantiation of the same skeleton.

At HLD scale, a multiplayer chess platform adds: WebSocket for real-time moves (replacing the console loop), a `games` table keyed by `game_id`, and the `Move` command objects become the event log - same event sourcing pattern as noted in the Splitwise and Tic-Tac-Toe HLD connections.

Python Implementation [https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/chess](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/chess)