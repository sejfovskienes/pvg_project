import pygame
import sys
import os
from PIL import Image

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape The Maze")

# Clock for controlling frame rate
clock = pygame.time.Clock()

#--- FUNCTIONS
def start_game_screen():
    print("Starting game screen...")

    # Screen dimensions
    SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

    # Paths to assets
    logo_path = os.path.join('assets', 'images', 'logo.png')
    torch_path = os.path.join('assets', 'gifs', 'torch.gif')
    start_btn_path = os.path.join('assets', 'images', 'start_btn.png')
    theme_sound_path = os.path.join('assets', 'sounds', 'theme_sound.mp3')

    # Load assets
    logo = pygame.image.load(logo_path)
    gif = Image.open(torch_path)
    start_btn = pygame.image.load(start_btn_path)

    # Create torch frames
    big_frames = []
    small_frames = []

    big_torch_size = (150, 150)  # Adjusted for 1920x1080
    small_torch_size = (75, 75)  # Adjusted for 1920x1080

    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_image = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_image.tobytes(), frame_image.size, frame_image.mode
        )
        big_frames.append(pygame.transform.scale(pygame_image, big_torch_size))
        small_frames.append(pygame.transform.scale(pygame_image, small_torch_size))

    # Resize start button
    btn_width, btn_height = start_btn.get_size()
    btn_scaling_factor = 0.12  # Adjusted scaling factor for larger screen
    btn_new_width = int(SCREEN_WIDTH * btn_scaling_factor)
    btn_new_height = int(btn_new_width * btn_height / btn_width)
    start_btn = pygame.transform.scale(start_btn, (btn_new_width, btn_new_height))

    # Position the logo
    logo_width, logo_height = logo.get_size()
    logo_x = (SCREEN_WIDTH - logo_width) // 2
    logo_y = (SCREEN_HEIGHT - logo_height) // 2.5  # Adjusted vertical position for screen

    # Position the torch animations
    torch_width, torch_height = big_frames[0].get_size()
    torch_left_x = logo_x - torch_width - 50  # Adjusted spacing for larger screen
    torch_left_y = logo_y + (logo_height - torch_height) // 2
    torch_right_x = logo_x + logo_width + 50  # Adjusted spacing for larger screen
    torch_right_y = torch_left_y

    # Position the start button
    btn_x = (SCREEN_WIDTH - btn_new_width) // 2
    btn_y = logo_y + logo_height + 110  # Adjusted spacing for start button

    # Animation settings
    frame_index = 0
    frame_delay = 100
    last_update_time = pygame.time.get_ticks()

    # Play theme sound
    pygame.mixer.music.load(theme_sound_path)
    pygame.mixer.music.play(loops=-1, start=0.0)

    # Initialize level status
    level_status = {i: "locked" for i in range(1, 11)}  # Example: 10 levels, all locked initially

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the start button is clicked
                if pygame.Rect(btn_x, btn_y, btn_new_width, btn_new_height).collidepoint(mouse_pos):
                    print("Start button clicked! Transitioning to level selection screen...")
                    level_selection_screen(small_frames, level_status)  # Call level selection screen
                    return  # Exit the start screen and move to level selection screen

        # Update torch animation
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > frame_delay:
            frame_index = (frame_index + 1) % len(big_frames)
            last_update_time = current_time

        # Draw the start screen
        screen.fill(BLACK)

        # Draw torch animations
        screen.blit(big_frames[frame_index], (torch_left_x, torch_left_y))
        screen.blit(big_frames[frame_index], (torch_right_x, torch_right_y))

        # Draw logo
        screen.blit(logo, (logo_x, logo_y))

        # Draw start button
        screen.blit(start_btn, (btn_x, btn_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def level_selection_screen(frames, level_status):
    print("Displaying level selection screen...")

    # Font settings
    font = pygame.font.Font(None, 64)  # Larger font for higher resolution
    small_font = pygame.font.Font(None, 36)  # Smaller font for button text

    # Level box settings
    rows, cols = 2, 5  # 2 rows, 5 columns
    box_width, box_height = 150, 150  # Larger boxes for better visibility
    padding = 40  # Adjusted padding for spacing

    # Calculate starting positions to center the grid
    start_x = (WIDTH - (cols * box_width + (cols - 1) * padding)) // 2
    start_y = (HEIGHT - (rows * box_height + (rows - 1) * padding)) // 2

    # Generate level boxes
    level_boxes = []
    for row in range(rows):
        for col in range(cols):
            level = row * cols + col + 1
            x = start_x + col * (box_width + padding)
            y = start_y + row * (box_height + padding)
            rect = pygame.Rect(x, y, box_width, box_height)
            level_boxes.append((level, rect))

    # Back button settings
    back_button_width, back_button_height = 100, 50
    back_button_x = (WIDTH - back_button_width) // 2  # Center horizontally
    back_button_y = start_y + (rows * box_height + (rows - 1) * padding) + 20  # Position below the level boxes
    back_button = pygame.Surface((back_button_width, back_button_height))
    back_button.fill(RED)
    back_button_text = small_font.render("Back", True, BLACK)
    back_button_text_rect = back_button_text.get_rect(center=back_button.get_rect().center)
    back_button.blit(back_button_text, back_button_text_rect)

    # Animation settings
    frame_index = 0
    frame_delay = 100  # Frame delay for animation
    last_update_time = pygame.time.get_ticks()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit event detected. Exiting level selection...")
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Level button clicks
                for level, rect in level_boxes:
                    if rect.collidepoint(mouse_pos) and level_status[level] == "unlocked":
                        print(f"Level {level} clicked!")
                        # show_maze(level, level_status)

                # Back button click
                if pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height).collidepoint(mouse_pos):
                    print("Back button clicked! Returning to start screen...")
                    start_game_screen()  # Call the start_game_screen function

        # Update torch animation
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > frame_delay:
            frame_index = (frame_index + 1) % len(frames)
            last_update_time = current_time

        # Draw elements
        screen.fill(BLACK)

        # Draw level boxes
        for level, rect in level_boxes:
            if level_status[level] == "locked":
                # Display animated frame for locked levels
                screen.blit(frames[frame_index], rect.topleft)
                color = (128, 128, 128)  # Gray for locked levels
            else:
                # Highlight unlocked levels on hover
                color = (255, 165, 0) if not rect.collidepoint(mouse_pos) else (255, 200, 0)
                pygame.draw.rect(screen, color, rect, border_radius=10)

            # Render level number text
            text = font.render(str(level), True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Draw back button
        screen.blit(back_button, (back_button_x, back_button_y))

        pygame.display.flip()
        clock.tick(60)







if __name__ == "__main__":
    start_game_screen()
