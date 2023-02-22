from camera import Camera
from robot import Robot
from findchessboard import find_chess_board_rects, get_square_with_point, square_to_chessboard_square, chessboard_to_square

if __name__ == "__main__":
    camera = Camera()
    robot = Robot("10.130.58.12")

    while True:
        frame = camera.get_frame()

        move_1, move_2 = ???
        
        while True:
            try:
                rects = find_chess_board_rects(frame)
                square_1 = get_square_with_point(move_1, rects)
                square_2 = get_square_with_point(move_2, rects)

                chess_square_1 = square_to_chessboard_square(square_1)
                chess_square_2 = square_to_chessboard_square(square_2)
                break
            except:
                pass
        
        chessmove = ???
        pos1 = chessboard_to_square(chessmove[0:2])
        pos2 = chessboard_to_square(chessmove[2:4])
        robot.move_piece(pos1[0], pos1[1], pos2[0], pos2[1])

        
        