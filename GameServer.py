from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib
from GameEngine import  Game
class Poco:
 def __init__(self):
    self.TicTacToe = Game()
 def startGame(self):
    return self.TicTacToe.start_game()
 def makeMove(self,move):
    if(not self.TicTacToe.check_valid_move(move) == True):
     raise xmlrpclib.Fault(11, "some message")
     return self.TicTacToe.make_moves(move)
 def endGame(self):
     value=None
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler,allow_none=True)
server.register_introspection_functions()

server.register_instance(Poco())
server.serve_forever()

class MyException(Exception):
    pass