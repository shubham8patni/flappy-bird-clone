document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const canvas = document.getElementById('game-canvas');
    const ctx = canvas.getContext('2d');
    const startScreen = document.getElementById('start-screen');
    const gameOverScreen = document.getElementById('game-over-screen');
    const startButton = document.getElementById('start-button');
    const restartButton = document.getElementById('restart-button');
    const scoreDisplay = document.getElementById('score');
    const finalScore = document.getElementById('final-score');

    // Game constants
    const WIDTH = canvas.width;
    const HEIGHT = canvas.height;
    const GRAVITY = 0.25;
    const FLAP_STRENGTH = -7;
    const PIPE_SPEED = 3;
    const PIPE_GAP = 150;
    const PIPE_FREQUENCY = 1800; // milliseconds
    const WATER_HEIGHT = 100;

    // Colors
    const COLORS = {
        SKY_BLUE: '#87CEEB',
        GREEN: '#008800',
        WATER_BLUE: '#40A4DF',
        FISH_ORANGE: '#FF8C00',
        WHITE: '#FFFFFF',
        BLACK: '#000000',
        CLOUD_WHITE: '#F0F0F0'
    };

    // Game variables
    let fish;
    let pipes = [];
    let clouds = [];
    let water;
    let score = 0;
    let gameActive = false;
    let lastPipe = 0;
    let lastCloud = 0;
    let animationFrame;
    let lastTime = 0;

    // Fish class
    class Fish {
        constructor() {
            this.x = 100;
            this.y = HEIGHT / 2;
            this.velocity = 0;
            this.width = 40;
            this.height = 25;
            this.flip = false;
            this.flipTimer = 0;
        }

        update() {
            // Apply gravity
            this.velocity += GRAVITY;
            this.y += this.velocity;

            // Keep fish on screen (top only)
            if (this.y <= 0) {
                this.y = 0;
                this.velocity = 0;
            }
            
            // Fish animation
            this.flipTimer++;
            if (this.flipTimer > 10) {
                this.flip = !this.flip;
                this.flipTimer = 0;
            }
        }

        flap() {
            this.velocity = FLAP_STRENGTH;
            this.flip = !this.flip;
        }

        draw() {
            // Draw fish body
            ctx.fillStyle = COLORS.FISH_ORANGE;
            ctx.beginPath();
            ctx.ellipse(this.x + this.width/2, this.y + this.height/2, this.width/2, this.height/2, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Draw tail
            ctx.beginPath();
            ctx.moveTo(this.x, this.y + this.height/2);
            ctx.lineTo(this.x - 15, this.y + this.height/4);
            ctx.lineTo(this.x - 15, this.y + 3*this.height/4);
            ctx.closePath();
            ctx.fill();
            
            // Draw eye
            ctx.fillStyle = COLORS.WHITE;
            ctx.beginPath();
            ctx.arc(this.x + this.width - 10, this.y + this.height/3, 5, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.fillStyle = COLORS.BLACK;
            ctx.beginPath();
            ctx.arc(this.x + this.width - 10, this.y + this.height/3, 2, 0, Math.PI * 2);
            ctx.fill();
            
            // Draw fin
            const finHeight = this.flip ? 8 : -8;
            ctx.fillStyle = COLORS.FISH_ORANGE;
            ctx.beginPath();
            ctx.moveTo(this.x + this.width/3, this.y);
            ctx.lineTo(this.x + this.width/2, this.y - finHeight);
            ctx.lineTo(this.x + 2*this.width/3, this.y);
            ctx.closePath();
            ctx.fill();
        }

        getBounds() {
            return {
                x: this.x,
                y: this.y,
                width: this.width,
                height: this.height
            };
        }
    }

    // Cloud class
    class Cloud {
        constructor() {
            this.x = WIDTH + random(10, 100);
            this.y = random(50, 200);
            this.width = random(60, 120);
            this.height = random(30, 50);
            this.speed = random(0.5, 1.5);
        }

        update() {
            this.x -= this.speed;
        }

        draw() {
            ctx.fillStyle = COLORS.CLOUD_WHITE;
            const radius = this.height / 2;
            const centers = [
                { x: this.x, y: this.y },
                { x: this.x + radius, y: this.y - radius/2 },
                { x: this.x + radius*2, y: this.y },
                { x: this.x + radius/2, y: this.y + radius/3 },
                { x: this.x + radius*1.5, y: this.y + radius/3 }
            ];
            
            centers.forEach(center => {
                ctx.beginPath();
                ctx.arc(center.x, center.y, radius, 0, Math.PI * 2);
                ctx.fill();
            });
        }
    }

    // Water surface class
    class WaterSurface {
        constructor() {
            this.height = WATER_HEIGHT;
            this.waveOffset = 0;
            this.wavePoints = [];
            this.updateWavePoints();
        }

        update() {
            this.waveOffset += 0.1;
            if (this.waveOffset > 10) {
                this.waveOffset = 0;
            }
            this.updateWavePoints();
        }

        updateWavePoints() {
            this.wavePoints = [];
            for (let x = 0; x <= WIDTH + 10; x += 10) {
                const y = HEIGHT - this.height + Math.sin(x/50 + this.waveOffset) * 5;
                this.wavePoints.push({x, y});
            }
        }

        draw() {
            // Draw water with waves
            ctx.fillStyle = COLORS.WATER_BLUE;
            ctx.beginPath();
            ctx.moveTo(this.wavePoints[0].x, this.wavePoints[0].y);
            
            this.wavePoints.forEach(point => {
                ctx.lineTo(point.x, point.y);
            });
            
            // Complete the shape
            ctx.lineTo(WIDTH, HEIGHT);
            ctx.lineTo(0, HEIGHT);
            ctx.closePath();
            ctx.fill();
            
            // Add water highlights
            ctx.fillStyle = 'rgba(100, 200, 255, 0.3)';
            for (let x = 20; x < WIDTH; x += 80) {
                const y = HEIGHT - this.height + 20;
                ctx.beginPath();
                ctx.ellipse(x + 20, y, 20, 5, 0, 0, Math.PI * 2);
                ctx.fill();
            }
        }
    }

    // Pipe class
    class Pipe {
        constructor() {
            this.x = WIDTH;
            this.height = random(100, 400);
            this.width = 60;
            this.passed = false;
        }

        update() {
            this.x -= PIPE_SPEED;
        }

        draw() {
            ctx.fillStyle = COLORS.GREEN;
            
            // Top pipe
            ctx.fillRect(this.x, 0, this.width, this.height);
            
            // Top pipe cap
            ctx.fillRect(this.x - 5, this.height - 20, this.width + 10, 20);
            
            // Bottom pipe
            ctx.fillRect(this.x, this.height + PIPE_GAP, this.width, HEIGHT);
            
            // Bottom pipe cap
            ctx.fillRect(this.x - 5, this.height + PIPE_GAP, this.width + 10, 20);
        }

        collide(fish) {
            const fishBounds = fish.getBounds();
            
            // Check collision with top pipe
            if (
                fishBounds.x + fishBounds.width > this.x &&
                fishBounds.x < this.x + this.width &&
                fishBounds.y < this.height
            ) {
                return true;
            }
            
            // Check collision with bottom pipe
            if (
                fishBounds.x + fishBounds.width > this.x &&
                fishBounds.x < this.x + this.width &&
                fishBounds.y + fishBounds.height > this.height + PIPE_GAP
            ) {
                return true;
            }
            
            return false;
        }
    }

    // Helper function for random number generation
    function random(min, max) {
        return Math.random() * (max - min) + min;
    }

    // Game functions
    function resetGame() {
        fish = new Fish();
        pipes = [];
        clouds = [];
        water = new WaterSurface();
        
        // Create initial clouds
        for (let i = 0; i < 3; i++) {
            clouds.push(new Cloud());
        }
        
        score = 0;
        gameActive = true;
        lastPipe = 0;
        lastCloud = 0;
        scoreDisplay.textContent = score;
        gameOverScreen.classList.add('hidden');
    }

    function gameOver() {
        gameActive = false;
        finalScore.textContent = `Score: ${score}`;
        gameOverScreen.classList.remove('hidden');
        cancelAnimationFrame(animationFrame);
    }

    function generatePipes(currentTime) {
        if (currentTime - lastPipe > PIPE_FREQUENCY) {
            pipes.push(new Pipe());
            lastPipe = currentTime;
        }
    }
    
    function generateClouds(currentTime) {
        if (currentTime - lastCloud > 3000) {  // Every 3 seconds
            if (Math.random() < 0.5) {  // 50% chance
                clouds.push(new Cloud());
            }
            lastCloud = currentTime;
        }
    }

    function update(currentTime) {
        const deltaTime = currentTime - lastTime;
        lastTime = currentTime;

        if (!gameActive) return;
        
        // Clear canvas
        ctx.fillStyle = COLORS.SKY_BLUE;
        ctx.fillRect(0, 0, WIDTH, HEIGHT);
        
        // Update fish
        fish.update();
        
        // Update water
        water.update();
        
        // Generate pipes
        generatePipes(currentTime);
        
        // Generate clouds
        generateClouds(currentTime);
        
        // Update clouds
        clouds.forEach((cloud, index) => {
            cloud.update();
            cloud.draw();
            
            // Remove clouds that are off-screen
            if (cloud.x + cloud.width < 0) {
                clouds.splice(index, 1);
            }
        });
        
        // Update pipes and check collisions
        pipes.forEach((pipe, index) => {
            pipe.update();
            pipe.draw();
            
            // Check collision
            if (pipe.collide(fish)) {
                gameOver();
            }
            
            // Check if fish passed the pipe
            if (!pipe.passed && pipe.x + pipe.width < fish.x) {
                pipe.passed = true;
                score++;
                scoreDisplay.textContent = score;
            }
            
            // Remove pipes that are off-screen
            if (pipe.x + pipe.width < 0) {
                pipes.splice(index, 1);
            }
        });
        
        // Check if fish hits the water
        if (fish.y + fish.height >= HEIGHT - WATER_HEIGHT) {
            gameOver();
        }
        
        // Draw water
        water.draw();
        
        // Draw fish
        fish.draw();
        
        // Continue animation
        if (gameActive) {
            animationFrame = requestAnimationFrame(update);
        }
    }

    function startGame() {
        resetGame();
        startScreen.classList.add('hidden');
        animationFrame = requestAnimationFrame(update);
    }

    // Event listeners
    startButton.addEventListener('click', startGame);
    restartButton.addEventListener('click', startGame);
    
    document.addEventListener('keydown', function(event) {
        if (event.code === 'Space') {
            event.preventDefault();
            if (gameActive) {
                fish.flap();
            } else if (gameOverScreen.classList.contains('hidden') && startScreen.classList.contains('hidden')) {
                startGame();
            }
        }
    });

    // Initial setup
    ctx.fillStyle = COLORS.SKY_BLUE;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    
    // Draw initial water
    water = new WaterSurface();
    water.draw();
}); 