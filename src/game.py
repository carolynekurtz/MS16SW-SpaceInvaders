"""Controle principal e regras do jogo Space Invaders."""

from random import choice, randint

import pygame

from .settings import (
    BLACK,
    DIRECTORY,
    FONT,
    GOLD,
    GREEN,
    RED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
    TEAL
)
from .sprites import Block, Edge, Invader, Mystery, Ship


class SpaceInvaders():
    """
    Classe que comanda os principais comandos do jogo.
    """

    def __init__(self):
        """
        Permite criar uma instÃ¢ncia do jogo.
        """
        # Definindo os caminhos dos arquivos necessÃ¡rios para o jogo
        self.ship_shot = pygame.sprite.GroupSingle()
        self.invader_shot = pygame.sprite.Group()

        """
        Para colocar em tela cheia usa o comando:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        """
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Coloca uma legenda para a janela
        pygame.display.set_caption("Space Invaders")
        # Coloca um Ã­cone na janela
        logo = pygame.image.load(DIRECTORY + "/assets/images/logo.png")
        pygame.display.set_icon(logo)
        self.score = 0
        self.level = 0
        self.speed = 0
        '''
        Criando um objeto do tipo pygame.font.Font, onde Ã© passada a fonte e o tamanho
        se a fonte for passada como None Ã© utilizada a padrÃ£o do sistema.
        '''
        self.font = self.create_font(60)
        self.score_font = self.create_font(15)
        self.explosion_sound = pygame.mixer.Sound(DIRECTORY + "/assets/sounds/invaderkilled.wav")

        # Carregando imagens necessÃ¡rias
        self.path_image_ship = DIRECTORY + "/assets/images/ship.png"
        background_image = pygame.image.load(DIRECTORY + "/assets/images/back.png")
        explosion_image = pygame.image.load(DIRECTORY + "/assets/images/explosion.png")
        lifes_image = pygame.image.load(DIRECTORY + "/assets/images/heart.png")

        self.ship = pygame.sprite.GroupSingle(
                                Ship(self.path_image_ship, (SCREEN_WIDTH - 50) // 2,
                                        (SCREEN_HEIGHT - 110)))
        self.ship_sprite = self.ship.sprites()[0]
        mystery_image = pygame.image.load(DIRECTORY + "/assets/images/boss3.png")
        self.mystery_image = pygame.transform.scale(mystery_image, [71, 39])
        self.mystery = pygame.sprite.GroupSingle(
                                Mystery(self.mystery_image, self.random_position(), 15))
        self.background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.lifes_image = pygame.transform.scale(lifes_image, (25, 25))
        self.explosion_image = pygame.transform.scale(explosion_image, (
                                    (SCREEN_WIDTH // 20), (SCREEN_WIDTH // 20)))
        self.clock = pygame.time.Clock()
        # Pausa (SM-13)
        self.paused = False
        self.pause_start = 0
        self.pause_font = self.create_font(60)
        self.pause_icon = pygame.image.load(DIRECTORY + "/assets/images/pause.png")
        self.play_icon = pygame.image.load(DIRECTORY + "/assets/images/play.png")
        self.pause_button_rect = self.pause_icon.get_rect(
            topleft=(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 34))
        self.invaders = pygame.sprite.OrderedUpdates()
        self.invaders_direction = 1
        self.increment_speed = False

        self.left_edge = pygame.sprite.GroupSingle(Edge(5, SCREEN_HEIGHT, 0, 0))
        self.right_edge = pygame.sprite.GroupSingle(Edge(5, SCREEN_HEIGHT, 795, 0))
        self.bottom_edge = pygame.sprite.GroupSingle(Edge(SCREEN_WIDTH, 5, 0, 560))
        self.groups = pygame.sprite.Group(self.ship_shot, self.invader_shot,
                                    self.invaders, self.mystery)

         # Janela de instruÃ§Ãµes (SM-15)
        self.instructions_shown = False

    def random_position(self):
        """
        Escolhe aleatoriamente uma posiÃ§Ã£o inicial no eixo x
        para a nave-mÃ£e.
        """
        return choice([-1700, -1900, -2200, -2500, -1500])

    def home_screen(self):
        """
        Exibe a tela inicial mantendo os comandos originais:
        ENTER/SPACE inicia o jogo e ESC fecha a aplicaÃ§Ã£o.
        """
        menu = True
        music_menu = pygame.mixer.Sound(DIRECTORY + "/assets/sounds/menu.wav")
        music_menu.play(-1)

        background = pygame.image.load(
            DIRECTORY + "/assets/images/menu_background.png"
        ).convert()
        background = pygame.transform.scale(
            background, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        logo = pygame.image.load(
            DIRECTORY + "/assets/images/logo.png"
        ).convert_alpha()
        logo = pygame.transform.scale(logo, (350, 197))
        logo_rect = logo.get_rect(center=(SCREEN_WIDTH // 2, 125))

        menu_font = self.create_font(18)
        subtitle_font = self.create_font(13)

        # MantÃ©m a nave-mÃ£e animada na tela inicial.
        mystery = pygame.image.load(
            DIRECTORY + "/assets/images/boss1.png"
        ).convert_alpha()
        mystery = pygame.transform.scale(mystery, (100, 56))
        rect_mystery = mystery.get_rect(center=(SCREEN_WIDTH // 2, 285))
        speed = [3, 2]

        start_rect = pygame.Rect(220, 390, 360, 58)
        exit_rect = pygame.Rect(220, 470, 360, 58)

        def draw_menu_button(rect, label, color):
            pygame.draw.rect(self.window, (5, 8, 28), rect)
            pygame.draw.rect(self.window, color, rect, 3)
            inner_rect = rect.inflate(-10, -10)
            pygame.draw.rect(self.window, (28, 20, 65), inner_rect, 1)

            # Pequenos recortes quadrados dÃ£o acabamento de interface arcade.
            corner_size = 7
            for x in (rect.left, rect.right - corner_size):
                for y in (rect.top, rect.bottom - corner_size):
                    pygame.draw.rect(
                        self.window, color,
                        (x, y, corner_size, corner_size)
                    )

            label_surface = menu_font.render(label, False, WHITE)
            self.window.blit(
                label_surface, label_surface.get_rect(center=rect.center)
            )

        subtitle = subtitle_font.render(
            "DEFEND THE GALAXY", False, (125, 190, 255)
        )
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 350))

        while menu:
            if (rect_mystery.left < 0 or
                    rect_mystery.right > SCREEN_WIDTH):
                speed[0] = -speed[0]
            if (rect_mystery.top < 230 or
                    rect_mystery.bottom > 335):
                speed[1] = -speed[1]

            rect_mystery.x += speed[0]
            rect_mystery.y += speed[1]

            for event in pygame.event.get():
                wants_to_quit = (
                    event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and
                     event.key == pygame.K_ESCAPE)
                )
                if wants_to_quit:
                    music_menu.stop()
                    return False

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.start_game()
                        music_menu.stop()
                        return True

            self.window.blit(background, (0, 0))
            self.window.blit(logo, logo_rect)
            self.window.blit(mystery, rect_mystery)
            self.window.blit(subtitle, subtitle_rect)

            draw_menu_button(
                start_rect, "ENTER / SPACE  START", (70, 225, 255)
            )
            draw_menu_button(
                exit_rect, "ESC  EXIT", (238, 75, 205)
            )

            self.clock.tick(60)
            pygame.display.update()

    def final_screen(self):
        """
        Cria a tela final do jogo.
        """
        music_menu = pygame.mixer.Sound(DIRECTORY + "/assets/sounds/menu.wav")
        music_menu.play(-1)
        self.game_over_screen()

        self.font50 = self.create_font(50)
        self.font20 = self.create_font(20)

        text1 = self.font50.render("FINAL SCORE: %d" % self.score, False, GOLD)
        text2 = self.font20.render("PRESS ENTER TO TRY AGAIN", False, WHITE)
        text3 = self.font20.render("PRESS ESC TO OUT", False, WHITE)

        text1_rect = text1.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 350))
        text2_rect = text2.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        text3_rect = text3.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))

        self.window.fill(BLACK)
        self.window.blit(text1, text1_rect)
        self.window.blit(text2, text2_rect)
        self.window.blit(text3, text3_rect)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    music_menu.stop()
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        music_menu.stop()
                        self.level = 0
                        self.speed = 0
                        self.ship = pygame.sprite.GroupSingle(
                                Ship(self.path_image_ship, (SCREEN_WIDTH) // 2, (SCREEN_HEIGHT - 110)))
                        self.ship_sprite = self.ship.sprites()[0]
                        self.start_game()
                        return

                    if event.key == pygame.K_ESCAPE:
                        music_menu.stop()
                        pygame.quit()
                        exit()

    def show_message_screen(self, message, color, duration_ms, x_offset):
        """
        Exibe uma mensagem centralizada na tela por um tempo determinado.

        RefatoraÃ§Ã£o aplicada: Extract Method. O laÃ§o de exibiÃ§Ã£o era idÃªntico
        em level_screen e game_over_screen (mudavam sÃ³ o texto, a cor, a
        duraÃ§Ã£o e a posiÃ§Ã£o) e foi extraÃ­do para este mÃ©todo. Qualquer
        ajuste nessas telas deve ser feito aqui, em um sÃ³ lugar.

        ParÃ¢metros:
            message: texto exibido.
            color: cor do texto.
            duration_ms: duraÃ§Ã£o da tela, em milissegundos.
            x_offset: valor usado para centralizar o texto na horizontal.
        """
        font = self.create_font(100)
        text = font.render(message, False, color)
        start = pygame.time.get_ticks()

        while ((pygame.time.get_ticks() - start) < duration_ms):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.window.blit(self.background, [0, 0])
            self.window.blit(text, [(SCREEN_WIDTH - x_offset) // 2, 220])
            pygame.display.update()

    def level_screen(self):
        """
        Cria a tela que indica o nÃ­vel que irÃ¡ iniciar.
        Ela dura 1 segundo (1000 milisegundos).
        """
        self.level += 1
        if (self.level > 1 and self.level < 6):
            self.speed += 0.3
        elif (self.level == 1):
            self.speed += 1

        # self.time marca o inÃ­cio do nÃ­vel e Ã© usado em update_direction.
        self.time = pygame.time.get_ticks()
        self.show_message_screen('LEVEL: ' + str(self.level), GOLD, 1000, 450)

    def game_over_screen(self):
        """
        Cria a tela de game over.
        Ela dura 1.5 segundo (1500 milisegundos).
        """
        self.show_message_screen('GAME OVER', RED, 1500, 600)

    def start_game(self):
        """
        Limpa todas as variÃ¡veis para que se possa iniciar o jogo.
        """
        self.groups.add(self.ship)
        self.invaders_direction = 1
        self.blocks = pygame.sprite.Group(self.build_blocks(0),
                                            self.build_blocks(1),
                                            self.build_blocks(2))
        self.invaders.empty()
        self.mystery.empty()
        self.invader_shot.empty()
        self.ship_shot.empty()
        if not self.instructions_shown:
            self.instructions_screen()
        self.level_screen()
        self.create_invaders()
        self.ship_sprite.initial_position()
        self.update()

    def build_blocks(self, number):
        """
        ConstrÃ³i cada bloco que fica entre os invasores e a nave.
        Cada bloco Ã© constituÃ­do de diversos pequenos blocos, o que facilita
        analisar as colisÃµes.

        number: Ã© o nÃºmero do bloco, isso ajuda a indicar a posiÃ§Ã£o
                que ele serÃ¡ construÃ­do.
        """
        aux = pygame.sprite.Group()
        for row in range(4):
            for column in range(10):
                blocker = Block(color=TEAL)
                blocker.rect.x = 45 + (300 * number) + (column * blocker.size)
                blocker.rect.y = 400 + (row * blocker.size)
                aux.add(blocker)
        return aux

    def create_invaders(self):
        """
        Cria os invasores e coloca todos em um grupo.
        """
        enemy_types = []

        for i in range(1, 8):
            enemy_types.append(pygame.image.load(DIRECTORY + ("/assets/images/invader%d.png" % (i % 2))))

        x = 25

        # Preenchendo os invasores pelas colunas.
        for j in range(7):
            y = 60
            for i in range(5):
                sprite = pygame.transform.scale(enemy_types[i],
                                ((SCREEN_WIDTH // 20), (SCREEN_WIDTH // 20)))
                self.invaders.add(Invader(sprite, x, y, self.speed))
                y += 45
            x += 62

    def showShipLives(self):
        """
        Mostra na tela as vidas que a nave possui.
        """
        y = 10
        for i in range(self.ship_sprite.lifes):
            self.window.blit(self.lifes_image, (y, 570))
            y += 40

    def enemy_shot(self):
        """
        Escolhe aleatoriamente um invasor para que ele realize algum disparo.
        """
        enemy = [i for i in self.invaders]

        for i in range(2):
            invader = choice(enemy)
            self.invader_shot.add(invader.shoot())

    def update(self):
        """
        Realiza todas as atualizaÃ§Ãµes necessÃ¡rias para o jogo.
        """
        score = self.score_font.render("SCORE: %d" % self.score, False, WHITE)

        current_time = pygame.time.get_ticks()

        if (current_time % 2000.0 < 20):
            self.enemy_shot()

        if ((len(self.mystery) == 0)):
            self.mystery.add(Mystery(self.mystery_image, self.random_position(), 15))

        self.window.blit(self.background, [0, 0])
        self.window.blit(score, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30))
        self.groups.draw(self.window)
        self.blocks.draw(self.window)

        self.groups.update(self.invaders_direction)
        self.update_direction()
        self.check_collisions()
        self.showShipLives()
        self.draw_pause_button()

        self.groups = pygame.sprite.Group(self.ship, self.ship_shot, self.invader_shot, self.invaders,
                                    self.left_edge, self.bottom_edge, self.right_edge, self.mystery)
        self.clock.tick(60)
        pygame.display.update()

    def check_collisions(self):
        """
        Realiza todas as checagens de colisÃµes do jogo e as suas
        consequÃªncias.
        """

        """
        Se ocorrer uma colisÃ£o entre os projÃ©teis da nave e de algum
        invasor ambas sÃ£o mortas e ocorre um acrÃ©scimo de um valor entre
        5 e 20 na pontuaÃ§Ã£o do jogador.
        """
        if pygame.sprite.groupcollide(self.ship_shot, self.invader_shot, True, True):
            self.score += randint(5, 20)

        # ColisÃ£o entre as balas e a borda inferior, apenas os disparos sÃ£o mortos.
        pygame.sprite.groupcollide(self.invader_shot, self.bottom_edge, True, False)
        # ColisÃ£o entre os disparos dos invasores e os blocos, ambos morrem.
        pygame.sprite.groupcollide(self.invader_shot, self.blocks, True, True)
        # ColisÃ£o entre o disparo da nave e os blocos, ambos morrem.
        pygame.sprite.groupcollide(self.ship_shot, self.blocks, True, True)
        # ColisÃ£o entre os blocos e os invasores, apenas os blocos morrem.
        pygame.sprite.groupcollide(self.blocks, self.invaders, True, False)

        # ColisÃ£o entre a nave e os invasores
        if pygame.sprite.groupcollide(self.ship, self.invaders, False, False):
            self.ship_sprite.die()

        # ColisÃ£o entre a nave-mÃ£e e o tiro da nave. A pontuaÃ§Ã£o serÃ¡ um valor entre 25 e 55.
        if pygame.sprite.groupcollide(self.mystery, self.ship_shot, True, True):
            self.score += choice([25, 35, 45, 55])
            self.explosion_sound.play()

        '''
        ColisÃ£o entre os disparos da nave e os invasores, ambos morrem.
        AlÃ©m disso Ã© colocado a imagem, o som de explosÃ£o e um acrÃ©scimo
        na pontuaÃ§Ã£o podendo ser [10, 15, 20, 25, 30, 35, 40].
        '''
        for atingidos in pygame.sprite.groupcollide(self.ship_shot, self.invaders, True, True).values():
            for invasor in atingidos:
                self.explosion_sound.play()
                self.window.blit(self.explosion_image, (invasor.rect.x, invasor.rect.y))
                self.score += choice([10, 15, 20, 25, 30, 35, 40])

        # Verifica a colisÃ£o dos disparos realizados pelos invasores e a nave. Apenas o tiro morre.
        if (pygame.sprite.groupcollide(self.ship, self.invader_shot, False, True)):
            self.explosion_sound.play()
            self.window.blit(self.explosion_image, (self.ship_sprite.rect.x, self.ship_sprite.rect.y))
            self.ship_sprite.die()

    def update_direction(self):
        """
        Atualiza a direÃ§Ã£o dos invasores.
        JÃ¡ que os invasores sÃ£o colocados na tela coluna a coluna Ã© possÃ­vel
        saber quem sÃ£o os primeiros e os Ãºltimos que foram inseridos para poder
        controlar os limites da tela.
        """
        arr = self.invaders.sprites()
        first = arr[0]
        last = arr[-1]

        # RefatoraÃ§Ã£o aplicada: Replace Nested Conditional with Guard Clauses.
        # ClÃ¡usula de guarda: se nenhum invasor chegou Ã  borda, nÃ£o hÃ¡ nada a fazer.
        if not ((last.rect.x > (SCREEN_WIDTH - last.rect.width - 10)) or (first.rect.x < 10)):
            return

        self.invaders_direction *= -1
        current_time = pygame.time.get_ticks()
        if (current_time - self.time > (8000 // self.speed)):
            self.down_invader(arr)

    def down_invader(self, arr):
        """
        Movimenta cada invasor pelo eixo y.
        """
        up_speed = (len(self.invaders) <= 8)

        for enemy in arr:
            if up_speed:
                enemy.up_speed()
            enemy.down_invader()

    def create_font(self, size):
        return pygame.font.Font(FONT, size)

    def can_shoot(self, event):
        """
        Indica se a nave pode atirar: o jogador apertou uma tecla de disparo
        (seta para cima ou espaÃ§o) e nÃ£o hÃ¡ outro tiro da nave na tela.

        RefatoraÃ§Ã£o aplicada: Decompose Conditional. A condiÃ§Ã£o que ficava
        em uma linha sÃ³ dentro de main foi extraÃ­da para este mÃ©todo, para
        que a regra de disparo tenha um nome e um lugar prÃ³prio.
        """
        pressed_shoot_key = event.key == pygame.K_UP or event.key == pygame.K_SPACE
        return pressed_shoot_key and not self.ship_shot

    def fire_ship_shot(self):
        """
        Cria o disparo da nave e o adiciona ao grupo de tiros.
        """
        self.ship_shot.add(self.ship_sprite.shoot())

    def toggle_pause(self):
        """
        Pausa ou retoma o jogo. Ao pausar, guarda o instante da pausa e
        exibe o aviso PAUSED. Ao retomar, soma o tempo parado a self.time,
        para que o controle de descida dos invasores (update_direction)
        nÃ£o conte o tempo em que o jogo ficou parado.
        """
        if self.paused:
            self.time += pygame.time.get_ticks() - self.pause_start
            self.paused = False
        else:
            self.pause_start = pygame.time.get_ticks()
            self.paused = True
            self.show_paused_message()
        self.draw_pause_button()
        pygame.display.update()

    def show_paused_message(self):
        """
        Desenha o aviso PAUSED no centro da tela, sobre a Ãºltima imagem do jogo.
        """
        text = self.pause_font.render("PAUSED", False, GOLD)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.window.blit(text, text_rect)


    def draw_pause_button(self):
        """
        Desenha o Ã­cone de pausa (ou de continuar, se o jogo estÃ¡ pausado).
        Antes, restaura o fundo na Ã¡rea do Ã­cone para nÃ£o sobrepor o desenho anterior.
        """
        self.window.blit(self.background, self.pause_button_rect, self.pause_button_rect)
        icon = self.play_icon if self.paused else self.pause_icon
        self.window.blit(icon, self.pause_button_rect)


    def instructions_screen(self):
        """
        Exibe a janela de instruÃ§Ãµes com as teclas do jogo.
        Aparece sÃ³ na primeira partida e fecha ao clicar no botÃ£o CLOSE
        ou ao apertar ENTER. O jogo nÃ£o comeÃ§a enquanto ela estÃ¡ aberta.
        """
        title_font = self.create_font(50)
        text_font = self.create_font(20)
        lines = ["ARROWS : MOVE", "SPACE OR UP : SHOOT", "P : PAUSE", "ESC : QUIT"]

        panel = pygame.Rect(0, 0, 560, 380)
        panel.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        button = pygame.Rect(0, 0, 240, 50)
        button.center = (SCREEN_WIDTH // 2, panel.bottom - 50)

        title = title_font.render("HOW TO PLAY", False, GOLD)
        button_text = text_font.render("CLOSE : ENTER", False, GREEN)

        opened = True
        while opened:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    opened = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button.collidepoint(event.pos):
                        opened = False

            self.window.blit(self.background, [0, 0])
            pygame.draw.rect(self.window, BLACK, panel)
            pygame.draw.rect(self.window, WHITE, panel, 3)
            self.window.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, panel.top + 55)))

            y = panel.top + 130
            for line in lines:
                text = text_font.render(line, False, WHITE)
                self.window.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, y)))
                y += 45

            pygame.draw.rect(self.window, GREEN, button, 3)
            self.window.blit(button_text, button_text.get_rect(center=button.center))
            self.clock.tick(60)
            pygame.display.update()

        self.instructions_shown = True

    def main(self):
        """
        MÃ©todo principal do jogo.
        """

        # VariÃ¡vel necessÃ¡ria para que o loop onde o jogo ocorre dure o tempo necessÃ¡rio.
        run = True
        menu = True

        while menu:
            command = self.home_screen()

            if not command:
                menu = False
                pygame.quit()
                exit()

            while run:
                if self.ship_sprite.lifes <= 0:
                    self.final_screen()
                    self.score = 0
                elif len(self.invaders) == 0:
                    self.start_game()
                else:
                    for event in pygame.event.get():
                        # Verificando se o usuÃ¡rio clicou na opÃ§Ã£o de fechar a janela.
                        if event.type == pygame.QUIT:
                            run, menu = False, False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                run, menu = False, False
                            if event.key == pygame.K_p:
                                self.toggle_pause()
                            if self.can_shoot(event) and not self.paused:
                                self.fire_ship_shot()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if self.pause_button_rect.collidepoint(event.pos):
                                self.toggle_pause()

                    if self.paused:
                        self.clock.tick(60)
                    else:
                        self.update()
