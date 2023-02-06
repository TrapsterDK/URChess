#stockfish Engine
from stockfish import Stockfish
class Engine:
    def __init__(self, path, depth):
        self.engine = Stockfish(path, depth)
        self.default_settings = {
            "Debug Log File": "",
            "Contempt": 0,
            "Min Split Depth": 0,
            "Threads": 4,
            "Ponder": "true",
            "Hash": 1000,
            "MultiPV": 1,
            "Skill Level": 20,
            "Move Overhead": 10,
            "Minimum Thinking Time": 20,
            "Slow Mover": 100,
            "UCI_Chess960": "false",
            "UCI_LimitStrength": "false",
            "UCI_Elo": 1350,
            "EvalFile": r"stockfish\nn-a3dc078bafc7.nnue",
            "Use NNUE": "true",
        }
        self.moves = 0
        #if it is white's turn turn = True else turn = False
        self.turn = True
        self.engine.set_position(["startposition"])
        

    def get_best_move(self):
        if self.turn:
            out = self.engine.get_best_move_time(100)
        elif not self.turn:
            out = self.engine.get_best_move_time(20)
        if out == None or self.moves > 1000:
            print("Mate")
            return None
        self.engine.make_moves_from_current_position([out])
        self.moves += 1
        self.turn = not self.turn
        return out

    def get_fen(self):
        return self.engine.get_fen_position()

    def get_moves(self):
        return self.moves
    
    def get_parameters(self):
        return self.engine.get_parameters()
    #from start position
    def set_position(self, moves):
        self.engine.set_position(moves)
        self.moves = 0
        self.turn = True

"""
stockfish = Stockfish(path="stockfish\stockfish-windows-2022-x86-64-avx2.exe", depth=500)
#stockfish.set_position(["e2e4"])
#stockfish.make_moves_from_current_position(["g4d7", "a8b8", "f1d1"])
moves = 0
#stockfish._set_option("EvalFile", r"stockfish\nn-a3dc078bafc7.nnue")
stockfish._set_option("Use NNUE", "false")
#print(stockfish.evalType)
#stockfish.set_position(["startposition"])
turn = False
while True:
    if turn:
        turn = False
    else:
        turn = True
    if turn:
        out = stockfish.get_best_move_time(100)
    elif not turn:
        out = stockfish.get_best_move_time(20)
    if out == None or moves > 1000:
        print("Mate")
        break
    
    stockfish.make_moves_from_current_position([out])
    moves += 1
    #print(out)

out=stockfish.get_fen_position()
print(out)
print(moves)
print(stockfish.get_parameters())
"""
