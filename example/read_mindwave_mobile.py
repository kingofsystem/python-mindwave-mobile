# -*- coding: utf-8 -*-
import time
import bluetooth
from mindwavemobile.MindwaveDataPoints import RawDataPoint, AttentionDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
import textwrap

if __name__ == '__main__':
    #Я не понял, что делает последний аргумент
    mindwaveDataPointReader = MindwaveDataPointReader('<Аддрес майндвэйва>', '<Аддрес адаптера>', 0) #Последняя - любая цыферка вроде
    mindwaveDataPointReader.start()
    if (mindwaveDataPointReader.isConnected()):
        while(True):
            dataPoint = mindwaveDataPointReader.readNextDataPoint()
            if (not dataPoint.__class__ is AttentionDataPoint):
                print dataPoint
    else:
        print(textwrap.dedent("""\
            Exiting because the program could not connect
            to the Mindwave Mobile device.""").replace("\n", " "))
        
