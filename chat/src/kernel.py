#-*- coding: utf-8 -*-

import socket
from os import system
from threading import Thread
from gc import collect

class Server(object):
    def __init__(self, host : str, port : int, encoding : str = 'utf-8'):
        self.host = host
        self.port = port
        self.encoding = encoding
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.clients = []
        self.is_running = True

    def send_to_clients(self, sender : socket.socket|None, message : str):
        for client in self.clients:
            client != sender and client.send(message.encode(self.encoding))

    def client_processing(self, client : socket.socket, address : tuple):
        while(self.is_running and client in self.clients):
            host, port = address
            message = client.recv(1024).decode(self.encoding).strip()
            if(not self.is_running): break
            elif(not message):
                message = f' [-] {host}:{port} - disconnected.'
                self.clients.remove(client)
                self.send_to_clients(client, message)
                print(message)
            else:
                message = f' [{host}:{port}]: {message}'
                self.send_to_clients(client, message)

    def client_registration(self, client : socket.socket, address : tuple):
        if(client in self.clients): return
        self.clients.append(client)
        Thread(target = self.client_processing, args = (client, address)).start()
        host, port = address
        message = f' [+] {host}:{port} - connected.'
        self.send_to_clients(client, message)
        print(message)

    def process_connections(self):
        while(self.is_running):
            try:
                client, address = self.socket.accept()
                if(not self.is_running): break
                self.client_registration(client, address)
                collect()
            except: pass

    def process_commands(self):
        while(self.is_running):
            command = input().strip().lower()
            print(f'\x1b[F [{self.host}:{self.port}]: {command}')
            if(command == 'stop'):
                self.stop()

    def start_stream(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.socket.setblocking(0)
        print(f' [#] The server is launched on {self.host}:{self.port} ~\n')
        print(' ~ Enter "stop" to stop the server.\n')

    def stop(self):
        self.is_running = False
        self.send_to_clients(None, '☠️')
        socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ).connect((self.host, self.port))
        self.socket.close()
        print('\n [#] Server\'s been stopped.\n')

    def launch(self):
        system('clear')
        self.start_stream()
        Thread(target = self.process_connections).start()
        Thread(target = self.process_commands).start()


class Client(object):
    def __init__(self, encoding : str = 'utf-8'):
        self.encoding = encoding
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.is_running = True

    def send_message(self, message : str):
        self.socket.send(message.encode(self.encoding))

    def process_messages(self):
        while(self.is_running):
            try: message = self.socket.recv(1024).decode(self.encoding)
            except: continue
            if(message == '☠️'):
                self.exit()
                print(' ~ Press "enter" to exit.')
                break
            elif(message): print(message)
            collect()

    def process_user_input(self):
        while(self.is_running):
            user_input = input().strip()
            if(not self.is_running): break
            if(not user_input): continue
            print(f'\x1b[F [you]: {user_input}')
            if(user_input == '/exit'):
                self.exit()
                break
            self.send_message(user_input)

    def exit(self):
        self.is_running = False
        self.socket.close()
        print('\n [#] Connection closed.\n')

    def connect(self, host : str, port : int):
        system('clear')
        self.socket.connect((host, port))
        self.socket.setblocking(0)
        Thread(target = self.process_messages).start()
        Thread(target = self.process_user_input).start()
        print(f' [#] Connected to {host}:{port} ~ \n')
        print(' ~ Enter "/exit" to exit.\n')
