import math
from dataclasses import dataclass
import pygame
import os
from pygame import freetype

WIDTH, HEIGHT = 1024, 600
SKY_COLOR = (135, 240, 255)
SNOW_COLOR = (242, 242, 242)
SNOW_HEIGHT = 100
SNOW_TOP = HEIGHT - SNOW_HEIGHT
SNOW_RECTANGLE = (0, SNOW_TOP, WIDTH, SNOW_HEIGHT)
GROUND_LEVEL = HEIGHT - (SNOW_HEIGHT // 2)
TREE_SPACING = 173
MAX_PLANE_SPEED = 25
CRUISING_ALTITUDE = 50
RUNWAY_COLOR = (60, 60, 60)
RUNWAY_Y = GROUND_LEVEL + 10
RUNWAY_LINES = (255, 255, 0)
SPEED_TEXT_COLOR = (255, 255, 255)
BAR_COLOR = (255, 0, 0)
EXTRA_TEXT_COLOR = (255, 0, 0)
PLANE_COLOR = (0, 0, 0)
PLANE_CRASHED_COLOR = (255, 0, 0)
DEFAULT_TEXT_COLOR = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Landing")
clock = pygame.time.Clock()
font = freetype.SysFont(None, 24)
big_font = freetype.SysFont(None, 48)
game_over = False

try:
    space_background = pygame.image.load("space_background.jpg")
    space_background = pygame.transform.scale(
        space_background, (WIDTH, HEIGHT))
except Exception:
    space_background = None

try:
    pygame.mixer.init()
    try:
        game_over_sound = pygame.mixer.Sound("game_over.wav")
    except pygame.error:
        game_over_sound = None
except pygame.error:
    game_over_sound = None


@dataclass
class Plane:
    x: int
    y: int
    state: str = "flying"
    speed: int = MAX_PLANE_SPEED
    rotation: int = 0
    color: tuple = (PLANE_COLOR)

    def draw(self):
        base_coords = [
            (-16, 0), (-13, 2), (-15, 7), (-12, 7), (-8, 2), (-1, 2),
            (-6, 6), (-5, 6), (8, 2), (16, 2), (19, -2), (8, -2),
            (-5, -8), (-6, -8), (-1, -2), (-13, -2)]
        rotated = base_coords if self.rotation == 0 else [
            (x * math.cos(self.rotation) - y * math.sin(self.rotation),
             x * math.sin(self.rotation) + y * math.cos(self.rotation))
            for x, y in base_coords]
        coords = [(WIDTH//2 + 4*x, self.y - 4*y) for x, y in rotated]
        pygame.draw.polygon(screen, self.color, coords)

    # The states are:
    #
    # "flying"     : the plane is in the air at the cruising altitude,
    #                moving forward. The user can press the down arrow
    #                key to start descending.
    # "descending" : the plane is descending towards the ground, facing
    #                downwards. The user can press the up arrow key to
    #                raise the nose and start landing. If they raise the
    #                nose too early, the plane will start rising again.
    #                If they raise the nose too late, the plane will
    #                crash. Raising it just right will put the plane
    #                in the "landing" state.
    # "landing"    : the plane has just brought the nose up, right above
    #                the ground, and is still going down. When it hits
    #                the ground, it will be in the "touching" state.
    # "touching"   : the plane has just touched the ground, and is
    #                still moving forward with the nose up. The user
    #                can press the down arrow key to lower the nose,
    #                but it will still be moving forward fast.
    # "down"       : the user has just lowered the nose so all wheels
    #                are on the ground and the plane is moving
    #                forward. The user needs to press the Return key
    #                here to start braking.
    # "braking"    : the plane is on the ground, decelerating. When
    #                it comes to a stop, it will be in the "stopped"
    #                state.
    # "stopped"    : the plane has come to a stop on the ground.
    #                In the stopped state, the user can press the right
    #                arrow key to start the plane moving again.
    # "starting"   : the plane is starting to move on the ground, and
    #                the user can press the up arrow key to take off.
    # "rising"     : the plane is rising after touching down. It will
    #                keep rising until it reaches the cruising altitude
    #                in which case it will automatically level off and
    #                return to the "flying" state.
    # "crashed"    : the plane has crashed and is no longer moving.

    def move(self):
        if self.state != "stopped":
            self.x += self.speed % TREE_SPACING
        if self.state == "flying":
            pass
        elif self.state == "descending":
            self.y += self.speed * 0.1
            if self.y >= GROUND_LEVEL:
                self.state = "crashed"
                self.color = (PLANE_CRASHED_COLOR)  # red for crashed
                self.speed = 0
                self.y = GROUND_LEVEL
                try:
                    if game_over_sound:
                        game_over_sound.play()
                except NameError:
                    pass

        elif self.state == "landing":
            self.y += self.speed * 0.1
            if self.y >= GROUND_LEVEL:
                self.state = "touching"
                self.y = GROUND_LEVEL
        elif self.state == "touching":
            pass
        elif self.state == "down":
            pass
        elif self.state == "braking":
            self.speed -= 0.1
            if self.speed <= 0:
                self.speed = 0
                self.state = "stopped"
        elif self.state == "starting":
            self.y = GROUND_LEVEL
            self.speed += 0.1
            if self.speed >= MAX_PLANE_SPEED:
                self.speed = MAX_PLANE_SPEED
        elif self.state == "rising":
            self.y -= self.speed * 0.1
            if self.y <= CRUISING_ALTITUDE:
                self.y = CRUISING_ALTITUDE
                self.state = "flying"
                self.rotation = 0


plane = Plane(0, y=CRUISING_ALTITUDE)


def draw_runway(surface):
    # dark runway
    runway_width = WIDTH * 1.5
    left = (WIDTH - runway_width) // 2
    pygame.draw.rect(surface, RUNWAY_COLOR,
                     (left, RUNWAY_Y - 10, runway_width, 40))

    # dashed centre line
    dash_w = 30
    dash_gap = dash_w
    # offset dashes by plane.x so they scroll when plane.x changes
    offset = int(plane.x) % (dash_w + dash_gap)
    start_x = left + 10 - offset

    while start_x < left + runway_width - 10:
        pygame.draw.rect(surface, RUNWAY_LINES,
                         (start_x, RUNWAY_Y + 5, dash_w, 4))
        start_x += dash_w + dash_gap


def draw_tree(x, y):
    pygame.draw.rect(screen, (102, 51, 0), (x-5, y-20, 10, 20))
    pygame.draw.polygon(screen, (242, 242, 242), [
                        (x-30, y-20), (x+30, y-20), (x, y-300)])


def draw_speedometer(surface, speed, altitude):
    # draw a simple horizontal bar at top-left
    bar_w = 200
    bar_h = 18
    x, y = 10, 10
    pygame.draw.rect(surface, (50, 50, 50), (x-2, y-2, bar_w+4, bar_h+4))
    pygame.draw.rect(surface, (30, 30, 30), (x, y, bar_w, bar_h))
    # fill proportionally
    fill = int((speed / MAX_PLANE_SPEED) * bar_w)
    pygame.draw.rect(surface, (BAR_COLOR), (x, y, fill, bar_h))
    text_x = int(x)
    text_y = int(y + bar_h + 15)
    font.render_to(surface, (text_x, text_y),
                   f"Speed: {int(speed)}", (SPEED_TEXT_COLOR))
    # draw altitude below
    alt_text_y = text_y + 30
    font.render_to(surface, (text_x, alt_text_y),
                   f"Altitude: {int(altitude)}", (SPEED_TEXT_COLOR))


def draw_scene():
    global game_over

    top_right_line1 = "Use the W/S keys to move the plane."
    top_right_line2 = "Press enter to slow down on runway. D to start plane again."

    # if the plane has crashed show GAME OVER, play sound after
    if plane.state == "crashed":
        # draw background/ground/runway as usual so text overlays correctly
        if space_background:
            screen.blit(space_background, (0, 0))
        else:
            screen.fill(SKY_COLOR)
        pygame.draw.rect(screen, SNOW_COLOR, SNOW_RECTANGLE)
        draw_runway(screen)
        x = -plane.x
        while x < WIDTH:
            draw_tree(x, SNOW_TOP)
            x += TREE_SPACING
        plane.draw()

        # play sound once when crash first observed
        if not game_over:
            if game_over_sound:
                game_over_sound.play()
            game_over = True

        # draw GAME OVER (or PLANE CRASHED in this context) text centered
        text = "PLANE CRASHED :("
        tx = WIDTH // 2 - 200
        ty = HEIGHT // 2 - 40
        big_font.render_to(screen, (tx, ty), text, (EXTRA_TEXT_COLOR))
        # small instruction
        font.render_to(screen, (WIDTH // 2 - 140, ty + 80),
                       "Please close the game, NOW!", (EXTRA_TEXT_COLOR))
        pygame.display.flip()
        return

    # normal drawing when not crashed
    if plane.state != "stopped":
        if space_background:
            screen.blit(space_background, (0, 0))
        else:
            screen.fill(SKY_COLOR)
        pygame.draw.rect(screen, SNOW_COLOR, SNOW_RECTANGLE)
        draw_runway(screen)
        x = -plane.x
        while x < WIDTH:
            draw_tree(x, SNOW_TOP)
            x += TREE_SPACING
        plane.draw()
        # pass altitude (height above ground) to speedometer
        altitude = max(0, int(GROUND_LEVEL - plane.y))
        draw_speedometer(screen, plane.speed, altitude)

        # instructions being drawn ons creen
        margin = 5
        # measure text widths so we can right-align
        r1 = font.get_rect(top_right_line1)
        r2 = font.get_rect(top_right_line2)
        rx1 = WIDTH - r1.width - margin
        ry1 = margin
        rx2 = WIDTH - r2.width - margin
        ry2 = ry1 + r1.height + 4
        font.render_to(screen, (rx1, ry1), top_right_line1,
                       (DEFAULT_TEXT_COLOR))
        font.render_to(screen, (rx2, ry2), top_right_line2,
                       (DEFAULT_TEXT_COLOR))

        plane.move()
    clock.tick(60)
    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and plane.state == "flying":
                plane.rotation = -0.2
                plane.state = "descending"
            elif event.key == pygame.K_w and plane.state == "descending":
                plane.rotation = 0.2
                if plane.y < GROUND_LEVEL - 100:
                    plane.state = "rising"
                else:
                    plane.state = "landing"
            elif event.key == pygame.K_s and plane.state == "touching":
                plane.rotation = 0
                plane.state = "down"
            elif event.key == pygame.K_RETURN and plane.state == "down":
                plane.state = "braking"
            elif event.key == pygame.K_d and plane.state == "stopped":
                plane.state = "starting"
            elif event.key == pygame.K_w and plane.state == "starting" \
                    and plane.speed == MAX_PLANE_SPEED:
                plane.rotation = 0.1
                plane.state = "rising"
    draw_scene()
