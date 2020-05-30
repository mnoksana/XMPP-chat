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
            sender_config = json.load(configFile)
        sender = XMPPSender(**sender_config)
        with open('receiver_config.json', 'r') as configFile:
            receiver_config = json.load(configFile)
        receiver = XMPPReceiver(**receiver_config)
        receiver.start()

        while sender.connection.isConnected():
            body = raw_input("Sent message: ")
            sender.send(str(receiver_config['receiver_login']), body)
            sleep(1)
