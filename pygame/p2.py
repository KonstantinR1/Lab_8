import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Drawing tools
LINE = 'line'
RECTANGLE = 'rectangle'
CIRCLE = 'circle'
ERASER = 'eraser'

# Initial values
radius = 10
color = BLACK
drawing_tool = LINE
drawing = False
points = []

# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Drawing")
clock = pygame.time.Clock()

def draw_shapes(surface, points, radius, drawing_tool, color):
    for i in range(len(points) - 1):
        start = points[i][:2]  # Extract x, y from the point
        end = points[i + 1][:2]  # Extract x, y from the point

        if points[i][2] == RECTANGLE:
            pygame.draw.rect(surface, color, (start[0], start[1], end[0] - start[0], end[1] - start[1]))
        elif points[i][2] == CIRCLE:
            distance = pygame.math.Vector2(end[0] - start[0], end[1] - start[1]).length()
            pygame.draw.circle(surface, color, (start[0], start[1]), int(distance))
        elif points[i][2] == ERASER:
            erase_shape(surface, end[0], end[1], radius)
        else:
            pygame.draw.line(surface, color, start, end, radius * 2)

def erase_shape(surface, x, y, radius):
    pygame.draw.circle(surface, WHITE, (x, y), radius)

def handle_key_events():
    global drawing_tool, color

    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        drawing_tool = RECTANGLE
    elif keys[pygame.K_c]:
        drawing_tool = CIRCLE
    elif keys[pygame.K_e]:
        drawing_tool = ERASER
    elif keys[pygame.K_s]:
        color = cycle_colors(color)

def cycle_colors(current_color):
    colors = [WHITE, RED, GREEN, BLUE]
    index = colors.index(current_color)
    next_index = (index + 1) % len(colors)
    return colors[next_index]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                points.append((event.pos[0], event.pos[1], drawing_tool))
                drawing = True
            elif event.button == 3:
                points.append((event.pos[0], event.pos[1], ERASER))
                drawing = True
        elif event.type == pygame.MOUSEMOTION and drawing:
            points.append((event.pos[0], event.pos[1], drawing_tool))
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False

    handle_key_events()

    screen.fill(BLACK)
    draw_shapes(screen, points, radius, drawing_tool, color)
    pygame.display.flip()
    clock.tick(FPS)
