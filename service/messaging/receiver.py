from threading import Thread

import xmpp


def message_callback(con, mess):
    print 'Received message:', mess.getFrom().getStripped(), mess.getBody()


class XMPPReceiver(Thread):
    connection = None  # type: xmpp.Client

    def __init__(self, receiver_login, receiver_password):
        super(XMPPReceiver, self).__init__()
        jid = xmpp.JID(receiver_login)
        user, server, password = jid.getNode(), jid.getDomain(), receiver_password

        self.connection = xmpp.Client(server=server, debug=[])
        conres = self.connection.connect()
        if not conres:
            raise ValueError("Unable to connect to server %s!" % server)
        if conres <> 'tls':
            print "Warning: unable to estabilish secure connection - TLS failed!"
        authres = self.connection.auth(user, password)
        if not authres:
            raise ValueError("Unable to authorize on %s - check login/password." % server)
        if authres <> 'sasl':
            print "Warning: unable to perform SASL auth os %s. Old authentication method used!" % server
        self.connection.RegisterHandler('message', message_callback)
        self.connection.sendInitPresence()

    def run(self):
        while True:
            self.connection.Process(1)
