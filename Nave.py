import pygame
from ElementoJogo import ElementoJogo

class Nave(ElementoJogo):
    def __init__(self, largura_tela, altura_tela, velocidade=8, cor=(0, 255, 100)):
        # Inicializa a classe base com posição inicial centralizada embaixo
        super().__init__(
            x=largura_tela // 2 - 20,
            y=altura_tela - 60,
            largura=40,
            altura=40,
            cor=cor,
            velocidade=velocidade
        )
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.vel_x = 0
        self.tiros = []  # Lista que guardará os tiros ativos

    def processar_evento(self, evento):
        """Controla os eventos de teclado para movimentação e disparo."""
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                self.vel_x = -self.velocidade
            elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                self.vel_x = self.velocidade
            elif evento.key == pygame.K_SPACE:
                self.atirar()

        elif evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT, pygame.K_a) and self.vel_x < 0:
                self.vel_x = 0
            elif evento.key in (pygame.K_RIGHT, pygame.K_d) and self.vel_x > 0:
                self.vel_x = 0

    def mover(self):
        """Aplica o deslocamento horizontal e trava nas bordas da tela."""
        self.rect.x += self.vel_x

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.largura_tela:
            self.rect.right = self.largura_tela

    def atirar(self):
        # Largura e altura do tiro
        largura_tiro = 4
        altura_tiro = 10

        # Cria o tiro centralizado no topo da nave
        tiro = pygame.Rect(
            self.rect.centerx - largura_tiro // 2,
            self.rect.top - altura_tiro,
            largura_tiro,
            altura_tiro
        )

        # Adiciona o tiro à lista de tiros ativos
        self.tiros.append(tiro)

    def atualizar_tiros(self):
        for tiro in self.tiros:
            # Move o tiro para cima
            tiro.y -= 25

        # Remove os tiros que saíram pelo topo da tela
        self.tiros = [tiro for tiro in self.tiros if tiro.bottom >= 0]

    def atualizar(self):
        self.mover()
        self.atualizar_tiros()

    def desenhar(self, tela):
        # Polimorfismo: desenha a nave em formato de triângulo
        pontos = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
        ]
        pygame.draw.polygon(tela, self.cor, pontos)

        # Desenha os tiros ativos na cor branca
        for tiro in self.tiros:
            pygame.draw.rect(tela, (255, 255, 255), tiro)