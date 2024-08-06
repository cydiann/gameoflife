import pygame

class Cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.alive = False
    
    def draw(self, win):
        """
        Çizim fonksiyonu: Hücrenin rengini ve kenar çizgisini çizer.
        """
        rect = pygame.Rect(self.x * self.size, self.y * self.size, self.size, self.size)
        color = (255, 255, 255) if self.alive else (0, 0, 0)  # Canlı hücreler beyaz, ölü hücreler siyah
        pygame.draw.rect(win, color, rect)  # Hücrenin dolgu rengini çiz
        pygame.draw.rect(win, (128, 128, 128), rect, 1)  # Hücrenin kenarlığını gri renkte çiz

    def toggle(self):
        """
        Hücrenin durumunu değiştirir: Canlı ise ölü, ölü ise canlı yapar.
        """
        self.alive = not self.alive
