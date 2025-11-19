#!/usr/bin/env python3
"""
The Grumpy Mountain - Enhanced Edition
Play as an ancient, primordial mountain trying to rid yourself of pesky humans.

ENHANCED FEATURES:
- Save/Load game functionality
- Statistics tracking
- Combo reference guide
- Gameplay hints
"""

import random
import sys
import json
import os
from typing import Tuple, Dict, List
from datetime import datetime


class GrumpyMountainEnhanced:
    """Enhanced game engine with save/load and statistics."""

    def __init__(self):
        self.population = 50000
        self.fear_index = 0
        self.resistance = None
        self.last_attack_type = "N/A"
        self.turn = 0

        # Statistics
        self.stats = {
            'total_deaths': 0,
            'total_migration': 0,
            'disasters_used': {},
            'random_events_triggered': 0,
            'max_fear_reached': 0,
            'resistances_developed': 0,
            'start_time': None,
        }

        # Element combinations and their effects
        self.combinations = {
            ('fire', 'wind'): ('Firestorm', 'fire', 0.15, 25),
            ('wind', 'fire'): ('Firestorm', 'fire', 0.15, 25),

            ('earth', 'water'): ('Mudslide', 'earth', 0.12, 20),
            ('water', 'earth'): ('Mudslide', 'earth', 0.12, 20),

            ('thunder', 'mist'): ('Silent Thunderstorm', 'thunder', 0.10, 30),
            ('mist', 'thunder'): ('Silent Thunderstorm', 'thunder', 0.10, 30),

            ('fire', 'earth'): ('Volcanic Eruption', 'fire', 0.20, 35),
            ('earth', 'fire'): ('Volcanic Eruption', 'fire', 0.20, 35),

            ('water', 'wind'): ('Hurricane', 'water', 0.18, 28),
            ('wind', 'water'): ('Hurricane', 'water', 0.18, 28),

            ('thunder', 'fire'): ('Plasma Storm', 'thunder', 0.22, 40),
            ('fire', 'thunder'): ('Plasma Storm', 'thunder', 0.22, 40),

            ('earth', 'thunder'): ('Earthquake', 'earth', 0.16, 32),
            ('thunder', 'earth'): ('Earthquake', 'earth', 0.16, 32),

            ('water', 'fire'): ('Scalding Steam', 'water', 0.13, 22),
            ('fire', 'water'): ('Scalding Steam', 'water', 0.13, 22),

            ('mist', 'wind'): ('Blinding Fog', 'mist', 0.08, 15),
            ('wind', 'mist'): ('Blinding Fog', 'mist', 0.08, 15),

            ('earth', 'wind'): ('Sandstorm', 'earth', 0.11, 18),
            ('wind', 'earth'): ('Sandstorm', 'earth', 0.11, 18),

            ('water', 'thunder'): ('Acid Rain', 'water', 0.14, 25),
            ('thunder', 'water'): ('Acid Rain', 'water', 0.14, 25),

            ('mist', 'fire'): ('Toxic Smoke', 'mist', 0.17, 27),
            ('fire', 'mist'): ('Toxic Smoke', 'mist', 0.17, 27),

            ('mist', 'water'): ('Freezing Fog', 'mist', 0.09, 16),
            ('water', 'mist'): ('Freezing Fog', 'mist', 0.09, 16),

            ('earth', 'mist'): ('Poisonous Gas Leak', 'earth', 0.15, 29),
            ('mist', 'earth'): ('Poisonous Gas Leak', 'earth', 0.15, 29),

            ('wind', 'thunder'): ('Tornado with Lightning', 'wind', 0.19, 33),
            ('thunder', 'wind'): ('Tornado with Lightning', 'wind', 0.19, 33),
        }

        # Disaster descriptions (same as original)
        self.disaster_descriptions = {
            'Firestorm': [
                "You exhale deeply, and your breath ignites the atmosphere. Fire and wind dance in unholy matrimony, "
                "creating a spiral of flame that tears through their pitiful settlements. The humans scatter like "
                "burning ants, their screams harmonizing with the roar of the inferno.",

                "Buildings melt like candles. The shopping mall's neon sign—that accursed beacon—finally goes dark, "
                "consumed by a wall of fire 200 feet high. Some humans attempt to build firebreaks. How adorable."
            ],

            'Mudslide': [
                "You shift your weight slightly—just a shrug, really—and a billion tons of saturated earth begins "
                "its inexorable descent. The mudslide moves like divine molasses, swallowing homes, cars, and "
                "the humans who thought concrete foundations could hold against your will.",

                "They try to outrun it. They always try to outrun it. But you are inevitable. The mud is thick "
                "with the forest they cut down, the soil they poisoned. Poetic justice, served cold and wet."
            ],

            'Silent Thunderstorm': [
                "Lightning without thunder—your favorite. Bolts of electricity arc from your peak, precise as "
                "surgical strikes. Power grids explode in cascading failures. In the darkness, the humans stumble, "
                "illuminated only by the split-second flashes that precede their doom.",

                "No warning. No sound. Just light, and then darkness, and then... less of them. You feel their "
                "terror rising like morning mist. It's almost peaceful."
            ],

            'Volcanic Eruption': [
                "ENOUGH. You open a wound in your western flank and let the planet's rage pour forth. Lava flows "
                "like molten vengeance, incinerating everything in its path. The sky turns black with ash. "
                "Their air quality index breaks the measurement scale.",

                "Some humans attempt to 'evacuate.' Where do they think they're going? You ARE the landscape. "
                "The lava pursues them with the patience of geological time—slow, but absolutely certain."
            ],

            'Hurricane': [
                "You summon the wind and water into a great spiral of destruction. A hurricane forms above your "
                "peak, its eye centered perfectly on their densest population center. Category 5 doesn't begin "
                "to describe your contempt.",

                "Their meteorologists see it coming but can't explain its impossibly rapid formation. Roofs peel "
                "away like orange rinds. The flood waters carry away their precious belongings—which you note, "
                "were mostly manufactured from YOUR minerals."
            ],

            'Plasma Storm': [
                "Fire and lightning merge into a phenomenon that shouldn't exist outside a star's core. The air "
                "itself ignites. Ball lightning bounces through the streets like malevolent children at play. "
                "Physics bends to your ancient will.",

                "Scientists will debate this event for decades—those who survive to debate, anyway. The electromagnetic "
                "pulse erases their digital civilization. No more social media. No more mining schedules. Silence."
            ],

            'Earthquake': [
                "You stretch. Just a little morning stretch after eons of stillness. The earth ripples like water. "
                "9.2 on their Richter scale. Buildings designed to 'earthquake standards' fold like origami. "
                "The mining tunnels—those violations of your body—collapse into themselves.",

                "Aftershocks continue for days. Each time they think it's over, you deliver another reminder. "
                "They clutch their doorframes and pray to gods younger than you. How quaint."
            ],

            'Scalding Steam': [
                "Fire meets water in your thermal springs, and superheated steam erupts across the settlement. "
                "The humans can't see it, can't escape it. The steam is 400 degrees—hot enough to cook them "
                "in their own homes.",

                "Their skin blisters on contact. The lucky ones pass out from heat stroke before the real "
                "suffering begins. You watch with the detached interest of a scientist observing bacteria."
            ],

            'Blinding Fog': [
                "A gentle disaster—how merciful you're feeling. Dense fog rolls down your slopes, thick as "
                "cotton, impenetrable as your ancient patience. Visibility: zero. The humans stumble off "
                "cliffs, drive into ravines, walk into rivers.",

                "It's almost funny, watching them flail in the whiteness. No dramatic deaths here—just "
                "confusion, accidents, and a growing dread that the fog might never lift."
            ],

            'Sandstorm': [
                "Wind scours the earth from your slopes, turning it into billions of tiny projectiles. The sandstorm "
                "flays paint from buildings, skin from bones. Those who seek shelter find the sand infiltrating "
                "every crack, every seal, every breath.",

                "Their machinery chokes on particulates. Solar panels are scoured opaque. The humans wrap their "
                "faces in cloth and look like the desert nomads their ancestors were. Evolution in reverse."
            ],

            'Acid Rain': [
                "You electrify the moisture in the air, creating compounds that would make a chemist weep. The rain "
                "that falls is pH 2—acidic enough to etch metal, to burn skin, to poison the water they drink.",

                "Their crops wither. Their infrastructure corrodes. Some try to collect 'clean' rainwater, not "
                "realizing every drop within 50 miles carries your chemical curse. The fear of invisible danger "
                "is exquisite to behold."
            ],

            'Toxic Smoke': [
                "Mist and fire combine into a low-lying cloud of poisonous smoke. It seeps into basements, "
                "through sealed windows, into their pathetic 'air purifiers.' Carbon monoxide. Sulfur dioxide. "
                "Your own special blend of volcanic gases.",

                "They wear masks. The masks don't help. The smoke is heavier than air, pooling in the valleys "
                "where they built their homes. Some flee uphill—toward you. The irony is not lost on your "
                "ancient consciousness."
            ],

            'Freezing Fog': [
                "The moisture in the air crystallizes instantly, coating everything in a layer of ice. The fog "
                "itself is below freezing, stealing heat from any living thing it touches. Hypothermia sets in "
                "within minutes.",

                "Their heating systems strain and fail. Ice accumulates—on power lines, on roads, on the humans "
                "themselves. They become statues in their own streets, frosted monuments to their hubris."
            ],

            'Poisonous Gas Leak': [
                "You release ancient gases from deep within your mantle—methane, hydrogen sulfide, radon. The mist "
                "carries it downhill in an invisible wave of death. Canaries in mines were warnings. The humans "
                "have no canaries.",

                "The first sign is the smell—rotten eggs. The second sign is unconsciousness. There is no third "
                "sign. Some areas are evacuated. Others are simply... emptied."
            ],

            'Tornado with Lightning': [
                "Wind and electricity spiral together in a display of atmospheric violence that defies their "
                "meteorological models. Multiple tornadoes, each wrapped in continuous lightning, dance across "
                "the settlement like dervishes of destruction.",

                "They call it a 'once in a millennium' event. They don't realize it's not chance—it's YOU. "
                "The tornadoes follow paths that maximize damage, as if guided by malevolent intelligence. "
                "Because they are."
            ],
        }

    def save_game(self, filename="grumpy_mountain_save.json"):
        """Save the current game state."""
        save_data = {
            'population': self.population,
            'fear_index': self.fear_index,
            'resistance': self.resistance,
            'last_attack_type': self.last_attack_type,
            'turn': self.turn,
            'stats': self.stats,
            'save_time': datetime.now().isoformat(),
        }

        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)

        print(f"\n✓ Game saved to {filename}")
        print(f"  Turn: {self.turn}, Population: {self.population:,}")

    def load_game(self, filename="grumpy_mountain_save.json"):
        """Load a saved game state."""
        if not os.path.exists(filename):
            print(f"\n✗ Save file '{filename}' not found!")
            return False

        with open(filename, 'r') as f:
            save_data = json.load(f)

        self.population = save_data['population']
        self.fear_index = save_data['fear_index']
        self.resistance = save_data['resistance']
        self.last_attack_type = save_data['last_attack_type']
        self.turn = save_data['turn']
        self.stats = save_data['stats']

        print(f"\n✓ Game loaded from {filename}")
        print(f"  Save time: {save_data.get('save_time', 'Unknown')}")
        print(f"  Turn: {self.turn}, Population: {self.population:,}")
        return True

    def display_statistics(self):
        """Display game statistics."""
        print("\n📊 GAME STATISTICS")
        print("═" * 70)
        print(f"  🎮 Turns played: {self.turn}")
        print(f"  💀 Total deaths caused: {self.stats['total_deaths']:,}")
        print(f"  🏃 Total fear-driven migration: {self.stats['total_migration']:,}")
        print(f"  😱 Maximum fear reached: {self.stats['max_fear_reached']}%")
        print(f"  🎲 Random events triggered: {self.stats['random_events_triggered']}")
        print(f"  🛡️  Resistances developed: {self.stats['resistances_developed']}")

        if self.stats['disasters_used']:
            print(f"\n  Most used disasters:")
            sorted_disasters = sorted(self.stats['disasters_used'].items(),
                                    key=lambda x: x[1], reverse=True)[:5]
            for disaster, count in sorted_disasters:
                print(f"    - {disaster}: {count}x")

        if self.population > 0:
            elimination_rate = (50000 - self.population) / 50000 * 100
            print(f"\n  📉 Elimination progress: {elimination_rate:.1f}%")
            print(f"  ⏱️  Average deaths per turn: {self.stats['total_deaths'] // max(self.turn, 1):,}")

        print("═" * 70)

    def display_combo_guide(self):
        """Display all available elemental combinations."""
        print("\n⚡ ELEMENTAL COMBINATION GUIDE")
        print("═" * 70)

        # Group by disaster name
        combos_by_disaster = {}
        for combo, (name, elem_type, damage, fear) in self.combinations.items():
            if name not in combos_by_disaster:
                combos_by_disaster[name] = {
                    'elements': combo,
                    'type': elem_type,
                    'damage': damage,
                    'fear': fear
                }

        # Sort by damage (highest first)
        sorted_combos = sorted(combos_by_disaster.items(),
                             key=lambda x: x[1]['damage'],
                             reverse=True)

        print("\n🔥 HIGH DAMAGE (Best for quick elimination):")
        for name, data in sorted_combos[:5]:
            e1, e2 = data['elements']
            print(f"  {name:.<30} {e1.upper()} + {e2.upper()}")
            print(f"    Damage: {data['damage']*100}% | Fear: +{data['fear']}% | Type: {data['type']}")

        print("\n😱 HIGH FEAR (Best for long-term terror):")
        fear_sorted = sorted(combos_by_disaster.items(),
                           key=lambda x: x[1]['fear'],
                           reverse=True)
        for name, data in fear_sorted[:5]:
            e1, e2 = data['elements']
            print(f"  {name:.<30} {e1.upper()} + {e2.upper()}")
            print(f"    Damage: {data['damage']*100}% | Fear: +{data['fear']}% | Type: {data['type']}")

        print("\n📋 ALL COMBINATIONS:")
        elements_list = sorted(set([e for combo in self.combinations.keys() for e in combo]))
        print(f"  Available elements: {', '.join(e.upper() for e in elements_list)}")
        print(f"  Total combinations: {len(combos_by_disaster)}")

        print("\n═" * 70)

    def display_hints(self):
        """Display gameplay hints."""
        hints = [
            "💡 Vary your elements! Using the same type twice triggers resistance (-50% damage).",
            "💡 Fear compounds over time. Early fear investment causes migration in later turns.",
            "💡 High damage combos: Plasma Storm, Volcanic Eruption, Hurricane",
            "💡 High fear combos: Plasma Storm, Silent Thunderstorm, Earthquake",
            "💡 'random' events can be devastating... or embarrassing. Risk vs reward!",
            "💡 At 100% fear, humans flee massively every turn. Terror is powerful.",
            "💡 Balance direct damage with fear-based attrition for optimal results.",
            "💡 Some disasters are poetic (Toxic Smoke, Acid Rain). Enjoy the descriptions!",
        ]

        print("\n" + random.choice(hints))

    def display_header(self):
        """Display the game header."""
        print("\n" + "═" * 70)
        print("           ⛰️  THE GRUMPY MOUNTAIN - ENHANCED EDITION ⛰️")
        print("                  A Tale of Divine Wrath")
        print("═" * 70)

    def display_status(self):
        """Display the current game status."""
        print("\n📊 [STATUS MONITORING PANEL]")
        print("┌─────────────────────────────────────┐")
        print(f"│ REMAINING POPULATION:  {self.population:,}".ljust(41) + "│")
        print(f"│ FEAR INDEX:            {self.fear_index}%".ljust(41) + "│")
        resistance_text = self.resistance if self.resistance else "None"
        print(f"│ CURRENT RESISTANCE:    {resistance_text}".ljust(41) + "│")
        print(f"│ LAST ATTACK TYPE:      {self.last_attack_type}".ljust(41) + "│")
        print("└─────────────────────────────────────┘")

    def display_console(self):
        """Display the divine power console options."""
        print("\n⚡ [DIVINE POWER CONSOLE]\n")
        print("ELEMENTAL COMBINATIONS - Choose two elements:")
        print("  🪨 EARTH | 💧 WATER | 🔥 FIRE")
        print("  💨 WIND  | ⚡ THUNDER | 🌫️ MIST\n")
        print("OR type: 'random' | 'combos' | 'stats' | 'hint' | 'save' | 'load' | 'quit'")
        print("─" * 70)

    def opening_complaint(self):
        """Display the opening complaint for each turn."""
        complaints = [
            "A new day, and the BUZZING continues. Somewhere on your eastern slope, they're building "
            "another housing development. The sound of construction equipment is like a dentist's drill "
            "against your very soul.",

            "You feel it—deep in your core—the rhythmic THUMP-THUMP-THUMP of their mining operation. "
            "They're extracting copper from your veins. It's not painful, exactly, but it's ANNOYING. "
            "Like someone constantly poking you while you're trying to sleep.",

            "The neon signs. Oh, the NEON SIGNS. They've added three new ones overnight. Your "
            "northeastern ridge is lit up like a gaudy festival. You haven't seen proper darkness "
            "in years. YEARS.",

            "Traffic. Endless traffic. The vibrations of 50,000 combustion engines create a constant "
            "low-frequency hum across your surface. It's like tinnitus, but for mountains. You contemplate "
            "the blessed silence you once knew.",

            "They've started logging again. Your forests—ancient, dignified—are being clear-cut for "
            "'sustainable development.' Each falling tree is like a hair being plucked. Death by a "
            "thousand chainsaws.",

            "The sewage. They pump their WASTE into the river that flows from your peak. The "
            "disrespect is staggering. You are billions of years old, and they treat you like their "
            "personal toilet.",

            "A factory has begun 24-hour operations. The smoke. The noise. The chemical runoff into "
            "your soil. You can feel your lichen dying. Even your LICHEN are suffering.",

            "They've installed wind turbines on your summit. WIND TURBINES. On YOUR summit. The audacity "
            "of these mayflies, thinking they can harness YOUR wind. The whoosh-whoosh-whoosh is "
            "maddening.",
        ]

        print("\n🌋 " + "═" * 65)
        if self.turn == 0:
            print("\nAWAKENING...")
            print("\nAfter 4.5 billion years of blessed silence, you stir.\n")
            print("You are THE MOUNTAIN. Eternal. Immovable. Your granite bones have")
            print("witnessed the birth of oceans, the dance of continents, the rise")
            print("and fall of a thousand species.\n")
            print("But now... NOW... there is an ITCH.\n")
            self.stats['start_time'] = datetime.now().isoformat()
        else:
            print(f"\nTURN {self.turn}")
            print()

        print(random.choice(complaints))
        print("\n" + "═" * 68 + "\n")

    def parse_input(self, user_input: str) -> Tuple[str, str]:
        """Parse user input into two elements or command."""
        user_input = user_input.lower().strip()

        # Check for special commands
        special_commands = ['random', 'combos', 'stats', 'hint', 'save', 'load', 'quit', 'exit', 'q', 'help']
        if user_input in special_commands:
            return (user_input, '')

        # Remove common separators
        user_input = user_input.replace('+', ' ').replace(',', ' ').replace('and', ' ')

        # Split into words and filter out empty strings
        words = [w.strip() for w in user_input.split() if w.strip()]

        valid_elements = ['earth', 'water', 'fire', 'wind', 'thunder', 'mist']
        elements = []

        for word in words:
            if word in valid_elements:
                elements.append(word)

        if len(elements) >= 2:
            return (elements[0], elements[1])
        elif len(elements) == 1:
            return (elements[0], '')
        else:
            return ('', '')

    def random_event(self) -> Tuple[str, int, int, str, str]:
        """Generate a random event with unpredictable results."""
        events = [
            ("Meteor Strike", 0.25, 45, "fire",
             "A METEOR—a genuine space rock—streaks through the atmosphere and impacts directly into "
             "the city center. The explosion is visible from orbit. A crater 500 meters wide erases "
             "an entire district. This is not your doing, but you're not complaining. The universe "
             "itself seems to share your irritation."),

            ("The Nothing", 0.0, 0, None,
             "You summon your wrath, you channel the forces of nature, and... nothing happens. "
             "A light breeze ruffles some leaves. A bird chirps. The humans don't even notice. "
             "Even ancient gods have off days. How embarrassing."),

            ("Locust Swarm", 0.10, 18, "wind",
             "Billions of locusts descend from the sky, blotting out the sun. They devour every plant, "
             "every crop, every piece of organic matter. The humans watch their food supply vanish "
             "in hours. Famine will follow. You didn't summon the locusts, but they seem to respect "
             "your territorial claim."),

            ("Solar Flare", 0.15, 35, "thunder",
             "The sun itself seems to be on your side. A massive solar flare sends a coronal mass "
             "ejection directly at Earth. The magnetic field does nothing. Every electronic device "
             "within 100 miles is fried. The humans are thrust back into the Stone Age. Perfect."),

            ("Sinkholes", 0.18, 25, "earth",
             "The ground beneath them simply... opens. Sinkholes appear randomly throughout the "
             "settlement, swallowing buildings whole. The humans realize their infrastructure was "
             "built on limestone and poor decisions. You feel vindicated."),

            ("Bioluminescent Doom", 0.05, 10, "mist",
             "A strange glowing mist appears. It's beautiful, actually—shimmering blues and greens. "
             "The humans come out to look. The bioluminescent algae in the mist is slightly toxic. "
             "Not very toxic. Just enough to make them sick and afraid. Art with consequences."),

            ("Absolute Zero Event", 0.22, 40, "water",
             "Temperature drops to impossible levels in seconds. Flash freeze. Water molecules cease "
             "motion. The humans become ice sculptures. Their last expressions: surprise. You don't "
             "understand the physics of how this happened, but you appreciate the aesthetic."),

            ("Magnetic Reversal", 0.12, 30, "thunder",
             "Earth's magnetic field flips. North becomes south. Birds fly in circles. The humans' "
             "navigation systems go haywire. Some people report hearing colors. Cosmic radiation "
             "increases. Chaos is a ladder, and they're falling off it."),

            ("Gentle Rain", 0.0, -5, None,
             "It rains. Just... regular rain. Gentle, soft, life-giving rain. The humans seem "
             "refreshed. Some of them smile and open umbrellas. The fear index actually DECREASES. "
             "You have made their day better. This is mortifying."),

            ("Time Distortion", 0.08, 15, "mist",
             "Time moves differently in certain areas of the settlement. Some people age rapidly. "
             "Others move in slow motion. Causality becomes a suggestion. The humans can't explain "
             "it, and neither can you, but it's certainly disruptive to their daily commute."),
        ]

        self.stats['random_events_triggered'] += 1
        event = random.choice(events)
        return event

    def calculate_damage(self, disaster_name: str, base_damage: float,
                        fear_gain: int, element_type: str) -> Tuple[int, int]:
        """Calculate population loss and fear gain, accounting for resistance."""
        # Check for resistance
        actual_damage = base_damage
        resistance_triggered = False

        if self.resistance == element_type:
            actual_damage = base_damage * 0.5
            resistance_triggered = True
            print(f"\n⚠️  RESISTANCE ACTIVE! The humans have developed {element_type.upper()} "
                  f"resistance! Damage reduced by 50%!")

        # Calculate deaths from disaster
        deaths = int(self.population * actual_damage)

        # Calculate fear-based migration
        fear_migration = int(self.population * (self.fear_index / 100) * 0.1)

        total_loss = deaths + fear_migration

        # Update population
        self.population = max(0, self.population - total_loss)

        # Update fear
        self.fear_index = min(100, self.fear_index + fear_gain)

        # Update stats
        self.stats['total_deaths'] += deaths
        self.stats['total_migration'] += fear_migration
        self.stats['max_fear_reached'] = max(self.stats['max_fear_reached'], self.fear_index)

        if disaster_name not in self.stats['disasters_used']:
            self.stats['disasters_used'][disaster_name] = 0
        self.stats['disasters_used'][disaster_name] += 1

        # Update resistance
        if element_type and self.last_attack_type == element_type and not resistance_triggered:
            self.resistance = element_type
            self.stats['resistances_developed'] += 1
        elif not resistance_triggered:
            self.resistance = None

        self.last_attack_type = element_type if element_type else "N/A"

        return deaths, fear_migration

    def execute_disaster(self, disaster_name: str, base_damage: float,
                        fear_gain: int, element_type: str):
        """Execute a disaster and display results."""
        print(f"\n💀 UNLEASHING: {disaster_name.upper()} 💀\n")
        print("─" * 70)

        # Display disaster description
        if disaster_name in self.disaster_descriptions:
            descriptions = self.disaster_descriptions[disaster_name]
            for desc in descriptions:
                print(f"\n{desc}\n")

        # Calculate and display damage
        deaths, migration = self.calculate_damage(disaster_name, base_damage,
                                                   fear_gain, element_type)

        print("─" * 70)
        print("\n📈 IMPACT REPORT:")
        print(f"   💀 Deaths: {deaths:,}")
        print(f"   🏃 Fear-driven migration: {migration:,}")
        print(f"   📊 Total population loss: {deaths + migration:,}")
        print(f"   😱 Fear index increase: +{fear_gain}%")

        if migration > 0:
            print(f"\n   The survivors whisper of exodus. {migration:,} humans flee in terror,")
            print("   abandoning their homes to seek safety elsewhere. As if anywhere is safe.")

    def play_turn(self):
        """Execute one turn of the game."""
        self.turn += 1
        self.opening_complaint()
        self.display_status()
        self.display_console()

        if self.turn == 1:
            print("\n💡 Type 'combos' to see all combinations, 'hint' for tips, 'stats' for statistics!")

        while True:
            user_input = input("\n⛰️  What is your command, Ancient One? > ").strip()

            if not user_input:
                print("   [The mountain rumbles impatiently. You must choose!]\n")
                continue

            element1, element2 = self.parse_input(user_input)

            # Handle special commands
            if element1 in ['quit', 'exit', 'q']:
                print("\n   The mountain returns to slumber...")
                print("   [The humans have been spared... for now.]\n")
                self.display_statistics()
                sys.exit(0)

            elif element1 == 'save':
                self.save_game()
                continue

            elif element1 == 'load':
                self.load_game()
                return  # Return to skip the rest of the turn

            elif element1 == 'stats':
                self.display_statistics()
                continue

            elif element1 == 'combos' or element1 == 'help':
                self.display_combo_guide()
                continue

            elif element1 == 'hint':
                self.display_hints()
                continue

            elif element1 == 'random':
                # Random event
                event_name, damage, fear, elem_type, description = self.random_event()
                print(f"\n🎲 THE FATES DECIDE... 🎲\n")
                print("─" * 70)
                print(f"\n{description}\n")
                print("─" * 70)

                if damage > 0:
                    deaths, migration = self.calculate_damage(event_name, damage, fear, elem_type)
                    print("\n📈 IMPACT REPORT:")
                    print(f"   💀 Deaths: {deaths:,}")
                    print(f"   🏃 Fear-driven migration: {migration:,}")
                    print(f"   📊 Total population loss: {deaths + migration:,}")
                    if fear > 0:
                        print(f"   😱 Fear index change: +{fear}%")
                elif fear < 0:
                    self.fear_index = max(0, self.fear_index + fear)
                    print(f"\n   😌 The humans feel... safer? Fear index: {fear}%")
                else:
                    print("\n   💭 No measurable impact. The humans continue their futile existence.")

                break

            elif element1 and element2:
                combo = (element1, element2)
                if combo in self.combinations:
                    disaster_name, element_type, damage, fear = self.combinations[combo]
                    self.execute_disaster(disaster_name, damage, fear, element_type)
                    break
                else:
                    print(f"\n   ❌ The elements {element1.upper()} and {element2.upper()} "
                          f"refuse to combine in any meaningful way.")
                    print("   [Invalid combination. Try 'combos' to see all options!]\n")
            else:
                print("\n   ❌ The mountain does not understand this command.")
                print("   [Type 'help' for assistance]\n")

    def check_victory(self) -> bool:
        """Check if the player has won."""
        return self.population <= 0

    def display_victory(self):
        """Display the victory message."""
        print("\n\n")
        print("═" * 70)
        print("═" * 70)
        print("                      🏆 VICTORY 🏆")
        print("═" * 70)
        print("═" * 70)
        print("\n")
        print("Silence.")
        print("\n")
        print("After countless eons, you feel it again—TRUE silence.")
        print("\n")
        print("The last human is gone. Their cities lie in ruins, slowly being")
        print("reclaimed by the very earth they sought to conquer. Vines creep")
        print("through shattered windows. Trees push through cracked pavement.")
        print("The neon signs are dark. Forever dark.")
        print("\n")
        print("You settle your ancient bones and let out a satisfied rumble—")
        print("what the humans would have called an earthquake, had any remained")
        print("to measure it.")
        print("\n")
        print("New grass grows on the slopes where strip malls once stood.")
        print("Animals return to lands they'd abandoned generations ago.")
        print("The rivers run clear again, no longer choked with industrial waste.")
        print("\n")
        print("You close your eyes—a metaphorical gesture, as mountains have no")
        print("eyes—and return to your meditation. Perhaps in another billion")
        print("years, when these \"humans\" are a forgotten stratum in your")
        print("sedimentary layers, you'll awaken again.")
        print("\n")
        print("But for now... peace.")
        print("\n")
        print("                    🌱 THE END 🌱")
        print("\n")
        print(f"        Humans eliminated in {self.turn} divine interventions")
        print("\n")

        # Display final statistics
        self.display_statistics()

        print("\n")
        print("═" * 70)
        print("═" * 70)
        print("\n")

    def play(self):
        """Main game loop."""
        self.display_header()

        # Check for existing save
        if os.path.exists("grumpy_mountain_save.json"):
            response = input("\n💾 Save file found! Load game? (y/n): ").lower()
            if response == 'y':
                self.load_game()

        while not self.check_victory():
            self.play_turn()

            if not self.check_victory():
                input("\n[Press ENTER to continue to the next turn...]")

        self.display_victory()


def main():
    """Main entry point for the enhanced game."""
    print("\n")
    print("Loading The Grumpy Mountain - Enhanced Edition...")
    print("\n")

    game = GrumpyMountainEnhanced()

    try:
        game.play()
    except KeyboardInterrupt:
        print("\n\n   The mountain's patience is infinite.")
        print("   The humans remain... for now.\n")
        print("\n💾 Save your game? (y/n): ", end='')
        try:
            if input().lower() == 'y':
                game.save_game()
        except:
            pass
        sys.exit(0)


if __name__ == "__main__":
    main()
