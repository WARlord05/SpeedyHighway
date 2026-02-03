"""
Core Game Module - CarRacing Class
SpeedyHighway v1.2.0
"""

import os
import sys
import random
import hashlib
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

from game.config import (
    __version__, DISPLAY_WIDTH, DISPLAY_HEIGHT, BLACK, WHITE, GREEN, RED, BLUE, YELLOW,
    DIFFICULTY_MODES, DIFFICULTY_MULTIPLIERS, SCORE_MULTIPLIERS, LANE_POSITIONS,
    ROAD_MIN_X, ROAD_MAX_X, AVAILABLE_CARS, CAR_WIDTH, CAR_START_X, ENEMY_CAR_WIDTH,
    ENEMY_CAR_HEIGHT, ENEMY_START_Y, BASE_ENEMY_SPEED, BASE_BG_SPEED, MAX_ENEMY_SPEEDS,
    MAX_BG_SPEEDS, SPECIAL_CAR_FRAMES, SPECIAL_CAR_ANIMATION_SPEED, KEY_REPEAT_DELAY,
    DAILY_CHALLENGES
)
from game.states import GameStates
from game.utils import get_resource_path
from managers.sound_manager import SoundManager
from managers.data_manager import load_game_data, save_game_data, create_default_game_data
from managers.achievement_manager import Achievement, generate_daily_challenge
from screens.menu import display_main_menu, display_seed_input, display_quit_confirmation
from screens.game_screen import display_enhanced_hud, display_pause_menu, display_countdown_timer
from screens.game_over import display_game_over_screen
from screens.high_scores import display_high_scores
from screens.achievements import display_achievements
from screens.car_selection import display_car_selection


class CarRacing:

    def __init__(self):
        pygame.init()
        self._set_icon()
        
        # Display
        self.display_width, self.display_height = DISPLAY_WIDTH, DISPLAY_HEIGHT
        self.black, self.white, self.green = BLACK, WHITE, GREEN
        self.red, self.blue, self.yellow = RED, BLUE, YELLOW
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        
        # Entropy system
        self._entropy_seed = None
        self._game_random = random.Random()
        self._replay_data = []
        self._is_replay_mode = False
        
        # Managers
        self.sound_manager = SoundManager()
        
        # State
        self.current_state = GameStates.MENU
        self.reset_confirmation_active = False
        self.quit_confirmation_active = False
        self.fullscreen_mode = False
        self.seed_input_active = False
        self.seed_input_text = ""
        
        # Load data and initialize
        self.game_data = load_game_data()
        self._init_achievements()
        self.daily_challenge, _ = generate_daily_challenge(self.game_data)
        save_game_data(self.game_data)
        self.initialize()
        self.sound_manager.play_music('menu_music')

    def _set_icon(self):
        try:
            icon_path = os.path.join("assets", "ico.png")
            if os.path.exists(icon_path):
                pygame.display.set_icon(pygame.image.load(icon_path))
        except Exception:
            pass

    def initialize(self, seed=None):
        self.crashed = self.paused = self.show_countdown = False
        self.unpause_timer = 0
        
        # Entropy
        if seed:
            self._set_seed(seed)
        elif not self._entropy_seed:
            self._generate_seed()
        
        # Scores
        self.base_score = self.bonus_score = self.near_miss_count = 0
        self.lane_change_count = self.survival_time = self.total_score = 0
        self.enemy_car_near_miss_counted = False
        self.near_miss_flash_timer = 0
        self.engine_started = False
        
        # Input
        self.last_key_press_time = {"left": 0, "right": 0}
        self.key_repeat_delay = KEY_REPEAT_DELAY
        self.key_pressed_last_frame = {"left": False, "right": False}
        
        # Settings from saved data
        self.difficulty_modes = DIFFICULTY_MODES
        self.current_difficulty = self.game_data.get("difficulty", 1)
        self.available_cars = AVAILABLE_CARS
        self.current_car = self.game_data.get("selected_car", 0)
        self.games_played = self.game_data.get("games_played", 0)
        
        # Special car animation
        self.special_car_frame = 0
        self.special_car_animation_timer = 0
        self.special_car_animation_speed = SPECIAL_CAR_ANIMATION_SPEED
        
        # Load assets
        self._load_car()
        self._load_enemy()
        self._load_background()
        self.count = 0

    def _load_car(self):
        car_file = self.available_cars[self.current_car]
        if car_file == "special":
            try:
                self.carImg_spc_frames = [
                    pygame.image.load(get_resource_path(os.path.join("assets", "spc", f"spc{i}.png")))
                    for i in range(SPECIAL_CAR_FRAMES)
                ]
                self.carImg = self.carImg_spc_frames[0]
            except pygame.error:
                self.carImg = pygame.image.load(get_resource_path(os.path.join("assets", "car_yellow.png")))
        else:
            self.carImg = pygame.image.load(get_resource_path(os.path.join("assets", car_file)))
        self.car_x_coordinate = CAR_START_X
        self.car_y_coordinate = int(self.display_height * 0.8)
        self.car_width = CAR_WIDTH

    def _load_enemy(self):
        self.enemy_car = pygame.image.load(get_resource_path(os.path.join("assets", "car_black.png")))
        self.enemy_car_startx = self._choice(LANE_POSITIONS)
        self.enemy_car_starty = ENEMY_START_Y
        mult = DIFFICULTY_MULTIPLIERS[self.current_difficulty]
        self.enemy_car_speed = int(BASE_ENEMY_SPEED * mult)
        self.enemy_car_width, self.enemy_car_height = ENEMY_CAR_WIDTH, ENEMY_CAR_HEIGHT

    def _load_background(self):
        self.bgImg = pygame.image.load(get_resource_path(os.path.join("assets", "back.jpg")))
        self.bgImg = pygame.transform.scale(self.bgImg, (self.display_width, self.display_height))
        self.bg_y1, self.bg_y2 = 0, -self.display_height
        self.bg_speed = int(BASE_BG_SPEED * DIFFICULTY_MULTIPLIERS[self.current_difficulty])
        
        try:
            icon = pygame.image.load(get_resource_path(os.path.join("assets", "ico.png")))
            scale = max(self.display_width / icon.get_width(), self.display_height / icon.get_height())
            self.menu_bg_icon = pygame.transform.scale(icon, (int(icon.get_width() * scale), int(icon.get_height() * scale)))
            self.menu_bg_icon_faded = self.menu_bg_icon.copy()
            overlay = pygame.Surface(self.menu_bg_icon.get_size())
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.menu_bg_icon_faded.blit(overlay, (0, 0))
        except Exception:
            self.menu_bg_icon = self.menu_bg_icon_faded = None

    def _generate_seed(self):
        ts = int(time.time() * 1000000)
        self._entropy_seed = int(hashlib.md5(f"{ts}{os.getpid()}{id(self)}".encode()).hexdigest()[:8], 16)
        self._game_random.seed(self._entropy_seed)
        print(f"Generated new entropy seed: {self._entropy_seed}")

    def _set_seed(self, seed):
        self._entropy_seed = seed
        self._game_random.seed(seed)
        print(f"Set entropy seed to: {seed}")

    def _choice(self, choices):
        if self._is_replay_mode and self._replay_data:
            return self._replay_data.pop(0)
        choice = self._game_random.choice(choices)
        if not self._is_replay_mode:
            self._replay_data.append(choice)
        return choice

    def get_entropy_seed(self):
        return self._entropy_seed

    def _init_achievements(self):
        self.achievements = [
            Achievement("first_game", "First Drive", "Play your first game", lambda: self.games_played >= 1),
            Achievement("score_1000", "Road Warrior", "Score 1000 points", lambda: self.total_score >= 1000),
            Achievement("score_5000", "Highway Legend", "Score 5000 points", lambda: self.total_score >= 5000),
            Achievement("near_miss_10", "Close Call", "Get 10 near misses", lambda: self.near_miss_count >= 10),
            Achievement("lane_master", "Lane Master", "Change lanes 50 times", lambda: self.lane_change_count >= 50),
            Achievement("survivor", "Survivor", "Survive 2 minutes", lambda: self.survival_time >= 7200),
            Achievement("speed_demon", "Speed Demon", "Reach max speed", lambda: self._check_speed_demon()),
            Achievement("speed_god", "Speed God", "40 speed in Insane", lambda: self._check_speed_god()),
            Achievement("perfect_game", "Perfect Game", "Complete daily challenge", lambda: self.daily_challenge.get("completed", False))
        ]
        for a in self.achievements:
            a.unlocked = self.game_data.get("achievements", {}).get(a.id, False)

    def _check_achievements(self):
        changed = False
        for a in self.achievements:
            if not a.unlocked and a.condition():
                a.unlocked = True
                self.game_data["achievements"][a.id] = True
                self.sound_manager.play_sound('achievement')
                changed = True
        if changed:
            save_game_data(self.game_data)

    def _check_speed_demon(self):
        return self.current_difficulty >= 2 and self.enemy_car_speed >= (18 if self.current_difficulty == 2 else 20)

    def _check_speed_god(self):
        return self.current_difficulty == 3 and self.enemy_car_speed >= 40

    def _calc_score(self):
        self.base_score = self.count
        bonus = self.near_miss_count * 10 + self.lane_change_count * 2 + (self.survival_time // 600) * 50
        self.total_score = int((self.base_score + bonus) * SCORE_MULTIPLIERS[self.current_difficulty])

    def _check_near_miss(self):
        if abs(self.car_x_coordinate - self.enemy_car_startx) <= 50 and abs(self.car_y_coordinate - self.enemy_car_starty) <= 100:
            if not self.enemy_car_near_miss_counted:
                self.near_miss_count += 1
                self.enemy_car_near_miss_counted = True
                self.near_miss_flash_timer = 30
                self.sound_manager.play_sound('near_miss')
        elif self.enemy_car_starty > self.car_y_coordinate + 50:
            self.enemy_car_near_miss_counted = False

    def _check_car_unlocks(self):
        unlocks = [(500, 1), (1500, 2), (3000, 3)]
        for score, idx in unlocks:
            if self.total_score >= score and idx not in self.game_data["unlocked_cars"]:
                self.game_data["unlocked_cars"].append(idx)
                save_game_data(self.game_data)
                self.sound_manager.play_sound('car_unlock')

    def racing_window(self):
        self._setup_display()
        self._game_loop()

    def _setup_display(self):
        flags = pygame.FULLSCREEN if self.fullscreen_mode else 0
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height), flags)
        pygame.display.set_caption(f'Speedy Highway v{__version__}')
        self._set_icon()

    def _toggle_fullscreen(self):
        self.fullscreen_mode = not self.fullscreen_mode
        self._setup_display()
        self.sound_manager.play_sound('menu_select')

    def _game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_confirmation_active = True
                elif event.type == pygame.USEREVENT + 1:
                    self.sound_manager.start_engine_loop()
                elif self.quit_confirmation_active:
                    self._handle_quit_confirm(event)
                else:
                    self._handle_event(event)
            
            self._update_state()
            pygame.display.update()
            self.clock.tick(60)

    def _handle_quit_confirm(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                self.sound_manager.cleanup()
                pygame.quit()
                sys.exit()
            elif event.key in (pygame.K_n, pygame.K_ESCAPE):
                self.quit_confirmation_active = False

    def _handle_event(self, event):
        handlers = {
            GameStates.MENU: self._handle_menu,
            GameStates.PLAYING: self._handle_game,
            GameStates.CAR_SELECTION: self._handle_car_select,
            GameStates.ACHIEVEMENTS: self._handle_achievements,
        }
        handler = handlers.get(self.current_state)
        if handler:
            handler(event)

    def _update_state(self):
        updates = {
            GameStates.MENU: self._update_menu,
            GameStates.PLAYING: self._update_game,
            GameStates.PAUSED: self._update_pause,
            GameStates.GAME_OVER: self._update_game_over,
            GameStates.HIGH_SCORES: self._update_high_scores,
            GameStates.ACHIEVEMENTS: self._update_achievements,
            GameStates.CAR_SELECTION: self._update_car_selection,
        }
        updates.get(self.current_state, lambda: None)()

    def _handle_menu(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if self.seed_input_active:
            self._handle_seed_input(event)
            return
        
        key_actions = {
            pygame.K_SPACE: self._start_game,
            pygame.K_h: lambda: setattr(self, 'current_state', GameStates.HIGH_SCORES),
            pygame.K_a: lambda: setattr(self, 'current_state', GameStates.ACHIEVEMENTS),
            pygame.K_c: lambda: setattr(self, 'current_state', GameStates.CAR_SELECTION),
            pygame.K_d: self._cycle_difficulty,
            pygame.K_s: lambda: (setattr(self, 'seed_input_active', True), setattr(self, 'seed_input_text', "")),
            pygame.K_f: self._toggle_fullscreen,
            pygame.K_m: lambda: self.sound_manager.set_master_volume(0 if self.sound_manager.master_volume > 0 else 0.7),
            pygame.K_n: lambda: self.sound_manager.set_music_volume(0 if self.sound_manager.music_volume > 0 else 0.7),
            pygame.K_ESCAPE: lambda: setattr(self, 'quit_confirmation_active', True),
        }
        action = key_actions.get(event.key)
        if action:
            self.sound_manager.play_sound('menu_select')
            action()

    def _handle_seed_input(self, event):
        if event.key == pygame.K_RETURN:
            try:
                self._set_seed(int(self.seed_input_text.strip())) if self.seed_input_text.strip() else self._generate_seed()
            except ValueError:
                self._generate_seed()
            self.seed_input_active = False
        elif event.key == pygame.K_ESCAPE:
            self.seed_input_active = False
        elif event.key == pygame.K_BACKSPACE:
            self.seed_input_text = self.seed_input_text[:-1]
        elif event.unicode.isdigit() or (event.unicode == '-' and not self.seed_input_text):
            if len(self.seed_input_text) < 15:
                self.seed_input_text += event.unicode

    def _start_game(self):
        self.current_state = GameStates.PLAYING
        self.initialize()
        self.sound_manager.play_engine_sound(self.current_car)
        self.sound_manager.play_music('game_music')
        self.engine_started = True

    def _cycle_difficulty(self):
        self.current_difficulty = (self.current_difficulty + 1) % len(DIFFICULTY_MODES)
        self.game_data["difficulty"] = self.current_difficulty
        save_game_data(self.game_data)

    def _update_menu(self):
        self.gameDisplay.fill(self.black)
        if self.quit_confirmation_active:
            display_quit_confirmation(self.gameDisplay, self)
        elif self.seed_input_active:
            display_seed_input(self.gameDisplay, self)
        else:
            display_main_menu(self.gameDisplay, self)

    def _handle_game(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.paused:
                    self.paused = False
                    self.show_countdown = True
                    self.unpause_timer = 180
                else:
                    self.paused = True
            elif event.key == pygame.K_f:
                self._toggle_fullscreen()

    def _update_game(self):
        if self.crashed:
            self._end_game()
            return
        
        if self.show_countdown:
            self.unpause_timer -= 1
            if self.unpause_timer <= 0:
                self.show_countdown = False

        if self.paused:
            display_pause_menu(self.gameDisplay)
        elif self.show_countdown:
            self._draw_game_frame()
            display_countdown_timer(self.gameDisplay, self.unpause_timer)
        else:
            self._run_game_logic()

    def _run_game_logic(self):
        self._draw_game_frame()
        
        # Move enemy
        self.enemy_car_starty += self.enemy_car_speed
        if self.enemy_car_starty > self.display_height:
            self.enemy_car_starty = -self.enemy_car_height
            self.enemy_car_startx = self._choice(LANE_POSITIONS)
            self.enemy_car_near_miss_counted = False

        # Update game state
        self.count += 1
        self.survival_time += 1
        self._calc_score()
        self._check_near_miss()
        self._check_achievements()
        self._check_car_unlocks()
        self._handle_input()
        self._update_special_car()
        
        if self.engine_started:
            self.sound_manager.update_engine_volume(min(1.0, self.enemy_car_speed / 20.0))

        # Increase difficulty
        if self.count % 100 == 0:
            max_speed = MAX_ENEMY_SPEEDS[self.current_difficulty]
            if max_speed is None or self.enemy_car_speed < max_speed:
                self.enemy_car_speed += 1
            max_bg = MAX_BG_SPEEDS[self.current_difficulty]
            if max_bg is None or self.bg_speed < max_bg:
                self.bg_speed += 1

        # Check collisions
        if self.car_x_coordinate < ROAD_MIN_X or self.car_x_coordinate > ROAD_MAX_X:
            self._crash('off_road')
        elif self._check_collision():
            self._crash('crash', 1.0)

    def _draw_game_frame(self):
        self.gameDisplay.fill(self.black)
        self._draw_background()
        self.gameDisplay.blit(self.enemy_car, (self.enemy_car_startx, self.enemy_car_starty))
        self.gameDisplay.blit(self.carImg, (self.car_x_coordinate, self.car_y_coordinate))
        display_enhanced_hud(self.gameDisplay, self)

    def _draw_background(self):
        self.gameDisplay.blit(self.bgImg, (0, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (0, self.bg_y2))
        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed
        if self.bg_y1 >= self.display_height:
            self.bg_y1 = self.bg_y2 - self.display_height
        if self.bg_y2 >= self.display_height:
            self.bg_y2 = self.bg_y1 - self.display_height

    def _check_collision(self):
        if self.car_y_coordinate + 20 < self.enemy_car_starty + self.enemy_car_height and self.car_y_coordinate + 50 > self.enemy_car_starty:
            car_left, car_right = self.car_x_coordinate + 10, self.car_x_coordinate + self.car_width - 10
            enemy_left, enemy_right = self.enemy_car_startx + 10, self.enemy_car_startx + self.enemy_car_width - 10
            return car_right > enemy_left and car_left < enemy_right
        return False

    def _crash(self, sound, vol=None):
        self.sound_manager.play_sound(sound, volume_override=vol)
        self.sound_manager.stop_engine_sound()
        self.engine_started = False
        self.crashed = True

    def _handle_input(self):
        keys = pygame.key.get_pressed()
        for direction, key_codes in [("left", [pygame.K_LEFT, pygame.K_a]), ("right", [pygame.K_RIGHT, pygame.K_d])]:
            pressed = any(keys[k] for k in key_codes)
            if pressed:
                if not self.key_pressed_last_frame[direction] or self.count - self.last_key_press_time[direction] >= self.key_repeat_delay:
                    self._move_left() if direction == "left" else self._move_right()
                    self.last_key_press_time[direction] = self.count
                self.key_pressed_last_frame[direction] = True
            else:
                self.key_pressed_last_frame[direction] = False

    def _move_left(self):
        moves = {295: 215, 415: 295, 495: 415, 215: 175}
        new_x = moves.get(self.car_x_coordinate)
        if new_x:
            self.car_x_coordinate = new_x
            if new_x in LANE_POSITIONS:
                self.lane_change_count += 1

    def _move_right(self):
        moves = {215: 295, 295: 415, 415: 495, 495: 535}
        new_x = moves.get(self.car_x_coordinate)
        if new_x:
            self.car_x_coordinate = new_x
            if new_x in LANE_POSITIONS:
                self.lane_change_count += 1

    def _update_special_car(self):
        if self.current_car == 3 and hasattr(self, 'carImg_spc_frames'):
            self.special_car_animation_timer += 1
            if self.special_car_animation_timer >= self.special_car_animation_speed:
                self.special_car_animation_timer = 0
                self.special_car_frame = (self.special_car_frame + 1) % len(self.carImg_spc_frames)
                self.carImg = self.carImg_spc_frames[self.special_car_frame]

    def _end_game(self):
        self.sound_manager.stop_engine_sound()
        self.engine_started = False
        self.games_played += 1
        self.game_data["games_played"] = self.games_played
        self.game_data["total_playtime"] = self.game_data.get("total_playtime", 0) + self.survival_time
        
        # Update high scores
        scores = self.game_data.get("high_scores", [])
        scores.append({
            "score": self.total_score,
            "difficulty": DIFFICULTY_MODES[self.current_difficulty],
            "survival_time": self.survival_time // 60,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        scores.sort(key=lambda x: x["score"], reverse=True)
        self.game_data["high_scores"] = scores[:10]
        
        # Check daily challenge
        if self.daily_challenge:
            checks = {"score": self.total_score, "survival": self.survival_time, "near_miss": self.near_miss_count, "lane_change": self.lane_change_count}
            target_type = self.daily_challenge.get("type")
            if checks.get(target_type, 0) >= self.daily_challenge.get("target", 0):
                self.daily_challenge["completed"] = True
                self.game_data["daily_challenge"] = self.daily_challenge
        
        save_game_data(self.game_data)
        self.current_state = GameStates.GAME_OVER

    def _update_pause(self):
        display_pause_menu(self.gameDisplay)

    def _update_game_over(self):
        display_game_over_screen(self.gameDisplay, self)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.current_state = GameStates.MENU
            self.sound_manager.play_music('menu_music')

    def _update_high_scores(self):
        display_high_scores(self.gameDisplay, self)
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.current_state = GameStates.MENU

    def _handle_achievements(self, event):
        if event.type == pygame.KEYDOWN:
            if self.reset_confirmation_active:
                if event.key == pygame.K_y:
                    self._reset_progress()
                    self.reset_confirmation_active = False
                elif event.key in (pygame.K_n, pygame.K_ESCAPE):
                    self.reset_confirmation_active = False
            elif event.key == pygame.K_ESCAPE:
                self.current_state = GameStates.MENU
            elif event.key == pygame.K_r:
                self.reset_confirmation_active = True

    def _update_achievements(self):
        display_achievements(self.gameDisplay, self)

    def _handle_car_select(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self._prev_car()
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._next_car()
            elif event.key == pygame.K_SPACE:
                self._select_car()
            elif event.key == pygame.K_ESCAPE:
                self.sound_manager.stop_engine_sound()
                self.current_state = GameStates.MENU

    def _prev_car(self):
        unlocked = self.game_data["unlocked_cars"]
        idx = unlocked.index(self.current_car)
        self.current_car = unlocked[idx - 1]
        self._load_car()
        self.sound_manager.play_engine_sound(self.current_car, loop=False)

    def _next_car(self):
        unlocked = self.game_data["unlocked_cars"]
        idx = unlocked.index(self.current_car)
        self.current_car = unlocked[(idx + 1) % len(unlocked)]
        self._load_car()
        self.sound_manager.play_engine_sound(self.current_car, loop=False)

    def _select_car(self):
        self.game_data["selected_car"] = self.current_car
        save_game_data(self.game_data)
        self.sound_manager.stop_engine_sound()
        self.current_state = GameStates.MENU

    def _update_car_selection(self):
        self._update_special_car()
        display_car_selection(self.gameDisplay, self)

    def _reset_progress(self):
        self.game_data = create_default_game_data()
        save_game_data(self.game_data)
        self.current_difficulty = 1
        self.current_car = 0
        self.games_played = 0
        self._init_achievements()
        self._load_car()
        self.daily_challenge, _ = generate_daily_challenge(self.game_data)


if __name__ == '__main__':
    CarRacing().racing_window()
