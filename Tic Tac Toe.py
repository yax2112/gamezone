import random
from tkinter import *
import pygame
from PIL import Image, ImageTk


class Game:
    def __init__(self, app):
        self.app = app  # The main application window
        self.app.title("Tic-Tac-Toe")  # Set the title of the window
        self.app.geometry('400x400')  # Set the dimensions of the window

        # Load and set the background image
        self.background_image = ImageTk.PhotoImage(Image.open(r"C:\Users\Hp\Desktop\game\image\t.png"))
        self.background_label = Label(self.app, image=self.background_image)  # Create label for background
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place background image on the screen

        # Initialize sound
        pygame.mixer.init()  # Initialize the pygame mixer module for sound
        pygame.mixer.music.load(r"C:\Users\Hp\Desktop\game\sound\bgmusic.mp3")  # Load background music
        pygame.mixer.music.play(-1)  # Loop the background music indefinitely

        # Button styling
        self.button_style = {
            'font': 'Arial 14 bold',  # Font for the button text
            'width': 15,  # Button width
            'height': 2,  # Button height
            'bg': 'black',  # Background color of button
            'fg': 'white',  # Text color of button
            'relief': 'raised',  # Style of button border
            'bd': 5,  # Border width
            'activebackground': '#2980b9',  # Button color when active
            'activeforeground': 'white'  # Text color when button is active
        }
        self.reset_game()  # Initialize the game state

    def reset_game(self):
        # Initialize the game board as a 3x3 grid of empty spaces
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.x_turn = True  # Set player X to start first
        self.mode = None  # No mode selected at the beginning
        # Restart background music when resetting the game
        pygame.mixer.music.load(r"C:\Users\Hp\Desktop\game\sound\bgmusic.mp3")  # Load background music again
        pygame.mixer.music.play(-1)  # Loop the background music

    def start(self):
        self.display_menu()  # Show the main menu

    def display_menu(self):
        self.reset_game()  # Reset the game state
        self.clear_frame()  # Clear the existing widgets in the frame

        # Label for the game title
        Label(self.app, text="Tic-Tac-Toe", font="Arial 20 bold", fg="black", bg="white").pack(pady=20)

        # Buttons for different game modes
        Button(self.app, text="Play with Computer", command=self.play_with_computer, **self.button_style).pack(pady=10)
        Button(self.app, text="Play with a Friend", command=self.play_with_friend, **self.button_style).pack(pady=10)
        Button(self.app, text="Exit", command=self.app.quit, **self.button_style).pack(pady=10)

    def play_with_computer(self):
        self.clear_frame()  # Clear the frame for a fresh start
        self.mode = "computer"  # Set the game mode to play with the computer
        self.display_board()  # Display the game board

    def play_with_friend(self):
        self.clear_frame()  # Clear the frame for a fresh start
        self.mode = "friend"  # Set the game mode to play with a friend
        self.display_board()  # Display the game board

    def clear_frame(self):
        # Destroy all existing widgets in the current frame
        for widget in self.app.winfo_children():
            widget.destroy()
        # Reapply the background image
        self.background_label = Label(self.app, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def display_board(self):
        # Clear the frame before displaying the game board
        self.clear_frame()
        # Create a grid of buttons for the Tic-Tac-Toe board
        for i in range(3):
            for j in range(3):
                Button(self.app, text=self.board[i][j], command=lambda i=i, j=j: self.make_move(i, j),
                       font="Arial 20 bold", width=5, height=2, bg="white").grid(row=i, column=j, padx=5, pady=5)

        # Add a button to return to the main menu
        Button(self.app, text="Back to Menu", command=self.display_menu, **self.button_style).grid(row=3, columnspan=3, pady=20)

    def make_move(self, i, j):
        # Check if the selected position is empty
        if self.board[i][j] == ' ':
            if self.x_turn:  # If it's player X's turn
                self.board[i][j] = 'X'  # Player X marks the spot
                if self.mode == "computer" and not self.check_winner():  # If playing against the computer
                    self.x_turn = False  # Switch to O's turn
                    self.ai_move()  # Let AI make its move
            else:  # If it's player O's turn
                self.board[i][j] = 'O'
            # Check for a winner after the move
            winner = self.check_winner()
            if winner or self.is_draw():
                self.display_winner(winner)  # Display the result of the game
            else:
                self.x_turn = not self.x_turn  # Switch turn
                self.display_board()  # Update the board

    def ai_move(self):
        # Find the best move for the AI (Minimax algorithm)
        best_move = self.get_best_move()
        if best_move:
            self.board[best_move[0]][best_move[1]] = 'O'  # AI places its mark
        winner = self.check_winner()  # Check if AI won after the move
        if winner or self.is_draw():
            self.display_winner(winner)  # Display the result of the game
        else:
            self.display_board()  # Update the board after AI's move

    def get_best_move(self):
        # Minimax algorithm to choose the best move for AI
        def evaluate(board):
            # Evaluate the board and return the score for a winner
            winner = self.check_winner()
            if winner == "O":
                return 1  # AI wins
            elif winner == "X":
                return -1  # Player X wins
            return 0  # No winner it draw

        def minimax(board, depth, is_maximizing):
            # Minimax function to calculate the best move recursively
            score = evaluate(board)
            if score == 1 or score == -1:
                return score  # Return the score if a terminal state is reached
            if self.is_draw():
                return 0  # Return 0 if it's a draw

            if is_maximizing:
                best_score = -float('inf')  # AI wants to maximize its score
                for i in range(3):
                    
                    for j in range(3):
                        if board[i][j] == ' ':
                            board[i][j] = 'O'  # Try placing O at the current position
                            score = minimax(board, depth + 1, False)  # Minimize for the next turn
                            board[i][j] = ' '  # Undo the move
                            best_score = max(best_score, score)  # Maximize AI's score
                return best_score
            else:
                best_score = float('inf')  # Player X wants to minimize the score
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == ' ':
                            board[i][j] = 'X'  # Try placing X at the current position
                            score = minimax(board, depth + 1, True)  # Maximize for the next turn
                            board[i][j] = ' '  # Undo the move
                            best_score = min(best_score, score)  # Minimize Player X's score
                return best_score

        best_move = None
        best_value = -float('inf')  # Initialize the best move
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'O'  # Try placing O at the current position
                    move_value = minimax(self.board, 0, False)  # Evaluate the move using minimax
                    self.board[i][j] = ' '  # Undo the move
                    if move_value > best_value:
                        best_value = move_value  # Update the best move
                        best_move = (i, j)
        return best_move  # Return the best move for AI

    def check_winner(self):
        # Check if there's a winner on the board
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]  # Return the winner (X or O)
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]  # Return the winner (X or O)
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]  # Return the winner (X or O)
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]  # Return the winner (X or O)
        return None  # No winner

    def is_draw(self):
        # Check if the game is a draw (no empty spaces left)
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))

    def display_winner(self, winner):
        # Clear the frame and display the winner or draw
        self.clear_frame()
        if winner:
            Label(self.app, text=f"{winner} Wins!", font="Arial 20 bold", bg="lightblue").pack(pady=20)
            pygame.mixer.music.load(r"C:\Users\Hp\Desktop\game\sound\win.mp3")  # Load the win sound
            pygame.mixer.music.play()  # Play the win sound
        else:
            Label(self.app, text="It's a Draw!", font="Arial 20 bold", bg="lightblue").pack(pady=20)
            pygame.mixer.music.load(r"C:\Users\Hp\Desktop\game\sound\loss.mp3")  # Load the loss sound
            pygame.mixer.music.play()  # Play the loss sound

        Button(self.app, text="Back to Menu", command=self.display_menu, **self.button_style).pack(pady=10)


# Run the game
app = Tk()
game = Game(app)  # Create a Game instance with the app window
game.start()  # Start the game by displaying the menu
app.mainloop()  # Run the Tkinter main loop


