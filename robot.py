import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
from time import sleep
import atexit
from threading import Thread
from typing import Any
import socket

TCP_PORT = 29999
RTDE_PORT = 30004
BUFFER_SIZE = 1024


class Robot:
    watchdog: Any
    rtde_con: Any
    empty_pos = 0
    messurements: list[float]

    def __init__(self, ip) -> None:
        config_filename = "robot_configuration.xml"
        conf = rtde_config.ConfigFile(config_filename)
        
        state_names, state_types = conf.get_recipe("state")
        watchdog_names, watchdog_types = conf.get_recipe("watchdog")

        self.rtde_con = rtde.RTDE(ip, RTDE_PORT)
        self.rtde_con.connect()
        
        self.rtde_con.send_output_setup(state_names, state_types)
        self.watchdog = self.rtde_con.send_input_setup(watchdog_names, watchdog_types)
        self.watchdog.input_int_register_0 = 0
        self.watchdog.input_int_register_1 = 0
        
        if not self.rtde_con.send_start():
            raise Exception("Error connecting to RTDE interface")

        print("RTDE connected")
        Thread(target=self.update_thread, daemon=True).start()

        
        self.tcp_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.tcp_con.connect((ip, TCP_PORT))
            self.tcp_con.recv(BUFFER_SIZE)
        except socket.error as e:
            raise Exception("Could not connect to LeBot: ", e)

        print("TCP connected")

    def update_thread(self) -> None:
        while True:
            try:
                self.rtde_con.receive_buffered()
            except Exception as e:
                print("Error receiving RTDE data: ", e)
                break

    def close(self) -> None:
        self.rtde_con.send_pause()
        self.rtde_con.disconnect()
        self.tcp_con.close()

    def get_watchdog(self) -> Any:
        return self.watchdog

    def set_watchdog(self, watchdog: Any) -> None:
        self.watchdog = watchdog

    def rtde_send(self) -> None:
        return self.rtde_con.send(self.watchdog)
        
    def play(self):
        self.tcp_con.send(b"play\n")
        response = self.tcp_con.recv(BUFFER_SIZE)
        print("Response: " + str(response))

    def stop(self):
        self.tcp_con.send(b"stop\n")
        response = self.tcp_con.recv(BUFFER_SIZE)
        print("Response: " + str(response))

    def pause(self):
        self.tcp_con.send(b"pause\n")
        response = self.tcp_con.recv(BUFFER_SIZE)
        print("Response: " + str(response))

    def load_program(self, program: str) -> None:
        self.tcp_con.send(b"load " + program.encode() + b"\n")
        response = self.tcp_con.recv(BUFFER_SIZE)
        print("Response: " + str(response))

    def running(self) -> str:
        self.tcp_con.send(b"running\n")
        response = self.tcp_con.recv(BUFFER_SIZE)
        return response.decode()[17:-1] == "true"

    def get_loaded_program(self) -> str:
        self.tcp_con.send(b"get loaded program\n")
        response = self.tcp_con.recv(BUFFER_SIZE)
        print("Response: " + str(response.decode()[17:-1]))
        return response.decode()[17:-1]


    def move_piece(self, x1, y1, x2, y2) -> None:
        print("Moving piece from " + str(x1) + ", " + str(y1) + " to " + str(x2) + ", " + str(y2))
        self.watchdog.input_int_register_0 = x1
        self.watchdog.input_int_register_1 = y1
        self.watchdog.input_int_register_2 = x2
        self.watchdog.input_int_register_3 = y2
        self.rtde_send()

        command = "chessmove.urp"
        if self.get_loaded_program() != "programs/" + command:
            self.load_program(command)
        
        self.stop()
        self.play()

        while not self.running():
            continue

        while self.running():
            continue

pieces_real_coordinates = [(-276.6, -59.8), (-502.2, -281.5)]
pieces_pixel_coordinates = [(486, 36), (91, 431)]

def get_piece_coordinate_from_pixel(x, y):
    x = (x - pieces_pixel_coordinates[0][0]) / (pieces_pixel_coordinates[1][0] - pieces_pixel_coordinates[0][0]) * (pieces_real_coordinates[1][0] - pieces_real_coordinates[0][0]) + pieces_real_coordinates[0][0]
    y = (y - pieces_pixel_coordinates[0][1]) / (pieces_pixel_coordinates[1][1] - pieces_pixel_coordinates[0][1]) * (pieces_real_coordinates[1][1] - pieces_real_coordinates[0][1]) + pieces_real_coordinates[0][1]

    return int(x), int(y)

def get_piece_coordinate_from_chessboard(x, y, board_side = 8):
    x, y = y, x
    x = (x - 1) / (board_side - 1) * (pieces_real_coordinates[1][0] - pieces_real_coordinates[0][0]) + pieces_real_coordinates[0][0]
    y = (y - 1) / (board_side - 1) * (pieces_real_coordinates[1][1] - pieces_real_coordinates[0][1]) + pieces_real_coordinates[0][1]

    return int(x), int(y)

if __name__ == "__main__":
    robot = Robot("10.130.58.12")

    #x1, y1 = get_piece_coordinate_from_pixel(pieces_pixel_coordinates[0][0], pieces_pixel_coordinates[0][1])
    #x2, y2 = get_piece_coordinate_from_pixel(pieces_pixel_coordinates[1][0], pieces_pixel_coordinates[1][1])

    x1, y1 = get_piece_coordinate_from_chessboard(5, 7)
    x2, y2 = get_piece_coordinate_from_chessboard(5, 5)

    robot.move_piece(x1, y1, x2, y2)



