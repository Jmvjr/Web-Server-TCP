#import socket module
from socket import *
import sys # In order to terminate the program
from threading import Thread

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare server socket
serverSocket.bind(("", 10000))
serverSocket.listen(5)

def client(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        #Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send(
            "Content-Type: text/html; charset=utf-8\r\n".encode()
        )
        connectionSocket.send("\r\n".encode())
        #Fill in start
        #Fill in end
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        
    except IOError:
        message = "<html><body><h1>404 Not Found</h1></body></html>"
        
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(message.encode())
    
    connectionSocket.close()

def make_client_thread(clientSocket):
    return Thread(
        target=client,
        args=(clientSocket,)
    )

while True:
    print("Ready to serve...")

    clientSocket, addr = serverSocket.accept()

    ct = make_client_thread(clientSocket)
    ct.start()
