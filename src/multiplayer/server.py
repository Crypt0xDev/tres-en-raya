from flask import Flask, render_template, request, jsonify
import socketio

app = Flask(__name__)
sio = socketio.Server(cors_allowed_origins='*')
app.wsgi_app = socketio.WSGIApp(sio, app)

# Store connected players
players = {}

@sio.event
def connect(sid, environ):
    print(f'Player {sid} connected')
    players[sid] = {'name': None, 'game_data': None}

@sio.event
def disconnect(sid):
    print(f'Player {sid} disconnected')
    if sid in players:
        del players[sid]

@sio.event
def join_game(sid, data):
    players[sid]['name'] = data['name']
    print(f'Player {sid} joined the game as {data["name"]}')

@sio.event
def make_move(sid, data):
    # Handle the move made by the player
    print(f'Player {sid} made a move: {data}')
    # Broadcast the move to other players
    sio.emit('move_made', {'player': players[sid]['name'], 'move': data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)