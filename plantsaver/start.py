import time
from plantinha import PlantSaver


plantsaver = PlantSaver()
loop_count = 6 # update the tags on first iteration
pump = False
pump_count = 1
pump_on_count = 0

while True:
    plantsaver.tick()
    print("====================================================")
    print("Moisture {:.1f}%".format(plantsaver.moisture_level))
    print("Temperature: {:.1f}C".format(plantsaver.temperature))
    print("Humidity: {:.1f}%".format(plantsaver.humidity))
    print("Status: "+plantsaver.status)
    print("Water level: "+str(plantsaver.water_left))
    print("Pump Cont: "+str(pump_count))
    print("Status code:"+plantsaver.status)

    # Check if water level is too dry and that the pump wasn't on for the past 15 minutes
    if plantsaver.status_code == 1 and pump_count >= plantsaver.pump_delay * 6:
        print("Turning pump ON for 10 seconds.")
        plantsaver.pump_water(True)
        pump_count = 0
    else:
        if pump_on_count < 2:
            pump_on_count = pump_on_count + 1
        else:
            pump_on_count = 0
            plantsaver.pump_water(False)
            pump_count = pump_count + 1

    # Update device tags every minute
    if loop_count == 6:
        plantsaver.update_device_tags()
        loop_count = 0
    else:
        loop_count = loop_count + 1

    time.sleep(10)
