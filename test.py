import ast
thingy ="{'KillPic': ':j', 'ProfilePic': ':0', 'Vote': '', 'killer': '2', 'starttime': 1532361934.4675279, 'target': '1', 'timeout': 100, 'type': 'vote'}"
thing = ast.literal_eval(thingy)
print(thing['KillPic'])
