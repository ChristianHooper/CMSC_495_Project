import pygame as pg



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

    '''
    play_bgm
    -------------
    Plays back ground music when called.
    '''
    def play_bgm(self):
        print()
        #pg.mixer.music.load(self.bgm_path)
        #pg.mixer.music.play(loops=-1)

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
        self.line_clear_sound.play()

    '''
    play_game_over
    -------------
    Plays game over music when called.
    '''
    def play_game_over(self):
        self.game_over_sound.play()

    '''
    play_rotate
    -------------
    Plays rotation sound when called.
    '''
    def play_rotate(self):
        self.rotate_sound.play()
