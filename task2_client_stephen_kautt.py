import socket
import time

host = "localhost"
port = 12345
packets = 50

def start():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        
        cwnd = 1
        ssthresh = 10
        seqNum = 0
        timeout = 2
        dupAcks = 0
        lastAck = -1
        
        def simulate():
            time.sleep(0.5)
        
        def handleAck(ack):
            nonlocal cwnd, ssthresh, dupAcks, lastAck
            if ack == lastAck:
                dupAcks += 1
            else:
                dupAcks = 0
                lastAck = ack
                if cwnd < ssthresh:
                    cwnd *= 2
                else:
                    cwnd += 1
                    
            if dupAcks == 3:
                ssthresh = cwnd//2
                cwnd = ssthresh
                dupAcks = 0
                
        def handleTimeout():
            nonlocal cwnd, ssthresh
            print("Timeout Occured")
            ssthresh = cwnd//2
            cwnd = 1
            
        while seqNum < packets:
            for i in range(cwnd):
                if seqNum >= packets:
                    break
                print(f"Sending Packet {seqNum}, cwnd = {cwnd}, ssthresh = {ssthresh}")
                client.sendall(str(seqNum).encode())
                seqNum += 1
                
            try:
                client.settimeout(timeout)
                data = client.recv(1024)
                if not data:
                    print("Server Closed")
                    break
                ack = int(data.decode())
                print(f"Received ACK {ack}")
                handleAck(ack)
            except socket.timeout:
                handleTimeout()
            except ConnectionResetError:
                print("Connection was reset by the server.")
                break
            simulate()
    except ConnectionResetError:
        print("Connection was closed by server unexpectedly.")
    finally:
        client.close()
        print("Client connection closed.")
    
if __name__ == "__main__":
    start()