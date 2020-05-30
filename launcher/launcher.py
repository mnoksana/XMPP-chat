import json

from service.messaging.receiver import XMPPReceiver
from service.messaging.sender import XMPPSender
from time import sleep


class Launcher:
    def __init__(self):
        pass

    @classmethod
    def launch(cls):
        with open('sender_config.json', 'r') as configFile:
            sender_config = json.load(configFile)   # load json config for sender
        sender = XMPPSender(**sender_config)    # map config to constructor
        with open('receiver_config.json', 'r') as configFile:
            receiver_config = json.load(configFile)     # load json config for receiver
        receiver = XMPPReceiver(**receiver_config)  # map config to constructor
        receiver.start()    # start receiver thread

        while sender.connection.isConnected():  # messaging while connection is alive
            body = raw_input("Sent message: ")
            sender.send(str(receiver_config['receiver_login']), body)
            sleep(1)
