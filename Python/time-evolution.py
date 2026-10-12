import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

# Function to calculate the function values for given z and t
def calculate_function_values(z, t):
    return np.exp(-0.1 * z) * np.cos(2 * np.pi * t - z)

# Set up the figure and axis
fig, ax = plt.subplots()
z_values = np.linspace(1, 20, 100)
line, = ax.plot(z_values, calculate_function_values(z_values, 1), label=r'$e^{-z} \cdot \cos(2 \pi \cdot 1 - z)$')
ax.set_xlabel('z')
ax.set_ylabel('Function Value')
ax.set_title('Animated Plot of the function')
ax.legend()
ax.grid(True)

# Animation update function
def update(t):
    line.set_ydata(calculate_function_values(z_values, t))
    return line,

# Create the animation
t_values = np.linspace(1, 1, 1)
animation = FuncAnimation(fig, update, frames=t_values, interval=200, blit=True)

# Save the animation as a GIF
#animation.save('decaying_wave.gif', writer='pillow', fps=15)

plt.show()