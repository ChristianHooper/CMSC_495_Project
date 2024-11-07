import pygame as pg
import dataStructures as ds

class Button:
    '''
    The class object used to represent basic gui element throughout the game.
    Changes to object should be made through the direct object class, not this gui element class.
    Blit Order: OtherSurfaces -> Buttons -> Text -> Surface -> Border -> Window
    ----------
    Attributes
    ----------
    self.surface :           The surface the composed the gui element. |(pg.surface)|
    self.position :          Where the gui element surface renders on the main window. |[int, int]]|
    self.transparent_color : The color value that when drawn will render the surface transparent. |(int, int, int)|
    self.color_fill :        The default surface color of the gui element, |(int, int, int)|
    self.border_size :       Width & Height of the border around the gui main surface. |pg.surface|
    self.border_color :      The fill color of the boarder. |(int, int, int)|
    self.font_position :     Where the font render on the main surface. |[int, int]|
    self.font:               The single default font object to be rendered onto main surface |pygame.font.Font object|
    self.text:               String text with renderer by font object. |'string'|
    self.text_color:         Color of the text to be rendered. |(int, int, int)|
    '''

    def __init__(self,
                window,
                position,
                xy_length,
                transparent_color=(255,255,255),
                fill_color=(128,128,255),
                border_size=0,
                border_color=(255,255,255),
                font=ds.FONTS['default_large'],
                font_position=[0,0],
                text_color=(255,255,255),
                text=''
    ):

        # Surface base frame
        self.surface = pg.Surface(zy_length, pg.SRCALPHA)
        self.position = position
        self.bounds = xy_length
        self.fill_color = fill_color
        self.surface.set_colorkey(transparent_color) # Default white (255, 255, 255)

        # Rendered text on surface
        self.font_position = font_position
        self.text_color = text_color
        self.text = text
        self.font = font.render(self.text, True, self.text_color)
        self.surface.blit(self.font, self.position)

        # Border backing frame
        self.border_size = border_size
        self.border = pg.Surface([self.bounds[0] + 2*self.border_size, self.bounds[0] + 2*self.border_size], pg.SRCALPHA)
        self.border_color = border_color
        self.border.fill(self.border_color)
        self.border.blit(self.surface, (self.border_size, self.border_size)) # Blit main surface onto border

        window.blit(self.border, self.position) # Composed gui element for rendering


    # Blits any elements or changes into the whole gui element to be rendered onto the game surface window.
    def blit_update(window, element_sequence=[[None,None]]):
        # Takes a sequence list an blit elements onto the main surface [[pg.surface, position],...]
        if element_sequence[0][0] != None: self.surface.blits(element_sequence)

        self.surface.blit(self.font, self.position) # Blit local single font to main surface
        self.border.blit(self.surface, (self.border_size, self.border_size)) # Blit main surface onto border
        window.blit(self.border, self.position) # Blit whole gui element onto window for rendering
