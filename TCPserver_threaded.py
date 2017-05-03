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
            # client.settimeout(60)
            threading.Thread(target = self.listenToClient, args = (connect,address)).start()

    def send_msg(self,connect, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        connect.sendall(msg)

    def listenToClient(self, connect, address):
        try:
            data = (connect.recv(8192)).strip()
            if data:
                print threading.current_thread().getName() + " is receiving request with " + data
                # print data
                recv_data = eval(data)
                # print type(recv_data)

                poplist = []
                if recv_data["type"] == "Init":
                    # print threading.current_thread().getName() + " start initializing "
                    poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"],
                                                  recv_data["problem"],pop = [])
                    # print threading.current_thread().getName() + " the size of result is " + str(sys.getsizeof(poplist))
                    # print threading.current_thread().getName() + " all good"

                elif recv_data["type"] == "Seed":
                    the_seed = pickle.loads(recv_data["pop"])
                    # print the_seed
                    poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"],
                                                 recv_data["problem"], the_seed)


                # connect.sendall(poplist)
                # connect.send(poplist)

                self.send_msg(connect,poplist)

                print threading.current_thread().getName() + " send the data with size of " + str(
                    sys.getsizeof(poplist))
                # print threading.current_thread().isAlive()


        except Exception as ex:
            print threading.current_thread().getName() + " is quiting with error: ", ex
            # print sys.exc_traceback.tb_lineno
            connect.close()
            return False


if __name__ == "__main__":
    ThreadedServer('',1337).listen()