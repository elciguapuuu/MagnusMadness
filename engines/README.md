# MinMax Engine

This directory contains a custom chess engine implementation using the MinMax algorithm with Alpha-Beta pruning. The engine is designed to be compatible with the UCI (Universal Chess Interface) protocol, allowing it to be used with `lichess-bot`.

## Files

*   **`play_uci.py`**: The main entry point for the engine. It handles UCI communication, time management, and the search algorithm.
*   **`evaluation.py`**: Contains the static evaluation function used to assess board positions.

## Engine Details

### Search Algorithm (`play_uci.py`)

The engine uses **Iterative Deepening** combined with **Minimax** and **Alpha-Beta Pruning**.

*   **Iterative Deepening**: The engine searches to depth 1, then depth 2, and so on, until the allocated time runs out. This ensures that the engine always has a "best move" ready to play if time is cut short.
*   **Alpha-Beta Pruning**: This optimization reduces the number of nodes evaluated in the search tree by pruning branches that cannot possibly influence the final decision.
*   **Move Ordering**: To improve the efficiency of Alpha-Beta pruning, moves are ordered so that captures are examined first.

### Evaluation Function (`evaluation.py`)

The evaluation function determines the favorability of a given board position. It uses a combination of:

*   **Material Balance**: Standard values are assigned to pieces (Pawn: 100, Knight: 320, Bishop: 330, Rook: 500, Queen: 900).
*   **Piece-Square Tables (PST)**: Positional bonuses are added based on where pieces are located on the board. For example:
    *   **Pawns** are rewarded for advancing and controlling the center.
    *   **Knights** are valued higher in the center and penalized on the edges.
    *   **Rooks** are encouraged to occupy the 7th rank and open files.
    *   **Kings** are encouraged to stay safe in the castle during the middlegame.

The evaluation is calculated from White's perspective and mirrored for Black.

## Usage

To use this engine with `lichess-bot`, configure your `config.yml` to point to the `play_uci.py` script as the engine executable.

