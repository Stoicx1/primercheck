
import snap7
import keyboard
import time

###########################################################
###	VARIABLES                                           ###
###########################################################
connected = False

###########################################################
### FUNCTIONS                                           ###
###########################################################

def printLocalTime():
	print(' ----------------------------------------')
	print("   Local time:", time.ctime(time.time()))
	print(' ----------------------------------------')

def tryReadDB(numDB, offsetDB, lengthData, name):
	global connected
	buffer = []
	try:
		if connected:
			buffer = client.db_read(numDB, offsetDB, lengthData)
			bufferLen = buffer[1]
			serialName = str(buffer, 'utf-8')[2:bufferLen+2]
			if len(serialName)>0:
				print(name+': '+serialName)
			else:
				print(name+': '+'N/A')
	except:
		connected = False
		print(Exception)


###########################################################
### MAIN                                                ###
###########################################################
client = snap7.client.Client()

while True:
	print()
	print('#####################################################################')
	print()

	if keyboard.is_pressed("ctrl"):
		break

	if connected == False:
		print('Connecting...')
		time.sleep(1)

		# Make connection to PLC
		try:
			client.disconnect()
			client.connect("192.168.11.100", 0, 1)
			if client.get_connected():
				connected = True
				print('Succesfully connected to: #', client)
		except:
			pass
		
		time.sleep(2)

	if connected == True:
		printLocalTime()
		tryReadDB(130,   0, 32, 'FA065     -> ')
		tryReadDB(130,  34, 32, 'FA066  FP -> ')
		tryReadDB(130,  68, 32, 'FA066  RP -> ')
		tryReadDB(130, 102, 32, 'FA066 SCL -> ')
		tryReadDB(130, 136, 32, 'FA066 SCR -> ')

	# Delay
	time.sleep(1)

