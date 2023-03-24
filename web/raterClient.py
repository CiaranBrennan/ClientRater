import requests
import json
import ast

username = ""
loggedIn = False

def main():
    while 1:
        print("""\nWelcome to Professor Rate
Please select what you would like to do:
register - Register an account on the system
login [url] - Login to the service hosted at the provided address
quit - Terminate the program""")
        userInput = input()
        choice = userInput.split(" ")

        if choice[0] == "login":
            if len(choice) != 1:
                login(choice[1])
            else:
                print("Please provide the URL of the web server.\n")

        elif choice[0] == "register":
            register()

        elif choice[0] == "quit":
            quit()

        else:
            print("\nInvalid option entered. Please try again.\n")


def register():
    url = "sc17cjb.pythonanywhere.com"
    username = ""
    while username != 'b':
        username = input("\nPlease enter your desired username (enter 'b' to go back):\n")
        if username == 'b':
            continue
        email = input("Please enter your email address:\n")
        password = input("Please enter your desired password:\n")
        passConfirm = input("Please confirm your password:\n")

        if password == passConfirm:
            body = {
            "username":username,
            "email": email,
            "password":password
            }

            try:
                regRequest = requests.post("http://" + url + "/api/register/", json = body)
            except:
                print("No API could be found at the given URL. Please try again.")
            if regRequest.text == "1":
                print("Account registered. Please log in.")
                login(url)
            else:
                print("An account with that username or email address already exists.\nPlease try again with different details or log in.\n")
        else:
            print("The passwords do not match, please try again")

def login(url):
    global username
    try:
        connTest = requests.get("http://" + url + "/api/")
    except:
        print("No API could be found at the given URL. Please try again.")
        return
    username = ""
    while username != 'b':
        username = input("\nConnected.\n\nPlease enter your username (type 'b' to return):\n")
        if username == 'b':
            continue
        password = input("\nPlease enter your password:\n")
        body = {
        "username":username,
        "password":password
        }
        loginRequest = requests.post("http://" + url + "/api/login/", json = body)
        if loginRequest.text == "1":
            rateMenu(url)
        else:
            print("Username or password incorrect. Please try again")


def rateMenu(url):
    global username
    choice = [""]
    while choice[0] != "logout":
        print("""\nLogged in as %s. Please select what you would like to do:
list - View all module instances and the professors teaching each one

view - View the overall rating of every professor in the system

average [professor code] [module code] - View the overall rating of a specific professor in a specific module

rate [professor code] [module code] [year] [semester] [rating] - Give a rating out of 5 to a professor in the given instance

logout - Log out of your account""" %username)
        userInput = input()
        choice = userInput.split(" ")
        if choice[0] == "list":
            instList(url)
        elif choice[0] == "view":
            viewList(url)
        elif choice[0] == "average":
            if len(choice) == 3:
                average(url, [choice[1], choice[2]])
            else:
                print("Invalid use of average.\nPlease use the format defined above.\n")
        elif choice[0] == "rate":
            if len(choice) == 6:
                rate(url, [choice[1], choice[2], choice[3], choice[4], choice[5]])
        elif choice[0] == "logout":
            username = 'b'
        else:
            print("Invalid option selected. Please try again.")

def instList(url):
    instRequest = requests.get("http://" + url + "/api/list/")
    instances = ast.literal_eval(instRequest.text)
    print("=" * 75)
    print("{:^5s}{:^25s}{:^5s}{:^10s}{:^30s}".format("Code", "Module", "Year", "Semester", "Taught By"))
    print("=" * 75)
    for instance in instances:
        if len(instance[4]) < 3:
            print("{:<5s}{:^25s}{:^5d}{:^10d}{:^30s}".format(instance[0], instance[1], instance[2], instance[3], instance[4][0] + ", Professor " + instance[5][0]))
            for i in range(1, len(instance[4])):
                print("{:<5s}{:^25s}{:^5s}{:^10s}{:^30s}\n".format("","" ,"" ,"" ,instance[4][1] + ", Professor " + instance[5][i]))
        else:
            print("{:<5s}{:^25s}{:^5d}{:^10d}{:^30s}\n".format(instance[0], instance[1], instance[2], instance[3], instance[4] + ", Professor " + instance[5]))

def viewList(url):
    viewRequest = requests.get("http://" + url + "/api/view/")
    professors = ast.literal_eval(viewRequest.text)
    print("=" * 40)
    print("{:^5s}{:^25s}{:<10s}".format("Code", "Professor", "Rating"))
    print("=" * 40)
    for professor in professors:
        print("{:<5s}{:^25s}{:^5s}".format(professor[0], professor[1], "*" * professor[2]))

def average(url, params):
    body = {
        "professor":params[0],
        "module":params[1]
    }
    avgRequest = requests.get("http://" + url + "/api/average/", json = json.dumps(body))
    if avgRequest.text == "0":
        print("No professor with the given code teaches the given module, please try again.\n")
    else:
        data = ast.literal_eval(avgRequest.text)
        print("\nThe rating of Professor %s (%s) in %s (%s) is %s" %(data[1], data[0], data[3], data[2], "*" * data[4]))

def rate(url, params):
    body = {
        "user":username,
        "professor":params[0],
        "module":params[1],
        "year":params[2],
        "semester":params[3],
        "rating":params[4]
    }
    rateRequest = requests.post("http://" + url + "/api/rate/", json = body)
    if rateRequest.text == "1":
        print("Rating successfully added.\n")
    elif rateRequest.text == "-1":
        print("Invalid value for rating. Please enter a number between 1 and 5 inclusive.\n")
    elif rateRequest.text == "-2":
        print("Invalid value for semester. Please either enter 1 or 2.\n")
    elif rateRequest.text == "-3":
        print("No instance with the given information was found. Please try again.\n")
    elif rateRequest.text == "-4":
        print("You have already rated that module, please try a different one.\n")
    else:
        print("An unknown error occurred, please try again.\n")

if __name__ == '__main__':
    main()
