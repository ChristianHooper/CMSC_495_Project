import pygame as pg
import random



'''
The default sound controller for creating both BGM and sounds effects.

----------
Attributes
----------
bgm_path :         Path to background music. |.mp3|
line_clear_sound : Mixer sound object played when a line is clear in tetris. |.wav|
game_over_sound :  Mixer sound object played when a tetris game ends. |.wav|
rotate_sound :     Mixer sound object played when a tetrominoes rotates. |.wav|

'''

class SoundController:
    def __init__(self):
        pg.mixer.init() # Initializes sound object

        # Use `pygame.mixer.music` for the background music
        self.bgm_path = 'sounds/background_music.mp3'  # File path to the background music
        self.line_clear_sound = pg.mixer.Sound('sounds/clear_line.wav')
        self.game_over_sound = pg.mixer.Sound('sounds/game_over.wav')
        self.rotate_sound = pg.mixer.Sound('sounds/rotate.wav')
        self.drop_sound = pg.mixer.Sound('sounds/drop_sound.wav')
        self.level_sound = pg.mixer.Sound('sounds/levelup_sound.wav')
        self.start_sound = pg.mixer.Sound('sounds/start_sound.wav')
        self.pause_sound = pg.mixer.Sound('sounds/pause_sound.wav')

        self.bgm = { # Holds back ground music file locations
            'bear':         'audio/Bear.mp3',
            'gummy':        'audio/Gummy.mp3',
            'overflowin':   'audio/Overflowin.mp3',
            'vendor':       'audio/Vendor.mp3',
            'Wax':          'audio/Wax.mp3',
            'Classic':      'sounds/background_music.mp3'
        }
        self.volume = 0.02

        # Event for music transition
        self.bgm_end_event = pg.USEREVENT + 1
        pg.mixer.music.set_endevent(self.bgm_end_event)

    '''
    play_bgm
    -------------
    Plays back ground music when called.
    '''
    def play_bgm(self):
        selection = random.choice(list(self.bgm.values()))
        pg.mixer.music.load(selection)
        pg.mixer.music.set_volume(self.volume)
        pg.mixer.music.play()
        #pg.mixer.music.play(loops=-1)

    def bgm_ending(self): self.play_bgm()

    '''
    stop_bgm
    -------------
    Stops playing back ground music when called.
    '''
    def stop_bgm(self):
        pg.mixer.music.stop()

    '''
    play_line_clear
    -------------
    Plays line clearing sound when called.
    '''
    def play_line_clear(self):
        self.line_clear_sound.set_volume(self.volume)
        self.line_clear_sound.play()

    '''
    play_game_over
    -------------
    Plays game over music when called.
    '''
    def play_game_over(self):
        self.game_over_sound.set_volume(self.volume)
        self.game_over_sound.play()

    '''
    play_rotate
    -------------
    Plays rotation sound when called.
    '''
    def play_rotate(self):
        self.rotate_sound.set_volume(self.volume)
        self.rotate_sound.play()

    def play_drop(self): self.drop_sound.set_volume(self.volume); self.drop_sound.play()

    def play_level_up(self): self.level_sound.set_volume(self.volume); self.level_sound.play()

    def play_start(self): self.start_sound.set_volume(self.volume); self.start_sound.play()

    def play_pause(self): self.pause_sound.set_volume(self.volume); self.pause_sound.play()