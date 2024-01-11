import optparse
import subprocess


def change_mac(interface, novoMac):
    print("Mac adress na interface: {} \nSerá mudado para: {}".format(interface, novoMac))
    subprocess.call("ifconfig {} down".format(interface), shell=True)
    subprocess.call("ifconfig {} hw ether {}".format(interface, novoMac), shell=True)
    subprocess.call("ifconfig {} up".format(interface), shell=True)


def get_argumentos():
    parser = optparse.OptionParser()
    parser.add_option("-i", dest="interface", help="Interface et0, wlan, etc")
    parser.add_option("-m", dest="novoMac", help="Mac novo desejado")
    (opcoes, _) = parser.parse_args()
    if not opcoes:
        parser.error("Por favor especifique os argumentos")
    return opcoes


def checar_novo_mac(mac_esperado):
    # Checa se novo mac é igual ao esperado.
    ifconfig_result = subprocess.check_output(["ifconfig", argumentos.interface])
    ifconfig_result = ifconfig_result.decode(
        'utf-8')  # subprocess check output retorna um objeto bytes que precisa ser decodificado para string
    if mac_esperado in ifconfig_result:
        print("Mac Adress alterado com sucesso para {}".format(mac_esperado))
    else:
        print("Mac Adress não foi alterado")


argumentos = get_argumentos()
change_mac(argumentos.interface, argumentos.novoMac)
checar_novo_mac(argumentos.novoMac)
