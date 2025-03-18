import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft
from tkinter import Tk, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def look_and_say_sequence(start, n):
    result = [start]

    for _ in range(n - 1):
        current = result[-1]
        next_sequence = ''
        count = 1

        for i in range(1, len(current)):  
            if current[i] == current[i - 1]:
                count += 1
            else:
                next_sequence += str(count) + current[i - 1]
                count = 1

        next_sequence += str(count) + current[-1]  # Add the last repeated character
        result.append(next_sequence)

    return result

# Function to generate plots
def generate_plots(event=None):  # event parameter allows binding to key
    n = 20 # Limit the sequence length for visualization
    # Generate the Look-and-say sequence correctly
    sequence = look_and_say_sequence('1', n)
    
    # Convert the sequence into an array of integers for FFT computation
    look_and_say_sequence_numbers = [int(''.join(filter(str.isdigit, term))) for term in sequence]

    # Shuffle the Look-and-say numbers randomly (no duplicates)
    np.random.shuffle(look_and_say_sequence_numbers)
    
    # Generate a random array containing Look-and-say numbers, ensuring no duplicates
    random_look_and_say_numbers = np.random.choice(look_and_say_sequence_numbers, size=n, replace=False)

    # Create a DataFrame from the random Look-and-say numbers
    df = pd.DataFrame({'x': random_look_and_say_numbers})

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

    # Example usage
    sequence = look_and_say_sequence('1', 20)
    for i, seq in enumerate(sequence):
        print(f'Term {i + 1}: {seq}')

    
    # Show the second plot in the Tkinter window
    generate_plots.canvas2 = FigureCanvasTkAgg(fig2, master=root)
    generate_plots.canvas2.draw()
    generate_plots.canvas2.get_tk_widget().pack()

# Create the Tkinter window
root = Tk()
root.title("Look-and-say Sequence Plot Generator")

# Create a button to generate plots
plot_button = Button(root, text="Generate Plots", command=generate_plots)
plot_button.pack()

# Bind the Enter key to the generate_plots function
root.bind('<Return>', generate_plots)  # <Return> is the Enter key

# Run the application
root.mainloop()
