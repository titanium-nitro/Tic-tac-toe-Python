import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width, screen_height = 400, 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tic-Tac-Toe")
programIcon = pygame.image.load('icon.png')

pygame.display.set_icon(programIcon)

# Colors
blue = (0, 0, 225)
white = (255, 255, 255)
black = (0, 0, 0)
red = (225, 0, 0)

# Create a font for the text
font = pygame.font.Font(None, 24)

# Create a button rectangle
button_rect = pygame.Rect(150, 120, 100, 40)
button_text = font.render("Start", True, white)

# Game variables
button_visible = True
game_active = False
board = [" " for _ in range(9)]  # Represents the Tic-Tac-Toe board
current_player = "X"  # Player is "X" and computer is "O"
game_result = ""  # Stores the result of the game

# Function to draw the Tic-Tac-Toe board
def draw_board():
    for i in range(1, 3):
        # Vertical lines
        pygame.draw.line(screen, white, (i * screen_width // 3, 0), (i * screen_width // 3, screen_height), 2)
        # Horizontal lines
        pygame.draw.line(screen, white, (0, i * screen_height // 3), (screen_width, i * screen_height // 3), 2)

    for index, cell in enumerate(board):
        if cell != " ":
            x = (index % 3) * screen_width // 3 + screen_width // 6
            y = (index // 3) * screen_height // 3 + screen_height // 6
            if cell == "X":
                pygame.draw.line(screen, red, (x - 50, y - 50), (x + 50, y + 50), 2)
                pygame.draw.line(screen, red, (x + 50, y - 50), (x - 50, y + 50), 2)
            else:
                pygame.draw.circle(screen, blue, (x, y), 50, 2)

# Function to check if a player has won
def check_win(player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
                      (0, 4, 8), (2, 4, 6)]  # diagonals
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Function to check if the game is over (win or tie)
def check_game_over():
    if check_win("X"):
        return "X wins"
    elif check_win("O"):
        return "O wins"
    elif " " not in board:
        return "Tie"
    return False

# Function for the computer to make a move
def computer_move():
    # Check if player can win
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            if check_win("X"):
                board[i] = "O"
                return True
            board[i] = " "  # undo the move

    # Random move
    empty_cells = [i for i, cell in enumerate(board) if cell == " "]
    if empty_cells:
        index = random.choice(empty_cells)
        board[index] = "O"
        return True
    return False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_visible and button_rect.collidepoint(event.pos):
                button_visible = False
                game_active = True
                board = [" " for _ in range(9)]  # Reset the board
                game_result = ""  # Reset the game result
            elif game_active:
                # Player move
                x, y = event.pos
                row = y // (screen_height // 3)
                col = x // (screen_width // 3)
                index = row * 3 + col
                if board[index] == " ":
                    board[index] = "X"
                    game_result = check_game_over()
                    if game_result:
                        game_active = False
                        button_visible = True
                    elif not computer_move():
                        game_result = check_game_over()
                        if game_result:
                            game_active = False  # No more moves, end game
                        button_visible = True

    # Clear the screen
    screen.fill(black)
    
    # Draw the button if it's visible
    if button_visible:
        pygame.draw.rect(screen, blue, button_rect)
        screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))
    elif game_active:
        draw_board()

    # Display the game result
    if game_result:
        result_text = font.render(game_result, True, white)
        screen.blit(result_text, (screen_width // 2 - result_text.get_width() // 2, 10))
                    

    pygame.display.flip()
