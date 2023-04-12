import pygame
EULER_STEP = 1.0
BIG_G = 6.674e-1
FPS = 60

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
def sqrt(x):
    t1, t2 = 2.0, 1.0
    while abs(t2 - t1) > 0.0001:
        t1 = t2
        t2 -= 0.5*(t2*t2 - x) / t2
    return t2
class object:
    def __init__(self, pos, vel, mass, radius):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.r = radius
    def __repr__(self):
        return f"[position = {self.pos}]"
    def gravity_affect(self, other):
        dist = other.pos - self.pos
        force_mag = BIG_G * self.mass * other.mass / dist.mag_square()
        inv_dist_mag = 1 / sqrt(dist.mag_square())
        return vec(force_mag * dist.x * inv_dist_mag,
        force_mag * dist.y * inv_dist_mag)
class frame:
    def __init__(self, objects_list, time):
        self.obj = objects_list
        self.time = time
    def display(self):
        active = True
        clock = pygame.time.Clock()
        window = pygame.display.set_mode((600, 600))
        while active:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
            window.fill((255, 255, 255))
            for obj in self.obj:
                pygame.draw.circle(window, (0, 0, 0), (obj.pos.x, obj.pos.y), obj.r, 0)
            pygame.display.update()
            self.advance()
    def advance(self):
        new_obj = []
        for ent1 in self.obj:
            netforce = vec(0.0,0.0)
            for ent2 in self.obj:
                if ent2.pos == ent1.pos:
                    continue
                netforce += ent1.gravity_affect(ent2)
            vel = vec(
                ent1.vel.x + netforce.x / ent1.mass * EULER_STEP,
                ent1.vel.y + netforce.y / ent1.mass * EULER_STEP
            )
            pos = vec(
                ent1.pos.x + vel.x * EULER_STEP,
                ent1.pos.y + vel.y * EULER_STEP
            )
            new_obj.append(object(pos, vel, ent1.mass))
        return frame(new_obj, self.time + EULER_STEP)

# frames are a list of objects and a time float
# use this template
setframe = frame(
#              position        velocity   mass
    [object(vec(-1.0,-1.0), vec(0.0,0.0), 1.0, 10),
    object(vec(-1.0,-1.0), vec(0.0,0.0), 1.0, 10)],
    0.0
)

# use frame.advance() to go to the next frame
# this is according to the EULER_STEP and BIG_G constants at the top  
setframe.display()