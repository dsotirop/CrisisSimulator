import pygame
import numpy as np
import imageio
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from classes.individual import Individual
from classes.zone import Zone

class Simulation:
    def __init__(self, grid_size, population_size, repulsion_strength_crisis, attraction_strength_safe, 
                 noise_strength, crisis_zone_radius, safe_zone_radius):
        self.grid_size = grid_size
        self.population_size = population_size
        self.repulsion_strength_crisis = repulsion_strength_crisis
        self.attraction_strength_safe = attraction_strength_safe
        self.noise_strength = noise_strength
        self.crisis_zone_radius = crisis_zone_radius
        self.safe_zone_radius = safe_zone_radius
        self.individuals = []
        self.crisis_zones = []
        self.safe_zones = []
        self.screen = None
        self.scale_factor = None
        self.frames = []  # List to store frames
        self.map_image_path = "zoomed_area_map.png"  # Path to save the map image

    def load_and_display_map(self):
        """Loads a map using GeoPandas, zooms in on a specific region, and saves it as an image."""
        # Load the world shapefile using GeoPandas
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        # Define a bounding box (xmin, ymin, xmax, ymax) for zooming in on a region
        bbox = (-10, 10, 25, 25)  # Example bounding box: Europe (adjust as needed)
        zoomed_area = world.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]

        # Plot the zoomed-in map and country names
        fig, ax = plt.subplots(figsize=(10, 10))
        zoomed_area.boundary.plot(ax=ax, color='black')

        # Add country names to the map
        zoomed_area.apply(lambda x: ax.text(x.geometry.centroid.x, x.geometry.centroid.y,
                                            x['name'], fontsize=8, fontproperties=FontProperties(weight='bold')),
                          axis=1)

        ax.set_title('Zoomed-in Map')
        ax.set_axis_off()  # Hide axes for a cleaner display

        # Save the map as an image to use in Pygame
        plt.savefig(self.map_image_path, bbox_inches='tight', pad_inches=0)
        plt.close()

    def generate_zones(self):
        # Generate random crisis zones
        self.crisis_zones = [
            Zone(np.random.uniform([20, 20], [80, 80]), self.crisis_zone_radius, 'crisis'),
            Zone(np.random.uniform([40, 40], [60, 60]), self.crisis_zone_radius, 'crisis')
        ]
        # Generate random safe zones outside the crisis zones
        self.safe_zones = [
            Zone(np.random.uniform([10, 10], [90, 90]), self.safe_zone_radius, 'safe'),
            Zone(np.random.uniform([10, 70], [90, 90]), self.safe_zone_radius, 'safe')
        ]

    def initialize_individuals(self):
        # Initialize individuals inside the crisis zones
        for i in range(self.population_size):
            zone = np.random.choice(self.crisis_zones)
            angle = np.random.uniform(0, 2 * np.pi)
            distance_from_center = np.random.uniform(0, zone.radius)
            x = zone.center[0] + distance_from_center * np.cos(angle)
            y = zone.center[1] + distance_from_center * np.sin(angle)
            self.individuals.append(Individual([x, y]))

    def draw_zones(self):
        for zone in self.crisis_zones:
            zone.draw(self.screen, self.scale_factor, color=(255, 0, 0))  # Red for crisis zones
        for zone in self.safe_zones:
            zone.draw(self.screen, self.scale_factor, color=(0, 255, 0))  # Green for safe zones

    def update_individuals(self):
        all_in_safe_zone = True
        for individual in self.individuals:
            force = individual.apply_forces(self.crisis_zones, self.safe_zones,
                                            self.repulsion_strength_crisis, self.attraction_strength_safe)
            individual.update_position(force, self.noise_strength, self.grid_size)
            if not individual.is_in_safe_zone(self.safe_zones, self.safe_zone_radius):
                all_in_safe_zone = False  # If any individual is not in a safe zone, continue simulation
        return all_in_safe_zone

    def draw_individuals(self):
        for individual in self.individuals:
            individual.draw(self.screen, self.scale_factor)

    def draw_grid(self):
        grid_color = (0, 0, 0, 100)  # RGBA with alpha for transparency
        grid_surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Enable alpha blending
        cell_size = width // 10  # Create 10x10 grid cells
        for x in range(0, width, cell_size):
            pygame.draw.line(grid_surface, grid_color, (x, 0), (x, height))  # Draw vertical lines
        for y in range(0, height, cell_size):
            pygame.draw.line(grid_surface, grid_color, (0, y), (width, y))  # Draw horizontal lines
        self.screen.blit(grid_surface, (0, 0))  # Overlay the grid on the main screen

    def save_frame(self):
        """Captures the current screen and saves it as an image for creating a GIF later."""
        frame = pygame.surfarray.array3d(self.screen)
        frame = np.transpose(frame, (1, 0, 2))  # Pygame uses a different axis ordering
        self.frames.append(frame)

    def save_gif(self, filename="simulation.gif"):
        """Creates a GIF from the captured frames."""
        imageio.mimsave(filename, self.frames, fps=10)

    def run(self):
        pygame.init()
        global width, height
        width, height = 800, 800
        self.screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()
        self.scale_factor = width / self.grid_size

        # Load and display the zoomed-in map
        self.load_and_display_map()

        # Load the saved map as background
        background = pygame.image.load(self.map_image_path)
        background = pygame.transform.scale(background, (width, height))

        # Initialize zones and individuals
        self.generate_zones()
        self.initialize_individuals()

        # Main simulation loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the screen and draw everything
            self.screen.blit(background, (0, 0))  # Draw the map background
            self.draw_zones()
            all_in_safe_zone = self.update_individuals()
            self.draw_individuals()
            self.draw_grid()

            # Capture the current frame for GIF
            self.save_frame()

            # Check if all individuals are in the safe zone
            if all_in_safe_zone:
                print("All individuals are in safe zones. Simulation stopped.")
                running = False

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            clock.tick(30)  # 30 frames per second

        # Save the captured frames as a GIF
        self.save_gif(filename="simulation.gif")

        # Clean up and close the Pygame window
        pygame.quit()