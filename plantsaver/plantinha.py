import time
import os
import automationhat
import Adafruit_DHT
from influxdb import InfluxDBClient
from balena import Balena

class PlantSaver:

    # influx db details
    influx_db_name = 'plant-data'
    influx_db_host = 'influxdb'

    def __init__(self):

        # Variables
        self.dht_sensor             = Adafruit_DHT.DHT22
        self.dht_pin                = int(self.set_variable("dht_pin", 11))
        self.max_value              = float(self.set_variable("max_value", 2.77)) 
        self.min_value              = float(self.set_variable("min_value", 1.46)) 
        self.target_soil_moisture   = int(self.set_variable("target_soil_moisture", 60))
        self.target_soil_threshold  = int(self.set_variable("target_soil_threshold", 15))
        self.pump_delay             = int(self.set_variable("pump_delay", 30))

        # Initial status
        self.status         = 'Starting'
        self.status_code    = 0
        # self.turbidity_level= None
        self.moisture_level = None
        self.pumping        = False
        self.temperature    = 0
        self.humidity       = 0

        # TO-DO only create the database if it doesn't already exist
        self.influx_client = InfluxDBClient(self.influx_db_host, 8086, database=self.influx_db_name)
        self.influx_client.create_database(self.influx_db_name)

        # set up an instance of the SDK - used for updating device tags
        self.balena = Balena()
        self.balena.auth.login_with_token(os.environ['BALENA_API_KEY'])

    # Checks if there is an environment variable set, otherwise save the default value
    def set_variable(self, name, default_value):
        if name in os.environ:
            self.value = os.environ.get(name)
        else: 
            self.value = default_value
        return self.value

    #def read_turbidity(self):
    #    self.turbidity_level= (automationhat.analog.two.read()*5.0/1024.0)

    def read_moisture(self):
        self.moisture_level= 100-(automationhat.analog.one.read()-self.min_value)/((self.max_value-self.min_value)/100)

    def read_temperature_humidity(self):
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.dht_sensor, self.dht_pin)
    
    def update_sensors(self):
    #    self.read_turbidity()
        self.read_moisture()
        self.read_temperature_humidity()
        self.read_float_switch()

    # Take a reading from the float switch and update the vars
    def read_float_switch(self):
        self.water_left = not bool(automationhat.input.one.read())

    # Update the device tags with the moisture level and the status on balenaCloud
    # This means that you'll be able to see the status of the plant from the dashboard
    def update_device_tags(self):
        self.balena.models.tag.device.set(os.environ['BALENA_DEVICE_UUID'], 'Status', str(self.status))
        moisture_string = str(round(self.moisture_level,2))+'%'
        self.balena.models.tag.device.set(os.environ['BALENA_DEVICE_UUID'], 'Moisture', moisture_string)

    # Store the current instance measurements within InfluxDB
    def write_measurements(self):
        measurements = [
            {
                'measurement': 'plant-data',
                'fields': {
        #            'turbidity': float(self.turbidity_level),
                    'moisture': float(self.moisture_level),
                    'pumping': int(self.pumping),
                    'water_left': int(self.water_left),
                    'status': int(self.status_code),
                    'temperature': float(self.temperature),
                    'humidity': float(self.humidity)
                }
            }
        ]

        self.influx_client.write_points(measurements)

    # Generate a status string so we have something to show in the logs
    # We also generate a status code which is used in the front end UI
    def update_status(self):
        if self.moisture_level < self.target_soil_moisture-self.target_soil_threshold:
            status = 'Too dry'
            self.status_code = 1
        elif self.moisture_level > self.target_soil_moisture+self.target_soil_threshold:
            status = 'Too wet'
            self.status_code = 2
        else:
            status = 'OK'
            self.status_code = 3

        if self.pumping:
            status = status + ', pump on'
        else: 
            status = status + ', pump off'

        if not self.water_left:
            status = status + ', water low'
        else:
            status = status + ', water normal'

        self.status = status

    # Pump water
    def pump_water(self, action):
        if action == True:
            automationhat.relay.one.on()
            self.pumping = True
        else:
            automationhat.relay.one.off()
            self.pumping = False

    # Refresh the relevant things - designed to be run once every 10 seconds
    def tick(self):
        self.update_sensors()
        self.update_status()
        self.write_measurements()
