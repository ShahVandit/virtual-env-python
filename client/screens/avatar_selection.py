# avatar_selection.py
import pygame
import os
SCREEN_WIDTH,SCREEN_HEIGHT=800, 600
class AvatarSelectionScreen:
    def __init__(self, screen, room_name):
        self.screen = screen
        self.room_name = room_name
        self.font = pygame.font.Font(None, 36)
        self.username = ''
        self.done = False
        self.active = False
        self.avatars = []  # Will hold tuples of (Surface, Rect, name)
        self.selected_avatar_index = None
        self.username_input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color_button = pygame.Color('purple')
        self.button = pygame.Rect(SCREEN_WIDTH // 2 + 110, SCREEN_HEIGHT // 2, 100, 40)
        self.enter_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200, 200, 50)
        self.button_font = pygame.font.Font(None, 36)
        self.button_text = "Enter Room"
        self.color = self.color_inactive
        self.load_avatars()

    def load_avatars(self):
        # Load avatar images and define their positions
        avatars_dir="assets\\images\\avatars"
        avatar_files = [f for f in os.listdir(avatars_dir) if f.endswith('.png')]
        avatar_spacing = 100  # Space between avatars
        total_width = (len(avatar_files) - 1) * avatar_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        avatar_files = [f for f in os.listdir(avatars_dir) if f.endswith('.png')]
        # Load avatar images and define their positions
        # avatar_names = ['doux_preview', 'mort_preview']
        for idx, file in enumerate(avatar_files):
            image_path = os.path.join(avatars_dir, file)
            image = pygame.image.load(image_path)
            image_rect = image.get_rect(center=(start_x + idx * avatar_spacing, SCREEN_HEIGHT // 2))
            self.avatars.append((image, image_rect, file[:-4]))

    def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if an avatar image was clicked
                for idx, (avatar_img, avatar_rect, _) in enumerate(self.avatars):
                    if avatar_rect.collidepoint(event.pos):
                        self.selected_avatar_index = idx

                # Check if the username input box was clicked
                if self.username_input_box.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        if self.selected_avatar_index is not None and self.username:
                            self.done = True  # Proceed to the virtual environment
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        self.username += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the "Enter Room" button was clicked
                if self.enter_button.collidepoint(event.pos) and self.selected_avatar_index is not None and self.username:
                    self.done = True  # Proceed to the virtual environment

    def draw(self):
        self.screen.fill((255, 255, 255))  # Clear screen

        # Draw the room name
        room_text_surf = self.font.render(f"Room Name: {self.room_name}", True, (0, 0, 0))
        room_text_rect = room_text_surf.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(room_text_surf, room_text_rect)

        # Draw avatars and highlight the selected one
        for idx, (avatar_img, avatar_rect, _) in enumerate(self.avatars):
            self.screen.blit(avatar_img, avatar_rect)
            if idx == self.selected_avatar_index:
                # Draw a rectangle around the selected avatar
                pygame.draw.rect(self.screen, (0, 255, 0), avatar_rect, 2)

        # Draw the username input box
        input_box_color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(self.screen, input_box_color, self.username_input_box, 2)
        username_surf = self.font.render(self.username, True, (0, 0, 0))
        self.screen.blit(username_surf, (self.username_input_box.x + 5, self.username_input_box.y + 5))        
        pygame.draw.rect(self.screen, (100, 100, 255), self.enter_button)
        enter_text_surface = self.button_font.render(self.button_text, True, (255, 255, 255))
        enter_text_rect = enter_text_surface.get_rect(center=self.enter_button.center)
        self.screen.blit(enter_text_surface, enter_text_rect)
    def update(self):
        # Update logic for avatar selection could go here
        pass

    def get_selected_avatar_image(self):
        # Return the image of the selected avatar
        if self.selected_avatar_index is not None:
            return self.avatars[self.selected_avatar_index][0]  # The first element of the tuple is the image
        else:
            return None  # No avatar was selected
    def is_done(self):
        return self.done

    def get_selected_avatar(self):
        return self.selected_avatar

    def get_username(self):
        return self.username
