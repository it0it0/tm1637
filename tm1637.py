# based on https://raspberrytips.nl/tm1637-4-digit-led-display-raspberry-pi/
#reworked for micropython

import sys
import os
import time
import machine

HexDigits = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71]

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_TYPICAL = 2
BRIGHT_HIGHEST = 7
OUTPUT = machine.Pin.OUT
INPUT = machine.Pin.IN
LOW = 0 #IO.LOW
HIGH = 1 #IO.HIGH

class TM1637:
	__doublePoint = False
	__Clkpin = 0
	__Datapin = 0
	__brightnes = BRIGHT_TYPICAL;
	__currentData = [0,0,0,0];


	def __init__( self, pinClock, pinData, brightnes ):
		self.__Clkpin = pinClock
		self.__Datapin = pinData
		self.__brightnes = brightnes;
		self.__pclk=machine.Pin(self.__Clkpin,machine.Pin.OUT)    
		self.__pdat=machine.Pin(self.__Datapin,machine.Pin.OUT) #IO.setup(self.__Datapin,OUTPUT)
	# end  __init__

	def Clear(self):
		b = self.__brightnes;
		point = self.__doublePoint;
		self.__brightnes = 0;
		self.__doublePoint = False;
		data = [0x7F,0x7F,0x7F,0x7F];
		self.Show(data);
		self.__brightnes = b;				# restore saved brightnes
		self.__doublePoint = point;
	# end  Clear

	def ShowInt(self, i):
		s = str(i)
		self.Clear()
		for i in range(0,len(s)):
			self.Show(i, int(s[i]))

	def Show( self, data ):
		for i in range(0,4):
			self.__currentData[i] = data[i];

		self.start();
		self.writeByte(ADDR_AUTO);
		self.stop();
		self.start();
		self.writeByte(STARTADDR);
		for i in range(0,4):
			self.writeByte(self.coding(data[i]));
		self.stop();
		self.start();
		self.writeByte(0x88 + self.__brightnes);
		self.stop();
	# end  Show

	def SetBrightnes(self, brightnes):		# brightnes 0...7
		if( brightnes > 7 ):
			brightnes = 7;
		elif( brightnes < 0 ):
			brightnes = 0;

		if( self.__brightnes != brightnes):
			self.__brightnes = brightnes;
			self.Show(self.__currentData);
		# end if
	# end  SetBrightnes

	def ShowDoublepoint(self, on):			# shows or hides the doublepoint
		if( self.__doublePoint != on):
			self.__doublePoint = on;
			self.Show(self.__currentData);
		# end if
	# end  ShowDoublepoint

	def writeByte( self, data ):
		for i in range(0,8):
			#IO.output( self.__Clkpin, LOW)
			self.__pclk.value(LOW)
			if(data & 0x01):
				self.__pdat.value(HIGH)
				#IO.output( self.__Datapin, HIGH)
			else:
				#IO.output( self.__Datapin, LOW)
				self.__pdat.value(LOW)
			data = data >> 1
			#IO.output( self.__Clkpin, HIGH)
			self.__pclk.value(HIGH)
		#endfor

		# wait for ACK
		self.__pclk.value(LOW)
		self.__pdat.value(HIGH)
		self.__pclk.value(HIGH)
		self.__pdat=machine.Pin(self.__Datapin,machine.Pin.IN)

		while(self.__pdat.value()):
			time.sleep(0.001)
			if( self.__pdat.value()):
				self.__pdat=machine.Pin(self.__Datapin,machine.Pin.OUT)
				self.__pdat.value(LOW)
				self.__pdat=machine.Pin(self.__Datapin,machine.Pin.IN)
		self.__pdat=machine.Pin(self.__Datapin,machine.Pin.OUT)
	# end writeByte

	def start(self):    # send start signal to TM1637
		self.__pclk.value(HIGH)
		self.__pdat.value(HIGH)
		self.__pdat.value(LOW)
		self.__pclk.value(LOW)

	# end start

	def stop(self):
		self.__pclk.value(LOW)
		self.__pdat.value(LOW)
		self.__pclk.value(HIGH)
		self.__pdat.value(HIGH)   
	# end stop

	def coding(self, data):
		if( self.__doublePoint ):
			pointData = 0x80
		else:
			pointData = 0;

		if(data == 0x7F):
			data = 0
		else:
			data = HexDigits[data] + pointData;
		return data
	# end coding

# end class TM1637





