# avatar_selection.py
import pygame
import os
SCREEN_WIDTH,SCREEN_HEIGHT=800, 600
class AvatarSelectionScreen:
    def __init__(self, screen, room_name, session_id):
        self.screen = screen
        self.room_name = room_name
        self.font = pygame.font.Font(None, 36)
        self.done = False
        self.active = False
        self.avatars = []
        self.selected_avatar_index = None
        self.user_name=""
        self.session_id=session_id
        self.user_name_input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50)
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

                # Check if the user_name input box was clicked
                if self.user_name_input_box.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        if self.selected_avatar_index is not None and self.user_name:
                            self.done = True  # Proceed to the virtual environment
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_name = self.user_name[:-1]
                    else:
                        self.user_name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the "Enter Room" button was clicked
                if self.enter_button.collidepoint(event.pos) and self.selected_avatar_index is not None and self.user_name:
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

        # Draw the user_name input box
        input_box_color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(self.screen, input_box_color, self.user_name_input_box, 2)
        user_name_surf = self.font.render(self.user_name, True, (0, 0, 0))
        self.screen.blit(user_name_surf, (self.user_name_input_box.x + 5, self.user_name_input_box.y + 5))        
        pygame.draw.rect(self.screen, (100, 100, 255), self.enter_button)
        enter_text_surface = self.button_font.render(self.button_text, True, (255, 255, 255))
        enter_text_rect = enter_text_surface.get_rect(center=self.enter_button.center)
        self.screen.blit(enter_text_surface, enter_text_rect)
    def update(self):
        # Update logic for avatar selection could go here
        pass
    def get_session_id(self):
        return self.session_id
    def get_selected_image(self):
        """Return the path of the selected avatar."""
        if self.selected_avatar_index is not None and self.selected_avatar_index < len(self.avatars):
            return self.avatars[self.selected_avatar_index][2]  # Return the path
        return None
    def get_room_name(self):
        return self.room_name
    def is_done(self):
        return self.done

    def select_avatar(self, avatar_id):
        """Select an avatar by its ID."""
        if avatar_id in self.avatars:
            self.selected_avatar_id = avatar_id


    def get_user_name(self):
        return self.user_name
