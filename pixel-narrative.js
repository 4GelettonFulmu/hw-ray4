// Pixel Narrative Game - Main JavaScript

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game state
let gameState = {
    paused: false,
    timeSpeed: 1,
    pollutionEnabled: true,
    day: 1,
    time: 0,
    pollutionLevel: 0,
    mountainMood: 'Peaceful',
    clouds: [],
    cityLights: [],
    smokePuffs: [],
    noiseBursts: [],
    people: []
};

// Pixel size for chunky pixel art effect
const PIXEL_SIZE = 2;

// Color palette
const COLORS = {
    skyBlue: '#87CEEB',
    skyDark: '#4682B4',
    mountainGray: '#696969',
    mountainDark: '#404040',
    mountainSnow: '#FFFFFF',
    cityBuilding: '#2C3E50',
    cityWindow: '#F39C12',
    cityWindowOff: '#34495E',
    cloudWhite: '#FFFFFF',
    smokeGray: 'rgba(100, 100, 100, 0.3)',
    grassGreen: '#228B22',
    ground: '#8B7355'
};

// Helper function to draw a pixel block
function drawPixel(x, y, color, size = PIXEL_SIZE) {
    ctx.fillStyle = color;
    ctx.fillRect(Math.floor(x), Math.floor(y), size, size);
}

// Helper function to draw a rectangle with pixel style
function drawPixelRect(x, y, width, height, color) {
    ctx.fillStyle = color;
    ctx.fillRect(Math.floor(x), Math.floor(y), width, height);
}

// Cloud class
class Cloud {
    constructor(x, y, size) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.speed = 0.2 + Math.random() * 0.3;
    }

    update() {
        this.x -= this.speed * gameState.timeSpeed;
        if (this.x < -this.size * 20) {
            this.x = canvas.width + this.size * 10;
        }
    }

    draw() {
        const pixelSize = 4;
        ctx.fillStyle = COLORS.cloudWhite;

        // Draw cloud shape with pixel blocks
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (Math.random() > 0.3) {
                    const offsetX = (i - this.size / 2) * pixelSize;
                    const offsetY = (j - this.size / 2) * pixelSize;

                    // Create fluffy cloud shape
                    const distance = Math.sqrt(offsetX * offsetX + offsetY * offsetY);
                    if (distance < this.size * 2) {
                        drawPixel(this.x + offsetX, this.y + offsetY, COLORS.cloudWhite, pixelSize);
                    }
                }
            }
        }
    }
}

// Smoke puff class
class SmokePuff {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.vx = -0.5 + Math.random() * 1;
        this.vy = -0.5 - Math.random() * 1;
        this.life = 1.0;
        this.size = 2 + Math.random() * 3;
    }

    update() {
        this.x += this.vx * gameState.timeSpeed;
        this.y += this.vy * gameState.timeSpeed;
        this.life -= 0.01 * gameState.timeSpeed;
        this.vx *= 0.98;
        this.vy *= 0.98;
    }

    draw() {
        const alpha = this.life * 0.4;
        ctx.fillStyle = `rgba(100, 100, 100, ${alpha})`;

        // Draw pixelated smoke
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (Math.random() > 0.5) {
                    drawPixel(this.x + i * 3, this.y + j * 3, ctx.fillStyle, 3);
                }
            }
        }
    }

    isDead() {
        return this.life <= 0;
    }
}

// Noise burst class (visual representation of city noise)
class NoiseBurst {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.life = 1.0;
        this.radius = 5 + Math.random() * 10;
    }

    update() {
        this.life -= 0.05 * gameState.timeSpeed;
        this.radius += 0.5 * gameState.timeSpeed;
    }

    draw() {
        const alpha = this.life * 0.3;

        // Draw pixelated noise waves
        for (let angle = 0; angle < Math.PI * 2; angle += Math.PI / 4) {
            const x = this.x + Math.cos(angle) * this.radius;
            const y = this.y + Math.sin(angle) * this.radius;

            ctx.fillStyle = `rgba(255, 255, 0, ${alpha})`;
            drawPixel(x, y, ctx.fillStyle, 4);

            ctx.fillStyle = `rgba(255, 200, 0, ${alpha})`;
            drawPixel(x + 4, y, ctx.fillStyle, 4);
        }
    }

    isDead() {
        return this.life <= 0;
    }
}

// Person class for city inhabitants
class Person {
    constructor(x, y, buildingIndex) {
        this.x = x;
        this.y = y;
        this.buildingIndex = buildingIndex;
        this.direction = Math.random() > 0.5 ? 1 : -1;
        this.speed = 0.2 + Math.random() * 0.3;
        this.color = Math.random() > 0.5 ? '#FF6B6B' : '#4ECDC4';
    }

    update() {
        this.x += this.direction * this.speed * gameState.timeSpeed;

        // Keep within building bounds
        const buildingLeft = 600 + (this.buildingIndex % 3) * 70;
        const buildingRight = buildingLeft + 60;

        if (this.x <= buildingLeft || this.x >= buildingRight) {
            this.direction *= -1;
        }
    }

    draw() {
        // Draw pixel person (4x6 pixels)
        drawPixel(this.x, this.y, this.color, 4);     // Head
        drawPixel(this.x, this.y + 4, this.color, 4);  // Body
        drawPixel(this.x - 2, this.y + 4, this.color, 2); // Left arm
        drawPixel(this.x + 4, this.y + 4, this.color, 2); // Right arm
        drawPixel(this.x - 2, this.y + 8, this.color, 2); // Left leg
        drawPixel(this.x + 2, this.y + 8, this.color, 2); // Right leg
    }
}

// Initialize clouds
function initClouds() {
    gameState.clouds = [];
    for (let i = 0; i < 8; i++) {
        gameState.clouds.push(new Cloud(
            Math.random() * canvas.width,
            50 + Math.random() * 150,
            3 + Math.random() * 4
        ));
    }
}

// Initialize city elements
function initCity() {
    gameState.cityLights = [];
    gameState.people = [];

    // Create window lights pattern
    for (let building = 0; building < 3; building++) {
        for (let floor = 0; floor < 12; floor++) {
            for (let window = 0; window < 4; window++) {
                gameState.cityLights.push({
                    x: 610 + building * 70 + window * 12,
                    y: 480 - floor * 15,
                    on: Math.random() > 0.3,
                    flickerTimer: Math.random() * 100
                });
            }
        }
    }

    // Create people in the city
    for (let i = 0; i < 20; i++) {
        const buildingIndex = Math.floor(Math.random() * 3);
        gameState.people.push(new Person(
            620 + buildingIndex * 70,
            500 + Math.random() * 80,
            buildingIndex
        ));
    }
}

// Draw the mountain
function drawMountain() {
    const mountainLeft = 50;
    const mountainPeak = 150;
    const mountainRight = 350;
    const mountainBase = 500;

    // Mountain body - dark gray
    ctx.fillStyle = COLORS.mountainGray;
    ctx.beginPath();
    ctx.moveTo(mountainLeft, mountainBase);
    ctx.lineTo(mountainPeak, 100);
    ctx.lineTo(mountainRight, mountainBase);
    ctx.closePath();
    ctx.fill();

    // Mountain shadows (darker side)
    ctx.fillStyle = COLORS.mountainDark;
    ctx.beginPath();
    ctx.moveTo(mountainPeak, 100);
    ctx.lineTo(mountainRight, mountainBase);
    ctx.lineTo(mountainPeak + 50, mountainBase);
    ctx.closePath();
    ctx.fill();

    // Snow cap with pixel effect
    ctx.fillStyle = COLORS.mountainSnow;
    ctx.beginPath();
    ctx.moveTo(mountainPeak - 40, 180);
    ctx.lineTo(mountainPeak, 100);
    ctx.lineTo(mountainPeak + 40, 180);
    ctx.closePath();
    ctx.fill();

    // Add pixel detail to snow
    for (let i = 0; i < 30; i++) {
        const x = mountainPeak - 30 + Math.random() * 60;
        const y = 100 + Math.random() * 80;
        if (y < 180) {
            drawPixel(x, y, COLORS.mountainSnow, 2);
        }
    }

    // Mountain base/grass
    ctx.fillStyle = COLORS.grassGreen;
    ctx.fillRect(0, mountainBase, 400, canvas.height - mountainBase);
}

// Draw the city
function drawCity() {
    const cityBaseY = 500;

    // Ground for city
    ctx.fillStyle = COLORS.ground;
    ctx.fillRect(500, cityBaseY, canvas.width - 500, canvas.height - cityBaseY);

    // Draw buildings
    for (let i = 0; i < 3; i++) {
        const x = 600 + i * 70;
        const height = 180 + Math.random() * 100;
        const y = cityBaseY - height;

        // Building body
        drawPixelRect(x, y, 60, height, COLORS.cityBuilding);

        // Building outline
        ctx.strokeStyle = '#1a1a1a';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, 60, height);
    }

    // Draw windows
    gameState.cityLights.forEach(light => {
        light.flickerTimer += gameState.timeSpeed;
        if (light.flickerTimer > 100) {
            light.on = Math.random() > 0.2;
            light.flickerTimer = 0;
        }

        const color = light.on ? COLORS.cityWindow : COLORS.cityWindowOff;
        drawPixelRect(light.x, light.y, 8, 10, color);
    });

    // Draw people
    gameState.people.forEach(person => {
        person.update();
        person.draw();
    });
}

// Draw sky with gradient
function drawSky() {
    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height / 2);
    gradient.addColorStop(0, COLORS.skyBlue);
    gradient.addColorStop(1, COLORS.skyDark);

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height / 2);
}

// Main render function
function render() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw sky
    drawSky();

    // Draw and update clouds
    gameState.clouds.forEach(cloud => {
        cloud.update();
        cloud.draw();
    });

    // Draw mountain
    drawMountain();

    // Draw city
    drawCity();

    // Draw pollution effects
    if (gameState.pollutionEnabled) {
        // Generate smoke puffs
        if (Math.random() < 0.3 * gameState.timeSpeed) {
            const chimney = 650 + Math.floor(Math.random() * 3) * 70;
            gameState.smokePuffs.push(new SmokePuff(chimney, 320));
        }

        // Generate noise bursts
        if (Math.random() < 0.1 * gameState.timeSpeed) {
            const noiseX = 620 + Math.random() * 180;
            const noiseY = 450 + Math.random() * 50;
            gameState.noiseBursts.push(new NoiseBurst(noiseX, noiseY));
        }
    }

    // Update and draw smoke
    gameState.smokePuffs = gameState.smokePuffs.filter(puff => {
        puff.update();
        puff.draw();
        return !puff.isDead();
    });

    // Update and draw noise
    gameState.noiseBursts = gameState.noiseBursts.filter(burst => {
        burst.update();
        burst.draw();
        return !burst.isDead();
    });
}

// Update game state
function updateGameState() {
    if (gameState.paused) return;

    gameState.time += gameState.timeSpeed;

    // Update day counter
    if (gameState.time > 500) {
        gameState.day++;
        gameState.time = 0;
        updateNarrative();
    }

    // Update pollution level
    if (gameState.pollutionEnabled) {
        gameState.pollutionLevel = Math.min(100, gameState.pollutionLevel + 0.1 * gameState.timeSpeed);
    }

    // Update mountain mood based on pollution
    if (gameState.pollutionLevel < 20) {
        gameState.mountainMood = 'Peaceful';
    } else if (gameState.pollutionLevel < 50) {
        gameState.mountainMood = 'Concerned';
    } else if (gameState.pollutionLevel < 80) {
        gameState.mountainMood = 'Troubled';
    } else {
        gameState.mountainMood = 'Angry';
    }

    // Update UI
    document.getElementById('timeDisplay').textContent = `Day ${gameState.day}`;
    document.getElementById('pollutionDisplay').textContent = `${Math.floor(gameState.pollutionLevel)}%`;
    document.getElementById('mountainMoodDisplay').textContent = gameState.mountainMood;
}

// Narrative system
const narratives = {
    0: "The mountain has stood here for millennia, watching silently. The city is young, ambitious, growing.",
    5: "The city's lights grow brighter each night. Progress, they call it. The mountain remembers when the stars were visible.",
    10: "Smoke rises from the factories. The mountain's snow begins to show grey streaks. The people don't notice—they're too busy.",
    15: "The mountain feels the pollution settling on its ancient slopes. How quickly things change when humans are involved.",
    20: "The city never sleeps now. Noise echoes across the valley day and night. The mountain sighs, a sound like distant thunder.",
    30: "Is there a balance to be found? The mountain wonders. It has seen civilizations rise and fall, but never one so loud.",
    40: "The mountain grows restless. The pollution clouds obscure its peak. It remembers the clean air, the pure snow.",
    50: "A critical moment approaches. The mountain and the city cannot coexist like this forever. Something must give."
};

function updateNarrative() {
    const narrativeText = narratives[gameState.day] ||
        "The eternal dance continues: nature and civilization, ancient and modern, silence and noise.";

    document.getElementById('narrativeText').textContent = narrativeText;
}

// Game loop
function gameLoop() {
    updateGameState();
    render();
    requestAnimationFrame(gameLoop);
}

// Button controls
document.getElementById('btnPause').addEventListener('click', () => {
    gameState.paused = !gameState.paused;
    document.getElementById('btnPause').textContent = gameState.paused ? '▶️ Resume' : '⏸️ Pause';
});

document.getElementById('btnSpeedUp').addEventListener('click', () => {
    gameState.timeSpeed = Math.min(5, gameState.timeSpeed + 0.5);
});

document.getElementById('btnSlowDown').addEventListener('click', () => {
    gameState.timeSpeed = Math.max(0.5, gameState.timeSpeed - 0.5);
});

document.getElementById('btnTogglePollution').addEventListener('click', () => {
    gameState.pollutionEnabled = !gameState.pollutionEnabled;
    const btn = document.getElementById('btnTogglePollution');
    btn.textContent = gameState.pollutionEnabled ? '🏭 Disable Pollution' : '✨ Enable Pollution';
});

document.getElementById('btnReset').addEventListener('click', () => {
    gameState.day = 1;
    gameState.time = 0;
    gameState.pollutionLevel = 0;
    gameState.timeSpeed = 1;
    gameState.paused = false;
    gameState.pollutionEnabled = true;
    gameState.smokePuffs = [];
    gameState.noiseBursts = [];
    initClouds();
    initCity();
    updateNarrative();
    document.getElementById('btnPause').textContent = '⏸️ Pause';
    document.getElementById('btnTogglePollution').textContent = '🏭 Toggle Pollution';
});

// Initialize and start
initClouds();
initCity();
updateNarrative();
gameLoop();
