import socket
import struct
import sys
import json

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

uuids = []
messages = []

print('sending acknowledgement to', ('224.3.29.71', 10000))
message = 'ack'
sock.sendto(message.encode('UTF-8'), ('224.3.29.71', 10000))

# Receive/respond loop
while True:
    print('waiting to receive message')
    data, address = sock.recvfrom(1024)

    try:
        data = json.loads(data)
    except:
        print(". . .")
    
    print('received %s bytes from %s' % (data, address))
    # if (address != socket.gethostbyname(socket.gethostname())):
    if(data == "b'ack"):
        for message in messages:
            if(message['expired_at'] > datetime.datetime.now()):
                print('sending message to', address)
                sock.sendto(message.encode('UTF-8'), address)
            else:
                messages.remove(message)
    else:
        messages.append(data)

        try:
            if(data['uuid'] not in uuids):
                uuids.append(data['uuid'])
                print(data)
        except:
            print(data)