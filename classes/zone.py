# This Python class provides fundamental computational functionality 
# for crisis and safe zones in the simulation.

# Import required Python modules.
import pygame
import numpy as np

# Zone class to represent both Crisis and Safe zones
class Zone:
    def __init__(self, center, radius, zone_type='crisis'):
        self.center = np.array(center)
        self.radius = radius
        self.zone_type = zone_type  # 'crisis' or 'safe'

    def draw(self, screen, scale_factor, color):
        pygame.draw.circle(screen, color, (int(self.center[0] * scale_factor), int(self.center[1] * scale_factor)),
                           int(self.radius * scale_factor), 2)