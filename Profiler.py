# Script for assessing the performance of Fernet cryptography
from cryptography.fernet import Fernet
import cProfile
try:
    from CryptoHandler_2 import Main as CryptoMain
    from CryptoHandler_2 import Utils as Utils
except(ImportError):
    print("Cannot import Cryptohandler")
    exit()

try:
    from MessageUtilities.MessageAnalysis import JsonTools
except(ImportError):
    exit()


class Main():
    def __init__(self):
        self.Profiler = cProfile.Profile()
        self.ProfileObjects = []
        self.ExamplePlaintext = []
        self.ExampleCiphertext = []
        self.ExampleKeys = []
        self.CryptoHandler = CryptoMain()
        self.CryptoUtils = Utils()
        self.JsonTools = JsonTools()

        self.ExamplePlaintext.append(self.LoadMessages(['avlc_all.avlc']))
        self.EncryptMessages()
        self.DecryptMessages()


    def GetFernetObject(self):
        Key = Fernet.generate_key()
        return Fernet(Key), Key

    def LoadMessages(self, MessageFile):
        RawMessages = self.JsonTools.MultiLoad(MessageFile)
        print("{} Messages loaded".format(len(RawMessages)))
        return RawMessages

    def EncryptMessages(self):
        print("Beginning performance profiling")
        print("Encrypting {} Messages".format(len(self.ExamplePlaintext)))
        self.Profiler.enable()
        for count in range(0,len(self.ExamplePlaintext[0])):
            FernetCipher, Key = self.GetFernetObject()
            #print(self.ExamplePlaintext[count])
            Bytestring = str(self.ExamplePlaintext[0][count]).encode('utf-8')
            self.ExampleCiphertext.append(FernetCipher.encrypt(Bytestring))
            self.ExampleKeys.append(Key)
        self.Profiler.disable()
        self.Profiler.print_stats()

    def DecryptMessages(self):
        SuccessCounter = 0
        print("Beginning performance profiling")
        print("Decrypting {} messages".format(len(self.ExampleCiphertext)))
        self.Profiler.enable()
        for x in range(0,len(self.ExampleCiphertext)):
            for y in range(0,len(self.ExampleKeys)):
                Plaintext = self.CryptoUtils.FernetDecrypt(self.ExampleCiphertext[x], self.ExampleKeys[y])
                #print("ATTEMPT: CTX:{}, K:{}".format(x, y))
                if Plaintext == 0:
                    pass
                else:
                    #print("hit")
                    SuccessCounter += 1
        self.Profiler.disable()
        self.Profiler.print_stats()
        print("Successful decryptions: {}".format(SuccessCounter))


test = Main()

