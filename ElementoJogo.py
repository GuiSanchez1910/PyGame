import pygame

class ElementoJogo:
    """Classe base para todos os objetos do jogo."""
    def __init__(self, x, y, largura, altura, cor=(255, 255, 255), velocidade=5):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = cor
        self.velocidade = velocidade

    def mover(self):
        """Método de movimentação a ser sobrescrito ou estendido pelas subclasses."""
        pass

    def desenhar(self, tela):
        """Desenho padrão (retângulo) caso a subclasse não sobrescreva."""
        pygame.draw.rect(tela, self.cor, self.rect)