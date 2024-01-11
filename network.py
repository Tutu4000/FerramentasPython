# Usa ARP (Adress resolution protocol) para descobrir dispositivos conectados na mesma rede
# route -n

import scapy.all as scapy
import optparse


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(
        dst="ff:ff:ff:ff:ff:ff")  # Quando um pacote é enviado para esse endereço, todos os dispositivos na rede recebem e processam o pacote.
    pacote = broadcast / arp_request  # combina os dois pacotes
    respondidos, nrespondidos = scapy.srp(pacote, timeout=1)  # iface = wlan0
    index = 0
    for i in respondidos:
        print("Endereço {}:".format(index))
        print("IP: " + i[1].psrc)  # ip recebida
        print("MAC: " + i[1].hwsrc)  # mac recebido
        print("\n")
        index += 1


def parse_argumentos():
    parser = optparse.OptionParser()
    parser.add_option("-i", dest="ip", help="Ip")
    (options, _) = parser.parse_args()
    return options


argumentos = parse_argumentos()
scan(argumentos.ip)
