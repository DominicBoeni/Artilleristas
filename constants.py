import pygame
import random

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid-based Ballerburg")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (230, 230, 230)
RED = (255, 0, 0)
LIGHT_RED = (255, 150, 150)
BLUE = (0, 0, 255)
LIGHT_BLUE = (150, 150, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
DARKGREEN = (0, 100, 0)
MOUNTAIN_GREY = (128, 128, 128)

# Initialize fonts
pygame.font.init()
FONT = pygame.font.Font(None, 24)
FONT_SMALL = pygame.font.Font(None, 20)

# Constants
MOUNTAIN_MIN_DISTANCE = 12
MOUNTAIN_MAX_DISTANCE = 20
MOUNTAIN_HEIGHT_ABOVE_CASTLE = random.randint(10, 20)
COIN_LIMIT = 7
TURNS_PER_COIN = 5
CANNON_COST = 5
REPAIR_COST = 4
REPAIR_AMOUNT = 60
COIN_PER_TURN = 1

# Wind properties
WIND_MIN = -20
WIND_MAX = 20
current_wind = 0

# Castle properties
CASTLE_GRID_WIDTH = 10
CASTLE_GRID_HEIGHT = 15
SQUARE_SIZE = 13

# Cannon properties
CANNON_WIDTH = 2
CANNON_HEIGHT = 2
CANNON_HEALTH = 100

# Button properties
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 40

# Ground properties
GROUND_MIN_HEIGHT = 2
GROUND_MAX_HEIGHT = 4
GROUND_HEALTH = 100

# UI constants
UI_BOX_TOP = 50  # Changed from 550 to 50 to move UI to the top
UI_BOX_PADDING = 10
