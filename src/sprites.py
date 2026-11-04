"""Sprites e entidades visuais do Space Invaders."""

import pygame

from .settings import (
    DIRECTORY,
    RED,
    SCREEN_WIDTH,
    SPRINGREEN,
    WHITE,
)


class Edge(pygame.sprite.Sprite):
    """
    Estrutura criada para facilitar a anÃ¡lise de colisÃµes com as bordas.
    """

    def __init__(self, width, height, x, y):
        """
        Cria as bordas do jogo.

        width: largura da borda.
        height: altura da borda.
        x: posiÃ§Ã£o no eixo x.
        y: posiÃ§Ã£o no eixo y.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Block(pygame.sprite.Sprite):
    """
    ResponsÃ¡vel por criar barreiras que protegem a nave.
    """

    def __init__(self, color = WHITE, size = 10):
        """
        Cria cada bloco com uma determinada cor e tamanho.

        color: cor que o bloco terÃ¡.
        size: tamanho de cada quadrado.
        """
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.size = size
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(color)
        self.rect = self.image.get_rect()


class Ship(pygame.sprite.Sprite):
    """
    Classe que representa a nave do jogador.
    """

    def __init__(self, path, pos_x, pos_y, speed = 5):
        """
        Cria uma nave.

        path: caminho onde estÃ¡ a imagem que representa a nave.
        pos_x: posiÃ§Ã£o inicial da nave no eixo x.
        pos_y: posiÃ§Ã£o inicial da nave no eixo y.
        speed: velocidade que a nave se deslocarÃ¡. Por padrÃ£o ela Ã© 5px.
        """
        pygame.sprite.Sprite.__init__(self)
        self.__initial_position = (pos_x, pos_y)
        # Carregando a imagem da nave
        self.__image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.__image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed
        # A nave inicia com 3 vidas
        self.lifes = 3
        # Sons que a nave possui quando atira ou quando Ã© atingida
        self.__sound_shot = pygame.mixer.Sound(DIRECTORY + "/assets/sounds/shoot.wav")
        self.__ship_explosion = pygame.mixer.Sound(DIRECTORY + "/assets/sounds/shipexplosion.wav")

    def initial_position(self):
        """
        Define as posiÃ§Ãµes iniciais da nave.
        """
        self.rect.x = self.__initial_position[0]
        self.rect.y = self.__initial_position[1]

    def die(self):
        """
        Assim que a nave Ã© atingida esse mÃ©todo Ã© chamado para realizar as devidas
        aÃ§Ãµes que sÃ£o necessÃ¡rias.
        As aÃ§Ãµes sÃ£o: reproduzir o som de explosÃ£o definido na construÃ§Ã£o do objeto,
        retornar a nave Ã  posiÃ§Ã£o inicial e reduzir a sua quantidade de vidas.
        """
        self.__ship_explosion.play()
        self.initial_position()
        self.lifes -= 1

    def shoot(self):
        """
        MÃ©todo que permite a nave atirar.
        Ao ser chamado Ã© liberado o som de tiro e criado um projÃ©til.
        """
        self.__sound_shot.play()
        bullet = Bullet(self.rect.midtop, 1)
        return bullet

    def update(self, *args):
        """
        MÃ©todo que realiza a atualizaÃ§Ã£o da posiÃ§Ã£o da nave Ã  medida que o
        jogador a movimenta.
        """
        # Se estiver pressionando o botÃ£o da seta da direita
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if self.rect.right < (SCREEN_WIDTH - self.speed):
                self.rect.x += self.speed
        # Se estiver pressionando o botÃ£o da seta da esquerda
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            if self.rect.left > self.speed:
                self.rect.x -= self.speed

    def __str__(self):
        """
        RepresentaÃ§Ã£o textual do objeto, indicando a sua posiÃ§Ã£o atual.
        """
        return "Ship in (%s, %s)" % (self.rect.x, self.rect.y)


class Invader(pygame.sprite.Sprite):
    """
    Classe que representa os invasores.
    """

    def __init__(self, sprite, pos_x, pos_y, speed = 1):
        """
        MÃ©todo responsÃ¡vel por criar cada invasor.

        sprite: imagem que representa cada invasor.
        pos_x: posiÃ§Ã£o inicial do invasor no eixo x.
        pos_y: posiÃ§Ã£o inicial do invasor no eixo y.
        speed: velocidade em que cada objeto se movimenta.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = sprite.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed

    def shoot(self):
        """
        MetÃ³do que permite cada invasor disparar.
        """
        bullet = Bullet(self.rect.midtop, -1, speed = 4, color = RED)
        return bullet

    def up_speed(self):
        """
        Aumenta a velocidade com que cada invasor se movimenta.
        """
        self.speed += 0.5

    def down_invader(self):
        """
        MÃ©todo que movimenta as sprites ao longo do eixo y.
        """
        self.rect.y += 20

    def update(self, direction):
        """
        MÃ©todo que movimentas as sprites ao longo do eixo x.
        """
        self.rect = self.rect.move(self.speed * direction, 0)

    def __str__(self):
        """
        RepresentaÃ§Ã£o textual do objeto, indicando a sua posiÃ§Ã£o atual.
        """
        return "Invader in (%s, %s)" % (self.rect.x, self.rect.y)


class Mystery(pygame.sprite.Sprite):
    """
    Classe que representa a Mystery do jogo tradicional.
    """

    def __init__(self, sprite, pos_x, pos_y, speed = 2.7):
        """
        MÃ©todo responsÃ¡vel por criar a nave-mÃ£e.

        sprite: imagem que representa a nave.
        pos_x: posiÃ§Ã£o inicial da nave no eixo x.
        pos_y: posiÃ§Ã£o inicial da nave no eixo y.
        speed: velocidade em que a nave se movimenta.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))
        self.speed = speed

    def update(self, *args):
        if (self.rect.x >= (SCREEN_WIDTH + 200)):
            self.kill()
        else:
            self.rect = self.rect.move(self.speed, 0)


class Bullet(pygame.sprite.Sprite):
    """
    Classe que representa as balas de todos os objetos que realizam disparos.
    """

    def __init__(self, pos_xy, direction, color = SPRINGREEN, speed = 8):
        """
        ConstrÃ³i um objeto do tipo Bullet.

        pos_xy: Ã© o ponto (x, y) que Ã© o ponto mÃ©dio da borda superior
                da sprite.
        direction: direÃ§Ã£o que o objeto se deslocarÃ¡.
        speed: velocidade que o objeto se deslocarÃ¡.
                Por padrÃ£o Ã© 8px.
        color: cor do objeto.
                Por padrÃ£o Ã© azul-marinho.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos_xy[0]
        self.rect.y = pos_xy[1]
        self.direction = direction
        self.speed = speed * direction

    def update(self, *args):
        """
        Atualiza o objeto durante o seu deslocamento.
        """
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            self.kill()
