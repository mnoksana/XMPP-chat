import xmpp


class XMPPSender:
    connection = None  # type: xmpp.Client

    def __init__(self, sender_login, sender_password):
        jid = xmpp.JID(sender_login)
        user, server, password = jid.getNode(), jid.getDomain(), sender_password

        self.connection = xmpp.Client(server=jid.getDomain(),
                                      debug=[])

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

    def send(self, receiver, message):
        self.connection.send(xmpp.protocol.Message(to=receiver,
                                                   body=message))
