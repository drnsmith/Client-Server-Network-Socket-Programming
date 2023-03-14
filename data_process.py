'''This is  a module that has shared data type, and then the client and server can communicate with that type.'''
import json, pickle
class ProcessData:
    dd = {1: "one", 2: "two", 3: "three", 4: "four"}3 dict. to be sent to server
    dict = json.dumps(dd)
    def __init__(self, data= dict):
        self.data = data
    def __str__(self): return self.data
