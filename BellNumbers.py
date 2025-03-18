import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft
from tkinter import Tk, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to calculate Bell Numbers up to n
def bell_number(n):
    bell = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    bell[0][0] = 1  # Base case

    for i in range(1, n + 1):
        bell[i][0] = bell[i - 1][i - 1]
        
        # Fill the bell triangle
        for j in range(1, i + 1):
            bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1]
    
    return [bell[i][0] for i in range(n + 1)]  # Return the Bell numbers for 0 to n

# Function to generate plots
def generate_plots(event=None):  # event parameter allows binding to key
    n = 150  # Limit the sequence length for visualization
    # Generate Bell Numbers
    bell_numbers = bell_number(n)
    
    # Shuffle the Bell numbers randomly (no duplicates)
    np.random.shuffle(bell_numbers)
    
    # Generate a random array containing Bell numbers, ensuring no duplicates
    random_bell_numbers = np.random.choice(bell_numbers, size=n, replace=False)

    # Create a DataFrame from the random Bell numbers
    df = pd.DataFrame({'x': random_bell_numbers})

    # Calculate the FFT of the dataframe using scipy.fft
    X = fft(df['x'].values)

    # Define the size of each marker based on the magnitude of each element in the FFT result
    sizes = 50

    # Clear previous plots (if any)
    if hasattr(generate_plots, "canvas1"):
        generate_plots.canvas1.get_tk_widget().pack_forget()
    if hasattr(generate_plots, "canvas2"):
        generate_plots.canvas2.get_tk_widget().pack_forget()

    # Redraw Input Dataframe Plot
    fig1, ax1 = plt.subplots()
    scatter1 = ax1.scatter(
        df.index, df['x'], c=df['x'], cmap='hsv', s=sizes, alpha=0.5
    )
    ax1.set_title("Input Dataframe")
    ax1.set_xlabel("Index")
    ax1.set_ylabel("Value")
    fig1.colorbar(scatter1, ax=ax1)

    # Show the first plot in the Tkinter window
    generate_plots.canvas1 = FigureCanvasTkAgg(fig1, master=root)
    generate_plots.canvas1.draw()
    generate_plots.canvas1.get_tk_widget().pack()

    # Redraw FFT Dataframe Plot
    magnitude = np.abs(X)
    phase = np.angle(X)
    sizes = 50  # Normalize and scale sizes
    fig2, ax2 = plt.subplots()
    scatter2 = ax2.scatter(
        np.real(X), np.imag(X), c=phase, cmap='hsv', s=sizes, alpha=0.7
    )
    ax2.set_title("FFT of Dataframe")
    ax2.set_xlabel("Real Part")
    ax2.set_ylabel("Imaginary Part")
    fig2.colorbar(scatter2, ax=ax2)
    
    # Change pandas settings to display all rows
    pd.set_option('display.max_rows', None)  # Display all rows, no truncation
    pd.set_option('display.max_columns', None)  # Display all columns (if any)
    # Print the DataFrame to show its contents
    print(df)
    
    # Show the second plot in the Tkinter window
    generate_plots.canvas2 = FigureCanvasTkAgg(fig2, master=root)
    generate_plots.canvas2.draw()
    generate_plots.canvas2.get_tk_widget().pack()

# Create the Tkinter window
root = Tk()
root.title("Bell Numbers Plot Generator")

# Create a button to generate plots
plot_button = Button(root, text="Generate Plots", command=generate_plots)
plot_button.pack()

# Bind the Enter key to the generate_plots function
root.bind('<Return>', generate_plots)  # <Return> is the Enter key

# Run the application
root.mainloop()
