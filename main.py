from camera import Camera
from robot import Robot, get_piece_coordinate_from_chessboard
from findchessboard import find_chess_board_rects, get_square_with_point, square_to_chessboard_square, chessboard_to_square, square_to_xy
from find_moves import find_move
from chess_mechanics import Chess

if __name__ == "__main__":
    camera = Camera(0)
    robot = Robot("10.130.58.12")
    chess = Chess()

    print("Started")
    while True:
        print("Waiting for move")
        moves = find_move(camera)
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
            if chess.move(chesssquare) == "Illegal Move":
                exit()
            break

        print("Moving piece")
        chessmove = chess.get_engine_move_time(1000)
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
 