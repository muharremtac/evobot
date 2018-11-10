from bluepy import btle
dev = btle.Peripheral("Your EvoBot MAC Address eg 03:04:05:06:07:A0")
remoteService = btle.UUID("0000fff3-0000-1000-8000-00805f9b34fb")
remoteCharacteristic = dev.getServiceByUUID(remoteService)
uuidConfig = btle.UUID("0000fff5-0000-1000-8000-00805f9b34fb")
remoteServiceConfig = remoteCharacteristic.getCharacteristics(uuidConfig)[0]

def forward():  
    for x in range(20):
      remoteServiceConfig.write(bytes(b'\x58\x02'), True)

def backward():  
    for x in range(20):
      remoteServiceConfig.write(bytes(b'\x58\x06'), True)

def left():
    for x in range(50):
      remoteServiceConfig.write(bytes(b'\x58\x0A'), True)

def rigth():	  
    for x in range(50):
      remoteServiceConfig.write(bytes(b'\x58\x0E'), True)

def dance():	  
    remoteServiceConfig.write(bytes(b'\x58\x42'), True)

def stop():	  
    remoteServiceConfig.write(bytes(b'\x58\x11\x40\x40\x00\x00'), True)
	
import paho.mqtt.client as mqttClient
import time
 
Connected = False #global variable for the state of the connection
 
broker_address= "your mqtt address"
port = 1883 # or your port

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")
		

def on_message(client, userdata, message):
    message_payload = str(message.payload.decode("utf-8"))
    print ("Message received: "  + message_payload)
    if message_payload == 'f':
       forward()
    elif message_payload == 'b':  
       backward()
    elif message_payload == 'l':  
       left()
    elif message_payload == 'r':  
       rigth()
    elif message_payload == 'd':  
       dance()   

client = mqttClient.Client("evobot")
client.on_connect=on_connect
client.on_message=on_message     

client.connect(broker_address, port=port)
client.loop_start()

while Connected != True:
    time.sleep(0.1)
 
client.subscribe("your topic")
 
try:
    while True:
      time.sleep(1)
 
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()	
    dev.disconnect()	
