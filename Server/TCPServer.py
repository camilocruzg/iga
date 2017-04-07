import socket
import time
from Functions import evolve
tcpsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

tcpsocket.bind(("",1337))
# ... and listen for anyone to contact you
# queueing up to five requests if you get a backlog
tcpsocket.listen(5)

# Servers are "infinite" loops handling requests
while True:

        # Wait for a connection
        connect, addr = tcpsocket.accept()
        data = (connect.recv(1024)).strip()
        print data
        recv_data = eval(data)
        if recv_data["type"] == "Init":
            poplist = evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"], recv_data["problem"])
            print poplist
        print data, addr, time.localtime()

        connect.send(str(poplist[:10]))

        # And there could be a lot more here!

        # When done with a connection close it

        # connect.close()
        print "\ndone",addr