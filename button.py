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

    def __init__(self, position, button_color, text_color, font, text, hover_color):
        self.position = position
        self.button_color = button_color
        self.text_color = text_color
        self.font = font
        self.text = text
        self.hover_color = hover_color
        self.bound = None
        # self.click_sound = pg.mixer.Sound('filepath/.wav')

    '''
    render
    -------------
    When called it renders the button with interactive functionality.
    '''
    def render(self, window): # Renders button onto window
        text_surface = self.font.render(self.text, True, self.text_color) # Creates text surface to be imposed on button
        self.bound = text_surface.get_rect(center=self.position) # Put position origin point in the middle of the button
        mouse_position = pg.mouse.get_pos() # Gets mouse position
        hovered = self.bound.collidepoint(mouse_position) # If mouse is over button
        color = self.hover_color if hovered else self.button_color # Changes color render if mouse is over
        pg.draw.rect(window, color, self.bound)
        window.blit(text_surface, self.bound)


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
