import socket
import time
from Functions import evolve
tcpsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

tcpsocket.bind(("", 1337))
tcpsocket.listen(5)

while True:
        connect, addr = tcpsocket.accept()
        data = (connect.recv(1024)).strip()
        print data
        recv_data = eval(data)
        if recv_data["type"] == "Init":
            poplist = evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"], recv_data["problem"])
            print poplist

        connect.send(str(poplist[0])+time.asctime())

        # And there could be a lot more here!


        # connect.close()
        print "\ndone",addr