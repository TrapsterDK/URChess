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
        #move_coord = self.get_coord(move)
        print(move)
        sqr_1 = self.engine.stockfish.get_what_is_on_square(move[0:2])
        sqr_2 = self.engine.stockfish.get_what_is_on_square(move[2:4])
        if sqr_1 == None and sqr_2 != None:
            out = move[2:4] + move[0:2]
            return out
        elif sqr_1 != None and sqr_2 == None:
            out = move[0:2] + move[2:4]
            return out
        elif sqr_1 == None and sqr_2 == None:
            return "Invalid move"
        elif sqr_1.value.isupper() and sqr_2.value.islower():
            out = move[0:2] + move[2:4]
            return out
        elif sqr_1.value.islower() and sqr_2.value.isupper():
            out = move[2:4] + move[0:2]
            return out
        '''
        if self.piece_positions[int(move_coord[1])][int(move_coord[0])] == 0 and self.piece_positions[int(move_coord[3])][int(move_coord[2])] != 0:
            out = move[2:4] + move[0:2]
            return out
        elif self.piece_positions[int(move_coord[1])][int(move_coord[0])] != 0 and self.piece_positions[int(move_coord[3])][int(move_coord[2])] == 0:
            out = move[0:2] + move[2:4]
            return out
        return "Invalid move"
        '''
        
    def move(self, move):
        move = move[0] + move[1]

        move = self.find_piece_move(move)

        if not self.engine.is_move_legal(move):
            return "Invalid move"
        self.engine.move(move)
        move_coord = self.get_coord(move)
        self.piece_positions[int(move_coord[3])][int(move_coord[2])], self.piece_positions[int(move_coord[1])][int(move_coord[0])] = self.piece_positions[int(move_coord[1])][int(move_coord[0])], self.piece_positions[int(move_coord[3])][int(move_coord[2])]
        return "valid move"
    
    def get_engine_move_time(self, time = None):
        if time is not None:
            time = self.time
        move = self.engine.get_best_move_time(self.time)
        #if move is a take
        #if self.piece_positions[self.letter_to_number(move[2])][int(move[3])] != 0:
        if self.engine.stockfish.will_move_be_a_capture(move) != self.engine.stockfish.Capture.NO_CAPTURE:
            out = [move[2:4] + "00", move[0:2] + move[2:4]]
            self.engine.move(move)
            return out
        self.engine.move(move)
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
        #self.engine.set_fen("rnbqkbnr1pppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.piece_positions[0][0] = 1
        self.piece_positions[0][1] = 1
        self.piece_positions[0][2] = 1
        self.piece_positions[0][3] = 1
        self.piece_positions[0][4] = 1
        self.piece_positions[0][5] = 1
        self.piece_positions[0][6] = 1
        self.piece_positions[0][7] = 1
        self.piece_positions[1][0] = 1
        self.piece_positions[1][1] = 1
        self.piece_positions[1][2] = 1
        self.piece_positions[1][3] = 1
        self.piece_positions[1][4] = 1
        self.piece_positions[1][5] = 1
        self.piece_positions[1][6] = 1
        self.piece_positions[1][7] = 1
        self.piece_positions[6][0] = 1
        self.piece_positions[6][1] = 1
        self.piece_positions[6][2] = 1
        self.piece_positions[6][3] = 1
        self.piece_positions[6][4] = 1
        self.piece_positions[6][5] = 1
        self.piece_positions[6][6] = 1
        self.piece_positions[6][7] = 1
        self.piece_positions[7][0] = 1
        self.piece_positions[7][1] = 1
        self.piece_positions[7][2] = 1
        self.piece_positions[7][3] = 1
        self.piece_positions[7][4] = 1
        self.piece_positions[7][5] = 1
        self.piece_positions[7][6] = 1
        self.piece_positions[7][7] = 1
    def get_coord(self, move):
        return str(self.letter_to_number(move[0])) + str(int(move[1])-1) + str(self.letter_to_number(move[2])) + str(int(move[3])-1)

