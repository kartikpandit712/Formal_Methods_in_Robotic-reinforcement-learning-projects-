import pygame
import random
from Wumpus_POMDP import WumpusWorldPOMDP
import sys
#print(pygame.ver)
# Constants
GRID_SIZE = 4
TILE_SIZE = 64  # size for each tile (64x64 pixels)
FPS = 30  # frames per second

# RGB Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Define the locations of pits, wumpus, and gold
pit_locs = [(1, 1), (2, 2), (3, 3)]  # Just an example, replace with actual pit locations
wumpus_loc = (0, 1)  # Replace with actual Wumpus location
gold_loc = (3, 0)  # Replace with actual gold location
start_position = (0, 0)

# Font setup for instructions
pygame.font.init()  # Initialize font module
font = pygame.font.SysFont('Arial', 18)

# Initialize Pygame
pygame.init()
#pygame.mixer.init()
screen = pygame.display.set_mode((GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE))

# Load images
robot_img = pygame.image.load('robot.png')
wumpus_img = pygame.image.load('wumpus.png')
pit_img = pygame.image.load('pit.png')
gold_img = pygame.image.load('gold.png')

def show_instructions():
    instructions = [
        "Use arrow keys to move.",
        "Press 'G' to grab the gold.",
        "Avoid the Wumpus and pits!",
        "Press 'R' to restart or 'Q' to quit."
    ]
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, WHITE)
        screen.blit(text, (5, GRID_SIZE * TILE_SIZE + 5 + (i * 20)))


def log_to_file(message):
    try:
        with open('game_output.txt', 'a') as file:
            file.write(message + '\n')
            file.flush()
    except Exception as e:
        print(f"Error writing to file: {e}")


def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()

def display_message(message):
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(GRID_SIZE * TILE_SIZE // 2, GRID_SIZE * TILE_SIZE // 2))
    
    screen.fill(BLACK)
    screen.blit(text, text_rect)
    pygame.display.flip()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting_for_key = False


def game_over(message):
    log_to_file(message)  # Log the game over message
    print(message)
    play_sound('game_over.wav')  # Replace with your actual game-over sound file
    pygame.time.wait(2000)  # Wait for 2 seconds to show the final state
    #pygame.quit()
    #sys.exit()
    display_message(message)
    restart_game()

def win_game():
    win_message = "You've got the gold!"
    log_to_file(win_message)  # Log the win message
    print("You've got the gold!")
    play_sound('win_sound.wav')  # Replace with your actual win sound file
    pygame.time.wait(2000)  # Wait for 2 seconds to show the final state
    #pygame.quit()
    #sys.exit()
    display_message(win_message)
    restart_game()

def restart_game():
    global wumpus_world
    wumpus_world.reset_world()
    #wumpus_world = WumpusWorldPOMDP(GRID_SIZE, pit_locs, wumpus_loc, gold_loc, start_position)


# You may need to scale images if they are not the same size as TILE_SIZE
robot_img = pygame.transform.scale(robot_img, (TILE_SIZE, TILE_SIZE))
wumpus_img = pygame.transform.scale(wumpus_img, (TILE_SIZE, TILE_SIZE))
pit_img = pygame.transform.scale(pit_img, (TILE_SIZE, TILE_SIZE))
gold_img = pygame.transform.scale(gold_img, (TILE_SIZE, TILE_SIZE))

# Game variables
clock = pygame.time.Clock()
running = True

# WumpusWorldPOMDP object from the previous implementation
# Make sure to modify the methods to work with the game loop
wumpus_world = WumpusWorldPOMDP(GRID_SIZE, pit_locs, wumpus_loc, gold_loc, start_position)

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_sprites():
    
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            position = (x * TILE_SIZE, y * TILE_SIZE)
            if (x, y) in wumpus_world.pit_locs:
                screen.blit(pit_img, position)
            elif (x, y) == wumpus_world.wumpus_loc:
                screen.blit(wumpus_img, position)
            elif (x, y) == wumpus_world.gold_loc:
                screen.blit(gold_img, position)
            # Add the robot sprite based on the agent's belief state
            # For simplicity, you could display it in its current state
            if (x, y) == wumpus_world.current_state:
                screen.blit(robot_img, position)

    pass



def main():
    #global running
    restart_game()  # Initialize the game state
    #while running:
    
    game_loop()

def game_loop():
    global running
   
    while running:
        action = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # pygame.quit()
                # sys.exit()
        # Game logic
                # Handle key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    action = 'move_north'
                elif event.key == pygame.K_DOWN:
                    action = 'move_south'
                elif event.key == pygame.K_LEFT:
                    action = 'move_west'
                elif event.key == pygame.K_RIGHT:
                    action = 'move_east'
                elif event.key == pygame.K_g:
                    action = 'grab'
                elif event.key == pygame.K_r:
                    # Reset the game
                    # Restart the game without recursion
                    restart_game()
                    #return #game_loop()  # Recursively call game_loop to restart the game
                elif event.key == pygame.K_q:
                    # Quit the game
                    running = False
                    # pygame.quit()
                    # sys.exit()
                # Perform the action
                if action:
                    next_state, observation = wumpus_world.simulate_action(action)
                    wumpus_world.update_belief_state(action, observation)
                    

                    # Check for game over conditions
                    if next_state in wumpus_world.pit_locs or next_state == wumpus_world.wumpus_loc:
                        game_over("Game Over: Fell into a pit or encountered the Wumpus!")
                        # print("Game Over: Fell into a pit or encountered the Wumpus!")
                        # running = False
                        # break
                        # restart_game()
                        # return 
                    # Check for win condition
                    elif wumpus_world.has_gold:
                        win_game()
                        # print("You've got the gold!")
                        # running = False
                        # break
                        # restart_game()
                        # return 
                     # Log the action taken and the result
                    action_message = f"Action taken: {action}, Resulting State: {next_state}, Observation: {observation}"
                    log_to_file(action_message)
        # You'll need to integrate the game logic from the previous step here,
        # which includes updating the belief state and choosing an action
        # action = wumpus_world.choose_action()
        # next_state, observation = wumpus_world.simulate_action(wumpus_world.current_state, action)
        # wumpus_world.current_state = next_state
        # wumpus_world.update_belief_state(action, observation)

        # Draw everything
        screen.fill(BLACK)
        draw_grid()
        draw_sprites()
        show_instructions() #display the instructions 

        # Update the display
        pygame.display.flip()

        # Tick
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

#game_loop()
main()
if __name__ == "__main__":
    main()