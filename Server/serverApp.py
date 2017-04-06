# """
# Usage:
#     curl -X POST localhost:1337/test -d "popsize=100&indsize=(2,3,4)&gens=5&problem=max"
# """
#
# from flask import Flask, render_template, request, url_for
from Functions import evolve
#
# app = Flask(__name__)
#
# @app.route('/')
# def form():
#     return "hello,world"
#
# @app.route('/hello', methods=['POST'])
# def hello():
#     name=request.form['yourname']
#     return "Welcome, ", name
#
# @app.route('/test',methods=['POST'])
# def test():
#     pop_size=request.form['popsize']
#     ind_size=request.form['indsize']
#     gens=request.form['gens']
#     prob=request.form['problem']
#     # return "the number is %s and %s"%(pop_size,ind_size)
#     poplist = evolve(pop_size,ind_size,gens,prob)
#     return str(poplist)
#
#
# if __name__ == '__main__':
#   app.run(
#         host="",
#         port=1337
#   )

import socket
import json
import time

# A UDP server

# Set up a UDP server
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Listen on port 1337
# (to all IP addresses on this system)
listen_addr = ("",1337)
UDPSock.bind(listen_addr)

# Report on all data packets received and
# where they came from in each case (as this is
# UDP, each may be from a different source and it's
# up to the server to sort this out!)
# while UDPSock.recvfrom(1024) is not None:
    # print "message received"
while 1:
    data,addr = UDPSock.recvfrom(4096)
    recv_data = eval(data)
    if recv_data["type"] == "Init":
        poplist = evolve(recv_data["popsize"], recv_data["indsize"], recv_data["gens"], recv_data["problem"])
        print poplist
    print data,addr,time.time()
    # UDPSock.sendto(str(time.asctime()), addr)
    UDPSock.sendto(str(str(time.asctime())+str(poplist[:10])),addr)
    # print poplist
