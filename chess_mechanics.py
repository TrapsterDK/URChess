from engine import Engine
class Chess:
    def __init__(self):
        self.engine = Engine(r"stockfish\stockfish-windows-2022-x86-64-avx2.exe", 3)
        self.piece_positions = [[0 for i in range(8)] for j in range(8)]
        self.start_pos()
        print(self.piece_positions)
    def get_visual(self):
        return self.engine.get_visual()
    def move(self, move):
        pass
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

        
