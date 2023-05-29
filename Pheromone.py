import pygame
class Pheromone:
    def __init__(self,parentCell, type):
        self.parent = parentCell
        self.x = parentCell.x
        self.y = parentCell.y
        self.timer = 100
        self.type = type
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.parent.color, (self.y, self.x), radius=2)
    
    def getID(self):
        return self.parent.ID
