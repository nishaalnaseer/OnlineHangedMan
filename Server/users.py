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

def createUsers(newUsers):
    """create users from input"""
    oldUsers = loadUsers()

    for userName, passWord in newUsers.items():
        oldUsers.update({userName: passWord})
    
    saveUsers(oldUsers)
    print("users created")

def updatePassword(updates):
    """updates existing password of users"""
    oldData = loadUsers()

    for userName, passWord in updates.items():
        oldData[userName] = passWord
    
    saveUsers(oldData)
    print("passwords updated")

loggedIn = []
def logged(userName="", password="", mode='r'):
    """return the list of users logged with mode 'r', and add a user to the 
    list with 'a'"""

    if mode == "a":
        if password == "" or userName == "":
            print("Mode 'a' incompatible with empty username or password")
            return "Mode 'a' incompatible with empty username or password"
        else:
            users = loadUsers()
            passwordOnFile = users[userName]

            if password != passwordOnFile:
                return "code0004:c"
            else:
                loggedIn.append(userName)
                return "code0004:s"

    else 'r':
        return loggedIn
