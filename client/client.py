import socket
import os
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
client.connect(('localhost', 12345))

picture = open('profile.jpg', 'rb')  # Open the image file in binary mode
if not os.path.exists('profile.jpg'):
    print(f"File not found!")
    client.close()
    exit()

with open('profile.jpg', 'rb') as file:
    picture_data = file.read()  

picture_size = len(picture_data)
client.sendall(str(picture_size).encode()) # Send the size of the image file
readymessage = client.recv(1024)  # Wait for the server to be ready
print(f"Friend says: {readymessage.decode()}")
bytes_sent = 0
chunk_size = 4096

print(f"Sending {picture_size} bytes of data...")

while bytes_sent < picture_size:
    chunk = picture_data[bytes_sent:bytes_sent + chunk_size]
    client.sendall(chunk)  # Send the image data in chunks
    bytes_sent += len(chunk)
    print(f"Sent {bytes_sent} bytes out of {picture_size} bytes")

thanks_message = client.recv(1024)  # Wait for the server's acknowledgment
print(f"Friend says: {thanks_message.decode()}")
print("Image sent successfully!")
client.close()  # Close the socket connection