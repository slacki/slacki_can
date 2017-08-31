import queue
import socket
import struct
from threading import Thread

from slacki_can.message import Message


class Bus:
    def __init__(self, interface='vcan0'):
        self.message_struct = '=IB3x8s'

        self.sock = socket.socket(
            socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        try:
            self.sock.bind((interface,))
        except OSError:
            print('Could not bind to interface', interface)
            exit(1)
        
        self.queue = queue.LifoQueue()
        self.t_read = Thread(target=self.__read, name='CanBus Read Thread')
        self.t_read.start()

    def send(self, message):
        packet = struct.pack(self.message_struct, message.message_id, message.dlc, message.data)
        self.sock.send(packet)

    def send_raw(self, message_id, data):
        self.send(Message(message_id, data))

    def receive(self):
        return self.queue.get(block=True)

    def __read(self):
        while True:
            packet = self.sock.recv(16)
            message_id, dlc, data = struct.unpack(self.message_struct, packet)
            self.queue.put(Message(message_id, data, dlc=dlc))
