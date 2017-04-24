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
#TODO can't work in windows
def recvall(sock):
    BUFF_SIZE = 8192 # 8 KiB
    data = ""
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        print sys.getsizeof(part)
        if len(part) < BUFF_SIZE:
            break
    return data


def tcp_con():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_socket.connect(("localhost", 4000))

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

    # tcp_socket.close()
    return result


if __name__ == '__main__':
    result = tcp_con()
    pop = []
    for each in result:
        pop.append(each)
    print pop

    # print out