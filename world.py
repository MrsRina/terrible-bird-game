import pygame, random, utils

class Entity:
    def __init__(self):
        self.name = "hi"
        self.collided = False
        self.rect = [20, 20, 60, 60]
        self.color = [255, 255, 255]
        self.motion = [0, 0]
        self.acceleration = [0, 0]
        self.on_ground = 0
        self.jumped = 0
        self.air_resistence = 3
        self.texture = None
    
    def jump(self):
        if (self.jumped):
            return

        self.motion[1] -= 4 * self.air_resistence # 4^2
        self.jumped = 1
    
    def attach_texture(self, texture):
        self.texture = pygame.transform.scale(texture, (self.rect[2], self.rect[3]));

    def on_update(self, dt):
        self.motion[0] += self.acceleration[0] * dt
        self.motion[1] += self.acceleration[1] * dt

        self.rect[0] += self.motion[0]
        self.rect[1] += self.motion[1]

        # isso é uma adição não realista do metodo euler, feito pro projeto,
        # com isso dá pra deixar mais smooth e menos estático.
        # ele segue a base do verlet (multiplica por dt^2)
        if (self.motion[1] > 0):
            self.motion[1] -= self.acceleration[1] * dt * dt
        elif (self.motion[1] < 0):
            self.motion[1] += self.acceleration[1] * dt * dt

        self.motion[0] = self.motion[0] * dt

class Collider:
    def __init__(self):
        self.collided = False
        self.color = [255, 0, 0]
        self.rect = [70, 70, 200, 200]
        self.draw_rect = [0, 0, 0, 0]
    
    def on_render(self, dt):
        self.draw_rect[0] = self.rect[0]
        self.draw_rect[1] = utils.linear_interpolation(self.draw_rect[1], self.rect[1], dt)
        self.draw_rect[2] = self.rect[2]
        self.draw_rect[3] = utils.linear_interpolation(self.draw_rect[3], self.rect[3], dt)

class Map:
    def __init__(self, game, tag):
        self.tag = tag
        self.loaded_map_list = []
        self.game = game
        self.last_check_x = -(self.game.screen_width / 2)
        self.create_platform = 0
        random.seed(666)
    
    def on_update(self):
        if not self.game.game_started:
            return
        
        diff = self.game.player.rect[0] - self.last_check_x
        dist = self.game.screen_width / 2

        if diff > dist:
            self.last_check_x += diff
            self.create_platform = 1

        if self.create_platform:
            r1 = self.game.screen_height * random.random()
            r2 = self.game.screen_height * random.random()

            for side in range(0, 2):
                collider = Collider()
                collider.rect[0] = self.last_check_x + dist
                collider.rect[2] = dist / 6
                collider.color[0] = random.random() * 255
                collider.color[1] = random.random() * 255
                collider.color[2] = random.random() * 255

                if side == 0:
                    collider.rect[1] = 0
                    collider.rect[3] = r1 / (2)
                else:
                    collider.rect[3] = r2 / (2 + (1 * random.random()))
                    collider.rect[1] = self.game.screen_height - collider.rect[3]
                
                self.loaded_map_list.append(collider)
                self.game.loaded_collider_list.append(collider)
                self.game.speed_boost_progress += 1

            self.create_platform = 0

        poll = None

        for colliders in self.loaded_map_list:
            colliders.on_render(self.game.delta_time + (self.game.speed_boost_progress / 1000));

            if (poll == None and colliders.rect[0] + colliders.rect[2] < self.game.camera[0] - diff):
                poll = colliders
            
            if utils.rect_collide_with(colliders.rect, self.game.player.rect):
                self.game.game_over = True
        
        if poll is not None:
            self.game.loaded_collider_list.remove(poll)
            self.loaded_map_list.remove(poll)