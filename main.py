import pygame
import random
import math
import sys

pygame.init()

screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Pygame Pong")

clock = pygame.time.Clock()

enemy_score = 0
player_score = 0

font = pygame.font.Font(None, 24)
e_text = font.render(f"{player_score}", True ,(0,0,0))



# paddle
class paddle(pygame.sprite.Sprite):         
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((50, 10))
        self.image.fill((52, 43, 43))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x - 25, y)

    def pupdate(self, speed):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.rect.x -= speed
        elif key[pygame.K_RIGHT]:
            self.rect.x += speed

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(1000, self.rect.right)

    def eupdate(self, bx, speed):
        if self.rect.centerx < bx:
            self.rect.x += speed
        elif self.rect.centerx > bx:
            self.rect.x -= speed

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(1000, self.rect.right)


# ball
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (48, 56, 65), (10, 10), 10)

        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 5
        self.angel = random.choice([45, 135, 225, 315])

        self.colliding = set()

        self.x = float(x)
        self.y = float(y)

    def update(self, group, width, heigh, player_score,  enemy_score):

        rad = math.radians(self.angel)

        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

        self.rect.center = (round(self.x), round(self.y))


        if self.rect.left <= 0:
            self.x = 10
            self.angel = 180 - self.angel

        elif self.rect.right >= width:
            self.x = width - 10
            self.angel = 180 - self.angel

        if self.rect.top <= 0:
            enemy_score += 1
            self.reset()

        elif self.rect.bottom >= heigh:
            player_score += 1
            self.reset()

        self.angel %= 360

        self.rect.center = (round(self.x), round(self.y))


        hits = pygame.sprite.spritecollide(self, group, False)

        current_hits = set(hits)

        for hit in hits:
            if hit not in self.colliding:

                self.angel = (360 - self.angel) % 360

                if self.rect.centery < hit.rect.centery:
                    self.y = hit.rect.top - 10
                else:
                    self.y = hit.rect.bottom + 10

                self.rect.center = (round(self.x), round(self.y))

                break

        self.colliding = current_hits

        return player_score, enemy_score

    def reset(self):
        self.__init__(500, 300)


epaddle = paddle(500, 5)
ppaddle = paddle(500, 585)
ball = Ball(500, 300)

paddles = pygame.sprite.Group()
enemys = pygame.sprite.Group()
players = pygame.sprite.Group()
balls = pygame.sprite.Group()

paddles.add(epaddle)
paddles.add(ppaddle)
enemys.add(epaddle)
players.add(ppaddle)
balls.add(ball)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    e_text = font.render(f"{player_score}", True ,(0,0,0))
    p_text = font.render(f"{enemy_score}", True ,(0,0,0))

    screen.fill((222, 251, 194))

    for enemy in enemys:
        enemy.eupdate(ball.rect.centerx + random.randint(0, 30), 4)

    for player in players:
        player.pupdate(5)

    player_score, enemy_score = ball.update(
    paddles, 1000, 600, player_score, enemy_score
)

    screen.blit(e_text, (480, 250))
    screen.blit(p_text, (480, 350))

    enemys.draw(screen)
    players.draw(screen)
    balls.draw(screen)

    pygame.display.update()
    clock.tick(60)
