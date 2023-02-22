from engine import Engine
class Chess:
    def __init__(self, time=5000, depth=100):
        self.engine = Engine(r"stockfish\stockfish-windows-2022-x86-64-avx2.exe", depth)
        self.piece_positions = [[0 for i in range(8)] for j in range(8)]
        self.start_pos()
        print(self.piece_positions)
        self.time = time
        self.depth = depth
    def get_visual(self):
        return self.engine.get_visual()
    def find_piece_move(self, move):
        move[0] = self.letter_to_number(move[0])
        move[2] = self.letter_to_number(move[2])
        if self.piece_positions[move[0]][move[1]] == "" and self.piece_positions[move[2]][move[3]] != "":
            out = move[2:4] + move[0:2]
            return out
        elif self.piece_positions[move[0]][move[1]] != "" and self.piece_positions[move[2]][move[3]] == "":
            out = move[0:2] + move[2:4]
            return out
        
    def move(self, move):
        move = move[0] + move[1]
        move = self.find_piece_move(move)
        if not self.engine.is_move_legal(move):
            return "Invalid move"
        self.engine.move(move)
        self.piece_positions[move[2]][move[3]], self.piece_positions[move[0]][move[1]] = self.piece_positions[move[0]][move[1]], self.piece_positions[move[2]][move[3]]
        return "valid move"
    def get_engine_move_time(self, time = None):
        if time is not None:
            return self.engine.get_best_move_time(time)
        move = self.engine.get_best_move_time(self.time)
        #if move is a take
        if self.piece_positions[move[2]][move[3]] != "":
            out = [move[2:4] + "00", move[0:2] + move[2:4]]
            return out
        return [move]
    
    def get_engine_move_depth(self, depth = None):
        if depth is not None:
            return self.engine.get_best_move_depth(depth)
        return self.engine.get_best_move_depth(self.depth)
    
        
    def letter_to_number(self, letter):
        if letter == "a":
            return 0
        elif letter == "b":
            return 1
        elif letter == "c":
            return 2
        elif letter == "d":
            return 3
        elif letter == "e":
            return 4
        elif letter == "f":
            return 5
        elif letter == "g":
            return 6
        elif letter == "h":
            return 7
    def number_to_letter(self, number):
        if number == 0:
            return "a"
        elif number == 1:
            return "b"
        elif number == 2:
            return "c"
        elif number == 3:
            return "d"
        elif number == 4:
            return "e"
        elif number == 5:
            return "f"
        elif number == 6:
            return "g"
        elif number == 7:
            return "h"
    def start_pos(self):
        Engine.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.piece_positions[0][0] = "R"
        self.piece_positions[0][1] = "N"
        self.piece_positions[0][2] = "B"
        self.piece_positions[0][3] = "Q"
        self.piece_positions[0][4] = "K"
        self.piece_positions[0][5] = "B"
        self.piece_positions[0][6] = "N"
        self.piece_positions[0][7] = "R"
        self.piece_positions[1][0] = "P"
        self.piece_positions[1][1] = "P"
        self.piece_positions[1][2] = "P"
        self.piece_positions[1][3] = "P"
        self.piece_positions[1][4] = "P"
        self.piece_positions[1][5] = "P"
        self.piece_positions[1][6] = "P"
        self.piece_positions[1][7] = "P"
        self.piece_positions[6][0] = "p"
        self.piece_positions[6][1] = "p"
        self.piece_positions[6][2] = "p"
        self.piece_positions[6][3] = "p"
        self.piece_positions[6][4] = "p"
        self.piece_positions[6][5] = "p"
        self.piece_positions[6][6] = "p"
        self.piece_positions[6][7] = "p"
        self.piece_positions[7][0] = "r"
        self.piece_positions[7][1] = "n"
        self.piece_positions[7][2] = "b"
        self.piece_positions[7][3] = "q"
        self.piece_positions[7][4] = "k"
        self.piece_positions[7][5] = "b"
        self.piece_positions[7][6] = "n"
        self.piece_positions[7][7] = "r"

chess = Chess()
list = ["e", 2, "e", 4]
#make list a string

        
