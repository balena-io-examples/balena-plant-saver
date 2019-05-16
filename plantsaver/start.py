import ADS1115
import gpiozero
import time
from influxdb import InfluxDBClient

ads = ADS1115.ADS1115()
pump = gpiozero.DigitalOutputDevice(16)
water_left = gpiozero.DigitalInputDevice(26)

influx_client = InfluxDBClient('influxdb', 8086, database='plant-data')
influx_client.create_database('plant-data')


def get_moisture():
    max_moisture = 1230
    min_moisture = 2600

    value = ads.readADCSingleEnded()
    range = min_moisture - max_moisture
    return round((100 - (((value - max_moisture)/range)*100)),1)

while True:
    moisture = get_moisture()

    print("{:.1f}% moisture content".format(moisture))

    # if(moisture > 2100 and water_left.value == True):
    #     pump.on()
    # else:
    #     pump.off()

    measurements = [
        {
            'measurement': 'plant-data',
            'fields': {
                'moisture': float(moisture)
            }
        }
    ]

    influx_client.write_points(measurements)
    time.sleep(10)
