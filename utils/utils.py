import pickle
import sys
import json
import numpy as np
import marshal

def print_error(line):
    print >> sys.stderr, line

def save_obj(obj, name ):
    with open('obj/' + name + '.pkl', 'wb') as f:
        marshal.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return marshal.load(f)


"""
def save_obj(obj, name ):
    with open('obj/' + name + '.json', 'w') as f:
        json.dump(obj, f, encoding="ISO-8859-1")#, pickle.HIGHEST_PROTOCOL)


def load_obj(name ):
    with open('obj/' + name + '.json', 'r') as f:
        return json.load(f)


"""
"""
def save_obj(obj, name ):
    np.save('obj/'+name+'.npy', obj)



def load_obj(name):
    return np.load('obj/'+name+'.npy').item()
"""