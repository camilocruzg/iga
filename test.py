# """Provides a scripting component.
#     Inputs:
#         x: The x script variable
#         y: The y script variable
#     Output:
#         a: The a output variable"""
#
# __author__ = "liujunyuan"
#
# import socket
#
# switch = 1
# if __name__ == '__main__' and switch == 1:
#     print "start"
#     # This is an example of a UDP client - it creates
#     # a socket and sends data through it
#
#     # create the UDP socket
#     UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
#     the_type = "Init"
#     popsize = 50
#     indsize = str((2, 3, 4))
#     gens = 5
#     problem = "max"
#     arg_json = {"type": the_type, "popsize": popsize, "indsize": indsize, "gens": gens, "problem": problem}
#
#     # Simply set up a target address and port ...
#     addr = ("localhost", 1337)
#     # ... and send data out to it!
#     UDPSock.sendto(str(arg_json), addr)
#     data, addr = UDPSock.recvfrom(4096)
#     print (data)
#     print"sent"
#
#     UDPSock.close()
#
#

"""
tcppart
"""

import socket
import pickle
import Init_Ind
import sys
def recvall(sock):
    var = 0
    BUFF_SIZE = 4096 # 4 KiB
    data = ""
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        print len(part)
        if len(part) < BUFF_SIZE:
            print sys.getsizeof(part)
            # either 0 or end of data
            break
        var += 1
        print var
    return data

# Set up a TCP/IP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


tcp_socket.connect(("localhost", 1337))

the_type = "Init"
popsize = 50
indsize = str((2, 3, 4))
gens = 5
problem = "max"
arg_json = {"type": the_type, "popsize": popsize, "indsize": indsize, "gens": gens, "problem": problem}
# Protocol exchange - sends and receives
tcp_socket.send(str(arg_json))

# resp = tcp_socket.recv(81920)
# print resp
# result = pickle.loads(resp)
# # print type(result)
# print result

data = recvall(tcp_socket)
result = pickle.loads(data)

print result[1].dom


tcp_socket.close()

test_data = [[1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0]
    ,[1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

