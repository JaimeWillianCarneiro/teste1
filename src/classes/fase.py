import pygame as pg
from src.settings import SCREEN_DIMENSIONS, GAME_TITLE
import random

class GameObject(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.life = 3
        self.x_position = x
        self.y_position = y
        self.width = width
        self.height = height
        self.image = pg.image.load('shaggy_right_1.png')
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.x_position, self.y_position
    
    def set_position(self, movement):
        self.x_position -= movement['x_moved']
        self.y_position -= movement['y_moved']
        self.rect.center = self.x_position, self.y_position
    
    def update(self, movement):
        self.setPosition(movement)




class Event(pg.sprite.Sprite):
    def __init__(self, player, start_zone, event_zone, end_zone, is_obrigatory, time):
        super().__init__()
        self.in_execution = False
        self.player = player
        self.start_zone = pg.Rect(*start_zone)
        self.event_zone = pg.Rect(*event_zone)
        self.end_zone = pg.Rect(*end_zone)
        self.is_obrigatory = is_obrigatory
        self.time = time
        self.rect = self.start_zone
        
    def can_start():
        pass
    
    def check_lost():
        pass
    
    def update():
        pass
        
        


class Fase:
    def __init__(self, screen, background, npcs, game_objects, mandatory_events, optional_events):
        self.screen = screen
        self.background = background
        self.fase_elements = pg.sprite.Group()
        
        # Monstro, protagonista e scooby snacks fictios #
        x = random.choice(range(SCREEN_DIMENSIONS[0]))
        y = random.choice(range(SCREEN_DIMENSIONS[1]))
        width = 100
        height = 150
        self.player = GameObject(SCREEN_DIMENSIONS[0]//2, SCREEN_DIMENSIONS[1]//2, width, height)
        self.monster = GameObject(x,y, width, height)
        self.scooby_snacks = GameObject(y, x, 50, 50)
        self.fase_elements.add(self.monster)
        self.fase_elements.add(self.scooby_snacks)
        #################################################
        
        self.npcs = pg.sprite.Group()
        for npc in npcs:
            self.npcs.add(npc)
            self.fase_elements.add(npc)
        
        self.game_objects = pg.sprite.Group()
        for game_object in game_objects:
            self.game_objects.add(game_object)
            self.fase_elements.add(game_object)
        
        self.mandatory_events = pg.sprite.Group()
        for mandatory_event in mandatory_events:
            self.mandatory_events.add(mandatory_event)
            self.fase_elements.add(mandatory_event)
        
        self.optional_events = pg.sprite.Group()
        for optional_event in optional_events:
            self.optional_events.add(optional_event)
            self.fase_elements.add(optional_event)


    def render_camera(self):
        """ Avalia quais elementos do jogo estão no campo de visão do protagonista para serem renderizados """
        objects_to_render = pg.sprite.spritecollide(self.background, self.fase_elements, False)
        to_render = pg.sprite.Group()
        to_render.add(self.player)
        for sprite in objects_to_render:
            to_render.add(sprite)
        
        to_render.draw(self.screen)
         
    
    def check_end(self):
        """  Verifica se o player passou pela fase (chama a próxima fase e encerra a atual) """
        if pg.sprite.collide_rect(self.player, self.scooby_snacks):
            return True
        return False
    
    def check_lost(self):
        """ Verifica se o player falhou (seja por tempo, seja por vida, seja por falha em algum evento da fase, etc) """
        if self.player.life <= 0:
            return True
        return False
            
    
    def update(self, movement):
        self.screen.fill((0, 0, 0))
        pg.draw.rect(self.screen, (255,255,255), self.background)
                    
        # Caso o player tenha passado de fase, encerra-a e inicia a proxima
        if self.check_end():
            # Exemplo de nova fase: ###############################
            game_objects = []
            npcs = []
            for i in range(3):
                x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
                y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
                width = 23
                height = 40
                game_objects.append(GameObject(x,y, width, height))

                x = random.choice(range(SCREEN_DIMENSIONS[0]))
                y = random.choice(range(SCREEN_DIMENSIONS[1]))
                width = 67
                height = 100
                npcs.append(GameObject(x,y, width, height))
            ##################################################
            
            return Fase(self.screen, self.background, npcs, game_objects, [], [])
            
            
        # Verifica se o player continua no jogo
        if not self.check_lost():
            # Atualiza as variaveis da fase que estao no campo de visao do personagem
            self.fase_elements.update(movement)
                
            self.player.life -= 0.01
        
        self.render_camera()
            
            
        return self