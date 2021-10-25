import select, socket

buffer = ""

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("localhost", 7778))

while True:
    data, addr = s.recvfrom(1024)
    if data:
        print(data)
    else:
        break
s.close()
