import random
import pygame
from ElementoJogo import ElementoJogo


class Asteroid(ElementoJogo):
    def __init__(self, largura_tela, altura_tela, velocidade=5, cor=(200, 50, 50)):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.raio = 35
        self.vida = 2
        self.destruido = False
        self.tempo_destruicao = 0

        super().__init__(
            x=0,
            y=0,
            largura=self.raio * 2,
            altura=self.raio * 2,
            cor=cor,
            velocidade=velocidade
        )

        imagem_original = pygame.image.load("img/joker.png").convert_alpha()
        self.imagem = pygame.transform.scale(imagem_original, (self.rect.width, self.rect.height))

        # Cria uma versão vermelha da imagem
        self.imagem_vermelha = self.imagem.copy()
        self.imagem_vermelha.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)

        # Imagem do segundo dano
        explosao_original = pygame.image.load("img/explosao.png").convert_alpha()

        self.imagem_explosao = pygame.transform.scale(explosao_original, (self.rect.width, self.rect.height))

        self.iniciar_status()

    def iniciar_status(self):
        diametro =self.raio * 2
        limite_x = self.largura_tela - diametro

        self.rect.x = random.randint(0, limite_x)
        self.rect.y = random.randint(-150, -50)
        self.velocidade = random.randint(3, 6)
        self.vida = 2
        self.destruido = False

    def mover(self):
        self.rect.y += self.velocidade

        # Reinicia no topo caso passe reto pelo fundo da tela
        if self.rect.top > self.altura_tela:
            self.iniciar_status()

    def desenhar(self, tela):
        if self.vida == 2:
            tela.blit(self.imagem, self.rect)

        elif self.vida == 1:
            tela.blit(self.imagem_vermelha, self.rect)

        elif self.vida == 0:
            tela.blit(self.imagem_explosao, self.rect)