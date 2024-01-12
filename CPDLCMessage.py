class Message:
    def __init__(self, USec, Sec, MsgFreq, SigLevel, NoiseLevel, MsgID, MsgRef, TxYear, TxMonth,
                 TxDay, TxHour, TxMin, TxSec, LogicalAckReq, MsgData, CPDLCMessageIdentifier, RawMessage, ICAOAircraftID):
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

        #AVLC Attributes
        self.ICAOAircraftID = ICAOAircraftID

        self.RawMessage = RawMessage

    def PrintMessage(self):
        print("""
    ************************************************************************
                                   CPDLC MESSAGE
    ************************************************************************
    Message Metadata  /
    ------------------
    Sec:            {}
    uSec:           {}
    Frequency:      {}
    Signal Level:   {}
    Noise Level:    {}
    MessageID:      {}
    ICAO 24-bit ID: {}

    ************************************************************************
    Message Data      /
    ------------------
    Message ID:     {}
    Message Ref:    {}
    Tx Date:        {}/{}/{}, {}:{}:{}
    LogAck Req:     {}


    ************************************************************************
    {}
    ************************************************************************        
            """.format(self.Sec, self.USec, self.MsgFreq, self.SigLevel, self.NoiseLevel, self.ICAOAircraftID, self.CPDLCMessageIdentifier,
                       self.MsgID, self.MsgRef, self.TxDay, self.TxMonth, self.TxYear, self.TxHour, self.TxMin,
                       self.TxSec,
                       self.LogicalAckReq, self.MsgData))

    def GetMessageType(self):
        return "CPDLC"