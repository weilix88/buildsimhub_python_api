import socket


def internet(host="8.8.8.8", port=53, timeout=3):   # port 53: DNS
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return True
    except:
        return False
