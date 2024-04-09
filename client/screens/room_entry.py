import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class RoomEntryScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 40)
        self.button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 40)  # Adjusted for better placement
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color_button_inactive = pygame.Color('purple')
        self.color_button_hover = pygame.Color('violet')
        self.color_button = self.color_button_inactive  # Initial button color
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.done = False
        self.title_surf = self.font.render('Welcome to the Virtual Environment', True, pygame.Color('black'))
        self.mouse_over_button = False  # To track if the mouse is over the button

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active  # Toggle active state
            elif self.button.collidepoint(event.pos) and self.text.strip():
                self.done = True  # Proceed only if there's some text
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.MOUSEMOTION:
            # Change button color on hover
            self.mouse_over_button = self.button.collidepoint(event.pos)
            self.color_button = self.color_button_hover if self.mouse_over_button else self.color_button_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN and self.text.strip():
                self.done = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def update(self):
        pass  # No specific update logic needed for the room entry

    def draw(self):
        # Draw the title centered
        self.screen.blit(self.title_surf, (SCREEN_WIDTH // 2 - self.title_surf.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        
        # Render the text
        txt_surface = self.font.render(self.text, True, self.color)
        width = max(200, txt_surface.get_width()+10)
        self.input_box.w = width
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
        self.screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        
        # Draw the button and center the button text
        btn_text_surf = self.font.render('Enter Room', True, pygame.Color('white'))
        pygame.draw.rect(self.screen, self.color_button, self.button)
        self.screen.blit(btn_text_surf, (self.button.x + (self.button.width - btn_text_surf.get_width()) // 2, self.button.y + (self.button.height - btn_text_surf.get_height()) // 2))

    def error_display(self, error_message):
        return error_message
    def is_done(self):
        return self.done

    def get_room_name(self):
        return self.text.strip()  # Return stripped text to handle accidental spaces
