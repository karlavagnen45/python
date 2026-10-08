def menu(title, prompt, options):
    print(f"{title}\n")
    for key, text in options.items():
        print(f" {key}) {text}\n")
    while True:
        choice = input(f"{prompt}")
        if choice in options:
            return(choice)
        
def login(users):
    while True:
        username = input("User: ")
        password = input("Password: ")
        if username in users and users[username] == password:
            print(f"\nWelcome {username}!")
            return(username)
            break
        else:
            print("\nInvalid username or password\n")
            
def add(prompt, string):
    _ = input(prompt)
    string.append(_)
    return(string)

def view(description, strings):
    print(f"{description}\n")
    listnr = 0
    for _ in(strings):
        listnr = listnr + 1
        print(f"{listnr}) {_}\n")
        
def user_login(user):
    while True:
        choice = menu("\nSelect an action", "Action: ", options)
        if choice == "a":
            add("\nLägg till en sträng: ", data[user])
        elif choice == "l":
            view(f"\n{user}s saker: ", data[user])
        elif choice == "q":
            print(f"\n{user} logged out.\n")
            break
        
#################################################
        
users = {"nisse":"apa", "bosse":"ko", "stina":"t-rex"}

data = {"nisse":["luva", "vante"], "bosse":["spik", "skruv", "hammare"], "stina":["tidsmaskin"]}

options = {"a":"Add item", "l":"List items", "q":"Log out"}

while True:
    user = login(users)
    
    user_login(user)
                  

