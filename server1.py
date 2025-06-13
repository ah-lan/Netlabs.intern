import socket 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 12345))
server.listen(1)
print("am steady waiting for the client to connect...")

client, addr =server.accept()
print(f"Connection from {addr}has been established")

while True:
    data = client.recv(1024)
    if not data:
        break
    print(f"Received: {data.decode()}")
    client.sendall(data)  # Echo back the received data
