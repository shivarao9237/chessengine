# Chess AI Project

This project implements a basic Chess AI capable of playing a game of chess against a human or another AI. It includes functionality for move generation, evaluation, and decision-making using a simple minimax approach with material scoring.

## Features

1. **Game Mechanics:**
   - A functional chessboard and pieces represented in an 8x8 array.
   - Standard chess rules implemented, including castling, en passant, pawn promotion, and checkmate/stalemate conditions.

2. **Move Generation:**
   - Generates all possible valid moves for each piece.
   - Ensures moves adhere to the rules of chess, including preventing moves that leave the king in check.

3. **AI Decision-Making:**
   - Uses a minimax-inspired algorithm to select the best move.
   - Evaluates board states based on material score, considering each piece's value.

4. **Random Move Selection:**
   - Includes a simple random move generator for testing purposes.

## How It Works

### Board Representation
The board is represented as an 8x8 array, where each square contains:
- `--` for empty squares.
- `wP`, `bP` for white and black pawns, respectively.
- `wK`, `bK` for white and black kings, respectively.
- Similarly for other pieces: `R` (Rook), `N` (Knight), `B` (Bishop), and `Q` (Queen).

### Classes and Functions

#### `GameState` Class
Manages the game state, including:
- Board setup and updates.
- Move history and undo functionality.
- Valid move generation and special rules handling.

#### Move Evaluation
The AI evaluates moves based on:
- **Material Score:** Calculates the total value of all pieces on the board using a predefined scoring system:
  - King: 0
  - Queen: 9
  - Rook: 5
  - Bishop: 3
  - Knight: 3
  - Pawn: 1
- **Minimax Search:** Simulates future moves to find the optimal move for the current player.

### Special Features
- **Castling:** Checks and executes castling moves if allowed.
- **En Passant:** Handles the en passant rule for pawns.
- **Pawn Promotion:** Automatically promotes pawns to queens upon reaching the last rank.
- **Checkmate and Stalemate Detection:** Determines when the game is over.

## Getting Started

### Prerequisites
- Python 3.x

### Running the Program
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chess-ai.git
   cd chess-ai
   ```
2. Run the main script:
   ```bash
   python chess_ai.py
   ```

### Customization
- Modify the `piecescore` dictionary to change the evaluation weights of different pieces.
- Adjust the AI logic in the `findbestmove` function to experiment with other evaluation strategies or search depths.

## Future Enhancements
- Implement a graphical user interface (GUI) for better user interaction.
- Add support for advanced AI algorithms like Alpha-Beta Pruning or Machine Learning.
- Improve move evaluation with positional scoring.
- Add configurable difficulty levels for the AI.

## Contribution
Contributions are welcome! Feel free to open issues or submit pull requests to enhance the project.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Inspiration from various chess AI tutorials and resources.
- OpenAI for providing support and guidance in creating this project.

