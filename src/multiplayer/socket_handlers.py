from flask_socketio import SocketIO, emit

socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    emit('response', {'message': 'Connected to the server!'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    emit('response', {'message': f'{username} has joined the game!'}, broadcast=True)

@socketio.on('make_move')
def handle_make_move(data):
    move = data['move']
    # Logic to handle the move and update game state
    emit('move_made', {'move': move}, broadcast=True)

@socketio.on('chat_message')
def handle_chat_message(data):
    message = data['message']
    emit('chat_response', {'message': message}, broadcast=True)