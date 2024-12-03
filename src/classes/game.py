import pygame 
from src.settings import * 
from src.classes.phase import Phase, PhaseManager
from src.classes.menu import Menu
from src.classes.background import Interface
import os
import numpy as np

class Game:
    """
    The main class representing the game.

    Attributes
    ----------
    bg_music : pygame.mixer.Sound
        The background music for the game.

    screen : pygame.Surface
        The main game window.

    clock : pygame.time.Clock
        A clock to control the game's frame rate.

    running : bool
        Flag indicating whether the game is currently running.

    Methods
    -------
    __init__()
        Initializes the game, including pygame and the game window.

    new()
        Initializes a new game, creating a new level and menu.

    run()
        Runs the main game loop, handling events and updating the game state.
    """
    def __init__(self) -> None:
        """
        Initializes the game

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        
        # Initialize pygame and create window
        pygame.init()
        pygame.mixer.init()


        # Create the screen and clock
        self.screen = pygame.display.set_mode((SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[0]))
        self.clock = pygame.time.Clock()
        

        # Game loop control
        self.running = True
        
        self.movement =  np.zeros(2)
        self.attack = np.zeros(2)

    def new(self):
        """
        Initializes a new game by creating a new level and menu.
        
        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        # Create a new level and menu
        self.level = PhaseManager(self.screen)
        self.menu = Menu(self.level)

        

    def run(self):
        """
        Runs the main game loop, handling events and updating the game state.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        # Game loop
        try:
            self.new()

            while self.running:

                self.movement = np.zeros(2)
                self.attack = np.zeros(2)
                self.clock.tick(FRAME_RATE)
                
                for event in pygame.event.get():
                    
                    if event.type == pygame.QUIT:
                            self.running = False

                    if event.type == pygame.KEYDOWN:
                       
                        # Tela cheia e sair de tela cheia
                        if event.key == pygame.K_F11:
                            
                            pygame.display.toggle_fullscreen()
                        if event.key == pg.K_ESCAPE:
                            pg.quit()
                            exit() 
                        if event.key == pygame.K_p:
                            self.menu.current_screen = "pause"
                            self.menu.pause()




                    # Pause the game
                    # if event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_ESCAPE:  # 'ESC' key to pause the game
                    #         self.menu.current_screen = "pause"
                    #         self.menu.pause()

                # print("SAIU DO FOR")
                if self.menu.current_screen == "main_menu":
                    self.menu.main_menu()
                    
                if self.menu.current_screen == "start":
                    self.menu.stop_music()
                    self.level.start_phase()
                    self.menu.current_screen = "play" 
             
                if self.menu.current_screen == "play":
                    
                    if pygame.key.get_pressed()[WASD_Keys.LEFT.value]:
                        self.movement[0] -= 1
                    if pygame.key.get_pressed()[WASD_Keys.RIGHT.value]:
                        self.movement[0] += 1
                    if pygame.key.get_pressed()[WASD_Keys.TOP.value]:
                        self.movement[1] -= 1
                    if pygame.key.get_pressed()[WASD_Keys.DOWN.value]:
                        self.movement[1] += 1
            
                    if pygame.key.get_pressed()[pygame.K_LEFT]:
                            
                        self.attack[0] -= 1
                    if pygame.key.get_pressed()[pygame.K_RIGHT]:
                        self.attack[0] += 1
                    if pygame.key.get_pressed()[pygame.K_UP]:
                        self.attack[1] -= 1
                    if pygame.key.get_pressed()[pygame.K_DOWN]:
                        self.attack[1] += 1
                    
                    self.level.update(self.movement, self.attack)
                    pygame.display.flip()
                    

                    if self.level.current_dialogue != None:
                        self.menu.dialogue()
                
                if self.level._current_phase.check_lost():
                    self.menu.current_screen = "game_over"
                    self.menu.selascou()

        
        # Handle errors
        
        except pygame.error as e:
            print(f"An error occurred during game execution: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during game execution: {e}")
        finally:
            pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()