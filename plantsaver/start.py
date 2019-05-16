import time
from plantsaver import PlantSaver

plantsaver = PlantSaver()
loop_count = 6 # update the tags on first iteration

while True:
    plantsaver.tick()

    print("Moisture: {:.1f}%".format(plantsaver.moisture_level))
    print("Status: "+plantsaver.status)

    # update this every minute
    if loop_count == 6:
        plantsaver.update_device_tags()
        loop_count = 0
    else:
        loop_count = loop_count + 1

    time.sleep(10)
