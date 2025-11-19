#!/usr/bin/env python3
"""
Demo playthrough of The Grumpy Mountain
Simulates a complete game session to showcase the experience
"""

import sys
import time
sys.path.insert(0, '/home/user/hw-ray4')

from grumpy_mountain import GrumpyMountain


def slow_print(text, delay=0.03):
    """Print text with a typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def demo_playthrough():
    """Run a scripted demo playthrough."""

    print("\n" + "="*70)
    print("           🎬 THE GRUMPY MOUNTAIN - DEMO PLAYTHROUGH 🎬")
    print("="*70)
    print("\nWitness the wrath of an ancient mountain as it reclaims its peace!")
    print("\nStarting in 3 seconds...\n")
    time.sleep(3)

    game = GrumpyMountain()

    # Scripted commands for demo
    demo_commands = [
        ("fire + wind", "Let's start with a classic FIRESTORM"),
        ("earth + water", "Time to bury them in MUD"),
        ("random", "Feeling lucky? Let the fates decide..."),
        ("thunder + fire", "PLASMA STORM - the ultimate devastation"),
        ("water + wind", "A HURRICANE to wash away their hopes"),
        ("earth + fire", "VOLCANIC ERUPTION - no mercy"),
        ("thunder + mist", "Silent death from above"),
        ("mist + fire", "Toxic smoke to finish the survivors"),
    ]

    turn = 0

    for command, description in demo_commands:
        if game.population <= 0:
            break

        turn += 1

        print("\n" + "🌋 " + "="*65)
        print(f"\n  TURN {turn}: {description}")
        print("\n" + "="*68 + "\n")
        time.sleep(1.5)

        # Display status
        game.display_status()
        time.sleep(1)

        print(f"\n⛰️  Command executed: {command.upper()}")
        print("\n" + "─"*70)
        time.sleep(1)

        # Parse and execute command
        element1, element2 = game.parse_input(command)

        if element1 == 'random':
            event_name, damage, fear, elem_type, desc = game.random_event()
            print(f"\n🎲 THE FATES DECIDE: {event_name.upper()} 🎲\n")
            print("─" * 70)
            time.sleep(0.5)
            slow_print(f"\n{desc}\n", 0.02)
            print("─" * 70)
            time.sleep(1)

            if damage > 0:
                deaths, migration = game.calculate_damage(event_name, damage, fear, elem_type)
                print("\n📈 IMPACT REPORT:")
                time.sleep(0.3)
                print(f"   💀 Deaths: {deaths:,}")
                time.sleep(0.3)
                print(f"   🏃 Fear-driven migration: {migration:,}")
                time.sleep(0.3)
                print(f"   📊 Total population loss: {deaths + migration:,}")
                time.sleep(0.3)
                if fear > 0:
                    print(f"   😱 Fear index change: +{fear}%")
            elif fear < 0:
                game.fear_index = max(0, game.fear_index + fear)
                print(f"\n   😌 The humans feel... safer? Fear index: {fear}%")
            else:
                print("\n   💭 No measurable impact.")

        elif element1 and element2:
            combo = (element1, element2)
            if combo in game.combinations:
                disaster_name, element_type, damage, fear_gain = game.combinations[combo]

                print(f"\n💀 UNLEASHING: {disaster_name.upper()} 💀\n")
                print("─" * 70)
                time.sleep(0.5)

                # Display disaster description
                if disaster_name in game.disaster_descriptions:
                    descriptions = game.disaster_descriptions[disaster_name]
                    for desc in descriptions:
                        slow_print(f"\n{desc}\n", 0.02)

                time.sleep(1)

                # Calculate damage
                deaths, migration = game.calculate_damage(disaster_name, damage,
                                                          fear_gain, element_type)

                print("─" * 70)
                print("\n📈 IMPACT REPORT:")
                time.sleep(0.3)
                print(f"   💀 Deaths: {deaths:,}")
                time.sleep(0.3)
                print(f"   🏃 Fear-driven migration: {migration:,}")
                time.sleep(0.3)
                print(f"   📊 Total population loss: {deaths + migration:,}")
                time.sleep(0.3)
                print(f"   😱 Fear index increase: +{fear_gain}%")

                if migration > 0:
                    time.sleep(0.5)
                    print(f"\n   The survivors whisper of exodus. {migration:,} humans flee in terror...")

        print("\n" + "─"*70)
        print(f"\n   Remaining population: {game.population:,}")
        print(f"   Current fear level: {game.fear_index}%")

        if game.resistance:
            print(f"   ⚠️  ALERT: Humans have developed {game.resistance.upper()} resistance!")

        print("\n")
        time.sleep(2)

        if game.population <= 0:
            break

    # Check victory
    if game.check_victory():
        time.sleep(1)
        print("\n\n")
        print("="*70)
        print("="*70)
        print("                      🏆 VICTORY 🏆")
        print("="*70)
        print("="*70)
        time.sleep(1)

        slow_print("\n\nSilence.\n", 0.05)
        time.sleep(1)
        slow_print("\nAfter countless eons, you feel it again—TRUE silence.\n", 0.04)
        time.sleep(1)
        slow_print("\nThe last human is gone. Their cities lie in ruins, slowly being", 0.04)
        slow_print("reclaimed by the very earth they sought to conquer.\n", 0.04)
        time.sleep(1)
        slow_print("\nNew grass grows on the slopes where strip malls once stood.", 0.04)
        slow_print("Animals return to lands they'd abandoned generations ago.", 0.04)
        slow_print("The rivers run clear again.\n", 0.04)
        time.sleep(1)
        slow_print("\nYou settle your ancient bones and return to your meditation.\n", 0.04)
        time.sleep(1)
        slow_print("\nPeace. Finally... peace.\n", 0.05)
        time.sleep(1)

        print("\n                    🌱 THE END 🌱\n")
        print(f"        Humans eliminated in {turn} divine interventions\n")
        print("="*70)
        print("="*70)
        print("\n")
    else:
        print("\n\n[Demo ended - Some humans still survive!]")
        print(f"Final population: {game.population:,}")
        print("\nThe mountain's work is not yet done...\n")


if __name__ == "__main__":
    demo_playthrough()
