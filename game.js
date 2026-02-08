const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const WINDOW_WIDTH = 800;
const WINDOW_HEIGHT = 600;
const HUD_HEIGHT = 50;
const CELL_SIZE = 20;
const GRID_WIDTH = WINDOW_WIDTH / CELL_SIZE;
const GRID_HEIGHT = (WINDOW_HEIGHT - HUD_HEIGHT) / CELL_SIZE;
const SNAKE_SPEED = 150;

const BLACK = '#0a0a0f';
const WHITE = '#f5f5fa';
const DARK_GREEN = '#147828';
const LIGHT_GREEN = '#50dc8a';
const RED = '#ff5050';
const DARK_RED = '#b41e1e';
const GOLD = '#ffd700';
const GRAY = '#64646e';

let snake = [];
let direction = { x: 1, y: 0 };
let nextDirection = { x: 1, y: 0 };
let food = { x: 0, y: 0 };
let score = 0;
let highScore = 0;
let gameOver = false;
let gameLoop = null;
let gameState = 'START';

function init() {
    canvas.width = WINDOW_WIDTH;
    canvas.height = WINDOW_HEIGHT - HUD_HEIGHT;
    resetGame();
    draw();
    document.addEventListener('keydown', handleKeyPress);
}

function resetGame() {
    snake = [
        { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) }
    ];
    direction = { x: 1, y: 0 };
    nextDirection = { x: 1, y: 0 };
    food = generateFood();
    score = 0;
    gameOver = false;
    updateScore();
}

function generateFood() {
    let newFood;
    do {
        newFood = {
            x: Math.floor(Math.random() * GRID_WIDTH),
            y: Math.floor(Math.random() * GRID_HEIGHT)
        };
    } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
    return newFood;
}

function draw() {
    ctx.fillStyle = BLACK;
    ctx.fillRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT - HUD_HEIGHT);

    drawGrid();
    drawSnake();
    drawFood();

    if (gameState === 'START') {
        showStartScreen();
    } else if (gameState === 'PLAYING' && gameOver) {
        showGameOverScreen();
    }
}

function drawGrid() {
    ctx.strokeStyle = '#14141a';
    ctx.lineWidth = 1;

    for (let x = 0; x <= WINDOW_WIDTH; x += CELL_SIZE) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, WINDOW_HEIGHT - HUD_HEIGHT);
        ctx.stroke();
    }

    for (let y = 0; y <= WINDOW_HEIGHT - HUD_HEIGHT; y += CELL_SIZE) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(WINDOW_WIDTH, y);
        ctx.stroke();
    }
}

function drawSnake() {
    snake.forEach((segment, index) => {
        const x = segment.x * CELL_SIZE;
        const y = segment.y * CELL_SIZE;

        if (index === 0) {
            drawSnakeHead(x, y);
        } else {
            drawSnakeBody(x, y, index);
        }
    });
}

function drawSnakeHead(x, y) {
    ctx.fillStyle = LIGHT_GREEN;
    ctx.beginPath();
    ctx.roundRect(x, y, CELL_SIZE, CELL_SIZE, 5);
    ctx.fill();

    ctx.strokeStyle = WHITE;
    ctx.lineWidth = 2;
    ctx.stroke();

    const eyeSize = 6;
    const pupilSize = 3;
    const eyeOffset = 5;

    let leftEye, rightEye;
    if (direction.x === 1) {
        leftEye = { x: x + CELL_SIZE - eyeOffset - 3, y: y + eyeOffset };
        rightEye = { x: x + CELL_SIZE - eyeOffset - 3, y: y + CELL_SIZE - eyeOffset };
    } else if (direction.x === -1) {
        leftEye = { x: x + eyeOffset + 3, y: y + eyeOffset };
        rightEye = { x: x + eyeOffset + 3, y: y + CELL_SIZE - eyeOffset };
    } else if (direction.y === -1) {
        leftEye = { x: x + eyeOffset, y: y + eyeOffset + 3 };
        rightEye = { x: x + CELL_SIZE - eyeOffset, y: y + eyeOffset + 3 };
    } else {
        leftEye = { x: x + eyeOffset, y: y + CELL_SIZE - eyeOffset - 3 };
        rightEye = { x: x + CELL_SIZE - eyeOffset, y: y + CELL_SIZE - eyeOffset - 3 };
    }

    ctx.fillStyle = WHITE;
    ctx.beginPath();
    ctx.arc(leftEye.x, leftEye.y, eyeSize, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(rightEye.x, rightEye.y, eyeSize, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = BLACK;
    ctx.beginPath();
    ctx.arc(leftEye.x, leftEye.y, pupilSize, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(rightEye.x, rightEye.y, pupilSize, 0, Math.PI * 2);
    ctx.fill();
}

function drawSnakeBody(x, y, index) {
    const colorIntensity = Math.max(60, 160 - index * 5);
    const color = `rgb(30, ${Math.min(220, colorIntensity + 70)}, 50)`;

    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x, y, CELL_SIZE, CELL_SIZE, 3);
    ctx.fill();

    ctx.strokeStyle = DARK_GREEN;
    ctx.lineWidth = 1;
    ctx.stroke();
}

function drawFood() {
    const x = food.x * CELL_SIZE;
    const y = food.y * CELL_SIZE;
    const centerX = x + CELL_SIZE / 2;
    const centerY = y + CELL_SIZE / 2;
    const radius = CELL_SIZE / 2 - 1;

    ctx.fillStyle = RED;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    ctx.fill();

    ctx.strokeStyle = DARK_RED;
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.fillStyle = '#ffb4b4';
    ctx.beginPath();
    ctx.arc(centerX - 4, centerY - 4, 3, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#ffdcdc';
    ctx.beginPath();
    ctx.arc(centerX - 3, centerY - 3, 2, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#32b432';
    ctx.beginPath();
    ctx.ellipse(centerX, y + 2, 4, 3, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.strokeStyle = '#1e8c30';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(centerX, y + 3);
    ctx.lineTo(centerX, y + 6);
    ctx.stroke();
}

function update() {
    if (gameState !== 'PLAYING' || gameOver) return;

    direction = { ...nextDirection };

    const head = {
        x: snake[0].x + direction.x,
        y: snake[0].y + direction.y
    };

    if (checkCollision(head)) {
        gameOver = true;
        showGameOverScreen();
        return;
    }

    snake.unshift(head);

    if (head.x === food.x && head.y === food.y) {
        score++;
        updateScore();
        food = generateFood();
    } else {
        snake.pop();
    }

    draw();
}

function checkCollision(head) {
    if (head.x < 0 || head.x >= GRID_WIDTH ||
        head.y < 0 || head.y >= GRID_HEIGHT) {
        return true;
    }

    return snake.some(segment => segment.x === head.x && segment.y === head.y);
}

function updateScore() {
    document.getElementById('score').textContent = score;

    if (score > highScore) {
        highScore = score;
        document.getElementById('high-score').textContent = highScore;
    }
}

function showStartScreen() {
    document.getElementById('startScreen').classList.remove('hidden');
    document.getElementById('gameOverScreen').classList.add('hidden');
}

function showGameOverScreen() {
    document.getElementById('startScreen').classList.add('hidden');
    document.getElementById('gameOverScreen').classList.remove('hidden');
    document.getElementById('final-score').textContent = score;

    if (score > highScore) {
        highScore = score;
        document.getElementById('high-score').textContent = highScore;
        document.getElementById('newRecord').classList.remove('hidden');
    } else {
        document.getElementById('newRecord').classList.add('hidden');
    }
}

function startGame() {
    gameState = 'PLAYING';
    document.getElementById('startScreen').classList.add('hidden');
    document.getElementById('gameOverScreen').classList.add('hidden');
    resetGame();

    if (gameLoop) clearInterval(gameLoop);
    gameLoop = setInterval(update, SNAKE_SPEED);
}

function handleKeyPress(event) {
    if (gameState === 'START') {
        startGame();
        return;
    }

    if (gameState === 'PLAYING' && !gameOver) {
        switch (event.key) {
            case 'ArrowUp':
                if (direction.y !== 1) nextDirection = { x: 0, y: -1 };
                break;
            case 'ArrowDown':
                if (direction.y !== -1) nextDirection = { x: 0, y: 1 };
                break;
            case 'ArrowLeft':
                if (direction.x !== 1) nextDirection = { x: -1, y: 0 };
                break;
            case 'ArrowRight':
                if (direction.x !== -1) nextDirection = { x: 1, y: 0 };
                break;
        }
    }

    if (gameState === 'PLAYING' && gameOver) {
        if (event.key === ' ') {
            startGame();
        } else if (event.key === 'Escape') {
            gameState = 'START';
            if (gameLoop) clearInterval(gameLoop);
            showStartScreen();
        }
    }
}

init();
