#!/usr/bin/env python
#
# marvelmind.py - small class for recieve and parse coordinates from Marvelmind mobile beacon by USB/serial port
#  Overhauled by Erin fierce, originally from  Alexander Rudykh 
#
### Attributes:
#
#   tty - serial port device name (physical or USB/virtual). It should be provided as an argument: 
#       /dev/ttyACM0 - typical for Linux / Raspberry Pi
#       /dev/tty.usbmodem1451 - typical for Mac OS X
#
#   baud - baudrate. Should be match to baudrate of hedgehog-beacon
#       default: 9600
#
#   maxvaluescount - maximum count of measurements of coordinates stored in buffer
#       default: 3
#
#   valuesUltrasoundPosition - buffer of measurements
#
#   debug - debug flag which activate console output    
#       default: False
#
#   pause - pause flag. If True, class would not read serial data
#
#   terminationRequired - If True, thread would exit from main loop and stop
#
#
### Methods:kjckdckdbckbdkcbkdcb
#
#   __init__ (self, tty="/dev/ttyACM0", baud=9600, maxvaluescount=3, debug=False) 
#       constructor
#
#   print_position(self)
#       print last measured data in default format
#
#   position(self)
#       return last measured data in array [x, y, z, timestamp]
#
#   stop(self)
#       stop infinite loop and close port
#
### Needed libraries:
#
# To prevent errors when installing crcmod module used in this script, use the following sequence of commands:
#   sudo apt-get install python-pip
#   sudo apt-get update
#   sudo apt-get install python-dev
#   sudo pip install crcmod
#
###

###
# Changes:
# lastValues -> valuesUltrasoundPosition
# recieveLinearDataCallback -> recieveUltrasoundPositionCallback
# lastImuValues -> valuesImuRawData
# recieveAccelerometerDataCallback -> recieveImuRawDataCallback
# mm and cm -> m
###

import crcmod
import serial
import struct
import collections
import time
from threading import Thread
import math

# import numpy as np
# import marvelmindQuaternion as mq

class MarvelmindHedge (Thread):
    def __init__ (self, adr, tty="/dev/ttyACM0", baud=9600, maxvaluescount=3, debug=False, recieveUltrasoundPositionCallback=None, recieveImuRawDataCallback=None, recieveImuDataCallback=None, recieveUltrasoundRawDataCallback=None):
        self.tty = tty  # serial
        self.baud = baud  # baudrate
        self.debug = debug  # debug flag
        self._bufferSerialDeque = collections.deque(maxlen=255)  # serial buffer

        self.valuesUltrasoundPosition = collections.deque([[0]*5]*maxvaluescount, maxlen=maxvaluescount) # ultrasound position buffer
        self.recieveUltrasoundPositionCallback = recieveUltrasoundPositionCallback
        
        self.valuesImuRawData = collections.deque([[0]*10]*maxvaluescount, maxlen=maxvaluescount) # raw imu data buffer
        self.recieveImuRawDataCallback = recieveImuRawDataCallback

        self.valuesImuData = collections.deque([[0]*14]*maxvaluescount, maxlen=maxvaluescount) # processed imu data buffer
        self.recieveImuDataCallback = recieveImuDataCallback

        self.valuesUltrasoundRawData = collections.deque([[0]*5]*maxvaluescount, maxlen=maxvaluescount)
        self.recieveUltrasoundRawDataCallback = recieveUltrasoundRawDataCallback


        self.pause = False
        self.terminationRequired = False
        
        self.adr = adr
        self.serialPort = None
        Thread.__init__(self)

    def print_position(self):
        if (isinstance(self.position()[1], int)):
            print ("Hedge {:d}: X: {:d} m, Y: {:d} m, Z: {:d} m at time T: {:.2f}".format(self.position()[0], self.position()[1], self.position()[2], self.position()[3], self.position()[4]/1000.0))
        else:
            print ("Hedge {:d}: X: {:.2f}, Y: {:.2f}, Z: {:.2f} at time T: {:.2f}".format(self.position()[0], self.position()[1], self.position()[2], self.position()[3], self.position()[4]/1000.0))

    def position(self):
        return list(self.valuesUltrasoundPosition)[-1];
    

    #here is a function i made to get the raw data from the marvelmind mobil beacon and 
    #calculate some useful values wwith them. especially the bearing. in order to do this i read 
    # over the data sheet linked below where it said the interfacting values needed so i could trace
    #it back to the correct source. with this the 
    # * on the mobile beacon the internal raw data flag must be enabled for it to be able to give those
    def orientation(self):

        #since the gyro getts angular velocity the time is needed to cancel out seconds and give 
        #just the angle 
        #calculates the loop period or the time between gyro reads
        b = datetime.datetime.now() - a
        a = datetime.datetime.now()
        LP = b.microseconds/(1000000*1.0)
        M_PI = 3.141592653589
        #might need to calibrate the values in the accel, gyro, and compass
        # Sensitivities as per interfaces data sheet: accel: 1mg/LSB, Gyro: 0.0175dps/LSB
        # compass: 1100LSB/Gauss. 
        # data sheet https://www.marvelmind.com/pics/marvelmind_beacon_interfaces_v2017_11_15.pdf


        #normaliing the accelerometer raw values
        acx = self.valuesImuRawData.ax
        acy = self.valuesImuRawData.ay
        acz = self.valuesImuRawData.az

        ax_norm = acx/math.sqrt(acx*acx + acy*acy + acz*acz)
        ay_norm = acy/math.sqrt(acx*acx + acy*acy + acz*acz)

        pitch = math.asin(ax_norm)
        roll = -math.asin(ay_norm/math.cos(pitch))
        
        #sensitivity of the gyro
        g_sens = 0.0175
        #this should return the gyro data in degrees / second
        gyro_x = self.valuesImuRawData.gx *g_sens
        gyro_y = self.valuesImuRawData.gy * g_sens
        gyro_z = self.valuesImuRawData.gz * g_sens

        #multiplying by the frequency of gyro samples will keave it as an angle
        gyro_ang_x += gyro_x *LP
        gyro_ang_y += gyro_y * LP
        gyro_ang_z += gyro_z * LP

        mag_sens = 1100
        mag_x = self.valuesImuRawData.mx / mag_sens
        mag_y = self.valuesImuRawData.my / mag_sens
        mag_z = self.valuesImuRawData.mz / mag_sens

       
            #adjusted for tilt
        mag_x_adj = mag_x*math.cos(pitch)+mag_z*math.sin(pitch)
        mag_y_adj = mag_x*math.sin(roll)*math.sin(pitch)+mag_y*math.cos(roll)-mag_z*math.sin(roll)*math.cos(pitch)

         #didnt end up using this yet
        bearing = 180* math.atan2(mag_y_adj,mag_x_adj)/M_PI
        if bearing < 0:
            bearing += 360
        return  = list(pitch, roll, gyro_ang_x, gyro_ang_y, gyro_ang_z, bearing)[-1]

        #gets the roll in degrees from the raw data values
        #roll = math.degrees(atan2(self.valuesImuRawData.ax,self.valuesImuRawData.az))
        #same thing but with the pitch
        #pitch = math.degrees(atan2(self.valuesImuRawData.ay,self.valuesImuRawData.az))

        #the compass is needed for the yaw but the calibration on that was difficult and it should 
        #an accurate enough heading for our purposes

        
        return list(self.valuesImuRawData)[-1];

    def calibrate_compass(self):
        #the compass was veyr complicated to calibrate but i left this here to leave it if theres time
        # also the yaw needs this but it should be accurate enough for muesume use.

    def stop(self):
        self.terminationRequired = True
        print ("stopping")

    def run(self):      
        while (not self.terminationRequired):
            if (not self.pause):
                try:
                    if (self.serialPort is None):
                        self.serialPort = serial.Serial(self.tty, self.baud, timeout=3)
                    readChar = self.serialPort.read(1)
                    while (readChar is not None) and (readChar is not '') and (not self.terminationRequired):
                        self._bufferSerialDeque.append(readChar)
                        readChar = self.serialPort.read(1)
                        bufferList = list(self._bufferSerialDeque)
                        
                        strbuf = (b''.join(bufferList))

                        pktHdrOffset = strbuf.find(b'\xff\x47')
                        if (pktHdrOffset >= 0 and len(bufferList) > pktHdrOffset + 4 and pktHdrOffset<220):
#                           print(bufferList)
                            isMmMessageDetected = False
                            isCmMessageDetected = False
                            isRawImuMessageDetected = False
                            isImuMessageDetected = False
                            isDistancesMessageDetected = False
                            pktHdrOffsetCm = strbuf.find(b'\xff\x47\x01\x00')
                            pktHdrOffsetMm = strbuf.find(b'\xff\x47\x11\x00')
                            pktHdrOffsetRawImu = strbuf.find(b'\xff\x47\x03\x00')
                            pktHdrOffsetDistances = strbuf.find(b'\xff\x47\x04\x00')
                            pktHdrOffsetImu = strbuf.find(b'\xff\x47\x05\x00')

                            if (pktHdrOffsetMm!=-1):
                                isMmMessageDetected = True
                                if (self.debug): print ('Message with US-position(mm) was detected')
                            elif (pktHdrOffsetCm!=-1):
                                isCmMessageDetected = True
                                if (self.debug): print ('Message with US-position(cm) was detected')
                            elif (pktHdrOffsetRawImu!=-1):
                                isRawImuMessageDetected = True
                                if (self.debug): print ('Message with raw IMU data was detected')
                            elif (pktHdrOffsetDistances!=-1):
                                isDistancesMessageDetected = True
                                if (self.debug): print ('Message with distances was detected')
                            elif (pktHdrOffsetImu!=-1):
                                isImuMessageDetected = True
                                if (self.debug): print ('Message with processed IMU data was detected')
                            msgLen = ord(bufferList[pktHdrOffset + 4])
                            if (self.debug): print ('Message length: ', msgLen)

                            try:
                                if (len(bufferList) > pktHdrOffset + 4 + msgLen + 2):
                                    usnCRC16 = 0
                                    if (isCmMessageDetected):
                                        usnTimestamp, usnX, usnY, usnZ, usnAdr, usnCRC16 = struct.unpack_from ('<LhhhxBxxxxH', strbuf, pktHdrOffset + 5)
                                        usnX = usnX/100.0
                                        usnY = usnY/100.0
                                        usnZ = usnZ/100.0
                                    elif (isMmMessageDetected):
                                        usnTimestamp, usnX, usnY, usnZ, usnAdr, usnCRC16 = struct.unpack_from ('<LlllxBxxxxH', strbuf, pktHdrOffset + 5)
                                        usnX = usnX/1000.0
                                        usnY = usnY/1000.0
                                        usnZ = usnZ/1000.0
                                        #these values are raw and need to be calibrated witht their sensetivities
                                    elif (isRawImuMessageDetected):
                                        ax, ay, az, gx, gy, gz, mx, my, mz, timestamp, usnCRC16 = struct.unpack_from ('<hhhhhhhhhxxxxxxLxxxxH', strbuf, pktHdrOffset + 5)
                                    elif (isImuMessageDetected):
                                        x, y, z, qw, qx, qy, qz, vx, vy, vz, ax, ay, az, timestamp, usnCRC16 = struct.unpack_from ('<lllhhhhhhhhhhxxLxxxxH', strbuf, pktHdrOffset + 5)

                                    crc16 = crcmod.predefined.Crc('modbus')
                                    crc16.update(strbuf[ pktHdrOffset : pktHdrOffset + msgLen + 5 ])
                                    CRC_calc = int(crc16.hexdigest(), 16)

                                    if CRC_calc == usnCRC16:
                                        if (isMmMessageDetected or isCmMessageDetected):
                                            value = [usnAdr, usnX, usnY, usnZ, usnTimestamp]
                                            self.valuesUltrasoundPosition.append(value)
                                            if (self.recieveUltrasoundPositionCallback is not None):
                                                self.recieveUltrasoundPositionCallback()
                                        elif (isRawImuMessageDetected):
                                            value = [ax, ay, az, gx, gy, gz, mx, my, mz, timestamp]
                                            self.valuesImuRawData.append(value)
                                            if (self.recieveImuRawDataCallback is not None):
                                                self.recieveImuRawDataCallback()
                                        # elif (isDistancesMessageDetected):
                                        #     value = 
                                        #     self.valuesUltrasoundRawData.append(value)
                                        #     if (self.recieveUltrasoundRawDataCallback is not None):
                                        #         self.recieveUltrasoundRawDataCallback()
                                        elif (isImuMessageDetected): #call number 0x0003
                                            value = [x/1000.0, y/1000.0, z/1000.0, qw/10000.0, qx/10000.0, qy/10000.0, qz/10000.0, vx/1000.0, vy/1000.0, vz/1000.0, ax/1000.0,ay/1000.0,az/1000.0, timestamp]
                                            self.valuesImuData.append(value)
                                            if (self.recieveImuDataCallback is not None):
                                                self.recieveImuDataCallback()
                                    else:
                                        if self.debug:
                                            print ('\n*** CRC ERROR')

                                    if pktHdrOffset == -1:
                                        if self.debug:
                                            print ('\n*** ERROR: Marvelmind USNAV beacon packet header not found (check modem board or radio link)')
                                        continue
                                    elif pktHdrOffset >= 0:
                                        if self.debug:
                                            print ('\n>> Found USNAV beacon packet header at offset %d' % pktHdrOffset)
                                    for x in range(0, pktHdrOffset + msgLen + 7):
                                        self._bufferSerialDeque.popleft()
                            except struct.error:
                                print ('smth wrong')
                except OSError:
                    if self.debug:
                        print ('\n*** ERROR: OS error (possibly serial port is not available)')
                    time.sleep(1)
                except serial.SerialException:
                    if self.debug:
                        print ('\n*** ERROR: serial port error (possibly beacon is reset, powered down or in sleep mode). Restarting reading process...')
                    self.serialPort = None
                    time.sleep(1)
            else: 
                time.sleep(1)
    
        if (self.serialPort is not None):
            self.serialPort.close()