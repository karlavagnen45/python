# ================================================================
# Tre i rad för valfri brädstorlek och vinstlängd
#
# Brädet är en 2D-Lista: board[rad][kolumn]
# En tom ruta är "" och en ifylld ruta är "X" eller "O"
# ================================================================

def splash():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n              Tre i rad\n\n                DV 07\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
# En enkel splash likt Biathlon-uppgiften

def create_board(rows, cols):
    return [[""for _ in range(cols)]for _ in range(rows)]
# Den yttre listan har en inre lista per rad, och varje inre lista har en tom sträng "" per kolumn.
# Alltså en 2D-lista. (_ i "for _ in ..." är loopvariabler som inte används till något.)


def draw_board(board):
    # Ritar spelbrädet i terminalen
    # Antal kolumner = längden på första raden (0 om brädet är tomt)
    cols = len(board[0]) if board else 0
    
    # Varje ruta är 5 tecken bred, så kantlinjen blir "+-----+-----+..."
    border = "+" + ("-----+") * cols
    
    print(border) # Översta kantlinjen
    for row in board:
        # str(cell).center(5) centrerar innehållet i en ruta som är 5 tecken bred.
        # "|".join(...) sätter | mellan rutorna på insidan av brädet,
        # vi lägger även till ett | i början och slutet för ytterkanterna.
        print("|" + "|".join(str(cell).center(5) for cell in row) + "|")
        print(border) # kantlinje under varje rad för att skapa stängda rutor.



def check_win(board, r, c, win_len):
    # Kollar om draget som precis lades på (r, c) gav en vinst.
    # En vinst kan bara uppstå i en linje som går genom det senaste draget,
    # så vi behöver inte söka genom hela brädet.
    rows = len(board)
    cols = len(board[0]) if board else 0
    player = board[r][c] # den som precis spelade
    if player == "":
        return None # tom ruta, ingen kan ha vunnit här
    
    #Fyra linjetyper räcker eftersom vi räknar åt båda hållen längs varje linje.
    # (dr, dc) = hur rad och kolumn ändras per steg.
    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]: # Motsvarar riktningar: →, ↓, ↘, ↙
        count = 1 # börjar på 1 eftersom draget vi urgår från räknas med
        
        # Räkna framåt: gå steg för steg i riktning (dr, dc)
        # i = avstånd från spelade rutan.
        # Vi fortsätter så länge vi är inom brädet OCH den räknade rutan tillhör spelaren
        # Villkoret "inom brädet" kontrolleras först, så vi indexerar aldrig utanför
        i = 1
        while (0 <= r + dr * i < rows and 0 <= c + dc * i < cols
               and board[r + dr * i][c + dc * i] == player):
            count += 1
            i += 1
        
        # Räkna bakåt: samma sak fast åt motsatt håll (minus istället för plus)
        # Det behövs eftersom det senaste draget kan ligga mitt i en rad
        # t.ex. X _ X där man fyller på mitten
        i = 1
        while (0 <= r - dr * i < rows and 0 <= c - dc * i < cols
               and board[r - dr * i][c - dc * i] == player):
            count += 1
            i += 1
        
        # count är nu hela längden på spelarens rad i denna riktning.
        # >= gör att även längre rader än win_len räknas som vinst
        if count >= win_len:
            return player
        
    return None # ingen av de fyra linjerna var tillräckligt lång


def is_full(board):
    # Returnerar True om det inte finns några tomma rutor kvar
    # Vi avbryter direkt när vi hittar en tom ruta (då är brädet inte fullt).
    for row in board:
        for cell in row:
            if cell == "":
                return False
    return True # hittade ingen tom ruta


def play_move(board, r, c, player):
    # Försöker läga ett drag. Returnerar True om det lyckades, annars False.
    # Funktionen bestämmer inte vad som hände vid ett felaktigt drag,
    # det gör istället anroparen (funktionen play_game)
    
    #Kontrollera att rutan finns i brädet. Det här skyddar också mot
    # indexet -1 (om spelaren skrev 0), som annar skulle "vika runt"
    # till sista raden/kolumnen i Python.
    if not (0 <= r < len(board) and 0 <= c < len(board[0])):
        return False # utanför spelplan
    if board[r][c] != "":
        return False # ruta redan ifylld
    board[r][c] = player # allt ok, placera draget
    return True


def ask_number(prompt):
    # Frågar tills spelaren skriver in ett heltal, och returnerar det som int.
    # isdigit() är True bara om hela texten består av siffror, så allt annat,
    # t.o.m. negativa tal avvisas innan int() körs.
    # Siffran 0 släpps igenom här, men fångas senare av play_move
    while True:
        text = input(prompt)
        if text.isdigit():
            return int(text)
        print("Skriv ett positivt heltal.")



def play_game(rows, cols, win_len):
    # Själva spelloopen. Storleken och vinstlängd bestäms inan funktionen anropas.
    board = create_board(rows, cols)
    player = "X" # X börjar
    
    while True: # varje varv = ett försök att göra ett drag
        draw_board(board)
        print(f"{player} att spela")
        
        # Parsar inputen med -1,
        # eftersom vi vill undvika att ha 0 som första rad respektive kolumn.
        r = ask_number("Rad: ") - 1
        c = ask_number("Kolumn: ") - 1
        
        # Ogiltigt drag (utanför brädet eller upptagen ruta):
        # continue hoppar till början av loopen utan att byta spelare,
        # så samma spelare får försöka igen
        if not play_move(board, r, c, player):
            print("Ogiltigt drag, försök igen.")
            continue
        
        # Vinstkontrollen kommer före oavgjort-kontrollen: om det sista
        # draget på fullt bräde gör en rad ska det räknas som vinst
        if check_win(board, r, c, win_len):
            draw_board(board) # visa slutläget så man ser vinstraden
            print(f"{player} har vunnit!")
            break # avsluta spelet
            
        if is_full(board):
            draw_board(board)
            print("Oavgjort.")
            break
        
        # Nådde vi hit var draget giltigt och spelet fortsätter: byt spelare.
        # Slutstycket här bör nog ändras ifall vi vill möjliggöra inställningar
        # för mer än två spelare.
        player = "O" if player == "X" else "X"







splash()
#menu("Welcome", "Select action: ", {"p":"play", "s":"settings", "q":"quit"})