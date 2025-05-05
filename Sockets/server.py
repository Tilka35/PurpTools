# Server script for Client and Server connection in python
import socket

# Socket object for server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP Connection
server.bind(('127.0.0.1', 9999)) # Bind server to localhost and unused port for communication

num_connections = 1
server.listen(num_connections) # Listen and allow one connection
print("Server is running...")

# Receive connections
def recv_conn():
    while True:
        try:        
            client, addr = server.accept() # Accept connections
            print(f"Connected to {addr}") # Print address of client
            
            client.send('Hello Client!'.encode()) # Encode and send message
            print(client.recv(1024).decode()) # Receive and decode message
            
            client.send("Acknowledged!".encode()) # Keep connection open
            client.close() # Close connection
        except Exception as e:
            print(f"Error {e}")
        
def main():
    recv_conn()

if __name__ == "__main__":
    main()