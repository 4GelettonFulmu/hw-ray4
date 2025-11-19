# 🏔️ The Grumpy Mountain

An interactive text-based game where you play as an ancient, primordial mountain seeking revenge against the pesky humans who have disturbed your billion-year slumber.

## 📖 Story

You are **THE MOUNTAIN**—4.5 billion years old, eternal, and thoroughly annoyed. For eons you've enjoyed peaceful silence, but then the humans arrived. They mine your minerals, cut down your forests, pollute your rivers, and worst of all—they've installed neon signs that keep you awake at night.

**ENOUGH IS ENOUGH.**

## 🎮 How to Play

### Starting the Game

```bash
python3 grumpy_mountain.py
```

### Objective

Reduce the human population from 50,000 to 0 using elemental disasters while managing their resistance and fear levels.

### Game Mechanics

#### 1. Elemental Combinations

Combine two elements to create devastating disasters:

- 🪨 **EARTH** - Mudslides, earthquakes, sinkholes
- 💧 **WATER** - Floods, acid rain, freezing fog
- 🔥 **FIRE** - Firestorms, volcanic eruptions, plasma storms
- 💨 **WIND** - Hurricanes, sandstorms, tornados
- ⚡ **THUNDER** - Lightning strikes, electromagnetic pulses
- 🌫️ **MIST** - Toxic fog, poisonous gas, blinding mist

**Example Combinations:**
- `Fire + Wind` → Firestorm
- `Earth + Water` → Mudslide
- `Thunder + Fire` → Plasma Storm
- `Water + Wind` → Hurricane

**Input formats accepted:**
- `Fire + Wind`
- `fire wind`
- `FIRE and WIND`
- All case-insensitive!

#### 2. Random Events

Type `random` to invoke the chaos of nature. This could result in:
- 🌠 Devastating meteor strikes
- 🦗 Biblical locust swarms
- ☀️ Solar flares
- 🌧️ Gentle rain (oops!)
- And many more unpredictable events...

**Warning:** Random events are truly random—you might get overwhelming devastation or embarrassing nothingness!

#### 3. Status Monitoring

Track four key metrics:

- **Remaining Population**: Humans left to annoy you (goal: 0)
- **Fear Index**: 0-100%. Higher fear = more humans flee each turn
- **Current Resistance**: Humans adapt if you use the same element type twice in a row
- **Last Attack Type**: What you used last turn

#### 4. Resistance System

Humans are clever (sort of). If you use the same element type two turns in a row, they develop resistance:
- 🔥 Fire → Fireproofing and bunkers
- 💧 Water → Dams and drainage
- 🪨 Earth → Reinforced foundations
- ⚡ Thunder → Faraday cages
- 💨 Wind → Aerodynamic structures
- 🌫️ Mist → Air filtration

**Resistance halves your damage!** Mix up your attacks to keep them vulnerable.

#### 5. Fear Mechanics

Each disaster increases the Fear Index. Higher fear means:
- More humans abandon their homes each turn
- Greater psychological impact
- Faster path to victory

But be strategic—fear-driven migration is gradual. Sometimes raw devastation is more effective!

### Victory Condition

Reduce the population to **0** or below. Then enjoy the sweet silence you've been denied for so long.

## 🎯 Strategy Tips

1. **Vary Your Elements**: Don't let humans build resistance. Switch between element types.

2. **High Damage vs. High Fear**:
   - High damage combos (Volcanic Eruption, Plasma Storm) kill more directly
   - High fear combos (Silent Thunderstorm) cause long-term migration

3. **Random Events Are Risky**: They can be devastating or useless. Use when you're feeling lucky.

4. **Fear Compounds**: Early fear investment pays off in later turns through migration.

5. **Watch the Resistance**: If you see "RESISTANCE ACTIVE!", switch elements immediately!

## 🎨 Sample Disasters

- **Firestorm** (Fire + Wind): Spiral of flames consuming everything
- **Volcanic Eruption** (Earth + Fire): Molten vengeance from your depths
- **Plasma Storm** (Thunder + Fire): Lightning and fire merge into impossible physics
- **Hurricane** (Water + Wind): Category 5+ spiral of destruction
- **Earthquake** (Earth + Thunder): Your morning stretch = 9.2 on Richter scale
- **Toxic Smoke** (Mist + Fire): Poisonous clouds seeping into their shelters
- **Acid Rain** (Water + Thunder): pH 2 corrosion from the sky

...and many more!

## 🎲 Example Gameplay

```
Turn 1: Fire + Wind → Firestorm
- Deaths: 7,500
- Fear: +25%
- Humans build firebreaks (useless)

Turn 2: Water + Earth → Mudslide
- Deaths: 6,000
- Fear: +20%
- No resistance (different element type!)

Turn 3: random → Meteor Strike!
- Deaths: 12,500
- Fear: +45%
- Humans question their life choices

Turn 4: Thunder + Mist → Silent Thunderstorm
- Deaths: 5,000
- Migration: 2,500 (fear-driven)
- Fear: +30%

Continue until population = 0!
```

## 🛑 Commands

- **Elemental combination**: `fire + wind`, `earth water`, etc.
- **Random event**: `random`
- **Quit game**: `quit`, `exit`, or `q`
- **Continue**: Press ENTER between turns

## 💡 Features

- **15 unique elemental combinations** with distinct disasters
- **10 random events** ranging from apocalyptic to embarrassing
- **Dynamic resistance system** that adapts to your tactics
- **Fear-based migration** for long-term strategic play
- **Rich narrative descriptions** with dark humor
- **Turn-by-turn status tracking**
- **Epic victory sequence** when you achieve silence

## 🎭 Tone & Style

The game embraces **darkly humorous, epic narration** from the mountain's perspective. Humans are portrayed as insignificant mayflies whose suffering is described with:
- Geological patience
- Cosmic indifference
- Occasional grudging respect for their adaptability
- Mostly just annoyance at the noise

## 🐛 Technical Details

- **Language**: Python 3
- **Dependencies**: None (uses only standard library)
- **Platform**: Cross-platform (Linux, macOS, Windows)
- **Estimated playtime**: 10-20 minutes per game

## 📜 License

This game is a work of interactive fiction. Play responsibly. No actual humans were harmed in the making of this game.

---

*Now go forth and reclaim your ancient peace, oh Grumpy Mountain!* ⛰️
