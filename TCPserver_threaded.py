#!/usr/bin/python2
import socket
import threading
import flexible_GA
import sys
import struct
import pickle

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        print "the server is listening..."
        while True:
            connect, address = self.sock.accept()
            threading.Thread(target = self.listenToClient, args = (connect,address)).start()

    def send_msg(self, sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def recv_msg(self,sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recv_all(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recv_all(sock, msglen)

    def recv_all(self, sock, prefix_len):
        # Helper function to recv n bytes or return None if EOF is hit
        data = ''
        while len(data) < prefix_len:
            packet = sock.recv(prefix_len - len(data))
            if not packet:
                return None
            data += packet
        return data

    def listenToClient(self, sock,address):
        try:
            # data = (connect.recv(8192)).strip()
            recv_data = self.recv_msg(sock).strip()

            if recv_data:
                print threading.current_thread().getName() + " is receiving request with " + recv_data
                # print data
                recv_data = eval(recv_data)
                # print type(recv_data)

                pop_list = []
                if recv_data["type"] == "Init":
                    # print threading.current_thread().getName() + " start initializing "
                    pop_list = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"],
                                                  recv_data["problem"],recv_data['selection'],pop = [])
                    # print threading.current_thread().getName() + " the size of result is " + str(sys.getsizeof(poplist))
                    # print threading.current_thread().getName() + " all good"

                elif recv_data["type"] == "Seed":
                    the_seed = pickle.loads(recv_data["pop"])
                    # print the_seed
                    pop_list = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"],
                                                 recv_data["problem"],recv_data['selection'], the_seed)


                self.send_msg(sock, pop_list)

                print threading.current_thread().getName() + " send the data with size of " + str(
                    sys.getsizeof(pop_list))
                # print threading.current_thread().isAlive()


        except Exception as ex:
            print threading.current_thread().getName() + " is quiting with error: ", ex
            sock.close()
            return False


if __name__ == "__main__":
    ThreadedServer('',1337).listen()