#simple fractal tree with pygame
import pygame
import pygame_gui
import math
import colorsys

pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

camera_x, camera_y = 0, 0
panning = False
last_mouse_pos = (0, 0)

N = 5
LENGTH = 50
INITIAL_ANGLE = -math.pi / 2
ROTATION = -math.pi/4

slider_n = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(10, 10, 200, 20),
    start_value=N,
    value_range=(1, 15),
    manager=manager
)

slider_length = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(10, 40, 200, 20),
    start_value=LENGTH,
    value_range=(1, 200),
    manager=manager
)

slider_angle = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(10, 70, 200, 20),
    start_value=math.degrees(INITIAL_ANGLE),
    value_range=(-180, 180),
    manager=manager
)

slider_rotation = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(10, 100, 200, 20),
    start_value=math.degrees(ROTATION),
    value_range=(-180, 180),
    manager=manager
)


def end_coordinates(start_point, length, angle):
    x = start_point[0] + length * math.cos(angle)
    y = start_point[1] + length * math.sin(angle)
    return (x, y)


def n_to_rainbow(n, max_n, saturation=1.0, value=0.8):
    hue = (n / max_n) % 1
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return (int(r * 255), int(g * 255), int(b * 255))


def draw_branch(start_point, angle, n, length, max_n, rotation):
    if n <= 0:
        return
    
    angle1 = angle - rotation 
    angle2 = angle + rotation 
    
    end_point1 = end_coordinates(start_point, math.pow(n,1.5) * length, angle1)
    end_point2 = end_coordinates(start_point, math.pow(n,1.5) * length, angle2)

    color1 = n_to_rainbow(n, max_n)
    color2 = n_to_rainbow(n + 0.2, max_n)  # Offset for variation
    
    screen_start = (start_point[0] + camera_x, start_point[1] + camera_y)
    screen_end1 = (end_point1[0] + camera_x, end_point1[1] + camera_y)
    screen_end2 = (end_point2[0] + camera_x, end_point2[1] + camera_y)
     
    pygame.draw.line(screen, color1, screen_start, screen_end1, max(1, n))
    pygame.draw.line(screen, color2, screen_start, screen_end2, max(1, n))
    
    draw_branch(end_point1, angle1, n-1, length, max_n, rotation)
    draw_branch(end_point2, angle2, n-1, length, max_n, rotation)

running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Process UI events first
        manager.process_events(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check if clicking on any slider
                mouse_on_ui = any(s.rect.collidepoint(event.pos) 
                                for s in [slider_n, slider_length, slider_angle, slider_rotation])
                if not mouse_on_ui:
                    panning = True
                    last_mouse_pos = event.pos
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                panning = False
        
        elif event.type == pygame.MOUSEMOTION:
            if panning:
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]
                camera_x += dx
                camera_y += dy
                last_mouse_pos = event.pos
        
        elif event.type == pygame.MOUSEWHEEL:
            LENGTH = max(1, min(200, LENGTH + event.y * 5))
            slider_length.set_current_value(LENGTH)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                N = max(1, N - 1)
                slider_n.set_current_value(N)
            elif event.key == pygame.K_RIGHT:
                N = min(10, N + 1) 
                slider_n.set_current_value(N)
            elif event.key == pygame.K_DOWN:
                ROTATION = ROTATION - math.pi/180
                slider_rotation.set_current_value(ROTATION)
            elif event.key == pygame.K_UP:
                ROTATION = ROTATION + math.pi/180 
                slider_rotation.set_current_value(ROTATION)


        # Update variables from sliders
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == slider_n:
                N = int(slider_n.get_current_value())
            elif event.ui_element == slider_length:
                LENGTH = slider_length.get_current_value()
            elif event.ui_element == slider_angle:
                INITIAL_ANGLE = math.radians(slider_angle.get_current_value())
            elif event.ui_element == slider_rotation:
                ROTATION = math.radians(slider_rotation.get_current_value())

    
    manager.update(time_delta)
    
    screen.fill((0, 0, 0))
    
    start_point = (WIDTH // 2, HEIGHT // 2)
    draw_branch(start_point, INITIAL_ANGLE, N, LENGTH, N, ROTATION)
    
    # Draw UI
    manager.draw_ui(screen)
    
    # Draw labels
    font = pygame.font.Font(None, 24)
    n_text = font.render(f'N: {N}', True, (255, 255, 255))
    length_text = font.render(f'Length: {int(LENGTH)}', True, (255, 255, 255))
    angle_text = font.render(f'Angle: {int(math.degrees(INITIAL_ANGLE))}°', True, (255, 255, 255))
    rotation_text = font.render(f'Rotation: {int(math.degrees(ROTATION))}°', True, (255, 255, 255))
    screen.blit(n_text, (220, 10))
    screen.blit(length_text, (220, 40))
    screen.blit(angle_text, (220, 70))
    screen.blit(rotation_text, (220, 100))
    
    pygame.display.flip()

pygame.quit()
