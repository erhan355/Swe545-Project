from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib
import threading
import uuid
from uuid import getnode as get_mac
import random


from GameEngine import  Game
class WorkerThread(threading.Thread):
    def __init__(self,tictactoe):

        self.TicTacToe = tictactoe
        threading.Thread.__init__(self)

    def startGame(self):
        return self.TicTacToe.start_game()
    def makeMove(self,move):
        if(not self.TicTacToe.check_valid_move(move) == True):
            raise xmlrpclib.Fault(11, "Invalid Move")
        else:
            result=self.TicTacToe.make_moves(move)
            resultBoolean=result["resultBoolean"]
            message=result["message"]
        return {'message':message, 'resultBoolean':resultBoolean}
    def endGame(self):
        value=None
class ThreadManager():
    def __init__(self):
        self.threadsDictionary = {}
        self.uniqueId = None
        self.dictionaryLock = threading.Lock()

    def authenticate(self):
        self.uniqueId =  random.getrandbits(16)
        #If this key presents in the dictionary try again
        while(self.threadsDictionary.has_key(self.uniqueId)):
            self.uniqueId=random.getrandbits(16)
        self.dictionaryLock.acquire()
        self.threadsDictionary[self.uniqueId]=None
        self.dictionaryLock.release()
        return self.uniqueId

    def start_new_game(self,uniqueId):
        if(not self.threadsDictionary.__len__()<=50):
            message= "The game server can't accept connections at the right now"
            resultBoolean=False
            return {'message':message, 'resultBoolean':resultBoolean}

        if(self.threadsDictionary.has_key(uniqueId)):
         game = Game()
         thread = WorkerThread(game)
         self.dictionaryLock.acquire()
         self.threadsDictionary[self.uniqueId] = thread
         self.dictionaryLock.release()
         thread.start()
         message= thread.startGame()
         resultBoolean=True
         return {'message':message, 'resultBoolean':resultBoolean}
        else:
    #Todo
    def end_game(self,uniqueId):
        thread = self.threadsDictionary[uniqueId]
        #Object is nullified
        thread.TicTacToe=None
        #Key is removed from dictionary
        self.dictionaryLock.acquire()
        self.threadsDictionary.pop(uniqueId,None)
        self.dictionaryLock.release()
    def make_move(self,move,uniqueId):
        print(threading.activeCount())
        thread = self.threadsDictionary[uniqueId]
        result=thread.makeMove(move)
        resultBoolean=result["resultBoolean"]
        message=result["message"]
        return {'message':message, 'resultBoolean':resultBoolean}

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler,allow_none=True)
server.register_introspection_functions()

server.register_instance(ThreadManager())
server.serve_forever()
