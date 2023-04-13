import pygame
EULER_STEP = 1
BIG_G = 6.674e-1 * 3
π = 3.1415926535
FPS = 60

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
            window.fill((60, 60, 60))
            for obj in self.obj:
                # get this to draw polar graphs :)
                pygame.draw.circle(window, (200, 200, 200), (obj.pos.x, obj.pos.y), obj.r, 0)
            pygame.display.update()
            iterations = 0
            while iterations <= 4: # change for multiple steps per frame
                self = self.advance()
                iterations += 1
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
            new_obj.append(object(pos, vel, ent1.mass, ent1.r))
        return frame(new_obj, self.time + EULER_STEP)

setframe = frame(
    [object(vec(300, 200), vec(0.2, 0), 80.0, 20),
    object(vec(100, 300), vec(0.5, 0), 40.0, 20),
    object(vec(300, 500), vec(-0.2,0), 50.0, 20)],
    0.0
)
# setframe.display()

# r = self.r - k*cos(t - a) = self.r - k*(cos(t)*cos(a) - sin(t)*sin(a))
# k = self.r * (self.r + other.r) / dist.mag
# F = m * v * self.r / (self.r - k)
# cos(a) = dist.x / dist.mag, sin(a) = dist.y / dist.mag