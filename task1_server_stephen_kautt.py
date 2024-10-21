import socket
import random
import time

packetLossProb = 0.1
packetAmount = 10000
host = "localhost"
port = 12345
expectedSeq = 0

def start():
    global expectedSeq
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print("Server Started")
        
        conn, addr = s.accept()
        with conn:
            print("Connection Found")
            while expectedSeq < packetAmount:
                data = conn.recv(1024)
                
                if not data:
                    print("NO DATA HERE")
                    break
                
                seqNum = int(data.decode())
                
                if random.random() < packetLossProb:
                    print(f"Packet {seqNum} dropped at server\n")
                    continue
                
                print(f"Received packet {seqNum}\n")
                time.sleep(0.1)
                
                if seqNum == expectedSeq:
                    expectedSeq += 1
                print(f"Sending the Ack for packet {expectedSeq - 1}\n")
                conn.sendall(str(expectedSeq - 1).encode())
        
if __name__ == "__main__":
    start()