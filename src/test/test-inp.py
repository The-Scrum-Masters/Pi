import os
from socket import *
from uuid import getnode

#get host ip
host = raw_input("Enter ip: ")
port = int(raw_input("Enter port: "))
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)

while True:
    trolleys = [ 'tr00', 'tr01', 'tr02', 'tr03', 'tr04', 'tr05', 'tr06', 'tr07', 'tr08', 'tr09', 'tr10', 'tr11', 'tr12']
    data = raw_input("enter input: ")
    form = "trollid:" + trolleys[int(data)]
    UDPSock.sendto(form, addr)

UDPSock.close()
os._exit(0)
