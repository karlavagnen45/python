from random import randint, choice # choice importeras direkt, så ingen separat "import random" behövs
 
 
def random_symbol():
    return choice(["X", "O"])
 
 
def random_index(limit):
    return randint(0, limit - 1) # limit = antal rader eller kolumner; högsta giltiga index är limit - 1
 

# Slumpfunktionerna arbetar direkt på det riktiga brädet (ingen kopia behövs längre).
# Rad och kolumn slumpas med varsin gräns, så det fungerar även på brädor som inte är kvadratiska.
def change_random_free_square(board):
    r = random_index(len(board)) # len(board) = antal rader
    c = random_index(len(board[0])) # len(board) = antal kolumner
    if board[r][c] == "":
        board[r][c] = random_symbol()
        return True
    return False # returvärde när rutan redan var upptagen
 
 
def delete_random_occupied_square(board):
    r = random_index(len(board))
    c = random_index(len(board[0]))
    if board[r][c] != "":
        board[r][c] = ""
        return True
    return False # returvärde när rutan redan var tom
 
 
def randmode_func(board):
    # Försöker lägga till eller ta bort en slimpmässig ruta tills en av dem lyckas
    # Hela brädet är spelplan, så inget behöver kopieras eller skrivas tillbaka
    while True:
        if change_random_free_square(board):
            break
        if delete_random_occupied_square(board):
            break
 
 
def splash():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n             Tic Tac Toe\n\n                DV 07\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

def line():
    print("~" * 100) # Används i menu() och asknumber()
 
 
def create_board(rows, cols):
    return [["" for _ in range(cols)] for _ in range(rows)]
 
 
def draw_board(board):  # används numera endast i slutet av play_game för att visa vinst
    cols = len(board[0]) if board else 0
    print()
    border = "  +" + ("-----+") * cols
    print(border)
    for row in board:
        print("  |" + "|".join(str(cell).center(5) for cell in row) + "|")
        print(border)
    print()
 
# Ritar brädet med kolumnnummer ovanför. Används i både vanligt läge och random mode.
def draw_board_c(board):
    cols = len(board[0]) if board else 0
    print("   " + " ".join(str(i + 1).center(5) for i in range(cols)) + " ")  # Skriver först ut kolumnnummer
    border = "  +" + ("-----+") * cols
    print(border)
    for row in board:
        print("  |" + "|".join(str(cell).center(5) for cell in row) + "|")
        print(border)
    print()

# Ritar brädet med en pil över vald kolumn och radnumer till vänster,
# så spelaren ser var pjäsen hamnar när raden ka väljas.
# Visas bara i play_game när grav = False
def draw_board_r(board, c):
    rows = len(board)
    cols = len(board[0]) if board else 0
    print()
    print("   " + " ".join(("↓" if j == c else "").center(5) for j in range(cols)))  # Skriver ut pil ovanför vald kolumn
    border = "  +" + ("-----+") * cols
    print(border)
    for i in range(rows):
        # {i + 1:<2} ger radnumret två teckens bredd, så raderna linjerar upp sig korrekt upp till rad 99
        print(f"{i + 1:<2}|" + "|".join(str(cell).center(5) for cell in board[i]) + "|")  # Skriver ut radnummer innan varje låda
        print(border)
    print()
 
 
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
        # Kräver minst 1, så bredd, höjd och vinstlängd aldrig blir 0
        if text.isdigit() and int(text) >= 1:
            line()
            return int(text)
        print("Enter a positive number.")
 
 
def play_game(rows, cols, win_len, grav, randmode):
    board = create_board(rows, cols) # brädet har exakt den storlek som visas i inställningarna
    player = "X"
    while True:
        # Samma utritning i båda lägena, så inga seåarata grenar för random mode behövs
        draw_board_c(board)
        print(f"{player} to play")
        c = ask_number("Column: ") - 1
        if c < 0 or c >= cols:
            print("Invalid column, try again.")
            continue
 
        if not grav:
            draw_board_r(board, c)
            r = ask_number("Row: ") - 1
        else:
            r = None
            # Scan from bottom to top to find the lowest empty cell in this column.
            # Gravity means the piece falls to the first available slot from the bottom.
            for br in range(rows - 1, -1, -1):
                if board[br][c] == "":
                    r = br
                    break
            # If no empty cell was found, the column is full.
            if r is None:
                print("\nColumn full, try again")
                continue
 
        if not play_move(board, r, c, player, randmode):
            print("Invalid row/column, try again.")
            continue
 
        if check_win(board, r, c, win_len):
            draw_board(board)
            print(f"{player} has won!")
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
            line()
            return n
 
 
def main():
    rows = 3
    cols = 3
    win_len = 3
    grav = False
    randmode = False
    splash()
    while True:
        svar = menu("Main menu", "Select: ", {"p": "play", "s": "settings", "q": "quit"})
        if svar == "p":
            while True:
                play_game(rows, cols, win_len, grav, randmode)
                svar_p = menu("Continue?", "Select: ", {"p": "Continue", "q": "Main Menu"})
                if svar_p == "q":
                    break
 
        elif svar == "s":
            while True:
                svar_s = menu("Settings", "Select: ", {
                    "1": f"Board width ({cols})",
                    "2": f"Board height ({rows})",
                    "3": f"Length to win ({win_len})",
                    "4": f"Gravity ({grav})",
                    "5": f"Random mode ({randmode})",
                    "q": "Return to main menu"})
                if svar_s == "1":
                    cols = ask_number("Select board width: ")
                elif svar_s == "2":
                    rows = ask_number("Select board height: ")
                elif svar_s == "3":
                    win_len = ask_number("Select length to win: ")
                elif svar_s == "4":
                    grav = not grav # växlar mellan True och False
                elif svar_s == "5":
                    randmode = not randmode # brädets storlek ändras inte längre när random mode slås på
                elif svar_s == "q":
                    break
 
        elif svar == "q":
            print("Goodbye")
            break
 
 
main()