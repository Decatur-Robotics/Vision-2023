import socket

def init():
    print("Starting socket server...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 4026))
    server.listen()
    print("Server initialized. Listening for connections...")
    conn, addr = server.accept()
    print(f"Received connection from {addr}!")
    return conn