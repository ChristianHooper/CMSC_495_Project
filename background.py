from dataStructures import COLOR
import pygame as pg
import random as rn



'''
Creates a background to be rendered on the base frame behind other GUI objects.
'''
class Background:
    def __init__(self, window, window_size, surface_number=24, transparency=200, rgb=(100, 100, 100), speed=1):
        self.window_size = window_size
        self.surface_transparency = transparency #How transparent the frames are
        self.surface_number = surface_number # The number of surfaces generated
        self.base_color = [rgb[0], rgb[1], rgb[2], self.surface_transparency] # The color and transparency of the surface
        self.circle_colors = [[rgb[0]+rn.randint(0, n), rgb[1], rgb[2], self.surface_transparency] for n in range(self.surface_number)]
        self.surface_list = self.generate_surfaces() # List of surfaces defines with input variables
        self.surface_color = (0, 0, 0, 0)
        # Animation variables
        self.surface_slopes = [rn.randint(0, window_size[0]) for _ in range(self.surface_number)]
        self.surface_positions = [[rn.randint(int(-window_size[0]/4), int(window_size[0]+(window_size[0]/4))), rn.randint(0, window_size[1])] for _ in range(self.surface_number)]
        self.surface_rotation = [rn.randint(0, 360) for _ in range(self.surface_number)]
        self.speed = speed
        #self.surface_direction = [rn.choice([True, False]) for _ in range(self.surface_number)]
        #print(self.surface_positions)


    def generate_surfaces(self):
        return_list = []
        for _ in range(self.surface_number):
            x_y = rn.randint(int(self.window_size[0]/8), int(self.window_size[0]/2))
            return_list.append(pg.Surface((x_y, x_y), pg.SRCALPHA)) # Creates the base list of surfaces
        return return_list

    def render_ground(self, window):


        for n, face in enumerate(self.surface_list):
            surface_center = (int(face.get_width()/2), int(face.get_height()/2))

            self.surface_rotation[n] += self.speed
            rotated = pg.transform.rotate(face, self.surface_rotation[n])
            rotated_rect = rotated.get_rect(center=(surface_center))
            face.fill(self.surface_color)
            pg.draw.circle(face,
            self.circle_colors[n],
            surface_center,
            face.get_width()/2)

            window.blit(rotated, (self.surface_positions[n][0]/2, self.surface_positions[n][1]/2))

