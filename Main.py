import random
import pygame
from PIL import Image
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

        bg_original = pygame.image.load("img/rainy.jpg").convert()
        self.bg = pygame.transform.scale(bg_original, (self.largura, self.altura))
        self.bg_y1 = 0
        self.bg_y2 = -self.altura
        self.vel_bg = 2

        self.asteroides = []
        self.limite_asteroides = 5
        self.tempo_ultimo_spawn = pygame.time.get_ticks()
        self.intervalo_spawn = 2000

        # Projétil
        img_tiro_original = pygame.image.load("img/batarang.png").convert_alpha()
        self.imagem_tiro = pygame.transform.scale(img_tiro_original, (20, 50))

        # Gif do Background
        self.frames_bg = []
        gif = Image.open("img/rain.gif")  # Coloque o nome exato do seu arquivo .gif

        try:
            while True:
                # Converte o frame atual para RGBA
                frame_rgba = gif.convert("RGBA")
                # Transforma o frame do Pillow em uma imagem do Pygame
                img_pygame = pygame.image.frombytes(frame_rgba.tobytes(), frame_rgba.size, "RGBA")
                # Redimensiona para o tamanho da tela
                img_pygame = pygame.transform.scale(img_pygame, (self.largura, self.altura))

                self.frames_bg.append(img_pygame)
                # Avança para o próximo frame do GIF
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass  # Chegou no fim do GIF, todos os frames foram carregados!

        self.indice_frame = 0
        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.velocidade_animacao = 80  # milissegundos por frame (diminua para ficar mais rápido, aumente para mais lento)

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

            rect_ast_nave = ast.rect.inflate(-50, -50)

            if self.nave.rect.colliderect(rect_ast_nave):
                self.game_over = True

            rect_ast_tiro = ast.rect.inflate(-20, -20)

            for tiro in self.nave.tiros[:]:
                if tiro.colliderect(rect_ast_tiro):
                    if tiro in self.nave.tiros:
                        self.nave.tiros.remove(tiro)

                    ast.iniciar_status()
                    self.pontos += 1

    def atualizar(self):
        if self.game_over:
            return

        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_frame > self.velocidade_animacao:
            self.tempo_ultimo_frame = agora
            self.indice_frame += 1

            # Volta para o primeiro frame se chegou ao fim (loop infinito)
            if self.indice_frame >= len(self.frames_bg):
                self.indice_frame = 0

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

        imagem_atual = self.frames_bg[self.indice_frame]
        self.tela.blit(imagem_atual, (0, 0))

        self.nave.desenhar(self.tela)

        for ast in self.asteroides:
            ast.desenhar(self.tela)

        # "Carimba" a imagem do tiro em cada projetil da lista de tiros
        for tiro in self.nave.tiros:
            self.tela.blit(self.imagem_tiro, tiro)

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