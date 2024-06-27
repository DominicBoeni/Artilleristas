import pygame
import random
import math
from constants import *
from cannon import Cannon
from ruler import Ruler
from square import Square
from constants import SQUARE_SIZE, CASTLE_GRID_WIDTH, CASTLE_GRID_HEIGHT


class Player:
    def __init__(self, x, y, color, light_color, is_left):
        self.castle_x = x
        self.castle_y = y
        self.color = color
        self.light_color = light_color
        self.is_left = is_left
        self.grid = [[Square(x + i * SQUARE_SIZE, y + j * SQUARE_SIZE) for i in range(CASTLE_GRID_WIDTH)] for j in range(CASTLE_GRID_HEIGHT)]
        self.ruler_type = random.choice(['King', 'Queen'])
        self.ruler = Ruler(x + 4 * SQUARE_SIZE, y + 11 * SQUARE_SIZE, self.ruler_type)
        self.place_ruler()
        self.cannons = [
            Cannon(x + SQUARE_SIZE, y - SQUARE_SIZE * 2, is_left),
            Cannon(x + SQUARE_SIZE * 8, y - SQUARE_SIZE * 2, is_left)
        ]
        self.selected_cannon = 0
        self.coins = 3
        self.turns = 0
        self.repair_mode = False
        self.repair_points_left = 0

    def place_ruler(self):
        ruler_x = 4
        ruler_y = 11
        for i in range(ruler_x - 1, ruler_x + 3):
            for j in range(ruler_y - 1, ruler_y + 4):
                if i == ruler_x - 1 or i == ruler_x + 2 or j == ruler_y - 1 or j == ruler_y + 3:
                    self.grid[j][i].type = 'air'
                    self.grid[j][i].health = 0
                elif j >= ruler_y and j < ruler_y + 3 and i >= ruler_x and i < ruler_x + 2:
                    self.grid[j][i].type = 'ruler'
                    self.grid[j][i].health = 0

    def add_coin(self):
        if self.coins < COIN_LIMIT:
            self.coins += 1

    def buy_cannon(self):
        if self.coins >= CANNON_COST:
            new_cannon_x = self.castle_x + SQUARE_SIZE * (1 if self.is_left else 8)
            new_cannon_y = self.castle_y - SQUARE_SIZE * 2
            self.cannons.append(Cannon(new_cannon_x, new_cannon_y, self.is_left))
            self.coins -= CANNON_COST
            return True
        return False
    
    def draw(self, screen):
        # Draw castle
        for row in self.grid:
            for square in row:
                if square.type == 'stone':
                    pygame.draw.rect(screen, self.color, (square.x, square.y, SQUARE_SIZE, SQUARE_SIZE))
                    pygame.draw.rect(screen, self.light_color, (square.x, square.y, SQUARE_SIZE, SQUARE_SIZE), 1)
                    
                    if square.health < 50:
                        damage_percentage = (50 - square.health) / 50
                        pygame.draw.line(screen, (100, 100, 100), (square.x, square.y), 
                                         (square.x + SQUARE_SIZE * damage_percentage, square.y + SQUARE_SIZE * damage_percentage), 2)
                        if damage_percentage > 0.5:
                            pygame.draw.line(screen, (100, 100, 100), (square.x + SQUARE_SIZE, square.y), 
                                             (square.x + SQUARE_SIZE * (1 - damage_percentage), square.y + SQUARE_SIZE * damage_percentage), 2)
        
        # Draw ruler
        screen.blit(self.ruler.image, (self.ruler.x, self.ruler.y))

        # Draw cannons
        for cannon in self.cannons:
            self.draw_cannon(screen, cannon)

    def draw_cannon(self, screen, cannon):
        cannon_color = (100, 100, 100)
        pygame.draw.rect(screen, cannon_color, (cannon.x, cannon.y, SQUARE_SIZE * 2, SQUARE_SIZE))
        
        # Draw cannon barrel
        angle_rad = math.radians(cannon.angle)
        end_x = cannon.x + SQUARE_SIZE + math.cos(angle_rad) * SQUARE_SIZE * 1.5
        end_y = cannon.y + SQUARE_SIZE / 2 - math.sin(angle_rad) * SQUARE_SIZE * 1.5
        pygame.draw.line(screen, cannon_color, (cannon.x + SQUARE_SIZE, cannon.y + SQUARE_SIZE / 2), (end_x, end_y), 5)

        # Draw health bar
        health_percentage = cannon.health / CANNON_HEALTH
        pygame.draw.rect(screen, (200, 70, 70), (cannon.x, cannon.y - 10, SQUARE_SIZE * 2, 5))
        pygame.draw.rect(screen, (70, 200, 70), (cannon.x, cannon.y - 10, SQUARE_SIZE * 2 * health_percentage, 5))

    def can_repair(self, x, y):
        # Check if within 5 squares of initial outer walls
        max_distance = 5 * SQUARE_SIZE
        if (x < self.castle_x - max_distance or 
            x >= self.castle_x + CASTLE_GRID_WIDTH * SQUARE_SIZE + max_distance or
            y < self.castle_y - max_distance or 
            y >= self.castle_y + CASTLE_GRID_HEIGHT * SQUARE_SIZE + max_distance):
            return False

        # Check if connected to a solid square
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx * SQUARE_SIZE, y + dy * SQUARE_SIZE
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                grid_x = (nx - self.castle_x) // SQUARE_SIZE
                grid_y = (ny - self.castle_y) // SQUARE_SIZE
                if 0 <= grid_x < CASTLE_GRID_WIDTH and 0 <= grid_y < CASTLE_GRID_HEIGHT:
                    if self.grid[grid_y][grid_x].type in ['stone', 'ground', 'mountain']:
                        return True
        return False

    def repair_square(self, x, y):
        if not self.can_repair(x, y):
            return False

        grid_x = (x - self.castle_x) // SQUARE_SIZE
        grid_y = (y - self.castle_y) // SQUARE_SIZE

        if 0 <= grid_x < CASTLE_GRID_WIDTH and 0 <= grid_y < CASTLE_GRID_HEIGHT:
            square = self.grid[grid_y][grid_x]
            if square.type == 'stone':
                square.health = min(square.health + 25, 100)
            elif square.type == 'air':
                square.type = 'stone'
                square.health = 100
            else:
                return False
            self.repair_points_left -= 1
            return True
        return False