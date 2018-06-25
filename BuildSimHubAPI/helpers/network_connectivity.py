import socket


def internet(host="8.8.8.8", port=53, timeout=3):   # port 53: DNS
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False
