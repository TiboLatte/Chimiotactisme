import random
import math
import pygame
import Pheromone
import codecs
import random
import string

class Cell:

    def __init__(self, type, screen):
        self.name = self.getName()
        self.WIDTH = 1080
        self.HEIGHT = 720
        self.radius = random.randint(10, 30)
        self.ID = random.randint(0, 1000)
        self.genome = None
        self.agac = ''.join(random.choice(string.ascii_lowercase) for _ in range(20))
        #Calculate the valid range for x and y positions, 0 is for readability
        x_min = 0 + self.radius *2 + self.radius
        x_max = self.WIDTH - self.radius * 2 - self.radius
        y_min = 0 + self.radius *2
        y_max = self.HEIGHT - self.radius * 3

        self.x = random.uniform(x_min, x_max)
        self.y = random.uniform(y_min, y_max)

      
        self.prevX = self.x
        self.prevY = self.y
        self.dx = 0
        self.dy = 0
        self.visited_pheromones = []
        self.speed = random.randint(1, 5)
        self.pheromone_count = 0
        self.isPheromoneInSight = False
        self.sensorRadius = self.radius + 2 * self.radius

        self.type = type
        self.setColor(screen)

    def setColor(self, screen):
        if self.type == "inflammatory":
            self.attracted = "none"
            self.secrete = "path"
            self.color = (255, 0, 0)
        elif self.type == "mastocyte":
            self.attracted = "path"
            self.secrete = "his"
            self.color = (0, 255, 0)
        elif self.type == "granulocyte":
            self.attracted = "his"
            self.secrete = "ILX"
            self.color = (0, 0, 255)
        else:
            self.attracted = "none"
            self.secrete = "none"
        self.draw(screen)

    def linkGenome(self, genome):
        self.genome = genome
        print("[INFO] : Linking Genome for cell %s" % self.name)
    def getName(self):
        with codecs.open("names.txt", mode="r+", encoding = "utf-8") as f:
            lines = f.readlines()
            name = random.choice(lines)
            name = name[:len(name)-2]
            
            return name

    def move(self, pheromones, cells):
        speed = self.speed
        rand = random.uniform(0, 1)

        best_pheromone = None
        best_weight = 0
        closestCell = None
        closestCellWeight = 0

        for pheromone in pheromones:
            best_pheromone, best_weight = self.get_pheromone_and_weight(pheromone, best_weight, best_pheromone)

        # If a suitable pheromone was found, move towards it
        if best_pheromone is not None:
            self.isPheromoneInSight = True
            angle = math.atan2(best_pheromone.y - self.y, best_pheromone.x - self.x)
            self.dx = math.cos(angle) * speed
            self.dy = math.sin(angle) * speed
            distance = self.calculateDistance(best_pheromone)
            if distance < 10:
                self.visited_pheromones.append(best_pheromone)
                bestPheromoneIndex = pheromones.index(best_pheromone)
                pheromones.pop(bestPheromoneIndex)
            
            for cell in cells:
                if self.type == "granulocyte":
                    closestCell, closestCellWeight = self.get_cell_and_weight(cell, closestCellWeight, closestCell, "inflammatory")

            if closestCell is not None:
                self.setColor()
                cells.remove(closestCell)
                self.color = (255, 200, 0)

        # Otherwise, move randomly with a probability of 0.1
        elif rand < 0.1:
            self.isPheromoneInSight = False
            angle = random.uniform(0.8, 2 * math.pi)
            self.dx = math.cos(angle) * speed
            self.dy = math.sin(angle) * speed

        for pheromone in pheromones:
            pheromone.timer -= 0.1
            if pheromone.timer <= 0:
                pheromones.remove(pheromone)

        # Update the cell's position
        new_x = self.x + self.dx
        new_y = self.y + self.dy

        # Check if the new position is within the window boundaries
        if (
            self.radius * 2 <= new_x <= self.WIDTH - self.radius * 2
            and self.radius * 2 <= new_y <= self.HEIGHT - self.radius * 2
        ):
            self.x = new_x
            self.y = new_y

        pheromone_threshold = 5

        if self.pheromone_count >= pheromone_threshold:
            self.visited_pheromones = []
            self.pheromone_count = 0
            print("Resetting pheromone count")

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (self.y, self.x), radius=self.radius)

    def dropPheromone(self, PHEROMONE_LIST, screen):
        if abs(self.x - self.prevX) > 20 or abs(self.y - self.prevY) > 20:

            self.prevX = self.x
            self.prevY = self.y
            pheromone = Pheromone.Pheromone(self, self.secrete)
            PHEROMONE_LIST.append(pheromone)

        for pheromone in PHEROMONE_LIST:
            pheromone.draw(screen)

    def is_close_to_pheromone(self, pheromone, range):
        distance = math.sqrt((pheromone.x - self.x)**2 +
                             (pheromone.y - self.y)**2)
        return distance < range

    def drawSensor(self, screen):
        if self.isPheromoneInSight:
            pygame.draw.circle(screen, (255, 0, 0),
                               (self.y, self.x), radius=self.sensorRadius, width=2)
        else:
            pygame.draw.circle(screen, (0, 255, 0),
                               (self.y, self.x), radius=self.sensorRadius, width=2)

    def calculateDistance(self, object):
        return math.sqrt((object.x - self.x) **
                         2 + (object.y - self.y) ** 2)

    def calculateDirection(self, object):
        return math.atan2(object.y - self.y, object.x-self.x)

    def get_pheromone_and_weight(self, pheromone, best_weight, best_pheromone):
        if pheromone.parent != self and pheromone not in self.visited_pheromones and pheromone.type == self.attracted:
            # Calculate the distance between the pheromone and the cell
            distance = self.calculateDistance(pheromone)  # Cell with pheromone
            if distance <= self.sensorRadius:
                # Calculate the direction from the cell to the pheromone
                direction = self.calculateDirection(pheromone)

                # Calculate the direction of the cell's movement
                movement_direction = math.atan2(self.dy, self.dx)

                # Calculate the weight of the pheromone
                weight = distance * math.cos(direction - movement_direction)

                # Update the best pheromone if this one has a higher weight
                if weight > best_weight:
                    best_pheromone = pheromone
                    best_weight = weight
        return best_pheromone, best_weight

    def get_cell_and_weight(self, cell, closestCellWeight, closestCell, type):
        if cell != self and cell.type == type:
            distance = self.calculateDistance(cell)
            if distance <= self.sensorRadius:
                direction = self.calculateDirection(cell)
                movementDirection = math.atan2(self.dy, self.dx)

                weight = distance * math.cos(direction - movementDirection)

                if weight > closestCellWeight:
                    closestCell = cell
                    closestCellWeight = weight
        return closestCell, closestCellWeight