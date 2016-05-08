import SocketServer
import socket
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
from GameEngine import  Game
# Threaded mix-in
class MultiThreadedXMLRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer): pass

# Example class to be published

def startNewGame():
        TicTacToe = Game()
        get_remote_machine_info()
        TicTacToe.start_game()
        return "Ok"


def get_remote_machine_info():
    remote_host = 'www.python.org'
    try:
        print "IP address: %s" %socket.gethostbyname(remote_host)
    except socket.error, err_msg:
        print "%s: %s" %(remote_host, err_msg)



# Instantiate and bind to localhost:8079
server = MultiThreadedXMLRPCServer(('', 8000), SimpleXMLRPCRequestHandler)

server.register_introspection_functions()

server.register_function(startNewGame)
# run!
server.serve_forever()