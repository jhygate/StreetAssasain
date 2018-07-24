import pickle
import os

def save_obj(obj,UserID,GameID,IorO):
    with open(IorO+str(GameID)+'/'+ str(UserID) + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(UserID,GameID,IorO):
    try:
        with open(IorO+str(GameID)+'/'+ str(UserID) + '.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return ([])

def append_to_buffer(toAppend,UserID,GameID,IorO):
    current = load_obj(UserID,GameID,IorO)
    current.append(toAppend)
    save_obj(current,UserID,GameID,IorO)

def empty_buffer(UserID,GameID,IorO):
    current = load_obj(UserID,GameID,IorO)
    if current != []:
        save_obj([], UserID,GameID,IorO)
    return current

def create_buffer(UserID,GameID,IorO):
    open(IorO+GameID+'/'+ UserID +".pkl",'a')
    save_obj([], UserID,GameID,IorO)

