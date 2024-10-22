from classes.simulation import Simulation

# Setup the internal simulation parameters.
grid_size = 100
population_size = 500
repulsion_strength_crisis = 0.1
attraction_strength_safe = 0.05
noise_strength = 0.02
crisis_zone_radius = 2
safe_zone_radius = 2

# Create a Simulation instance and run it
simulation = Simulation(grid_size, population_size, repulsion_strength_crisis, 
                        attraction_strength_safe,noise_strength, 
                        crisis_zone_radius, safe_zone_radius)
simulation.run()