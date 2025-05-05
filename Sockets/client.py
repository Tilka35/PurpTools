# Client script for Client and Server connection in python
import socket

# Socket object for client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP Connection
client.connect(('127.0.0.1', 9999)) # Bind server to localhost and unused port for communication

def send_conn():
    try:
        print(client.recv(1024).decode()) # Receive from server and decode
        client.send('Hello Server!'.encode()) # Encode and send to server
    finally:
        client.close()
    
def main():
    send_conn()
    
if __name__ == "__main__":
    main()