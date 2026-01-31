import os
import random
import json
import sys
import warnings
import hashlib
import time
from datetime import datetime, timedelta

__version__ = "1.2.0"
__author__ = "Tanay Vidhate (WARlord05)"
__description__ = "Speedy Highway Racing Game - Enhanced Edition"

warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

os.environ['SDL_VIDEO_WINDOW_POS'] = 'centered'

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.current_engine_sound = None
        self.engine_channel = None
        self.startup_channel = None
        self.engine_startup_playing = False
        self.master_volume = 0.7
        self.sfx_volume = 0.8
        self.engine_volume = 0.6
        self.crash_channel = None
        self.music_volume = 0.5
        self.music_playing = False
        self.load_sounds()
    
    def load_sounds(self):
        sound_files = {
            'crash': 'crash.wav',
            'off_road': 'off_road.wav',
            'engine_default': 'engine_default.wav',
            'engine_default_loop': 'engine_default1.wav',
            'engine_blue': 'engine_blue.wav',
            'engine_blue_loop': 'engine_blue1.wav',
            'engine_red': 'engine_red.wav',
            'engine_red_loop': 'engine_red1.wav',
            'engine_special': 'engine_special.wav',
            'engine_special_loop': 'engine_special1.wav',
            'near_miss': 'near_miss.wav',
            'achievement': 'achievement.wav',
            'menu_select': 'menu_select.wav',
            'car_unlock': 'car_unlock.wav'
        }
        
        music_files = {
            'menu_music': 'menu_music.mp3',
            'game_music': 'game_music.mp3'
        }
        
        for sound_name, filename in sound_files.items():
            try:
                sound_path = get_resource_path(os.path.join("assets", "sounds", filename))
                if os.path.exists(sound_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                else:
                    self.sounds[sound_name] = None
                    print(f"Warning: Sound file {filename} not found. Feature will be silent.")
            except pygame.error as e:
                print(f"Warning: Could not load sound {filename}: {e}")
                self.sounds[sound_name] = None
        
        for music_name, filename in music_files.items():
            try:
                music_path = get_resource_path(os.path.join("assets", "music", filename))
                if os.path.exists(music_path):
                    self.sounds[music_name] = music_path
                else:
                    self.sounds[music_name] = None
                    print(f"Warning: Music file {filename} not found. Background music will be silent.")
            except Exception as e:
                print(f"Warning: Could not load music {filename}: {e}")
                self.sounds[music_name] = None
    
    def play_sound(self, sound_name, volume_override=None):
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                sound = self.sounds[sound_name]
                volume = volume_override if volume_override else self.sfx_volume * self.master_volume
                sound.set_volume(volume)
                
                if sound_name == 'crash':
                    if self.crash_channel:
                        self.crash_channel.stop()
                    self.crash_channel = sound.play()
                    if self.crash_channel:
                        self.crash_channel.set_volume(min(1.0, volume * 1.2))
                else:
                    sound.play()
            except pygame.error as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def play_engine_sound(self, car_type, loop=True):
        startup_sounds = {
            0: 'engine_default',
            1: 'engine_blue', 
            2: 'engine_red',
            3: 'engine_special'
        }
        
        loop_sounds = {
            0: 'engine_default_loop',
            1: 'engine_blue_loop', 
            2: 'engine_red_loop',
            3: 'engine_special_loop'
        }
        
        startup_sound_name = startup_sounds.get(car_type, 'engine_default')
        loop_sound_name = loop_sounds.get(car_type, 'engine_default_loop')
        
        self.stop_engine_sound()
        
        if loop and startup_sound_name in self.sounds and self.sounds[startup_sound_name]:
            try:
                startup_sound = self.sounds[startup_sound_name]
                self.startup_channel = startup_sound.play()
                if self.startup_channel:
                    self.startup_channel.set_volume(self.engine_volume * self.master_volume)
                    self.engine_startup_playing = True
                    
                if loop_sound_name in self.sounds and self.sounds[loop_sound_name]:
                    self.current_engine_sound = self.sounds[loop_sound_name]
                    startup_length = int(startup_sound.get_length() * 1000)
                    pygame.time.set_timer(pygame.USEREVENT + 1, startup_length)
                    
            except pygame.error as e:
                print(f"Error playing engine startup sound: {e}")
        elif not loop and startup_sound_name in self.sounds and self.sounds[startup_sound_name]:
            try:
                startup_sound = self.sounds[startup_sound_name]
                self.startup_channel = startup_sound.play()
                if self.startup_channel:
                    self.startup_channel.set_volume(self.engine_volume * self.master_volume)
            except pygame.error as e:
                print(f"Error playing engine preview sound: {e}")
    
    def start_engine_loop(self):
        if self.current_engine_sound and not self.engine_channel:
            try:
                self.engine_channel = self.current_engine_sound.play(-1)
                if self.engine_channel:
                    self.engine_channel.set_volume(self.engine_volume * self.master_volume)
                self.engine_startup_playing = False
            except pygame.error as e:
                print(f"Error playing engine loop sound: {e}")
    
    def stop_engine_sound(self):
        if self.engine_channel:
            self.engine_channel.stop()
            self.engine_channel = None
        if self.startup_channel:
            self.startup_channel.stop()
            self.startup_channel = None
        self.current_engine_sound = None
        self.engine_startup_playing = False
        pygame.time.set_timer(pygame.USEREVENT + 1, 0)
    
    def update_engine_volume(self, speed_factor):
        if self.engine_channel:
            volume = min(1.0, 0.3 + (speed_factor * 0.7))
            final_volume = volume * self.engine_volume * self.master_volume
            self.engine_channel.set_volume(final_volume)
        if self.startup_channel and self.engine_startup_playing:
            volume = min(1.0, 0.3 + (speed_factor * 0.7))
            final_volume = volume * self.engine_volume * self.master_volume
            self.startup_channel.set_volume(final_volume)
    
    def set_master_volume(self, volume):
        self.master_volume = max(0.0, min(1.0, volume))
        if self.engine_channel:
            self.engine_channel.set_volume(self.engine_volume * self.master_volume)
        if self.startup_channel and self.engine_startup_playing:
            self.startup_channel.set_volume(self.engine_volume * self.master_volume)
        self.update_master_volume_with_music()
    
    def cleanup(self):
        self.stop_engine_sound()
        self.stop_music()
        if self.crash_channel:
            self.crash_channel.stop()
            self.crash_channel = None
        pygame.mixer.quit()
    
    def play_music(self, music_name):
        if music_name in self.sounds and self.sounds[music_name]:
            try:
                if self.music_playing:
                    pygame.mixer.music.stop()
                
                pygame.mixer.music.load(self.sounds[music_name])
                pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
                pygame.mixer.music.play(-1)
                self.music_playing = True
            except pygame.error as e:
                print(f"Error playing music {music_name}: {e}")
    
    def stop_music(self):
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
    
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        if self.music_playing:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    
    def update_master_volume_with_music(self):
        if self.music_playing:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)

def get_resource_path(relative_path):
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
        
        try:
            icon_path = os.path.join("assets", "ico.png")
            if os.path.exists(icon_path):
                icon = pygame.image.load(icon_path)
                pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Could not load window icon during initialization: {e}")
        
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
        
        self._entropy_seed = None
        self._game_random = random.Random()
        self._replay_data = []
        self._is_replay_mode = False
        
        self.sound_manager = SoundManager()
        
        self.current_state = GameStates.MENU
        self.previous_state = GameStates.MENU
        
        self.reset_confirmation_active = False
        self.quit_confirmation_active = False
        self.fullscreen_mode = False
        self.seed_input_active = False
        self.seed_input_text = ""
        
        self.load_game_data()
        
        self.init_achievements()
        
        self.daily_challenge = self.generate_daily_challenge()
        
        self.initialize()
        
        self.sound_manager.play_music('menu_music')

    def initialize(self, seed=None):
        self.crashed = False
        self.paused = False
        self.unpause_timer = 0
        self.show_countdown = False
        
        if seed is not None:
            self.set_entropy_seed(seed)
        elif self._entropy_seed is None:
            self.generate_new_entropy_seed()
        
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
        
        self.engine_started = False
        
        self.last_key_press_time = {"left": 0, "right": 0}
        self.key_repeat_delay = 11
        self.key_pressed_last_frame = {"left": False, "right": False}
        
        self.difficulty_modes = ["Easy", "Normal", "Hard", "Insane"]
        self.current_difficulty = self.game_data.get("difficulty", 1)
        
        self.available_cars = ["car.png", "car_blue.png", "car_red.png", "special"]
        self.current_car = self.game_data.get("selected_car", 0)
        
        self.special_car_frame = 0
        self.special_car_animation_timer = 0
        self.special_car_animation_speed = 15
        
        self.games_played = self.game_data.get("games_played", 0)
        self.total_playtime = self.game_data.get("total_playtime", 0)
        self.best_streak = self.game_data.get("best_streak", 0)
        self.current_streak = 0

        selected_car_filename = self.available_cars[self.current_car]
        if selected_car_filename == "special":
            try:
                self.carImg_spc_frames = []
                for i in range(12):
                    frame_path = get_resource_path(os.path.join("assets", "spc", f"spc{i}.png"))
                    frame_img = pygame.image.load(frame_path)
                    self.carImg_spc_frames.append(frame_img)
                self.carImg = self.carImg_spc_frames[0]
            except pygame.error:
                print("Warning: Special car images (spc0.png to spc11.png) not found in spc folder. Using car_yellow.png as fallback.")
                self.carImg = pygame.image.load(get_resource_path(os.path.join("assets", "car_yellow.png")))
        else:
            self.carImg = pygame.image.load(get_resource_path(os.path.join("assets", selected_car_filename)))
        self.car_x_coordinate = 215
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 99

        self.enemy_car = pygame.image.load(get_resource_path(os.path.join("assets", "car_black.png")))
        self.enemy_car_startx = self.deterministic_choice([215, 295, 415, 495])
        self.enemy_car_starty = -600
        
        difficulty_multiplier = [0.7, 1.0, 1.3, 1.6][self.current_difficulty]
        self.enemy_car_speed = int(5 * difficulty_multiplier)
        self.enemy_car_width = 99
        self.enemy_car_height = 100

        self.bgImg = pygame.image.load(get_resource_path(os.path.join("assets", "back.jpg")))
        self.bgImg = pygame.transform.scale(self.bgImg, (self.display_width, self.display_height))
        
        
        try:
            self.menu_bg_icon = pygame.image.load(get_resource_path(os.path.join("assets", "ico.png")))
            icon_rect = self.menu_bg_icon.get_rect()
            scale_factor = max(self.display_width / icon_rect.width, self.display_height / icon_rect.height)
            new_width = int(icon_rect.width * scale_factor)
            new_height = int(icon_rect.height * scale_factor)
            self.menu_bg_icon = pygame.transform.scale(self.menu_bg_icon, (new_width, new_height))
            
            self.menu_bg_icon_faded = self.menu_bg_icon.copy()
            dark_overlay = pygame.Surface((new_width, new_height))
            dark_overlay.set_alpha(180)
            dark_overlay.fill((0, 0, 0))
            self.menu_bg_icon_faded.blit(dark_overlay, (0, 0))
        except Exception as e:
            print(f"Could not load menu background icon: {e}")
            self.menu_bg_icon = None
            self.menu_bg_icon_faded = None
        
        self.bg_x1 = 0
        self.bg_x2 = 0
        self.bg_y1 = 0
        self.bg_y2 = -self.display_height
        self.bg_speed = int(3 * difficulty_multiplier)
        self.count = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))
    
    def generate_new_entropy_seed(self):
        """Generate a new entropy seed based on current time and system state"""
        timestamp = int(time.time() * 1000000)
        system_hash = hashlib.md5(f"{timestamp}{os.getpid()}{id(self)}".encode()).hexdigest()
        self._entropy_seed = int(system_hash[:8], 16)
        self._game_random.seed(self._entropy_seed)
        print(f"Generated new entropy seed: {self._entropy_seed}")
    
    def set_entropy_seed(self, seed):
        """Set a specific entropy seed for deterministic gameplay"""
        self._entropy_seed = seed
        self._game_random.seed(seed)
        print(f"Set entropy seed to: {seed}")
    
    def get_entropy_seed(self):
        """Get the current entropy seed"""
        return self._entropy_seed
    
    def deterministic_choice(self, choices):
        """Make a deterministic choice from a list using the entropy seed"""
        if self._is_replay_mode and self._replay_data:
            return self._replay_data.pop(0) if self._replay_data else choices[0]
        else:
            choice = self._game_random.choice(choices)
            if not self._is_replay_mode:
                self._replay_data.append(choice)
            return choice
    
    def deterministic_randint(self, min_val, max_val):
        """Generate a deterministic random integer using the entropy seed"""
        if self._is_replay_mode and self._replay_data:
            return self._replay_data.pop(0) if self._replay_data else min_val
        else:
            value = self._game_random.randint(min_val, max_val)
            if not self._is_replay_mode:
                self._replay_data.append(value)
            return value
    
    def start_replay(self, seed, replay_data):
        """Start replay mode with given seed and recorded data"""
        self._is_replay_mode = True
        self._entropy_seed = seed
        self._game_random.seed(seed)
        self._replay_data = replay_data.copy()
        print(f"Starting replay with seed: {seed}")
    
    def stop_replay(self):
        """Stop replay mode and return to normal gameplay"""
        self._is_replay_mode = False
        self._replay_data = []
        print("Stopped replay mode")
    
    def get_replay_data(self):
        """Get the current replay data for saving"""
        return {
            'seed': self._entropy_seed,
            'data': self._replay_data.copy()
        }

    def load_game_data(self):
        try:
            data_path = get_resource_path(os.path.join("data", "game_data.json"))
            with open(data_path, "r") as f:
                self.game_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.create_default_game_data()
    
    def create_default_game_data(self):
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
            "daily_challenge": {},
            "highest_difficulty_reached": 0,
            "best_scores_per_difficulty": [0, 0, 0, 0]
        }
    
    def ensure_game_data_exists(self):
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
        self.achievements = [
            Achievement("first_game", "First Drive", "Play your first game", lambda: self.games_played >= 1),
            Achievement("score_1000", "Road Warrior", "Score 1000 points", lambda: self.total_score >= 1000),
            Achievement("score_5000", "Highway Legend", "Score 5000 points", lambda: self.total_score >= 5000 and self.current_difficulty >= 1),
            Achievement("near_miss_10", "Close Call", "Get 10 near misses in one game", lambda: self.near_miss_count >= 10),
            Achievement("lane_master", "Lane Master", "Change lanes 50 times in one game", lambda: self.lane_change_count >= 50),
            Achievement("survivor", "Survivor", "Survive for 2 minutes", lambda: self.survival_time >= 7200),
            Achievement("speed_demon", "Speed Demon", "Reach maximum speed", lambda: self.check_speed_demon_achievement()),
            Achievement("speed_god", "Speed God", "Reach 40 speed in Insane difficulty", lambda: self.check_speed_god_achievement()),
            Achievement("perfect_game", "Perfect Game", "Complete daily challenge", lambda: self.daily_challenge.get("completed", False))
        ]
        
        self.ensure_game_data_exists()
        for achievement in self.achievements:
            achievement.unlocked = self.game_data.get("achievements", {}).get(achievement.id, False)
    
    def check_achievements(self):
        self.ensure_game_data_exists()
        achievements_changed = False
        for achievement in self.achievements:
            if not achievement.unlocked and achievement.condition():
                achievement.unlocked = True
                self.game_data["achievements"][achievement.id] = True
                self.show_achievement_notification(achievement)
                achievements_changed = True
        
        if achievements_changed:
            self.save_game_data()
    
    def show_achievement_notification(self, achievement):
        print(f"Achievement Unlocked: {achievement.name} - {achievement.description}")
        self.sound_manager.play_sound('achievement')
    
    def generate_daily_challenge(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if self.game_data.get("last_daily_challenge") != today:
            challenges = [
                {"type": "score", "target": 2000, "description": "Score 2000 points"},
                {"type": "survival", "target": 3600, "description": "Survive for 1 minute"},
                {"type": "near_miss", "target": 15, "description": "Get 15 near misses"},
                {"type": "lane_change", "target": 30, "description": "Change lanes 30 times"}
            ]
            challenge_seed = int(hashlib.md5(today.encode()).hexdigest()[:8], 16)
            challenge_random = random.Random(challenge_seed)
            challenge = challenge_random.choice(challenges)
            challenge["completed"] = False
            self.game_data["last_daily_challenge"] = today
            self.game_data["daily_challenge"] = challenge
            self.save_game_data()
            return challenge
        return self.game_data.get("daily_challenge", {})
    
    def calculate_enhanced_score(self):
        self.base_score = self.count
        
        near_miss_bonus = self.near_miss_count * 10
        lane_change_bonus = self.lane_change_count * 2
        survival_bonus = (self.survival_time // 600) * 50
        
        difficulty_multiplier = [1.0, 1.2, 1.5, 2.0][self.current_difficulty]
        
        self.bonus_score = near_miss_bonus + lane_change_bonus + survival_bonus
        self.total_score = int((self.base_score + self.bonus_score) * difficulty_multiplier)
        
        return self.total_score
    
    def check_near_miss(self):
        if (abs(self.car_x_coordinate - self.enemy_car_startx) <= 50 and 
            abs(self.car_y_coordinate - self.enemy_car_starty) <= 100):
            
            if not self.enemy_car_near_miss_counted:
                self.near_miss_count += 1
                self.enemy_car_near_miss_counted = True
                self.near_miss_flash_timer = 30
                self.sound_manager.play_sound('near_miss')
        
        elif self.enemy_car_starty > self.car_y_coordinate + 50:
            self.enemy_car_near_miss_counted = False
    
    def unlock_car(self, car_index):
        self.ensure_game_data_exists()
        if car_index not in self.game_data["unlocked_cars"]:
            self.game_data["unlocked_cars"].append(car_index)
            self.save_game_data()
            self.sound_manager.play_sound('car_unlock')
    
    def check_car_unlocks(self):
        if self.total_score >= 500 and 1 not in self.game_data["unlocked_cars"]:
            self.unlock_car(1)
        if self.total_score >= 1500 and 2 not in self.game_data["unlocked_cars"]:
            self.unlock_car(2)
        if self.total_score >= 3000 and 3 not in self.game_data["unlocked_cars"]:
            self.unlock_car(3)
    
    def update_special_car_animation(self):
        if hasattr(self, 'carImg_spc_frames') and len(self.carImg_spc_frames) > 0:
            self.special_car_animation_timer += 1
            if self.special_car_animation_timer >= self.special_car_animation_speed:
                self.special_car_animation_timer = 0
                self.special_car_frame = (self.special_car_frame + 1) % len(self.carImg_spc_frames)
                self.carImg = self.carImg_spc_frames[self.special_car_frame]

    def racing_window(self):
        self.setup_display()
        self.main_game_loop()
    
    def setup_display(self):
        """Setup display mode based on fullscreen setting"""
        if self.fullscreen_mode:
            self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height), pygame.FULLSCREEN)
        else:
            self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        
        pygame.display.set_caption(f'Speedy Highway - Retro Racing v{__version__}')
        
        try:
            icon_path = os.path.join("assets", "ico.png")
            if os.path.exists(icon_path):
                icon = pygame.image.load(icon_path)
                pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Could not load window icon: {e}")
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.fullscreen_mode = not self.fullscreen_mode
        self.setup_display()
        self.sound_manager.play_sound('menu_select')
    
    def main_game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if not self.quit_confirmation_active:
                        self.quit_confirmation_active = True
                        self.sound_manager.play_sound('menu_select')
                elif event.type == pygame.USEREVENT + 1:
                    self.sound_manager.start_engine_loop()
                else:
                    if self.quit_confirmation_active:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_y:
                                self.sound_manager.cleanup()
                                pygame.quit()
                                sys.exit()
                            elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                                self.quit_confirmation_active = False
                                self.sound_manager.play_sound('menu_back')
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
        if self.current_state == GameStates.MENU:
            self.handle_menu_events(event)
        elif self.current_state == GameStates.PLAYING:
            self.handle_game_events(event)
        elif self.current_state == GameStates.CAR_SELECTION:
            self.handle_car_selection_events(event)
        elif self.current_state == GameStates.ACHIEVEMENTS:
            self.handle_achievements_events(event)
    
    def handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if self.seed_input_active:
                self.handle_seed_input_events(event)
                return
                
            if event.key == pygame.K_SPACE:
                self.sound_manager.play_sound('menu_select')
                self.current_state = GameStates.PLAYING
                self.initialize()
                self.sound_manager.play_engine_sound(self.current_car)
                self.sound_manager.play_music('game_music')
                self.engine_started = True
            elif event.key == pygame.K_h:
                self.sound_manager.play_sound('menu_select')
                self.current_state = GameStates.HIGH_SCORES
            elif event.key == pygame.K_a:
                self.sound_manager.play_sound('menu_select')
                self.current_state = GameStates.ACHIEVEMENTS
            elif event.key == pygame.K_c:
                self.sound_manager.play_sound('menu_select')
                self.current_state = GameStates.CAR_SELECTION
            elif event.key == pygame.K_d:
                self.sound_manager.play_sound('menu_select')
                self.cycle_difficulty()
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                current_volume = self.sound_manager.master_volume
                self.sound_manager.set_master_volume(current_volume - 0.1)
                self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                current_volume = self.sound_manager.master_volume
                self.sound_manager.set_master_volume(current_volume + 0.1)
                self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_LEFTBRACKET:
                current_music_volume = self.sound_manager.music_volume
                self.sound_manager.set_music_volume(current_music_volume - 0.1)
                self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_RIGHTBRACKET:
                current_music_volume = self.sound_manager.music_volume
                self.sound_manager.set_music_volume(current_music_volume + 0.1)
                self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_m:
                if self.sound_manager.master_volume > 0:
                    self.sound_manager.set_master_volume(0)
                else:
                    self.sound_manager.set_master_volume(0.7)
                self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_n:
                if self.sound_manager.music_volume > 0:
                    self.sound_manager.set_music_volume(0)
                else:
                    self.sound_manager.set_music_volume(0.7)
                self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_s:
                self.seed_input_active = True
                self.seed_input_text = ""
                self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_f:
                self.toggle_fullscreen()
            elif event.key == pygame.K_RETURN and (pygame.key.get_pressed()[pygame.K_LALT] or pygame.key.get_pressed()[pygame.K_RALT]):
                self.toggle_fullscreen()
            elif event.key == pygame.K_ESCAPE:
                if not self.quit_confirmation_active:
                    self.quit_confirmation_active = True
                    self.sound_manager.play_sound('menu_select')
    
    def handle_seed_input_events(self, event):
        if event.key == pygame.K_RETURN:
            try:
                if self.seed_input_text.strip():
                    custom_seed = int(self.seed_input_text.strip())
                    self.set_entropy_seed(custom_seed)
                    print(f"Custom entropy seed set to: {custom_seed}")
                else:
                    self.generate_new_entropy_seed()
                    print("Empty input. Generated new random seed.")
            except ValueError:
                print("Invalid seed input. Generated new random seed.")
                self.generate_new_entropy_seed()
            
            self.seed_input_active = False
            self.seed_input_text = ""
            self.sound_manager.play_sound('menu_select')
            
        elif event.key == pygame.K_ESCAPE:
            self.seed_input_active = False
            self.seed_input_text = ""
            self.sound_manager.play_sound('menu_select')
            
        elif event.key == pygame.K_BACKSPACE:
            self.seed_input_text = self.seed_input_text[:-1]
            
        else:
            if event.unicode.isdigit() or (event.unicode == '-' and len(self.seed_input_text) == 0):
                if len(self.seed_input_text) < 15:
                    self.seed_input_text += event.unicode
    
    def handle_car_selection_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.sound_manager.play_sound('menu_select')
                self.previous_car()
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.sound_manager.play_sound('menu_select')
                self.next_car()
            elif event.key == pygame.K_SPACE:
                self.sound_manager.play_sound('menu_select')
                self.select_car()
            elif event.key == pygame.K_ESCAPE:
                self.sound_manager.play_sound('menu_select')
                self.sound_manager.stop_engine_sound()
                self.current_state = GameStates.MENU
                self.sound_manager.play_music('menu_music')
    
    def cycle_difficulty(self):
        self.ensure_game_data_exists()
        self.current_difficulty = (self.current_difficulty + 1) % len(self.difficulty_modes)
        self.game_data["difficulty"] = self.current_difficulty
        self.save_game_data()
    
    def previous_car(self):
        unlocked_cars = self.game_data["unlocked_cars"]
        current_index = unlocked_cars.index(self.current_car)
        self.current_car = unlocked_cars[current_index - 1]
        self.reload_car_image()
        self.sound_manager.play_engine_sound(self.current_car, loop=False)
    
    def next_car(self):
        unlocked_cars = self.game_data["unlocked_cars"]
        current_index = unlocked_cars.index(self.current_car)
        if current_index < len(unlocked_cars) - 1:
            self.current_car = unlocked_cars[current_index + 1]
        else:
            self.current_car = unlocked_cars[0]
        self.reload_car_image()
        self.sound_manager.play_engine_sound(self.current_car, loop=False)
    
    def select_car(self):
        self.ensure_game_data_exists()
        self.game_data["selected_car"] = self.current_car
        self.save_game_data()
        self.reload_car_image()
        self.current_state = GameStates.MENU
        self.sound_manager.stop_engine_sound()
    
    def reload_car_image(self):
        selected_car_filename = self.available_cars[self.current_car]
        if selected_car_filename == "special":
            try:
                self.carImg_spc_frames = []
                for i in range(12):
                    frame_path = get_resource_path(os.path.join("assets", "spc", f"spc{i}.png"))
                    frame_img = pygame.image.load(frame_path)
                    self.carImg_spc_frames.append(frame_img)
                self.carImg = self.carImg_spc_frames[0]
                self.special_car_frame = 0
            except pygame.error:
                print("Warning: Special car images (spc0.png to spc11.png) not found in spc folder. Using car_yellow.png as fallback.")
                self.carImg = pygame.image.load(get_resource_path(os.path.join("assets", "car_yellow.png")))
        else:
            self.carImg = pygame.image.load(get_resource_path(os.path.join("assets", selected_car_filename)))

    def update_menu(self):
        self.gameDisplay.fill(self.black)
        
        if self.quit_confirmation_active:
            self.display_quit_confirmation()
        elif self.seed_input_active:
            self.display_seed_input()
        else:
            self.display_main_menu()
    
    def display_main_menu(self):
        if hasattr(self, 'menu_bg_icon_faded') and self.menu_bg_icon_faded:
            icon_rect = self.menu_bg_icon_faded.get_rect()
            x = (self.display_width - icon_rect.width) // 2
            y = (self.display_height - icon_rect.height) // 2
            self.gameDisplay.blit(self.menu_bg_icon_faded, (x, y))
        
        panel_width = 650
        panel_height = 450
        panel_x = (self.display_width - panel_width) // 2
        panel_y = 60
        
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(160)
        panel_surface.fill((0, 0, 0))
        
        pygame.draw.rect(panel_surface, (64, 64, 64), (0, 0, panel_width, panel_height), 3)
        
        self.gameDisplay.blit(panel_surface, (panel_x, panel_y))
        
        font_title = pygame.font.SysFont("comicsansms", 48, True)
        title = font_title.render("SPEEDY HIGHWAY", True, self.white)
        self.gameDisplay.blit(title, (400 - title.get_width() // 2, 80))
        
        font_version = pygame.font.SysFont("lucidaconsole", 16)
        version_text = font_version.render(f"v{__version__} - Enhanced Edition", True, self.yellow)
        self.gameDisplay.blit(version_text, (400 - version_text.get_width() // 2, 145))
        
        font_menu = pygame.font.SysFont("lucidaconsole", 24)
        fullscreen_status = "ON" if self.fullscreen_mode else "OFF"
        options = [
            "SPACE - Start Game",
            "H - High Scores",
            "A - Achievements", 
            "C - Car Selection",
            f"D - Difficulty: {self.difficulty_modes[self.current_difficulty]}",
            f"F - Fullscreen: {fullscreen_status}",
            "ESC - Quit"
        ]
        
        for i, option in enumerate(options):
            text = font_menu.render(option, True, self.white)
            self.gameDisplay.blit(text, (400 - text.get_width() // 2, 200 + i * 35))
        
        font_small = pygame.font.SysFont("lucidaconsole", 16)
        volume_percent = int(self.sound_manager.master_volume * 100)
        volume_text = f"Sound Volume: {volume_percent}% (+/- to adjust, M to mute)"
        volume_render = font_small.render(volume_text, True, self.yellow)
        self.gameDisplay.blit(volume_render, (400 - volume_render.get_width() // 2, 435))
        
        music_volume_percent = int(self.sound_manager.music_volume * 100)
        music_text = f"Music Volume: {music_volume_percent}% ([/] to adjust, N to mute)"
        music_render = font_small.render(music_text, True, self.yellow)
        self.gameDisplay.blit(music_render, (400 - music_render.get_width() // 2, 455))
        
        fullscreen_text = "ALT+ENTER - Toggle fullscreen anytime"
        fullscreen_render = font_small.render(fullscreen_text, True, self.green)
        self.gameDisplay.blit(fullscreen_render, (400 - fullscreen_render.get_width() // 2, 475))
        
        seed_text = f"Entropy Seed: {self._entropy_seed} (S to set custom seed)"
        seed_render = font_small.render(seed_text, True, self.blue)
        seed_bg = pygame.Surface((seed_render.get_width() + 10, seed_render.get_height() + 4))
        seed_bg.set_alpha(180)
        seed_bg.fill((0, 0, 0))
        self.gameDisplay.blit(seed_bg, (5, 8))
        self.gameDisplay.blit(seed_render, (10, 10))
        
        
        if self.daily_challenge:
            challenge_text = f"Daily Challenge: {self.daily_challenge.get('description', 'N/A')}"
            if self.daily_challenge.get('completed', False):
                challenge_text += " [COMPLETE]"
            text = font_small.render(challenge_text, True, self.yellow)
            challenge_bg = pygame.Surface((text.get_width() + 10, text.get_height() + 4))
            challenge_bg.set_alpha(180)
            challenge_bg.fill((0, 0, 0))
            self.gameDisplay.blit(challenge_bg, (5, 548))
            self.gameDisplay.blit(text, (10, 550))
    
    def display_seed_input(self):
        if hasattr(self, 'menu_bg_icon_faded') and self.menu_bg_icon_faded:
            icon_rect = self.menu_bg_icon_faded.get_rect()
            x = (self.display_width - icon_rect.width) // 2
            y = (self.display_height - icon_rect.height) // 2
            self.gameDisplay.blit(self.menu_bg_icon_faded, (x, y))
        
        
        panel_width = 550
        panel_height = 400
        panel_x = (self.display_width - panel_width) // 2
        panel_y = (self.display_height - panel_height) // 2
        
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(180)
        panel_surface.fill((0, 0, 0))
        
        
        pygame.draw.rect(panel_surface, (64, 64, 64), (0, 0, panel_width, panel_height), 3)
        
        self.gameDisplay.blit(panel_surface, (panel_x, panel_y))
        
        font_title = pygame.font.SysFont("comicsansms", 48, True)
        font_text = pygame.font.SysFont("lucidaconsole", 24)
        font_small = pygame.font.SysFont("lucidaconsole", 16)
        
        title = font_title.render("CUSTOM ENTROPY SEED", True, self.yellow)
        self.gameDisplay.blit(title, (400 - title.get_width() // 2, 150))
        
        instruction = font_text.render("Enter a custom seed (integer):", True, self.white)
        self.gameDisplay.blit(instruction, (400 - instruction.get_width() // 2, 250))
        
        input_box_rect = pygame.Rect(300, 300, 200, 40)
        pygame.draw.rect(self.gameDisplay, self.white, input_box_rect, 2)

        input_text = font_text.render(self.seed_input_text, True, self.white)
        text_x = input_box_rect.x + 5
        text_y = input_box_rect.y + (input_box_rect.height - input_text.get_height()) // 2
        self.gameDisplay.blit(input_text, (text_x, text_y))
        
        cursor_x = text_x + input_text.get_width()
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.line(self.gameDisplay, self.white, 
                           (cursor_x, text_y), 
                           (cursor_x, text_y + input_text.get_height()), 2)
        
        instructions = [
            "ENTER - Confirm seed",
            "ESC - Cancel",
            "BACKSPACE - Delete character",
            "",
            f"Current seed: {self._entropy_seed}"
        ]
        
        for i, instruction in enumerate(instructions):
            color = self.yellow if instruction else self.white
            if instruction:
                text = font_small.render(instruction, True, color)
                self.gameDisplay.blit(text, (400 - text.get_width() // 2, 400 + i * 25))
    
    def display_quit_confirmation(self):
        if hasattr(self, 'menu_bg_icon_faded') and self.menu_bg_icon_faded:
            icon_rect = self.menu_bg_icon_faded.get_rect()
            x = (self.display_width - icon_rect.width) // 2
            y = (self.display_height - icon_rect.height) // 2
            self.gameDisplay.blit(self.menu_bg_icon_faded, (x, y))
        
        
        panel_width = 500
        panel_height = 300
        panel_x = (self.display_width - panel_width) // 2
        panel_y = (self.display_height - panel_height) // 2
        
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(200)
        panel_surface.fill((20, 20, 20))
        
        pygame.draw.rect(panel_surface, (128, 128, 128), (0, 0, panel_width, panel_height), 3)
        
        self.gameDisplay.blit(panel_surface, (panel_x, panel_y))
        
        font_title = pygame.font.SysFont("comicsansms", 48, True)
        font_text = pygame.font.SysFont("lucidaconsole", 24)
        font_small = pygame.font.SysFont("lucidaconsole", 18)
        
        title = font_title.render("QUIT GAME?", True, self.red)
        self.gameDisplay.blit(title, (400 - title.get_width() // 2, 200))
        
        message = font_text.render("Are you sure you want to quit?", True, self.white)
        self.gameDisplay.blit(message, (400 - message.get_width() // 2, 280))
        
        warning = font_small.render("Any unsaved progress will be lost.", True, self.yellow)
        self.gameDisplay.blit(warning, (400 - warning.get_width() // 2, 320))
        
        instructions = [
            "Y - Yes, quit the game",
            "N - No, go back to menu",
            "ESC - Cancel"
        ]
        
        for i, instruction in enumerate(instructions):
            color = self.green if instruction.startswith("N") else self.yellow
            text = font_small.render(instruction, True, color)
            self.gameDisplay.blit(text, (400 - text.get_width() // 2, 350 + i * 25))
    
    def update_game(self):
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
                self.enemy_car_startx = self.deterministic_choice([215, 295, 415, 495])
                self.enemy_car_near_miss_counted = False

            self.car(self.car_x_coordinate, self.car_y_coordinate)
            
            self.count += 1
            self.survival_time += 1
            self.calculate_enhanced_score()
            self.check_near_miss()
            self.check_achievements()
            self.check_car_unlocks()
            
            if self.current_car == 3:
                self.update_special_car_animation()
            
            self.handle_continuous_input()
            
            if self.engine_started:
                speed_factor = min(1.0, self.enemy_car_speed / 20.0)
                self.sound_manager.update_engine_volume(speed_factor)
            
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


            ROAD_MIN_X = 200
            ROAD_MAX_X = 520
            
            if self.car_x_coordinate < ROAD_MIN_X or self.car_x_coordinate > ROAD_MAX_X:
                self.sound_manager.play_sound('off_road')
                self.sound_manager.stop_engine_sound()
                self.engine_started = False
                self.crashed = True


            if (self.car_y_coordinate + 20 < self.enemy_car_starty + self.enemy_car_height and 
                self.car_y_coordinate + 50 > self.enemy_car_starty):
                car_left = self.car_x_coordinate + 10
                car_right = self.car_x_coordinate + self.car_width - 10
                enemy_left = self.enemy_car_startx + 10
                enemy_right = self.enemy_car_startx + self.enemy_car_width - 10
                
                if (car_right > enemy_left and car_left < enemy_right):
                    self.sound_manager.play_sound('crash', volume_override=1.0)
                    self.sound_manager.stop_engine_sound()
                    self.engine_started = False
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
        self.display_pause_menu()
    
    def update_game_over(self):
        self.display_game_over_screen()
    
    def update_high_scores(self):
        self.display_high_scores()
    
    def update_achievements(self):
        self.display_achievements()
    
    def update_car_selection(self):
        if self.current_car == 3:
            self.update_special_car_animation()
        self.display_car_selection()
    
    def handle_game_events(self, event):
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
            elif event.key == pygame.K_f:
                self.toggle_fullscreen()
            elif event.key == pygame.K_RETURN and (pygame.key.get_pressed()[pygame.K_LALT] or pygame.key.get_pressed()[pygame.K_RALT]):
                self.toggle_fullscreen()
            elif not self.paused and not self.show_countdown:
                pass
    
    def move_left(self):
        old_x = self.car_x_coordinate
        if self.car_x_coordinate == 295:
            self.car_x_coordinate = 215
        elif self.car_x_coordinate == 415:
            self.car_x_coordinate = 295
        elif self.car_x_coordinate == 495:
            self.car_x_coordinate = 415
        elif self.car_x_coordinate == 215:
            self.car_x_coordinate = 175
        
        if old_x != self.car_x_coordinate and self.car_x_coordinate in [215, 295, 415, 495]:
            self.lane_change_count += 1
    
    def move_right(self):
        old_x = self.car_x_coordinate
        if self.car_x_coordinate == 215:
            self.car_x_coordinate = 295
        elif self.car_x_coordinate == 295:
            self.car_x_coordinate = 415
        elif self.car_x_coordinate == 415:
            self.car_x_coordinate = 495
        elif self.car_x_coordinate == 495:
            self.car_x_coordinate = 535
            
        if old_x != self.car_x_coordinate and self.car_x_coordinate in [215, 295, 415, 495]:
            self.lane_change_count += 1

    def handle_continuous_input(self):
        keys = pygame.key.get_pressed()
        current_frame = self.count
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not self.key_pressed_last_frame["left"]:
                self.move_left()
                self.last_key_press_time["left"] = current_frame
                self.key_pressed_last_frame["left"] = True
            elif (current_frame - self.last_key_press_time["left"]) >= self.key_repeat_delay:
                self.move_left()
                self.last_key_press_time["left"] = current_frame
        else:
            self.key_pressed_last_frame["left"] = False
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
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
        self.sound_manager.stop_engine_sound()
        self.engine_started = False
        
        self.ensure_game_data_exists()
        self.games_played += 1
        self.game_data["games_played"] = self.games_played
        self.game_data["total_playtime"] += self.survival_time
        
        self.check_achievements()
        
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
                self.game_data["daily_challenge"] = self.daily_challenge
            elif challenge_type == "survival" and self.survival_time >= target:
                self.daily_challenge["completed"] = True
                self.game_data["daily_challenge"] = self.daily_challenge
            elif challenge_type == "near_miss" and self.near_miss_count >= target:
                self.daily_challenge["completed"] = True
                self.game_data["daily_challenge"] = self.daily_challenge
            elif challenge_type == "lane_change" and self.lane_change_count >= target:
                self.daily_challenge["completed"] = True
                self.game_data["daily_challenge"] = self.daily_challenge
        
        self.save_game_data()
        self.current_state = GameStates.GAME_OVER
    
    def display_game_over_screen(self):
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
            self.sound_manager.play_music('menu_music')
            self.sound_manager.play_music('menu_music')
    
    def display_high_scores(self):
        self.gameDisplay.fill(self.black)
        
        if hasattr(self, 'menu_bg_icon_faded') and self.menu_bg_icon_faded:
            icon_rect = self.menu_bg_icon_faded.get_rect()
            x = (self.display_width - icon_rect.width) // 2
            y = (self.display_height - icon_rect.height) // 2
            self.gameDisplay.blit(self.menu_bg_icon_faded, (x, y))
        
        panel_width = 700
        panel_height = 450
        panel_x = (self.display_width - panel_width) // 2
        panel_y = (self.display_height - panel_height) // 2
        
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(160)
        panel_surface.fill((0, 0, 0))
        
        pygame.draw.rect(panel_surface, (64, 64, 64), (0, 0, panel_width, panel_height), 3)
        
        self.gameDisplay.blit(panel_surface, (panel_x, panel_y))
        
        font_title = pygame.font.SysFont("comicsansms", 48, True)
        font_text = pygame.font.SysFont("lucidaconsole", 18)
        font_highlight = pygame.font.SysFont("comicsansms", 32, True)
        
        title = font_title.render("HIGH SCORES", True, self.yellow)
        self.gameDisplay.blit(title, (400 - title.get_width() // 2, panel_y + 30))
        
        highest_difficulty = self.game_data.get("highest_difficulty_reached", 0)
        best_scores = self.game_data.get("best_scores_per_difficulty", [0, 0, 0, 0])
        best_score_in_highest_diff = best_scores[highest_difficulty]
        
        if best_score_in_highest_diff > 0:
            highlight_text = f"Your Best in {self.difficulty_modes[highest_difficulty]}: {best_score_in_highest_diff}"
            highlight_render = font_highlight.render(highlight_text, True, self.green)
            self.gameDisplay.blit(highlight_render, (400 - highlight_render.get_width() // 2, panel_y + 80))
        
        high_scores = self.game_data.get("high_scores", [])
        start_y = panel_y + 130 if best_score_in_highest_diff > 0 else panel_y + 100
        
        for i, score_data in enumerate(high_scores[:10]):
            score_text = f"{i+1}. {score_data['score']} - {score_data['difficulty']} - {score_data['date']}"
            text = font_text.render(score_text, True, self.white)
            self.gameDisplay.blit(text, (panel_x + 20, start_y + i * 30))
        
        instruction = font_text.render("Press ESC to return to menu", True, self.yellow)
        self.gameDisplay.blit(instruction, (400 - instruction.get_width() // 2, panel_y + 410))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.current_state = GameStates.MENU
            self.sound_manager.play_music('menu_music')
    
    def display_achievements(self):
        self.gameDisplay.fill(self.black)
        
        if hasattr(self, 'menu_bg_icon_faded') and self.menu_bg_icon_faded:
            icon_rect = self.menu_bg_icon_faded.get_rect()
            x = (self.display_width - icon_rect.width) // 2
            y = (self.display_height - icon_rect.height) // 2
            self.gameDisplay.blit(self.menu_bg_icon_faded, (x, y))
        
        font_title = pygame.font.SysFont("comicsansms", 48, True)
        font_text = pygame.font.SysFont("lucidaconsole", 16)
        font_small = pygame.font.SysFont("lucidaconsole", 14)
        
        if self.reset_confirmation_active:
            panel_width = 600
            panel_height = 400
            panel_x = (self.display_width - panel_width) // 2
            panel_y = (self.display_height - panel_height) // 2
            
            panel_surface = pygame.Surface((panel_width, panel_height))
            panel_surface.set_alpha(200)
            panel_surface.fill((20, 20, 20))
            
            pygame.draw.rect(panel_surface, (128, 128, 128), (0, 0, panel_width, panel_height), 3)
            
            self.gameDisplay.blit(panel_surface, (panel_x, panel_y))
            
            title = font_title.render("RESET PROGRESS", True, self.red)
            self.gameDisplay.blit(title, (400 - title.get_width() // 2, panel_y + 30))
            
            warning_text = font_title.render("WARNING!", True, self.red)
            self.gameDisplay.blit(warning_text, (400 - warning_text.get_width() // 2, panel_y + 90))
            
            confirm_lines = [
                "This will permanently delete ALL your progress:",
                "- All achievements",
                "- High scores", 
                "- Car unlocks",
                "- Settings",
                "",
                "Are you sure you want to continue?"
            ]
            
            for i, line in enumerate(confirm_lines):
                color = self.white if line else self.white
                text = font_text.render(line, True, color)
                self.gameDisplay.blit(text, (400 - text.get_width() // 2, panel_y + 140 + i * 25))
            
            yes_text = font_title.render("Y - YES, DELETE EVERYTHING", True, self.red)
            self.gameDisplay.blit(yes_text, (400 - yes_text.get_width() // 2, panel_y + 310))
            
            no_text = font_title.render("N - NO, KEEP MY DATA", True, self.green)
            self.gameDisplay.blit(no_text, (400 - no_text.get_width() // 2, panel_y + 350))
            
        else:
            panel_width = 700
            panel_height = 450
            panel_x = (self.display_width - panel_width) // 2
            panel_y = (self.display_height - panel_height) // 2
            
            panel_surface = pygame.Surface((panel_width, panel_height))
            panel_surface.set_alpha(160)
            panel_surface.fill((0, 0, 0))
            
            pygame.draw.rect(panel_surface, (64, 64, 64), (0, 0, panel_width, panel_height), 3)
            
            self.gameDisplay.blit(panel_surface, (panel_x, panel_y))
            
            title = font_title.render("ACHIEVEMENTS", True, self.green)
            self.gameDisplay.blit(title, (400 - title.get_width() // 2, panel_y + 30))
            
            for i, achievement in enumerate(self.achievements):
                color = self.green if achievement.unlocked else self.red
                status = "[UNLOCKED]" if achievement.unlocked else "[LOCKED]"
                text = f"{status} {achievement.name}: {achievement.description}"
                rendered_text = font_text.render(text, True, color)
                self.gameDisplay.blit(rendered_text, (panel_x + 20, panel_y + 100 + i * 30))
            
            instructions = [
                "ESC - Back to Menu",
                "R - Reset Progress (WARNING: This will delete all your data!)"
            ]
            
            for i, instruction in enumerate(instructions):
                color = self.yellow if i == 0 else self.red
                text = font_small.render(instruction, True, color)
                self.gameDisplay.blit(text, (panel_x + 20, panel_y + 400 + i * 20))
    
    def display_car_selection(self):
        self.gameDisplay.fill(self.black)
        
        if hasattr(self, 'menu_bg_icon_faded') and self.menu_bg_icon_faded:
            icon_rect = self.menu_bg_icon_faded.get_rect()
            x = (self.display_width - icon_rect.width) // 2
            y = (self.display_height - icon_rect.height) // 2
            self.gameDisplay.blit(self.menu_bg_icon_faded, (x, y))
        
        panel_width = 600
        panel_height = 450
        panel_x = (self.display_width - panel_width) // 2
        panel_y = (self.display_height - panel_height) // 2
        
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(160)
        panel_surface.fill((0, 0, 0))
        
        pygame.draw.rect(panel_surface, (64, 64, 64), (0, 0, panel_width, panel_height), 3)
        
        self.gameDisplay.blit(panel_surface, (panel_x, panel_y))
        
        font_title = pygame.font.SysFont("comicsansms", 48, True)
        font_text = pygame.font.SysFont("lucidaconsole", 20)
        
        title = font_title.render("CAR SELECTION", True, self.blue)
        self.gameDisplay.blit(title, (400 - title.get_width() // 2, panel_y + 30))
        
        preview_y = panel_y + 80
        self.gameDisplay.blit(self.carImg, (400 - self.carImg.get_width() // 2, preview_y))
        
        unlocked_cars = self.game_data["unlocked_cars"]
        car_names = ["Default", "Lamborghini", "Ferrari", "Rolls Royce"]

        for i, car_index in enumerate(unlocked_cars):
            color = self.yellow if car_index == self.current_car else self.white
            car_text = f"{car_names[car_index]}"
            if car_index == self.current_car:
                car_text = f"> {car_text} <"
            
            text = font_text.render(car_text, True, color)
            self.gameDisplay.blit(text, (400 - text.get_width() // 2, panel_y + 200 + i * 40))
        
        instructions = [
            "A/D or LEFT/RIGHT - Navigate",
            "SPACE - Select Car",
            "ESC - Back to Menu"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_text.render(instruction, True, self.white)
            self.gameDisplay.blit(text, (400 - text.get_width() // 2, panel_y + 360 + i * 25))

    def display_message(self, msg):
        """Display a message to the user (currently just triggers game over)"""
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

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render(f"SpeedyHighway v{__version__}", True, self.white)
        self.gameDisplay.blit(text, (600, 500))
        text = font.render("Thanks & Regards,", True, self.white)
        self.gameDisplay.blit(text, (600, 520))
        text = font.render("Tanay Vidhate", True, self.white)
        self.gameDisplay.blit(text, (600, 540))
        text = font.render("(WARlord05)", True, self.white)
        self.gameDisplay.blit(text, (600, 560))

    def check_speed_demon_achievement(self):
        if self.current_difficulty >= 2:
            if self.current_difficulty == 2:
                return self.enemy_car_speed >= 18
            elif self.current_difficulty == 3:
                return self.enemy_car_speed >= 20
        return False
    
    def check_speed_god_achievement(self):
        if self.current_difficulty == 3:
            return self.enemy_car_speed >= 40
        return False
    
    def handle_achievements_events(self, event):
        if event.type == pygame.KEYDOWN:
            if self.reset_confirmation_active:
                if event.key == pygame.K_y:
                    self.reset_progress()
                    self.reset_confirmation_active = False
                    self.sound_manager.play_sound('menu_select')
                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    self.reset_confirmation_active = False
                    self.sound_manager.play_sound('menu_select')
            else:
                if event.key == pygame.K_ESCAPE:
                    self.current_state = GameStates.MENU
                    self.sound_manager.play_music('menu_music')
                elif event.key == pygame.K_r:
                    self.reset_confirmation_active = True
                    self.sound_manager.play_sound('menu_select')
    
    def reset_progress(self):
        self.create_default_game_data()
        self.save_game_data()

        self.load_game_data()
        

        self.current_difficulty = self.game_data.get("difficulty", 1)
        self.current_car = self.game_data.get("selected_car", 0)
        self.games_played = self.game_data.get("games_played", 0)
        self.total_playtime = self.game_data.get("total_playtime", 0)
        self.best_streak = self.game_data.get("best_streak", 0)
        self.current_streak = 0
        
        self.init_achievements()

        self.reload_car_image()
        
        self.daily_challenge = self.generate_daily_challenge()
        
        print("Progress reset successfully!")
    
if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()
