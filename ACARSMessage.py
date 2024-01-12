class Message:
    def __init__(self, Sec, USec, MsgFreq, SigLevel, NoiseLevel,
                 CRC, AircraftReg, ACARSMode, ACARSLabel, ACARSBlockID, ACARSAck, FlightNum, MessageNum,
                 MessageSeq, Sublabel, MessageText, RawMessage, ICAOAircraftID):
        # Timing Attributes
        self.Sec = Sec
        self.USec = USec
        self.MsgFreq = MsgFreq
        self.SigLevel = SigLevel
        self.NoiseLevel = NoiseLevel

        #AVLC Attributes
        self.ICAOAircraftID = ICAOAircraftID

        # ACARS Message Attributes
        self.CRC = CRC
        self.AircraftReg = AircraftReg
        self.ACARSMode = ACARSMode
        self.ACARSLabel = ACARSLabel
        self.ACARSBlockID = ACARSBlockID
        self.ACARSAck = ACARSAck
        self.FlightNum = FlightNum
        self.MessageNum = MessageNum
        self.MessageSeq = MessageSeq
        self.Sublabel = Sublabel
        self.MessageText = MessageText
        self.RawMessage = RawMessage

    def PrintMessage(self):
        print("""
************************************************************************
                               ACARS MESSAGE
************************************************************************
Message Metadata  /
------------------
Sec:            {}
uSec:           {}
Frequency:      {}
Signal Level:   {}
Noise Level:    {}
ICAO 24-bit ID: {}

************************************************************************
Message Data      /
------------------
CRC Check:      {}
Aircraft Reg:   {}
Mode:           {}
Label:          {}
Block ID:       {}
Ack Required:   {}
Flight Num:     {}
Message Num:    {}
Message Seq:    {}
Sublabel:       {}

************************************************************************
{}
************************************************************************
        """.format(self.Sec, self.USec, self.MsgFreq, self.SigLevel, self.NoiseLevel, self.ICAOAircraftID, self.CRC, self.AircraftReg, self.ACARSMode,
                   self.ACARSLabel, self.ACARSBlockID, self.ACARSAck, self.FlightNum, self.MessageNum, self.MessageSeq, self.Sublabel, self.MessageText))

    def GetMessageType(self):
        return "ACARS"