import time
import os
import adafruit_dht
from balena import Balena
import json
import paho.mqtt.client as mqtt

# Choose the library to use (either 'automationhat' or 'growhat')
SENSOR_LIBRARY = 'automationhat'  # Change this based on your preference

if SENSOR_LIBRARY == 'automationhat':
    import automationhat as sensor_lib
elif SENSOR_LIBRARY == 'growhat':
    import growhat as sensor_lib
else:
    raise ValueError(f"Invalid sensor library: {SENSOR_LIBRARY}")

class PlantSaver:

    def __init__(self):

        self.client                 = mqtt.Client("1")

        # Variables
        self.dht_sensor             = adafruit_dht.DHT22
        self.dht_pin                = int(self.set_variable("dht_pin", 11))
        self.max_value              = float(self.set_variable("max_value", 2.77)) 
        self.min_value              = float(self.set_variable("min_value", 1.46)) 
        self.target_soil_moisture   = int(self.set_variable("target_soil_moisture", 60))
        self.target_soil_threshold  = int(self.set_variable("target_soil_threshold", 15))
        self.pump_delay             = int(self.set_variable("pump_delay", 15))

        # Initial status
        self.status         = 'Starting'
        self.status_code    = 0
        self.moisture_level = None
        self.pumping        = False
        self.temperature    = 0
        self.humidity       = 0

        # set up an instance of the SDK - used for updating device tags
        self.balena = Balena()
        self.balena.auth.login_with_token(os.environ['BALENA_API_KEY'])

        # Initialize the selected sensor library
        sensor_lib.init()

    # ... (rest of the code remains unchanged)

    def read_moisture(self):
        self.moisture_level = sensor_lib.moisture()

    def read_temperature_humidity(self):
        self.humidity, self.temperature = adafruit_dht.read_retry(self.dht_sensor, self.dht_pin)
    
    def read_float_switch(self):
        # Update this part based on the specific requirements for the float switch with the selected library
        pass

    def pump_water(self, action):
        # Update this part based on the specific requirements for the pump with the selected library
        pass

    def tick(self):
        self.update_sensors()
        self.update_status()
        self.write_measurements()
