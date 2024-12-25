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


clock = pygame.time.Clock()

#--- HELPER FUNCTIONS
def scale_button(button, scaling_factor):
    btn_width, btn_height = button.get_size()
    btn_new_width = int(WIDTH * scaling_factor)
    btn_new_height = int(btn_new_width * btn_height / btn_width)
    return pygame.transform.scale(button, (btn_new_width, btn_new_height))

#---GAME FUNCTIONS

def start_game_screen():
    print("Starting game screen...")

    # Screen dimensions
    SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

    # Paths to assets
    logo_path = os.path.join('assets', 'images', 'logo.png')
    torch_path = os.path.join('assets', 'gifs', 'torch.gif')
    start_btn_path = os.path.join('assets', 'images', 'start_btn.png')
    about_us_btn_path = os.path.join('assets', 'images', 'about_us_btn.png')
    exit_btn_path = os.path.join('assets', 'images', 'exit_btn.png')
    theme_sound_path = os.path.join('assets', 'sounds', 'theme_sound.mp3')

    # Load assets
    logo = pygame.image.load(logo_path)
    gif = Image.open(torch_path)
    start_btn = pygame.image.load(start_btn_path)
    about_us_btn = pygame.image.load(about_us_btn_path)
    exit_btn = pygame.image.load(exit_btn_path)


    big_frames = []

    big_torch_size = (150, 150)

    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_image = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_image.tobytes(), frame_image.size, frame_image.mode
        )
        big_frames.append(pygame.transform.scale(pygame_image, big_torch_size))

    start_btn = scale_button(start_btn, 0.12)
    about_us_btn = scale_button(about_us_btn, 0.12)
    exit_btn = scale_button(exit_btn, 0.12)


    logo_width, logo_height = logo.get_size()
    logo_x = (SCREEN_WIDTH - logo_width) // 2
    logo_y = (SCREEN_HEIGHT - logo_height) // 2.5


    torch_width, torch_height = big_frames[0].get_size()
    torch_left_x = logo_x - torch_width - 50
    torch_left_y = logo_y + (logo_height - torch_height) // 2
    torch_right_x = logo_x + logo_width + 50
    torch_right_y = torch_left_y

    button_spacing = 40
    btn_width, btn_height = start_btn.get_size()

    start_btn_x = (SCREEN_WIDTH - (3 * btn_width + 2 * button_spacing)) // 2
    start_btn_y = logo_y + logo_height + 110

    about_us_btn_x = start_btn_x + btn_width + button_spacing
    about_us_btn_y = start_btn_y

    exit_btn_x = about_us_btn_x + btn_width + button_spacing
    exit_btn_y = start_btn_y


    frame_index = 0
    frame_delay = 100
    last_update_time = pygame.time.get_ticks()


    pygame.mixer.music.load(theme_sound_path)
    pygame.mixer.music.play(loops=-1, start=0.0)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(start_btn_x, start_btn_y, btn_width, btn_height).collidepoint(mouse_pos):
                    print("Start button clicked! Transitioning to level selection screen...")
                    level_selection_screen(big_frames, level_status={i: "locked" for i in range(1, 11)})
                    return
                if pygame.Rect(about_us_btn_x, about_us_btn_y, btn_width, btn_height).collidepoint(mouse_pos):
                    print("About Us button clicked! Transitioning to About Us screen...")
                    about_us_screen()
                    return
                if pygame.Rect(exit_btn_x, exit_btn_y, btn_width, btn_height).collidepoint(mouse_pos):
                    print("Exit button clicked! Exiting game...")
                    pygame.quit()
                    return


        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > frame_delay:
            frame_index = (frame_index + 1) % len(big_frames)
            last_update_time = current_time

        screen.fill(BLACK)

        screen.blit(big_frames[frame_index], (torch_left_x, torch_left_y))
        screen.blit(big_frames[frame_index], (torch_right_x, torch_right_y))

        screen.blit(logo, (logo_x, logo_y))

        screen.blit(start_btn, (start_btn_x, start_btn_y))
        screen.blit(about_us_btn, (about_us_btn_x, about_us_btn_y))
        screen.blit(exit_btn, (exit_btn_x, exit_btn_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def about_us_screen():
    print("Displaying About Us screen...")

    about_img_path = os.path.join('assets', 'images', 'about1.png')
    back_btn_path = os.path.join('assets', 'images', 'back_btn.png')
    torch_gif_path = os.path.join('assets', 'gifs', 'torch.gif')

    about_img = pygame.image.load(about_img_path)
    back_btn = pygame.image.load(back_btn_path)
    back_btn = scale_button(back_btn, 0.12)

    gif = Image.open(torch_gif_path)
    torch_frames = []

    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_image = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_image.tobytes(), frame_image.size, frame_image.mode
        )
        torch_frames.append(pygame.transform.scale(pygame_image, (150, 150)))

    about_img_width, about_img_height = about_img.get_size()
    about_img_x = (WIDTH - about_img_width) // 2
    about_img_y = (HEIGHT - about_img_height) // 2

    torch_width, torch_height = torch_frames[0].get_size()
    torch_left_x = about_img_x - torch_width - 50
    torch_right_x = about_img_x + about_img_width + 50
    torch_y = about_img_y + (about_img_height - torch_height) // 2

    back_btn_x = (WIDTH - back_btn.get_width()) // 2
    back_btn_y = about_img_y + about_img_height + 50

    frame_index = 0
    frame_delay = 100
    last_update_time = pygame.time.get_ticks()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(back_btn_x, back_btn_y, back_btn.get_width(), back_btn.get_height()).collidepoint(mouse_pos):
                    print("Back button clicked! Returning to start screen...")
                    start_game_screen()
                    return

        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > frame_delay:
            frame_index = (frame_index + 1) % len(torch_frames)
            last_update_time = current_time

        screen.fill(BLACK)

        screen.blit(torch_frames[frame_index], (torch_left_x, torch_y))
        screen.blit(torch_frames[frame_index], (torch_right_x, torch_y))

        screen.blit(about_img, (about_img_x, about_img_y))

        screen.blit(back_btn, (back_btn_x, back_btn_y))

        pygame.display.flip()
        clock.tick(60)


def level_selection_screen(frames, level_status):
    print("Displaying level selection screen...")

    back_button_image = pygame.image.load("assets/images/back_btn.png")

    btn_scaling_factor = 0.12
    btn_width = int(WIDTH * btn_scaling_factor)
    btn_height = int(btn_width * back_button_image.get_height() / back_button_image.get_width())
    back_button_image = pygame.transform.scale(back_button_image, (btn_width, btn_height))

    font = pygame.font.Font(None, 64)
    small_font = pygame.font.Font(None, 36)

    rows, cols = 2, 5
    box_width, box_height = 150, 150
    padding = 40

    start_x = (WIDTH - (cols * box_width + (cols - 1) * padding)) // 2
    start_y = (HEIGHT - (rows * box_height + (rows - 1) * padding)) // 2

    level_boxes = []
    for row in range(rows):
        for col in range(cols):
            level = row * cols + col + 1
            x = start_x + col * (box_width + padding)
            y = start_y + row * (box_height + padding)
            rect = pygame.Rect(x, y, box_width, box_height)
            level_boxes.append((level, rect))

    back_button_x = (WIDTH - btn_width) // 2
    back_button_y = start_y + (rows * box_height + (rows - 1) * padding) + 20
    back_button_rect = pygame.Rect(back_button_x, back_button_y, btn_width, btn_height)

    frame_index = 0
    frame_delay = 100
    last_update_time = pygame.time.get_ticks()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit event detected. Exiting level selection...")
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                for level, rect in level_boxes:
                    if rect.collidepoint(mouse_pos) and level_status[level] == "unlocked":
                        print(f"Level {level} clicked!")
                        # show_maze(level, level_status)

                if back_button_rect.collidepoint(mouse_pos):
                    print("Back button clicked! Returning to start screen...")
                    start_game_screen()

        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > frame_delay:
            frame_index = (frame_index + 1) % len(frames)
            last_update_time = current_time

        screen.fill(BLACK)

        for level, rect in level_boxes:
            if level_status[level] == "locked":
                screen.blit(frames[frame_index], rect.topleft)
                color = (128, 128, 128)
            else:
                color = (255, 165, 0) if not rect.collidepoint(mouse_pos) else (255, 200, 0)
                pygame.draw.rect(screen, color, rect, border_radius=10)

            text = font.render(str(level), True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        screen.blit(back_button_image, (back_button_x, back_button_y))

        pygame.display.flip()
        clock.tick(60)








if __name__ == "__main__":
    start_game_screen()
