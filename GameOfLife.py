import pygame
import numpy as np

# Pygame start 
pygame.init()

# display size
win_width = 800
win_height = 800
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Game of Life')

# cell size
cell_size = 10 # cell number
cols, rows = win_width // cell_size, win_height // cell_size

# cell grille
grid = np.zeros((cols, rows))

# colors
black = (0, 0, 0)
white = (255, 255, 255)
highlight_color = (255, 0, 0)  # click cell color (red)
button_color = (0, 255, 0)  # Start button color (green)
button_hover_color = (0, 200, 0)  # Button above color
stop_button_color = (255, 0, 0)  # Stop button color (red)
stop_button_hover_color = (200, 0, 0)  # Stop button above color 
zoom_in_botton_rect = (210, 10, 100, 40) #zoom button

# fps settings
clock = pygame.time.Clock()
fps = 10

# game situation
running = False

# button settings
start_button_rect = pygame.Rect(win_width // 2 - 110, win_height - 50, 100, 40)
stop_button_rect = pygame.Rect(win_width // 2 + 10, win_height - 50, 100, 40)

# slider variables
zoom_slider_rect = pygame.Rect(650, 10, 140, 20)
speed_slider_rect = pygame.Rect(650, 40, 140, 20)
zoom_slider_value = 18 # default cell size
speed_slider_value = 10 # default fps
zoom_dragging = False
speed_dragging = False

# slider function
def draw_slider(win, rect, value, max_value):
    pygame.draw.rect(win, white, rect, 2) # slider background
    fill_rect = rect.copy()
    fill_rect.width = rect.width * (value / max_value)
    pygame.draw.rect(win, white, fill_rect) # filled part 

# slider function to call
def draw_sliders(win):
    draw_slider(win, zoom_slider_rect, zoom_slider_value, 40)
    draw_slider(win, speed_slider_rect, speed_slider_value, 30)

def update_slider_value(x_pos, rect, max_value):
    relative_x = x_pos - rect.x
    value = max(0, min(max_value, (relative_x / rect.width) * max_value))
    return value

def handle_slider_event(event, dragging, rect, value, max_value):
    if event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(event.pos):
        dragging = True 
    elif event.type == pygame.MOUSEMOTION and dragging:
        value = update_slider_value(event.pos[0], rect, max_value)
    elif event.type == pygame.MOUSEBUTTONUP:
        dragging = False
    return dragging, value
    
# cells 
def draw_grid(win, grid):
    for x in range(cols):
        for y in range(rows):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            color = white if grid[x, y] == 1 else black
            pygame.draw.rect(win, color, rect)
            pygame.draw.rect(win, (128, 128, 128), rect, 1) # cell border color  

def update_grid(grid):
    new_grid = grid.copy()
    for x in range(cols):
        for y in range(rows):
            num_neighbors = np.sum(grid[x-1:x+2, y-1:y+2]) - grid[x, y]
            if grid[x, y] == 1:
                if num_neighbors < 2 or num_neighbors > 3:
                    new_grid[x, y] = 0
            else:
                if num_neighbors == 3:
                    new_grid[x, y] = 1
    return new_grid

def handle_click(grid, pos):
    x, y = pos 
    col = x // cell_size
    row = y // cell_size
    if 0 <= col < cols and 0 <= row < rows:
        grid[col, row] = 1 - grid[col, row] # cell start/stop

def draw_buttons(win):
    mouse_pos = pygame.mouse.get_pos()
    
    start_color = button_hover_color if start_button_rect.collidepoint(mouse_pos) else button_color
    pygame.draw.rect(win, start_color, start_button_rect)
    font = pygame.font.SysFont(None, 24)
    start_text = font.render('Start', True, black)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    win.blit(start_text, start_text_rect)
    
    stop_color = stop_button_hover_color if stop_button_rect.collidepoint(mouse_pos) else stop_button_color
    pygame.draw.rect(win, stop_color, stop_button_rect)
    stop_text = font.render('Stop', True, black)
    stop_text_rect = stop_text.get_rect(center=stop_button_rect.center)
    win.blit(stop_text, stop_text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                running = True
            elif stop_button_rect.collidepoint(event.pos):
                running = False
            else:
                handle_click(grid, event.pos)
        zoom_dragging, zoom_slider_value = handle_slider_event(event, zoom_dragging, zoom_slider_rect, zoom_slider_value, 40)
        speed_dragging, speed_slider_value = handle_slider_event(event, speed_dragging, speed_slider_rect, speed_slider_value, 30)

    if running:
        grid = update_grid(grid)
    
    cell_size = int(zoom_slider_value)
    fps = int(speed_slider_value)

    win.fill(black)
    draw_grid(win, grid)
    draw_buttons(win)
    draw_sliders(win)
    pygame.display.update()
    clock.tick(fps)
