import numpy as np
import matplotlib.pyplot as plt

# Parâmetros da simulação
width = 200
height = 50
viscosity = 0.02
timesteps = 5000

# Definição dos vetores de velocidade
c = np.array([[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [-1, -1], [1, -1]])

def initialize_lattice(width, height):
    q = 9
    lattice = np.zeros((height, width, q))
    for y in range(height):
        for x in range(width):
            for i in range(q):
                lattice[y, x, i] = 1.0 / q
    return lattice

def equilibrium_density(density, velocity, i, weight, cs2):
    dot_product = velocity[..., 0] * c[i, 0] + velocity[..., 1] * c[i, 1]
    return density * weight[i] * (1 + 3 * dot_product / cs2 + 4.5 * (dot_product ** 2) / (cs2 ** 2) - 1.5 * (velocity[..., 0] ** 2 + velocity[..., 1] ** 2) / cs2)

def simulate_lattice_boltzmann(lattice, timesteps, viscosity):
    q = 9
    weight = np.array([4 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 36, 1 / 36, 1 / 36, 1 / 36])
    cs2 = 1 / 3
    tau = 3 * viscosity + 0.5
    omega = 1 / tau

    for t in range(timesteps):
        # Calculate density and velocity
        density = np.sum(lattice, axis=2)
        velocity = np.tensordot(lattice, c, axes=1) / density[..., None]

        # Apply Zou/He boundary condition
        velocity[0, :, 0] = 0.1
        velocity[0, :, 1] = 0

        # Calculate equilibrium and collision
        for i in range(q):
            equilibrium = equilibrium_density(density, velocity, i, weight, cs2)
            lattice[..., i] += omega * (equilibrium - lattice[..., i])

        # Streaming
        for i in range(q):
            lattice[..., i] = np.roll(lattice[..., i], c[i], axis=(0, 1))

    return velocity


lattice = initialize_lattice(width, height)
velocity = simulate_lattice_boltzmann(lattice, timesteps, viscosity)

# Transpose the velocity array
transposed_velocity = np.transpose(velocity, axes=(1, 0, 2))

# Calculate the magnitude of the velocity
magnitude = np.sqrt(transposed_velocity[..., 0] ** 2 + transposed_velocity[..., 1] ** 2)

# Create a meshgrid for the quiver plot
X, Y = np.meshgrid(np.arange(0, width, 1), np.arange(0, height, 1))

# Use quiver plot to visualize the velocity field
fig, ax = plt.subplots(figsize=(10, 5))
quiv = ax.quiver(X, Y, transposed_velocity[..., 0], transposed_velocity[..., 1], magnitude, cmap='plasma', angles='xy', scale_units='xy', scale=1)
cbar = fig.colorbar(quiv, ax=ax)
cbar.set_label('Velocity Magnitude')

# Set the aspect ratio
ax.set_aspect('equal')

# Show the plot
plt.show()