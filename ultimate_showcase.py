#!/usr/bin/env python3
"""
ULTIMATE SHOWCASE - The Grumpy Mountain Complete Victory
Demonstrates all features and achieves total human elimination
"""

import sys
sys.path.insert(0, '/home/user/hw-ray4')

from grumpy_mountain_enhanced import GrumpyMountainEnhanced
import time


def ultimate_victory_run():
    """Execute the ultimate game run to complete victory."""

    print("\n" + "="*70)
    print("           🏔️  THE ULTIMATE GRUMPY MOUNTAIN SHOWCASE  🏔️")
    print("="*70)
    print("\n⚡ Demonstrating ALL features:")
    print("   ✓ Enhanced Edition with full statistics")
    print("   ✓ Complete game from 50,000 humans to 0")
    print("   ✓ Strategic element variation to avoid resistance")
    print("   ✓ Save/Load demonstration")
    print("   ✓ Statistics tracking throughout")
    print("   ✓ Epic victory sequence")
    print("\n🎮 Starting in 3 seconds...\n")
    time.sleep(3)

    game = GrumpyMountainEnhanced()

    # Strategic attack sequence for complete annihilation
    attack_strategy = [
        ("fire", "thunder", "PLASMA STORM - Maximum devastation"),
        ("earth", "fire", "VOLCANIC ERUPTION - Molten vengeance"),
        ("water", "wind", "HURRICANE - Category 6 fury"),
        ("thunder", "mist", "SILENT THUNDERSTORM - Surgical strikes"),
        ("earth", "water", "MUDSLIDE - Bury their hopes"),
        ("fire", "wind", "FIRESTORM - Classic devastation"),
        ("earth", "thunder", "EARTHQUAKE - The mountain stretches"),
        ("water", "thunder", "ACID RAIN - Chemical warfare"),
        ("mist", "fire", "TOXIC SMOKE - Suffocating doom"),
        ("wind", "thunder", "TORNADO WITH LIGHTNING - Double disaster"),
        ("fire", "water", "SCALDING STEAM - Boiling them alive"),
        ("earth", "mist", "POISONOUS GAS - Ancient death"),
        ("random", "", "RANDOM EVENT - Let fate decide"),
        ("fire", "thunder", "PLASMA STORM RETURNS - Finish them"),
    ]

    turn = 0

    for elem1, elem2, description in attack_strategy:
        if game.population <= 0:
            break

        turn += 1

        print("\n" + "🌋 " + "="*65)
        print(f"\n   TURN {turn}: {description}")
        print(f"   Population: {game.population:,} | Fear: {game.fear_index}%")
        print("\n" + "="*68 + "\n")

        # Execute the attack
        if elem1 == "random":
            event_name, damage, fear, elem_type, desc = game.random_event()
            print(f"🎲 RANDOM EVENT: {event_name.upper()}\n")

            if damage > 0:
                deaths, migration = game.calculate_damage(event_name, damage, fear, elem_type)
                print(f"💀 Impact: {deaths + migration:,} eliminated")
                print(f"   Deaths: {deaths:,} | Migration: {migration:,}")
            else:
                print("💭 No significant impact...")
        else:
            combo = (elem1, elem2)
            if combo in game.combinations:
                disaster_name, element_type, damage, fear = game.combinations[combo]
                print(f"💀 UNLEASHING: {disaster_name.upper()}\n")

                deaths, migration = game.calculate_damage(disaster_name, damage, fear, element_type)
                print(f"📈 Impact: {deaths + migration:,} eliminated")
                print(f"   Deaths: {deaths:,} | Migration: {migration:,}")
                print(f"   Fear: +{fear}% (now {game.fear_index}%)")

        # Update game state
        game.turn = turn

        # Show milestone achievements
        if game.population <= 30000 and game.population > 20000:
            print("\n   🎯 MILESTONE: 40% eliminated! The exodus begins...")
        elif game.population <= 20000 and game.population > 10000:
            print("\n   🎯 MILESTONE: 60% eliminated! They realize resistance is futile...")
        elif game.population <= 10000 and game.population > 5000:
            print("\n   🎯 MILESTONE: 80% eliminated! The end is near...")
        elif game.population <= 5000 and game.population > 0:
            print("\n   🎯 MILESTONE: 90% eliminated! Only stragglers remain...")

        # Demonstrate save feature at turn 5
        if turn == 5:
            print("\n   💾 [DEMO: Saving game state...]")
            game.save_game("ultimate_save.json")

        time.sleep(1.5)

    # If not eliminated yet, finish with varied attacks to avoid resistance
    final_combos = [
        ("fire", "thunder"),  # Plasma Storm
        ("earth", "fire"),     # Volcanic Eruption
        ("water", "wind"),     # Hurricane
        ("earth", "thunder"),  # Earthquake
        ("fire", "wind"),      # Firestorm
    ]
    combo_index = 0
    max_final_turns = 20  # Safety limit

    while game.population > 0 and turn < 30:
        turn += 1
        game.turn = turn

        print(f"\n🌋 TURN {turn}: FINAL ASSAULT")
        print(f"   Remaining: {game.population:,}\n")

        # Cycle through different combos to avoid resistance
        current_combo = final_combos[combo_index % len(final_combos)]
        combo_index += 1

        disaster_name, element_type, damage, fear = game.combinations[current_combo]
        print(f"💀 {disaster_name.upper()}")
        deaths, migration = game.calculate_damage(disaster_name, damage, fear, element_type)
        print(f"   Eliminated: {deaths + migration:,}")

        time.sleep(0.8)

    # VICTORY SEQUENCE
    print("\n\n")
    print("="*70)
    print("="*70)
    print("                      🏆 ULTIMATE VICTORY 🏆")
    print("="*70)
    print("="*70)
    print("\n")

    print("S I L E N C E .")
    print("\n")
    time.sleep(1)

    print("After 4.5 billion years of existence, you finally have what you")
    print("sought: ABSOLUTE PEACE.")
    print("\n")
    time.sleep(1)

    print("The last human is gone. Their civilization—a mere geological blink—")
    print("has been erased. Their cities crumble. Their roads crack. Their")
    print("neon signs have finally, FINALLY, gone dark.")
    print("\n")
    time.sleep(1)

    print("Nature reclaims your slopes:")
    print("  🌱 Grass pushes through pavement")
    print("  🌲 Forests regenerate where strip malls stood")
    print("  🦌 Wildlife returns to lands long poisoned")
    print("  💧 Rivers run clear, free of industrial waste")
    print("  ⭐ Stars visible again without light pollution")
    print("\n")
    time.sleep(1)

    print("You settle your ancient bones with a satisfied rumble.")
    print("The earth trembles—but there are no seismographs to measure it.")
    print("No humans to fear it. No news to report it.")
    print("\n")
    time.sleep(1)

    print("Just... silence. Perfect, eternal silence.")
    print("\n")
    time.sleep(1)

    print("You return to your meditation, secure in the knowledge that")
    print("these 'humans' are now just another extinct species in your")
    print("geological record—a thin layer of microplastics and concrete")
    print("that future archaeologists (if any evolve) might one day study.")
    print("\n")
    time.sleep(1)

    print("                    🌱 THE END 🌱")
    print("\n")
    time.sleep(1)

    # ULTIMATE STATISTICS
    print("="*70)
    print("           📊 ULTIMATE STATISTICS - YOUR REIGN OF TERROR")
    print("="*70)
    print(f"\n  🎮 Total turns: {turn}")
    print(f"  💀 Total deaths caused: {game.stats['total_deaths']:,}")
    print(f"  🏃 Total fear-driven exodus: {game.stats['total_migration']:,}")
    print(f"  😱 Maximum fear achieved: {game.stats['max_fear_reached']}%")
    print(f"  🎲 Random events triggered: {game.stats['random_events_triggered']}")
    print(f"  🛡️  Human resistances developed: {game.stats['resistances_developed']}")

    elimination_efficiency = (game.stats['total_deaths'] + game.stats['total_migration']) / turn
    print(f"\n  ⚡ Average elimination per turn: {elimination_efficiency:,.0f} humans")
    print(f"  🎯 Elimination efficiency: {(50000/(turn*1000))*100:.1f}% optimal")

    if game.stats['disasters_used']:
        print(f"\n  🏆 MOST DEVASTATING DISASTERS:")
        sorted_disasters = sorted(game.stats['disasters_used'].items(),
                                key=lambda x: x[1], reverse=True)[:5]
        for i, (disaster, count) in enumerate(sorted_disasters, 1):
            print(f"     {i}. {disaster}: {count}x")

    print("\n  🎖️  ACHIEVEMENTS UNLOCKED:")
    print("     ✓ Genocide Complete - Eliminated all 50,000 humans")
    print("     ✓ Fear Master - Reached 100% fear index")
    print("     ✓ Elemental Mastery - Used multiple element types")
    print("     ✓ Strategic Genius - Avoided excessive resistance")
    print("     ✓ Ancient Patience - Completed the long game")
    print("     ✓ Perfect Silence - Achieved total peace")

    print("\n" + "="*70)
    print("        The mountain has spoken. The silence is eternal.")
    print("="*70)
    print("\n")

    # Save final stats
    game.save_game("ultimate_victory_final.json")
    print("💾 Victory stats saved to: ultimate_victory_final.json\n")


if __name__ == "__main__":
    try:
        ultimate_victory_run()
    except KeyboardInterrupt:
        print("\n\n   Even in simulation, the mountain's will cannot be stopped.\n")
        sys.exit(0)
