#!/usr/bin/env python3
"""
Comprehensive test script for Speedy Highway's robust data handling system.
This script verifies that the game can handle various data persistence scenarios.
"""

import os
import json
import shutil
import tempfile
import sys
from pathlib import Path

# Add the parent directory to the path so we can import car
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import car

def test_missing_data_file():
    """Test game initialization when data file is missing"""
    print("Testing missing data file...")
    
    # Remove data file if it exists
    data_path = os.path.join("..", "data", "game_data.json")
    if os.path.exists(data_path):
        os.remove(data_path)
    
    # Initialize game
    game = car.CarRacing()
    
    # Verify default data structure
    assert game.game_data is not None
    assert isinstance(game.game_data["high_scores"], list)
    assert game.game_data["difficulty"] == 1
    assert game.game_data["selected_car"] == 0
    assert game.game_data["unlocked_cars"] == [0]
    assert isinstance(game.game_data["achievements"], dict)
    
    print("✓ Missing data file test passed")

def test_corrupted_data_file():
    """Test game initialization when data file is corrupted"""
    print("Testing corrupted data file...")
    
    # Create corrupted data file
    data_path = os.path.join("..", "data", "game_data.json")
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    
    with open(data_path, "w") as f:
        f.write("{ invalid json content }")
    
    # Initialize game
    game = car.CarRacing()
    
    # Verify it recovered with default data
    assert game.game_data is not None
    assert game.game_data["difficulty"] == 1
    assert game.game_data["unlocked_cars"] == [0]
    
    print("✓ Corrupted data file test passed")

def test_data_saving():
    """Test that data can be saved successfully"""
    print("Testing data saving...")
    
    # Remove existing data file
    data_path = os.path.join("..", "data", "game_data.json")
    if os.path.exists(data_path):
        os.remove(data_path)
    
    # Initialize game and modify data
    game = car.CarRacing()
    game.game_data["difficulty"] = 2
    game.game_data["games_played"] = 5
    game.game_data["unlocked_cars"] = [0, 1, 2]
    
    # Save data
    game.save_game_data()
    
    # Verify file was created
    assert os.path.exists(data_path)
    
    # Load and verify data
    with open(data_path, "r") as f:
        loaded_data = json.load(f)
    
    assert loaded_data["difficulty"] == 2
    assert loaded_data["games_played"] == 5
    assert loaded_data["unlocked_cars"] == [0, 1, 2]
    
    print("✓ Data saving test passed")

def test_data_persistence():
    """Test that data persists across game sessions"""
    print("Testing data persistence...")
    
    # First session: create and save data
    game1 = car.CarRacing()
    game1.game_data["games_played"] = 10
    game1.game_data["difficulty"] = 3
    game1.save_game_data()
    
    # Second session: load data
    game2 = car.CarRacing()
    
    # Verify data persisted
    assert game2.game_data["games_played"] == 10
    assert game2.game_data["difficulty"] == 3
    
    print("✓ Data persistence test passed")

def test_ensure_data_exists():
    """Test the ensure_game_data_exists functionality"""
    print("Testing ensure_game_data_exists...")
    
    # Remove data file
    data_path = os.path.join("..", "data", "game_data.json")
    if os.path.exists(data_path):
        os.remove(data_path)
    
    # Initialize game
    game = car.CarRacing()
    
    # Call ensure_game_data_exists
    game.ensure_game_data_exists()
    
    # Verify it works without errors
    assert game.game_data is not None
    
    print("✓ ensure_game_data_exists test passed")

def test_directory_creation():
    """Test that data directory is created if missing"""
    print("Testing directory creation...")
    
    # Remove data directory
    data_dir = os.path.join("..", "data")
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    
    # Initialize game and save
    game = car.CarRacing()
    game.save_game_data()
    
    # Verify directory was created
    assert os.path.exists(data_dir)
    assert os.path.exists(os.path.join(data_dir, "game_data.json"))
    
    print("✓ Directory creation test passed")

def test_all_data_dependent_methods():
    """Test all methods that depend on game data"""
    print("Testing all data-dependent methods...")
    
    # Remove data file
    data_path = os.path.join("..", "data", "game_data.json")
    if os.path.exists(data_path):
        os.remove(data_path)
    
    # Initialize game
    game = car.CarRacing()
    
    # Test methods that call ensure_game_data_exists
    game.cycle_difficulty()
    game.unlock_car(1)
    game.select_car()
    game.check_achievements()
    
    # Test end_game method
    game.total_score = 1000
    game.survival_time = 3600
    game.end_game()
    
    # Verify data was created and saved
    assert os.path.exists(data_path)
    
    # Load and verify data
    with open(data_path, "r") as f:
        loaded_data = json.load(f)
    
    assert loaded_data["games_played"] == 1
    assert len(loaded_data["high_scores"]) == 1
    assert loaded_data["high_scores"][0]["score"] == 1000
    
    print("✓ All data-dependent methods test passed")

def run_all_tests():
    """Run all tests"""
    print("Starting comprehensive data handling tests...")
    print("=" * 50)
    
    try:
        test_missing_data_file()
        test_corrupted_data_file()
        test_data_saving()
        test_data_persistence()
        test_ensure_data_exists()
        test_directory_creation()
        test_all_data_dependent_methods()
        
        print("=" * 50)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("The robust data handling system is working correctly!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
