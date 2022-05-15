import json

def loadUsers():
    """load users from users.json"""
    try:
        with open("users.json", 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        print("code0001:f FileNotFoundError")
        users = {}
    
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
    if len(args) > 3:
        return "code0000:m"

    try:
        userName = args[1]
        password = args[2]
    except IndexError:
        return "code0004:i"

    oldUsers = loadUsers()
    oldUsers.update({userName: password})
    
    saveUsers(oldUsers)

    return "code0004:p"

def updatePassword(updates):
    """updates existing password of users"""
    oldData = loadUsers()

    for userName, passWord in updates.items():
        oldData[userName] = passWord
    
    saveUsers(oldData)
    print("passwords updated")