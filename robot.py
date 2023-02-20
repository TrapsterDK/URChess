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
        self.clear_messurements()

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
            self.rtde_con.receive_buffered()

    def close(self) -> None:
        self.rtde_con.send_pause()
        self.rtde_con.disconnect()
        self.tcp_con.close()

    def get_state(self) -> dict:
        return self.rtde_con.receive()

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


    def move_piece(self) -> None:
        command = "chessmove.urp"
        self.rtde_send()

        if self.get_loaded_program() != "programs/" + command:
            self.load_program(command)
        
        self.stop()
        self.play()

        while not self.running():
            continue


