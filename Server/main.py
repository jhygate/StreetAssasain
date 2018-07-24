"""HERES THE PLAN! WE ARE ON V0.0000001
Ignore fancy GUI, we are gonna make it as text based as possible!, DONT THINK ABOUT THE PHOTOS WE JUST NEED TO PUT IT IN A DICTIONARY THEN ITS FINE
ToDo:
- Create an API system acting as a socket {This seems sketchy as anything but if it works who cares}
    - Poll a GET request on the API which checks a command buffer file
    - POST request just appends to a cmd file
    - Poll from the server check files for cmds and excecute
-Work thorugh slowly, to create the correct dictionaries we need!

FAR FAR FUTURE:
-Add SQL back in
-Make it OOP
-Make a nice GUI (tkinter, then ...kivvy?)

ENDGAME, Dont stretch too far cos this is kinda tricky:
-CRI
    """



import time
import BufferManagement
import os

def SetupGame(gameID,timeout,amount_players): #Getting FREAKY with yo double variable names brah
    """Gathers all mah lovely players and return a beautifull list
    That list contains a bunch of dictionaries containg all the data you could ever want as a whopping DICT
    Needs to:
    - Create Buffer File ('IN' and 'OUT')"""
    GameInfo = {'StartTime':time.time(),
                'timeout':timeout,
                'ID':gameID}
    player = {'connection' : ''}
    livingPlayers = []
    for i in range(amount_players):
        livingPlayers.append(player)
    return livingPlayers, GameInfo

def listen(livingPlayers):
    """Either:
    - Repeatedly check for change in DB (If API affects DB)
    - Listen to the Sockets """
    for player in livingPlayers:
        messages = BufferManagement.empty_buffer(player['UserID'],player['GameID'],"IN")
        if messages != []:
            return messages, player

def GetPlayerForID(livingPlayers,ID):
    for player in livingPlayers:
        if player['ID'] == ID:
            return player

def send(User,data):
    """Sends the given data to the specified user... pretty simple"""
    BufferManagement.append_to_buffer(data,User)
    pass

def GiveTarget(livingPlayers,ID):
    """returns the new target of the specified ID
        OH! Its gonna do this in a simple way for now:
        -target = player one above in list of players"""
    player = GetPlayerForID(ID)
    target = livingPlayers[((livingPlayers.index(player))+1)%len(livingPlayers)]['ID']
    livingPlayers[livingPlayers.index(player)]['target'] = target
    return target

    pass

def RemoveKill(livingPlayers,vote): #Do ya need a function for this? Freaky python connections might get wierd (+ double V name)
    """So a votes just finished and you need to tell people what happend:
    - Tell target they are dead
    - remove target from game(just take em awy from that one list?)
    - Tell player that they killed em, give em a new target for their GUI"""
    send(GetPlayerForID(vote['target'])['connection'],"YOU ARE DEAD")
    livingPlayers.remove(vote['target'])
    send(GetPlayerForID(vote['killer'])['connection'],GiveTarget(vote['killer']))
    return livingPlayers

def SurviveKill(livingPlayers,vote): #Do ya need a function for this? Freaky python connections might get wierd (+ double V name)
    """So a votes just finished and you need to tell people what happend:
    - Tell target they are ALIVE
    - Tell player that they FAILED"""
    send(vote['target'],"YOU ARE ALIVE")
    send(vote['killer'],"KILL FAILED")
    return livingPlayers

def VoteInfo(KillPic):
    """Creates and returns the whopper of a dict that is VOTEINFO!! YAAAAY LOOK AT ALL THAT INFO IN AN EASILY ACCESIBLE LIST ITS NOT SLOPPY AT ALL HOW DARE YOU SAY THAT"""
    killer, target, KillPic, timeout = ""
    return killer,target,KillPic,timeout

def SendKill(UserMessage):
    """Begin the voting chain, send the intial vote to the target"""
    send(UserMessage['target'],VoteInfo(UserMessage['KillPic']))

def EndCriteria(Vote):
    """Checks if the vote is done yet, its bored and wants to go home"""
    if (time.time() - Vote['VoteInfo']['timeout']) < Vote['VoteInfo']['StartTime']:
        return True
    if Vote['TotalVotes'] == len(livingPlayers)-2:
        return True


def Vote1(UserMessage):
    """OMG TARGET JUST REPLIED TO THEIR OWN DEATH WE GOTTA DO SOME STUFF:
    - If they dead... Kill em
    - Create a vote array 4 keeping track of developments
    - Send this super exciting new vote to all my happy players"""
    if UserMessage['Vote'] == True:
        RemoveKill(livingPlayers, UserMessage['ID'])
    else:
        CurrentVotes.append({'VoteInfo':UserMessage['VoteInfo'],
                            'Tally':0,
                            'TotalVotes':0}) #[0] whatever Vote info ya want, [1] Tally, [2] How many have voted
        for player in livingPlayers:
            if player == UserMessage['killer'] or player == UserMessage['target']:
                pass
            else:
                send(player['connection'],UserMessage['VoteInfo'])


def Vote2(UserMessage):
    """YAAAAY ONE OF MY PLAYERS LISTENED TO ME AND REPLIED <3:
    - Update Server voteing record
    - Finish the vote if its done"""
    for vote in CurrentVotes:
        if UserMessage['VoteInfo'] == vote['VoteInfo']:
            if UserMessage['Vote'] == True:
                vote['Tally'] += 1
                vote['TotalVotes'] += 1
            if UserMessage['Vote'] == False:
                vote['Tally'] -= 1
                vote['TotalVotes'] += 1
        if EndCriteria(vote):
            if vote['Tally'] >= 1:
                RemoveKill(livingPlayers,vote['VoteInfo'])
            else:
                SurviveKill(livingPlayers,vote['VoteInfo'])
            CurrentVotes.remove(vote)

def DataPLZ(UserMessage):
    player = GetPlayerForID(livingPlayers, UserMessage['ID'])
    send(player['connection'],player)

def execute(UserMessage,player):
    """Just decluttering code, checks which Server actoin to run"""
    if UserMessage['Action'] == "Kill": #This list represents the commands file I had before, neater that way?
        SendKill(UserMessage)
    if UserMessage['Action'] == 'Vote1':
        Vote1(UserMessage)
    if UserMessage['Action'] == 'Vote2':
        Vote2(UserMessage)
    if UserMessage['Action'] == "DataPLZ":
        DataPLZ(UserMessage)
    pass

def IsGameRunning(livingPlayers):
    if len(livingPlayers) == 1:
        return False,"1P"
    elif time.time() - GameInfo['timeout'] < GameInfo['StartTime']:
        return False,"Timeout"
    else:
        return True,""

gameID = int(input("gameID?"))
timeout = int(input("timeout?"))
amount_players = int(input("how many players?"))

livingPlayers, GameInfo = SetupGame(gameID,timeout,amount_players)
GameRunning = True
CurrentVotes = []
while GameRunning:
    UserMessages, player = listen(livingPlayers)
    for message in UserMessages:
        execute(message,player)
    GameRunning, reason = IsGameRunning(livingPlayers)
for player in livingPlayers:
    send(player['connection'],reason)
os.rmdir('obj'+GameInfo['gameID'])

