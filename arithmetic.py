import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft
from tkinter import Tk, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to calculate Arithmetic sequence
def arithmetic_sequence(n, a1=3, d=3):
    # Generate arithmetic sequence based on given a1 (first term) and d (common difference)
    sequence = [a1 + (i * d) for i in range(n)]
    return sequence

# Function to generate plots
def generate_plots(event=None):  # event parameter allows binding to key
    n = 333
    # Generate the Arithmetic sequence
    arith_numbers = arithmetic_sequence(n)
    
    # Shuffle the Arithmetic sequence numbers randomly (no duplicates)
    np.random.shuffle(arith_numbers)
    
    # Generate a random array containing Arithmetic sequence numbers, ensuring no duplicates
    random_arith_numbers = np.random.choice(arith_numbers, size=n, replace=False)

    # Create a DataFrame from the random Arithmetic sequence numbers
    df = pd.DataFrame({'x': random_arith_numbers})

    # Calculate the FFT of the dataframe using scipy.fft
    X = fft(df['x'].values)

    # Define the size of each marker based on the magnitude of each element in the FFT result
    sizes =80

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
    sizes =  50  # Normalize and scale sizes
    fig2, ax2 = plt.subplots()
    scatter2 = ax2.scatter(
        np.real(X), np.imag(X), c=phase, cmap='hsv', s=sizes, alpha=0.314
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
root.title("Arithmetic Sequence Plot Generator")

# Create a button to generate plots
plot_button = Button(root, text="Generate Plots", command=generate_plots)
plot_button.pack()

# Bind the Enter key to the generate_plots function
root.bind('<Return>', generate_plots)  # <Return> is the Enter key

# Run the application
root.mainloop()
