# import modules
import random
import sys
import copy


class Game:
    "Tic-Tac-Toe class. This class holds the user interaction, and game logic"
    def __init__(self):
        self.board = [' '] * 9
        self.player_marker = ''
        self.bot_name = 'TBot'
        self.bot_marker = ''
        self.winning_combos = (
        [6, 7, 8], [3, 4, 5], [0, 1, 2], [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6],
    )
        self.corners = [0,2,6,8]
        self.sides = [1,3,5,7]
        self.middle = 4
        self.GameFinished=False
        self.form = '''
           \t| %s | %s | %s |
           \t-------------
           \t| %s | %s | %s |
           \t-------------
           \t| %s | %s | %s |
           '''

    def print_board(self,board = None):
        "Display board on screen"
        if board is None:
            return  self.form % tuple(self.board[6:9] + self.board[3:6] + self.board[0:3])
        else:
            # when the game starts, display numbers on all the grids
            return  self.form % tuple(board[6:9] + board[3:6] + board[0:3])

    def help(self):
        return '''
\n\t The game board has 9 sqaures(3X3).
\n\t Two players take turns in marking the spots/grids on the board.
\n\t The first player to have 3 pieces in a horizontal, vertical or diagonal row wins the game.
\n\t To place your mark in the desired square, simply type the number corresponding with the square on the grid
\n\t Press Ctrl + C to quit
'''

    def quit_game(self):
        "exits game"
        self.print_board
        return "\n\t Thanks for playing :-) \n\t Come play again soon!\n"

    def is_winner(self, board, marker):
        "check if this marker will win the game"
        # order of checks:
        #   1. across the horizontal top
        #   2. across the horizontal middle
        #   3. across the horizontal bottom
        #   4. across the vertical left
        #   5. across the vertical middle
        #   6. across the vertical right
        #   7. across first diagonal
        #   8. across second diagonal
        for combo in self.winning_combos:
            if (board[combo[0]] == board[combo[1]] == board[combo[2]] == marker):
                return True
        return False

    def get_bot_move(self):
        # check if bot can win in the next move
        for i in range(0,len(self.board)):
            board_copy = copy.deepcopy(self.board)
            if self.is_space_free(board_copy, i):
                self.make_move(board_copy,i,self.bot_marker)
                if self.is_winner(board_copy, self.bot_marker):
                    return i

        # check if player could win on his next move
        for i in range(0,len(self.board)):
            board_copy = copy.deepcopy(self.board)
            if self.is_space_free(board_copy, i):
                self.make_move(board_copy,i,self.player_marker)
                if self.is_winner(board_copy, self.player_marker):
                    return i

        # check for space in the corners, and take it
        move = self.choose_random_move(self.corners)
        if move != None:
            return move

        # If the middle is free, take it
        if self.is_space_free(self.board,self.middle):
            return self.middle


        # else, take one free space on the sides
        return self.choose_random_move(self.sides)

    def is_space_free(self, board, index):
        "checks for free space of the board"
        # print "SPACE %s is taken" % index
        return board[index] == ' '

    def is_board_full(self):
        "checks if the board is full"
        for i in range(1,9):
            if self.is_space_free(self.board, i):
                return False
        return True

    def make_move(self,board,index,move):
        board[index] =  move

    def choose_random_move(self, move_list):
        possible_winning_moves = []
        for index in move_list:
            if self.is_space_free(self.board, index):
                possible_winning_moves.append(index)
                if len(possible_winning_moves) != 0:
                    return random.choice(possible_winning_moves)
                else:
                    return None

    def start_game(self):
       "welcomes user, prints help message and hands over to the main game loop"
       welcomeScreen = '''\n\t-----------------------------------
                \n\t   TIC-TAC-TOE Game
                \n\t------------------------------------
             '''
       self.player_marker, self.bot_marker = "X","Y"
       if random.randint(0,1) == 0:
           bot_move =self.get_bot_move()
           self.make_move(self.board, bot_move, self.bot_marker)

           welcomeScreen+=self.help()
           welcomeScreen+=self.print_board()
           welcomeScreen+= "I moved first now its your turn \n \t"

       else:
           welcomeScreen+=self.help()
           welcomeScreen+=self.print_board(range(1,10))
           welcomeScreen+= "You will go first \n \t"
       return  welcomeScreen
    def check_valid_move(self,move):
        if(move not in [1,2,3,4,5,6,7,8,9] or not self.is_space_free(self.board,move-1)):
            return True
        else:
            return  False
    def make_moves(self,move):
        message=""
        move = int(move)
        #Player Movement
        self.make_move(self.board,(move - 1), self.player_marker)
        if(self.is_winner(self.board, self.player_marker)):
                   self.GameFinished=True
                   message=self.print_board()
                   message+= "\n\tCONGRATULATIONS %s, YOU HAVE WON THE GAME!!! \\tn"
        elif(self.is_board_full()):
                   self.GameFinished=True
                   message=self.print_board()
                   message=+ "\n\t-- Match Draw --\t\n"
        #Bot Movement
        else:
                   bot_move =  self.get_bot_move()
                   self.make_move(self.board, bot_move, self.bot_marker)
                   if (self.is_winner(self.board, self.bot_marker)):
                    self.GameFinished=True
                    message=self.print_board()
                    message=+ "\n\t%s HAS WON!!!!\t\n" % self.bot_name
                   else:
                    message=self.print_board()

        return {'message':message, 'resultBoolean':self.GameFinished}