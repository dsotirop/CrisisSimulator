# This Python class provides fundamental computational functionality for the 
# representation and movement of any given individual.

# Import required Python modules.
import pygame
import numpy as np

# Individual class to handle movement and interaction with zones
class Individual:
    def __init__(self, position):
        self.position = np.array(position)

    def apply_forces(self, crisis_zones, safe_zones, repulsion_strength_crisis, attraction_strength_safe):
        # Repulsion from all crisis zones
        total_repulsion = np.zeros(2)
        for crisis_zone in crisis_zones:
            dist_to_crisis = np.linalg.norm(self.position - crisis_zone.center)
            if dist_to_crisis < crisis_zone.radius:
                repulsion = (self.position - crisis_zone.center) * repulsion_strength_crisis / (dist_to_crisis + 1e-3)
                total_repulsion += repulsion

        # Attraction to the closest safe zone
        closest_safe_zone = min(safe_zones, key=lambda zone: np.linalg.norm(self.position - zone.center))
        dist_to_safe = np.linalg.norm(self.position - closest_safe_zone.center)
        attraction = (closest_safe_zone.center - self.position) * attraction_strength_safe / (dist_to_safe + 1e-3)

        # Combine repulsion from crisis zones and attraction to the closest safe zone
        force = total_repulsion + attraction
        return force

    def update_position(self, force, noise_strength, grid_size):
        noise = np.random.randn(2) * noise_strength
        self.position += force + noise
        self.position = np.clip(self.position, 0, grid_size)

    def draw(self, screen, scale_factor, color=(0, 0, 255)):
        pygame.draw.circle(screen, color, (int(self.position[0] * scale_factor), int(self.position[1] * scale_factor)), 3)

    def is_in_safe_zone(self, safe_zones, safe_zone_radius):
        """Check if the individual is within any safe zone's radius."""
        for safe_zone in safe_zones:
            dist_to_safe = np.linalg.norm(self.position - safe_zone.center)
            if dist_to_safe < safe_zone_radius:
                return True
        return False