import matplotlib.pyplot as plt
import matplotlib.patches as patches
import colorsys

def plot_cantor_set(data, num_rows):
    fig, ax = plt.subplots(figsize=(10, 6))

    row_height = 1  # Vertical space between rows

    for row in range(num_rows):
        # Filter segments for the current row
        row_segments = [segment for segment in data if segment[0] == row and segment[2] != 0]

        num_segments = len(row_segments)

        for element, (r, e, label) in enumerate(row_segments):
            start = e / (3 ** r)
            end = (e + 1) / (3 ** r)
            y_pos = -r * row_height  # Plot lower rows further down

            # Generate a unique color for each segment in the row
            hue = element / num_segments  # Normalize hue value between 0 and 1
            r_col, g_col, b_col = colorsys.hsv_to_rgb(hue, 0.7, 0.9)  # Convert HSV to RGB

            # Draw a line segment as a rectangle with the generated color
            rect = patches.Rectangle((start, y_pos - 0.05), end - start, 0.1, linewidth=1,
                                     edgecolor=(r_col, g_col, b_col), facecolor=(r_col, g_col, b_col))
            ax.add_patch(rect)

    ax.set_title("Cantor Set Visualizer (Line-Wise Chromatic Gradient)")
    ax.set_xlabel("Position")
    ax.set_ylabel("Row")
    ax.set_yticks([-i for i in range(num_rows)])
    ax.set_yticklabels([f"Row {i}" for i in range(num_rows)])
    ax.set_xlim(0, 1)  # Keep this fixed to show the full range from 0 to 1
    ax.set_ylim(-num_rows, 1)

    plt.show()


def generate_cantor_data(rows):
    data = [[0, 0, 1]]
    current_label = 2
    for row in range(1, rows):
        new_row = []
        for element in range(3 ** row):
            if element % 3 == 1:  # Removed segment
                new_row.append([row, element, 0])
            else:  # Remaining segment
                new_row.append([row, element, current_label])
                current_label += 1
        data.extend(new_row)
    return data


num_rows = 10  # Number of rows to generate (increase this for more detail)
data = generate_cantor_data(num_rows)
plot_cantor_set(data, num_rows)
