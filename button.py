import pygame as pg
import dataStructures as ds

class Button:
    '''
    The class object used to represent a button throughout the game.

    ----------
    Attributes
    ----------
    position :     Two int tuple 0-> screen size
    button_color : Three int tuple 0->255
    text_color :   Three int tuple 0->255
    font :         pygame.font.Font object
    test :         string
    hover_color :  Three int tuple 0->255
    '''

    def __init__(self, position, button_color, text_color, font, text, hover_color, text_outline=False, outline_size=8, inflate=[0,0]):
        self.position = position
        self.button_color = button_color
        self.text_color = text_color
        self.font = font
        self.text = text
        self.hover_color = hover_color
        self.bound = None
        self.text_outline = text_outline
        self.outline_size = outline_size
        self.inflate = inflate
        # self.click_sound = pg.mixer.Sound('filepath/.wav')

    '''
    render
    -------------
    When called it renders the button with interactive functionality.
    '''
    def render(self, window): # Renders button onto window
        text_surface = self.font.render(self.text, True, self.text_color) # Creates text surface to be imposed on button
        text_rect = text_surface.get_rect(center=self.position) # Put position origin point in the middle of the button
        back_rect = text_rect.inflate(8, 8)
        self.bound = text_rect.inflate(self.inflate[0], self.inflate[1])
        mouse_position = pg.mouse.get_pos() # Gets mouse position
        hovered = self.bound.collidepoint(mouse_position) # If mouse is over button
        color = self.hover_color if hovered else self.button_color # Changes color render if mouse is over
        if not self.text_outline: pg.draw.rect(window, color, self.bound)
        elif self.text_outline:
            pg.draw.rect(window, color, self.bound, self.outline_size)
            transparent_rect = pg.Surface((back_rect.width, back_rect.height), pg.SRCALPHA)
            pg.draw.rect(transparent_rect, (86, 77, 140, 64), transparent_rect.get_rect())
            window.blit(transparent_rect, back_rect)
        window.blit(text_surface, text_rect)


    '''
    render
    -------------
    Returns boolean if the user clicked on the button with the mouse or not.
    '''
    def clicked(self, mouse_click):
        if self.bound.collidepoint(mouse_click):
            #self.click_sound.play() # Play sound when clicked
            return True
        else: return False
