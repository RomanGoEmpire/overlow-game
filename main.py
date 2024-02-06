import pygame

from overflow import SCREEN_SIZE, PLAYER_COUNT, Player, Game


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Overflow")
    players = [
        Player("Player 1", (255, 0, 0)),
        Player("Player 2", (0, 255, 0)),
        Player("Player 3", (0, 0, 255)),
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
        game.visualizer.draw(screen)
        pygame.display.update()
        pygame.time.delay(100)
        game.play()
