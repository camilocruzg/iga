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
            # print "receiving data from " + str(address)
            try:
                data = (connect.recv(1024)).strip()
                if data:
                    print data
                    recv_data = eval(data)
                    poplist = []
                    if recv_data["type"] == "Init":
                        poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"],
                                                     recv_data["problem"])

                        # print "the size of sending is  "+str(sys.getsizeof(poplist))
                        # print type(poplist)
                        # pop_to_send = pickle.dumps(poplist)
                        print "the size of sending is  " + str(sys.getsizeof(poplist))

                    elif recv_data["type"] == "Seed":
                        poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"],
                                                     recv_data["problem"], recv_data["pop"])
                        pass
                    connect.send(poplist)

            except:
                raise Exception("empty")
            # print data
            # recv_data = eval(data)
            # poplist = []
            # if recv_data["type"] == "Init":
            #     poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"],
            #                                  recv_data["problem"])
            #
            #     # print "the size of sending is  "+str(sys.getsizeof(poplist))
            #     # print type(poplist)
            #     # pop_to_send = pickle.dumps(poplist)
            #     print "the size of sending is  " + str(sys.getsizeof(poplist))
            #
            # elif recv_data["type"] == "Seed":
            #     poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"],
            #                                  recv_data["problem"], recv_data["pop"])
            #     pass
            # connect.send(poplist)
            # connect.close()

            # try:
            #     data = client.recv(size)
            #     if data:
            #         # Set the response to echo back the recieved data
            #         response = data
            #         client.send(response)
            #     else:
            #         raise Exception('Client disconnected')
            # except:
            #     client.close()
            #     return False

if __name__ == "__main__":
    ThreadedServer('',1337).listen()