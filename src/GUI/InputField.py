import pygame as pg


class InputField:
    """adapted from: https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame"""
    COLOR_ACTIVE = 'White'
    COLOR_INACTIVE = 'Grey'

    def __init__(self, x, y, w, h, text=''):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.Rect(x, y, w, h)
        self.color = InputField.COLOR_INACTIVE
        self.text = text
        self.font = pg.font.SysFont("Arial", 14)
        self.txt_surface = self.font.render(text, True, (0, 0, 0))
        self.active = False
        self.final_text = ""

    def handle_event(self, screen, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = InputField.COLOR_ACTIVE if self.active else InputField.COLOR_INACTIVE
            pg.display.update()
        if event.type == pg.KEYDOWN:
            if self.active is True:
                if event.key == pg.K_RETURN:
                    string = self.text
                    self.text = ''
                    self.final_text = string
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, (0, 0, 0))

    def update(self):
        """Method to resize the box if the text is too long."""
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
