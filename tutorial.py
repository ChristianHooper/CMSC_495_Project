import pygame as pg
import dataStructures as ds
from button import Button

def tutorial(window, clock, window_size):
    running_menu = True
    large_font = ds.FONTS['default_large']
    
    # Font settings for tutorial text
    title_font = pg.font.Font(None, 48)
    header_font = pg.font.Font(None, 36)
    text_font = pg.font.Font(None, 28)
    
    # Create text elements
    title_text = title_font.render("How to Play", True, ds.COLOR['white'])
    title_rect = title_text.get_rect(center=(window_size[0]/2, window_size[1]*0.1))
    
    # Single Player Text
    sp_header = header_font.render("Single Player Controls (WASD)", True, ds.COLOR['green'])
    sp_controls = [
        "W - Rotate piece",
        "A - Move left",
        "S - Move down faster",
        "D - Move right",
        "Space - Pause Game"
    ]
    
    # Multiplayer Text
    mp_header = header_font.render("Multiplayer Controls (Arrow Keys)", True, ds.COLOR['red'])
    mp_controls = [
        "Up Arrow   - Rotate piece",
        "Left Arrow - Move left",
        "Down Arrow - Move down faster",
        "Right Arrow - Move right"
        
    ]
    
    # Create surfaces for control text
    sp_text_surfaces = [text_font.render(text, True, ds.COLOR['white']) for text in sp_controls]
    mp_text_surfaces = [text_font.render(text, True, ds.COLOR['white']) for text in mp_controls]

    back_button = Button(
        position=(window_size[0]/1.2, window_size[1]/1.2),
        button_color=ds.COLOR['green'],
        text_color=ds.COLOR['red'],
        font=large_font,
        text='Main Menu',
        hover_color=ds.COLOR['white'],
    )

    while running_menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return None

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_position = pg.mouse.get_pos()
                    if back_button.clicked(mouse_position):
                        return ds.GAME_STATE['menu']

        # Render order
        window.fill(ds.COLOR['black'])
        
        # Draw title
        window.blit(title_text, title_rect)
        
        # Draw Single Player section
        window.blit(sp_header, (window_size[0]*0.2, window_size[1]*0.25))
        for i, text_surface in enumerate(sp_text_surfaces):
            window.blit(text_surface, (window_size[0]*0.2, window_size[1]*0.35 + i*30))
            
        # Draw Multiplayer section
        window.blit(mp_header, (window_size[0]*0.2, window_size[1]*0.6))
        for i, text_surface in enumerate(mp_text_surfaces):
            window.blit(text_surface, (window_size[0]*0.2, window_size[1]*0.7 + i*30))
        
        # Draw button
        back_button.render(window)
        
        pg.display.flip()