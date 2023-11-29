import socket
import os
import json

def list_files(directory, extension):
    return [f for f in os.listdir(directory) if f.endswith(extension)]

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
        return "File saved successfully."

def rename_file(old_name, new_name):
    os.rename(old_name, new_name)
    return "File renamed successfully."

def create_file(file_path):
    open(file_path, 'a').close()
    return "File created successfully."

# Socket setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)

print("Server is listening for connections...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connected with {addr}")

    message = client_socket.recv(1024).decode()
    command, *args = message.split('|')

    response = ""
    try:
        if command == 'list_files':
            response = json.dumps(list_files(*args))
        elif command == 'read_file':
            response = read_file(*args)
        elif command == 'write_file':
            response = write_file(*args)
        elif command == 'rename_file':
            response = rename_file(*args)
        elif command == 'create_file':
            response = create_file(*args)
        else:
            response = "Unknown command."
    except Exception as e:
        response = f"Error: {str(e)}"

    client_socket.sendall(response.encode())
    client_socket.close()
