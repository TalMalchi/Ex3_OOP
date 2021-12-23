import pygame as pg
from typing import Tuple


class Button:
    """adapted from: https://pythonprogramming.altervista.org/buttons-in-pygame/?doing_wp_cron=1640112829.2162640094757080078125"""
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text, pos: Tuple[int, int], bg=(200, 200, 200)):
        self.x, self.y = pos[0] + 5, pos[1]
        self.font = pg.font.SysFont("Times New Roman", 20)

        """Change the text whe you click"""
        self.text = self.font.render(text, False, pg.Color("Black"))
        self.size = self.text.get_size()
        self.surface = pg.Surface((self.size[0] + 5, self.size[1]))
        self.surface.fill(bg)
        self.surface.blit(self.text, (2.5, 0))
        self.rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, screen) -> None:
        screen.blit(self.surface, (self.x, self.y))

    def click(self, event) -> bool:
        x, y = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False
