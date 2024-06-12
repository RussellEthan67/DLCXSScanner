import mysql.connector
import json
from colorama import Fore, init

init(autoreset=True)

dangerous_characters = [">", "'", '"', "<", "/", ";"]


def read_payload_file(file_name, cursor, uidu):
    try:
        with open(file_name, 'r') as f:
            for line in f:
                try:
                    payload, waf = line.strip().split(' | ')
                except ValueError:
                    payload = line
                    waf = "None"
                print(f"Payload: {payload} , WAF: {waf}")
                command = "INSERT INTO QueryList (QueryValue, UpdownVote, UserID, WAF) VALUES (%s, 0, %s, %s)"
                cursor.execute(
                    command, (payload, waf, uidu))
                print(Fore.GREEN + "Successfully contributed a payload")
    except FileNotFoundError:
        print(Fore.RED + f"File '{file_name}' not found.")


def add_payload(payload: str = None,  waf: str = None, filename: str = None,) -> None:
    if waf:
        waf = waf.lower()

    if filename:
        with open(filename, "r") as payloads:
            payloads = payloads.readlines()

        for payload in payloads:
            new_data = {"Payload": payload,
                        "Attribute": [], "count": 0, "waf": waf}

            for char in payload:
                if char in dangerous_characters:
                    if char in new_data["Attribute"]:
                        pass
                    else:
                        new_data["Attribute"].append(char)

            f = open("payloads.json", 'a+')
            data = json.load(f)
            data.append(new_data)
            with open("payloads.json", "w") as write_data:
                json.dump(data, write_data, indent=4)
    else:
        new_data = {"Payload": payload,
                    "Attribute": [], "count": 0, "waf": waf}

        for char in payload:
            if char in dangerous_characters:
                new_data["Attribute"].append(char)

        f = open("payloads.json", 'a+')
        f.seek(0)
        if f.read(1):
            f.seek(0)
            data = json.load(f)
        else:
            data = []
        data.append(new_data)
        with open("payloads.json", "w") as write_data:
            json.dump(data, write_data, indent=4)


def login(user, password):
    Connect = mysql.connector.connect(host="103.185.53.64", user="xsspaylo_admin", passwd="admin123xsspaylo",
                                      database="xsspaylo_xsspayloadsubmitter")

    cursor = Connect.cursor()

    command = "use xsspaylo_xsspayloadsubmitter"
    cursor.execute(command)

    command = "select * from Users where UserName=%s and UserPassword=%s"
    cursor.execute(command, (user, password))
    result = cursor.fetchone()

    if result == None:
        print(Fore.RED + "Invalid username or password!")
    else:
        print(Fore.GREEN + "Successfully login!")
        return result


def register(user, password):
    role = "user"

    Connect = mysql.connector.connect(host="103.185.53.64", user="xsspaylo_admin", passwd="admin123xsspaylo",
                                      database="xsspaylo_xsspayloadsubmitter")
    cursor = Connect.cursor()

    command = "use xsspaylo_xsspayloadsubmitter"
    cursor.execute(command)
    command = "INSERT INTO Users (UserName, UserPassword, UserRole) VALUES (%s, %s, %s)"
    cursor.execute(command, (user, password, role))
    command = "SELECT * FROM Users WHERE UserName=%s AND UserPassword=%s"
    cursor.execute(command, (user, password))
    result = cursor.fetchone()

    if result == None:
        print(Fore.RED + "Failed registering users!")
    else:
        print(Fore.GREEN + "Successfully Registered!")


def query():
    Connect = mysql.connector.connect(host="103.185.53.64", user="xsspaylo_admin", passwd="admin123xsspaylo",
                                      database="xsspaylo_xsspayloadsubmitter")
    cursor = Connect.cursor(buffered=True)
    command = "use xsspaylo_xsspayloadsubmitter"
    cursor.execute(command)
    command = "SELECT * FROM QueryList"
    cursor.execute(command)
    result = cursor.fetchall()
    print("Payload List:")
    for row in result:
        print("ID = ", row[0], "\t", "Query = ",
              row[1], "\t", "WAF = ", row[4])
    if uid is None:
        pass
    else:
        uidu = uid[0]
        if uidu != 0:
            while True:
                print("1. Contribute new payload")
                print("2. Upvote or down vote")
                print("3. Download payload locally")
                print("4. Back")
                user_input = input("Select Option: ")
                try:
                    user_input = int(user_input)
                except ValueError:
                    print(Fore.RED + "Invalid input please try again!")
                else:
                    user_input = int(user_input)
                    if user_input == 1:
                        print("1. Contribute a single payload")
                        print("2. Contribute a file of payload")
                        inp = int(input("Select Option: "))
                        if inp == 1:
                            payload_input = str(input("Type your Payload: "))
                            waf_input = str(input("Type your WAF: "))
                            command = "INSERT INTO QueryList (QueryValue, WAF, UpdownVote, UserID) VALUES (%s, %s, 0, %s)"
                            cursor.execute(
                                command, (payload_input, waf_input, uidu))
                            print(Fore.GREEN + "Successfully contributed a payload")
                        elif inp == 2:
                            print(Fore.RED +
                                  "Make sure your payload file is formatted correctly ( Payload | WAF )")
                            file_input = str(input("Type your payload file: "))
                            read_payload_file(file_input, cursor, uidu)
                    elif user_input == 2:
                        print(
                            "Select the Payload then press 1 to Upvote and 2 to Down-vote")
                        user_input = input("Select Payload: ")
                        Updownvote = input("Upvote or Down-vote: ")
                        try:
                            user_input = int(user_input)
                            Updownvote = int(Updownvote)
                        except ValueError:
                            print(Fore.RED + "Invalid input, please try again!")
                        else:
                            user_input = int(user_input)
                            Updownvote = int(Updownvote)
                            command = "SELECT ud.UpdownVote FROM QueryList q, UpdownVoteList ud WHERE q.QueryID = ud.QueryID AND ud.UserID = %s AND ud.QueryID = %s"
                            cursor.execute(command, (uidu, user_input))
                            res = cursor.rowcount
                            command = "SELECT MAX(QueryID) FROM QueryList"
                            cursor.execute(command)
                            maxID = cursor.fetchone()
                            if user_input > maxID[0]:
                                print(
                                    Fore.RED + "Please enter the id within the range between 1 -", maxID[0])
                            elif Updownvote != 1 and Updownvote != 2:
                                print(
                                    Fore.RED + "Please enter only 1 or 2 to upvote or down-vote")
                            else:
                                if res == 0:
                                    if Updownvote == 2:
                                        command = "UPDATE QueryList SET UpdownVote = UpdownVote - 1 WHERE QueryID = %s"
                                        cursor.execute(command, (user_input,))
                                        command = "INSERT INTO UpdownVoteList (UserID, QueryID, UpdownVote) VALUES (%s, %s, %s)"
                                        cursor.execute(
                                            command, (uidu, user_input, Updownvote))
                                        print(
                                            Fore.GREEN + "Successfully down-voted this payload.")
                                    elif Updownvote == 1:
                                        command = "UPDATE QueryList SET UpdownVote = UpdownVote + 1 WHERE QueryID = %s"
                                        cursor.execute(command, (user_input,))
                                        command = "INSERT INTO UpdownVoteList (UserID, QueryID, UpdownVote) VALUES (%s, %s, %s)"
                                        cursor.execute(
                                            command, (uidu, user_input, Updownvote))
                                        print(Fore.GREEN +
                                              "Successfully upvote this payload.")
                                else:
                                    if Updownvote == 2:
                                        command = "UPDATE UpdownVoteList ud, QueryList q SET ud.UpdownVote = 2, q.UpdownVote = q.UpdownVote - 1 WHERE ud.QueryID = q.QueryID AND ud.UserID = %s;"
                                        cursor.execute(command, (uidu,))
                                        print(
                                            Fore.GREEN + "Successfully down-voted this payload.")
                                    elif Updownvote == 1:
                                        command = "UPDATE UpdownVoteList ud, QueryList q SET ud.UpdownVote = 1, q.UpdownVote = q.UpdownVote + 1 WHERE ud.QueryID = q.QueryID AND ud.UserID = %s;"
                                        cursor.execute(command, (uidu,))
                                        print(
                                            Fore.GREEN + "Successfully upvote this payload.")
                    elif user_input == 3:
                        print("1. Download every single payload")
                        print("2. Download certain payload")
                        inx = int(input("Select Option: "))
                        if inx == 1:
                            for row in result:
                                payload = row[1]
                                waf = row[4]
                                add_payload(payload, waf)
                            print(
                                Fore.GREEN + 'Successfully download every payload locally.')
                        elif inx == 2:
                            user_inp = input(
                                "Type WAF payload you want to download: ")
                            i = 0
                            for row in result:
                                if row[1] == user_inp:
                                    i = i + 1
                                    payload = row[1]
                                    waf = row[4]
                                    add_payload(payload, waf)
                            if i == 0:
                                print(Fore.RED +
                                      f"No {user_inp} payload can be found")
                    else:
                        break


def leaderboard():
    Connect = mysql.connector.connect(host="103.185.53.64", user="xsspaylo_admin", passwd="admin123xsspaylo",
                                      database="xsspaylo_xsspayloadsubmitter")
    cursor = Connect.cursor()
    command = "use xsspaylo_xsspayloadsubmitter"
    cursor.execute(command)
    command = "SELECT u.UserName,SUM(q.UpdownVote) AS Points FROM QueryList q, Users u WHERE q.UserID = u.UserID GROUP BY q.UserID DESC"
    cursor.execute(command)
    result = cursor.fetchall()
    print("Leaderboard:")
    for row in result:
        print("Username = ", row[0], "\t", "Points = ", row[1])


uid = None


def main():
    global uid
    if uid is None:
        print("1. Login")
        print("2. Register")
        print("3. Payload List")
        print("4. Leader Board")
        print("5. Exit")
        user_input = input("Select Option: ")
        try:
            user_input = int(user_input)
        except ValueError:
            print(Fore.RED + "Invalid input, please try again!")
        else:
            user_input = int(user_input)
            if user_input == 1:
                user = input("Input username: ")
                password = input("Input password: ")
                uid = login(user, password)
            elif user_input == 2:
                user = input("Input username: ")
                password = input("Input password: ")
                register(user, password)
            elif user_input == 3:
                query()
            elif user_input == 4:
                leaderboard()
            elif user_input == 5:
                print("Returning to main menu....")
                return 1
            else:
                print("Other choice")

    else:
        print("1. Logout")
        print("2. Payload List")
        print("3. Leader Board")
        print("4. Exit")
        user_input = input("Select Option: ")
        try:
            user_input = int(user_input)
        except ValueError:
            print(Fore.RED + "Invalid input. Please try again!")
        else:
            user_input = int(user_input)
            if user_input == 1:
                uid = None
            elif user_input == 2:
                query()
            elif user_input == 3:
                leaderboard()
            elif user_input == 4:
                print("Returning to main menu...")
                return 1
            else:
                print(Fore.RED + "Please choose other choice")


def start():
    while True:
        values = main()
        if values == 1:
            break
