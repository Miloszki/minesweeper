import pygame
import random
from collections import deque 
from buttons import Button

pygame.init()
pygame.font.init()
pygame.display.set_caption("Minesweeper")
TILE_CODES = {
    'hidden': 0,
    'shown': 1,
    'bomb': -1,
    'flag': 2
}

#NUMROWS, NUMCOLS, NUMMINES
DIFFICULTY_LEVELS = {
    'Beginner': (9,9,10),
    'Intermediate': (16,16,40),
    'Expert': (21, 21, 90)
}


TILE_COLOR = (100,100,100)
TEXT_COLOR = (255,100,100)
BG_COLOR = (0,0,0)
WINDOW_SIZE = (1000,1000)
CLICKED_TILE_COLOR = (20,20,20)
FLAGGED_TILE_COLOR = (200,200,0)
NUM_COLORS = {
    -1: (255, 192, 203),  # pink
    0: (255, 255, 255),  # white
    1: (0, 0, 255),      # blue
    2: (0, 128, 0),      # green
    3: (255, 0, 0),      # red
    4: (0, 0, 128),      # navy
    5: (128, 0, 32),     # burgundy
    6: (0, 128, 128),    # teal
    7: (0, 0, 0),        # black
    8: (128, 128, 128)
}

#constants for looping over tile neighbors 
DROWS = [-1,0,1]
DCOLS = DROWS.copy()

FONT = pygame.font.SysFont('Arial', int(WINDOW_SIZE[1]*25/600)) #scaling font for an original height of 600
GAMEOVER_FONT = pygame.font.SysFont('Arial', 70)
screen = pygame.display.set_mode(WINDOW_SIZE)
width, height = screen.get_size()



def draw_menu(window, diff):
    horizontal_offset = width * 0.1
    beginner_button = Button(horizontal_offset, height/2 , 'Beginner')
    intermediate_button = Button(horizontal_offset + width/3, height/2 , 'Intermediate')
    expert_button = Button(horizontal_offset + width*2/3, height/2, 'Expert')
    start_game_button = Button(width/2 , height*2/3, 'Start game')

    if diff is not None:
        if start_game_button.draw(window):
            return diff, True
        
    if beginner_button.draw(window):
        diff = 'Beginner'

    if intermediate_button.draw(window):
        diff = 'Intermediate'

    if expert_button.draw(window):
        diff = 'Expert'

    return diff, False


def get_tile_neighbors(row,col,rows,cols):
    neighbors = []

    for drow_offset in DROWS:
        for dcol_offset in DCOLS:
            if drow_offset == 0 and dcol_offset == 0:
                continue
            drow = row + drow_offset
            dcol = col + dcol_offset
            if 0 <= drow < rows and 0 <= dcol < cols:
                neighbors.append((drow, dcol))

    return neighbors

def create_safearea(start_pos):
    safe_area = set()
    for drow_offset in DROWS:
        for dcol_offset in DCOLS:
            drow = start_pos[0] + drow_offset
            dcol = start_pos[1] + dcol_offset
            if 0 <= drow < NUM_ROWS and 0 <= dcol < NUM_COLS:    
                safe_area.add((drow, dcol))
    return safe_area

def create_grid(rows,cols, mines, start_pos, game_started=False):
    grid = [[0 for _ in range(cols)] for  _ in range(rows)]

    mine_indexes = set()
    if not game_started:
        safe_area = create_safearea(start_pos)

    while len(mine_indexes) < mines:
        row, col = random.randint(0,rows-1), random.randint(0,cols-1)
        pos = row, col

        if (row,col) in safe_area:
            continue
        if pos in mine_indexes:
            continue

        mine_indexes.add(pos)
        grid[row][col] = TILE_CODES['bomb']

    for mine in mine_indexes:
        neighbors = get_tile_neighbors(*mine, rows, cols)
        for r,c in neighbors:
            if grid[r][c] != TILE_CODES['bomb']:
                grid[r][c] += 1

    return grid

def draw(window, field, cover):
    window.fill(BG_COLOR)
    flag = pygame.image.load(r"icons/pixil_flag.png").convert()
    bomb= pygame.image.load(r"icons/pixil_bomb.png").convert()
    
    scaled_flag = pygame.transform.scale(flag,(SIZE,SIZE))
    scaled_bomb = pygame.transform.scale(bomb,(SIZE,SIZE))
    for i, row in enumerate(field):
        x= i*SIZE
        for j, val in enumerate(row):
            y = j * SIZE

            rect = pygame.Rect(x,y,SIZE,SIZE)
            is_covered = cover[i][j] == 0
            is_flagged = cover[i][j] == 2

            if is_covered:
                pygame.draw.rect(screen,TILE_COLOR,rect)
                pygame.draw.rect(screen,'black',rect,2)
                continue
            elif is_flagged:
                pygame.draw.rect(screen,FLAGGED_TILE_COLOR,rect)
                window.blit(scaled_flag,(x,y))
                pygame.draw.rect(screen,'black',rect,2)
                continue
            else:
                pygame.draw.rect(screen,CLICKED_TILE_COLOR,rect)
                pygame.draw.rect(screen,'black',rect,2)

            if val != 0:
                txt = FONT.render(str(val),2,NUM_COLORS[val])
                window.blit(txt,(x + (SIZE/2 -txt.get_width()/2), y + (SIZE/2 - txt.get_height()/2)))
            if val == -1:
                window.blit(scaled_bomb,(x,y))

    pygame.display.update()

def check_gameover(grid,cover):
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if cover[i][j] == 1 and val == -1:


                for i, row in enumerate(grid):
                    for j, val in enumerate(row):
                        if val == -1:
                            cover[i][j] = 1
                draw(screen, grid, cover)
                gameover_txt = GAMEOVER_FONT.render('GAME OVER', 2, 'red')
                screen.blit(gameover_txt, (width / 2 - gameover_txt.get_width() / 2, height / 2 - gameover_txt.get_height() / 2))
                pygame.display.update()
                pygame.time.wait(2000)
                main()

def check_win(grid,cover):
    hidden_tiles = 0
    flagged_tiles = 0

    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            if cover[i][j] == 0:
               hidden_tiles += 1 
            if cover[i][j] == 2:
                flagged_tiles += 1

    important_tiles = hidden_tiles + flagged_tiles
    if important_tiles == NUM_MINES:
        gameover_txt = GAMEOVER_FONT.render('YOU HAVE WON', 2, 'green')
        screen.blit(gameover_txt, (width // 2 - gameover_txt.get_width() // 2, height // 2 - gameover_txt.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        main()               

def grid_bfs(pos, grid, visited_mask):
    q = deque()
    x, y = pos
    ll=[]
    ll.append([(x,y)])
    q.append((x, y))

    while len(q) > 0:
        cell = q.popleft()
        x, y = cell

        if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
            continue
        if visited_mask[x][y]:
            continue

        visited_mask[x][y] = 1
        if grid[x][y] == 0:
            neighbors = []

            for drow_offset in DROWS:
                for dcol_offset in DCOLS:
                    if drow_offset == 0 and dcol_offset == 0:
                        continue
                    drow = x + drow_offset
                    dcol = y + dcol_offset
                    if 0 <= drow < NUM_ROWS and 0 <= dcol < NUM_COLS:
                        if not visited_mask[drow][dcol]:
                            neighbors.append((drow, dcol))

            q.extend(neighbors)
            ll.append(neighbors)

    flat_ll = [x for xs in ll for x in xs]
    return flat_ll

def basic_middle_button(pos,grid, cover_grid):
    x,y = pos
    ca8_neighbors = []
    clicked_tile_val = grid[x][y]
    flags_found = 0

    for drow_offset in DROWS:
        for dcol_offset in DCOLS:
            if drow_offset == 0 and dcol_offset == 0:
                continue
            drow = x + drow_offset
            dcol = y + dcol_offset
            if 0 <= drow < NUM_ROWS and 0 <= dcol < NUM_COLS:
                if cover_grid[drow][dcol] == 2:
                    flags_found += 1

    if flags_found < clicked_tile_val:
        return []

    for drow_offset in DROWS:
        for dcol_offset in DCOLS:
            if drow_offset == 0 and dcol_offset == 0:
                continue
            drow = x + drow_offset
            dcol = y + dcol_offset
            if 0 <= drow < NUM_ROWS and 0 <= dcol < NUM_COLS:
                if cover_grid[drow][dcol] != 2:
                    ca8_neighbors.append((drow, dcol))

    return ca8_neighbors

def get_grid_pos(mouse_pos):
    mx, my = mouse_pos
    row = mx // SIZE
    col = my // SIZE
    return row,col

def middle_click_functionality(row,col,grid,cover_grid):    
    visited_mask = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    list_neighbouring_empty_tiles = grid_bfs((row,col), grid, visited_mask)
    for r,c in list_neighbouring_empty_tiles:
        cover_grid[r][c] = 1

    if grid[row][col] > 0:
        neighbors = basic_middle_button((row,col),grid,cover_grid)
        for r,c in neighbors:
            cover_grid[r][c] = 1
            if grid[r][c] == 0:
                visited_mask = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
                list_neighbouring_empty_tiles = grid_bfs((r,c), grid, visited_mask)
                for r,c in list_neighbouring_empty_tiles:
                    cover_grid[r][c] = 1

def right_click_functionality(x,y,cover):
    if cover[x][y] == 0:
        cover[x][y] = 2
    elif cover[x][y] == 2:
        cover[x][y] = 0

def initialize_game_constants(chosen_difficulty):
    global NUM_ROWS, NUM_COLS, NUM_MINES, SIZE

    NUM_ROWS = DIFFICULTY_LEVELS[chosen_difficulty][0]
    NUM_COLS = DIFFICULTY_LEVELS[chosen_difficulty][1]
    NUM_MINES = DIFFICULTY_LEVELS[chosen_difficulty][2]
    SIZE = WINDOW_SIZE[0] // NUM_ROWS

def main_menu():
    running = True
    difficulty = None
    while running:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (keys[pygame.K_w] and keys[pygame.K_LCTRL]):
                running = False
        difficulty, game_started = draw_menu(screen,difficulty)

        if game_started:
            initialize_game_constants(difficulty)
            main()
        pygame.display.update()


def main():
    running = True
    game_started = None
    cover_grid = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    grid = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    # Draw the initial grid
    draw(screen, grid, cover_grid)

    while running:
        try:
            keys = pygame.key.get_pressed()
        except pygame.error:
            pass

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (keys[pygame.K_w] and keys[pygame.K_LCTRL]):
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
                if (event.button) == 1:
                    cover_grid = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

                    row, col = get_grid_pos(pygame.mouse.get_pos())
                    grid = create_grid(NUM_ROWS, NUM_COLS, NUM_MINES, start_pos=(row, col), game_started=game_started)
                    game_started = True
                    draw(screen, grid, cover_grid)  # Redraw the grid after creating it

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    row, col = get_grid_pos(pygame.mouse.get_pos())
                    if row >= NUM_ROWS or col >= NUM_COLS:
                        continue
                    if cover_grid[row][col] == 0 or cover_grid[row][col] == 2:
                        right_click_functionality(row, col, cover_grid)
                    else:
                        middle_click_functionality(row, col, grid, cover_grid)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button) == 1:
                    row, col = get_grid_pos(pygame.mouse.get_pos())
                    if row >= NUM_ROWS or col >= NUM_COLS:
                        continue
                    if grid[row][col] == 0:
                        visited_mask = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
                        list_neighbouring_empty_tiles = grid_bfs((row, col), grid, visited_mask)
                        for r, c in list_neighbouring_empty_tiles:
                            cover_grid[r][c] = 1

                    cover_grid[row][col] = 1

                elif (event.button) == 3:
                    row, col = get_grid_pos(pygame.mouse.get_pos())
                    if row >= NUM_ROWS or col >= NUM_COLS:
                        continue
                    right_click_functionality(row, col, cover_grid)

                elif (event.button) == 2 or keys[pygame.K_SPACE]:
                    row, col = get_grid_pos(pygame.mouse.get_pos())
                    if row >= NUM_ROWS or col >= NUM_COLS:
                        continue
                    middle_click_functionality(row, col, grid, cover_grid)


        if game_started:
            draw(screen, grid, cover_grid)  
            check_gameover(grid, cover_grid)
            check_win(grid, cover_grid)

    pygame.quit()

if __name__ == "__main__":
    main_menu()

