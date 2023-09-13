import paho.mqtt.client as mqtt
import serial 
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY_SIZE = 16
IV_SIZE = 12
AD_SIZE = 8
CT_SIZE = 32
PT_SIZE = 32
TAG_SIZE = 16
BUFFER_SIZE = 68

AES_KEY = bytes([0x00] * KEY_SIZE)

 
def on_connect(client, userdata, flags, rc): # func for making connection
	print(f"Connected to MQTT Server {ADD} at port {PORT}")
	print("Connection returned result: " + str(rc) )
	topic = "encrypted"
	client.subscribe(topic)
	print(f"Subscribed to topic: {topic}")

def on_message(client, userdata, msg): # Func for Sending msg
	print("received message!")
	s = msg.payload
	print(msg.topic+" "+str(s))
	
	iv = s[0:IV_SIZE] # 0 - 11
	ad = s[IV_SIZE: IV_SIZE + AD_SIZE] # 12 - 19
	ct = s[IV_SIZE + AD_SIZE: IV_SIZE + AD_SIZE + CT_SIZE] # 20 - 51
	tag = s[IV_SIZE + AD_SIZE + CT_SIZE: IV_SIZE + AD_SIZE + CT_SIZE + TAG_SIZE] # 52 - 67
			
	aesgcm = AESGCM(AES_KEY)
	msg = aesgcm.decrypt(iv, ct+tag, ad)
	print("Decrypted message: ", msg.rstrip(b"\x00"))
		

ADD = "54.198.230.159"
PORT = 1883
	
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(ADD, PORT, 60)
client.loop_forever()