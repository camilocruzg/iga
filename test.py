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
import sys
import time
import struct

#TODO can't work in windows
# def recvall(sock):
#     BUFF_SIZE = 4096 # 8 KiB
#     data = ""
#     while True:
#         part = sock.recv(BUFF_SIZE)
#         data += part
#         # time.sleep(0.001)
#         print sys.getsizeof(part)
#
#         if len(part) < BUFF_SIZE:
#             break
#     return data

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def tcp_con():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_socket.connect(("115.146.93.196", 1337))
    # tcp_socket.connect(("", 1337))


    the_type = "Init"
    popsize = 50
    indsize = str((2, 3, 4))
    gens = 5
    problem = "max"
    arg_json = {"type": the_type, "popsize": popsize, "indsize": indsize, "gens": gens, "problem": problem}
    # Protocol exchange - sends and receives
    tcp_socket.send(str(arg_json))

    # resp = tcp_socket.recv(80960)
    # # print resp
    # result = pickle.loads(resp)
    # # print type(result)
    # print result


    # data = recvall(tcp_socket)


    data = recv_msg(tcp_socket)
    result = pickle.loads(data)

    tcp_socket.close()
    return result


if __name__ == '__main__':
    result = tcp_con()
    pop = []
    for each in result:
        pop.append(each)
    print pop

    # print out
