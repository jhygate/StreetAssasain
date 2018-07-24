"""ToDo:
- Append Votes to Vote List
- Add Vote Command"""



import httplib2
import urllib
import json
import base64

import sys
import time
import ast



def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0)
    sys.stdout.write('\033[93m')

delay_print("")
delay_print("Hello There \n")
delay_print("Welcome to S.T.R.E.E.T A.S.S.A.S.I.A.N ........\n")
delay_print("USER ID:")
UserID = input("$")
delay_print("GAME ID:")
GameID = input("$")




def HelpText():
    delay_print("You can:\n")
    delay_print("-JoinGame: JoinGame Profile_pic\n")
    delay_print("-GetCommand: GetCommand \n")
    delay_print("-Vote: Vote  voteObj\n")
    delay_print("-KillTarget: KillTarget KillPic\n")
    delay_print("-Help: Help\n")
    delay_print("-ShowVotes: ShowVotes\n")

HelpText()

def JoinGame(UserID, GameID, Profile_pic):
    data = {'ID': UserID,
            'GameID': GameID,
            'target': 0,
            'ProfilePic': Profile_pic}
    url = 'http://127.0.0.1:5002/JoinGame/' + UserID + '/' + GameID
    content = http.request(url, "POST", json.dumps(data))
    return content

def GetCommand(UserID, GameID):
    url = 'http://127.0.0.1:5002/GetCommand/' + UserID + '/' + GameID
    content = (http.request(url,"GET"))
    out = (ast.literal_eval(content[1].decode('utf-8')))
    print(out)
    print(type(out))
    return out

def Vote(Vote,voteObj):
    voteObj['vote'] = vote

def KillTarget(UserID,GameID,KillPic):
    url = 'http://127.0.0.1:5002/Kill/' + UserID + '/' + GameID
    data = {'Action': 'Kill',
            'KillPic': KillPic}
    content = http.request(url, "POST", json.dumps(data))


running = True
http = httplib2.Http()
votes = []
while running:
    usrinput = input("$")
    commands = usrinput.split()

    if usrinput != "":
        if commands[0] == "JoinGame":
            out = JoinGame(UserID, GameID, commands[1])
            if out[0]['status'] == '200':
                delay_print("Join Success\n")
            else:
                delay_print("Join Failure\n")

        if commands[0] == "GetCommand":
           #delay_print(GetCommand(UserID,GameID))
            pass

        if commands[0] == "Vote":
            pass
        if commands[0] == "KillTarget":
            KillTarget(UserID,GameID,commands[1])
        if commands[0] == "Help":
            HelpText()
        if commands[0] == "ShowVotes":
            print("Current Votes:",votes)
    server_commands = GetCommand(UserID, GameID)
    print(server_commands)
    for command in server_commands:
        command = ast.literal_eval(str(command))
        if command != []:
            if command['type'] == "vote":
                votes.append(server_commands)
            delay_print(("new command:",str(command)+"\n"))

