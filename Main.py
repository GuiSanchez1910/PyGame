import pygame
from Nave import Nave
from Asteroid import Asteroid


class Jogo:
    def __init__(self, largura=800, altura=600):
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Space Shooter - Projeto Base")

        self.clock = pygame.time.Clock()
        self.fps = 10
        self.rodando = True
        self.pontos = 0

        # Elementos do jogo
        self.nave = Nave(self.largura, self.altura)
        self.asteroide = Asteroid(self.largura, self.altura)

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            self.nave.processar_evento(evento)

    def checar_colisoes(self):
        for tiro in self.nave.tiros[:]:
            if tiro.colliderect(self.asteroide.rect):
                self.nave.tiros.remove(tiro)
                self.asteroide.iniciar_status()
                self.pontos += 1
                print(f"Acertou! Pontos = {self.pontos}")

        if self.nave.rect.colliderect(self.asteroide.rect):
            self.rodando = False
            print(f"Game Over! Um asteroide te atingiu. \nPontuação Final: {self.pontos}")

    def atualizar(self):
        self.nave.atualizar()
        self.asteroide.mover()
        self.checar_colisoes()

    def desenhar(self):
        self.tela.fill((15, 15, 25))
        self.nave.desenhar(self.tela)
        self.asteroide.desenhar(self.tela)
        pygame.display.flip()

    def executar(self):
        while self.rodando:
            self.clock.tick(self.fps)
            self.processar_eventos()
            self.atualizar()
            self.desenhar()

        pygame.quit()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()