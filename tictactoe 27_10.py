def splash():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n             Tic Tac Toe\n\n                DV 07\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

def create_board(rows, cols):
    return [[""for _ in range(cols)]for _ in range(rows)]

def draw_board(board): # används numera endast i slutet av play_game för att visa vinst
    cols = len(board[0]) if board else 0
    print()
    border = "  +" + ("-----+") * cols
    print(border)
    for row in board:
        print("  |" + "|".join(str(cell).center(5) for cell in row) + "|")
        print(border)

def draw_board_c(board):
    cols = len(board[0]) if board else 0
    print("   " + " ".join(str(i + 1).center(5) for i in range(cols)) + " ") #Skriver först ut kolumnnummer, i princip samma kod som på rad 22
    border = "  +" + ("-----+") * cols
    print(border)
    for row in board:
        print("  |" + "|".join(str(cell).center(5) for cell in row) + "|") 
        print(border)

def draw_board_r(board, c):
    rows = len(board)
    cols = len(board[0]) if board else 0
    print()
    print("   " + " ".join(("↓" if j == c else "").center(5) for j in range(cols))) #Skriver ut pil ovanför vald kolumn
    border = "  +" + ("-----+") * cols
    print(border)
    for i in range(rows):
        print(f"{i + 1} |" + "|".join(str(cell).center(5) for cell in board[i]) + "|") #Skriver ut radnummer innan varje låda
        print(border)



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


def play_move(board, r, c, player):
    if not (0 <= r < len(board) and 0 <= c < len(board[0])):
        return False
    if board[r][c] != "":
        return False
    board[r][c] = player
    return True


def ask_number(prompt):
    while True:
        text = input(prompt)
        if text.isdigit():
            return int(text)
        print("Enter a positive number.")



def play_game(rows, cols, win_len, grav):
    board = create_board(rows, cols)
    player = "X"
    while True:
        draw_board_c(board)
        print(f"{player} to play")
        c = ask_number("Column: ") - 1
        if c < 0 or c >= cols:
            print("Invalid column, try again.")
            continue
        
        draw_board_r(board, c)
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
            
        if not play_move(board, r, c, player):
            print("Invalid row/column, try again.")
            continue
        
        if check_win(board, r, c, win_len):
            print(f"{player} has won!")
            draw_board(board)
            break
            
        if is_full(board):
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
    splash()
    while True:
        svar = menu("Main menu", "Select: ", {"p":"play", "s":"settings", "q":"quit"})
        if svar == "p":
            while True:
                play_game(rows, cols, win_len, grav)
                svar_p = menu("Continue?", "Select: ", {"p":"Continue", "q":"Main Menu"})
                if svar_p == "q":
                    break
            
            
        elif svar == "s":
            while True:
                svar_s = menu("Settings", "Select: ", {"1":f"Board width ({cols})", "2":f"Board height ({rows})", "3":f"Length to win ({win_len})", "4":f"Gravity ({grav})", "q":"Return to main menu"})
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
                elif svar_s == "q":
                    break
                
                
        elif svar == "q":
            print("Goodbye")
            break

main()