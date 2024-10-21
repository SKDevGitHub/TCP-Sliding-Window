import threading
import time
import random
import socket

window = 5
start = 0
end = 4
nextSeq = 0
ackRecieve = -1
timeout = 2
packetAmount = 10000
packetLossProb = 0.1
host = "localhost"
port = 12345
lock = threading.Lock()

def sendPacket(seqNum, conn):
    if random.random() < packetLossProb:
        print(f"Packet {seqNum} has become lost!")
        return False
    time.sleep(1)
    print(f"Sending packet {seqNum}")
    conn.sendall(str(seqNum).encode())
    return True
        
def recieveAck(conn):
    global ackRecieve
    global start
    global end
    conn.settimeout(timeout)
    while ackRecieve < packetAmount - 1:
        try:
            ack = conn.recv(1024)
            if not ack:
                print("Connection Closed")
                break
            ack = int(ack.decode())
            print(f"Received ACK: {ack}\n")
            time.sleep(1)
            with lock:
                ackRecieve = max(ackRecieve, ack)
                if ackRecieve >= start:
                    start = ackRecieve + 1
                    end = min(start + window - 1, packetAmount - 1)
        except socket.timeout:
            print(f"UH OH Timeout has occured, will retransmit packets {start} to {end}")
                
def startClient():
    global nextSeq
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            ackThread = threading.Thread(target = recieveAck, args = (s,))
            ackThread.start()
        
            while start < packetAmount:
                for i in range(start, end + 1):
                    if i < packetAmount and sendPacket(i, s):
                        nextSeq = i + 1
                with lock:
                    if ackRecieve >= packetAmount - 1:
                        break
                    
            ackThread.join()
        except Exception as e:
            print(f"An error occured: {e}")
    
if __name__ == "__main__":
    startClient()