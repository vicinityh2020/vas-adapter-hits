# Getting started - HITS use case

This doc will guide you through the setup of HITS use case 1.

## Devices and Gateways Configurations

Please follow all of the instructions given in this chapter in their chronological order.

### PNI
You Login to your PNI control panel [here](https://parking.pnicloud.com)

##### 1. Set up the Gateway (GW)

The gateway is preconfigured, and needs only to be plugged into the power source 
and the router via the ethernet cable. 

To make sure that the gateway is connected: 
1. Log in to your [PNI control panel](https://parking.pnicloud.com)
2. Click **Network** in the menu
3. Verify that the gateway was last seen 30 seconds ago or less.

**P.S**. The `Unknown` status is considered "OK" as stated by the PNI tech support.

##### 2. Set up the parking sensor(s)
The parking sensors are preconfigured, and must be placed in the vicinity of the RF 
signal to the gateway.

##### 3. Re-enabling sensors after GW & device relocation

After relocating the sensor, you have to recalibrate it. 

**IMPORTANT:** Make sure that the sensor is left alone during the recalibration
period. It should not have any cars entering or leaving during the period. 
Do not attempt to "re-recalibrate" the sensor if its status says *Recalibrating*. 
Let it do its work.

**IMPORTANT 2:** Calibration may take up to 24 hours for it to recalibrate itself 
if the connection with the GW was lost for a longer period of time. 
The normal time for calibration is 5-10 minutes if the sensors were connected to the 
gateway throughout all the time.

1. In the [PNI control panel](https://parking.pnicloud.com), 
click **Sensors** in the upper menu
2. Click **Recalibrate** next to the sensor you wish to recalibrate 

You should see a status change to indicate the ongoing calibration. 
The status will revert back to `Vacant` upon completion.

### IKEA light

The IKEA light bundle consists of 3 components
1. Remote controller
2. Gateway
3. Light bulb

##### 1. Set up the Gateway & light bulb

1. Connect both the gateway and the light bulb to a power source.
2. Connect the gateway to your router via the ethernet cable.
3. Turn on the light bulb via the remote controller (press on the middle button)

The light needs to be on in order for us to control it. 
If the remote controller cannot turn on the light, check that the physical switch 
on the light bulb is actually on as well. 

Install the IKEA light app on your Android/iOS phone. Make sure the light bulb and the
phone are on the same network. Upon launching the app, it will try to detect your gateway.
If it did, you have set up everything correctly.

##### 2. Installing the OpenHAB

1. Download the [openHAB 2 Distribution](https://www.openhab.org/download/)
2. Start the openHAB by `cd`ing into its folder and running the `./start.sh` or the
batch file if you are on Windows.
3. Complete the [First-time setup](https://www.openhab.org/docs/tutorial/1sttimesetup.html)

##### 3. Registering the light bulb
Use Paper UI to configure your bulbs:

1. Install Tradfri binding

2. Use the binding to locate your ikea gateway.

3. Use the newly installed gateway to discover the bulbs (appear as items)

4. Create 'links' for each available property of the bulb.

5. At this point you should be able to modify the colour of the bulbs using the UI. 
You might need to add the properties into the dashboard, if they do not appear automatically.



## Step 1 - Running the devices' VICINITY Node

Configure and run all of the mentioned components below as described
in their respective readme files. <br> 
Run them in the following order:

1. [PNI adapter](https://github.com/vicinityh2020/vicinity-adapter-hits)
2. [Light bulb adapter](https://github.com/vicinityh2020/openhab-adapter-ikealight)
3. [VICINITY gateway](https://github.com/vicinityh2020/vicinity-gateway-api)
4. (Last to be run) [VICINITY agent](https://github.com/vicinityh2020/vicinity-agent)

## Step 2 - Enabling the devices in the VICINITY Cloud

Login to the [VICINITY Cloud](https://vicinity.bavenir.eu)

If you've run the STEP 1 successfully, you should be able to see your new sensor devices listed in `Devices`. Your personal devices are marked with a turquoise "My Device" label.
Your personal devices should include 
* 3 parking sensors (names starting with 008...)
* IKEA light 1

1. Click on "more info" in order to open the device page
2. Click **Enable device**. This will make it exposed to the P2P network
3. Click **Edit** under "Access Level"
4. Change from **Private** to **Public with Data Under Request** 
5. Hit **Save**

## Step 3 - Running the VAS VICINITY Node

Configure and run all of the mentioned components below as described
in their respective readme files. <br> 
Run them in the following order:

1. [VAS Adapter](https://github.com/vicinityh2020/vas-adapter-hits)
2. [VICINITY gateway](https://github.com/vicinityh2020/vicinity-gateway-api)
3. [Celery worker](https://github.com/vicinityh2020/vas-adapter-hits#celery-worker)
4. (Last to be run) [VICINITY agent](https://github.com/vicinityh2020/vicinity-agent)

## Step 4 - Enabling the service in the VICINITY Cloud

Like the devices, the service must also be enabled in the vicinity cloud.

1. Click **Services** in the left-side menu
2. If you have run the VAS VICINITY Node, your service should be visible here
3. Click **More info** under `HITS - VAS Adapter` service box
4. Click **Enable service**. This will make it exposed to the P2P network
5. Click **Edit** under "Access Level"
6. Change from **Private** to **Public with Data Under Request** 
7. Hit **Save**

Congratulations, your devices are now permitted to be accessed by other services (including your own service) through VAS adapter from other VICINITY nodes.