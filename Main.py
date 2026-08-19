import random
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
        self.fps = 60
        self.rodando = True
        self.pontos = 0

        # Elementos do jogo
        self.nave = Nave(self.largura, self.altura)

        self.asteroides = []
        self.limite_asteroides = 5
        self.tempo_ultimo_spawn = pygame.time.get_ticks()
        self.intervalo_spawn = 2000

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            self.nave.processar_evento(evento)

    def checar_colisoes(self):
        for ast in self.asteroides[:]:
            if self.nave.rect.colliderect(ast.rect):
                self.rodando = False
                print(f"Game Over! A nave foi atingida :( \nPontuação Final: {self.pontos}")

            for tiro in self.nave.tiros[:]:
                if tiro.colliderect(ast.rect):
                    if tiro in self.nave.tiros:
                        self.nave.tiros.remove(tiro)

                    ast.iniciar_status()
                    self.pontos += 1
                    print(f"Acertou! Pontos: {self.pontos}")

    def atualizar(self):
        self.nave.atualizar()

        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_spawn > self.intervalo_spawn:
            self.tempo_ultimo_spawn = agora

            if len(self.asteroides) < self.limite_asteroides:
                quantidade = random.randint(1, 2)

                for _ in range(quantidade):
                    if len(self.asteroides) < self.limite_asteroides:
                        self.asteroides.append(Asteroid(self.largura, self.altura))

        for ast in self.asteroides:
            ast.mover()

        self.checar_colisoes()

    def desenhar(self):
        self.tela.fill((15, 15, 25))
        self.nave.desenhar(self.tela)

        for ast in self.asteroides:
            ast.desenhar(self.tela)

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