
from random import randrange  # Import for random number generation
from collections import deque  # Import deque for BFS queue
from turtle import *  # Import turtle graphics for game visuals
import time  # Import time for timer and elapsed time calculation
import pygame  # Import pygame for sound effects
from freegames import square, vector  # Import square and vector for game elements

# Initialize food and snake positions
food = vector(0, 0)  # Initial position of the food
snake = [vector(10, 0)]  # Initial position of the snake
aim = vector(0, -10)  # Initial movement direction of the snake

# Directions for BFS: up, down, right, left
DIRECTIONS = [(0, -10), (0, 10), (10, 0), (-10, 0)]  # Valid movement directions

# Initialize score and timer
score = 0  # Initialize score to zero
start_time = time.time()  # Start timer when the game starts

# Initialize high score
high_score = 0  # Variable to store the high score

# Pygame mixer initialization for sound
pygame.mixer.init()  # Initialize pygame mixer for audio
pygame.mixer.music.load(r"C:\Users\Hp\Desktop\game\sound\background.mp3")  # Load background music
pygame.mixer.music.play(-1, 0.0)  # Loop the background music indefinitely

# Load sound effects
eat_sound = pygame.mixer.Sound(r"C:\Users\Hp\Desktop\game\sound\eat.mp3")  # Load eat sound effect
game_over_sound = pygame.mixer.Sound(r"C:\Users\Hp\Desktop\game\sound\crash.mp3")  # Load game-over sound effect

def bfs(start, food, snake):
    """Breadth-First Search to find the shortest path to the food."""
    queue = deque([(start, [])])  # Queue stores current position and path
    visited = set([(start.x, start.y)])  # Keep track of visited positions

    while queue:
        current, path = queue.popleft()  # Get the current position and path

        if current == food:  # If food is reached, return the path
            return path

        for dx, dy in DIRECTIONS:  # Explore all valid directions
            next_pos = vector(current.x + dx, current.y + dy)  # Compute the next position

            if -200 < next_pos.x < 190 and -200 < next_pos.y < 190 and (next_pos.x, next_pos.y) not in visited:
                visited.add((next_pos.x, next_pos.y))  # Mark the position as visited
                queue.append((next_pos, path + [next_pos]))  # Add next position and path to the queue

    return []  # Return empty list if no path to food is found

def change(x, y):
    """Change snake direction to user-specified direction."""
    if (aim.x, aim.y) != (-x, -y):  # Prevent reversing direction
        aim.x = x  # Update horizontal direction
        aim.y = y  # Update vertical direction

def inside(head):
    """Return True if the snake's head is inside the play area."""
    return -200 < head.x < 190 and -200 < head.y < 190  # Check boundaries

def draw_border():
    """Draw the border around the play area."""
    penup()
    goto(-200, 200)  # Start position for the border
    pendown()
    color('black')  # Border color
    for _ in range(4):  # Draw 4 sides of the rectangle
        forward(400)
        right(90)

def draw_score():
    """Draw the current score, high score, and timer on the screen."""
    penup()
    goto(-180, 200)  # Position for the score
    color('green')  # Text color for the score
    write(f"Score: {score}", align="left", font=("Arial", 14, "bold"))
    
    goto(150, 200)  # Position for high score
    write(f"High Score: {high_score}", align="center", font=("Arial", 14, "bold"))

    elapsed_time = int(time.time() - start_time)  # Calculate elapsed time
    goto(-9, 200)  # Position for timer
    color('red')
    write(f"Time: {elapsed_time}s", align="center", font=("Arial", 14, "bold"))

def game_over():
    """Handle the game-over state."""
    global high_score
    pygame.mixer.music.stop()  # Stop background music
    game_over_sound.play()  # Play game-over sound
    clear()  # Clear the screen
    
    if score > high_score:  # Update high score if current score is higher
        high_score = score

    penup()
    goto(0, 0)  # Center position for game-over message
    color("red")
    write(f"Game Over\nScore: {score}\nHigh Score: {high_score}", align="center", font=("Arial", 20, "bold"))

    goto(0, -50)  # Position for "Play Again" message
    color("blue")
    write("Click to Play Again", align="center", font=("Arial", 14, "bold"))
    update()
    onscreenclick(restart_game)  # Restart game on screen click

def restart_game(x, y):
    """Reset the game to start again."""
    global score, snake, food, start_time, aim
    score = 0  # Reset score
    snake = [vector(10, 0)]  # Reset snake position
    food = vector(randrange(-15, 15) * 10, randrange(-15, 15) * 10)  # Place food randomly
    start_time = time.time()  # Reset timer
    aim = vector(0, -10)  # Reset direction
    pygame.mixer.music.play(-1, 0.0)  # Restart background music

    clear()
    draw_border()
    move()

def move():
    """Move the snake forward based on user input or BFS."""
    global score
    head = snake[-1].copy()  # Copy the head of the snake

    path = bfs(head, food, snake)  # Find path to food using BFS

    if aim.x != 0 or aim.y != 0:  # If aim is set, use manual movement
        head.move(aim)
    elif path:  # If path exists, follow the BFS path
        next_step = path[0]
        head = vector(next_step.x, next_step.y)
    else:  # Fallback to aim
        head.move(aim)

    if not inside(head) or head in snake:  # Check collision with boundary or self
        game_over()
        return

    snake.append(head)  # Add new head position

    if head == food:  # Check if food is eaten
        score += 1
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
        eat_sound.play()  # Play sound for eating
    else:
        snake.pop(0)  # Remove the tail

    clear()  # Clear the screen

    for body in snake:  # Draw the snake
        square(body.x, body.y, 9, 'black')

    square(food.x, food.y, 9, 'red')  # Draw the food
    draw_border()  # Draw border
    draw_score()  # Update score and timer

    update()
    ontimer(move, 200)  # Schedule the next move

# Setup Turtle
setup(630, 500, 370, 0)  # Set up the window size and position
hideturtle()  # Hide the turtle cursor
tracer(False)  # Disable animation for smooth rendering
listen()  # Enable keyboard input

bgpic(r"C:\Users\Hp\Desktop\game\image\i5.gif")  # Set background image
bgcolor("black")  # Set background color to black

draw_border()  # Draw the border

# Bind arrow keys for movement
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')

move()  # Start the game loop
done()  # Keep the window open

