import pygame
window = pygame.display.set_mode((600, 600))
class Ball:
    def __init__(self, r, x, y, vx, vy, m):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.m = m
    def draw(self):
        pygame.draw.circle(window, (0, 0, 0), (self.x, self.y), self.r, 0)
    def update(self):
        # TODO, put math code to get new position here
        pass

active = True
clock = pygame.time.Clock()
fps = 60

# objs = [Ball(parameters), Ball(parameters), ...]
while active:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             active = False
    window.fill((255, 255, 255))
    for obj in objs:
        obj.draw()
        obj.update()
    pygame.display.update()