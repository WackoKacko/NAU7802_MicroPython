from machine import SoftI2C as I2C, Pin

import nau7802py


i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
myScale = nau7802py.NAU7802(i2c) # Create instance of the NAU7802 class


print('Qwiic Scale Example')

if not myScale.begin():
    print('Scale not detected. Please check wiring. Freezing...')
    while True:
        pass
  
print('Scale detected!')

myScale.setLDO(nau7802py.NAU7802_LDO_Values['NAU7802_LDO_3V0']) #AVDD (output) can be set to 2.4V, 2.7V, 3.0V, 3.3V, 3.6V, 3.9V, 4.2V, or 4.5V. Digital voltae supply (input) to LDO must be at least 0.3V greater than selected AVDD!

myScale.setGain(nau7802py.NAU7802_Gain_Values['NAU7802_GAIN_128']) # Gain can be set to 1, 2, 4, 8, 16, 32, 64, or 128.

myScale.setSampleRate(nau7802py.NAU7802_SPS_Values['NAU7802_SPS_10']) # Sample rate can be set to 10, 20, 40, 80, or 320Hz

myScale.calibrateAFE() # Does an internal calibration. Recommended after power up, gain changes, sample rate changes, or channel changes.


while True:
    if myScale.available():
        currentReading = myScale.getReading();
        print('Reading: ', currentReading)
