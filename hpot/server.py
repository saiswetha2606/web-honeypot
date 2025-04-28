import os
import json
import socket
import paramiko
from threading import Thread

# Load configuration
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "config.json")

with open(config_path, "r") as config_file:
    config = json.load(config_file)

# Honeypot class
class Honeypot(paramiko.ServerInterface):
    def __init__(self, log_file):
        self.log_file = log_file

    def check_auth_password(self, username, password):
        log_message = f"Login attempt - Username: {username}, Password: {password}"
        print(log_message)
        with open(self.log_file, "a") as log:
            log.write(log_message + "\n")
        return paramiko.AUTH_FAILED

# Start honeypot
def start_honeypot():
    host = config["host"]
    port = config["port"]
    max_connections = config["max_connections"]
    log_file = config["log_file"]
    banner = config["banner"]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(max_connections)
    print(f"Honeypot listening on {host}:{port}")

    while True:
        client, addr = server.accept()
        print(f"Connection from {addr}")
        client.sendall(banner.encode())
        transport = paramiko.Transport(client)
        transport.add_server_key(paramiko.RSAKey.generate(2048))
        server_instance = Honeypot(log_file)
        try:
            transport.start_server(server=server_instance)
            channel = transport.accept()
            if channel:
                channel.close()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client.close()

if __name__ == "__main__":
    start_honeypot()
