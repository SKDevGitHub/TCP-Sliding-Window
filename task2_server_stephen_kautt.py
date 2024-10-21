import socket
import random
import time

host = "localhost"
port = 12345
lossProb = 0.1

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print("Server Started")
    
    while True:
        connection, clientAddress = server.accept()
        print(f"Connection Found at {clientAddress}")
        try:
            while True:
                data = connection.recv(1024)
                if not data:
                    print("No Data")
                    break
                seqNum = int(data.decode())
                print(f"Received packet {seqNum}")

                if random.random() > lossProb:
                    print(f"Sending ACK for packet {seqNum}")
                    connection.sendall(str(seqNum).encode())
                else:
                    print(f"Packet {seqNum} lost")
        except socket.timeout:
            print("Socket timeout occured. Closing connection.")
        except ConnectionResetError:
            print(f"Connection was reset by client {clientAddress}")
        except Exception as e:
            print(f"An error occured: {e}")
        finally:
            connection.close()
            print(f"Connection with {clientAddress} closed.")
                 
if __name__ == "__main__":
    start()