import xmlrpclib
class GameClient:
     def __init__(self):
        self.uniqueId = None
        self.server=  xmlrpclib.ServerProxy('http://localhost:8000')
     def startGame(self):
         self.server = xmlrpclib.ServerProxy('http://localhost:8000')
         self.uniqueId=self.server.authenticate()
         result= self.server.start_new_game(self.uniqueId)
         resultBoolean=result["resultBoolean"]
         message=result["message"]
         return {'message':message, 'resultBoolean':resultBoolean}

     def makeMove(self,move):
         result=self.server.make_move(move,self.uniqueId)
         resultBoolean=result["resultBoolean"]
         message=result["message"]
         return {'message':message, 'resultBoolean':resultBoolean}
     def endGame(self):
         self.server.end_game(self.uniqueId)
#Client Loop
while(True):
 choiceVar = raw_input("Enter 1 : Start The Tic Tac Toe Game"+
                    "\n"+"Enter 2 : Exit"+
                    "\n"
                    )
 if(choiceVar=="2"):
  break
 if(choiceVar!="1"):
   continue
 gameClient=GameClient()
 result= gameClient.startGame()
 isGameCanBePlayed=result["resultBoolean"]
 if(not isGameCanBePlayed):
    print(result["message"])
 else:
  print(result["message"])
  gameFinished=False
  while not gameFinished:
   try:
     move=int(input("Please make your move"))
     result=gameClient.makeMove(move)

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
        gameClient.endGame()

