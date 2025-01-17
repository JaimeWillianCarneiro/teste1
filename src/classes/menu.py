"""
This module contains the class that abstrain a menu. This class have a lot of
utility functions to handle buttons and their events.
"""
from settings import  SCREEN_DIMENSIONS, START_SOUND_MENU, START_BACKGROUND_MENU, START_COLUMNS_MENU, START_ROWS_MENU, FINAL_SOUND_MENU, FINAL_SCREEN_MENU, FINAL_ROWS_MENU, FINAL_COLUMNS_MENU
from classes.background import Background
import pygame
import sys
import json


screen = pygame.display.set_mode((0,0))

def get_font(size):
    """
    Get a Pygame font object with a specified size.

    Parameters
    ----------
    size : int
        The font size.

    Returns
    -------
    pygame.font.Font
        A Pygame font object.
    """

    return pygame.font.Font(r"assets/font.ttf", size)


class Button:
    """
    Represents a clickable button in the game.

    Attributes
    ----------
    image : pygame.Surface
        The image representing the button.

    x_pos : int
        The x-coordinate of the button's center.

    y_pos : int
        The y-coordinate of the button's center.

    font : pygame.font.Font
        The font used for rendering text on the button.

    base_color : str
        The base color of the button's text.

    hovering_color : str
        The color of the button's text when hovering.

    text_input : str
        The text displayed on the button.

    text : pygame.Surface
        The rendered text surface.

    rect : pygame.Rect
        The rectangular area of the button.

    text_rect : pygame.Rect
        The rectangular area of the rendered text.

    Methods
    -------
    update(screen)
        Updates and renders the button on the given screen.

    check_for_input(position)
        Checks if a given position is within the button's area.

    change_color(position)
        Changes the color of the button's text based on the mouse position.
    """

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
        Initializes the Button instance.

        Parameters
        ----------
        image : pygame.Surface
            The image representing the button.

        pos : tuple
            The x, y coordinates of the button's center.

        text_input : str
            The text displayed on the button.

        font : pygame.font.Font
            The font used for rendering text on the button.

        base_color : str
            The base color of the button's text.

        hovering_color : str
            The color of the button's text when hovering.

        Returns
        -------
        None.
        """ 
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Updates and renders the button on the given screen.

        Parameters
        ----------
        screen : pygame.Surface
            The screen where the button will be rendered.

        Returns
        -------
        None.
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        """
        Checks if a given position is within the button's area.

        Parameters
        ----------
        position : tuple
            The x, y coordinates of the position to check.

        Returns
        -------
        bool
            True if the position is within the button's area, False otherwise.
        """

        return self.rect.collidepoint(position)

    def change_color(self, position):
        """
        Changes the color of the button's text based on the mouse position.

        Parameters
        ----------
        position : tuple
            The x, y coordinates of the mouse position.

        Returns
        -------
        None.
        """

        if self.check_for_input(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)



class Menu:
    """
        Represents the menu system in the game.

        Attributes
        ----------
        current_screen : str
            The current active screen.

        level : Level
            The instance of the game level associated with the menu.

        Methods
        -------
        main_menu(background_image_path)
            Displays the main menu screen with buttons for play, credits, and quit.

        credits()
            Displays the credits screen with information about the game developers.

        pause()
            Displays the pause screen with options to resume, go to the main menu, or quit the game.

        game_over()
            Displays the game over screen with the option to return to the main menu.
    """
    def __init__(self, level)-> None:
        """
        Initializes the Menu instance.

        Parameters
        ----------
        level : PhaseManager
            The instance of the game PhaseManager associated with the menu.

        Returns
        -------
        None.
        """
        
        self.clock = pygame.time.Clock()
        
        # Configurações do mixer (áudio)
        pygame.mixer.init()

        self.current_screen = "main_menu"
        self.level= level
        self.first_dialogue = False
        
        self.typing = pygame.mixer.Sound('assets\sounds\som_dialogo.wav')
        self.fgv = pygame.mixer.Sound('assets\sounds\\frente_fgv.mp3')
        self.laboratorio = pygame.mixer.Sound('assets\sounds\laboratorio.wav')
        self.botao_3 = pygame.mixer.Sound('assets\sounds\\botao_cena3.mp3')
        self.start_botao =  pygame.mixer.Sound('assets\sounds\\start.mp3')
        
    def load_audio(self, audio_path):
        """
        Load and play the background audio.
         
        Returns
        -------
        None
        """
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.set_volume(0.5)  # Ajustar o volume
            pygame.mixer.music.play(-1)  # Reproduzir em loop
        except pygame.error as e:
            print(f"Erro ao carregar o áudio: {e}")

    def play_music(self, x = -1):
        pygame.mixer.music.play(x)
    
    def stop_music(self):
        pygame.mixer.music.stop()
    
    def extract_frames(self) -> list:
        """
        Extract the frames from the sprite sheet and resize them for the screen.
         
        Returns
        -------
        list
            A lista with all the frames of the video
        """
        frames = []
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.sprite_sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                frame = pygame.transform.scale(frame, (self.screen_width, self.screen_height))
                frames.append(frame)
        return frames
    
    def main_menu(self):  
        """
        Displays the inicial screen of the game, with the option to press enter to start it.

        Returns
        -------
        None.
        """
        running = True

        #  Configurações de tela
        self.screen_width = SCREEN_DIMENSIONS[0]
        self.screen_height = SCREEN_DIMENSIONS[1]

        self.load_audio(START_SOUND_MENU)
        
        # Configurações dos frames
        self.columns = START_COLUMNS_MENU
        self.rows = START_ROWS_MENU
        
        #  Carregar  a imagem com os frames
        self.sprite_sheet = pygame.image.load(START_BACKGROUND_MENU).convert_alpha()
        self.dimensions = (self.sprite_sheet.get_width(), self.sprite_sheet.get_height())
        self.frame_width = self.dimensions[0] // self.columns
        self.frame_height = self.dimensions[1] // self.rows
        
        # Extrair frames da sprite sheet
        self.frames = self.extract_frames()
        
        #  Controle da animação
        self.current_frame = 0
        self.frame_delay = 100  # Tempo entre frames em milissegundos
        self.last_update_time = pygame.time.get_ticks()
        

        with open(f"jsons\\cutscene_dialogs.json", "r") as file:
            cutscene = json.load(file)
        self.level.current_dialogue = 0
        self.level.dialogues = cutscene['dialogs']
            
        while self.current_screen == "main_menu":
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        exit()
                    
                    
                    if event.type == pygame.KEYDOWN:
                        
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                        if event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                                         
                            self.current_screen = "initial_cutscene"
                            pygame.display.update()
                            

                
                # Atualizar o frame da animação
                self.current_frame += 0.12
                if self.current_frame >= len(self.frames):
                    self.current_frame = 0

                # Desenhar na tela
                screen.blit(self.frames[int(self.current_frame)], (0, 0))
                pygame.display.flip()
                
                pygame.display.update()
                
                
    def pause(self):
        """
        Displays the pause screen with options to resume, go to the main menu, or quit the game.

        Returns
        -------
        None.
        """
        
        background = pygame.image.load('assets/menus/pause_screen.png')  # Caminho para sua imagem
        background = pygame.transform.scale(background, (850, 600))  
        background_width, background_height = background.get_size()
        
        screen_width, screen_height = screen.get_size()
        background_rect = background.get_rect(center=SCREEN_DIMENSIONS/2)  
        
        background_x = (screen_width - background_width) 
        background_y = (screen_height - background_height) 
        
        while self.current_screen == "pause":
            pause_mouse_pos = pygame.mouse.get_pos() #pegar a pos do mouse

            # Desenhar a imagem de fundo
            screen.blit(background, background_rect.topleft)

            #  Texto botões
            resume_button = Button(image=None, pos=(screen_width // 2, background_rect.topleft[1] + background_height*0.435),
                               text_input="RESUME", font=get_font(40), base_color="Black", hovering_color="White")
            menu_button = Button(image=None, pos=(screen_width // 2, background_rect.topleft[1] + background_height*0.62),
                             text_input="MENU", font=get_font(40), base_color="Black", hovering_color="White")
            quit_button = Button(image=None, pos=(screen_width // 2, background_rect.topleft[1] + background_height*0.8),
                             text_input="QUIT", font=get_font(40), base_color="Black", hovering_color="White")


            for button in [resume_button, menu_button, quit_button]:
                button.change_color(pause_mouse_pos)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start_botao.play(0)
                    pygame.time.delay(100)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.check_for_input(pause_mouse_pos):
                        self.start_botao.play(0)
                        pygame.time.delay(50)
                        self.current_screen = "play"
                    if menu_button.check_for_input(pause_mouse_pos):
                        self.current_screen = "main_menu"
                        self.level.quit_phase()
                        self.start_botao.play(0)
                        pygame.time.delay(50)
                        self.load_audio(START_SOUND_MENU)
                        self.play_music(-1)
                    if quit_button.check_for_input(pause_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def selascou(self):
        """
        Displays the game over screen with the option to try the fase again.

        Returns
        -------
        None.
        """

        background = pygame.image.load('assets/menus/selascou_screen.png')  # Caminho para sua imagem
        background = pygame.transform.scale(background, (600, 260))  
        background_width, background_height = background.get_size()
        
        screen_width, screen_height = screen.get_size()
        background_rect = background.get_rect(center=SCREEN_DIMENSIONS/2)  

        while self.current_screen == "game_over":
            pause_mouse_pos = pygame.mouse.get_pos() #pegar a pos do mouse

            # Desenhar a imagem de fundo
            screen.blit(background, background_rect.topleft)

            #  Texto botões

            try_again_button = Button(image=None, pos=(screen_width // 2, background_rect.topleft[1] + background_height*0.72),
                               text_input="TRY AGAIN", font=get_font(28), base_color="Black", hovering_color="White")

            try_again_button.change_color(pause_mouse_pos)
            try_again_button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if try_again_button.check_for_input(pause_mouse_pos):
                        self.start_botao.play(0)
                        pygame.time.delay(50)
                        self.current_screen = "play"
                        self.level.start_phase()


            pygame.display.update()


    def dialogue(self, i):
        """
        Displays the dialog in the json.

        Returns
        -------
        None.
        """

        def draw_dialog_box(speaker, screen, x, y, width, height, bg_color=(50, 50, 50), border_color=(255, 255, 255), border_width=2):
            """Desenha um retângulo padrão para o diálogo."""
            pygame.draw.rect(screen, bg_color, (x, y, width, height))
            pygame.draw.rect(screen, border_color, (x, y, width, height), border_width)
            picture = pygame.image.load(f'assets/spritesheets/{speaker}_dialogue.png')
            picture = pygame.transform.scale(picture, (100, 100))
            screen.blit(picture, (x + 20, y + (height - 120)))  # Ajustado para alinhar a imagem ao fundo


        def wrap_text(text, font, max_width):
            """Divide o texto em linhas que cabem na largura máxima."""
            words = text.split(" ")
            lines = []
            current_line = ""

            for word in words:
                if font.size(current_line + word)[0] + 100 <= max_width:
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "

            if current_line:
                lines.append(current_line.strip())

            return lines


        def display_dialog(dialog, screen, font, max_width, start_y, line_spacing, box_height=150, reveal_speed=50, start_time=0):
            """Renderiza o diálogo e revela o texto aos poucos."""
            box_width = max_width + 40
            box_x = 30
            box_y = start_y - 20

            # Desenha o retângulo de fundo
            draw_dialog_box(dialog["speaker"], screen, box_x, box_y, box_width, box_height)

            # Renderiza o nome do personagem
            speaker_text = font.render(dialog["speaker"] + ":", True, (255, 255, 255))
            screen.blit(speaker_text, (box_x + 130, start_y))

            # Divide o texto em linhas
            wrapped_lines = wrap_text(dialog["text"], font, max_width)

            # Calcula o número de caracteres a serem exibidos
            time_elapsed = pygame.time.get_ticks() - start_time
            total_chars = time_elapsed // reveal_speed  # Calcula quantas letras mostrar com base no tempo

            # Renderiza o texto progressivamente
            y_offset = start_y + 40
            char_count = 0
            for line in wrapped_lines:
                if y_offset + line_spacing > box_y + box_height:
                    break  # Não exibe além da altura do box

                if char_count + len(line) < total_chars:
                    # Mostra a linha inteira se já passou do tempo
                    rendered_line = font.render(line, True, (255, 255, 255))
                    screen.blit(rendered_line, (box_x + 130, y_offset))
                    char_count += len(line)
                else:
                    # Mostra apenas parte da linha
                    visible_chars = total_chars - char_count
                    rendered_line = font.render(line[:visible_chars], True, (255, 255, 255))
                    screen.blit(rendered_line, (box_x + 130, y_offset))
                    break

                y_offset += line_spacing
           
            if total_chars >= sum(len(line) for line in wrapped_lines):
                self.typing.stop()

            # Verifica se todas as letras já foram exibidas
            return total_chars >= sum(len(line) for line in wrapped_lines)


        # Loop principal
        current_dialog = 0
        running = True
        dialog_done = False
        self.typing.play(loops=-1)
        dialog_start_time = pygame.time.get_ticks()  # Marca o início do diálogo
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and dialog_done:  # Avança apenas se o texto estiver completo
                        current_dialog += 1
                        dialog_done = False
                        self.typing.play(loops=-1)
                        if current_dialog >= len(self.level.dialogues[f"dialog_{i}"]):
                            
                            running = False
                        else:
                            dialog_start_time = pygame.time.get_ticks()  # Reinicia o temporizador para o próximo diálogo

            if current_dialog < len(self.level.dialogues[f"dialog_{i}"]):
                # self.typing.play(loops=-1)
                dialog_done = display_dialog(
                    dialog=self.level.dialogues[f"dialog_{i}"][current_dialog],
                    screen=screen,
                    font=pygame.font.Font("assets/font.ttf", 18),
                    max_width=SCREEN_DIMENSIONS[0] - 100,
                    start_y=SCREEN_DIMENSIONS[1] - 150,
                    line_spacing=40,
                    box_height=150,
                    reveal_speed=10,  # Controla a velocidade das letras
                    start_time=dialog_start_time  # Passa o tempo de início
                )


            
            pygame.display.update()
        self.typing.stop()
        self.level.current_dialogue = None

    def initial_cutscene(self):
        """
        Displays the first cutscene of the game, introducing the players and it's premise.

        Returns
        -------
        None.
        """
        self.fgv.play(loops=-1)
        background = pygame.image.load('assets/backgrounds/fachada_fgv.png')  # Caminho para sua imagem
        background = pygame.transform.scale(background, SCREEN_DIMENSIONS)  
        background_rect = background.get_rect(center=SCREEN_DIMENSIONS/2)
        screen.blit(background, background_rect.topleft)
        pygame.time.delay(500)

        self.dialogue(0)
        pygame.time.delay(500)
        self.fgv.stop()

        self.laboratorio.play(loops=-1)
        background = pygame.image.load('assets/backgrounds/laboratorio.png')  # Caminho para sua imagem
        background = pygame.transform.scale(background, SCREEN_DIMENSIONS)  
        background_rect = background.get_rect(center=SCREEN_DIMENSIONS/2)
        screen.blit(background, background_rect.topleft)
        pygame.time.delay(500)
        
        self.dialogue(1)
        pygame.time.delay(500)
        self.laboratorio.stop()

        self.botao_3.play(loops=0)
        background = pygame.image.load('assets/backgrounds/botao.png')  # Caminho para sua imagem
        background = pygame.transform.scale(background, SCREEN_DIMENSIONS) 
        background_rect = background.get_rect(center=SCREEN_DIMENSIONS/2) 
        screen.blit(background, background_rect.topleft)
        pygame.time.delay(500)
        
        self.dialogue(2)
        pygame.time.delay(500)
        self.botao_3.stop()

        pygame.display.update()

        self.current_screen = "play"
        self.level.start_phase()

    def final_screen(self):
        """
        Displays the final screen of the the game, thanking the gamer for playing.

        Returns
        -------
        None.
        """
        running = True

        #  Configurações de tela
        self.screen_width = SCREEN_DIMENSIONS[0]
        self.screen_height = SCREEN_DIMENSIONS[1]
        
        # Configurações dos frames
        self.columns = FINAL_COLUMNS_MENU
        self.rows = FINAL_ROWS_MENU
        
        #  Carregar  a imagem com os frames
        self.sprite_sheet = pygame.image.load(FINAL_SCREEN_MENU).convert_alpha()
        self.dimensions = (self.sprite_sheet.get_width(), self.sprite_sheet.get_height())
        self.frame_width = self.dimensions[0] // self.columns
        self.frame_height = self.dimensions[1] // self.rows
        
        # Extrair frames da sprite sheet
        self.frames = self.extract_frames()
        
        #  Controle da animação
        self.current_frame = 0
        self.frame_delay = 100  # Tempo entre frames em milissegundos
        self.last_update_time = pygame.time.get_ticks()

        final_music = pygame.mixer.Sound('audios\\backmusic.mp3')
        final_music.play(-1)
            
        while self.current_screen == "final_screen":
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        exit()
                    
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                            self.level.phase_counter = 0
                            self.current_screen = "main_menu"
                            final_music.stop()
                            pygame.display.update()
                            

                
                # Atualizar o frame da animação
                self.current_frame += 0.12
                if self.current_frame >= len(self.frames):
                    self.current_frame = 0

                # Desenhar na tela
                screen.blit(self.frames[int(self.current_frame)], (0, 0))
                pygame.display.flip()
                
                pygame.display.update()
                