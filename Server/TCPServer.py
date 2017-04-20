import socket
import flexible_GA
import pickle
import time
import sys
import json

tcpsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

tcpsocket.bind(("", 1337))
tcpsocket.listen(5)
print "the server is listening..."
while True:
        connect, addr = tcpsocket.accept()
        data = (connect.recv(1024)).strip()
        print data
        recv_data = eval(data)
        poplist = []
        # pop_to_send = ""
        if recv_data["type"] == "Init":
            poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"], recv_data["problem"])
            # print "the size of sending is  "+str(sys.getsizeof(poplist))
            # print type(poplist)
            # pop_to_send = pickle.dumps(poplist)
            print "the size of sending is  "+str(sys.getsizeof(poplist))
            print type(poplist)
            # with open("test.data", "w") as f:
            #     pickle.dumps(poplist)


        elif recv_data["type"] == "Seed":
            poplist = flexible_GA.evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"], recv_data["problem"], recv_data["pop"])

            pass
        connect.send(poplist)
        # And there could be a lot more here!


        # connect.close()
        print "\ndone",addr