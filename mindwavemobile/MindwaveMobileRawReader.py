import bluetooth
import time
import textwrap


class MindwaveMobileRawReader:
    START_OF_PACKET_BYTE = 0xaa;
    def __init__(self, address=None, btAddres=None, btNum=None):
        self._buffer = [];
        self._bufferPosition = 0;
        self._isConnected = False;
        self._mindwaveMobileAddress = address
        self._btAddres = btAddres
        self._btNum = btNum
        
    def connectToMindWaveMobile(self):
        # First discover mindwave mobile address, then connect.
        # Headset address of my headset was'9C:B7:0D:72:CD:02';
        # not sure if it really can be different?
        # now discovering address because of https://github.com/robintibor/python-mindwave-mobile/issues/4
        if (self._mindwaveMobileAddress is not None):            
            print ("Discovered Mindwave Mobile...")
            self._connectToAddress(self._mindwaveMobileAddress)
        else:
            self._printErrorDiscoveryMessage()
        
    def _findMindwaveMobileAddress(self):
        nearby_devices = bluetooth.discover_devices(lookup_names = True)
        for address, name in nearby_devices:
            if (name == "MindWave Mobile"):
                return address
        return None
        
    def _connectToAddress(self, mindwaveMobileAddress):
        self.mindwaveMobileSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        #Если ты указал адресс в конструкторе, то мы подключаемся через адаптер, который нада!
        if self._btAddres not == None and self._btNum not == None:
            self.mindwaveMobileSocket.bind((self._btAddres, self._btNum,)) #Внутри кортеж!!!

        while (not self._isConnected):
            try:
                self.mindwaveMobileSocket.connect(
                    (mindwaveMobileAddress, 1))
                self._isConnected = True
            except bluetooth.btcommon.BluetoothError as error:
                print "Could not connect: ", error, "; Retrying in 5s..."
                time.sleep(5) 
           

    def isConnected(self):
        return self._isConnected

    def _printErrorDiscoveryMessage(self):
         print(textwrap.dedent("""\
                    Could not discover Mindwave Mobile. Please make sure the
                    Mindwave Mobile device is in pairing mode and your computer
                    has bluetooth enabled.""").replace("\n", " "))

    def _readMoreBytesIntoBuffer(self, amountOfBytes):
        newBytes = self._readBytesFromMindwaveMobile(amountOfBytes)
        self._buffer += newBytes
    
    def _readBytesFromMindwaveMobile(self, amountOfBytes):
        missingBytes = amountOfBytes
        receivedBytes = ""
        # Sometimes the socket will not send all the requested bytes
        # on the first request, therefore a loop is necessary...
        while(missingBytes > 0):
            receivedBytes += self.mindwaveMobileSocket.recv(missingBytes)
            missingBytes = amountOfBytes - len(receivedBytes)
        return receivedBytes;

    def peekByte(self):
        self._ensureMoreBytesCanBeRead();
        return ord(self._buffer[self._bufferPosition])

    def getByte(self):
        self._ensureMoreBytesCanBeRead(100);
        return self._getNextByte();
    
    def  _ensureMoreBytesCanBeRead(self, amountOfBytes):
        if (self._bufferSize() <= self._bufferPosition + amountOfBytes):
            self._readMoreBytesIntoBuffer(amountOfBytes)
    
    def _getNextByte(self):
        nextByte = ord(self._buffer[self._bufferPosition]);
        self._bufferPosition += 1;
        return nextByte;

    def getBytes(self, amountOfBytes):
        self._ensureMoreBytesCanBeRead(amountOfBytes);
        return self._getNextBytes(amountOfBytes);
    
    def _getNextBytes(self, amountOfBytes):
        nextBytes = map(ord, self._buffer[self._bufferPosition: self._bufferPosition + amountOfBytes])
        self._bufferPosition += amountOfBytes
        return nextBytes
    
    def clearAlreadyReadBuffer(self):
        self._buffer = self._buffer[self._bufferPosition : ]
        self._bufferPosition = 0;
    
    def _bufferSize(self):
        return len(self._buffer);
    
#------------------------------------------------------------------------------ 
