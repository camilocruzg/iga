
import socket
import pickle
import Init_Ind
import sys
import struct
import os

popsize = int(pop_size)
indsize = ind_size
gens = int(generations)
problem = prob_type

gh_path = ghdoc.Path
path = os.path.dirname(os.path.realpath(gh_path))
path += "\seed"

def readSeed(file_path):
    f = open(file_path,"r")
    data = f.read()
    data = pickle.loads(data)
    f.close()
    os.remove(file_path)
    return data

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

def send_msg(connect, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    connect.sendall(msg)

def tcp_init():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#    tcp_socket.connect(("115.146.93.196", 1337))
    tcp_socket.connect(("localhost", 1337))

    the_type = "Init"
    arg_json = {"type": the_type, "popsize": popsize, "indsize": indsize, "gens": gens, "problem": problem,"selection":selection}
    # Protocol exchange - sends and receives
    send_msg(tcp_socket,str(arg_json))
#    tcp_socket.send(str(arg_json))

    data = recv_msg(tcp_socket)
    result = pickle.loads(data)

    tcp_socket.close()
    return result

def tcp_seed(var):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#    tcp_socket.connect(("115.146.93.196", 1337))
    tcp_socket.connect(("localhost", 1337))
#    var = readSeed(path)
    print "the length of seeds is " , len(var)
    serial_seed = pickle.dumps(var)
    the_type = "Seed"
    arg_json = {"type": the_type, "popsize": popsize, "indsize": indsize, "gens": gens, "problem": problem,"selection":selection,"pop":serial_seed}
    # Protocol exchange - sends and receives
    send_msg(tcp_socket,str(arg_json))
#    tcp_socket.send(str(arg_json))

    data = recv_msg(tcp_socket)
    result = pickle.loads(data)

    tcp_socket.close()
    return result


if __name__ == '__main__' and on_off == True:
    if os.path.isfile(path):
        var = readSeed(path)
        b = "Seed(s): " + str(len(var))
        result = tcp_seed(var)
        pop = []
        for each in result:
            pop.append(each)
        a = pop
#        c = True
        print "Seed"
        print a
    else:
        b = "Seed(s): 0"
        result = tcp_init()
        pop = []
        for each in result:
            pop.append(each)
        a = pop
#        c = False
        print "Init"
        print func
        print a


