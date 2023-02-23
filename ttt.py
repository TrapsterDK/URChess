from chess_mechanics import Chess

#test
chess = Chess()
chess.move(["e2", "e4"])
chess.move(["e7", "e5"])
print(chess.get_engine_move_time(1000))
print(chess.get_visual())