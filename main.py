import nau7802py, time

myScale = nau7802py.NAU7802() # Create instance of the NAU7802 class

#
# Begin void setup() equivalent
#

print('Qwiic Scale Example')

if not myScale.begin():
    print('Scale not detected. Please check wiring. Freezing...')
    while True:
        pass
  
print('Scale detected!')

myScale.setLDO(nau7802py.NAU7802_LDO_Values['NAU7802_LDO_4V5']) #AVDD can be set to 2.4V, 2.7V, 3.0V, 3.3V, 3.6V, 3.9V, 4.2V, or 4.5V. Voltae supply to LDO must be at least 0.3V greater than selected AVDD!

myScale.setGain(nau7802py.NAU7802_Gain_Values['NAU7802_GAIN_2']) # Gain can be set to 1, 2, 4, 8, 16, 32, 64, or 128.

myScale.setSampleRate(nau7802py.NAU7802_SPS_Values['NAU7802_SPS_40']) # Sample rate can be set to 10, 20, 40, 80, or 320Hz

myScale.calibrateAFE() # Does an internal calibration. Recommended after power up, gain changes, sample rate changes, or channel changes.

#
# Begin void loop() equivalent
#

while True:
    if myScale.available():
        currentReading = myScale.getReading();
        print('Reading: ', currentReading)
        time.sleep(0.1)



# Here's some blinkLED code if you need a Pymakr sanity check.
# import machine #you can ignore the yellow underline here
# import time

# def toggle_led(t):
#     led_pin.value(not led_pin.value())

# led_pin = machine.Pin(2, machine.Pin.OUT)
# led_timer = machine.Timer(1)
# led_timer.init(mode=machine.Timer.PERIODIC, period=1000, callback=toggle_led)


# while True:
#     led_pin.value(1)
#     print("ON...")
#     time.sleep(1)
#     led_pin.value(0)
#     print("OFF...")
#     time.sleep(1)