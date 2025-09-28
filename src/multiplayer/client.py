import socket
import threading

class MultiplayerClient:
    def __init__(self, host='localhost', port=12345):
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect(self.server_address)
            print(f"Connected to server at {self.server_address}")
            self.listen_for_messages()
        except Exception as e:
            print(f"Failed to connect to server: {e}")

    def listen_for_messages(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Message from server: {message}")
                else:
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send_message(self, message):
        try:
            self.socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")

    def close(self):
        self.socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    client = MultiplayerClient()
    client.connect()

    while True:
        user_input = input("Enter message to send (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            client.close()
            break
        client.send_message(user_input)