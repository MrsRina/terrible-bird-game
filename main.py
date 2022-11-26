import pygame, utils, world

class app:
    def __init__(self, version):
        self.version = version
        self.delta_time = 16.0
        self.capped_fps = 60
        self.cpu_reduce_ticks_timing = utils.Timing()

        self.screen_width = 1280
        self.screen_height = 800
        self.rect_info = [0, 0, 200, 50]

        self.lodaded_entity_list = []
        self.loaded_collider_list = []
        self.player = world.Entity()
        self.player.name = "hi hi oi oi j"
        self.add_entity_to_world(self.player)
        self.camera = [0, 0]
        self.player.air_resistence = 2.0
        self.map = world.Map(self, "oi")
        self.loaded_collider_list.append(world.Collider())

        self.game_over = False
        self.game_paused = False
        self.game_afk = True
        self.game_started = False
        self.speed_boost_progress = 20
        self.gravity = 0.9 # there is no accurace here
        self.walls_elapsed = 0
        self.timing_jump = utils.Timing()

    def init(self):
        pygame.init()

        # DOUBLEBUF para ele dar swap duas vezes no buffer final (geralmente é 1).
        self.root = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.DOUBLEBUF) 
        pygame.display.set_caption("hi somegame :))")

    def add_entity_to_world(self, entity):
        self.lodaded_entity_list.append(entity)

    def mainloop(self):
        self.loop = 1
        self.player.attach_texture(pygame.image.load("bird.png").convert_alpha())

        interval_cpu_ticks = 1000 / self.capped_fps
        delta_time_clamped = interval_cpu_ticks / 100

        while (self.loop):
            # por que rodar além de 60 vezes?
            if (self.cpu_reduce_ticks_timing.reach(interval_cpu_ticks)):
                self.cpu_reduce_ticks_timing.reset()

                self.delta_time = self.cpu_reduce_ticks_timing.current_ticks / 100
                self.delta_time = delta_time_clamped if self.delta_time > delta_time_clamped else self.delta_time
                self.root.fill((0, 0, 0))

                self.on_event()
                self.on_update()
                self.on_render()
    
                pygame.display.flip()

    def shutdown(self):
        pygame.quit()
    
    def on_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = 0

            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                self.game_started = True

    def on_update(self):
        if self.game_over:
            self.speed_boost_progress = 0
            self.player.jumped = 0

        self.spawn_objects()
        self.do_player_movements()
        self.map.on_update()

        # do update here
        for entities in self.lodaded_entity_list:
            entities.on_update(self.delta_time)
        
        # é um target, não interfere no player
        self.camera[0] = self.player.rect[0] - (self.screen_width / 2)
        # o eixo y é fixo
        # self.camera[1] = self.player.rect[1] - (self.screen_height / 2)

    def spawn_objects(self):
        pass

    def do_player_movements(self):
        self.player.acceleration[0] = self.speed_boost_progress
        self.player.acceleration[1] = self.gravity

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            if not self.player.jumped:
                self.timing_jump.reset()

            self.player.jump()
        
        if pressed_keys[pygame.K_LEFT]:
            self.speed_boost_progress -= 1
        elif pressed_keys[pygame.K_RIGHT]:
            self.speed_boost_progress += 1
        
        # A var jumped iria resetar se o player tocasse no chão (on ground)
        # mas não tem chão, então é preciso um timeout sincrono com os ticks
        # da cpu.
        if (self.player.jumped and self.timing_jump.reach(750)):
            self.player.jumped = 0

    def on_render(self):
        relative_camera = [0, 0, 0, 0]

        for entitites in self.lodaded_entity_list:
            relative_camera[0] = entitites.rect[0] - self.camera[0]
            relative_camera[1] = entitites.rect[1] - self.camera[1]
            relative_camera[2] = entitites.rect[2]
            relative_camera[3] = entitites.rect[3]

            if entitites.texture is not None:
                self.root.blit(entitites.texture, relative_camera)
            else:
                pygame.draw.rect(self.root, entitites.color, relative_camera)

        for objects in self.loaded_collider_list:
            relative_camera[0] = objects.draw_rect[0] - self.camera[0]
            relative_camera[1] = objects.draw_rect[1] - self.camera[1]
            relative_camera[2] = objects.draw_rect[2]
            relative_camera[3] = objects.draw_rect[3]

            pygame.draw.rect(self.root, objects.color, relative_camera)

        if self.game_afk:
            self.rect_info[0] = (self.screen_width / 2) - (self.rect_info[2] / 2)
            self.rect_info[1] = (self.screen_height / 2) + self.rect_info[3]

if 1:
    game = app("0.1.0")
    game.init()
    game.mainloop()
    game.shutdown()