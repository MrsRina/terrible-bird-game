import pygame, math

def linear_interpolation(a, b, dt):
    if (dt == 0):
        return a

    return a + (b - a) * dt

def rect_collide_with(r1, r2):
    return r1[0] < r2[0] + r2[2] and r1[0] + r1[2] > r2[0] and \
           r1[1] < r2[1] + r2[3] and r1[1] + r1[3] > r2[1]

class Timing:
    def __init__(self):
        self.elapsed_ticks = 0
        self.current_ticks = 0
        self.ticks_going_on = 0
    
    def reach(self, ms):
        self.ticks_going_on = pygame.time.get_ticks()
        self.current_ticks = self.ticks_going_on - self.elapsed_ticks

        return self.current_ticks > ms
    
    def reset(self):
        self.elapsed_ticks = self.ticks_going_on
