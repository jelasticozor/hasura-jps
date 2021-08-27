import socket


def can_open_socket(host, port, timeout_in_sec=5.0):
    try:
        with socket.create_connection((host, port), timeout=timeout_in_sec):
            return True
    except OSError:
        return False
