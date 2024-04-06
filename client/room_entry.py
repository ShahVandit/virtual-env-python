# room_entry.py
import pygame
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class RoomEntryScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 40)
        self.button = pygame.Rect(SCREEN_WIDTH // 2 + 110, SCREEN_HEIGHT // 2, 100, 40)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color_button = pygame.Color('purple')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.done = False
        self.title_surf = self.font.render('Welcome to the virtual environment', True, pygame.Color('black'))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = True
            elif self.button.collidepoint(event.pos):
                self.done = True  # User is trying to submit the room name
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.done = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def update(self):
        # No update logic for the room entry
        pass

    def draw(self):
        # Draw title
        self.screen.blit(self.title_surf, (SCREEN_WIDTH // 2 - self.title_surf.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        
        # Render the text.
        txt_surface = self.font.render(self.text, True, self.color)
        
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        self.input_box.w = width
        
        # Draw the text box.
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
        self.screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        
        # Draw the button.
        btn_text = self.font.render('ENTER ROOM', True, pygame.Color('white'))
        pygame.draw.rect(self.screen, self.color_button, self.button)
        self.screen.blit(btn_text, (self.button.x+5, self.button.y+5))

    def is_done(self):
        return self.done
    
    def get_room_name(self):
        return self.text
