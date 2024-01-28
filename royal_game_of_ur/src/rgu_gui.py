import pygame
import rgu
import sys

## BUGS:
# kan niet tegen buiten het grid klikken

#initialize a game
rgu = rgu.RGU()
rgu.new_game()


pygame.init()

size = width, height = 700, 400
speed = [1,1]
white = 255, 255, 255
red = 255, 0, 0

black = 0,0,0
margin_left = 30
margin_top = 27
square_width = 75
square_height = 73

screen = pygame.display.set_mode(size)


# Load images and extract rects
board = pygame.image.load("board_transparent_bg.png")
board_rect = board.get_rect()

white_stone = pygame.image.load("white_stone.png")
white_stone_rect = white_stone.get_rect()

dark_stone = pygame.image.load("dark_stone.png")
dark_stone_rect = dark_stone.get_rect()

# Create 7 copies of the stone rects
ws = [white_stone_rect.copy() for i in range(rgu.num_stones)]
ds = [dark_stone_rect.copy() for i in range(rgu.num_stones)]

# Create a grid of Rects for placing stones
square_rect = [[],[],[]]
for h in range(3):
    for w in range(8):
        square_rect[h].append(pygame.Rect(margin_left+square_width*w,
                                          margin_top+square_height*h,
                                          square_width, square_height))



def get_grid_click(pos):
    for h, row in enumerate(square_rect):
        for w, stone in enumerate(row):
            if stone.collidepoint(pos):
                return h,w
            
            
def check_valid_move(h,w, valid):
    if rgu.translate[h,w] not in valid:
        return -1
    if rgu.board[h,w] < 0 and rgu.player == 0:
        return -1
    if rgu.board[h,w] > 0 and rgu.player == 1:
        return -1
    return rgu.translate[h,w]
            
gamestate = 0
def next_gamestate():
    global gamestate
    gamestate = (gamestate+1) %2
    
game_font = pygame.font.SysFont("Arial", 30)




while 1:
    if gamestate == 0:
        roll = rgu.roll_dice()
        print("Player {} rolls: {}".format(rgu.player, roll))
        #print(rgu.evaluate_possible_moves(roll))
        #print(rgu.get_best_move(roll))
        if roll != 0 and rgu.get_possible_moves(roll):
            next_gamestate()
        else:
            rgu.change_player()
    
    if gamestate == 1 and rgu.player == 1:
        move = rgu.get_best_move(roll)[0]
        m = rgu.do_move(move, roll)
        if m not in rgu.reroll_idx:                    
            rgu.change_player()
        next_gamestate()
        
        
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            h,w = get_grid_click(event.pos)
            move = check_valid_move(h,w,rgu.get_possible_moves(roll))
            if move >= 0:
                m = rgu.do_move(move, roll)
                if m not in rgu.reroll_idx:                    
                    rgu.change_player()
                next_gamestate()

                
    
        
          
    
    # Update the board
    l = d = 0
    for i, h in enumerate(rgu.board):
        for j, w in enumerate(h):
            if w > 0:
                for k in range(w):
                    ws[l].center = square_rect[i][j].center
                    l += 1
            if w < 0:
                for k in range(-w):
                    ds[d].center = square_rect[i][j].center
                    d += 1   
    
    # Draw the board
    screen.fill(white)    
    screen.blit(board, board_rect)
        
    for i in ws:
        screen.blit(white_stone, i)
    
    for i in ds:
        screen.blit(dark_stone, i)
    
    
    # Draw text: Roll, Player, Score/stack sizes
    if rgu.check_winner() == -1:
        roll_label = game_font.render("Player {} rolls: {}".format(rgu.player, roll), 1, black)
    else:
        roll_label = game_font.render("Player {} has won".format(rgu.check_winner()), 1, black)
        gamestate = 3
    player_0_start = game_font.render("{}".format(rgu.track[0,0]), 1, black)
    player_1_start = game_font.render("{}".format(rgu.track[1,0]), 1, black)
    
    player_0_end = game_font.render("{}".format(rgu.track[0,-1]), 1, black)
    player_1_end = game_font.render("{}".format(rgu.track[1,-1]), 1, black)
    
    
    
    screen.blit(roll_label, (282,300))    
    screen.blit(player_1_start, (360,230))
    screen.blit(player_0_start, (360,10))
    screen.blit(player_0_end, (420,10))
    screen.blit(player_1_end, (420,230))
    
    
    pygame.display.flip()

    