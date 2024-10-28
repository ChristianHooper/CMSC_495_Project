import pygame as pg
import dataStructures as ds

def menu(window, clock, window_size):

    running_menu = True
    large_font = pg.font.Font(None, size=64) # File path to custom font: if possible add later (https://www.dafont.com/)
    title_text = large_font.render('G5-Tetris', True, ds.COLOR['white']) # Title text attributes
    title_position = title_text.get_rect(center=(window_size[0]/2, window_size[1]/10)) # Position of where text will render

    while running_menu:
        for event in pg.event.get():
            if event.type == pg.QUIT: return None

        window.fill(ds.COLOR['black'])
        window.blit(title_text, title_position)
        pg.display.flip()
