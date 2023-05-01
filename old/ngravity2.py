import pygame
import random
from pygame.locals import *

EULER_STEP = 0.1
BIG_G = 6.674e0
PUSH_CONSTANT = 10
π = 3.1415926535
FPS = 120
STEPS_FRAME = 20

minX = 0
maxX = 1440
minY = 0
maxY = 720
mouse_X = 0
mouse_Y = 0

def sqrt(x):
    t1, t2 = 2.0, 1.0
    while abs(t2 - t1) > 0.0001:
        t1 = t2
        t2 -= 0.5*(t2*t2 - x) / t2
    return t2
def cos(x):
    running = 1.0
    total = 0.0
    for term in range(1,8):
        total += running
        running *= -x*x  / (2*term) / (2*term-1)
    return total
def sin(x):
    running = x
    total = 0.0
    for term in range(1,8):
        total += running
        running *= -x*x / (2*term) / (2*term+1)
    return total

class vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}, {self.y})"
    def __neg__(self):
        return vec(-self.x, -self.y)
    def __add__(s1, s2):
        return vec(s1.x + s2.x, s1.y + s2.y)
    def __sub__(s1, s2):
        return vec(s1.x - s2.x, s1.y - s2.y)
    def mag_square(self):
        return self.x*self.x + self.y*self.y
    def mag(self):
        return sqrt(self.x*self.x + self.y*self.y)

class object:
    color = (255, 255, 255)
    def __init__(self, pos, vel, mass, radius):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.r = radius

    def set_color(self, color):
        self.color = color

    def __repr__(self):
        return f"[position = {self.pos}]"

    def dense(self):
        return self.mass / (π*self.r*self.r)

    def check_border(self, boundary_values=None):
        if boundary_values is None:
            border_min_x = minX
            border_max_x = maxX
            border_min_y = minY
            border_max_y = maxY
        else:
            border_min_x, border_min_y, border_max_x, border_max_y = boundary_values

        if self.pos.x + self.r >= border_max_x or self.pos.x - self.r <= border_min_x:
            self.vel.x = -self.vel.x
        if self.pos.y + self.r >= border_max_y or self.pos.y - self.r <= border_min_y:
            self.vel.y = -self.vel.y

    def gravity_effect(self, other):
        dist = other.pos - self.pos
        force_mag = BIG_G * self.mass * other.mass / dist.mag_square()
        inv_dist_mag = 1 / dist.mag()
        return vec(force_mag * dist.x * inv_dist_mag,
                   force_mag * dist.y * inv_dist_mag)

    def collision_effect(self, other):
        delta = (self.pos - other.pos)
        if delta.mag_square() > (self.r+other.r) * (self.r+other.r):
            return vec(0.0, 0.0)
        dmag = delta.mag()
        divot = self.r + other.r - dmag
        density = PUSH_CONSTANT * (self.mass/(π*self.r*self.r) + other.mass/(π*other.r*other.r))
        halfchord = sqrt ( self.r*self.r - (dmag*dmag + self.r*self.r - other.r*other.r)**2 / (4*dmag*dmag) )
        multiplier = divot * halfchord * density / dmag
        return vec(delta.x * multiplier, delta.y * multiplier)
    
class Ball(object):
    def __init__(self, pos, vel, mass, radius, color):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.r = radius
        self.color = color
        self.dragging = False


class frame:
    def __init__(self, objects_list, time):
        self.obj = objects_list
        self.time = time

    def create_button(self, label, position, window, bgcolor=(200, 200, 200)):
        font = pygame.font.Font(None, 30)
        text = font.render(label, 1, (0, 0, 0))
        rect = pygame.Rect(position, (100, 40))
        pygame.draw.rect(window, bgcolor, rect)
        window.blit(text, rect.move(5, 5))  # Add shading
        return rect

    def draw_menu(self, window):
        pygame.draw.rect(window, (200, 200, 200), (0, 0, maxX, 50))
        add_ball_rect = self.create_button("Add Ball", (20, 10), window)
        change_bound_rect = self.create_button("Change Bound", (140, 10), window)
        pause_rect = self.create_button("Pause", (340, 10), window)

    def draw_pause_icon(self, window, size=40):
        padding = 20
        bar_width = size // 4
        bar_height = size
        bar_gap = bar_width // 2
        xpos = maxX - padding - (bar_width * 2 + bar_gap)
        ypos = maxY - padding - bar_height

        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(xpos, ypos, bar_width, bar_height))
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(xpos + bar_width + bar_gap, ypos, bar_width, bar_height))

    def display(self):
        def add_ball():
            radius = 20
            center_x, center_y = maxX // 2, (maxY + 50) // 2
            for offset in range(0, max(maxX, maxY), 5):
                for angle in range(0, 360, 5):
                    dx = int(offset * cos(angle))
                    dy = int(offset * sin(angle))
                    new_pos = vec(center_x + dx, center_y + dy)
                    is_free = True
                    for existing_ball in self.obj:
                        if (existing_ball.pos - new_pos).mag() <= radius + existing_ball.r:
                            is_free = False
                            break
                    if is_free:
                        return Ball(new_pos, vec(0, 0), 20, 20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            return None

        pygame.init()

        active = True
        clock = pygame.time.Clock()
        window = pygame.display.set_mode((maxX, maxY))
        font = pygame.font.Font(None, 25)

        moving_ball = None
        add_ball_mode = False
        change_boundary_mode = False
        boundary_values = (minX, minY + 50, maxX, maxY)

        paused = False

        while active:
            mouse_X, mouse_Y = pygame.mouse.get_pos()
            key = pygame.key.get_pressed()

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                if event.type == MOUSEBUTTONDOWN:
                    if 20 <= mouse_X <= 120 and 10 <= mouse_Y <= 50:
                        add_ball_mode = not add_ball_mode
                    
                    if 140 <= mouse_X <= 240 and 10 <= mouse_Y <= 50:
                        change_boundary_mode = not change_boundary_mode
                        
                        if not change_boundary_mode:
                            boundary_values = (minX, minY + 50, maxX, maxY)  # Update this line
                        else:
                            reduced_bound = 0.15
                            boundary_values = (minX * reduced_bound,
                                            minY * reduced_bound + 50,  # Update this line
                                            maxX * (1 - reduced_bound / 2),
                                            maxY * (1 - reduced_bound / 2))
                        for obj in self.obj:
                            obj.pos.x = max(min(obj.pos.x, boundary_values[2] - obj.r), boundary_values[0] + obj.r)
                            obj.pos.y = max(min(obj.pos.y, boundary_values[3] - obj.r), boundary_values[1] + obj.r)

                    if 340 <= mouse_X <= 440 and 10 <= mouse_Y <= 50:
                        paused = not paused
                    if not add_ball_mode:
                        for obj in self.obj:
                            if (obj.pos.x - mouse_X) ** 2 + (obj.pos.y - mouse_Y) ** 2 <= obj.r ** 2:
                                moving_ball = obj
                                break
                    else:
                        new_ball = add_ball()
                        if new_ball:
                            self.obj.append(new_ball)

                if event.type == MOUSEBUTTONUP:
                    moving_ball = None
            

            # Update moving_ball's position upon dragging
            if moving_ball:
                moving_ball.pos.x = mouse_X
                moving_ball.pos.y = mouse_Y
                moving_ball.vel.x = 0
                moving_ball.vel.y = 0
                moving_ball.dragging = True
                
            else:
                ball_dragging = False
                for obj in self.obj:
                    obj.dragging = False

            window.fill((0, 0, 0))
            if change_boundary_mode:
                pygame.draw.rect(window, (255, 255, 0), boundary_values, 2)

            self.draw_menu(window)

            for obj in self.obj:
                obj.check_border(boundary_values)
                pygame.draw.circle(window, obj.color, (int(obj.pos.x), int(obj.pos.y)), obj.r, 0)

            if paused:  # Add this block
                self.draw_pause_icon(window)

            pygame.display.flip()

            if not paused:
                for iteration in range(STEPS_FRAME):
                    self = self.advance()


    def total_momentum(self):
        total = vec(0.0, 0.0)
        for entity in self.obj:
            total += vec(entity.mass*entity.vel.x, entity.mass*entity.vel.y)
        return total

    def total_energy(self):
        total = 0.0
        for ent1 in self.obj:
            for ent2 in self.obj:
                if ent1.pos == ent2.pos:
                    continue
                dist = ent2.pos - ent1.pos
                total -= 0.5 * ent1.mass * ent2.mass * BIG_G / dist.mag()
            total += 0.5 * ent1.mass * ent1.vel.mag_square()
        return total

    def advance(self):
        new_obj = []
        for ent1 in self.obj:
            if ent1.dragging:
                new_obj.append(ent1)
                continue
            netforce = vec(0.0,0.0)
            for ent2 in self.obj:
                if ent2.pos == ent1.pos:
                    continue
                netforce += ent1.collision_effect(ent2)
                netforce += ent1.gravity_effect(ent2)
            vel = vec(
                ent1.vel.x + netforce.x / ent1.mass * EULER_STEP,
                ent1.vel.y + netforce.y / ent1.mass * EULER_STEP
            )
            pos = vec(
                ent1.pos.x + vel.x * EULER_STEP,
                ent1.pos.y + vel.y * EULER_STEP
            )
            new_obj.append(Ball(pos, vel, ent1.mass, ent1.r, ent1.color))
        return frame(new_obj, self.time + EULER_STEP)


setframe = frame(
    [
        Ball(vec(100, 100), vec(0.2, 0), 20, 20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
        Ball(vec(500, 400), vec(-0.2, 0), 20, 20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
        Ball(vec(200, 500), vec(0.3, 0), 20, 20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
        Ball(vec(1100, 200), vec(0, 0.1), 20, 20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
        Ball(vec(900, 200), vec(0, -0.1), 20, 20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
    ],
    0
)

setframe.display()
