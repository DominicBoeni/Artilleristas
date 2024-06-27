from constants import *
import pygame
from PIL import Image, ImageDraw

def create_ruler_image(ruler_type):
    width, height = SQUARE_SIZE * 2, SQUARE_SIZE * 3
    image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    if ruler_type == 'King':
        # Draw a simple crown
        draw.polygon([(width//4, height//4), (width//2, 0), (3*width//4, height//4)], fill=(255, 215, 0))
        draw.rectangle([width//4, height//4, 3*width//4, height//3], fill=(255, 215, 0))
    else:  # Queen
        # Draw a simple tiara
        draw.arc([0, 0, width, height//2], 0, 180, fill=(255, 215, 0), width=5)
        draw.rectangle([0, height//4, width, height//3], fill=(255, 215, 0))
    
    # Draw the body
    draw.rectangle([width//4, height//3, 3*width//4, height], fill=(150, 150, 150))
    
    # Convert to PyGame surface
    mode = image.mode
    size = image.size
    data = image.tobytes()
    return pygame.image.fromstring(data, size, mode)

class Ruler:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.image = create_ruler_image(type)
        self.image = pygame.transform.scale(self.image, (SQUARE_SIZE * 2, SQUARE_SIZE * 3))