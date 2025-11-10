import pygame
import math
from dataclasses import dataclass
import pygame.freetype

pygame.init()

try:
    pygame.mixer.init()
    try:
        game_over_sound = pygame.mixer.Sound("game_over.wav")
    except pygame.error:
        game_over_sound = None
except pygame.error:
    game_over_sound = None

game_over = False

WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("K'tah")
clock = pygame.time.Clock()
font = pygame.freetype.SysFont('sans', 100)
GRASS_COLOR = (0, 100, 0)
frozen = False
UNFREEZE = pygame.USEREVENT + 1
scarecrow = None
REMOVE_SCARECROW = pygame.USEREVENT + 2
SCARECROW_COLOR = (255, 255, 0)


@dataclass
class Agent:
    x: int
    y: int
    radius: int
    speed: int
    color: tuple

    def is_collided_with(self, other):
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance < (self.radius + other.radius)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move_towards(self, target):
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.hypot(dx, dy)
        if distance > 3.0:
            # Allow three pixels of leeway to avoid jittering
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed


@dataclass
class Player(Agent):
    x: int = WIDTH // 2
    y: int = HEIGHT // 2
    radius: int = 20
    speed: int = 10
    color: tuple = (200, 200, 255)

    def teleport(self, pos):
        self.x, self.y = pos

    def is_caught_by_any_of(self, zombies):
        for zombie in zombies:
            if self.is_collided_with(zombie):
                return True
        return False


@dataclass
class Zombie(Agent):
    speed: int = 3
    radius: int = 20
    color: tuple = (80, 255, 0)


def draw_scene():
    global game_over
    if player.is_caught_by_any_of(zombies):
        if not game_over:
            game_over = True
            if game_over_sound:
                game_over_sound.play()
        font.render_to(screen, (220, 300), "GAME OVER! :(", (255, 0, 0))
        pygame.display.flip()
        return
    if player.is_caught_by_any_of(zombies):
        return
    player.move_towards(pygame.mouse.get_pos())
    if not frozen:
        for zombie in zombies:
            zombie.move_towards((player.x, player.y))
    screen.fill((GRASS_COLOR))
    if scarecrow is not None:
        pygame.draw.circle(screen, SCARECROW_COLOR, scarecrow, 20)
    player.draw()
    for zombie in zombies:
        if not frozen:
            target = scarecrow or (player.x, player.y)
            zombie.move_towards(target)
        zombie.draw()
    pygame.display.flip()


player = Player()
zombies = [
    Zombie(x=20, y=20, speed=2, radius=10),
    Zombie(x=WIDTH-20, y=20, radius=40),
    Zombie(x=20, y=HEIGHT-20, speed=2.5, radius=23),
    Zombie(x=WIDTH-20, y=HEIGHT-20, speed=3.2, radius=18),
    Zombie(x=40, y=40, speed=1.5),
    Zombie(x=WIDTH-40, y=40, speed=3.5, radius=45),
    Zombie(x=40, y=HEIGHT-40, speed=2.3, radius=50),
    Zombie(x=WIDTH-40, y=HEIGHT-40, speed=1, radius=15)]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                player.teleport(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if not frozen:
                    frozen = True
                    pygame.time.set_timer(UNFREEZE, 5000, loops=1)
            elif event.key == pygame.K_s:
                if scarecrow is None:
                    scarecrow = (player.x, player.y)
                    pygame.time.set_timer(REMOVE_SCARECROW, 5000, loops=1)
        elif event.type == UNFREEZE:
            frozen = False
        elif event.type == REMOVE_SCARECROW:
            scarecrow = None

    clock.tick(60)
    draw_scene()
