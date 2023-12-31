import serial
import time
import string
import binascii

import paho.mqtt.publish as publish

IV_SIZE = 12
AD_SIZE = 8
CT_SIZE = 32
TAG_SIZE = 16
BUFFER_SIZE = IV_SIZE + AD_SIZE + CT_SIZE + TAG_SIZE

ser = serial.Serial("/dev/rfcomm0", 9600)
print("waiting for incoming message")

while True:
	if ser.in_waiting >= BUFFER_SIZE: # We know incoming payload are 68-byte each, so we process when the full payload has arrived.
		s = ser.read_all() # read all bytes in the buffer
		
		print(f"{len(s)} bytes of encrypted data received from BT. ")

		if (len(s) == 68): # check payload length
			iv = s[0:IV_SIZE] # the 0th - 11th bytes resemble IV
			ad = s[IV_SIZE: IV_SIZE + AD_SIZE] # 12 - 19, Associated Data
			ct = s[IV_SIZE + AD_SIZE: IV_SIZE + AD_SIZE + CT_SIZE] # 20 - 51, Ciphertext
			tag = s[IV_SIZE + AD_SIZE + CT_SIZE:
				IV_SIZE + AD_SIZE + CT_SIZE + TAG_SIZE] # 52 - 67, tag

			# hexlify() transforms raw bytes into hex form which is easier for us to observe
			print("IV: ", binascii.hexlify(iv, " "))
			print("AD: ", binascii.hexlify(ad, " "))
			print("CT: ", binascii.hexlify(ct, " "))
			print("tag: ", binascii.hexlify(tag, " "))
			print("---")

			# Publish to MQTT broker
			publish.single("encrypted", s, hostname="54.198.230.159")
			print(f"{len(s)} bytes published to {hostname}. ")
		
