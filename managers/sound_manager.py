"""
Sound Manager Module
SpeedyHighway v1.2.0

Checks And Handles all sound effects
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

from game.utils import get_resource_path


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
