from camera import Camera
from robot import Robot, get_piece_coordinate_from_chessboard
from findchessboard import find_chess_board_rects, get_square_with_point, square_to_chessboard_square, chessboard_to_square, square_to_xy
from find_moves import find_move
from chess_mechanics import Chess

def option_mode(option = None):
    if option == "invalid move":
        print("An invalid move was made, please try again")
        print("the current board is: ")
        print(chess.get_visual())
        print("press m to manual enter the move")
        print("press n to make the move again (move tour piece back to the original position before pressing n)")
        user = input()
        if user == "m":
            print("enter the move in the form of chess notation (e.g. e2e4)")
            move = input()
            if chess.move(move) == None:
                print("Invalid move")
                option_mode("invalid move")
            else:
                print("Valid move")
                return
        elif user == "n":
            print("move your piece back to the original position")
            print("press y when you are ready")
            user = input()
            if user == "y":
                print("finding moves")
                moves = find_move(camera)
                print("Found moves coordinates", moves)
                squares = [get_square_with_point(move, rects) for move in moves]
                squares = [square for square in squares if square is not None]
                chesssquare = [square_to_chessboard_square(square) for square in squares]
                print("Found chessboard moves", chesssquare)
                if chess.move(chesssquare) == None:
                    print("Invalid move")
                    option_mode("invalid move")
                    #do something
                else:
                    print("Valid move")
                    return
            else:
                print("Invalid input")
                option_mode("invalid move")
        else:
            print("Invalid input")
            option_mode("invalid move")
    elif option == "stop":
        print("you have stopped the detection")
        print("the current board is: ")
        print(chess.get_visual())
        print("press n to take new zero pick")
        print("press b to go two moves back")
        user = input()
        if user == "n":
            return
        elif user == "b":
            chess.undo()
            print("the current board is: ")
            print(chess.get_visual())
            print("press n to take new zero pick")
            user = input()
            if user == "n":
                return
            else:
                print("Invalid input")
                option_mode("stop")
        else:
            print("Invalid input")
            option_mode("stop")


        


if __name__ == "__main__":
    robot = Robot("10.130.58.12")
    camera = Camera(0)
    chess = Chess()

    print("Started")
    while True:
        print("Waiting for move, wait 3 seconds")
        moves = find_move(camera)
        if moves is None:
            option_mode("stop")
            continue
        print("Found moves coordinates", moves)
        
        print("Finding chessboard")
        while True:
            frame = camera.get_frame()[1]

            rects = find_chess_board_rects(frame)
            if rects is None:
                continue
            print("Found  chessboard")
            squares = [get_square_with_point(move, rects) for move in moves]
            squares = [square for square in squares if square is not None]
            chesssquare = [square_to_chessboard_square(square) for square in squares]
            print("Found chessboard moves", chesssquare)
            if chess.move(chesssquare) == None:
                print("Invalid move")
                option_mode("invalid move")
                #do something
            break

        print("Moving piece")
        chessmove = chess.get_engine_move_time(1000)
        print(chess.get_visual())
        print("Moves: ", chessmove)
        for move in chessmove:
            pos1 = chessboard_to_square(move[0:2])
            x1, y1 = square_to_xy(pos1)
            if move[2:4] == "00":
                x2, y2 = -1, -1
            else:
                pos2 = chessboard_to_square(move[2:4])
                x2, y2 = square_to_xy(pos2)

            print("Moving piece from", x1, y1, "to", x2, y2)

            px1, py1 = get_piece_coordinate_from_chessboard(x1, y1)
            px2, py2 = get_piece_coordinate_from_chessboard(x2, y2)

            print("Moving piece from", px1, py1, "to", px2, py2)

            robot.move_piece(px1, py1, px2, py2)

        print(chess.get_visual())
 