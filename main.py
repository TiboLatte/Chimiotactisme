import pygame
from cell import Cell
import random
import math
from genome import Genome
pygame.init()

WIDTH = 1080
HEIGHT = 900
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

def handleGenomeInitialization(cells):
    print("Genome initialization")


## initialize pygame and create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chimiotactisme")
clock = pygame.time.Clock()     ## For syncing the FPS
run = True
prevSelectedCell = 0
selectedCellIndex = 0


while run:
    # Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    keys = pygame.key.get_pressed()          


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_i:
                cellUnit = Cell(type="inflammatory", screen=screen)
                CELL_LIST.append(cellUnit)
                cellUnitGenome = Genome(cellUnit)
                cellUnit.linkGenome(cellUnitGenome)
            if event.key == pygame.K_m:
                cellUnit = Cell(type="mastocyte", screen=screen)
                CELL_LIST.append(cellUnit)
                cellUnitGenome = Genome(cellUnit)
                cellUnit.linkGenome(cellUnitGenome)
            if event.key == pygame.K_g:
                cellUnit = Cell(type="granulocyte", screen=screen)
                print(cellUnit.attracted)
                CELL_LIST.append(cellUnit)
                cellUnitGenome = Genome(cellUnit)
                cellUnit.linkGenome(cellUnitGenome)
            if event.key == pygame.K_RIGHT:
                
                if selectedCellIndex < len(CELL_LIST):
                    selectedCellIndex += 1
                    if prevSelectedCell > 0:
                        CELL_LIST[prevSelectedCell - 1].setColor(screen)  # Reset the color of the previously clicked cell
                    CELL_LIST[selectedCellIndex - 1].setColor(screen)  # Set the color of the newly clicked cell
                    prevSelectedCell = selectedCellIndex  # Update the previously clicked cell
                    display_message = True
                    message = CELL_LIST[selectedCellIndex - 1].name + "\n Genome: 0002210" + "\n Index : " + str(selectedCellIndex)
                    CELL_LIST[selectedCellIndex - 1].color = (255, 120, 10)
                if selectedCellIndex > len(CELL_LIST):
                    selectedCellIndex = 0

            if event.key == pygame.K_LEFT:
                
                if selectedCellIndex > 0:
                    selectedCellIndex -= 1
                    if prevSelectedCell > 0:
                        CELL_LIST[prevSelectedCell - 1].setColor(screen)  # Reset the color of the previously clicked cell
                    CELL_LIST[selectedCellIndex - 1].setColor(screen)  # Set the color of the newly clicked cell
                    prevSelectedCell = selectedCellIndex  # Update the previously clicked cell
                    display_message = True
                    message = CELL_LIST[selectedCellIndex - 1].name + "\n Genome: 0002210"
                    CELL_LIST[selectedCellIndex - 1].color = (255, 120, 10)
                if selectedCellIndex < 0:
                    selectedCellIndex = len(CELL_LIST) - 1  
            if event.key == pygame.K_n: #LINK GENOME
                CELL_LIST[selectedCellIndex - 1].genome.linkGenome()
            if event.key == pygame.K_r:
                print("Genome for " + CELL_LIST[selectedCellIndex - 1].name)
                print(CELL_LIST[selectedCellIndex - 1].genome.genesList)



                

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
