import socket
import time
try:
    from util import Notify as NotifyMain
except("Failed to import Notify."):
    exit()
Notify = NotifyMain.Main()
Notify.SetMode("C")
Debug = NotifyMain.Debug()

class Server:
    def __init__(self, Host, Port, Type):
        self.Host = Host
        self.Port = Port
        self.Socket = ""
        self.Connection = ""
        self.ClientAddr = ""
        self.Data = []

    def Receive(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.Socket:
            self.Socket.bind((self.Host, self.Port))
            self.Socket.listen()
            self.Connection, self.ClientAddr = self.Socket.accept()
            with self.Connection:
                print("Client Connect @ {}".format(self.ClientAddr))
                while True:
                    try:
                        RxData = self.Connection.recv(8196)
                        if not RxData:
                            break
                        self.Socket.close()
                        self.Data.append(RxData)
                    except(ConnectionResetError):
                        self.Data.append(RxData)
                        break
                    #break
    def Transmit(self, MessageList):
        for count in range(0,len(MessageList)):
            if type(MessageList[count]) == bytes:
                pass
            else:
                return 1
        try:
            self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.Socket.connect((self.Host, self.Port))
            for message in MessageList:
                self.Socket.sendall(message)
                Debug.Message("Sent: {}".format(len(message)))
                time.sleep(0.01)
        except(ConnectionRefusedError):
            Notify.Error("Connection Refused")
        except(ConnectionResetError):
            Notify.Error("Connection Reset")
        except(ConnectionAbortedError):
            Notify.Error("Connection Aborted")
        finally:
            self.Socket.close()

    def GetReceivedData(self):
        #print(self.Data)
        return self.Data


class TestServer:
    def __init__(self):
        self.Host = "127.0.0.1"
        self.Port = 15995
        self.Connection = ""
        self.ClientAddr = ""
        self.Data = []

    def Serve(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.Host, self.Port))
            s.listen()
            self.Connection, self.ClientAddr = s.accept()
            with self.Connection:
                print("Client Connect @ {}".format(self.ClientAddr))
                while True:
                    data = self.Connection.recv(8192)
                    if not data:
                        break
                    s.close()
                    self.Data.append(data)



class TestClient:
    def __init__(self):
        self.ExampleMessage = b''
        self.Host = "127.0.0.1"
        self.Port = 15995

    def ClientConnect(self, msgList):
        counter = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.Host, self.Port))
            for msg in msgList:
                s.sendall(msg)
                counter +=1
                print(counter)
            #s.sendall(msg)
            #data = s.recv(1024)
        #print("Rec: {}".format(data))

