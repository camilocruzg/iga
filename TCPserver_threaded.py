import socket
import threading
import flexible_GA
import sys



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

    def listenToClient(self, connect, address):
        while True:
            try:
                data = (connect.recv(1024)).strip()
                if data:
                    print threading.current_thread().getName() + " is receiving request with " + data
                    # print data
                    recv_data = eval(data)
                    poplist = []
                    if recv_data["type"] == "Init":
                        # print threading.current_thread().getName() + " start initializing "
                        poplist = flexible_GA.evolve1(recv_data["popsize"], recv_data["indsize"], recv_data["gens"], recv_data["problem"])
                        # print threading.current_thread().getName() + " the size of result is " + str(sys.getsizeof(poplist))
                        # print threading.current_thread().getName() + " all good"

                    elif recv_data["type"] == "Seed":
                        poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"], recv_data["problem"], recv_data["pop"])
                        pass
                    connect.send(poplist)
                    print threading.current_thread().getName() + " send the data with size of " + str(sys.getsizeof(poplist))

            except Exception as ex:
                print threading.current_thread().getName() + " is quiting with error: ", ex
                # print sys.exc_traceback.tb_lineno
                connect.close()
                return False

if __name__ == "__main__":
    ThreadedServer('',4000).listen()