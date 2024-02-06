import pygame

from overflow import SCREEN_SIZE, PLAYER_COUNT, Player, Game


def convert_hex_to_rgb(hex_color: str) -> tuple:
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Overflow")
    players = [
        Player("Player 1", convert_hex_to_rgb("#4EADF9")),
        Player("Player 2", convert_hex_to_rgb("#80D540")),
        Player("Player 3", convert_hex_to_rgb("#D1B03A")),
    ]
    if len(players) != PLAYER_COUNT:
        raise ValueError(f"Player count must be {PLAYER_COUNT}")

    game = Game(players)

    print("Setup the game")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game.visualizer.draw(screen, game.current_player)
        pygame.display.update()
        pygame.time.delay(100)
        game.play()
