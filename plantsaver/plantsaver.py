import os
import ADS1115
import gpiozero
from influxdb import InfluxDBClient
from balena import Balena

class PlantSaver:
    # moisture sensor config
    max_moisture = 1230
    min_moisture = 2600
    target_soil_moisture = 50 # this will be a balenaCloud config var
    target_soil_threshold = 10 # no action will be taken if current moisture is target +/- this value

    # define input/output pins
    pump_control_pin = 16
    float_switch_pin = 26

    # i2c device address definitions
    adc_i2c_address = 0x48
    led_matrix = 0x46
    led_matrix_type = 'sense-hat'

    # influx db details
    influx_db_name = 'plant-data'
    influx_db_host = 'influxdb'

    def __init__(self):
        self.ads = ADS1115.ADS1115(self.adc_i2c_address)
        self.pump = gpiozero.DigitalOutputDevice(self.pump_control_pin)
        self.float_switch = gpiozero.DigitalInputDevice(self.float_switch_pin)

        self.influx_client = InfluxDBClient(self.influx_db_host, 8086, database=self.influx_db_name)
        self.influx_client.create_database(self.influx_db_name)

        # set up an instance of the SDK - used for updating device tags
        self.balena = Balena()
        self.balena.auth.login_with_token(os.environ['BALENA_API_KEY'])

        # some instance status vars
        self.status = 'Starting'
        self.status_code = 0
        self.moisture_level = None
        self.pumping = False

    # Update the device tags with the moisture level and the status on balenaCloud
    # This means that you'll be able to see the status of the plant from the dashboard
    def update_device_tags(self):
        self.balena.models.tag.device.set(os.environ['BALENA_DEVICE_UUID'], 'Status', str(self.status))
        moisture_string = str(self.moisture_level)+'%'
        self.balena.models.tag.device.set(os.environ['BALENA_DEVICE_UUID'], 'Moisture', moisture_string)

    # Store the current instance measurements within InfluxDB
    def write_measurements(self):

        measurements = [
            {
                'measurement': 'plant-data',
                'fields': {
                    'moisture': float(self.moisture_level),
                    'pumping': int(self.pumping),
                    'water_left': int(self.water_left),
                    'status': int(self.status_code)
                }
            }
        ]

        self.influx_client.write_points(measurements)

    # Take a reading from the moisture sensor and the float switch and update the vars with the current status
    def update_sensors(self):
        self.read_moisture()
        self.read_float_switch()

    # Take a reading from the moisture sensor,
    # then convert this into a percentage based on the defined minimum and maximum
    def read_moisture(self):
        value = self.ads.readADCSingleEnded()
        range = self.min_moisture - self.max_moisture
        self.moisture_level = round((100 - (((value - self.max_moisture)/range)*100)),1)

    # Take a reading from the float switch and update the vars
    def read_float_switch(self):
        self.water_left = bool(self.float_switch.value)

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


        if self.pumping == True:
            status = status + ', pump running'

        if self.water_left == False:
            status = status + ', water low'

        self.status = status

    # Refresh the relevant things - designed to be run once every 10 seconds
    def tick(self):
        self.update_sensors()
        self.update_status()
        self.write_measurements()
