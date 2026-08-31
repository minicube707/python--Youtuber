import numpy as np
import cellpylib as cpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class CustomRule(cpl.BaseRule):
    """Custom cellular automaton rule."""

    def __call__(self, n, c, t):
        # Return the center cell value increased by one
        return n[1] + 1


# Create an instance of the custom rule
rule = CustomRule()

# Initialize a one-dimensional cellular automaton with 100 cells
cellular_automaton = cpl.init_simple(100)

# Evolve the cellular automaton for 60 timesteps
cellular_automaton = cpl.evolve(
    cellular_automaton,
    timesteps=60,
    memoize=True,
    apply_rule=rule,
)

# Plot the complete evolution
cpl.plot(cellular_automaton)


# Create the figure and axes for the animation
fig, ax = plt.subplots()

# Display the cellular automaton as a matrix
mat = ax.matshow(
    cellular_automaton,
    cmap="binary",
)

# Hide the axes
plt.axis("off")


def animate(i):
    """Update the animation with the current timestep."""
    mat.set_data(cellular_automaton[: i + 1])
    return [mat]


# Create the animation
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=60,
    interval=50,
    blit=True,
    repeat=False,
)

# Display the animation
plt.show()