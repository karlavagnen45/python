from random import randint
from random import choice
import random

def random_symbol():
    _ = ["X", "O"]
    return random.choice(_)

def random_index(board):
    return randint(0, len(board)-1)

def change_random_free_square(board):
    random_row = random_index(board)
    random_col = random_index(board)
    if board[random_row][random_col] == "":
        board[random_row][random_col] = random_symbol()
        return True
        
def delete_random_occupied_square(board):
        random_row = random_index(board)
        random_col = random_index(board)
        if board[random_row][random_col] != "":
            board[random_row][random_col] = ""
            return True
        
def convert_board(board):
    return [rad[:-1] for rad in board[:-1]]

def fill_org_board(board_kopia, board):
    for row in range(len(board_kopia)):
        for col in range(len(board_kopia[row])):
            board[row][col] = board_kopia[row][col]
        
def randmode_func(board):
    board_kopia = convert_board(board)
    while True:
        if change_random_free_square(board_kopia):
            break
        if delete_random_occupied_square(board_kopia):
            break
    fill_org_board(board_kopia, board)

def splash():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n             Tic Tac Toe\n\n                DV 07\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

def create_board(rows, cols):
    return [[""for _ in range(cols)]for _ in range(rows)]

def draw_board(board):
    cols = len(board[0]) if board else 0
    border = "+" + ("-----+") * cols
    print(border)
    for row in board:
        print("|" + "|".join(str(cell).center(5) for cell in row) + "|")
        print(border)


def draw_randmode_board(board):
    cols = len(board[0]) if board else 0
    border = "+" + "-----+" * (cols - 1)

    print(border)
    for row in board[:-1]:
        inner = "|".join(str(cell).center(5) for cell in row[:-1])
        outer = str(row[-1]).center(5)       # sista kolumnen, utan kant
        print("|" + inner + "|" + outer)
        print(border)

    # Sista raden: alla celler utan kanter, i linje med kolumnerna ovanför
    print(" " + " ".join(str(cell).center(5) for cell in board[-1]))

def check_win(board, r, c, win_len):
    rows = len(board)
    cols = len(board[0]) if board else 0
    player = board[r][c]
    if player == "":
        return None
    
    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        count = 1
        i = 1
        while (0 <= r + dr * i < rows and 0 <= c + dc * i < cols
               and board[r + dr * i][c + dc * i] == player):
            count += 1
            i += 1

        i = 1
        while (0 <= r - dr * i < rows and 0 <= c - dc * i < cols
               and board[r - dr * i][c - dc * i] == player):
            count += 1
            i += 1
    
        if count >= win_len:
            return player
    return None


def is_full(board):
    for row in board:
        for cell in row:
            if cell == "":
                return False
    return True


def play_move(board, r, c, player, randmode):
    if not (0 <= r < len(board) and 0 <= c < len(board[0])):
        return False
    if board[r][c] != "":
        return False
    board[r][c] = player
    if randmode:
       if randint(1, 3) > 1:
            randmode_func(board)
    return True


def ask_number(prompt):
    while True:
        text = input(prompt)
        if text.isdigit():
            return int(text)
        print("Enter a positive number.")



def play_game(rows, cols, win_len, grav, randmode):
    board = create_board(rows, cols)
    player = "X"
    while True:
        if randmode:
            draw_randmode_board(board)
            print(f"{player} to play")
            c = ask_number("Column: ") - 1
            if c < 0 or c >= cols:
                print("Invalid column, try again.")
                continue
        else:
            draw_board(board)
            print(f"{player} to play")
            c = ask_number("Column: ") - 1
            if c < 0 or c >= cols:
                print("Invalid column, try again.")
                continue
        if not grav:
            r = ask_number("Row: ") - 1
        else:
            r = None
            # Scan from bottom to top to find the lowest empty cell in this column.
            # Gravity means the piece falls to the first available slot from the bottom.
            for br in range (rows - 1, -1, -1):
                if board[br][c] == "":
                    r = br
                    break
            # If no empty cell was found, the column is full.
            if r == None:
                print("\nColumn full, try again")
                continue
            
        if not play_move(board, r, c, player, randmode):
            print("Invalid row/column, try again.")
            continue
        if check_win(board, r, c, win_len):
            if randmode:
                draw_randmode_board(board)
                print(f"{player} has won!")
                break
            else:
                draw_board(board)
                print(f"{player} has won!")
                break
            
        if is_full(board):
            if randmode:
                draw_randmode_board(board)
                print("Draw.")
                break
            else:
               draw_board(board)
               print("Draw.")
               break
            
        player = "O" if player == "X" else "X"

def menu(title, prompt, options):
    print(f"{title}\n")
    for x in options:
        print(f"   {x}) {options[x]}")
    print()
    while True:
        n = input(prompt)
        if n in options:
            print()
            return n

def main():
    rows = 3
    cols = 3
    win_len = 3
    grav = False
    randmode = False
    splash()
    while True:
        svar = menu("Main menu", "Select: ", {"p":"play", "s":"settings", "q":"quit"})
        if svar == "p":
            while True:
                play_game(rows, cols, win_len, grav, randmode)
                svar_p = menu("Continue?", "Select: ", {"y":"Continue", "q":"Main Menu"})
                if svar_p == "q":
                    break
            
            
        elif svar == "s":
            while True:
                svar_s = menu("Settings", "Select: ", {"1":f"Board width ({cols})", "2":f"Board height ({rows})", "3":f"Length to win ({win_len})", "4":f"Gravity ({grav})","5":f"Random mode ({randmode})", "q":"Return to main menu"})
                if svar_s == "1":
                    cols = ask_number("Select board width: ")
                    print(f"Board width set to")
                elif svar_s == "2":
                    rows = ask_number("Select board height: ")
                elif svar_s == "3":
                    win_len = ask_number("Select length to win: ")
                elif svar_s == "4":
                    if grav == False:
                        grav = True
                    else:
                        grav = False
                elif svar_s == "5":
                    if randmode == False:
                        randmode = True
                        rows = 4
                        cols = 4
                    else:
                        randmode = False
                elif svar_s == "q":
                    break
                
                
        elif svar == "q":
            print("Goodbye")
            break

main()