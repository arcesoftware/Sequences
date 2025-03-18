import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft
from tkinter import Tk, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to calculate Factorial
def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# Function to generate Factorial sequence
def factorial_sequence(n):
    return [factorial(i) for i in range(1, n + 1)]

# Function to generate plots
def generate_plots(event=None):  # event parameter allows binding to key
    n = 12 # Adjust for smaller n because factorial grows very fast
    # Generate the Factorial numbers sequence
    factorial_numbers_sequence = factorial_sequence(n)
    
    # Shuffle the Factorial numbers randomly (no duplicates)
    np.random.shuffle(factorial_numbers_sequence)
    
    # Generate a random array containing Factorial numbers, ensuring no duplicates
    random_factorial_numbers = np.random.choice(factorial_numbers_sequence, size=n, replace=False)

    # Create a DataFrame from the random Factorial numbers
    df = pd.DataFrame({'x': random_factorial_numbers})

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
        df.index, df['x'], c=df['x'], cmap='hsv', s=sizes, alpha=1.0
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
        np.real(X), np.imag(X), c=phase, cmap='hsv', s=sizes, alpha=1.0
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
root.title("Factorial Sequence Plot Generator")

# Create a button to generate plots
plot_button = Button(root, text="Generate Plots", command=generate_plots)
plot_button.pack()

# Bind the Enter key to the generate_plots function
root.bind('<Return>', generate_plots)  # <Return> is the Enter key

# Run the application
root.mainloop()
