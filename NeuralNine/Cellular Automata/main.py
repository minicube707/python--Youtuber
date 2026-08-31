import numpy as np
import cellpylib as cpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Initialize the cellular automaton with a single active cell
cellular_automaton = np.array([[0, 0, 1, 0, 0]])

# Evolve the cellular automaton using Wolfram's Rule 110
cellular_automaton = cpl.evolve(
    cellular_automaton,
    timesteps=5,
    memoize=True,
    apply_rule=lambda n, c, t: cpl.nks_rule(n, rule=110),
)

# Plot the evolution of the cellular automaton
cpl.plot(cellular_automaton)


# Initialize a new cellular automaton
cellular_automaton = np.array([[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]])

# Create a simple cellular automaton with 30 cells
cellular_automaton = cpl.init_simple(30)

# Evolve the cellular automaton using Wolfram's Rule 30
cellular_automaton = cpl.evolve(
    cellular_automaton,
    timesteps=20,
    memoize=True,
    apply_rule=lambda n, c, t: cpl.nks_rule(n, rule=30),
)

# Plot the evolution of the cellular automaton
cpl.plot(cellular_automaton)


# Create a figure and axes for the animation
fig, ax = plt.subplots()

# Display the cellular automaton as a matrix
mat = ax.matshow(
    cellular_automaton,
    cmap="binary",
)

# Hide the axes
ax.axis("off")


def animate(i):
    """Update the displayed rows for each animation frame."""
    mat.set_data(cellular_automaton[: i + 1])
    return [mat]


# Create the animation
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=30,
    interval=50,
    blit=True,
    repeat=False,
)

# Display the animation
plt.show()