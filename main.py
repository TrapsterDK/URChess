from camera import Camera
from robot import Robot
from findchessboard import find_chess_board_rects, get_square_with_point, square_to_chessboard_square, chessboard_to_square, square_to_xy
from find_moves import find_move
from chess_mechanics import Chess

if __name__ == "__main__":
    camera = Camera()
    robot = Robot("10.130.58.12")
    chess = Chess()

    print("Started")
    while True:
        frame = camera.get_frame()

        print("Waiting for move")
        moves = find_move(camera)
        
        print("Finding chessboard")
        while True:
            try:
                rects = find_chess_board_rects(frame)
                squares = [get_square_with_point(move, rects) for move in moves]
                chesssquare = [square_to_chessboard_square(square) for square in squares]
                chess.move(chesssquare)
                break
            except:
                pass
        

        print("Moving piece")
        chessmove = chess.get_engine_move_time(1000)
        for move in chessmove:
            pos1 = chessboard_to_square(chessmove[0:2])
            x1, y1 = square_to_xy(pos1)
            if pos2 == "00":
                x2, y2 = -1, -1
            else:
                pos2 = chessboard_to_square(chessmove[2:4])
                x2, y2 = square_to_xy(pos2)
            robot.move_piece(x1, y1, x2, y2)

        print(chess.get_visual())
 