
import tkinter as tk  # Import tkinter for GUI creation
from tkinter import messagebox  # Import messagebox for showing error dialogs
import subprocess  # Import subprocess to run external scripts
from PIL import Image, ImageTk  # Import PIL for handling images
import pygame  # Import pygame for handling audio playback

# Initialize pygame mixer to play background music
pygame.mixer.init()

# Function to run the specified game script
def run_game(game_script):
    try:
        # Stop the background music before starting the game
        pygame.mixer.music.stop()
        # Execute the game script as a subprocess
        process = subprocess.Popen(['python', game_script])
        # Wait for the game process to finish
        process.wait()
        # Resume the background music once the game is closed
        pygame.mixer.music.play(-1, 0.0)
    except Exception as e:
        # Show an error message if there's an issue running the game
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to create a styled button for each game
def create_button(parent, game_name, script_name):
    print(f"Creating button for: {game_name}")  # Debugging message for button creation
    return tk.Button(
        parent,  # The parent container (frame)
        text=game_name,  # Label of the button
        command=lambda: run_game(script_name),  # Action to perform on button click
        bg='black',  # Button background color
        fg='white',  # Button text color
        font=('time new roman', 16, 'bold'),  # Button font style
        padx=20,  # Padding inside the button (left-right)
        pady=2,  # Padding inside the button (top-bottom)
        relief='raised',  # Button border style
        borderwidth=5,  # Width of the button border
        width=9  # Width of the button
    )

# Main function to set up the game zone interface
def main():
    root = tk.Tk()  # Create the main window
    root.title("Game Zone")  # Set the window title
    root.geometry("570x422")  # Set the size of the window

    # Create a canvas to display the background image
    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack(fill="both", expand=True)  # Expand canvas to fit the window

    try:
        # Load and display the background image
        background_image = Image.open(r"C:\Users\Hp\Desktop\game\image\1.png")  # Load the image
        background_photo = ImageTk.PhotoImage(background_image)  # Convert image for use in tkinter
        canvas.create_image(0, 0, image=background_photo, anchor="nw")  # Place the image on the canvas
        root.background_photo = background_photo  # Keep a reference to avoid garbage collection
    except Exception as e:
        # Print an error message if the image fails to load
        print(f"Error loading image: {e}")

    # Create a frame to hold the game buttons
    button_frame = tk.Frame(root, bg='#f2f2f2')  # Frame with light gray background
    button_frame.place(x=370, y=255)  # Position the frame on the canvas

    try:
        # Create and position buttons for each game
        button1 = create_button(button_frame, "1.Tic Tac Toe", r"C:\Users\Hp\Desktop\game\Tic Tac Toe.py")
        button1.pack(pady=3)  # Add vertical spacing between buttons
        button2 = create_button(button_frame, "2.Snake Game", r"C:\Users\Hp\Desktop\game\Snake.py")
        button2.pack(pady=3)  # Add vertical spacing between buttons
        button3 = create_button(button_frame, "3.Pacman", r"C:\Users\Hp\Desktop\game\pacman using hill.py")
        button3.pack(pady=3)  # Add vertical spacing between buttons
    except Exception as e:
        # Print an error message if there's an issue creating buttons
        print(f"Error creating button: {e}")

    # Load and play background music in a loop
    try:
        pygame.mixer.music.load(r"C:\Users\Hp\Desktop\game\sound\BG.mp3")  # Load the music file
        pygame.mixer.music.play(-1, 0.0)  # Play music indefinitely from the beginning
    except Exception as e:
        # Print an error message if the music fails to load
        print(f"Error loading background music: {e}")

    root.mainloop()  # Start the Tkinter event loop to display the window

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
