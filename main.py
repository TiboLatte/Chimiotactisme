import pygame
from cell import Cell
import random
import math

pygame.init()

WIDTH = 1080
HEIGHT = 720
FPS = 30    

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CELL_NUMBER = 3
CELL_LIST = []
PHEROMONE_LIST = []

# Define the message box dimensions and position
MESSAGE_BOX_WIDTH = 300
MESSAGE_BOX_HEIGHT = 100
MESSAGE_BOX_PADDING = 10
MESSAGE_BOX_POSITION = (20, 10)
display_message = False
# Create the font object
font = pygame.font.SysFont("comicsansms", 23, bold=False, italic=False)


def drawMessage(message):
    # Split the message into individual lines
    lines = message.split("\n")
    # Calculate the height of each line
    line_height = font.get_linesize()

    # Calculate the total height of the text
    text_height = len(lines) * line_height

    # Create a surface for the background of the message box
    bg_surface = pygame.Surface((MESSAGE_BOX_WIDTH, MESSAGE_BOX_HEIGHT))
    bg_surface.fill((200, 200, 200))  # Light gray background
    bg_surface.set_alpha(128)  # Semi-transparent

    # Calculate the y-position to vertically center the text within the message box
    text_y = MESSAGE_BOX_POSITION[1] + (MESSAGE_BOX_HEIGHT - text_height -40) // 2

    # Blit the background surface onto the screen
    screen.blit(bg_surface, (MESSAGE_BOX_POSITION[0] - MESSAGE_BOX_PADDING, MESSAGE_BOX_POSITION[1] - MESSAGE_BOX_PADDING))

    # Draw the box border
    pygame.draw.rect(screen, BLACK, (MESSAGE_BOX_POSITION[0] - MESSAGE_BOX_PADDING, MESSAGE_BOX_POSITION[1] - MESSAGE_BOX_PADDING, MESSAGE_BOX_WIDTH, MESSAGE_BOX_HEIGHT), 2)

    # Render and blit each line of text onto the screen
    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (MESSAGE_BOX_POSITION[0], text_y))
        text_y += line_height


## initialize pygame and create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chimiotactisme")
clock = pygame.time.Clock()     ## For syncing the FPS
run = True
prev_clicked_cell = None


while run:
    # Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        cellUnit = Cell(type="inflammatory",screen=screen)
        CELL_LIST.append(cellUnit)
    if keys[pygame.K_m]:
        cellUnit = Cell(type="mastocyte",screen=screen)
        CELL_LIST.append(cellUnit)

    if keys[pygame.K_g]:
        cellUnit = Cell(type="granulocyte",screen=screen)
        print(cellUnit.attracted)
        CELL_LIST.append(cellUnit)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                mouse_pos = pygame.mouse.get_pos()
                clicked_cell = None
                min_distance = float('inf')

                for cell in CELL_LIST:
                    sqx = (mouse_pos[0] - cell.x) ** 2
                    sqy = (mouse_pos[1] - cell.y) ** 2
                    distance = math.sqrt(sqx + sqy)

                    if distance < min_distance:
                        min_distance = distance
                        clicked_cell = cell

                    if clicked_cell is not None and min_distance < 200:
                        if prev_clicked_cell is not None:
                            prev_clicked_cell.setColor(screen)  # Reset the color of the previously clicked cell
                        clicked_cell.setColor(screen)  # Set the color of the newly clicked cell
                        prev_clicked_cell = clicked_cell  # Update the previously clicked cell
                        display_message = True
                        message = clicked_cell.name + "\n Genome: 0002210"
                        clicked_cell.color = (255, 255, 10)

    screen.fill(WHITE)
    if display_message:
        drawMessage(message)

    # Game logic
    for cell in CELL_LIST:
        cell.move(PHEROMONE_LIST, CELL_LIST)
        cell.dropPheromone(PHEROMONE_LIST, screen)
        cell.draw(screen)
        cell.drawSensor(screen)

    for pheromone in PHEROMONE_LIST:
        pheromone.draw(screen)

    pygame.display.flip()

pygame.quit()
