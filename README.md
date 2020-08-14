# Balena Plant Saver

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/img01.jpg?raw=true)

This is a Raspberry Pi balenaCloud starter project to help you water your precious plants. See temperature, humidity, and soil moisture levels. Set watering thresholds and timings to automate the watering of your plants.

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/img03.png?raw=true)

Access your plant's dashboard from anywhere in the world using balenaCloud. Add new plant monitors quickly and easily using the same application code on different devices. Use your imagination (and some extra parts) and turn balenaPlant into a balenaGarden. :)

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/01-all-parts.jpg)

## Hardware you'll need
This project uses the Pimironi Automation pHAT to make things a bit more user-friendly. Here's the list of materials:

* Raspberry Pi ZeroWH/3B/4 (that's what we've tested so far)
* A 32GB+ SD car
* Pimironi Automation pHAT
* DHT22 temperature and humidity sensor
* Capacitive soil moisture sensor
* Float switch
* 5V peristaltic pump (with water tube-- some vendors don't include the tubing-- *remember the tubing!!!*)

## Software you'll need
Here's the software that you'll need to get going:

* a free [balenaCloud](https://dashboard.balena-cloud.com/signup) account (first ten devices are fully featured and free)
* [balenaEtcher](https://www.balena.io/etcher/) to burn OS images to SD cards
* (optional) [balenaCLI](https://www.balena.io/docs/reference/balena-cli/) if you want to hack on this project, push code locally, etc.

![](/img/01b-plant-water.jpg)

Oh yeah... you'll want a plant to test with. We recommend something resilient that you can over or underwater as you test. A bamboo works great. And the most important part: *water*.

---

## Set up the hardware

### Connect the Automation pHAT to the Raspberry Pi

After preparing the Automation pHAT (soldering terminals on, etc.), connect it to the Raspberry Pi via GPIO pins.

### Solder on DHT22 sensor

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/02-dht22.jpg)

Connect the power and ground to the 3.3V pins. Connect the data pin to the `SCLK` pin, which is GPIO pin 11 (you'll see this referenced in the plant watering code).

### Add capacitive moisture sensor

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/03-soil-moisture-sensor.jpg)

As seen on this [balenaForum post](https://forums.balena.io/t/building-a-smart-houseplant-monitor-and-waterer/9170/21), it's helpful to paint or coat the exposed electronic components of this sensor with outdoor paint or nail polish. Power the soil moisture sensor using the 5V terminals on the Automation pHAT, and insert the data wire into the `ADC 1` terminal (since the sensor is giving us an analog signal to convert).

### Add the float switch

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/04-float-switch.jpg)

Power the float switch using the 5V terminal and connect the other wire into the `INPUT 1` terminal.

### Add the water pump

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/05-pump-relay.jpg)

Power the peristaltic pump using the 5V terminal on the Automation pHAT. Connect the pump's ground wire to the `NO` (Normally Open) terminal.

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/06-pump-replay-close.jpg)

Close the circuit for the water pump by using a wire to connect the `COM` terminal to `GND`.

### Set everything up

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/07-test-setup.jpg)

At this point, you can set your plant watering test up. Add the moisture sensor to the plant's soil (or lack thereof in the case of this bamboo). Add the pumping end of the water pump into your water source and the dousing end into the plant's soil. NOTE: It's not clear on some pumps as to which port does what-- once you test, mark or tape a line to help tell which is which.

#### Build or 3D print additional accessories

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/img02.jpg?raw=true)

The original project creators built 3D-printed parts to hold various parts or to enclose the electronics for the project. Check out this [forum thread](https://forums.balena.io/t/building-a-smart-houseplant-monitor-and-waterer/9170/21) to learn more.

---

## Add and deploy the application

### Deploy with balena

Once you're logged into your balenaCloud account (remember: first ten devices are free and fully-featured), click the button below to automagically deploy the project to your account.

[![Deploy with balena](https://camo.githubusercontent.com/610358f5d0de9bfe856b58d4e22dcc64db6383cc/68747470733a2f2f62616c656e612e696f2f6465706c6f792e706e67)](https://dashboard.balena-cloud.com/deploy)

![](https://www.balena.io/blog/content/images/2020/07/deploy-default.png)

Name your application, select your device type, and click `Create and deploy`. You'll be taken to your dashboard and our builders will start creating your application in the background.

![](https://www.balena.io/blog/content/images/2020/06/build-indicator.png)

### Add a device

![](https://www.balena.io/blog/content/images/2020/06/os-download.png)

Once that step is complete, add a new device by clicking `Add device` and selecting your device type. If you plan on using Wi-Fi, add your credentials here. Otherwise, proceed with an Ethernet cable connected to your internet setup. Complete the modal and your OS will download.

### Flash the OS onto your SD card

![](https://www.balena.io/blog/content/images/2020/07/etcher-1.png)

Insert the SD card into your computer, boot up Etcher and flash the downloaded balenaOS to your card. Insert the card into your device and wait for it to power on and show up on your dashboard within your app. Once the device downloads all the software, the application should be ready to use.

---

## Using balenaPlant

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/device-url.jpg)

Now it's time to put everything to the test. Access your device within the application. You'll see its details including tags that show moisture levels and whether or not the water level is high or low. You'll also see a local or public URL option for the device. Use either of these to access the Grafana dashboard for the sensors.

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/grafana-dash.jpg)

Clicking on either URL takes you to the Grafana dashboard for the setup. From here you can see a timeseries graph of temperature and humidity, water level, and recorded pump activity. For advanced Grafana users, feel free to experiment with adding alerts for each chart (we won't cover that in this readme though).

### Automated watering

By default, balenaPlant checks the water level of the plant approximately every 15 minutes. This is a reasonable time for a few reasons:

* running the pump infrequently prevents the motor from burning out
* watering with long intervals between each session allows soil or growing material to absorb water for a more accurate reading

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/device-var.jpg)

You can change the pump delay time by changing the `Device variable` (located on the left-side menu in balenaCloud). Set `pump_delay` to a higher number for a longer wait time and a lower one for a shorter wait between watering. If properly set, you'll never overwater because even if the elapsed delay goes by, the pump won't start if the moisure level is too high.

Other device variables to change include:

| Device variable       | Definition                                 | Default value |
|-----------------------|--------------------------------------------|---------------|
| target_soil_moisture  | Sets target moisture percentage            | 60            |
| target_soil_threshold | Sets threshold of moisture past target     | 15            |
| pump_delay            | Adds time between how often pump code runs | 15            |

### Experiment and explore

![](https://github.com/balena-io-playground/balena-plant-saver/blob/master/img/08-basil-test.jpg)

Once you test a few things here and there, try other kinds of plants, adjust the soil moisture targets, and take one chore off your to-do list.

Check out this [livestream build](https://www.youtube.com/watch?v=r0ZR6COwdRo) (uses the balenaCLI method) or [visit our Forums](https://forums.balena.io/t/building-a-smart-houseplant-monitor-and-waterer/9170/21) for more information.