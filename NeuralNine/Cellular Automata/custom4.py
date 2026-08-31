import numpy as np
import cellpylib as cpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class CustomRule(cpl.BaseRule):
    """Custom implementation of Conway's Game of Life rule."""

    def __call__(self, n, c, t):
        # Check whether the center cell is currently dead.
        if n[1][1] == 0:
            # A dead cell becomes alive if exactly three cells are alive.
            if np.sum(n) == 3:
                return 1
            else:
                return 0

        # The center cell is currently alive.
        else:
            # Exclude the center cell from the neighbor count.
            # A live cell survives with two or three live neighbors.
            if np.sum(n) - 1 == 2 or np.sum(n) - 1 == 3:
                return 1
            else:
                return 0


# Create an instance of the custom rule.
rule = CustomRule()

# Initialize a 60x60 two-dimensional cellular automaton.
cellular_automaton = cpl.init_simple2d(60, 60)


# Glider
cellular_automaton[
    :,
    [28, 29, 30, 30],
    [30, 31, 29, 31],
] = 1

# Blinker
cellular_automaton[
    :,
    [40, 40, 40],
    [15, 16, 17],
] = 1

# Light Weight Space Ship
cellular_automaton[
    :,
    [18, 18, 19, 20, 21, 21, 21, 21, 20],
    [45, 48, 44, 44, 44, 45, 46, 47, 48],
] = 1


# Evolve the cellular automaton for 250 timesteps.
cellular_automaton = cpl.evolve2d(
    cellular_automaton,
    timesteps=250,
    neighbourhood="Moore",
    memoize="recursive",
    apply_rule=rule,
)


# Create the figure and axes for the animation.
fig, ax = plt.subplots()

# Set the plot limits.
ax.set_xlim((0, 60))
ax.set_ylim((0, 60))

# Display the initial state of the cellular automaton.
img = ax.imshow(
    cellular_automaton[0],
    interpolation="nearest",
    cmap="Greys",
)

# Hide the axes.
plt.axis("off")


def init():
    """Initialize the animation with the first state."""
    img.set_data(cellular_automaton[0])
    return (img,)


def animate(i):
    """Update the animation with the state at timestep i."""
    img.set_data(cellular_automaton[i])
    return (img,)


# Create the animation.
ani = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=250,
    interval=30,
    blit=True,
    repeat=False,
)

# Display the animation.
plt.show()