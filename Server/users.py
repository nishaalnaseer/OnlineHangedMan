import json

def loadUsers():
    """load users from users.json"""
    try:
        with open("users.json", 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        return {}
    
    return users

def saveUsers(users):
    """save users to users.json, accepts data as function input"""
    with open("users.json", 'w') as f:
        json.dump(users, f)

def checkUser(userName):
    """check if user is in dict from file"""
    users = loadUsers()

    try:
        users[userName]
    except KeyError:
        print(f"code0002:f {userName} not on file")
        return f"code0002:f"
    else:
        return 1

def signup(args):
    """create users from input"""
    username = args[1]
    password = args[2]

    oldUsers = loadUsers()

    try:
        if username in oldUsers.keys():
            print(oldUsers.keys())
            # if so the code afterwards will not be executed
            return "Username already taken."
    except AttributeError:
        new_user_list = {username: password}
    else:
        # update the list of user dict
        new_user_list = oldUsers.update({username: password})
        print(new_user_list)
    
    saveUsers(new_user_list)  # save dictionary

    return "User Successfully Created!"
    

def updatePassword(updates):
    """updates existing password of users"""
    oldData = loadUsers()

    for userName, passWord in updates.items():
        oldData[userName] = passWord
    
    saveUsers(oldData)
    print("passwords updated")

loggedIn = []
def signin(args):
    """accepts a list of arguments"""
    try:
        password = args[1]
        userName = args[0]
    except IndexError:
        return "Invalid number of arguments"

    if username in loggedIn:
        return "User already logged in"

    if password == "" or userName == "":
        print("Mode 'a' incompatible with empty username or password")

    users = loadUsers()
    try:
        passwordOnFile = users[userName]
    except KeyError:
        return "code0004:w"

    if password != passwordOnFile:
        return "code0004:c"
    else:
        loggedIn.append(userName)
        return "code0004:s"