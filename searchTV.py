import socket
import sys
import re
import requests

from tvs.lg import LGSmartTV


def getip():
    strngtoXmit = 'M-SEARCH * HTTP/1.1' + '\r\n' + \
                  'HOST: 239.255.255.250:1900' + '\r\n' + \
                  'MAN: "ssdp:discover"' + '\r\n' + \
                  'MX: 2' + '\r\n' + \
                  'ST: urn:schemas-upnp-org:device:MediaRenderer:1' + '\r\n' + '\r\n'

    bytestoXmit = strngtoXmit.encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    found = False
    gotstr = 'notyet'
    i = 0
    ipaddress = None
    sock.sendto(bytestoXmit, ('239.255.255.250', 1900))

    while not found and i <= 5 and gotstr == 'notyet':
        try:
            gotbytes, addressport = sock.recvfrom(512)
            gotstr = gotbytes.decode()
        except:
            i += 1
            sock.sendto(bytestoXmit, ( '239.255.255.250', 1900))
        if re.search('LG', gotstr):
            ipaddress, _ = addressport
            found = True
        else:
            gotstr = 'notyet'
        i += 1
    sock.close()
    if not found:
        sys.exit("Lg TV not found")

    return ipaddress


def main():
    ip_address = getip()
    key = "467132"

    lg_tv = LGSmartTV(ip_address, auth_key=key, session="2134347550")
    lg_tv.authenticate()
    lg_tv.send_command("TV_CMD_VOLUME_UP")

main()

#print getip()
