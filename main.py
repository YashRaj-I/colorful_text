import pygame
import pygame_gui
import math
import sys

pygame.init()
pygame.display.set_caption("Animated Text Visualizer")

# Constants
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Fonts
font = pygame.font.Font("freesansbold.ttf", 80)
font_small = pygame.font.Font(None, 36)

# Input UI Elements
input_box = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((WIDTH//2 - 200, HEIGHT//2 - 100), (400, 50)),
    manager=manager
)
input_box.set_text("Enter Text Here")

animation_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=[
        "Water Wave Text Animation",
        "Cool Text Effect",
        "Color Text Animation",
        "Disappearing Text Animation",
        "Text + Background Animation"
    ],
    starting_option="Text + Background Animation",
    relative_rect=pygame.Rect((WIDTH//2 - 200, HEIGHT//2 - 30), (400, 50)),
    manager=manager
)

play_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH//2 - 75, HEIGHT//2 + 50), (150, 50)),
    text='Play Animation',
    manager=manager
)

# State
user_text = "Enter Text Here"
selected_animation = "Text + Background Animation"
show_ui = True
paused = False

# Draw Effects
def draw_water_wave(text, base_y, time):
    spacing = 60
    for i, char in enumerate(text):
        # Calculate wave offset
        offset = math.sin(time * 0.005 + i * 0.5) * 30
        y_offset = int(20 * math.sin(time * 0.005))
        
        # Calculate color cycling
        r = int(127 + 128 * math.sin(time * 0.004 + i * 0.2))
        g = int(127 + 128 * math.sin(time * 0.004 + i * 0.2 + 2))
        b = int(127 + 128 * math.sin(time * 0.004 + i * 0.2 + 4))
        char_color = (r, g, b)
        
        # Render character with current color
        char_surf = font.render(char, True, char_color)
        
        # Position calculation
        x_pos = WIDTH//2 - len(text)*spacing//2 + i*spacing
        y_pos = base_y + offset + y_offset
        screen.blit(char_surf, (x_pos, y_pos))

def draw_cool_glow_bounce(text, time):
    r = int(127 + 128 * math.sin(time * 0.004))
    g = int(127 + 128 * math.sin(time * 0.004 + 2))
    b = int(127 + 128 * math.sin(time * 0.004 + 4))
    y_offset = int(20 * math.sin(time * 0.005))
    glow_color = (r, g, b)
    glow = font.render(text, True, glow_color)
    screen.blit(glow, (WIDTH//2 - glow.get_width()//2, HEIGHT//2 - glow.get_height()//2 + y_offset))

def draw_Color_text(text, time):
    # Calculate color cycling (similar to water wave effect)
    r = int(127 + 128 * math.sin(time * 0.004))
    g = int(127 + 128 * math.sin(time * 0.004 + 2))
    b = int(127 + 128 * math.sin(time * 0.004 + 4))
    text_color = (r, g, b)
    
    # Render normal and flipped versions
    normal_surface = font.render(text, True, text_color)
    
    
    # Calculate blend amount with smoother transition
    blend = (math.sin(time * 0.005) + 1) / 2  # Range 0-1
    
    # Create transparent surface for compositing
    surface = pygame.Surface(normal_surface.get_size(), pygame.SRCALPHA)
    
    # Draw normal text (full opacity)
    surface.blit(normal_surface, (0, 0))
    
    
    # Optional: Add glow effect
    glow_color = (r//2, g//2, b//2)  # Dimmer version of main color
    glow_surface = font.render(text, True, glow_color)
    for offset in [(-1,-1), (1,-1), (-1,1), (1,1)]:  # Simple glow effect
        screen.blit(glow_surface, 
                   (WIDTH//2 - surface.get_width()//2 + offset[0], 
                    HEIGHT//2 - surface.get_height()//2 + offset[1]))
    
    # Draw the composed text
    screen.blit(surface, 
               (WIDTH//2 - surface.get_width()//2, 
                HEIGHT//2 - surface.get_height()//2))

def draw_disappearing_text(text, time):
    # Calculate color cycling (same as water wave and flip text)
    r = int(127 + 128 * math.sin(time * 0.004))
    g = int(127 + 128 * math.sin(time * 0.004 + 2))
    b = int(127 + 128 * math.sin(time * 0.004 + 4))
    text_color = (r, g, b)
    
    # Smoother alpha transition (0-255 range)
    alpha = int((math.sin(time * 0.005) + 1) * 127.5)  # Now goes 0-255
    
    # Render text with current color
    surface = font.render(text, True, text_color)
    surface.set_alpha(alpha)
    
    # Optional glow effect (dimmer version of main color)
    if alpha > 30:  # Only show glow when text is somewhat visible
        glow_alpha = min(alpha // 2, 100)  # Softer glow
        glow_color = (r//2, g//2, b//2)
        glow_surface = font.render(text, True, glow_color)
        glow_surface.set_alpha(glow_alpha)
        
        # Draw glow offset in multiple directions
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            screen.blit(glow_surface, 
                       (WIDTH//2 - surface.get_width()//2 + dx * 2, 
                        HEIGHT//2 - surface.get_height()//2 + dy * 2))
    
    # Draw main text
    screen.blit(surface, 
               (WIDTH//2 - surface.get_width()//2, 
                HEIGHT//2 - surface.get_height()//2))

def draw_text_with_background(text, time):
    bg_r = int(127 + 128 * math.sin(time * 0.002))
    bg_g = int(127 + 128 * math.sin(time * 0.002 + 2))
    bg_b = int(127 + 128 * math.sin(time * 0.002 + 4))
    screen.fill((bg_r, bg_g, bg_b))
    surface = font.render(text, True, (0, 0, 0))
    screen.blit(surface, (WIDTH//2 - surface.get_width()//2, HEIGHT//2 - surface.get_height()//2))

def show_exit_hint():
    label = font_small.render("Press ESC to return", True, (180, 180, 180))
    screen.blit(label, (WIDTH - label.get_width() - 20, HEIGHT - 40))

# Animation Loop
def run_animation_loop():
    global show_ui, paused
    show_ui = False
    animation_running = True
    paused = False

    while animation_running:
        time_ms = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    animation_running = False
                    show_ui = True
                elif event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            if selected_animation != "Text + Background Animation":
                screen.fill("black")

            if selected_animation == "Water Wave Text Animation":
                draw_water_wave(user_text, HEIGHT // 2, time_ms)
            elif selected_animation == "Cool Text Effect":
                draw_cool_glow_bounce(user_text, time_ms)
            elif selected_animation == "Color Text Animation":
                draw_Color_text(user_text, time_ms)
            elif selected_animation == "Disappearing Text Animation":
                draw_disappearing_text(user_text, time_ms)
            elif selected_animation == "Text + Background Animation":
                draw_text_with_background(user_text, time_ms)

            show_exit_hint()
            pygame.display.flip()
        clock.tick(60)

# Main UI Loop
running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if show_ui:
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_element == input_box:
                user_text = input_box.get_text()

            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == animation_dropdown:
                selected_animation = event.text

            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == play_button:
                user_text = input_box.get_text()
                run_animation_loop()

            manager.process_events(event)

    if show_ui:
        screen.fill("black")
        manager.update(time_delta)
        manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
