# Flappy Mouse

A Flappy Bird clone built with Python and Pygame.

## Setup

1. Ensure you have Python 3.x installed
2. Activate the virtual environment:
   ```
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate     # On Windows
   ```
3. The game requires pygame, which is already installed in the virtual environment

## How to Play

1. Run the game:
   ```
   python main.py
   ```
2. Press SPACE to make the bird flap
3. Navigate through the pipes without hitting them
4. If you hit a pipe or the ground, the game ends
5. Press SPACE to restart after game over

## Controls

- SPACE: Flap/Restart
- Close window to quit

## Project Structure

- `main.py`: The main game file with all game logic
- `venv/`: Virtual environment with Python dependencies
- `assets/`: Directory for game assets (currently using simple shapes)

## Dependencies

- Python 3.x
- Pygame 