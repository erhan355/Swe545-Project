import xmlrpclib
class GameClient:
     def startGame(self):
         server.startNewGame();
server = xmlrpclib.ServerProxy('http://localhost:8000')
print server.startGame()
gameFinished=False
while not gameFinished:

 try:
   move=int(input("Please make your move"))
   result=server.makeMove(move)

   if(result["resultBoolean"]):
     gameFinished=True
   print result["message"]
 except xmlrpclib.Fault as err:
    if(err.faultCode==11):
       print ("Invalid move. Please try again: (1-9)")
    else:
       print "A fault occurred"
       print "Fault code: %d" % err.faultCode
       print "Fault string: %s" % err.faultString
       gameFinished=True
    server.endGame()
