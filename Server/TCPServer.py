import socket
import flexible_GA
import sys
import threading

class myThread (threading.Thread):
    def __init__(self, connect):
        threading.Thread.__init__(self)
        self.connect = connect
        # self.name = name
        # self.counter = counter
    def run(self):
        print "Starting " + self.name
        data = (self.connect.recv(1024)).strip()
        print data
        recv_data = eval(data)
        poplist = []

        if recv_data["type"] == "Init":
            poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"], recv_data["problem"])

            print "the size of sending is  " + str(sys.getsizeof(poplist))

        elif recv_data["type"] == "Seed":
            poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"], recv_data["problem"], recv_data["pop"])
            pass
        connect.send(poplist)
        print "Exiting " + self.name
        connect.close()




tcpsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

tcpsocket.bind(("", 1337))
tcpsocket.listen(5)

print "the server is listening..."
while True:
        connect, addr = tcpsocket.accept()
        print "receiving data from " + str(addr)
        data = (connect.recv(1024)).strip()
        print data
        recv_data = eval(data)
        poplist = []

        if recv_data["type"] == "Init":
            poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"], recv_data["problem"])

            print "the size of sending is  "+str(sys.getsizeof(poplist))

        elif recv_data["type"] == "Seed":
            poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"], recv_data["problem"], recv_data["pop"])
            pass
        connect.send(poplist)
