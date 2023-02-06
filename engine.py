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
            "Hash": 2048,
            "MultiPV": 1,
            "Skill Level": 20,
            "Move Overhead": 10,
            "Minimum Thinking Time": 20,
            "Slow Mover": 100,
            "UCI_Chess960": "false",
            "UCI_LimitStrength": "false",
            "UCI_Elo": 1350,
            "EvalFile": r"stockfish\new.nnue",
            "Use NNUE": "true",
        }
        self.moves = 0
        #if it is white's turn turn = True else turn = False
        self.turn = True
    

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
    
    def move(self, move):
        self.engine.make_moves_from_current_position([move])
        self.moves += 1
        self.turn = not self.turn
    
    def set_fen(self, fen):
        self.engine.set_fen_position(fen)
        self.moves = 0
        self.turn = True
    #get best move in time
    def get_best_move_time(self, time):
        return self.engine.get_best_move_time(time)
    #get best move in depth

    def get_best_move_depth(self, depth):
        return self.engine.get_best_move_depth(depth)
