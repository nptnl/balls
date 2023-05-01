# objects.py
from vec import vec, sqrt, sin, cos

π = 3.1415926535
BIG_G = 6.674e0
PUSH_CONSTANT = 10

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