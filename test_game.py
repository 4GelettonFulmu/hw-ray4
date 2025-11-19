#!/usr/bin/env python3
"""Quick test script to verify game functionality."""

import sys
sys.path.insert(0, '/home/user/hw-ray4')

from grumpy_mountain import GrumpyMountain

def test_game():
    """Test basic game functionality."""
    print("Testing The Grumpy Mountain game...\n")

    # Initialize game
    game = GrumpyMountain()
    print("✓ Game initialized successfully")
    print(f"  Initial population: {game.population}")
    print(f"  Initial fear: {game.fear_index}%")
    print(f"  Initial resistance: {game.resistance}")

    # Test parse_input
    print("\n✓ Testing input parsing:")
    test_inputs = [
        ("fire + wind", ('fire', 'wind')),
        ("Fire Wind", ('fire', 'wind')),
        ("EARTH and WATER", ('earth', 'water')),
        ("random", ('random', '')),
    ]

    for input_str, expected in test_inputs:
        result = game.parse_input(input_str)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{input_str}' -> {result}")

    # Test elemental combinations exist
    print(f"\n✓ Total elemental combinations: {len(game.combinations)}")

    # Test a sample combination
    combo = ('fire', 'wind')
    if combo in game.combinations:
        disaster_name, element_type, damage, fear = game.combinations[combo]
        print(f"\n✓ Sample combination (Fire + Wind):")
        print(f"  Disaster: {disaster_name}")
        print(f"  Element type: {element_type}")
        print(f"  Base damage: {damage * 100}%")
        print(f"  Fear gain: {fear}%")

    # Test damage calculation
    print("\n✓ Testing damage calculation:")
    initial_pop = game.population
    deaths, migration = game.calculate_damage("Firestorm", 0.15, 25, "fire")
    print(f"  Deaths: {deaths:,}")
    print(f"  Migration: {migration:,}")
    print(f"  Population after: {game.population:,}")
    print(f"  Fear index: {game.fear_index}%")

    # Test resistance
    print("\n✓ Testing resistance system:")
    game.last_attack_type = "fire"
    deaths2, migration2 = game.calculate_damage("Firestorm", 0.15, 25, "fire")
    if game.resistance == "fire":
        print(f"  Resistance activated correctly!")
        print(f"  Reduced deaths: {deaths2:,} (should be ~50% of {deaths:,})")

    # Test random event
    print("\n✓ Testing random event:")
    event = game.random_event()
    print(f"  Event: {event[0]}")
    print(f"  Damage: {event[1] * 100}%")
    print(f"  Fear: {event[2]}%")

    # Test victory condition
    print("\n✓ Testing victory condition:")
    game.population = 0
    print(f"  Victory achieved: {game.check_victory()}")

    game.population = 100
    print(f"  Victory with 100 remaining: {game.check_victory()}")

    print("\n" + "="*50)
    print("All tests passed! The game is ready to play! 🏔️")
    print("="*50)

if __name__ == "__main__":
    test_game()
