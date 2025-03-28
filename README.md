# 🐠 FlappyFish

A Flappy Bird-inspired game built with Python, featuring both a desktop version (Pygame) and a web version (Flask/JavaScript).

![FlappyFish Game](assets/screenshot.png)

## 🎮 Features

- Flappy Bird-inspired gameplay with an underwater twist
- Colorful fish character that jumps out of water to avoid obstacles
- Animated water surface with realistic waves
- Moving clouds in the background for visual depth
- Desktop application using Pygame
- Web version playable in any browser
- Simple, intuitive controls
- Score tracking

## 🔍 Game Preview

In FlappyFish, you control a small orange fish trying to navigate through a series of green pipes. The fish must jump out of the water and avoid both the pipes and falling back into the water. Each successfully passed pipe increases your score. The game features:

- Animated fish with flipping fins
- Dynamic wave movements
- Floating clouds that drift through the sky
- Increasing difficulty as you progress

## 🔧 Prerequisites

- Python 3.x
- pip (Python package manager)
- Web browser (for the web version)

## 📥 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/flappyfish.git
   cd flappyfish
   ```

2. Create and activate the virtual environment:
   ```bash
   python3 -m venv venv
   
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🎲 Desktop Version

### Running the Game

```bash
python main.py
```

### Controls

- **SPACE**: Jump/Flap
- **SPACE** (when game over): Restart
- Close window to quit

## 🌐 Web Version

### Running the Server

```bash
python app.py
```

Then open your browser and navigate to: `http://127.0.0.1:5000/`

### Controls

- **SPACE** or click "Start Game" button: Start game
- **SPACE**: Jump/Flap
- Click "Play Again" button or press **SPACE** after game over to restart

## 🎯 Game Mechanics

- The fish automatically falls due to gravity
- Press SPACE to make the fish jump upward
- Navigate through the pipes without hitting them
- Each successfully passed pipe adds 1 to your score
- The game ends if you hit a pipe or fall into the water
- Difficulty gradually increases with your score

## 📁 Project Structure

```
flappyfish/
├── main.py            # Desktop game (Pygame)
├── app.py             # Web server (Flask)
├── requirements.txt   # Project dependencies
├── README.md          # This file
├── LICENSE            # MIT License
├── assets/            # Game assets
├── static/            # Web assets
│   ├── css/           # Stylesheets
│   │   └── style.css  # Game styling
│   └── js/            # JavaScript files
│       └── game.js    # Web game logic
├── templates/         # HTML templates
│   └── index.html     # Game webpage
└── venv/              # Virtual environment
```

## 💻 Development

The game is built with:
- **Pygame** for the desktop version
- **Flask** for the web server
- **HTML5 Canvas** for the web game rendering
- **JavaScript** for the web game logic

### Code Architecture

- The game implements Object-Oriented Programming with classes for:
  - Fish (player character)
  - Pipes (obstacles)
  - Water surface (animated with waves)
  - Clouds (background elements)
- Both versions (Python and JavaScript) follow the same architecture

## 🚀 Deployment

### Web Version

To deploy the web version to a production server:

1. Set up a server with Python installed
2. Clone the repository and install dependencies
3. Use a WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```
4. Set up a reverse proxy with Nginx or Apache

## 🛠️ Future Improvements

- [ ] Add sound effects and background music
- [ ] Implement different difficulty levels
- [ ] Create mobile touch controls
- [ ] Add power-ups and collectible items
- [ ] Implement a high-score system
- [ ] Add different fish character options

## 🤝 Contributing

Contributions are welcome! Feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by the original Flappy Bird game
- Built as a learning project for Python game development
- Special thanks to the Python and JavaScript communities for their excellent documentation

## 📧 Contact

For questions or suggestions, please open an issue on this repository. 