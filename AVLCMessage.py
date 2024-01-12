class ACARSMessage:
    def __init__(self, Sec, USec, MsgFreq, SigLevel, NoiseLevel,
                 CRC, AircraftReg, ACARSMode, ACARSLabel, ACARSBlockID, ACARSAck, FlightNum, MessageNum,
                 MessageSeq, Sublabel, MessageText, RawMessage):
        # Timing Attributes
        self.Sec = Sec
        self.USec = USec
        self.MsgFreq = MsgFreq
        self.SigLevel = SigLevel
        self.NoiseLevel = NoiseLevel

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

class CPDLCMessage:
    def __init__(self, USec, Sec, MsgFreq, SigLevel, NoiseLevel, MsgID, MsgRef, TxYear, TxMonth,
                 TxDay, TxHour, TxMin, TxSec, LogicalAckReq, MsgData, CPDLCMessageIdentifier, RawMessage):
        self.USec = USec
        self.Sec = Sec
        self.MsgFreq = MsgFreq
        self.SigLevel = SigLevel
        self.NoiseLevel = NoiseLevel
        self.MsgID = MsgID
        self.MsgRef = MsgRef
        self.TxYear = TxYear
        self.TxMonth = TxMonth
        self.TxDay = TxDay
        self.TxHour = TxHour
        self.TxMin = TxMin
        self.TxSec = TxSec
        self.LogicalAckReq = LogicalAckReq
        self.MsgData = MsgData
        self.CPDLCMessageIdentifier = CPDLCMessageIdentifier

        self.RawMessage = RawMessage

class OtherMessage:
    def __init__(self, USec, Sec, MsgFreq, SigLevel, NoiseLevel, RawMessage):
        self.USec = USec
        self.Sec = Sec
        self.MsgFreq = MsgFreq
        self.SigLevel = SigLevel
        self.NoiseLevel = NoiseLevel

        self.RawMessage = RawMessage

