from threading import Thread

import xmpp


def message_callback(con, mess):
    print 'Received message:', mess.getFrom().getStripped(), mess.getBody()


class XMPPReceiver(Thread):
    connection = None  # type: xmpp.Client

    def __init__(self, receiver_login, receiver_password):
        super(XMPPReceiver, self).__init__()  # Thread constructor
        jid = xmpp.JID(receiver_login)  # init jid object
        user, server, password = jid.getNode(), jid.getDomain(), receiver_password

        self.connection = xmpp.Client(server=server, debug=[])  # init client connection
        conres = self.connection.connect()  # connect to domain
        if not conres:  # check connection
            raise ValueError("Unable to connect to server %s!" % server)
        if conres != 'tls':  # warn if no TLS protocol
            print "Warning: unable to estabilish secure connection - TLS failed!"
        authres = self.connection.auth(user, password)  # authenticate
        if not authres:     # assert auth
            raise ValueError("Unable to authorize on %s - check login/password." % server)
        if authres != 'sasl':  # warn if no SASL protocol in auth
            print "Warning: unable to perform SASL auth os %s. Old authentication method used!" % server
        self.connection.RegisterHandler('message', message_callback)    # add handler for messages
        self.connection.sendInitPresence()  # for old servers

    def run(self):
        while True:
            self.connection.Process(1)  # check for new messages every 1 second
