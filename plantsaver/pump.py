import time
from plantinha import PlantSaver

plantsaver = PlantSaver()

print("Turning ON")
plantsaver.pump_water(True)
time.sleep(10)
print("Turning OFF")
plantsaver.pump_water(False)
time.sleep(10)