import socket
import threading
import select
import sys

def handle_client(client_socket):
    try:
        while True:
            # Use select to check if data is available
            rlist, _, _ = select.select([client_socket, sys.stdin], [], [], 0.1)
            for sock in rlist:
                if sock is client_socket:
                    # Receive data from client
                    data = client_socket.recv(4096).decode('utf-8', errors='ignore')
                    if not data:
                        print("Client disconnected")
                        client_socket.close()
                        return
                    print(data, end='', flush=True)
                elif sock is sys.stdin:
                    # Read command from server input
                    command = input()
                    if command.lower() == 'exit':
                        client_socket.close()
                        return
                    client_socket.send((command + '\n').encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def main():
    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = 4898       # Arbitrary port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"Listening on {HOST}:{PORT}")
        
        client_socket, addr = server.accept()
        print(f"Connected by {addr}")
        
        # Handle client in a separate thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
        client_handler.join()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    main()