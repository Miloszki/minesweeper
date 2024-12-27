 
import pygame
import random
from pprint import pprint
from collections import deque 

pygame.init()
pygame.font.init()
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

TILE_CODES = {
    'hidden': 0,
    'shown': 1,
    'bomb': -1,
    'flag': 2
}
TILE_COLOR = (100,100,100)
TEXT_COLOR = (255,100,100)
BG_COLOR = (0,0,0)
WINDOW_SIZE = (800,800)
CLICKED_TILE_COLOR = (20,20,20)
FLAGGED_TILE_COLOR = (200,200,0)
NUM_ROWS = 15
NUM_COLS = 15
NUM_MINES = 25
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
SIZE = WINDOW_SIZE[0] // NUM_ROWS
FONT = pygame.font.SysFont('Arial', 25)
GAMEOVER_FONT = pygame.font.SysFont('Arial', 70)
screen = pygame.display.set_mode(WINDOW_SIZE)
width, height = screen.get_size()

def get_tile_neighbours(row,col,rows,cols): #change to for loop in the future?
    neighbours = []

    if row >0:
        neighbours.append((row-1, col))
    if row < (rows) - 1:
        neighbours.append((row +1, col))

    if col > 0:
        neighbours.append((row,col-1))
    if col < (cols) - 1:
        neighbours.append((row,col+1))

    if row > 0 and col > 0:
        neighbours.append((row-1,col-1))

    if row > 0  and col < (cols) - 1:
        neighbours.append((row-1, col+1))

    if row < (rows) -1 and col > 0:
        neighbours.append((row+1, col-1))

    if row < (rows) -1 and col < (cols) - 1:
        neighbours.append((row+1,col+1))

    return neighbours    

def create_grid(rows,cols, mines):
    grid = [[0 for _ in range(cols)] for  _ in range(rows)]

    mine_indexes = set()
    while len(mine_indexes) < mines:
        row, col = random.randint(0,rows-1), random.randint(0,cols-1)
        pos = row, col

        if pos in mine_indexes:
            continue

        mine_indexes.add(pos)
        grid[row][col] = TILE_CODES['bomb']

    for mine in mine_indexes:
        neighbours = get_tile_neighbours(*mine, rows, cols)
        for r,c in neighbours:
            if grid[r][c] != TILE_CODES['bomb']:
                grid[r][c] += 1

    return grid

def draw(window, field, cover):
    
    window.fill(BG_COLOR)
    
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
                pygame.draw.rect(screen,'black',rect,2)
                continue
            else:
                pygame.draw.rect(screen,CLICKED_TILE_COLOR,rect)
                pygame.draw.rect(screen,'black',rect,2)

            if val != 0:
                txt = FONT.render(str(val),2,NUM_COLORS[val])
                window.blit(txt,(x + (SIZE/2 -txt.get_width()/2), y + (SIZE/2 - txt.get_height()/2)))

    pygame.display.update()


def find_empty_neighbours(init_pos, grid):
    empty_neighbours = []
    x,y = init_pos

    
    if x >0:
        if grid[x-1][y] == 0:
            empty_neighbours.append((x-1, y))
    if x < (NUM_ROWS) - 1:
        if grid[x+1][y] == 0:
            empty_neighbours.append((x +1, y))

    if y > 0:
        if grid[x][y-1] == 0:
            empty_neighbours.append((x,y-1))

    if y < (NUM_COLS) - 1:
        if grid[x][y+1] == 0:
            empty_neighbours.append((x,y+1))

    if x > 0 and y > 0:
        if grid[x-1][y-1] == 0:
            empty_neighbours.append((x-1,y-1))

    if x > 0  and y < (NUM_COLS) - 1:
        if grid[x-1][y+1] == 0:
            empty_neighbours.append((x-1, y+1))

    if x < (NUM_ROWS) -1 and y > 0:
        if grid[x+1][y-1] == 0:
            empty_neighbours.append((x+1, y-1))

    if x < (NUM_ROWS) -1 and y < (NUM_COLS) - 1:
        if grid[x+1][y+1] == 0:
            empty_neighbours.append((x+1,y+1))

    return empty_neighbours


def recursive_find_empty_neighbours(pos,grid):
    neighbours_next = [pos]
    x,y = pos
    if len(neighbours_next) == 0:
        return empty_neighbours
    if grid[x][y] == 0:
        empty_neighbours = recursive_find_empty_neighbours('a',grid)
    return empty_neighbours



def grid_bfs(pos, grid, visited_mask):
    q = deque()
    ll=[]
    x, y = pos

    q.append((x, y))

    while len(q) > 0:
        cell = q.popleft()
        x, y = cell

        if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
            continue
        if visited_mask[x][y]:
            continue

        visited_mask[x][y] = 1
        #znajdz ciag pustych pol
        if grid[x][y] == 0:
            neighbors = []
            if x + 1 < len(grid) and not visited_mask[x + 1][y]:
                neighbors.append((x + 1, y))
            if x - 1 >= 0 and not visited_mask[x - 1][y]:
                neighbors.append((x - 1, y))
            if y + 1 < len(grid[0]) and not visited_mask[x][y + 1]:
                neighbors.append((x, y + 1))
            if y - 1 >= 0 and not visited_mask[x][y - 1]:
                neighbors.append((x, y - 1))

            if x + 1 < len(grid) and y + 1 < len(grid[0]) and not visited_mask[x + 1][y + 1]:
                neighbors.append((x+1, y + 1))
            if x + 1 < len(grid) and y - 1 >= 0 and not visited_mask[x + 1][y - 1]:
                neighbors.append((x+1, y - 1))
            if x - 1 >= 0 and y + 1 < len(grid[0]) and not visited_mask[x - 1][y + 1]:
                neighbors.append((x-1, y + 1))
            if x - 1 >= 0 and y - 1 >= 0 and not visited_mask[x - 1][y - 1]:
                neighbors.append((x-1, y - 1))


            q.extend(neighbors)
            ll.append(neighbors)

        
    flat_ll = [x for xs in ll for x in xs]
    print(flat_ll)
    return flat_ll

def basic_middle_button(pos,grid, cover_grid, max_iter=8):
    #jezeli jest flaga obok np 1 musi miec >= flag obok siebie zeby dzialalo
    x,y = pos
    ca8_neighbours = []
    clicked_tile_val = grid[x][y]
    print('value',clicked_tile_val)
    # if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
    #         pass
    flags_found = 0
    #check if enough flags are selected nearby
    if x > 0:
        if cover_grid[x-1][y] == 2:
            flags_found += 1

    if x < (NUM_ROWS) - 1:        
        if cover_grid[x+1][y] == 2:
            flags_found += 1

    if y > 0:
        if cover_grid[x][y-1] == 2:
            flags_found += 1

    if y < (NUM_COLS) - 1:
        if cover_grid[x][y+1] == 2:
            flags_found += 1

    if x > 0 and y > 0:
        if cover_grid[x-1][y-1] == 2:
            flags_found += 1

    if x > 0 and y < NUM_COLS - 1:
        if cover_grid[x-1][y+1] == 2:
            flags_found += 1
    if x < NUM_ROWS - 1 and y > 0:
        if cover_grid[x+1][y-1] == 2: 
            flags_found += 1

    if x < NUM_ROWS- 1  and y < NUM_COLS -1:
        if cover_grid[x+1][y+1] == 2:
            flags_found += 1

    if flags_found < clicked_tile_val:
        return []



    if x > 0:
        if cover_grid[x-1][y] != 2 and grid[x-1][y] != -1 :
            ca8_neighbours.append([x-1,y])
    if x < (NUM_ROWS) - 1:
        if cover_grid[x+1][y] != 2 and grid[x+1][y] != -1 :
            ca8_neighbours.append([x +1, y])

    if y > 0:
        if cover_grid[x][y-1] != 2 :
            ca8_neighbours.append([x,y-1])

    if y < (NUM_COLS) - 1:
        if cover_grid[x][y+1] != 2 :
            ca8_neighbours.append([x,y+1])

    if x > 0 and y > 0:
        if cover_grid[x-1][y-1] != 2 :
            ca8_neighbours.append([x-1,y-1])

    if x > 0  and y < (NUM_COLS) - 1:
        if cover_grid[x-1][y+1] != 2 :
            ca8_neighbours.append([x-1, y+1])

    if x < (NUM_ROWS) -1 and y > 0:
        if cover_grid[x+1][y-1] != 2 :
            ca8_neighbours.append([x+1, y-1])

    if x < (NUM_ROWS) -1 and y < (NUM_COLS) - 1:
        if cover_grid[x+1][y+1] != 2  :
            ca8_neighbours.append([x+1,y+1])

    flat_ca8_neighbours = [x for xs in ca8_neighbours for x in xs]
    
    return ca8_neighbours

def get_grid_pos(mouse_pos):
    mx, my = mouse_pos
    row = mx // SIZE
    col = my // SIZE
    return row,col

def main():
    running = True
    grid = create_grid(NUM_ROWS, NUM_COLS, NUM_MINES)
    cover_grid = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    
    while running:
        keys = pygame.key.get_pressed()
        draw(screen,grid, cover_grid)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
            #left click
                if (event.button) == 1:
                    row, col = get_grid_pos(pygame.mouse.get_pos())
                    if row >= NUM_ROWS or col >= NUM_COLS:
                        continue
                    if grid[row][col] == 0:
                        visited_mask = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
                        list_neighbouring_empty_tiles = grid_bfs((row,col), grid, visited_mask)
                        for r,c in list_neighbouring_empty_tiles:
                            cover_grid[r][c] = 1
                    #game over
                    if grid[row][col] == -1:
                        print('gameover')
                        gameover_txt = GAMEOVER_FONT.render('GAME OVER', 2, 'red')
                        screen.blit(gameover_txt, (width // 2 - gameover_txt.get_width() // 2, height // 2 - gameover_txt.get_height() // 2))
                        pygame.display.update()
                        #usprawnic zebyu mozna bylo zrestartowac gre
                        # pygame.time.wait(2000)
                    cover_grid[row][col] = 1

                #right click - flagging
                elif (event.button) == 3:
                    row, col = get_grid_pos(pygame.mouse.get_pos())
                    if cover_grid[row][col] == 0:
                        cover_grid[row][col] = 2
                    elif cover_grid[row][col] == 2:
                        cover_grid[row][col] = 0
                    if row >= NUM_ROWS or col >= NUM_COLS:
                        continue

                #middle click
                if (event.button) == 2:
                    row, col = get_grid_pos(pygame.mouse.get_pos())
                    if row >= NUM_ROWS or col >= NUM_COLS:
                        continue
                    #algorytm sprawdzania czy wokol sa bomby etc.
                    visited_mask = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
                    list_neighbouring_empty_tiles = grid_bfs((row,col), grid, visited_mask)
                    for r,c in list_neighbouring_empty_tiles:
                        cover_grid[r][c] = 1

                    if grid[row][col] > 0:
                        neighbours = basic_middle_button((row,col),grid,cover_grid)
                        for r,c in neighbours:
                            cover_grid[r][c] = 1


            if event.type == pygame.QUIT or (keys[pygame.K_w] and keys[pygame.K_LCTRL]):
                running = False

        ####
        clock.tick(60)
    
    pygame.quit()



if __name__ == "__main__":
    main()