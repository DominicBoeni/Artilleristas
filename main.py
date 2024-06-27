import pygame
from constants import *
from player import Player
from ground import create_ground, draw_ground
from ui import draw_ui, handle_button_click
from game_logic import handle_game_action
from game_state import GameState

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid-based Ballerburg")

ground = create_ground()

player1 = Player(50, HEIGHT - CASTLE_GRID_HEIGHT * SQUARE_SIZE - ground[50 // SQUARE_SIZE] * SQUARE_SIZE, RED, LIGHT_RED, True)
player2 = Player(WIDTH - 50 - CASTLE_GRID_WIDTH * SQUARE_SIZE, HEIGHT - CASTLE_GRID_HEIGHT * SQUARE_SIZE - ground[(WIDTH - 50) // SQUARE_SIZE] * SQUARE_SIZE, BLUE, LIGHT_BLUE, False)

game_state = GameState(player1, player2, ground)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            if game_state.current_player.repair_mode:
                handle_game_action("repair_click", event.pos, game_state)
            else:
                action, value = handle_button_click(event.pos, game_state.current_player)
                if action:
                    handle_game_action(action, value, game_state)
        elif event.type == pygame.KEYDOWN:
            if game_state.current_player.cannons:
                if event.key == pygame.K_LEFT:
                    value = -5 if pygame.key.get_mods() & pygame.KMOD_SHIFT else -1
                    handle_game_action("angle", value, game_state)
                elif event.key == pygame.K_RIGHT:
                    value = 5 if pygame.key.get_mods() & pygame.KMOD_SHIFT else 1
                    handle_game_action("angle", value, game_state)
                elif event.key == pygame.K_UP:
                    value = 5 if pygame.key.get_mods() & pygame.KMOD_SHIFT else 1
                    handle_game_action("power", value, game_state)
                elif event.key == pygame.K_DOWN:
                    value = -5 if pygame.key.get_mods() & pygame.KMOD_SHIFT else -1
                    handle_game_action("power", value, game_state)
                elif event.key == pygame.K_TAB:
                    game_state.current_player.selected_cannon = (game_state.current_player.selected_cannon + 1) % len(game_state.current_player.cannons)
                elif event.key == pygame.K_SPACE and not game_state.game_over:
                    handle_game_action("fire", None, game_state)

    # Clear the screen
    screen.fill(WHITE)

    # Draw game elements
    draw_ground(screen, game_state.ground)
    game_state.player1.draw(screen)
    game_state.player2.draw(screen)
    for player in [game_state.player1, game_state.player2]:
        for i, cannon in enumerate(player.cannons):
            player.draw_cannon(screen, cannon)
            if i == player.selected_cannon and player == game_state.current_player:
                pygame.draw.circle(screen, (0, 255, 0), (int(cannon.x + SQUARE_SIZE), int(cannon.y + SQUARE_SIZE)), SQUARE_SIZE + 5, 2)

    draw_ui(screen, game_state.current_player, game_state.current_wind)

    if game_state.current_player.repair_mode:
        font = pygame.font.Font(None, 36)
        repair_text = font.render(f"Repair Mode: {game_state.current_player.repair_points_left} points left", True, BLACK)
        ui_left = 50 if game_state.current_player.is_left else WIDTH - 350
        screen.blit(repair_text, (ui_left, HEIGHT - 40))

    if game_state.game_over:
        winner = "Player 1" if game_state.current_player != game_state.player1 else "Player 2"
        font = pygame.font.Font(None, 36)
        game_over_text = font.render(f"{winner} wins!", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 70, HEIGHT // 2))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

pygame.quit()


