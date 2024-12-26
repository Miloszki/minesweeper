 
import pygame
import random
from pprint import pprint

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
TILE_COLOR = (255,255,255)
TEXT_COLOR = (255,100,100)
BG_COLOR = (0,0,0)
WINDOW_SIZE = (800,800)
BLOCK_SIZE = 10
NUM_ROWS = 5
NUM_COLS = 5
NUM_MINES = 10
NUM_COLORS = {
    1: 'blue',
    2: 'green',
    3: 'red',
    4: 'navy',
    5: 'burgundy',
    6: 'teal',
    7: 'black',
    8: 'gray'
}
FONT = pygame.font.SysFont('Arial', 20)

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
    if col > (cols) - 1:
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
        print(pos)
        grid[row][col] = TILE_CODES['bomb']

    for mine in mine_indexes:
        neighbours = get_tile_neighbours(*mine, rows, cols)
        for r,c in neighbours:
            grid[r][c] += 1

    return grid

def draw(window, field, cover):
    window.fill(BG_COLOR)
    size = WINDOW_SIZE[0] // NUM_ROWS
    for i, row in enumerate(field):
        for j, val in enumerate(row):
             txt = FONT.render(str(val),False,NUM_COLORS[val])
             window.blit(txt,(i,j))



    pygame.display.update()


def main():
    running = True
    grid = create_grid(NUM_ROWS, NUM_COLS, NUM_MINES)
    pprint(grid)
    while running:
        keys = pygame.key.get_pressed()
        



    #     #####
    #     draw(screen)
        


    #     for x in range(0, width, BLOCK_SIZE ):
    #         for y in range(0, height, BLOCK_SIZE):
    #             rect = pygame.Rect(x,y,BLOCK_SIZE,BLOCK_SIZE)
    #             pygame.draw.rect(screen,TILE_COLOR,rect,1)
    #             tile_text = font.render(str(TILE_CODES['hidden']),False,TEXT_COLOR)
    #             screen.blit(tile_text,(x + BLOCK_SIZE//2,y+ BLOCK_SIZE//2))




        
    


        for event in pygame.event.get():
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = pygame.mouse.get_pos()
            #     print(mouse_pos)

            if event.type == pygame.QUIT or (keys[pygame.K_w] and keys[pygame.K_LCTRL]):
                running = False

        ####
        # pygame.display.flip()
        # clock.tick(60)
    
    pygame.quit()



if __name__ == "__main__":
    main()