import pygame
import math
pygame.init()

# Window dimensions
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
circle_radius = 50

speaker_pos = [200,200]
speaker_image = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\client\\public\\boombox.png') 
speaker_image = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\client\\public\\boombox.png') 
pygame.mixer.music.load("C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\client\\public\\disco.mp3")
pygame.mixer.music.play(-1)  # -1 for infinite loop
pygame.mixer.music.set_volume(0)  # Start with music muted

def calculate_pan_and_volume(player_pos, source_pos, max_distance):
    """
    Calculate stereo panning and volume attenuation based on distance and angle.
    :param player_pos: Tuple (x, y) position of the player.
    :param source_pos: Tuple (x, y) position of the sound source.
    :param max_distance: Maximum distance for hearing.
    :return: Tuple (left_volume, right_volume) for stereo panning.
    """
    # Calculate distance and angle
    dx = source_pos[0] - player_pos[0]
    dy = source_pos[1] - player_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    angle = math.atan2(dy, dx)
    
    # Simple volume attenuation based on distance
    volume = max(0, 1 - distance / max_distance)
    
    # Stereo panning based on angle
    # Assuming right is 0 radians, and left is Pi radians
    pan = (math.cos(angle) + 1) / 2  # Normalize to 0 (left) to 1 (right)
    left_volume = volume * (1 - pan)
    right_volume = volume * pan
    
    return left_volume, right_volume

def calculate_distance_and_angle(pos1, pos2):
    distance = math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)
    angle_radians = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])
    angle_degrees = math.degrees(angle_radians)
    return distance, angle_degrees

def is_within_speaker_range(player_pos, speaker_pos, range_radius):
    return math.sqrt((player_pos[0] - speaker_pos[0])**2 + (player_pos[1] - speaker_pos[1])**2) <= speaker_range_radius


# Set the title of the window
pygame.display.set_caption('Virtual Playground')
player1_image = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\project\\virtual-env-python\\client\\public\\doux_preview.png')
player2_image = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\client\\public\\mort_preview.png')
pygame.mixer.init() 
pygame.font.init()  # Initialize the font module
font = pygame.font.Font(None, 36)

# Initialize player positions
player1_pos = [100, 100]  # Example starting position for player 1
player2_pos = [200, 100]  # Example starting position for player 2
left_volume, right_volume = calculate_pan_and_volume(player1_pos, player2_pos, 100)
# channel = sound.play(-1)  # Loop indefinitely
# channel.set_volume(left_volume, right_volume)

# Load and scale the background image
background_image = pygame.image.load('public/map.png')  # Ensure this path is correct
background_image = pygame.transform.scale(background_image, (window_width, window_height))
speaker_range_radius = 150 

music_playing = False
last_toggler = None  # 'player1' or 'player2'
# Main game loop
running = True
while running:
    toggled_this_frame = False  # Add a flag to prevent multiple toggles in one frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Get pressed keys
    keys = pygame.key.get_pressed()
    
    # Player 1 movement with arrow keys
    if keys[pygame.K_LEFT]:
        player1_pos[0] -= 1
    if keys[pygame.K_RIGHT]:
        player1_pos[0] += 1
    if keys[pygame.K_UP]:
        player1_pos[1] -= 1
    if keys[pygame.K_DOWN]:
        player1_pos[1] += 1

    # Player 2 movement with WASD keys
    if keys[pygame.K_a]:
        player2_pos[0] -= 1
    if keys[pygame.K_d]:
        player2_pos[0] += 1
    if keys[pygame.K_w]:
        player2_pos[1] -= 1
    if keys[pygame.K_s]:
        player2_pos[1] += 1

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw players
    screen.blit(player1_image, player1_pos)
    screen.blit(player2_image, player2_pos)
    # Draw speaker
    screen.blit(speaker_image, speaker_pos)
    pygame.draw.circle(screen, (100, 100, 100), speaker_pos, speaker_range_radius, 1)  # Draw range circle
    player1_in_range = is_within_speaker_range(player1_pos, speaker_pos, speaker_range_radius)
    player2_in_range = is_within_speaker_range(player2_pos, speaker_pos, speaker_range_radius)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t and (player1_in_range or player2_in_range) and not toggled_this_frame:
                toggler = 'player1' if player1_in_range else 'player2'
                # Toggle music playing state if the same player toggles or if it's the first toggle
                if last_toggler is None or last_toggler == toggler:
                    music_playing = not music_playing
                    last_toggler = toggler if music_playing else None
                    toggled_this_frame = True  # Ensure it doesn't toggle again in the same frame

    # Volume adjustment logic remains the same and can follow here
    if player1_in_range or player2_in_range:
        pygame.mixer.music.set_volume(1.0 if music_playing else 0)
    else:
        pygame.mixer.music.set_volume(0)
    if music_playing and last_toggler is not None:
        player_name_text = font.render(last_toggler + " is playing the music", True, (255, 255, 255))
        screen.blit(player_name_text, (10, 10))  # Position the text at the top-left corner
    pygame.draw.circle(screen, (255, 0, 0), player1_pos, circle_radius, 2)  # Red circle for player 1
    pygame.draw.circle(screen, (0, 0, 255), player2_pos, circle_radius, 2)  # Blue circle for player 2

    distance, angle = calculate_distance_and_angle(player1_pos, player2_pos)
    print(f"Distance: {distance:.2f}, Angle: {angle:.2f} degrees") 

    pygame.display.flip()


# pygame.quit()
# sys.exit()

# Load player images
pygame.quit()
