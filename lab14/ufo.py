import pygame
from dataclasses import dataclass

WIDTH, HEIGHT = 800, 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Invasion")
clock = pygame.time.Clock()

SKY_COLOR = (0, 0, 0)
SUN_COLOR = (200, 200, 200)
SUN_POSITION = (WIDTH - 50, 50)
SUN_RADIUS = 150
GRASS_COLOR = (0, 128, 0)
GRASS_HEIGHT = 100
GRASS_TOP = HEIGHT - GRASS_HEIGHT
GRASS_RECTANGLE = (0, GRASS_TOP, WIDTH, GRASS_HEIGHT)


@dataclass
class UFO:
    x: int
    y: int
    width: int = 100
    height: int = 30
    color: tuple = (128, 128, 128)
    speed: int = 1

    def draw(self):
        pygame.draw.ellipse(
            screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(
            screen, self.color,
            (self.x + self.width//4, self.y-self.height//3, self.width//2, self.height))

    def move(self):
        self.x += self.speed
        if self.x > WIDTH:
            self.x = -self.width


ufos = [
    UFO(x=0, y=50, color=(0, 180, 255)),
    UFO(x=200, y=100, color=(200, 200, 5), speed=3.5, width=80, height=20),
    UFO(x=400, y=150, color=(35, 145, 160), width=120, speed=3),
    UFO(x=600, y=200, color=(255, 180, 80), speed=4),
    UFO(x=800, y=250, color=(5, 200, 255), width=105, speed=4.5),
    UFO(x=1000, y=300, color=(255, 180, 255), width=105, speed=5)]


def draw_scene():
    screen.fill(SKY_COLOR)
    pygame.draw.circle(screen, SUN_COLOR, SUN_POSITION, SUN_RADIUS)
    pygame.draw.rect(screen, GRASS_COLOR, GRASS_RECTANGLE)
    for ufo in ufos:
        ufo.draw()
        ufo.move()
        clock.tick(240)
    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    draw_scene()
