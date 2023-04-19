import pygame
EULER_STEP = 0.1
BIG_G = 6.674e0
PUSH_CONSTANT = 10
π = 3.1415926535
FPS = 60
STEPS_FRAME = 20

minX = 0
maxX = 1200
minY = 0
maxY = 600

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
    def __init__(self, pos, vel, mass, radius):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.r = radius
    def __repr__(self):
        return f"[position = {self.pos}]"
    def dense(self):
        return self.mass / (π*self.r*self.r)
    def check_border(self):
        if self.pos.x + self.r >= maxX or self.pos.x - self.r <= minX:
            self.vel.x = -self.vel.x
        if self.pos.y + self.r >= maxY or self.pos.y - self.r <= minY:
            self.vel.y = -self.vel.y
    def gravity_affect(self, other):
        dist = other.pos - self.pos
        force_mag = BIG_G * self.mass * other.mass / dist.mag_square()
        inv_dist_mag = 1 / dist.mag()
        return vec(force_mag * dist.x * inv_dist_mag,
        force_mag * dist.y * inv_dist_mag)
    def collision_affect(self, other):
        delta = (self.pos - other.pos)
        if delta.mag_square() > (self.r+other.r) * (self.r+other.r):
            return vec(0.0, 0.0)
        dmag = delta.mag()
        divot = self.r + other.r - dmag
        density = PUSH_CONSTANT * (self.mass/(π*self.r*self.r) + other.mass/(π*other.r*other.r))
        halfchord = sqrt ( self.r*self.r - (dmag*dmag + self.r*self.r - other.r*other.r)**2 / (4*dmag*dmag) )
        multiplier = divot * halfchord * density / dmag
        return vec(delta.x * multiplier, delta.y * multiplier)
    
class frame:
    def __init__(self, objects_list, time):
        self.obj = objects_list
        self.time = time
    def display(self):
        active = True
        clock = pygame.time.Clock()
        window = pygame.display.set_mode((1200, 600))
        while active:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
            window.fill((60, 60, 60))
            for obj in self.obj:
                obj.check_border()
                pygame.draw.circle(window, (200, 200, 200), (obj.pos.x, obj.pos.y), obj.r, 0)
            pygame.display.update()
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
            netforce = vec(0.0,0.0)
            for ent2 in self.obj:
                if ent2.pos == ent1.pos:
                    continue
                netforce += ent1.collision_affect(ent2)
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
    [object(vec(100, 100), vec(0.2, 0), 20, 20),
    object(vec(500, 400), vec(-0.2, 0), 20, 20),
    object(vec(200, 500), vec(0.3, 0), 20, 20),
    object(vec(1100, 200), vec(0, 0.1), 20, 20),
    object(vec(900, 200), vec(0, -0.1), 20, 20)],
    0
)
setframe.display()
