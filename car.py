import os
import random
import json
import sys
import warnings
import hashlib
import time
from time import sleep
from datetime import datetime, timedelta

__version__ = "1.0.1"
__author__ = "WARlord05 (Enhanced from Tanay Vidhate's original)"
__description__ = "Speedy Highway Racing Game - Enhanced Edition"

warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

_entropy_seed = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

os.environ['SDL_VIDEO_WINDOW_POS'] = 'centered'

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class GameStates:
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3
    HIGH_SCORES = 4
    ACHIEVEMENTS = 5
    CAR_SELECTION = 6

class Achievement:
    def __init__(self, id, name, description, condition):
        self.id = id
        self.name = name
        self.description = description
        self.condition = condition
        self.unlocked = False


class CarRacing:
    def __init__(self):
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        
        self.current_state = GameStates.MENU
        self.previous_state = GameStates.MENU
        
        self.load_game_data()
        
        self.init_achievements()
        
        self.daily_challenge = self.generate_daily_challenge()
        
        self.initialize()

    def initialize(self):
        self.crashed = False
        self.paused = False
        self.unpause_timer = 0
        self.show_countdown = False
        
        self.base_score = 0
        self.bonus_score = 0
        self.near_miss_count = 0
        self.lane_change_count = 0
        self.survival_time = 0
        self.total_score = 0
        self.score_multiplier = 1.0
        
        self.last_near_miss_enemy_pos = None
        self.enemy_car_near_miss_counted = False
        
        self.near_miss_flash_timer = 0
        
        self.last_key_press_time = {"left": 0, "right": 0}
        self.key_repeat_delay = 12
        self.key_pressed_last_frame = {"left": False, "right": False}
        
        self.difficulty_modes = ["Easy", "Normal", "Hard", "Insane"]
        self.current_difficulty = self.game_data.get("difficulty", 1)
        
        self.available_cars = ["car.png", "car_blue.png", "car_red.png", "car_yellow.png"]
        self.current_car = self.game_data.get("selected_car", 0)
        
        self.games_played = self.game_data.get("games_played", 0)
        self.total_playtime = self.game_data.get("total_playtime", 0)
        self.best_streak = self.game_data.get("best_streak", 0)
        self.current_streak = 0

        selected_car_filename = self.available_cars[self.current_car]
        self.carImg = pygame.image.load(get_resource_path(os.path.join("assets", selected_car_filename)))
        self.car_x_coordinate = 240
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        self.enemy_car = pygame.image.load(get_resource_path(os.path.join("assets", "car_red.png")))
        self.enemy_car_startx = random.choice([240, 320, 440, 520])
        self.enemy_car_starty = -600
        
        difficulty_multiplier = [0.7, 1.0, 1.3, 1.6][self.current_difficulty]
        self.enemy_car_speed = int(5 * difficulty_multiplier)
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        self.bgImg = pygame.image.load(get_resource_path(os.path.join("assets", "back.jpg")))
        self.bgImg = pygame.transform.scale(self.bgImg, (self.display_width, self.display_height))
        self.bg_x1 = 0
        self.bg_x2 = 0
        self.bg_y1 = 0
        self.bg_y2 = -self.display_height
        self.bg_speed = int(3 * difficulty_multiplier)
        self.count = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def load_game_data(self):
        """Load game data from JSON file"""
        try:
            data_path = get_resource_path(os.path.join("data", "game_data.json"))
            with open(data_path, "r") as f:
                self.game_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.create_default_game_data()
    
    def create_default_game_data(self):
        """Create default game data structure"""
        self.game_data = {
            "high_scores": [],
            "difficulty": 1,
            "selected_car": 0,
            "unlocked_cars": [0],
            "achievements": {},
            "games_played": 0,
            "total_playtime": 0,
            "best_streak": 0,
            "last_daily_challenge": None,
            "highest_difficulty_reached": 0,
            "best_scores_per_difficulty": [0, 0, 0, 0]
        }
    
    def ensure_game_data_exists(self):
        """Ensure game data exists and is valid, recreate if necessary"""
        if not hasattr(self, 'game_data') or self.game_data is None:
            self.load_game_data()
            return
        
        try:
            data_path = get_resource_path(os.path.join("data", "game_data.json"))
            if not os.path.exists(data_path):
                self.save_game_data()
        except Exception:
            pass

    def save_game_data(self):
        """Save game data to JSON file"""
        if not hasattr(self, 'game_data') or self.game_data is None:
            self.create_default_game_data()
        
        try:
            data_path = get_resource_path(os.path.join("data", "game_data.json"))
            os.makedirs(os.path.dirname(data_path), exist_ok=True)
            with open(data_path, "w") as f:
                json.dump(self.game_data, f, indent=2)
        except (OSError, PermissionError):
            try:
                if hasattr(sys, '_MEIPASS'):
                    data_path = os.path.join(os.path.dirname(sys.executable), "game_data.json")
                else:
                    data_path = os.path.join(os.getcwd(), "game_data.json")
                with open(data_path, "w") as f:
                    json.dump(self.game_data, f, indent=2)
            except Exception as e:
                print(f"Warning: Could not save game data: {e}")
                pass
    
    def init_achievements(self):
        """Initialize achievement system"""
        self.achievements = [
            Achievement("first_game", "First Drive", "Play your first game", lambda: self.games_played >= 1),
            Achievement("score_1000", "Road Warrior", "Score 1000 points", lambda: self.total_score >= 1000),
            Achievement("score_5000", "Highway Legend", "Score 5000 points", lambda: self.total_score >= 5000),
            Achievement("near_miss_10", "Close Call", "Get 10 near misses in one game", lambda: self.near_miss_count >= 10),
            Achievement("lane_master", "Lane Master", "Change lanes 50 times in one game", lambda: self.lane_change_count >= 50),
            Achievement("survivor", "Survivor", "Survive for 2 minutes", lambda: self.survival_time >= 7200),
            Achievement("speed_demon", "Speed Demon", "Reach maximum speed", lambda: self.check_speed_demon_achievement()),
            Achievement("speed_god", "Speed God", "Reach 40 speed in Insane difficulty", lambda: self.check_speed_god_achievement()),
            Achievement("perfect_game", "Perfect Game", "Complete daily challenge", lambda: self.daily_challenge.get("completed", False))
        ]
        
        for achievement in self.achievements:
            achievement.unlocked = self.game_data.get("achievements", {}).get(achievement.id, False)
    
    def check_achievements(self):
        """Check and unlock achievements"""
        self.ensure_game_data_exists()
        for achievement in self.achievements:
            if not achievement.unlocked and achievement.condition():
                achievement.unlocked = True
                self.game_data["achievements"][achievement.id] = True
                self.show_achievement_notification(achievement)
    
    def show_achievement_notification(self, achievement):
        """Show achievement unlock notification"""
        print(f"Achievement Unlocked: {achievement.name} - {achievement.description}")
    
    def generate_daily_challenge(self):
        """Generate daily challenge"""
        today = datetime.now().strftime("%Y-%m-%d")
        if self.game_data.get("last_daily_challenge") != today:
            challenges = [
                {"type": "score", "target": 2000, "description": "Score 2000 points"},
                {"type": "survival", "target": 3600, "description": "Survive for 1 minute"},
                {"type": "near_miss", "target": 15, "description": "Get 15 near misses"},
                {"type": "lane_change", "target": 30, "description": "Change lanes 30 times"}
            ]
            challenge = random.choice(challenges)
            challenge["completed"] = False
            self.game_data["last_daily_challenge"] = today
            return challenge
        return self.game_data.get("daily_challenge", {})
    
    def calculate_enhanced_score(self):
        """Calculate score with bonuses"""
        self.base_score = self.count
        
        near_miss_bonus = self.near_miss_count * 10
        lane_change_bonus = self.lane_change_count * 2
        survival_bonus = (self.survival_time // 600) * 50
        
        difficulty_multiplier = [1.0, 1.2, 1.5, 2.0][self.current_difficulty]
        
        self.bonus_score = near_miss_bonus + lane_change_bonus + survival_bonus
        self.total_score = int((self.base_score + self.bonus_score) * difficulty_multiplier)
        
        return self.total_score
    
    def check_near_miss(self):
        """Check for near miss (enemy car passing close by)"""
        if (abs(self.car_x_coordinate - self.enemy_car_startx) <= 60 and 
            abs(self.car_y_coordinate - self.enemy_car_starty) <= 120):
            
            if not self.enemy_car_near_miss_counted:
                self.near_miss_count += 1
                self.enemy_car_near_miss_counted = True
                self.near_miss_flash_timer = 30
        
        elif self.enemy_car_starty > self.car_y_coordinate + 100:
            self.enemy_car_near_miss_counted = False
    
    def unlock_car(self, car_index):
        """Unlock a new car"""
        self.ensure_game_data_exists()
        if car_index not in self.game_data["unlocked_cars"]:
            self.game_data["unlocked_cars"].append(car_index)
            self.save_game_data()
    
    def check_car_unlocks(self):
        """Check if new cars should be unlocked based on score"""
        if self.total_score >= 500 and 1 not in self.game_data["unlocked_cars"]:
            self.unlock_car(1)
        if self.total_score >= 1500 and 2 not in self.game_data["unlocked_cars"]:
            self.unlock_car(2)
        if self.total_score >= 3000 and 3 not in self.game_data["unlocked_cars"]:
            self.unlock_car(3)

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption(f'Speedy Highway - Retro Racing v{__version__}')
        self.main_game_loop()
    
    def main_game_loop(self):
        """Main game loop with state management"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_state_events(event)
            
            if self.current_state == GameStates.MENU:
                self.update_menu()
            elif self.current_state == GameStates.PLAYING:
                self.update_game()
            elif self.current_state == GameStates.PAUSED:
                self.update_pause()
            elif self.current_state == GameStates.GAME_OVER:
                self.update_game_over()
            elif self.current_state == GameStates.HIGH_SCORES:
                self.update_high_scores()
            elif self.current_state == GameStates.ACHIEVEMENTS:
                self.update_achievements()
            elif self.current_state == GameStates.CAR_SELECTION:
                self.update_car_selection()
            
            pygame.display.update()
            self.clock.tick(60)
        
        pygame.quit()
    
    def handle_state_events(self, event):
        """Handle events based on current state"""
        if self.current_state == GameStates.MENU:
            self.handle_menu_events(event)
        elif self.current_state == GameStates.PLAYING:
            self.handle_game_events(event)
        elif self.current_state == GameStates.CAR_SELECTION:
            self.handle_car_selection_events(event)
    
    def handle_menu_events(self, event):
        """Handle menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.current_state = GameStates.PLAYING
                self.initialize()
            elif event.key == pygame.K_h:
                self.current_state = GameStates.HIGH_SCORES
            elif event.key == pygame.K_a:
                self.current_state = GameStates.ACHIEVEMENTS
            elif event.key == pygame.K_c:
                self.current_state = GameStates.CAR_SELECTION
            elif event.key == pygame.K_d:
                self.cycle_difficulty()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    def handle_car_selection_events(self, event):
        """Handle car selection events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.previous_car()
            elif event.key == pygame.K_RIGHT:
                self.next_car()
            elif event.key == pygame.K_SPACE:
                self.select_car()
            elif event.key == pygame.K_ESCAPE:
                self.current_state = GameStates.MENU
    
    def cycle_difficulty(self):
        """Cycle through difficulty modes"""
        self.ensure_game_data_exists()
        self.current_difficulty = (self.current_difficulty + 1) % len(self.difficulty_modes)
        self.game_data["difficulty"] = self.current_difficulty
        self.save_game_data()
    
    def previous_car(self):
        """Select previous car if unlocked"""
        unlocked_cars = self.game_data["unlocked_cars"]
        current_index = unlocked_cars.index(self.current_car)
        self.current_car = unlocked_cars[current_index - 1]
        self.reload_car_image()
    
    def next_car(self):
        """Select next car if unlocked"""
        unlocked_cars = self.game_data["unlocked_cars"]
        current_index = unlocked_cars.index(self.current_car)
        if current_index < len(unlocked_cars) - 1:
            self.current_car = unlocked_cars[current_index + 1]
        else:
            self.current_car = unlocked_cars[0]
        self.reload_car_image()
    
    def select_car(self):
        """Confirm car selection"""
        self.ensure_game_data_exists()
        self.game_data["selected_car"] = self.current_car
        self.save_game_data()
        self.reload_car_image()
        self.current_state = GameStates.MENU
    
    def reload_car_image(self):
        """Reload car image based on current selection"""
        selected_car_filename = self.available_cars[self.current_car]
        self.carImg = pygame.image.load(get_resource_path(os.path.join("assets", selected_car_filename)))

    def update_menu(self):
        """Update and draw main menu"""
        self.gameDisplay.fill(self.black)
        
        font_title = pygame.font.SysFont("comicsansms", 48, True)
        title = font_title.render("SPEEDY HIGHWAY", True, self.white)
        self.gameDisplay.blit(title, (400 - title.get_width() // 2, 80))
        
        font_version = pygame.font.SysFont("lucidaconsole", 16)
        version_text = font_version.render(f"v{__version__} - Enhanced Edition", True, self.yellow)
        self.gameDisplay.blit(version_text, (400 - version_text.get_width() // 2, 145))
        
        font_menu = pygame.font.SysFont("lucidaconsole", 24)
        options = [
            "SPACE - Start Game",
            "H - High Scores",
            "A - Achievements", 
            "C - Car Selection",
            f"D - Difficulty: {self.difficulty_modes[self.current_difficulty]}",
            "ESC - Quit"
        ]
        
        for i, option in enumerate(options):
            text = font_menu.render(option, True, self.white)
            self.gameDisplay.blit(text, (400 - text.get_width() // 2, 200 + i * 40))
        
        if self.daily_challenge:
            font_small = pygame.font.SysFont("lucidaconsole", 16)
            challenge_text = f"Daily Challenge: {self.daily_challenge.get('description', 'N/A')}"
            if self.daily_challenge.get('completed', False):
                challenge_text += " ✓"
            text = font_small.render(challenge_text, True, self.yellow)
            self.gameDisplay.blit(text, (10, 570))
    
    def update_game(self):
        """Update main game (equivalent to old run_car)"""
        if self.crashed:
            self.end_game()
            return
        
        if self.show_countdown:
            self.unpause_timer -= 1
            if self.unpause_timer <= 0:
                self.show_countdown = False
                
        if not self.paused and not self.show_countdown:
            self.gameDisplay.fill(self.black)
            self.back_ground_raod()

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.choice([240, 320, 440, 520])
                self.enemy_car_near_miss_counted = False

            self.car(self.car_x_coordinate, self.car_y_coordinate)
            
            self.count += 1
            self.survival_time += 1
            self.calculate_enhanced_score()
            self.check_near_miss()
            self.check_achievements()
            self.check_car_unlocks()
            
            self.handle_continuous_input()
            
            self.display_enhanced_hud()
            
            if (self.count % 100 == 0):
                if self.current_difficulty == 0:
                    if self.enemy_car_speed < 10:
                        self.enemy_car_speed += 1
                    if self.bg_speed < 7:
                        self.bg_speed += 1
                elif self.current_difficulty == 1:
                    if self.enemy_car_speed < 15:
                        self.enemy_car_speed += 1
                    if self.bg_speed < 12:
                        self.bg_speed += 1
                elif self.current_difficulty == 2:
                    if self.enemy_car_speed < 18:
                        self.enemy_car_speed += 1
                    if self.bg_speed < 15:
                        self.bg_speed += 1
                elif self.current_difficulty == 3:
                    self.enemy_car_speed += 1
                    self.bg_speed += 1

            if self.car_x_coordinate not in [240, 320, 440, 520]:
                self.crashed = True

            if (self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height and 
                self.car_y_coordinate + 80 > self.enemy_car_starty):
                if (self.car_x_coordinate + self.car_width > self.enemy_car_startx and 
                    self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width):
                    self.crashed = True
                    
        elif self.paused:
            self.display_pause_menu()
        elif self.show_countdown:
            self.gameDisplay.fill(self.black)
            self.back_ground_raod()
            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.display_enhanced_hud()
            self.display_countdown_timer()
    
    def update_pause(self):
        """Update pause state"""
        self.display_pause_menu()
    
    def update_game_over(self):
        """Update game over screen"""
        self.display_game_over_screen()
    
    def update_high_scores(self):
        """Update high scores screen"""
        self.display_high_scores()
    
    def update_achievements(self):
        """Update achievements screen"""
        self.display_achievements()
    
    def update_car_selection(self):
        """Update car selection screen"""
        self.display_car_selection()
    
    def handle_game_events(self, event):
        """Handle game events (equivalent to old event handling)"""
        if event.type == pygame.ACTIVEEVENT:
            if event.gain == 0:
                self.paused = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.paused:
                self.paused = False
                self.show_countdown = True
                self.unpause_timer = 180
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.paused:
                    self.paused = False
                    self.show_countdown = True
                    self.unpause_timer = 180
                else:
                    self.paused = True
                    self.show_countdown = False
            elif not self.paused and not self.show_countdown:
                pass
    
    def move_left(self):
        """Handle left movement with lane change tracking"""
        old_x = self.car_x_coordinate
        if self.car_x_coordinate == 320:
            self.car_x_coordinate = 240
        elif self.car_x_coordinate == 440:
            self.car_x_coordinate = 320
        elif self.car_x_coordinate == 520:
            self.car_x_coordinate = 440
        elif self.car_x_coordinate == 240:
            self.car_x_coordinate = 200
        
        if old_x != self.car_x_coordinate and self.car_x_coordinate in [240, 320, 440, 520]:
            self.lane_change_count += 1
    
    def move_right(self):
        """Handle right movement with lane change tracking"""
        old_x = self.car_x_coordinate
        if self.car_x_coordinate == 240:
            self.car_x_coordinate = 320
        elif self.car_x_coordinate == 320:
            self.car_x_coordinate = 440
        elif self.car_x_coordinate == 440:
            self.car_x_coordinate = 520
        elif self.car_x_coordinate == 520:
            self.car_x_coordinate = 560
            
        if old_x != self.car_x_coordinate and self.car_x_coordinate in [240, 320, 440, 520]:
            self.lane_change_count += 1

    def handle_continuous_input(self):
        """Handle continuous input for smoother movement"""
        keys = pygame.key.get_pressed()
        current_frame = self.count
        
        if keys[pygame.K_LEFT]:
            if not self.key_pressed_last_frame["left"]:
                self.move_left()
                self.last_key_press_time["left"] = current_frame
                self.key_pressed_last_frame["left"] = True
            elif (current_frame - self.last_key_press_time["left"]) >= self.key_repeat_delay:
                self.move_left()
                self.last_key_press_time["left"] = current_frame
        else:
            self.key_pressed_last_frame["left"] = False
        
        if keys[pygame.K_RIGHT]:
            if not self.key_pressed_last_frame["right"]:
                self.move_right()
                self.last_key_press_time["right"] = current_frame
                self.key_pressed_last_frame["right"] = True
            elif (current_frame - self.last_key_press_time["right"]) >= self.key_repeat_delay:
                self.move_right()
                self.last_key_press_time["right"] = current_frame
        else:
            self.key_pressed_last_frame["right"] = False
    
    def display_enhanced_hud(self):
        """Display enhanced HUD with more information"""
        font = pygame.font.SysFont("lucidaconsole", 20)
        font_small = pygame.font.SysFont("lucidaconsole", 14)
        
        score_text = font.render(f"Score: {self.total_score}", True, self.white)
        self.gameDisplay.blit(score_text, (10, 10))
        
        bonus_text = font_small.render(f"Bonus: {self.bonus_score}", True, self.yellow)
        self.gameDisplay.blit(bonus_text, (10, 35))
        
        near_miss_color = self.white
        if self.near_miss_flash_timer > 0:
            near_miss_color = self.green
            self.near_miss_flash_timer -= 1
        
        near_miss_text = font_small.render(f"Near Misses: {self.near_miss_count}", True, near_miss_color)
        self.gameDisplay.blit(near_miss_text, (10, 55))
        
        lane_text = font_small.render(f"Lane Changes: {self.lane_change_count}", True, self.blue)
        self.gameDisplay.blit(lane_text, (10, 75))
        
        speed_text = font_small.render(f"Speed: {self.enemy_car_speed}", True, self.red)
        self.gameDisplay.blit(speed_text, (650, 10))
        
        diff_text = font_small.render(f"Difficulty: {self.difficulty_modes[self.current_difficulty]}", True, self.white)
        self.gameDisplay.blit(diff_text, (650, 30))
        
        survival_seconds = self.survival_time // 60
        time_text = font_small.render(f"Time: {survival_seconds}s", True, self.white)
        self.gameDisplay.blit(time_text, (650, 50))
    
    def end_game(self):
        """Handle game end and score saving"""
        self.ensure_game_data_exists()
        self.games_played += 1
        self.game_data["games_played"] = self.games_played
        self.game_data["total_playtime"] += self.survival_time
        
        if self.current_difficulty > self.game_data.get("highest_difficulty_reached", 0):
            self.game_data["highest_difficulty_reached"] = self.current_difficulty
        
        best_scores = self.game_data.get("best_scores_per_difficulty", [0, 0, 0, 0])
        if self.total_score > best_scores[self.current_difficulty]:
            best_scores[self.current_difficulty] = self.total_score
            self.game_data["best_scores_per_difficulty"] = best_scores
        
        high_scores = self.game_data.get("high_scores", [])
        high_scores.append({
            "score": self.total_score,
            "difficulty": self.difficulty_modes[self.current_difficulty],
            "survival_time": self.survival_time // 60,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.game_data["high_scores"] = high_scores[:10]
        
        if self.daily_challenge:
            challenge_type = self.daily_challenge.get("type")
            target = self.daily_challenge.get("target", 0)
            
            if challenge_type == "score" and self.total_score >= target:
                self.daily_challenge["completed"] = True
            elif challenge_type == "survival" and self.survival_time >= target:
                self.daily_challenge["completed"] = True
            elif challenge_type == "near_miss" and self.near_miss_count >= target:
                self.daily_challenge["completed"] = True
            elif challenge_type == "lane_change" and self.lane_change_count >= target:
                self.daily_challenge["completed"] = True
        
        self.save_game_data()
        self.current_state = GameStates.GAME_OVER
    
    def display_game_over_screen(self):
        """Display game over screen with statistics"""
        self.gameDisplay.fill(self.black)
        
        font_title = pygame.font.SysFont("comicsansms", 72, True)
        font_text = pygame.font.SysFont("lucidaconsole", 20)
        font_small = pygame.font.SysFont("lucidaconsole", 16)
        
        title = font_title.render("GAME OVER", True, self.red)
        self.gameDisplay.blit(title, (400 - title.get_width() // 2, 100))
        
        stats = [
            f"Final Score: {self.total_score}",
            f"Base Score: {self.base_score}",
            f"Bonus Score: {self.bonus_score}",
            f"Near Misses: {self.near_miss_count}",
            f"Lane Changes: {self.lane_change_count}",
            f"Survival Time: {self.survival_time // 60}s",
            f"Difficulty: {self.difficulty_modes[self.current_difficulty]}"
        ]
        
        for i, stat in enumerate(stats):
            text = font_text.render(stat, True, self.white)
            self.gameDisplay.blit(text, (400 - text.get_width() // 2, 200 + i * 30))
        
        instruction = font_small.render("Press SPACE to return to menu", True, self.yellow)
        self.gameDisplay.blit(instruction, (400 - instruction.get_width() // 2, 500))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.current_state = GameStates.MENU
    
    def display_high_scores(self):
        """Display high scores screen"""
        self.gameDisplay.fill(self.black)
        
        font_title = pygame.font.SysFont("comicsansms", 48, True)
        font_text = pygame.font.SysFont("lucidaconsole", 18)
        font_highlight = pygame.font.SysFont("comicsansms", 32, True)
        
        title = font_title.render("HIGH SCORES", True, self.yellow)
        self.gameDisplay.blit(title, (400 - title.get_width() // 2, 30))
        
        highest_difficulty = self.game_data.get("highest_difficulty_reached", 0)
        best_scores = self.game_data.get("best_scores_per_difficulty", [0, 0, 0, 0])
        best_score_in_highest_diff = best_scores[highest_difficulty]
        
        if best_score_in_highest_diff > 0:
            highlight_text = f"Your Best in {self.difficulty_modes[highest_difficulty]}: {best_score_in_highest_diff}"
            highlight_render = font_highlight.render(highlight_text, True, self.green)
            self.gameDisplay.blit(highlight_render, (400 - highlight_render.get_width() // 2, 90))
        
        high_scores = self.game_data.get("high_scores", [])
        start_y = 140 if best_score_in_highest_diff > 0 else 120
        
        for i, score_data in enumerate(high_scores[:10]):
            score_text = f"{i+1}. {score_data['score']} - {score_data['difficulty']} - {score_data['date']}"
            text = font_text.render(score_text, True, self.white)
            self.gameDisplay.blit(text, (50, start_y + i * 30))
        
        instruction = font_text.render("Press ESC to return to menu", True, self.yellow)
        self.gameDisplay.blit(instruction, (400 - instruction.get_width() // 2, 500))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.current_state = GameStates.MENU
    
    def display_achievements(self):
        """Display achievements screen"""
        self.gameDisplay.fill(self.black)
        
        font_title = pygame.font.SysFont("comicsansms", 48, True)
        font_text = pygame.font.SysFont("lucidaconsole", 16)
        
        title = font_title.render("ACHIEVEMENTS", True, self.green)
        self.gameDisplay.blit(title, (400 - title.get_width() // 2, 50))
        
        for i, achievement in enumerate(self.achievements):
            color = self.green if achievement.unlocked else self.red
            status = "✓" if achievement.unlocked else "✗"
            text = f"{status} {achievement.name}: {achievement.description}"
            rendered_text = font_text.render(text, True, color)
            self.gameDisplay.blit(rendered_text, (50, 120 + i * 30))
        
        instruction = font_text.render("Press ESC to return to menu", True, self.yellow)
        self.gameDisplay.blit(instruction, (400 - instruction.get_width() // 2, 500))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.current_state = GameStates.MENU
    
    def display_car_selection(self):
        """Display car selection screen"""
        self.gameDisplay.fill(self.black)
        
        font_title = pygame.font.SysFont("comicsansms", 48, True)
        font_text = pygame.font.SysFont("lucidaconsole", 20)
        
        title = font_title.render("CAR SELECTION", True, self.blue)
        self.gameDisplay.blit(title, (400 - title.get_width() // 2, 50))
        
        preview_y = 120
        self.gameDisplay.blit(self.carImg, (400 - self.carImg.get_width() // 2, preview_y))
        
        unlocked_cars = self.game_data["unlocked_cars"]
        car_names = ["Default", "Blue Racer", "Red Speed", "Yellow Lightning"]
        
        for i, car_index in enumerate(unlocked_cars):
            color = self.yellow if car_index == self.current_car else self.white
            car_text = f"{car_names[car_index]}"
            if car_index == self.current_car:
                car_text = f"> {car_text} <"
            
            text = font_text.render(car_text, True, color)
            self.gameDisplay.blit(text, (400 - text.get_width() // 2, 250 + i * 40))
        
        instructions = [
            "LEFT/RIGHT - Navigate",
            "SPACE - Select Car",
            "ESC - Back to Menu"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_text.render(instruction, True, self.white)
            self.gameDisplay.blit(text, (400 - text.get_width() // 2, 450 + i * 30))

    def display_message(self, msg):
        """Legacy display message method - now redirects to game over"""
        self.current_state = GameStates.GAME_OVER

    def display_pause_menu(self):
        overlay = pygame.Surface((self.display_width, self.display_height))
        overlay.set_alpha(128)
        overlay.fill(self.black)
        self.gameDisplay.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont("comicsansms", 72, True)
        pause_text = font.render("PAUSED", True, self.white)
        self.gameDisplay.blit(pause_text, (400 - pause_text.get_width() // 2, 200 - pause_text.get_height() // 2))
        
        font_small = pygame.font.SysFont("lucidaconsole", 20)
        instruction1 = font_small.render("Press ESC to Resume", True, self.white)
        instruction2 = font_small.render("Click on window to resume", True, self.white)
        self.gameDisplay.blit(instruction1, (400 - instruction1.get_width() // 2, 280))
        self.gameDisplay.blit(instruction2, (400 - instruction2.get_width() // 2, 310))

    def display_countdown_timer(self):
        countdown_number = (self.unpause_timer // 60) + 1
        
        overlay = pygame.Surface((self.display_width, self.display_height))
        overlay.set_alpha(100)
        overlay.fill(self.black)
        self.gameDisplay.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont("comicsansms", 120, True)
        countdown_text = font.render(str(countdown_number), True, self.white)
        self.gameDisplay.blit(countdown_text, (400 - countdown_text.get_width() // 2, 300 - countdown_text.get_height() // 2))
        
        font_small = pygame.font.SysFont("comicsansms", 36, True)
        ready_text = font_small.render("Get Ready!", True, self.white)
        self.gameDisplay.blit(ready_text, (400 - ready_text.get_width() // 2, 200 - ready_text.get_height() // 2))

    def back_ground_raod(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = self.bg_y2 - self.display_height

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = self.bg_y1 - self.display_height

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def highscore(self, count):
        """Legacy method - now uses enhanced HUD"""
        pass

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render(f"SpeedyHighway v{__version__}", True, self.white)
        self.gameDisplay.blit(text, (600, 500))
        text = font.render("Thanks & Regards,", True, self.white)
        self.gameDisplay.blit(text, (600, 520))
        text = font.render("Tanay Vidhate", True, self.white)
        self.gameDisplay.blit(text, (600, 540))
        text = font.render("Enhanced by WARlord05", True, self.white)
        self.gameDisplay.blit(text, (600, 560))

    def check_speed_demon_achievement(self):
        """Check if Speed Demon achievement should be unlocked based on difficulty"""
        if self.current_difficulty == 0:
            return self.enemy_car_speed >= 10
        elif self.current_difficulty == 1:
            return self.enemy_car_speed >= 15
        elif self.current_difficulty == 2:
            return self.enemy_car_speed >= 18
        elif self.current_difficulty == 3:
            return self.enemy_car_speed >= 20
        return False
    
    def check_speed_god_achievement(self):
        """Check if Speed God achievement should be unlocked (only in Insane difficulty)"""
        if self.current_difficulty == 3:
            return self.enemy_car_speed >= 40
        return False
    
if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()