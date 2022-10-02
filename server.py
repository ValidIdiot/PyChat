import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 10
active_clients = []

def listener(client, username):
    while True:
        response = client.recv(2048).decode('utf-8')
        if response != "":
            final_msg = username + ": " + response
            send_public_messages(final_msg)
        else:
            print(f"The message sent from client {username} was empty..")

def dm(client, message):
    client.sendall(message.encode())

def send_public_messages(message):
    for user in active_clients:
        dm(user[1], message)

def client_handler(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            break

        else:
            print("Client username is empty.")
    threading.Thread(target=listener, args=(client, username, )).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print("Running the server on " + HOST + "...")
    except:
        print("Unable to bind to host: " + HOST + " and port: " + str(PORT))
    
    server.listen(LISTENER_LIMIT)

    while True:
        client, address = server.accept()
        print("Succsessfully connected to client: " + address[0], address[1])

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()