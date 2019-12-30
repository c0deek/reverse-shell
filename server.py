import socket
import sys

def create_socket():
    try:
        global HOST
        global PORT
        global s
        
        HOST = ""
        PORT = 9876
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: "+ str(msg))


def bind_socket():
    try:
        global HOST
        global PORT
        global s

        print("Binding the Port: " + str(PORT))

        s.bind((HOST, PORT))
        s.listen(5)

    except socket.error as msg:
        print("Socket binding error" + str(msg) + "\nRetrying...")
        bind_socket()


def accept_socket():
    conn, addr = s.accept()
    print("Connected to [" + str(addr[0]) + ":" + str(addr[1]) + "]")
    send_commands(conn)
    conn.close()


def send_commands(conn):
    while True:
        cmd = input("> ")
        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()

        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(2048), "utf-8")
            print(client_response, end="")


def main():
    create_socket()
    bind_socket()
    accept_socket()

if __name__ == "__main__":
    main()
