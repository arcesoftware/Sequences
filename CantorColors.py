import matplotlib.pyplot as plt
import matplotlib.patches as patches
import colorsys
from numba import njit, prange
import numpy as np


@njit(parallel=True)
def generate_cantor_data(rows):
    max_elements = 0
    for r in range(rows):
        max_elements += 3 ** r  # Calculate the total number of segments iteratively

    data = np.zeros((max_elements, 3), dtype=np.int32)

    index = 0
    current_label = 1

    for row in range(rows):
        for element in range(3 ** row):  # Not using prange here to preserve the order
            if element % 3 == 1:  # Removed segment
                data[index] = [row, element, 0]
            else:  # Remaining segment
                data[index] = [row, element, current_label]
                current_label += 1
            index += 1

    return data[:index]  # Return the filled portion of the array


def plot_cantor_set(data, num_rows):
    fig, ax = plt.subplots(figsize=(10, 6))

    row_height = 1  # Vertical space between rows

    for row in range(num_rows):
        # Filter segments for the current row
        row_segments = data[(data[:, 0] == row) & (data[:, 2] != 0)]

        num_segments = len(row_segments)

        for element, (r, e, label) in enumerate(row_segments):
            start = e / (3 ** r)
            end = (e + 1) / (3 ** r)
            y_pos = -r * row_height  # Plot lower rows further down

            # Generate a unique color for each segment
            np.random.seed(label)  # Seed the RNG to ensure unique colors per label
            r_col, g_col, b_col = np.random.rand(3)  # Generate random RGB values

            # Draw a line segment as a rectangle with the generated color
            rect = patches.Rectangle((start, y_pos - 0.05), end - start, 0.1, linewidth=1,
                                     edgecolor=(r_col, g_col, b_col), facecolor=(r_col, g_col, b_col))
            ax.add_patch(rect)

    ax.set_title("Cantor Set Visualizer (Random Color Gradient)")
    ax.set_xlabel("Position")
    ax.set_ylabel("Row")
    ax.set_yticks([-i for i in range(num_rows)])
    ax.set_yticklabels([f"Row {i}" for i in range(num_rows)])
    ax.set_xlim(0, 1)  # Keep this fixed to show the full range from 0 to 1
    ax.set_ylim(-num_rows, 1)

    plt.show()


num_rows = 15  # Number of rows to generate (increase this for more detail)
data = generate_cantor_data(num_rows)
plot_cantor_set(data, num_rows)
