import numpy as np
import cellpylib as cpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Initialize a 60x60 cellular automaton
cellular_automaton = cpl.init_simple2d(60, 60)

# Add the first initial pattern
cellular_automaton[:, [28, 29, 30, 30], [30, 31, 29, 31]] = 1

# Add the second initial pattern
cellular_automaton[:, [40, 40, 40], [15, 16, 17]] = 1

# Add the third initial pattern
cellular_automaton[
    :,
    [18, 18, 19, 20, 21, 21, 21, 21, 20],
    [45, 48, 44, 44, 44, 45, 46, 47, 48],
] = 1

# Evolve the cellular automaton using Conway's Game of Life
cellular_automaton = cpl.evolve2d(
    cellular_automaton,
    timesteps=250,
    neighbourhood="Moore",
    memoize="recursive",
    apply_rule=cpl.game_of_life_rule,
)

# Plot the complete evolution
cpl.plot2d(cellular_automaton)


# Create the figure and axes for the animation
fig, ax = plt.subplots()

# Set the limits of the plot
ax.set_xlim((0, 60))
ax.set_ylim((0, 60))

# Display the first state of the cellular automaton
img = ax.imshow(
    cellular_automaton[0],
    interpolation="nearest",
    cmap="Greys",
)

# Hide the axes
plt.axis("off")


def init():
    """Initialize the animation with the first state."""
    img.set_data(cellular_automaton[0])
    return (img,)


def animate(i):
    """Update the animation with the state at timestep i."""
    img.set_data(cellular_automaton[i])
    return (img,)


# Create the animation
ani = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=250,
    interval=30,
    blit=True,
    repeat=False,
)

# Display the animation
plt.show()


#####

# Initialize a random 60x60 cellular automaton
cellular_automaton = cpl.init_random2d(60, 60)

# Evolve the cellular automaton using Conway's Game of Life
cellular_automaton = cpl.evolve2d(
    cellular_automaton,
    timesteps=250,
    neighbourhood="Moore",
    memoize="recursive",
    apply_rule=cpl.game_of_life_rule,
)

# Create a new figure and axes for the random initialization
fig, ax = plt.subplots()

# Set the limits of the plot
ax.set_xlim((0, 60))
ax.set_ylim((0, 60))

# Display the first state of the cellular automaton
img = ax.imshow(
    cellular_automaton[0],
    interpolation="nearest",
    cmap="Greys",
)

# Hide the axes
plt.axis("off")

# Create the animation using the same animation functions
ani = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=250,
    interval=30,
    blit=True,
    repeat=False,
)

# Display the animation
plt.show()