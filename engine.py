#stockfish Engine
from stockfish import Stockfish
class Engine:
    def __init__(self, path, depth):
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
            "Use NNUE": "true"
        }
        self.engine = Stockfish(path, depth)
        self.engine.update_engine_parameters(self.default_settings)
        self.moves = 0
        #if it is white's turn turn = True else turn = False
        self.turn = True
        self.last_fen = None
    

    def get_fen(self):
        return self.engine.get_fen_position()

    def get_moves(self):
        return self.moves
    
    def get_parameters(self):
        return self.engine.get_parameters()
    
    def move(self, move):
        self.last_fen = self.engine.get_fen_position()
        self.engine.make_moves_from_current_position([move])
        self.moves += 1
        self.turn = not self.turn
    
    def set_fen(self, fen, moves=0, turn=True):
        self.engine.set_fen_position(fen)
        self.moves = moves
        self.turn = turn

    def get_best_move_time(self, time):
        return self.engine.get_best_move_time(time)


    def get_best_move_depth(self, depth):
        temp_depth = self.engine.depth
        self.engine.depth = depth
        best_move = self.engine.get_best_move()
        self.engine.depth = temp_depth
        return best_move
    
    def is_move_legal(self, move):
        return self.engine.is_move_correct(move)
    

    def undo_move(self):
        self.engine.set_fen_position(self.last_fen)
        self.moves = 0
        self.turn = not self.turn

    def get_visual(self):
        return self.engine.get_board_visual()

        