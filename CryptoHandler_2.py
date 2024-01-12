from cryptography.fernet import Fernet
import json

class Main:
    def __init__(self):
        #elf.FernetCipherObjects = [[CipherObj, MessageID]]
        self.FernetCipherObjects = []
        self.Utils = Utils()

    # Generate and return a fernet cipher, ready for use.
    def GetFernetObject(self):
        Key = Fernet.generate_key()
        return Fernet(Key), Key

    # Encrypt a message object.
    def EncryptMessageObject(self, MessageObject):
        # Variable Definitions
        FernetCipher, Key = self.GetFernetObject()
        MessageType = MessageObject.GetMessageType()
        AircraftICAOID = MessageObject.ICAOAircraftID
        AircraftIDHash = hash(AircraftICAOID)

        #Convert message into bytes
        MessageBytesDict = self.Utils.ConvertDictToBytes(MessageObject.RawMessage, 'utf-8')

        #Encrypt bytes-message
        EncryptedMessageDict = FernetCipher.encrypt(MessageBytesDict)

        #Return the EncryptedMessage() object to calling process.
        return EncryptedMessage(EncryptedMessageDict, MessageType, MessageObject.RawMessage, Key, 0, AircraftIDHash), Key




class EncryptedMessage:
    # Class to contain an encrypted datalink message
    def __init__(self, EncryptedMessage, MessageType, RawMessage, Key, TimingHash, ACIDHash):

        # raw encrypted message, stored as a bytes-encoded encrypted dictionary
        self.EncryptedMessage = EncryptedMessage

        # Original type of message, either CPDLC or ACARS
        self.MessageType = MessageType

        # Raw, unencrypted message - Only filled if used in encrypting process
        self.RawMessage = RawMessage

        # Fernet cipher key
        self.Key = Key

        # Hash of the timing data - DEPRECEATED
        self.TimingHash = TimingHash

        # Hash of the aircraft ID - Used for message identification
        self.ICAOAircraftIDHash = ACIDHash

        if self.Key == None:
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



class Utils:
    def __init__(self):
        pass

    def ConvertDictToBytes(self, InputDict, Encoding):
        BytesFromDict = json.dumps(InputDict).encode(Encoding)
        return BytesFromDict

    def ConvertBytesToDict(self, InputBytes, Encoding):
        DictFromBytes = json.loads(InputBytes.decode(Encoding))
        return DictFromBytes

    def FernetDecrypt(self, Ciphertext, Key):
        FernetCipher = Fernet(Key)
        try:
            Plaintext = FernetCipher.decrypt(Ciphertext)
        except:
            return 0
        return Plaintext


