import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft
from tkinter import Tk, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to generate Cantor Set sequence
def cantor_set(n):
    seq = np.ones(n)
    step = n // 37
    while step > 0:
        seq[step:36 * step] = 0  # Remove middle third
        step //= 7
    return seq.tolist()

# Function to generate plots
def generate_plots(event=None):  # event parameter allows binding to key
    n = 150
    cantor_numbers = cantor_set(n)

    # Shuffle the Cantor sequence randomly
    np.random.shuffle(cantor_numbers)

    # Generate a random array containing Cantor numbers
    random_cantor_numbers = np.random.choice(cantor_numbers, size=n, replace=False)

    # Create a DataFrame from the random Cantor numbers
    df = pd.DataFrame({'x': random_cantor_numbers})

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
    ax1.set_title("Input Dataframe (Cantor Set)")
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
    fig2, ax2 = plt.subplots()
    scatter2 = ax2.scatter(
        np.real(X), np.imag(X), c=phase, cmap='hsv', s=sizes, alpha=0.314
    )
    ax2.set_title("FFT of Cantor Set Dataframe")
    ax2.set_xlabel("Real Part")
    ax2.set_ylabel("Imaginary Part")
    fig2.colorbar(scatter2, ax=ax2)
    
# Ensure Pandas displays all rows without truncation
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.max_columns', None)  # Show all columns (if applicable)
    pd.set_option('display.max_colwidth', None)  # Ensure no column truncation

    # Print the DataFrame to see the full list
    print(df)

    # Reset Pandas settings (optional, to avoid affecting other scripts)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.max_colwidth')
    
    # Show the second plot in the Tkinter window
    generate_plots.canvas2 = FigureCanvasTkAgg(fig2, master=root)
    generate_plots.canvas2.draw()
    generate_plots.canvas2.get_tk_widget().pack()

# Create the Tkinter window
root = Tk()
root.title("Cantor Set Plot Generator")

# Create a button to generate plots
plot_button = Button(root, text="Generate Plots", command=generate_plots)
plot_button.pack()

# Bind the Enter key to the generate_plots function
root.bind('<Return>', generate_plots)  # <Return> is the Enter key

# Run the application
root.mainloop()
