// Pixel Narrative Game - Enhanced with Mountain Abilities

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
    noiseLevel: 0,
    fearLevel: 0,
    population: 100,
    mountainHealth: 100,
    mountainMood: 'Peaceful',
    clouds: [],
    cityLights: [],
    smokePuffs: [],
    noiseBursts: [],
    people: [],
    trees: [],
    buildings: [],
    growthPixels: [],
    snowPixels: [],
    blizzardParticles: [],

    // Active effects
    windActive: false,
    windTimer: 0,
    earthquakeActive: false,
    earthquakeTimer: 0,
    blizzardActive: false,
    blizzardTimer: 0,
    blizzardIntensity: 0,
    avalancheActive: false,
    avalancheTimer: 0,
    screenShake: { x: 0, y: 0 },

    // Ability cooldowns
    windCooldown: 0,
    earthquakeCooldown: 0,
    blizzardCooldown: 0,
    growthCooldown: 0
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
    mountainSnowDirty: '#C0C0C0',
    cityBuilding: '#2C3E50',
    cityWindow: '#F39C12',
    cityWindowOff: '#34495E',
    cityWindowBlue: '#4DB8FF',
    cloudWhite: '#FFFFFF',
    smokeGray: 'rgba(128, 64, 128, 0.4)', // Purple smoke
    grassGreen: '#228B22',
    grassDead: '#8B7355',
    ground: '#8B7355',
    treeGreen: '#2F4F2F',
    treeDead: '#6B5D4F'
};

// Helper function to draw a pixel block
function drawPixel(x, y, color, size = PIXEL_SIZE) {
    ctx.fillStyle = color;
    ctx.fillRect(Math.floor(x + gameState.screenShake.x), Math.floor(y + gameState.screenShake.y), size, size);
}

// Helper function to draw a rectangle with pixel style
function drawPixelRect(x, y, width, height, color) {
    ctx.fillStyle = color;
    ctx.fillRect(
        Math.floor(x + gameState.screenShake.x),
        Math.floor(y + gameState.screenShake.y),
        width,
        height
    );
}

// Cloud class
class Cloud {
    constructor(x, y, size) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.baseSpeed = 0.2 + Math.random() * 0.3;
        this.trail = [];
    }

    update() {
        const speedMultiplier = gameState.windActive ? 3 : 1;
        const speed = this.baseSpeed * speedMultiplier * gameState.timeSpeed;

        // Store trail positions during wind
        if (gameState.windActive && Math.random() < 0.3) {
            this.trail.push({ x: this.x, y: this.y, life: 1.0 });
        }

        this.x -= speed;
        if (this.x < -this.size * 20) {
            this.x = canvas.width + this.size * 10;
        }

        // Update trail
        this.trail = this.trail.filter(t => {
            t.life -= 0.05;
            return t.life > 0;
        });
    }

    draw() {
        const pixelSize = 4;

        // Draw trail
        this.trail.forEach(t => {
            ctx.globalAlpha = t.life * 0.5;
            ctx.fillStyle = COLORS.cloudWhite;
            for (let i = 0; i < this.size * 0.5; i++) {
                for (let j = 0; j < this.size * 0.5; j++) {
                    if (Math.random() > 0.5) {
                        drawPixel(t.x + i * pixelSize * 2, t.y + j * pixelSize * 2, COLORS.cloudWhite, pixelSize);
                    }
                }
            }
            ctx.globalAlpha = 1.0;
        });

        // Draw main cloud
        ctx.fillStyle = COLORS.cloudWhite;
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (Math.random() > 0.3) {
                    const offsetX = (i - this.size / 2) * pixelSize;
                    const offsetY = (j - this.size / 2) * pixelSize;
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
        this.forcedRight = false;
    }

    update() {
        // Wind pushes smoke to the right
        if (gameState.windActive) {
            this.vx = 3 + Math.random() * 2;
            this.vy *= 0.5;
            this.forcedRight = true;
        }

        this.x += this.vx * gameState.timeSpeed;
        this.y += this.vy * gameState.timeSpeed;
        this.life -= 0.01 * gameState.timeSpeed;
        this.vx *= 0.98;
        this.vy *= 0.98;
    }

    draw() {
        const alpha = this.life * 0.4;
        ctx.fillStyle = COLORS.smokeGray.replace('0.4', alpha);

        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (Math.random() > 0.5) {
                    drawPixel(this.x + i * 3, this.y + j * 3, ctx.fillStyle, 3);
                }
            }
        }
    }

    isDead() {
        return this.life <= 0 || this.x > canvas.width + 50;
    }
}

// Noise burst class
class NoiseBurst {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.life = 1.0;
        this.radius = 5 + Math.random() * 10;
        this.chaotic = false;
        this.exclamations = [];
    }

    update() {
        this.life -= 0.05 * gameState.timeSpeed;
        this.radius += 0.5 * gameState.timeSpeed;

        // Earthquake makes noise chaotic
        if (gameState.earthquakeActive && !this.chaotic) {
            this.chaotic = true;
            for (let i = 0; i < 5; i++) {
                this.exclamations.push({
                    x: this.x + (Math.random() - 0.5) * 30,
                    y: this.y + (Math.random() - 0.5) * 30,
                    life: 1.0
                });
            }
        }

        this.exclamations.forEach(exc => {
            exc.life -= 0.02;
            exc.y -= 0.5;
        });
        this.exclamations = this.exclamations.filter(e => e.life > 0);
    }

    draw() {
        if (gameState.earthquakeActive && this.chaotic) {
            // Draw red exclamations
            this.exclamations.forEach(exc => {
                ctx.fillStyle = `rgba(255, 0, 0, ${exc.life})`;
                ctx.font = '20px Courier New';
                ctx.fillText('!', exc.x + gameState.screenShake.x, exc.y + gameState.screenShake.y);
            });
        } else if (!gameState.blizzardActive) {
            // Normal yellow noise waves
            const alpha = this.life * 0.3;
            for (let angle = 0; angle < Math.PI * 2; angle += Math.PI / 4) {
                const x = this.x + Math.cos(angle) * this.radius;
                const y = this.y + Math.sin(angle) * this.radius;
                ctx.fillStyle = `rgba(255, 255, 0, ${alpha})`;
                drawPixel(x, y, ctx.fillStyle, 4);
                ctx.fillStyle = `rgba(255, 200, 0, ${alpha})`;
                drawPixel(x + 4, y, ctx.fillStyle, 4);
            }
        }
    }

    isDead() {
        return this.life <= 0 && this.exclamations.length === 0;
    }
}

// Person class
class Person {
    constructor(x, y, buildingIndex) {
        this.x = x;
        this.y = y;
        this.buildingIndex = buildingIndex;
        this.direction = Math.random() > 0.5 ? 1 : -1;
        this.baseSpeed = 0.2 + Math.random() * 0.3;
        this.color = Math.random() > 0.5 ? '#FF6B6B' : '#4ECDC4';
        this.visible = true;
        this.scattered = false;
    }

    update() {
        if (!this.visible) return;

        let speed = this.baseSpeed;

        // Wind slows people and pushes them right
        if (gameState.windActive) {
            this.x += 1.5 * gameState.timeSpeed;
            speed *= 0.5;
        }

        // Earthquake scatters people
        if (gameState.earthquakeActive && !this.scattered) {
            this.direction = Math.random() > 0.5 ? 1 : -1;
            this.scattered = true;
            speed *= 2;
        }

        // Blizzard makes people hide
        if (gameState.blizzardActive && gameState.blizzardIntensity > 0.3) {
            this.visible = false;
            return;
        }

        this.x += this.direction * speed * gameState.timeSpeed;

        const buildingLeft = 600 + (this.buildingIndex % 3) * 70;
        const buildingRight = buildingLeft + 60;

        if (this.x <= buildingLeft || this.x >= buildingRight) {
            this.direction *= -1;
        }
    }

    draw() {
        if (!this.visible) return;

        drawPixel(this.x, this.y, this.color, 4);
        drawPixel(this.x, this.y + 4, this.color, 4);
        drawPixel(this.x - 2, this.y + 4, this.color, 2);
        drawPixel(this.x + 4, this.y + 4, this.color, 2);
        drawPixel(this.x - 2, this.y + 8, this.color, 2);
        drawPixel(this.x + 2, this.y + 8, this.color, 2);
    }
}

// Tree class for mountain vegetation
class Tree {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.swayOffset = 0;
        this.swayPhase = Math.random() * Math.PI * 2;
    }

    update() {
        if (gameState.windActive) {
            this.swayOffset = Math.sin(Date.now() * 0.01 + this.swayPhase) * 3;
        } else {
            this.swayOffset *= 0.9;
        }
    }

    draw() {
        const isDead = gameState.pollutionLevel > 50;
        const color = isDead ? COLORS.treeDead : COLORS.treeGreen;

        drawPixel(this.x + this.swayOffset, this.y, color, 4);
        drawPixel(this.x + this.swayOffset, this.y + 4, color, 4);
    }
}

// Building class
class Building {
    constructor(index) {
        this.index = index;
        this.x = 600 + index * 70;
        this.baseHeight = 180 + Math.random() * 100;
        this.height = this.baseHeight;
        this.damaged = false;
        this.coveredByGrowth = 0; // 0 to 1
    }

    damage(amount) {
        this.height = Math.max(50, this.height - amount);
        this.damaged = true;
    }

    update() {
        // Growth covers building
        gameState.growthPixels.forEach(gp => {
            if (gp.x >= this.x && gp.x <= this.x + 60) {
                this.coveredByGrowth = Math.min(1, this.coveredByGrowth + 0.001);
            }
        });
    }

    draw() {
        const y = 500 - this.height;

        // Building body
        drawPixelRect(this.x, y, 60, this.height, COLORS.cityBuilding);

        // Growth overlay
        if (this.coveredByGrowth > 0) {
            ctx.globalAlpha = this.coveredByGrowth;
            drawPixelRect(this.x, y, 60, this.height, COLORS.treeGreen);
            ctx.globalAlpha = 1.0;
        }

        // Building outline
        ctx.strokeStyle = '#1a1a1a';
        ctx.lineWidth = 2;
        ctx.strokeRect(
            this.x + gameState.screenShake.x,
            y + gameState.screenShake.y,
            60,
            this.height
        );
    }
}

// Growth pixel class
class GrowthPixel {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.vx = 0.5 + Math.random() * 1;
        this.vy = 0.3 + Math.random() * 0.7;
        this.size = 3 + Math.random() * 4;
        this.life = 1.0;
    }

    update() {
        this.x += this.vx * gameState.timeSpeed;
        this.y += this.vy * gameState.timeSpeed;

        // Stop at city edge
        if (this.x > 800) {
            this.vx = 0;
            this.vy = 0;
        }
    }

    draw() {
        for (let i = 0; i < this.size; i++) {
            drawPixel(this.x + i * 2, this.y + i * 2, COLORS.treeGreen, 3);
        }
    }
}

// Blizzard particle class
class BlizzardParticle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = -10;
        this.vx = -1 - Math.random() * 2;
        this.vy = 2 + Math.random() * 3;
        this.size = 2 + Math.random() * 2;
    }

    update() {
        this.x += this.vx * gameState.timeSpeed * 0.5;
        this.y += this.vy * gameState.timeSpeed * 0.5;
    }

    draw() {
        drawPixel(this.x, this.y, '#FFFFFF', this.size);
    }

    isDead() {
        return this.y > canvas.height;
    }
}

// Initialize functions
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

function initCity() {
    gameState.cityLights = [];
    gameState.people = [];
    gameState.buildings = [];

    // Create buildings
    for (let i = 0; i < 3; i++) {
        gameState.buildings.push(new Building(i));
    }

    // Create window lights
    for (let building = 0; building < 3; building++) {
        for (let floor = 0; floor < 12; floor++) {
            for (let window = 0; window < 4; window++) {
                gameState.cityLights.push({
                    building: building,
                    x: 610 + building * 70 + window * 12,
                    y: 480 - floor * 15,
                    on: Math.random() > 0.3,
                    flickerTimer: Math.random() * 100,
                    malfunctioning: false
                });
            }
        }
    }

    // Create people
    for (let i = 0; i < 20; i++) {
        const buildingIndex = Math.floor(Math.random() * 3);
        gameState.people.push(new Person(
            620 + buildingIndex * 70,
            500 + Math.random() * 80,
            buildingIndex
        ));
    }
}

function initTrees() {
    gameState.trees = [];
    // Add trees on mountain slopes
    for (let i = 0; i < 30; i++) {
        const x = 60 + Math.random() * 280;
        const y = 300 + Math.random() * 150;
        gameState.trees.push(new Tree(x, y));
    }
}

// Ability functions
function activateWind() {
    if (gameState.windCooldown > 0) return;

    gameState.windActive = true;
    gameState.windTimer = 300; // 5 seconds
    gameState.windCooldown = 600; // 10 seconds

    // Immediate effects
    gameState.pollutionLevel = Math.max(0, gameState.pollutionLevel - 30);
    gameState.noiseLevel += 20; // Wind sound

    updateNarrative('special', 'The mountain summons a mighty wind! Clouds race across the sky, smoke is blown away!');
}

function activateEarthquake() {
    if (gameState.earthquakeCooldown > 0) return;

    gameState.earthquakeActive = true;
    gameState.earthquakeTimer = 60; // 1 second
    gameState.earthquakeCooldown = 900; // 15 seconds

    // Immediate effects
    gameState.fearLevel = Math.min(100, gameState.fearLevel + 40);
    gameState.noiseLevel = 0; // Noise silenced briefly

    // Damage random building
    const building = gameState.buildings[Math.floor(Math.random() * gameState.buildings.length)];
    building.damage(50);

    // Malfunction 30% of lights
    gameState.cityLights.forEach(light => {
        if (Math.random() < 0.3) {
            light.malfunctioning = true;
            light.on = false;
        }
    });

    updateNarrative('special', 'The earth trembles! Buildings crack, lights flicker out, and the city panics!');
}

function activateBlizzard() {
    if (gameState.blizzardCooldown > 0) return;

    gameState.blizzardActive = true;
    gameState.blizzardTimer = 600; // 10 seconds
    gameState.blizzardIntensity = 0;
    gameState.blizzardCooldown = 1200; // 20 seconds

    updateNarrative('special', 'A fierce blizzard descends! The city freezes, people seek shelter...');
}

function activateGrowth() {
    if (gameState.growthCooldown > 0) return;
    if (gameState.pollutionLevel > 50) {
        updateNarrative('special', 'The mountain is too polluted to summon growth! Clear the air first!');
        return;
    }

    gameState.growthCooldown = 800; // ~13 seconds

    // Spawn growth pixels from mountain
    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            const x = 100 + Math.random() * 200;
            const y = 400 + Math.random() * 100;
            gameState.growthPixels.push(new GrowthPixel(x, y));
        }, i * 20);
    }

    updateNarrative('special', 'Nature strikes back! Green tendrils spread from the mountain, reclaiming the land!');
}

// Drawing functions
function drawMountain() {
    const mountainLeft = 50;
    const mountainPeak = 150;
    const mountainRight = 350;
    const mountainBase = 500;

    // Determine colors based on pollution
    const isDead = gameState.pollutionLevel > 50;
    const grassColor = isDead ? COLORS.grassDead : COLORS.grassGreen;
    const snowColor = isDead ? COLORS.mountainSnowDirty : COLORS.mountainSnow;

    // Mountain body
    ctx.fillStyle = COLORS.mountainGray;
    ctx.beginPath();
    ctx.moveTo(mountainLeft + gameState.screenShake.x, mountainBase + gameState.screenShake.y);
    ctx.lineTo(mountainPeak + gameState.screenShake.x, 100 + gameState.screenShake.y);
    ctx.lineTo(mountainRight + gameState.screenShake.x, mountainBase + gameState.screenShake.y);
    ctx.closePath();
    ctx.fill();

    // Mountain shadows
    ctx.fillStyle = COLORS.mountainDark;
    ctx.beginPath();
    ctx.moveTo(mountainPeak + gameState.screenShake.x, 100 + gameState.screenShake.y);
    ctx.lineTo(mountainRight + gameState.screenShake.x, mountainBase + gameState.screenShake.y);
    ctx.lineTo((mountainPeak + 50) + gameState.screenShake.x, mountainBase + gameState.screenShake.y);
    ctx.closePath();
    ctx.fill();

    // Snow cap
    ctx.fillStyle = snowColor;
    ctx.beginPath();
    ctx.moveTo((mountainPeak - 40) + gameState.screenShake.x, 180 + gameState.screenShake.y);
    ctx.lineTo(mountainPeak + gameState.screenShake.x, 100 + gameState.screenShake.y);
    ctx.lineTo((mountainPeak + 40) + gameState.screenShake.x, 180 + gameState.screenShake.y);
    ctx.closePath();
    ctx.fill();

    // Dirty snow pixels if polluted
    if (isDead) {
        for (let i = 0; i < 20; i++) {
            const x = mountainPeak - 30 + Math.random() * 60;
            const y = 100 + Math.random() * 80;
            if (y < 180) {
                drawPixel(x, y, '#404040', 2);
            }
        }
    }

    // Mountain base grass
    ctx.fillStyle = grassColor;
    ctx.fillRect(
        0 + gameState.screenShake.x,
        mountainBase + gameState.screenShake.y,
        400,
        canvas.height - mountainBase
    );

    // Draw trees
    gameState.trees.forEach(tree => {
        tree.update();
        tree.draw();
    });
}

function drawCity() {
    const cityBaseY = 500;

    // Ground - may be uneven due to growth
    ctx.fillStyle = COLORS.ground;
    if (gameState.growthPixels.length > 10) {
        // Draw bumpy ground
        for (let x = 500; x < canvas.width; x += 10) {
            const bumpHeight = Math.random() * 5;
            ctx.fillRect(
                x + gameState.screenShake.x,
                cityBaseY + gameState.screenShake.y - bumpHeight,
                10,
                canvas.height - cityBaseY + bumpHeight
            );
        }
    } else {
        ctx.fillRect(
            500 + gameState.screenShake.x,
            cityBaseY + gameState.screenShake.y,
            canvas.width - 500,
            canvas.height - cityBaseY
        );
    }

    // Draw buildings
    gameState.buildings.forEach(building => {
        building.update();
        building.draw();
    });

    // Draw windows
    gameState.cityLights.forEach(light => {
        if (gameState.buildings[light.building].coveredByGrowth > 0.7) {
            return; // Don't draw lights in covered areas
        }

        light.flickerTimer += gameState.timeSpeed;
        if (light.flickerTimer > 100) {
            if (light.malfunctioning) {
                light.on = Math.random() > 0.7; // Erratic flickering
            } else {
                light.on = Math.random() > 0.2;
            }
            light.flickerTimer = 0;
        }

        let color = light.on ? COLORS.cityWindow : COLORS.cityWindowOff;

        // Blizzard makes lights turn blue then fade
        if (gameState.blizzardActive && gameState.blizzardIntensity > 0.3) {
            if (light.on) {
                color = COLORS.cityWindowBlue;
                if (gameState.blizzardIntensity > 0.6 && Math.random() > 0.5) {
                    color = COLORS.cityWindowOff;
                }
            }
        }

        drawPixelRect(light.x, light.y, 8, 10, color);
    });

    // Draw people
    gameState.people.forEach(person => {
        if (gameState.buildings[person.buildingIndex].coveredByGrowth < 0.7) {
            person.update();
            person.draw();
        }
    });
}

function drawSky() {
    let skyColor1 = COLORS.skyBlue;
    let skyColor2 = COLORS.skyDark;

    // Blizzard adds cyan filter
    if (gameState.blizzardActive) {
        skyColor1 = '#B0E0E6';
        skyColor2 = '#87CEEB';
    }

    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height / 2);
    gradient.addColorStop(0, skyColor1);
    gradient.addColorStop(1, skyColor2);

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height / 2);

    // Blizzard overlay
    if (gameState.blizzardActive) {
        ctx.fillStyle = `rgba(176, 224, 230, ${gameState.blizzardIntensity * 0.3})`;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
}

// Main render function
function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawSky();

    // Draw and update clouds
    gameState.clouds.forEach(cloud => {
        cloud.update();
        cloud.draw();
    });

    drawMountain();
    drawCity();

    // Pollution effects
    if (gameState.pollutionEnabled) {
        if (Math.random() < 0.3 * gameState.timeSpeed) {
            const chimney = 650 + Math.floor(Math.random() * 3) * 70;
            gameState.smokePuffs.push(new SmokePuff(chimney, 320));
        }

        if (Math.random() < 0.1 * gameState.timeSpeed && !gameState.blizzardActive) {
            const noiseX = 620 + Math.random() * 180;
            const noiseY = 450 + Math.random() * 50;
            gameState.noiseBursts.push(new NoiseBurst(noiseX, noiseY));
        }
    }

    // Update and draw effects
    gameState.smokePuffs = gameState.smokePuffs.filter(puff => {
        puff.update();
        puff.draw();
        return !puff.isDead();
    });

    gameState.noiseBursts = gameState.noiseBursts.filter(burst => {
        burst.update();
        burst.draw();
        return !burst.isDead();
    });

    // Draw growth pixels
    gameState.growthPixels.forEach(gp => {
        gp.update();
        gp.draw();
    });

    // Blizzard particles
    if (gameState.blizzardActive) {
        if (Math.random() < 0.5) {
            gameState.blizzardParticles.push(new BlizzardParticle());
        }

        gameState.blizzardParticles = gameState.blizzardParticles.filter(p => {
            p.update();
            p.draw();
            return !p.isDead();
        });
    }
}

// Update game state
function updateGameState() {
    if (gameState.paused) return;

    gameState.time += gameState.timeSpeed;

    // Day counter
    if (gameState.time > 500) {
        gameState.day++;
        gameState.time = 0;
        updateNarrative();
    }

    // Update pollution
    if (gameState.pollutionEnabled && !gameState.blizzardActive) {
        gameState.pollutionLevel = Math.min(100, gameState.pollutionLevel + 0.15 * gameState.timeSpeed);
    }

    // Update noise
    if (!gameState.blizzardActive) {
        const smokeCoverage = gameState.smokePuffs.length / 50;
        gameState.noiseLevel = Math.min(100, gameState.noiseBursts.length * 2);
    }

    // Wind effects
    if (gameState.windActive) {
        gameState.windTimer--;
        if (gameState.windTimer <= 0) {
            gameState.windActive = false;
            gameState.noiseLevel = Math.max(0, gameState.noiseLevel - 15);
        }
    }

    // Earthquake effects
    if (gameState.earthquakeActive) {
        gameState.earthquakeTimer--;
        gameState.screenShake.x = (Math.random() - 0.5) * 4;
        gameState.screenShake.y = (Math.random() - 0.5) * 4;

        if (gameState.earthquakeTimer <= 0) {
            gameState.earthquakeActive = false;
            gameState.screenShake.x = 0;
            gameState.screenShake.y = 0;
        }
    }

    // Blizzard effects
    if (gameState.blizzardActive) {
        gameState.blizzardTimer--;
        gameState.blizzardIntensity = Math.min(1, gameState.blizzardIntensity + 0.01);
        gameState.noiseLevel = Math.max(0, gameState.noiseLevel - 2);
        gameState.population = Math.max(0, gameState.population - 0.05);

        // Slow down time perception
        if (gameState.blizzardIntensity > 0.5) {
            gameState.timeSpeed = Math.max(0.5, gameState.timeSpeed * 0.95);
        }

        if (gameState.blizzardTimer <= 0) {
            gameState.blizzardActive = false;
            gameState.blizzardIntensity = 0;
            gameState.blizzardParticles = [];
        }
    }

    // Update cooldowns
    gameState.windCooldown = Math.max(0, gameState.windCooldown - 1);
    gameState.earthquakeCooldown = Math.max(0, gameState.earthquakeCooldown - 1);
    gameState.blizzardCooldown = Math.max(0, gameState.blizzardCooldown - 1);
    gameState.growthCooldown = Math.max(0, gameState.growthCooldown - 1);

    // Automatic consequences
    checkAutomaticConsequences();

    // Update mountain mood
    updateMountainMood();

    // Update UI
    updateUI();
}

function checkAutomaticConsequences() {
    // High pollution consequences
    if (gameState.pollutionLevel > 50 && !gameState.mountainHealthWarned) {
        updateNarrative('special', 'Warning! The mountain\'s vegetation is dying from pollution!');
        gameState.mountainHealthWarned = true;
    }

    // Noise touches mountain - avalanche
    const noiseReachingMountain = gameState.noiseBursts.some(burst =>
        burst.radius > 50 && burst.x < 400
    );

    if (noiseReachingMountain && !gameState.avalancheActive && Math.random() < 0.01) {
        triggerAvalanche();
    }
}

function triggerAvalanche() {
    gameState.avalancheActive = true;
    updateNarrative('special', 'AVALANCHE! The noise has angered the mountain! Snow crashes down!');

    // Damage city
    gameState.buildings.forEach(building => {
        if (Math.random() < 0.5) {
            building.damage(30);
        }
    });

    // Reduce mountain health
    gameState.mountainHealth = Math.max(0, gameState.mountainHealth - 10);

    setTimeout(() => {
        gameState.avalancheActive = false;
    }, 3000);
}

function updateMountainMood() {
    const totalStress = gameState.pollutionLevel + gameState.noiseLevel + gameState.fearLevel;

    if (totalStress < 50) {
        gameState.mountainMood = 'Peaceful';
    } else if (totalStress < 100) {
        gameState.mountainMood = 'Concerned';
    } else if (totalStress < 150) {
        gameState.mountainMood = 'Troubled';
    } else if (totalStress < 200) {
        gameState.mountainMood = 'Angry';
    } else {
        gameState.mountainMood = 'Furious';
    }
}

function updateUI() {
    document.getElementById('timeDisplay').textContent = `Day ${gameState.day}`;
    document.getElementById('pollutionDisplay').textContent = `${Math.floor(gameState.pollutionLevel)}%`;
    document.getElementById('noiseDisplay').textContent = `${Math.floor(gameState.noiseLevel)}%`;
    document.getElementById('fearDisplay').textContent = `${Math.floor(gameState.fearLevel)}%`;
    document.getElementById('populationDisplay').textContent = `${Math.floor(gameState.population)}%`;
    document.getElementById('mountainMoodDisplay').textContent = gameState.mountainMood;

    // Update ability buttons
    updateAbilityButton('btnWind', gameState.windCooldown);
    updateAbilityButton('btnEarthquake', gameState.earthquakeCooldown);
    updateAbilityButton('btnBlizzard', gameState.blizzardCooldown);
    updateAbilityButton('btnGrowth', gameState.growthCooldown);

    // Disable growth if too polluted
    const growthBtn = document.getElementById('btnGrowth');
    if (gameState.pollutionLevel > 50) {
        growthBtn.disabled = true;
        growthBtn.title = 'Cannot use - Mountain too polluted!';
    } else if (gameState.growthCooldown === 0) {
        growthBtn.disabled = false;
        growthBtn.title = '';
    }
}

function updateAbilityButton(btnId, cooldown) {
    const btn = document.getElementById(btnId);
    if (cooldown > 0) {
        btn.disabled = true;
        const seconds = Math.ceil(cooldown / 60);
        btn.title = `Cooldown: ${seconds}s`;
    } else {
        btn.disabled = false;
        btn.title = '';
    }
}

// Narrative system
const narratives = {
    1: "The mountain watches as the city awakens. Lights flicker on, people bustle about. It's almost... charming.",
    5: "The city grows. More buildings, more lights, more noise. The mountain remembers quieter times.",
    10: "Pollution begins to cloud the valley. The mountain's trees still stand strong, but for how long?",
    15: "The noise echoes against the mountain's slopes. Day and night blur into constant clamor.",
    20: "The mountain grows restless. Use your powers wisely to restore balance before it's too late.",
    30: "The city shows no signs of slowing. Will you let it consume everything, or will you fight back?",
    40: "Critical levels approaching. The mountain's patience wears thin. Action must be taken!",
    50: "This cannot continue. The mountain prepares to reclaim what was taken..."
};

function updateNarrative(type = 'normal', customText = null) {
    if (type === 'special' && customText) {
        document.getElementById('narrativeText').textContent = customText;
        return;
    }

    const narrativeText = narratives[gameState.day] ||
        "The eternal dance continues: nature versus civilization, silence versus noise, old versus new.";

    document.getElementById('narrativeText').textContent = narrativeText;
}

// Game loop
function gameLoop() {
    updateGameState();
    render();
    requestAnimationFrame(gameLoop);
}

// Event listeners
document.getElementById('btnWind').addEventListener('click', activateWind);
document.getElementById('btnEarthquake').addEventListener('click', activateEarthquake);
document.getElementById('btnBlizzard').addEventListener('click', activateBlizzard);
document.getElementById('btnGrowth').addEventListener('click', activateGrowth);

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
    location.reload();
});

// Initialize and start
initClouds();
initCity();
initTrees();
updateNarrative();
gameLoop();
