import socketserver
import socket
import threading
import sys

def load_file(filename):
    all_data = {}
    with open(filename,"r") as file_in:
        for line in file_in:
            data = line.strip().split("=")
            all_data[data[0]] = data[1]
    return all_data 

def get_reversed_directory(directory):
    reversed_directory = {}
    for key,value in directory.items():
        new_key = value.split(",")[0]
        reversed_directory[new_key] = key
    return reversed_directory

config = load_file(sys.argv[1])
directory = load_file(sys.argv[2])
reverse_directory = get_reversed_directory(directory)

class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        msg = str(self.request[0].strip(), "UTF-8")
        if self.client_address[0] in reverse_directory:
            print("{} : {}".format(reverse_directory[self.client_address[0]], msg))
        else:
            print("{} : {}".format(self.client_address[0], msg))

def send(destination, msg):
    destination_list = destination.split(",")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(bytes(msg, "UTF-8"), (destination_list[0], int(destination_list[1])))
        
config = load_file(sys.argv[1])
directory = load_file(sys.argv[2])
with socketserver.UDPServer(("localhost",int(config["PORT"])), MyServer) as server:
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    quit = False
    while not quit:
        msg = input().strip().split("|")
        if msg[0] == "quit":
            quit = True
        elif msg[0] in directory:
            send(directory[msg[0]],msg[1])
        else:
            print("Error!")
    server.shutdown()


