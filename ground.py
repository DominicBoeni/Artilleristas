import random
from constants import *

def create_mountain(ground, castle1_x, castle2_x, base_height):
    mountain_start = random.randint(castle1_x + MOUNTAIN_MIN_DISTANCE * SQUARE_SIZE, 
                                    castle1_x + MOUNTAIN_MAX_DISTANCE * SQUARE_SIZE) // SQUARE_SIZE
    mountain_end = random.randint(castle2_x - MOUNTAIN_MAX_DISTANCE * SQUARE_SIZE, 
                                  castle2_x - MOUNTAIN_MIN_DISTANCE * SQUARE_SIZE) // SQUARE_SIZE
    mountain_peak = max(ground) + MOUNTAIN_HEIGHT_ABOVE_CASTLE
    
    for i in range(mountain_start, mountain_end + 1):
        progress = (i - mountain_start) / (mountain_end - mountain_start)
        height = int(base_height + (mountain_peak - base_height) * (1 - abs(2 * progress - 1)))
        jitter = random.randint(-1, 1)
        ground[i] = max(ground[i], height + jitter)
    
    return ground

def create_ground():
    ground = [random.randint(GROUND_MIN_HEIGHT, GROUND_MAX_HEIGHT) for _ in range(WIDTH // SQUARE_SIZE)]
    
    # Smooth the ground
    for i in range(1, len(ground) - 1):
        if abs(ground[i] - ground[i-1]) > 1:
            ground[i] = ground[i-1] + (1 if ground[i] > ground[i-1] else -1)
    
    # Set the ground under and around castles
    castle1_start = 50 // SQUARE_SIZE
    castle2_start = (WIDTH - 50 - CASTLE_GRID_WIDTH * SQUARE_SIZE) // SQUARE_SIZE
    for i in range(castle1_start - 3, castle1_start + CASTLE_GRID_WIDTH + 3):
        ground[i] = 3
    for i in range(castle2_start - 3, castle2_start + CASTLE_GRID_WIDTH + 3):
        ground[i] = 3
    
    # Create mountain
    mountain_base = 3  # Height of the base of the mountain
    ground = create_mountain(ground, 50, WIDTH - 50 - CASTLE_GRID_WIDTH * SQUARE_SIZE, mountain_base)
    
    return ground

def draw_ground(screen, ground):
    for x, height in enumerate(ground):
        if height > GROUND_MAX_HEIGHT:
            pygame.draw.rect(screen, MOUNTAIN_GREY, (x * SQUARE_SIZE, HEIGHT - height * SQUARE_SIZE, SQUARE_SIZE, height * SQUARE_SIZE))
        else:
            pygame.draw.rect(screen, DARKGREEN, (x * SQUARE_SIZE, HEIGHT - height * SQUARE_SIZE, SQUARE_SIZE, height * SQUARE_SIZE))

