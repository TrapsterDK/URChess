#test program
from engine import Engine

engine = Engine(r"stockfish\stockfish-windows-2022-x86-64-avx2.exe", 3)
#start from this fen position "r2qk2r/ppp2ppp/8/1NbppbN1/1nBPPBn1/8/PPP2PPP/R2QK2R w KQkq - 8 9"
#engine.set_fen("r1bq1rk1/np1p1ppp/p2P2n1/8/B7/2P2N2/P4PPP/R1BQK2R w KQ - 1 14")
#move = engine.engine.get_best_move()
#print(move)

#turn = True
#moves = 0

while True:
    #get best move in 1s
    move = engine.get_best_move_time(5000)
    print(move)
    if move == None:
        print(engine.get_fen())
        print("Mate")
        break
    #make move
    engine.move(str(move))
    user = True
    print(engine.get_visual())
    #check if game is over
    while user:
        user_input = input("Enter move: ")
        try:
            engine.move(str(user_input))
            user = False
        except:
            print("Invalid move")
    

#print final fen
print(engine.get_fen())


#stockfish = Stockfish(path="stockfish\stockfish-windows-2022-x86-64-avx2.exe", depth=500)

