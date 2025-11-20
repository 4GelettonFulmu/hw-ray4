# 🏔️ Mountain & City: A Pixel Narrative

An interactive pixel-art narrative experience exploring the relationship between nature and civilization.

## Overview

This project presents a visual narrative told through pixel art and animations. Watch as an ancient mountain silently observes a growing city, with all the noise and pollution that comes with human progress.

## Features

### Visual Elements

- **🏔️ Mountain (Left Side)**
  - Large, imposing mountain with dark gray coloring
  - Bright white snow-capped peak
  - Detailed pixel shading and texture
  - Green grass at the base

- **🌆 City (Lower Right)**
  - Three tall buildings representing urban growth
  - Crowded with pixelated inhabitants
  - Bright, flickering window lights (yellow when on, dark when off)
  - Moving pixel people visible on the streets

- **☁️ Animated Sky**
  - Bright blue gradient sky
  - Multiple clouds floating steadily to the left
  - Dynamic cloud movement at varying speeds

- **💨 Pollution Effects**
  - Semi-transparent pixelated smoke rising from city buildings
  - Visual noise bursts (yellow waves) representing city sounds
  - Pollution gradually accumulates over time

### Interactive Controls

- **⏸️ Pause/Resume**: Freeze or resume the animation
- **⚡ Speed Up Time**: Accelerate the passage of time
- **🐌 Slow Down Time**: Slow down the animation
- **🏭 Toggle Pollution**: Enable or disable pollution effects
- **🔄 Reset Scene**: Return to the beginning

### Narrative System

The narrative evolves across multiple days, telling the story of the mountain's perspective as it watches the city grow and change. The mountain's mood shifts based on pollution levels:

- **Peaceful** (0-20% pollution): The mountain is calm
- **Concerned** (20-50% pollution): The mountain notices changes
- **Troubled** (50-80% pollution): The mountain is disturbed
- **Angry** (80-100% pollution): The mountain is distressed

## How to Run

1. Open `pixel-narrative.html` in any modern web browser
2. The experience will start automatically
3. Use the control buttons to interact with the narrative

## Technical Details

- **Technology**: HTML5 Canvas, Vanilla JavaScript
- **Canvas Size**: 800x600 pixels
- **Rendering**: Pixel-perfect rendering with crisp edges
- **Animation**: RequestAnimationFrame for smooth 60fps animation
- **Style**: Retro pixel art aesthetic

## File Structure

```
pixel-narrative.html    - Main HTML structure and styling
pixel-narrative.js      - Game logic, rendering, and animations
```

## Features Breakdown

### Pixel Art Rendering
- All elements rendered with chunky pixel blocks
- Crisp-edge image rendering for authentic retro look
- Custom pixel drawing functions for consistency

### Animation System
- Cloud objects with independent movement speeds
- Smoke particle system with life cycles
- Noise burst effects with expanding radius
- Moving people with AI-driven behavior

### Interactive Elements
- Real-time control of animation speed
- Dynamic pollution system
- Responsive narrative based on game state
- Live statistics display

## Credits

Created as an interactive narrative experience exploring environmental themes through pixel art.

## Browser Compatibility

Works best in modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

---

**Enjoy the narrative!** Watch as the ancient mountain and modern city tell their story through pixels and time.
