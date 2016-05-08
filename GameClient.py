import xmlrpclib

server = xmlrpclib.ServerProxy('http://localhost:8000')
server.startNewGame();