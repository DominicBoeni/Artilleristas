import pygame
from constants import *

def draw_button(screen, x, y, text, color, width, height, enabled=True):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color if enabled else GRAY, button_rect, border_radius=5)
    pygame.draw.rect(screen, BLACK, button_rect, 1, border_radius=5)  # thin outline
    text_surface = FONT.render(text.upper(), True, BLACK if enabled else DARK_GRAY)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def draw_wind_indicator(screen, x, y, wind_strength):
    indicator_width = 100
    indicator_height = 30
    pygame.draw.rect(screen, LIGHT_GRAY, (x, y, indicator_width, indicator_height), border_radius=15)
    
    arrow_length = abs(wind_strength) * 4
    arrow_color = BLACK if abs(wind_strength) < 5 else (BLUE if wind_strength < 0 else RED)
    
    start_x = x + indicator_width // 2
    end_x = start_x + (arrow_length if wind_strength >= 0 else -arrow_length)
    
    pygame.draw.line(screen, arrow_color, (start_x, y + indicator_height // 2), 
                     (end_x, y + indicator_height // 2), 3)
    
    if wind_strength != 0:
        pygame.draw.polygon(screen, arrow_color, [
            (end_x, y + indicator_height // 2),
            (end_x - 5 * (1 if wind_strength >= 0 else -1), y + indicator_height // 2 - 5),
            (end_x - 5 * (1 if wind_strength >= 0 else -1), y + indicator_height // 2 + 5)
        ])
    
    wind_text = FONT_SMALL.render(f"{abs(wind_strength)}", True, BLACK)
    screen.blit(wind_text, (x + indicator_width // 2 - wind_text.get_width() // 2, y + indicator_height + 5))

def draw_ui(screen, current_player, current_wind):
    ui_left = 50 if current_player.is_left else WIDTH - 350
    ui_top = UI_BOX_TOP
    
    # Draw UI background
    pygame.draw.rect(screen, WHITE, (ui_left - UI_BOX_PADDING, ui_top - UI_BOX_PADDING, 
                                     300 + UI_BOX_PADDING * 2, 300 + UI_BOX_PADDING * 2), border_radius=10)
    
    # Draw angle controls
    draw_button(screen, ui_left, ui_top, "<<", LIGHT_BLUE, 30, 30)
    draw_button(screen, ui_left + 40, ui_top, "<", LIGHT_BLUE, 30, 30)
    draw_button(screen, ui_left + 180, ui_top, ">", LIGHT_BLUE, 30, 30)
    draw_button(screen, ui_left + 220, ui_top, ">>", LIGHT_BLUE, 30, 30)
    
    angle_text = FONT.render(f"Angle: {current_player.cannons[current_player.selected_cannon].angle}°", True, BLACK)
    screen.blit(angle_text, (ui_left + 80, ui_top + 5))
    
    # Draw power controls
    draw_button(screen, ui_left, ui_top + 40, "++", LIGHT_RED, 30, 30)
    draw_button(screen, ui_left + 40, ui_top + 40, "+", LIGHT_RED, 30, 30)
    draw_button(screen, ui_left + 180, ui_top + 40, "-", LIGHT_RED, 30, 30)
    draw_button(screen, ui_left + 220, ui_top + 40, "--", LIGHT_RED, 30, 30)
    
    power_text = FONT.render(f"Power: {current_player.cannons[current_player.selected_cannon].power}", True, BLACK)
    screen.blit(power_text, (ui_left + 80, ui_top + 45))
    
    # Draw action buttons
    draw_button(screen, ui_left, ui_top + 80, "Fire", GREEN, 250, 40)
    draw_button(screen, ui_left, ui_top + 130, f"Buy Cannon ({CANNON_COST})", YELLOW, 250, 40, current_player.coins >= CANNON_COST)
    draw_button(screen, ui_left, ui_top + 180, f"Repair ({REPAIR_COST})", ORANGE, 250, 40, current_player.coins >= REPAIR_COST)
    
    # Draw player info
    coins_text = FONT.render(f"Coins: {current_player.coins}", True, BLACK)
    screen.blit(coins_text, (ui_left, ui_top + 230))
    
    turns_text = FONT.render(f"Turns: {current_player.turns}", True, BLACK)
    screen.blit(turns_text, (ui_left + 150, ui_top + 230))
    
    # Draw wind indicator
    draw_wind_indicator(screen, WIDTH // 2, 30, current_wind)
    wind_text = FONT.render(f"Wind: {current_wind}", True, BLACK)
    screen.blit(wind_text, (WIDTH // 2 - 50, 10))

    # Display selected cannon
    selected_cannon_text = FONT.render(f"Selected Cannon: {current_player.selected_cannon + 1}", True, BLACK)
    screen.blit(selected_cannon_text, (ui_left, ui_top + 260))

    # Display repair mode if active
    if current_player.repair_mode:
        repair_text = FONT.render(f"Repair Mode: {current_player.repair_points_left} points", True, BLACK)
        screen.blit(repair_text, (ui_left, ui_top + 290))

def handle_button_click(pos, current_player):
    ui_left = 50 if current_player.is_left else WIDTH - 350
    ui_top = UI_BOX_TOP
    x, y = pos

    # Angle controls
    if ui_top <= y < ui_top + 30:
        if ui_left <= x < ui_left + 30: return "angle", -5
        elif ui_left + 40 <= x < ui_left + 70: return "angle", -1
        elif ui_left + 180 <= x < ui_left + 210: return "angle", 1
        elif ui_left + 220 <= x < ui_left + 250: return "angle", 5

    # Power controls
    if ui_top + 40 <= y < ui_top + 70:
        if ui_left <= x < ui_left + 30: return "power", 5
        elif ui_left + 40 <= x < ui_left + 70: return "power", 1
        elif ui_left + 180 <= x < ui_left + 210: return "power", -1
        elif ui_left + 220 <= x < ui_left + 250: return "power", -5

    # Action buttons
    if ui_left <= x < ui_left + 250:
        if ui_top + 80 <= y < ui_top + 120: return "fire", None
        elif ui_top + 130 <= y < ui_top + 170: return "buy_cannon", None
        elif ui_top + 180 <= y < ui_top + 220: return "repair", None

    return None, None
