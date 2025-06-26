# Liabary
from asyncio import Runner
import logging
from logging.handlers import RotatingFileHandler
import socket
import paramiko
import threading
import atexit

#Constansts
logging_format = logging.Formatter('%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
SSH_BANNER = "SSH-2.0-MySSHServer_2.7.2"

#host_key ='server.key'
host_key = paramiko.RSAKey(filename='server.key')

#loggers & logging file
funnel_logger=logging.getLogger('Funnel_logger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler('audit.log', maxBytes=2000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

creds_logger=logging.getLogger('Creds_logger')
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler('Cmd_audit.log', maxBytes=2000, backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)

# Emulated Shell
def emulated_shell(channel, client_ip):
    channel.send(b"kompeki@plaza:~$")
    command = b""
    while True:
        char = channel.recv(1)
        if not char:
            channel.close()
            break

        # Handle backspace (ASCII DEL 127 or BS 8)
        if char in [b'\x7f', b'\x08']:
            if len(command) > 0:
                command = command[:-1]
                # Move cursor back, erase char, move back again
                channel.send(b'\b \b')
            continue

        # Only echo printable characters
        if char not in [b'\r', b'\n']:
            channel.send(char)
            command += char
        else:
            cmd = command.strip()

            # EXIT command handling

            if cmd == b'exit':
                channel.send(b"\r\nGoodbye!\r\n")
                creds_logger.info(f'client {client_ip} Executed Command: {command.strip().decode()}')
                funnel_logger.info(f'client {client_ip} disconnected')
                print(f"Client {client_ip} disconnected")
                channel.close()
                break

            # PWD Command handling
            
            elif cmd == b'pwd':
                response = b"/usr/local\r\n"
                creds_logger.info(f'client {client_ip} Executed Command: {command.strip().decode()}')

            # Clear Command handling
            
            elif cmd == b'clear':
                response = b"\033[H\033[J"
                creds_logger.info(f'client {client_ip} Executed Command: {command.strip().decode()}')

            # Whoami Command handling
            
            elif cmd == b'whoami':
                response = b"neon\r\n"
                creds_logger.info(f'client {client_ip} Executed Command: {command.strip().decode()}')

            # LS Command handling
            
            elif cmd == b'ls':
                response = b"corpoHoney.conf\r\n"
                creds_logger.info(f'client {client_ip} Executed Command: {command.strip().decode()}')

            # Cat Command handling
            
            elif cmd == b'cat corpoHoney.conf':
                response = b"corporate honeypot configuration file\r\n"
                creds_logger.info(f'client {client_ip} Executed Command: {command.strip().decode()}')
            # Help Command handling
            
            elif cmd == b'help':
                response = b"Available commands: pwd, clear, whoami, ls, cat, help, exit\r\n"
                creds_logger.info(f'client {client_ip} Executed Command: {command.strip().decode()}')
            # Unknown Command handling
            
            else:
                response = b"Command not found\r\n"
                creds_logger.info(f'client {client_ip} Executed Command: {command.strip().decode()}')

            # Send the response back to the client

            if cmd != b'exit':
                channel.send(b"\r\n")
                channel.send(response)
                channel.send(b"kompeki@plaza:~$")
            command = b""

# SSH SERVER + Socket

class Server(paramiko.ServerInterface):
    def __init__(self,client_ip, input_username=None, input_password=None):
        self.event = threading.Event()
        self.client_ip =client_ip
        self.input_username=input_username
        self.input_password=input_password

    def check_channel_request(self, kind:str, chanid:int) -> int:
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def get_allowed_auths(self,username):
        return "password"

    def check_auth_password(self, username, password):
        # First log the attempt
        funnel_logger.info(f'Client {self.client_ip} attempted to login with Username:{username}, Password:{password}')
        creds_logger.info(f'Client {self.client_ip} attempted to login with Username:{username}, Password:{password}')
        
        if self.input_username is not None and self.input_password is not None:
            if username == self.input_username and password == self.input_password:
                # Log successful login
                funnel_logger.info(f'Client {self.client_ip} logged in SUCCESSFULLY with Username:{username}')
                creds_logger.info(f'Client {self.client_ip} logged in SUCCESSFULLY with Username:{username}')
                return paramiko.AUTH_SUCCESSFUL
            else:
                # Log failed login with specific reason
                if username != self.input_username:
                    reason = "Wrong Username"
                else:
                    reason = "Wrong Password"
                funnel_logger.info(f'Client {self.client_ip} login FAILED: {reason} for Username:{username}')
                creds_logger.info(f'Client {self.client_ip} login FAILED: {reason} for Username:{username}')
                return paramiko.AUTH_FAILED
        else:
            # This is the case where we accept any credentials
            funnel_logger.info(f'Client {self.client_ip} logged in SUCCESSFULLY with Username:{username} (any credentials Accepted)')
            creds_logger.info(f'Client {self.client_ip} logged in SUCCESSFULLY with Username:{username} (any credentials Accepted)')
            return paramiko.AUTH_SUCCESSFUL    
            
    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_exec_request(self, channel, term,width, height, pixelwidth, pixelheight, modes):
        return True
        
    def check_channel_exec_request(self, channel, command):
        command = str(command)
        return True
        
def client_handle(client,adr,username,password):
    client_ip = adr[0]
    print(f"Connected to server {client_ip}")

    try:
        
        transport = paramiko.Transport(client)
        transport.local_version = SSH_BANNER
        server = Server(client_ip=client_ip, input_username=username, input_password=password)

        transport.add_server_key(host_key)

        transport.start_server(server=server)

        channel = transport.accept(100)
        if channel is None:
            logging.error(f"Failed to open channel for {client_ip}")
            return
        
        standard_banner = b"Welcome to the SSH Server!\r\n"
        channel.send(standard_banner)
        emulated_shell(channel, client_ip=client_ip)


    except Exception as error:
        print(f"Error: {error}")
        print("Connection closed.")

    finally:
        try:
            transport.close()
        except Exception as error:
            print(f"Error closing transport: {error}")
            print("Connection closed.")

        client.close()
    
# provision SSh - based Honey Pot             

def honey_pot(address,username, password, port):

    socks=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socks.bind((address, port))

    socks.listen(100)
    print(f"SSH server listening on {address}:{port}")

    while True:
        try:
            client, adr = socks.accept()
            ssh_honeypot_thread = threading.Thread(target=client_handle, args=(client, adr, username, password))
            ssh_honeypot_thread.start()
            print(f"Connection from {adr}")
        
        except Exception as error:
            print(f"Error: {error}")

#log HANDLERS

def close_loggers():
    for handler in funnel_logger.handlers:
        handler.close()
    for handler in creds_logger.handlers:
        handler.close()

atexit.register(close_loggers)


#username and password for the honeypot

#honey_pot('127.0.0.1', 'neon', 'neon123',2223)

#test
