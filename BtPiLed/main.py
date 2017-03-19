from bluetooth import * 
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM) 

def pwm(pin, ratio):
	cmd = "echo " + str(pin) + "=" + str(ratio) + " > /dev/pi-blaster"
	os.system(cmd)

def setledcolor(red, green, blue):
	pwm(RED_LED_PIN, red)
	pwm(GREEN_LED_PIN, green)
	pwm(BLUE_LED_PIN, blue)

GREEN_LED_PIN = 17
RED_LED_PIN = 22
BLUE_LED_PIN = 4 

GPIO.setup(GREEN_LED_PIN, GPIO.OUT) 
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(BLUE_LED_PIN, GPIO.OUT)
 
server_socket=BluetoothSocket(RFCOMM) 

server_socket.bind(("",3)) 

server_socket.listen(1) 

port = server_socket.getsockname()[1] 
uuid = "ec1a5aa0-a500-11e3-a5e2-0800200c9a66" 
advertise_service( server_socket, "PiServer",
	service_id = uuid,
	service_classes = [uuid, SERIAL_PORT_CLASS],
	profiles = [ SERIAL_PORT_PROFILE ]) 

client_socket, adress = server_socket.accept() 

print ("Connection established with ",adress)  

try:
	while True:
		data = client_socket.recv(1024)
		if not data: break
		command = data.split('\n')
		if command[0] == "SetRGB":
			setledcolor(float(command[1]), float(command[2]), float(command[3]))
		print "received [%s]" % data
		client_socket.send(data) 
except IOError:
	pass 
print "Disconnected" 
client_socket.close() 
server_socket.close()
