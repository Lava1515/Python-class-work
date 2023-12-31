import os
import pygame


WIN = pygame.display.set_mode((1000, 500))
FPS = 60
Image = pygame.image.load(os.path.join('Lava.png'))
Image = pygame.transform.scale(Image, (1000, 500))
# Image = pygame.transform.rotate(Image, 90) # rotate image


def draw_Win(player):
    WIN.fill((255, 0, 0))
    WIN.blit(Image, (player.x, player.y))
    pygame.display.update()


def move_player(keys_pressed, player):
    if keys_pressed[pygame.K_a] and player.x > 0: # go left
        player.x -= 1
    if keys_pressed[pygame.K_d] and player.x + 1000 < 1000:  # go right
        print(player.x)
        player.x += 1
    if keys_pressed[pygame.K_s]:  # go down
        player.y += 1
    if keys_pressed[pygame.K_w]:  # go up
        player.y -= 1


def main():
    player = pygame.Rect(0, 0, 1000, 500) # x , y , image width , image highet

    clock = pygame.time.Clock()
    run = True

    while run:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        move_player(keys_pressed, player)

        draw_Win(player)

    pygame.quit()


if __name__ == '__main__':
    main()
