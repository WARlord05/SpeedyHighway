# Music Files Required

Place the following music files in this directory (`assets/music/`):

## Required Music Files

### menu_music.mp3
- **Purpose**: Background music for menu screens
- **Loop**: Should be seamless loop for continuous playback
- **Style**: Energetic, upbeat menu music
- **Duration**: 1-3 minutes (will loop automatically)

### game_music.mp3
- **Purpose**: Background music during gameplay
- **Loop**: Should be seamless loop for continuous playback
- **Style**: Fast-paced, driving music to match racing gameplay
- **Duration**: 2-4 minutes (will loop automatically)

## Music Controls

- **[** key: Decrease music volume
- **]** key: Increase music volume  
- **N** key: Mute/unmute music
- **+/-** keys: Adjust sound effects volume
- **M** key: Mute/unmute all sound effects

## Music Implementation Features

✅ **Automatic Music Transitions**: Music changes based on game state
✅ **Volume Controls**: Separate music and sound effect volume controls
✅ **Seamless Looping**: Music loops continuously without interruption
✅ **State-Based Playback**: Different music for menu vs gameplay
✅ **Memory Management**: Proper cleanup when game exits

## File Format Requirements

- **Format**: MP3 (recommended) or OGG
- **Quality**: 128-192 kbps (balance between quality and file size)
- **Channels**: Stereo or Mono
- **Sample Rate**: 44.1 kHz standard

## Current Implementation Status

🎵 **Background Music System**: ✅ Complete
🎛️ **Volume Controls**: ✅ Complete
🔄 **State Transitions**: ✅ Complete
🎮 **Menu Integration**: ✅ Complete

## Notes

- Music files will be loaded automatically when the game starts
- If music files are missing, the game will continue without background music
- Music volume is independent of sound effects volume
- All music controls are shown on the main menu
