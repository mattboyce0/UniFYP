import socket
import time
import datetime
import json
import csv
import cProfile

try:
    # Import Notify.py - used for coloured terminal text/bullet points
    # Import Debug.py - Used for printing additional 'debug' messages that can be enabled and disabled.
    import util.Notify as NotifyMain

    Notify = NotifyMain.Main()
    Notify.SetMode("C")

    Debug = NotifyMain.Debug()
    Debug.SetDebugMode(True)
except(ImportError):
    print("Cannot import Notify.")
    exit()

SECONDS_IN_MIN = 60
C = 299792458

# NetHandler Import
try:
    import NetHandler_2 as NetHandler
except(ImportError):
    Notify.Error("Failed to load NetHandler")

# Cryptohandler import
try:
    import CryptoHandler_2 as CryptoHandler
except(ImportError):
    Notify.Error("Failed to load CryptoHandler")

# CPDLC Message Object Import
try:
    import CPDLCMessage as CPDLCMessage
except(ImportError):
    Notify.Error("Failed to load CPDLCMessage")

# ACARS Message Object Import
try:
    import ACARSMessage as ACARSMessage
except(ImportError):
    Notify.Error("Failed to load ACARSMessage")

# EncryptedMessageObject Import
try:
    import EncMessage as EncryptedMessageObject
except(ImportError):
    Notify.Error("Failed to load EncMessage")

# JsonTools Import
try:
    from MessageUtilities.MessageAnalysis import JsonTools
except(ImportError):
    Notify.Error("Failed to import JsonTools")

# MessageUtils import
try:
    from MessageUtilities.MessageAnalysis import MessageAnalysis
except(ImportError):
    Notify.Error("Failed to load MessageUtils")
Debug.Message("Successfully Imported Required Modules")

# Main Message Processing Block
class MessageProcessingMain:
    def __init__(self, MasterMessageList, ProgMode):
        # Object Definition
        self.CryptoHandler = CryptoHandler.Main()
        self.CryptoUtils = CryptoHandler.Utils()
        #self.NetHandler = NetHandler.Server("127.0.0.1", 5995)
        self.JsonTools = JsonTools()
        self.MessageUtils = MessageAnalysis()

        # Reads JSON message objects from a file or list of files
        self.MasterMessageList = self.JsonTools.MultiLoad(MasterMessageList)

        # Lists of sorted message objects
        self.ACARSMessageList = []
        self.CPDLCMessageList = []
        self.OtherMessageList = []

        # Network variables
        self.HOST = "127.0.0.1"
        self.PORT = 15995
        self.ReceivedDataBuffer = []

        # Variables for TemporalAnalysis function
        self.TimeSecList = []
        self.TimeSegmentSizeMins = 5

        # Variables for crypto work
        #elf.EncryptedObjectArray = [["ACARS", 0, EncryptedObject]]
        self.EncryptedObjectArray = []
        self.RawEncryptedMessageArray = []
        self.KeyFileName = "keyfile.json"
        self.KeyArray = []


        if ProgMode == "TX":
            self.TransmitterSetup()
        elif ProgMode == "RX":
            self.ReceiverSetup()
        elif ProgMode == "DB":
            self.DebugSetup()


        #self.InitialSetup()

    ## Setup functions
    def TransmitterSetup(self):
        # Start the main program in transmitter mode
        # Decode AVLC messages
        Notify.Info("Extracting Messages from File")
        self.ExtractMessagesFromFile(self.MasterMessageList)

        # Encrypt Messages
        Notify.Info("Encrypting Messages")
        self.EncryptMessages()

        # Transmit Messages
        Notify.Info("Transmitting Messages")
        self.TransmitAllMessages()

    def ReceiverSetup(self):
        # Start the main program in receiver mode
        # Create server instance and receive encrypted messages. Store messages in encrypted message array
        self.StartNetServer()

        # Instantialise encrypted messages into EncryptedMessage() objects
        self.LoadEncryptedMessages(self.RawEncryptedMessageArray, self.KeyFileName)
        self.DecryptMessages(self.EncryptedObjectArray, self.KeyArray)

    def DebugSetup(self):
        self.ExtractMessagesFromFile(self.MasterMessageList)
        self.EncryptMessages()
        self.WriteKeysToFile(self.EncryptedObjectArray)
        self.LoadKeyFile('keyfile.csv')


        for count in range(0,len(self.EncryptedObjectArray)):
            self.ReceivedDataBuffer.append(self.EncryptedObjectArray[count][0].RawMessage)
        Profiler = cProfile.Profile()
        Profiler.enable()
        self.DecryptMessages(self.EncryptedObjectArray, self.KeyArray)
        Profiler.disable()
        Profiler.print_stats()

    ## Message Extraction
    def ExtractMessagesFromFile(self, RawMessageArray):
        ACARSMessagePresent = False
        CPDLCMessagePresent = False
        for message in range(0,len(RawMessageArray)):

            ## Variable Definitions
            USec = 0
            Sec = 0
            MsgFreq = ""
            SigLevel = ""
            NoiseLevel = ""
            DEBUG_msg_store = RawMessageArray[message]

            ICAOAircraftID = ""

            #ACARS
            CRC = False
            AircraftReg = ""
            ACARSMode = ""
            ACARSLabel = ""
            ACARSBlockID = ""
            ACARSAck = ""
            FlightNum = ""
            MessageNum = ""
            MessageSeq = ""
            Sublabel = ""
            MessageText = ""

            #CPDLC
            MsgID = ""
            MsgRef = ""
            TxYear = ""
            TxMonth = ""
            TxDay = ""
            TxHour = ""
            TxMin = ""
            TxSec = ""
            LogicalAckReq = False
            MsgData = []
            CPDLCMessageIdentifier = ""

            ## Extract timing data
            try:
                USec = RawMessageArray[message]["vdl2"]["t"]["usec"]
                Sec = RawMessageArray[message]["vdl2"]["t"]["sec"]
                MsgFreq = RawMessageArray[message]["vdl2"]["freq"]
                SigLevel = RawMessageArray[message]["vdl2"]["sig_level"]
                NoiseLevel = RawMessageArray[message]["vdl2"]["noise_level"]
            except(KeyError):
                Debug.Message("No timing data for {}.".format(message))

            ## Extract ICAO 24-bit Aircraft ID
            try:
                ICAOAircraftID = RawMessageArray[message]["vdl2"]["avlc"]["src"]["addr"]
            except(KeyError):
                Debug.Message("No ICAO ID for {}".format(message))

            #Check Message Type
            if self.CheckACARSPresence(RawMessageArray[message]):
                ACARSMessagePresent = True
                try:
                    CRC = RawMessageArray[message]["vdl2"]["avlc"]["acars"]["crc_ok"]
                    AircraftReg = RawMessageArray[message]["vdl2"]["avlc"]["acars"]["reg"]
                    ACARSMode = RawMessageArray[message]["vdl2"]["avlc"]["acars"]["mode"]
                    ACARSLabel = RawMessageArray[message]["vdl2"]["avlc"]["acars"]["label"]
                    ACARSBlockID = RawMessageArray[message]["vdl2"]["avlc"]["acars"]["blk_id"]
                    ACARSAck = RawMessageArray[message]["vdl2"]["avlc"]["acars"]["ack"]
                    FlightNum = RawMessageArray[message]["vdl2"]["avlc"]["acars"]["flight"]
                    MessageNum = RawMessageArray[message]["vdl2"]["avlc"]["acars"]["msg_num"]
                    MessageSeq = RawMessageArray[message]["vdl2"]["avlc"]["acars"]["msg_num_seq"]
                    MessageText = RawMessageArray[message]["vdl2"]["avlc"]["acars"]["msg_text"]
                except(KeyError):
                    ACARSMessagePresent = False
            else:
                ACARSMessagePresent = False

            if self.CheckCPDLCPresence(RawMessageArray[message]):
                CPDLCMessagePresent = True
                try:
                    try:
                        MsgID = RawMessageArray[message]["vdl2"]["avlc"]["x25"]["clnp"]["cotp"]["cpdlc"][
                            "atc_downlink_message"]["header"]["msg_id"]
                    except(KeyError):
                        MsgID = -1
                    try:
                        MsgRef = RawMessageArray[message]["vdl2"]["avlc"]["x25"]["clnp"]["cotp"]["cpdlc"][
                            "atc_downlink_message"]["header"]["msg_ref"]
                    except(KeyError):
                        MsgRef = "None"
                    try:
                        TxYear = RawMessageArray[message]["vdl2"]["avlc"]["x25"]["clnp"]["cotp"]["cpdlc"][
                            "atc_downlink_message"]["header"]["timestamp"]["date"]["year"]
                    except(KeyError):
                        TxYear = 0
                    try:
                        TxMonth = RawMessageArray[message]["vdl2"]["avlc"]["x25"]["clnp"]["cotp"]["cpdlc"][
                            "atc_downlink_message"]["header"]["timestamp"]["date"]["month"]
                    except(KeyError):
                        TxMonth = ""
                    try:
                        TxDay = RawMessageArray[message]["vdl2"]["avlc"]["x25"]["clnp"]["cotp"]["cpdlc"][
                            "atc_downlink_message"]["header"]["timestamp"]["date"]["day"]
                    except(KeyError):
                        TxDay = ""
                    try:
                        TxHour = RawMessageArray[message]["vdl2"]["avlc"]["x25"]["clnp"]["cotp"]["cpdlc"][
                            "atc_downlink_message"]["header"]["timestamp"]["time"]["hour"]
                    except(KeyError):
                        TxHour = 0
                    try:
                        TxMin = RawMessageArray[message]["vdl2"]["avlc"]["x25"]["clnp"]["cotp"]["cpdlc"][
                            "atc_downlink_message"]["header"]["timestamp"]["time"]["min"]
                    except(KeyError):
                        TxMin = 0
                    try:
                        TxSec = RawMessageArray[message]["vdl2"]["avlc"]["x25"]["clnp"]["cotp"]["cpdlc"][
                            "atc_downlink_message"]["header"]["timestamp"]["time"]["sec"]
                    except(KeyError):
                        TxSec = 0
                    try:
                        LogicalAckReq = RawMessageArray[message]["vdl2"]["avlc"]["x25"]["clnp"]["cotp"]["cpdlc"][
                            "atc_downlink_message"]["header"]["logical_ack"]
                    except(KeyError):
                        LogicalAckReq = False
                    try:
                        MsgData = RawMessageArray[message]["vdl2"]["avlc"]["x25"]["clnp"]["cotp"]["cpdlc"][
                            "atc_downlink_message"]["msg_data"]
                    except(KeyError):
                        MsgData = ["none"]

                    CPDLCMessageIdentifier = message
                except():
                    CPDLCMessagePresent = False
            else:
                CPDLCMessagePresent = False

            ## Instantiate correct object based on extracted data
            if ACARSMessagePresent:
                self.ACARSMessageList.append(ACARSMessage.Message(Sec, USec, MsgFreq, SigLevel, NoiseLevel, CRC,
                                                                  AircraftReg, ACARSMode, ACARSLabel, ACARSBlockID, ACARSAck, FlightNum,
                                                                  MessageNum, MessageSeq, Sublabel, MessageText,
                                                                  RawMessageArray[message], ICAOAircraftID))
            elif CPDLCMessagePresent:
                self.CPDLCMessageList.append(CPDLCMessage.Message(USec, Sec, MsgFreq, SigLevel, NoiseLevel, MsgID, MsgRef, TxYear, TxMonth,
                                                                  TxDay, TxHour, TxMin, TxSec, LogicalAckReq, MsgData,
                                                                  CPDLCMessageIdentifier, RawMessageArray[message], ICAOAircraftID))

            else:
                self.OtherMessageList.append(RawMessageArray[message])
        Notify.Success("Message Extraction Complete. {} ACARS, {} CPDLC, {} Others".format(len(self.ACARSMessageList), len(self.CPDLCMessageList), len(self.OtherMessageList)))


    def CheckACARSPresence(self, Message):
        #ACARSMessageElementsPresent = 0
        try:
            if Message["vdl2"]["avlc"]["acars"] != None:
                return True
            else:
                return False
        except(KeyError):
            return False

    def CheckCPDLCPresence(self, Message):
        try:
            if Message["vdl2"]["avlc"]["x25"]["clnp"]["cotp"]["cpdlc"] != None:
                return True
            else:
                return False
        except(KeyError):
            return False

    ## Network Functions
    def StartNetServer(self):
        # Receive Encrypted Messages from remote host
        self.Reciever = NetHandler.Server(self.HOST, self.PORT, "RX")
        ReceivedDataList = []
        while True:
            self.Reciever.Receive()
            try:
                Notify.Success("Receiving Data...")
                self.ReceivedDataBuffer = self.Reciever.GetReceivedData()

                for count in range(0,len(self.ReceivedDataBuffer)):
                    if self.ReceivedDataBuffer[count] == b'BREAK':
                        Notify.Info("Caught Break Signal")
                    else:
                        pass
                break

            except():
                Notify.Warning("Server Exception Caught.")
                Notify.Info("{} messages received.".format(len(self.ReceivedDataBuffer)))
                #print(self.ReceivedDataBuffer)

    def StartNetClient(self, EncryptedMesssageList):
        # Transmit Encrypted Messages to remote host
        Notify.Info("Starting Transmission")
        Notify.Info("Transmission Target: {}:{}".format(self.HOST, self.PORT))
        self.Client = NetHandler.Server(self.HOST, self.PORT, "TX")
        XmitDataArray = []
        for count in range(0,len(EncryptedMesssageList)):
            XmitDataArray.append(EncryptedMesssageList[count].EncryptedMessage)
        Notify.Info("{} Messages to transmit.".format(len(XmitDataArray)))

    ## Encryption and Decryption
    def LocateHashedAircraftID(self, TargetHash):
        Debug.Message("Target Hash: {}".format(TargetHash))
        for count in range(0,len(self.ACARSMessageList)):
            if hash(self.ACARSMessageList[count].ICAOAircraftID) == TargetHash:
                return True, self.ACARSMessageList[count]
        for count in range(0,len(self.CPDLCMessageList)):
            if hash(self.CPDLCMessageList[count].ICAOAircraftID) == TargetHash:
                return True, self.CPDLCMessageList[count]
        return False

    def LoadEncryptedMessages(self, MessageFile, KeyFile):
        print(json.loads(KeyFile))
        print(self.KeyArray)

    def EncryptMessages(self):
        ACARSEncryptedCount = 0
        CPDLCEncryptedCount = 0

        # Encrypt all ACARS objects
        for count in range(0,len(self.ACARSMessageList)):
            self.EncryptedObjectArray.append(self.CryptoHandler.EncryptMessageObject(self.ACARSMessageList[count]))
            ACARSEncryptedCount += 1

        #Encrypt all CPDLC objects
        for count in range(0,len(self.CPDLCMessageList)):
            self.EncryptedObjectArray.append(self.CryptoHandler.EncryptMessageObject(self.CPDLCMessageList[count]))
            CPDLCEncryptedCount += 1
        Notify.Info("{} Messages encrypted. ({} ACARS, {} CPDLC)".format((ACARSEncryptedCount + CPDLCEncryptedCount), ACARSEncryptedCount, CPDLCEncryptedCount))


    def DecryptMessages(self, MessageList, KeyArray):
        DecryptedMessages = []
        ## Debug Messages
        Debug.Message("DECRYPT: CTX_LIST_LEN: {}".format(len(MessageList)))
        Debug.Message("DECRYPT: KEY_ARR_LEN: {}".format(len(KeyArray)))

        # Iterate through the list of encrypted messages
        for MessageCounter in range(0,len(MessageList)):

            #Check every key against current message
            for KeyCounter in range(0,len(KeyArray)):
                # 0 = Wrong key 1 = Correct key
                result =  self.CryptoUtils.FernetDecrypt(MessageList[MessageCounter][0].EncryptedMessage, KeyArray[KeyCounter][0].encode())
                if result == 0:
                    pass
                else:
                    DecryptedMessages.append(result)
        print(DecryptedMessages[4])

    ## Message Transmssion

    def TransmitAllMessages(self):
        if Debug.DebugMode == True:
            Notify.Info("TransmitAllMessages(): Messages to Transmit: {}, Keys to write: {}, keyfile Name: {}".format(len(self.EncryptedObjectArray),
                                                                                                                      self.KeyArray, self.KeyFileName))
        self.WriteKeysToFile(self.EncryptedObjectArray)
        self.TransmitMessageList(self.EncryptedObjectArray)
        #Main function for transmission of messages, and writing keys to file
        #TODO Create/check for keyfile
        #TODO Append keys to file
        #TODO Timestamp for verification of keyfile
        #TODO Encode, and transmit messages to remote host
        #TODO Verify transmission?

    def TransmitMessageList(self, MessageList):
        # Function to transmit messages over socket object
        MessageBytes = []
        # Iterate through message list array and encode for transmission
        for count in range(0,len(MessageList)):
            #MessageBytes.append(self.CryptoUtils.ConvertDictToBytes(MessageList[count].RawMessage, 'utf-8'))
            MessageBytes.append(MessageList[count][0].EncryptedMessage)
        Debug.Message("TransmitMessageList(): {} messages encoded for transmission.".format(len(MessageList)))

        # create socket object and transmit through encoded message list
        try:
            SocketObject =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            SocketObject.connect((self.HOST, self.PORT))

            for count in range(0,len(MessageBytes)):
                Debug.Message(MessageBytes[count])
                SocketObject.sendall(MessageBytes[count])
                time.sleep(0.01)

        except(ConnectionRefusedError):
            Notify.Error("Connection Refused")
        except(ConnectionResetError):
            Notify.Error("Connection Reset")
        except(ConnectionAbortedError):
            Notify.Error("Connection Aborted")
        finally:
            SocketObject.close()

    def WriteKeysToFile(self, EncryptedMessageList):
        KeyFileArray = []
        # Iterate through list of encrypted messages
        for EncryptedMessage in EncryptedMessageList:
            Key = EncryptedMessage[1]
            MsgHash = EncryptedMessage[0].ICAOAircraftIDHash
            # Write key and ACID hash to array
            KeyFileArray.append([Key.decode(), MsgHash])
        with open('keyfile.csv', 'w+') as keyfile:
            csv.writer(keyfile, delimiter=',').writerows(KeyFileArray)


        file = open('keyfile.csv', 'r')
        content = file.read()
        #print(content)

    def LoadKeyFile(self, KeyFileName):
        Keys = []
        Notify.Info("Loading keys from file: {}".format(KeyFileName))
        try:
            with open(KeyFileName) as KeyFile:
                reader = csv.reader(KeyFile, delimiter=',')
                for row in reader:
                    if row == []:
                        pass
                    else:
                        Keys.append(row)
            Notify.Success("Loaded {} keys.".format(len(Keys)))
            #print(Keys)
            self.KeyArray = Keys
            #return Keys
        except(FileNotFoundError):
            Notify.Error("Cannot locate {}".format(KeyFileName))


class Controller:
    def __init__(self, MML):
        self.MainMenu()
        self.MessageProcessing = MessageProcessingMain(MML, self.ProgramMode)
        # Defines whether the program acts as a transmitter of encrypted messages
        # or a receiver of encrypted messages

    def MainMenu(self):
        print("""
        ******************************************
                    FYP Project - B018567J
        AVLC-Based Encryption Layer utilising Fernet
        ******************************************
        [1] TX + ENC
        [2] RX + DEC
        [3] Display Messages
        [4] Exit
        ******************************************
        """)
        while True:
            try:
                menuchoice = int(input("> "))
                if menuchoice not in [1,2,3]:
                    Notify.Error("Please enter a valid selection")
                else:
                    break
            except(ValueError):
                Notify.Error("Please enter a valid selection")
        if menuchoice == 1:
            self.ProgramMode = "TX"
        elif menuchoice == 2:
            self.ProgramMode = "RX"
        elif menuchoice == 3:
            self.ProgramMode = "PT"
        else:
            exit()

Test = MessageProcessingMain(['avlc_all.avlc'], "DB")



