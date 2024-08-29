import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

screen.fill(BG_COLOR)
draw_lines()

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == ''

def check_draw():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == '':
                return False
    return True

def draw_cross(row, col):
    start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
    end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
    pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
    start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
    end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
    pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

def draw_circle(row, col):
    center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
    pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CROSS_COLOR if player == 'X' else CIRCLE_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CROSS_COLOR if player == 'X' else CIRCLE_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), LINE_WIDTH)

def draw_asc_diagonal(player):
    color = CROSS_COLOR if player == 'X' else CIRCLE_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), LINE_WIDTH)

def draw_desc_diagonal(player):
    color = CROSS_COLOR if player == 'X' else CIRCLE_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), LINE_WIDTH)

def check_win(player):
    for col in range(BOARD_COLS):
        if (board[0][col] == board[1][col]) and (board[1][col] == board[2][col]) and (board[0][col] == player):
            draw_vertical_winning_line(col, player)
            return True

    for row in range(BOARD_ROWS):
        if (board[row][0] == board[row][1]) and (board[row][1] == board[row][2]) and (board[row][0] == player):
            draw_horizontal_winning_line(row, player)
            return True

    if (board[0][2] == board[1][1]) and (board[1][1] == board[2][0]) and (board[0][2] == player):
        draw_asc_diagonal(player)
        return True

    if (board[0][0] == board[1][1]) and (board[1][1] == board[2][2]) and (board[0][0] == player):
        draw_desc_diagonal(player)
        return True

    return False

def vcheck_win(player):
    for col in range(BOARD_COLS):
        if (board[0][col] == board[1][col]) and (board[1][col] == board[2][col]) and (board[0][col] == player):
            return True

    for row in range(BOARD_ROWS):
        if (board[row][0] == board[row][1]) and (board[row][1] == board[row][2]) and (board[row][0] == player):
            return True

    if (board[0][2] == board[1][1]) and (board[1][1] == board[2][0]) and (board[0][2] == player):
        return True

    if (board[0][0] == board[1][1]) and (board[1][1] == board[2][2]) and (board[0][0] == player):
        return True

    return False

def minimax(position, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or vcheck_win('O') or vcheck_win('X') or check_draw():
        if vcheck_win('O'):
            return 1
        elif vcheck_win('X'):
            return -1
        else:
            return 0

    if maximizingPlayer:
        maxEval = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if position[row][col] == '':
                    position[row][col] = 'O'
                    eval = minimax(position, depth - 1, alpha, beta, False)
                    position[row][col] = ''
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return maxEval
    else:
        minEval = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if position[row][col] == '':
                    position[row][col] = 'X'
                    eval = minimax(position, depth - 1, alpha, beta, True)
                    position[row][col] = ''
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return minEval

def best_move():
    bestScore = -math.inf
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == '':
                board[row][col] = 'O'
                score = minimax(board, 9, -math.inf, math.inf, False)
                board[row][col] = ''
                if score > bestScore:
                    bestScore = score
                    move = (row, col)
    return move

player = 'X'
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            if available_square(clicked_row, clicked_col) and player == 'X':
                mark_square(clicked_row, clicked_col, player)
                draw_cross(clicked_row, clicked_col)
                if check_win(player):
                    game_over = True
                    print(f"Player {player} wins!")
                elif check_draw():
                    game_over = True
                    print("It's a draw!")
                pygame.display.update()
                player = 'O'

        if player == 'O' and not game_over:
            move = best_move()
            if move:
                mark_square(move[0], move[1], 'O')
                draw_circle(move[0], move[1])
                if check_win('O'):
                    game_over = True
                    print("Player O wins!")
                elif check_draw():
                    game_over = True
                    print("It's a draw!")
                pygame.display.update()
                player = 'X'

        if game_over:
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
                        screen.fill(BG_COLOR)
                        draw_lines()
                        player = 'X'
                        game_over = False
                        pygame.display.update()

    pygame.display.update()
