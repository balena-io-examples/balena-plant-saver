import time
from plantinha import PlantSaver

plantsaver = PlantSaver()

while True:
    plantsaver.tick()

    print("====================================================")
    print("Moisture: {:.1f}%".format(plantsaver.moisture_level))
    print("Temperature: {:.1f}C".format(plantsaver.temperature))
    print("Humidity: {:.1f}%".format(plantsaver.humidity))
    print("Status: "+plantsaver.status)

    # # update this every minute
    # if loop_count == 6:
    #     plantsaver.update_device_tags()
    #     loop_count = 0
    # else:
    #     loop_count = loop_count + 1

    time.sleep(10)