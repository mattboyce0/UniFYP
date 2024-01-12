class EncryptedMessageAlt:
    def __init__(self, EncryptedData, TimingHash, MsgID, MessageType, MessageArrayHash, MessageSource):
        self.EncryptedMessageData = EncryptedData
        self.TimingHash = TimingHash
        self.MessageID = MsgID
        self.MessageType = MessageType
        self.MessageArrayHash = MessageArrayHash
        self.MessageSource = MessageSourc

    def PrintInformation(self):
        print("""
        ======================================
                ENCRYPTED MESSAGE
        ======================================
        Encrypted Data Length:  {}
        Timing Hash:            {}
        Message ID:             {}
        Message Type:           {}
        OriginatingArrayHash:   {}
        MessageSource:          {}
        ======================================
        """.format(len(self.EncryptedMessageData), self.TimingHash, self.MessageID, self.MessageType,
                   self.MessageArrayHash, self.MessageSource))


class EncryptedMessage:
    def __init__(self, EncryptedMessage, RawMessage, TimingHash, ACIDHash):
        self.EncryptedMessage = EncryptedMessage
        self.MessageType = ""
        self.RawMessage = RawMessage
        self.TimingHash = TimingHash
        self.ICAOAircraftIDHash = ACIDHash

        if self.RawMessage == "Null":
            self.Source = "REMOTE"
        else:
            self.Source = "LOCAL"

    def PrintMessage(self):
        print("""
        ************************************************************************
                                    Encrypted Message
        ************************************************************************
        Message Metadata  /
        ------------------
        Encrypted Data Length:      {}
        Original Message Type:      {}
        Aircraft ID Hash:           {}
        Timing Hash:                {}
        Originating Source:         {}
        ************************************************************************
        {}
        ************************************************************************
        """.format(len(self.EncryptedMessage), self.MessageType, self.ICAOAircraftIDHash, self.TimingHash, self.Source,
                   self.EncryptedMessage))
