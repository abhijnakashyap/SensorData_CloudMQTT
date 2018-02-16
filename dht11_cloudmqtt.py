import RPi.GPIO as GPIO
import time, sys
import paho.mqtt.client as mqtt
import json
import dht11
import datetime

# the sensor has to be connected to pin 1 for power, pin 6 for ground
# and pin 7 for signal(board numbering!).
 
key = 'Add you key here'

temp = 0
humd = 0
gas = 0
distance = 0

def action(pin):
    print('Sensor detected action!')
    return

client = mqtt.Client()

client.username_pw_set("your username", "your password")
client.connect('m14.cloudmqtt.com',19600,60)
client.loop_start()
client.subscribe("sensordata",0)


try:
	while True:
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		instance = dht11.DHT11(pin=4)
		GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.add_event_detect(18, GPIO.RISING)
		GPIO.add_event_callback(18, action)
		TRIG = 23
		ECHO = 24
		print "Distance Measurement In Progress"
		GPIO.setup(TRIG,GPIO.OUT)
		GPIO.setup(ECHO,GPIO.IN)
		GPIO.output(TRIG, False)
		print "Waiting For Sensor To Settle"
		time.sleep(1)
		GPIO.output(TRIG, True)
		time.sleep(0.000001)
		GPIO.output(TRIG, False)
		while GPIO.input(ECHO)==0:
			pulse_start = time.time()
		while GPIO.input(ECHO)==1:
			pulse_end = time.time()     
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 2)
		distance = str(distance)
		print "Distance:",distance,"cm"
		sensor_data = {'proximity': distance}	
		result = instance.read()
    		if result.is_valid():
        		print("Last valid input: " + str(datetime.datetime.now()))
        		print("Temperature: %d C" % result.temperature)
        		print("Humidity: %d %%" % result.humidity)
			temp = str(result.temperature)
			humd = str(result.humidity)
		MQTT_TOPIC = "sensordata"
                MQTT_MSG = json.dumps({"Temp": temp,"Humd": humd,"Distance": distance});
		client.publish(MQTT_TOPIC, MQTT_MSG)
		GPIO.cleanup()
		time.sleep(10)
		
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()


 



        	
		
	
		

       

