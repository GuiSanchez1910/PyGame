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

        # Fontes do jogo
        self.fonte_placar = pygame.font.SysFont(None, 32)
        self.fonte_titulo = pygame.font.SysFont(None, 72)
        self.fonte_instrucao = pygame.font.SysFont(None, 28)

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.rodando = True
        self.pontos = 0
        self.game_over = False
        

        # Elementos do jogo
        self.nave = Nave(self.largura, self.altura)

        self.asteroides = []
        self.limite_asteroides = 5
        self.tempo_ultimo_spawn = pygame.time.get_ticks()
        self.intervalo_spawn = 2000

    def reiniciar(self):
        self.game_over = False
        self.pontos = 0
        self.nave = Nave(self.largura, self.altura)
        self.asteroides = []
        self.tempo_ultimo_spawn = pygame.time.get_ticks()

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False
                elif self.game_over and evento.key == pygame.K_r:
                    self.reiniciar()

            if not self.game_over:
                self.nave.processar_evento(evento)

    def checar_colisoes(self):
        for ast in self.asteroides[:]:
            if self.nave.rect.colliderect(ast.rect):
                self.game_over = True

            for tiro in self.nave.tiros[:]:
                if tiro.colliderect(ast.rect):
                    if tiro in self.nave.tiros:
                        self.nave.tiros.remove(tiro)

                    ast.iniciar_status()
                    self.pontos += 1

    def atualizar(self):
        if self.game_over:
            return

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

        # Exibe o placar
        texto_pontos = self.fonte_placar.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        self.tela.blit(texto_pontos, (10, 10))

        # Overlay de Game Over
        if self.game_over:
            overlay = pygame.Surface((self.largura, self.altura))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.tela.blit(overlay, (0, 0))

            titulo = self.fonte_titulo.render("GAME OVER", True, (255, 80, 80))
            pontos = self.fonte_placar.render(f"Pontuação Final: {self.pontos}", True, (255, 255, 255))
            instrucao = self.fonte_instrucao.render("R para reiniciar | ESC para sair", True, (200, 200, 200))

            self.tela.blit(titulo, ((self.largura - titulo.get_width()) // 2, 220))
            self.tela.blit(pontos, ((self.largura - pontos.get_width()) // 2, 310))
            self.tela.blit(instrucao, ((self.largura - instrucao.get_width()) // 2, 360))

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