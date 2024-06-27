import pygame
from constants import *
import random
import math
from ground import create_ground
from player import Player
from game_state import GameState

def handle_game_action(action, value, game_state):
    current_player = game_state.current_player
    if action == "angle":
        active_cannon = current_player.cannons[current_player.selected_cannon]
        if current_player.is_left:
            active_cannon.angle = max(0, min(180, active_cannon.angle + value))
        else:
            active_cannon.angle = max(0, min(180, active_cannon.angle - value))
    elif action == "power":
        active_cannon = current_player.cannons[current_player.selected_cannon]
        active_cannon.power = max(10, min(100, active_cannon.power + value))
    elif action == "fire" and not game_state.game_over:
        active_cannon = current_player.cannons[current_player.selected_cannon]
        hit = fire_cannon(current_player, active_cannon, game_state)
        if hit:
            # Check if the opponent has lost
            opponent = game_state.player2 if current_player == game_state.player1 else game_state.player1
            if not opponent.cannons:
                game_state.game_over = True
            # Check for ruler defeat (assuming the ruler's health is stored in the grid)
            ruler_defeated = all(square.type != 'ruler' for row in opponent.grid for square in row)
            if ruler_defeated:
                game_state.game_over = True
        game_state.end_turn()
    elif action == "buy_cannon":
        if current_player.buy_cannon():
            current_player.selected_cannon = len(current_player.cannons) - 1
    elif action == "repair" and current_player.coins >= REPAIR_COST:
        current_player.coins -= REPAIR_COST
        current_player.repair_mode = True
        current_player.repair_points_left = REPAIR_AMOUNT
    elif action == "repair_click" and current_player.repair_mode and current_player.repair_points_left > 0:
        x, y = value
        if current_player.repair_square(x, y):
            if current_player.repair_points_left == 0:
                current_player.repair_mode = False
                game_state.end_turn()

    return game_state.game_over


def end_turn(current_player, player1, player2):
    current_player.add_coin()
    update_wind()
    current_player.repair_mode = False
    new_current_player = player2 if current_player == player1 else player1
    if new_current_player.cannons:
        new_current_player.selected_cannon = 0
        return new_current_player, False  # Not game over
    else:
        return current_player, True  # Game over, current player wins

def restart_game():
    global player1, player2, current_player, game_over, ground
    ground = create_ground()
    player1 = Player(50, HEIGHT - CASTLE_GRID_HEIGHT * SQUARE_SIZE - ground[50 // SQUARE_SIZE] * SQUARE_SIZE, RED, LIGHT_RED, True)
    player2 = Player(WIDTH - 50 - CASTLE_GRID_WIDTH * SQUARE_SIZE, HEIGHT - CASTLE_GRID_HEIGHT * SQUARE_SIZE - ground[(WIDTH - 50) // SQUARE_SIZE] * SQUARE_SIZE, BLUE, LIGHT_BLUE, False)
    current_player = player1
    player1.repair_mode = False
    player2.repair_mode = False
    game_over = False

def update_wind():
    global current_wind
    current_wind = random.randint(WIND_MIN, WIND_MAX)

def handle_repair(player, pos):
    x, y = pos
    repaired = False

    # Check if clicked on a castle square
    grid_x = int((x - player.castle_x) // SQUARE_SIZE)
    grid_y = int((y - player.castle_y) // SQUARE_SIZE)
    if 0 <= grid_x < CASTLE_GRID_WIDTH and 0 <= grid_y < CASTLE_GRID_HEIGHT:
        square = player.grid[grid_y][grid_x]
        if square.type == 'stone' and square.health < 50:
            repair_amount = min(10, 50 - square.health, player.repair_points_left)
            square.health += repair_amount
            player.repair_points_left -= repair_amount
            repaired = True

    # Check if clicked on a cannon
    for cannon in player.cannons:
        if (cannon.x <= x < cannon.x + SQUARE_SIZE * CANNON_WIDTH and
            cannon.y <= y < cannon.y + SQUARE_SIZE * CANNON_HEIGHT):
            if cannon.health < CANNON_HEALTH:
                repair_amount = min(10, CANNON_HEALTH - cannon.health, player.repair_points_left)
                cannon.health += repair_amount
                player.repair_points_left -= repair_amount
                repaired = True
                break

    return repaired

def check_collision(x, y, firing_player, force, game_state):
    # Check collision with ground
    ground_height = game_state.ground[int(x) // SQUARE_SIZE] * SQUARE_SIZE
    if y >= HEIGHT - ground_height:
        return True, 0

    # Check collision with players
    for player in [game_state.player1, game_state.player2]:
        if player != firing_player:
            castle_x = player.castle_x
            castle_y = player.castle_y
            for i in range(CASTLE_GRID_WIDTH):
                for j in range(CASTLE_GRID_HEIGHT):
                    square = player.grid[j][i]
                    square_x = castle_x + i * SQUARE_SIZE
                    square_y = castle_y + j * SQUARE_SIZE
                    if square_x <= x < square_x + SQUARE_SIZE and square_y <= y < square_y + SQUARE_SIZE:
                        if square.type != 'air':
                            square.health -= force
                            if square.health <= 0:
                                square.type = 'air'
                                square.health = 0
                            return True, force // 2

            # Check collision with player's cannons
            for cannon in player.cannons:
                if (cannon.x <= x < cannon.x + SQUARE_SIZE * CANNON_WIDTH and
                    cannon.y <= y < cannon.y + SQUARE_SIZE * CANNON_HEIGHT):
                    cannon.health -= force
                    if cannon.health <= 0:
                        player.cannons.remove(cannon)
                    return True, force // 2

            # Check collision with player's ruler
            ruler_x = castle_x + 4 * SQUARE_SIZE
            ruler_y = castle_y + 11 * SQUARE_SIZE
            if (ruler_x <= x < ruler_x + 2 * SQUARE_SIZE and
                ruler_y <= y < ruler_y + 3 * SQUARE_SIZE):
                player.ruler.health -= force
                if player.ruler.health <= 0:
                    game_state.game_over = True
                return True, 0

    return False, force

def fire_cannon(player, cannon, game_state):
    start_x = cannon.x + SQUARE_SIZE
    start_y = cannon.y + SQUARE_SIZE
    angle = math.radians(cannon.angle)
    velocity_x = math.cos(angle) * cannon.power / 2.5 + game_state.current_wind / 10
    velocity_y = -math.sin(angle) * cannon.power / 2.5
    
    x, y = start_x, start_y
    force = cannon.power
    
    screen = pygame.display.get_surface()
    
    # Create a surface for the trajectory
    trajectory_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    while 0 <= x < WIDTH and force > 0:
        if 0 <= y < HEIGHT:
            # Draw trajectory
            pygame.draw.circle(trajectory_surface, (200, 200, 200, 100), (int(x), int(y)), 2)
            
            # Draw current position
            pygame.draw.circle(screen, (200, 70, 70), (int(x), int(y)), 4)
            screen.blit(trajectory_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(20)
        
        old_x, old_y = x, y
        x += velocity_x
        y += velocity_y
        velocity_y += 0.25  # Reduced gravity effect
        
        # Check collision
        steps = max(abs(int(x - old_x)), abs(int(y - old_y)))
        for i in range(steps):
            check_x = old_x + (x - old_x) * i / steps
            check_y = old_y + (y - old_y) * i / steps
            hit, force = check_collision(check_x, check_y, player, force, game_state)
            if hit and force <= 0:
                # Draw impact
                pygame.draw.circle(screen, (255, 200, 50), (int(check_x), int(check_y)), 10)
                pygame.display.flip()
                pygame.time.delay(100)
                return True
        
        if x < 0 or x >= WIDTH or y >= HEIGHT:
            return False
    
    return False

