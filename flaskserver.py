from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO
from chess_mechanics import Chess

app = Flask(__name__)
socketio = SocketIO(app)

chess = None

@app.errorhandler(404)
@app.route('/')
def index():
    return 'Hello World'

def run(chess_: Chess):
    global chess
    chess = chess_
    socketio.run()

if __name__ == '__main__':
    chess = Chess()
    run(chess)
