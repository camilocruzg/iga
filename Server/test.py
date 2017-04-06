"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "liujunyuan"

import socket
print "start"
# This is an example of a UDP client - it creates
# a socket and sends data through it

# create the UDP socket
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

the_type = "Init"
popsize = 50
indsize = str((2,3,4))
gens = 5
problem = "max"
arg_json = {"type":the_type, "popsize": popsize,"indsize":indsize,"gens":gens, "problem":problem}

# Simply set up a target address and port ...
addr = ("localhost",1337)
# ... and send data out to it!
UDPSock.sendto(str(arg_json),addr)
data,addr = UDPSock.recvfrom(4096)
print (data)
print"sent"

UDPSock.close()