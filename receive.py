import socket
import struct
import sys
import json
import datetime

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
        print('received %s bytes from %s' % (data, address))
    except:
        data = data.decode()
        print('received %s bytes from %s' % (data, address))
        print(". . .")
    
    # if (address != socket.gethostbyname(socket.gethostname())):
    if(data == 'ack'):
        for message in messages:
            if(datetime.datetime.strptime(message['expired_at'], '%Y-%m-%d %H:%M:%S.%f') > datetime.datetime.now()):
                print('sending message to', address)
                sock.sendto(json.dumps(message).encode('UTF-8'), address)
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