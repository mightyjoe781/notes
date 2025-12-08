# Tic-Tac-Toe

Tic-Tac-Toe is a famous 2 player game played on 3x3 board. Its deterministic game (easy to draw).

More on Game : https://en.wikipedia.org/wiki/Tic-tac-toe

## Design Requirements

Given Requirements

- The Tic-Tac-Toe game should be played on a 3x3 grid.
- Two players take turns marking their symbols (X or O) on the grid.
- The first player to get three of their symbols in a row (horizontally, vertically, or diagonally) wins the game.
- If all the cells on the grid are filled and no player has won, the game ends in a draw.
- The game should have a user interface to display the grid and allow players to make their moves
- The game should handle player turns and validate moves to ensure they are legal.
- The game should detect and announce the winner or a draw at the end of the game.

Solution Requirements

- Its enough to have simple Demo Class to showcase working of the program.

## Class Design

There are few things which are quite easy to model here, quite obvious.

- Board ~ Decomposed into Cells (from react tutorial i guess)
- Player

From Requirements we can draw few more functionality that is required.

- We need to maintain GameState which would help us understand whether Game has ended or not
- We need interface to display the state of the board at any point, and don't allow players to fill already filled Cells (prevent Invalid Moves)
- We need to check whether Game has ended or not, Check every state for potential end of game (Different Winning Strategies)
- Since we are going to use Demo class, we need a Game Class to hide complexity (Abstraction)

## Class Diagrams

![](assets/Pasted%20image%2020251207210625.png)

Above are the basic Classes which will serve as Model. We need a Context Class (Game) which will hide complexity of operating all technical stuff like handling draw/wins etc, validate player moves. Demo Class will call and use this context class.

![](assets/Pasted%20image%2020251207211942.png)

## Implementation Example

Link : https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/tictactoe

