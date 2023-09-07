import ujson, time, nau7802py, sys

from machine import Pin

myScale = nau7802py.NAU7802() # Create instance of the NAU7802 class

# Gives user the ability to set a known weight on the scale and calculate a calibration factor
def calibrateScale():
    print("Scale calibration")
    while True:
        # hak1=input("", end="")
        # hak2=input("", end="")
        print("Setup scale with no weight on it. Press a key when ready.")
        _ = sys.stdin.readline()
        if _ not in ["", "\n", "\r"]:
            ascii_values = [ord(char) for char in _]
            print(f"Received input: {ascii_values}")
            if _:
                print("Ok, this will take just a few seconds...")
                break
    myScale.calculateZeroOffset(64) # Zero or Tare the scale. Average over 64 readings.
    print("New zero offset: " + str(round(myScale.getZeroOffset())))
    print("Place known weight on scale. Please ensure the weight is in place and stable.")
    while True:
        # hak1=input("", end="")
        # hak2=input("", end="")
        print("Please enter the weight, without units, currently sitting on the scale (for example, '4.25'): ", end = "")
        _ = sys.stdin.readline()
        if _ not in ["", "\n", "\r"]:
            ascii_values = [ord(char) for char in _]
            print(f"Received input: {ascii_values}")
            try:
                weightOnScale = float(_)
                print("Ok, this will take another few seconds...")
                break
            except ValueError:
                print("Invalid input. Try again.")
    myScale.calculateCalibrationFactor(float(weightOnScale), 64)    # Tell the library how much weight is currently on it
    print("New cal factor: " + str(round(myScale.getCalibrationFactor(), 2)))
    print("New Scale Reading: " +  str(round(myScale.getWeight(), 2)))
    recordSystemSettings()    # Commit these values to file

# Record the current system settings to NVM
def recordSystemSettings(filename='calibrationSettings.json'):
    # Get various values from the library and commit them to NVM
    settings = {'calibrationFactor': myScale.getCalibrationFactor(),
                'zeroOffset': myScale.getZeroOffset()}
                
    with open(filename, 'w') as fh:
        fh.write(ujson.dumps(settings))

# Reads the current system settings from NVM
def readSystemSettings(filename='calibrationSettings.json'):
    try:
        with open(filename, 'r') as fh:
            settings = ujson.loads(fh.read())
    except OSError:  # (FileNotFoundError, basically) File doesn't exist; you must perform calibration.
        print("CALIBRATION FILE NOT FOUND")
        return False # If readSystemSettings is False, you calibrate.

    # Pass these values to the library
    myScale.setCalibrationFactor(settings['calibrationFactor'])
    myScale.setZeroOffset(settings['zeroOffset'])
    return True

# Setup
if not myScale.begin(): #might have to correct this...
    if not myScale.begin():
        print('Scale not detected. Please check wiring. Freezing...')
        while True:
            pass
print("Scale detected!")
myScale.setLDO(nau7802py.NAU7802_LDO_Values['NAU7802_LDO_3V0']) #AVDD can be set to 2.4V, 2.7V, 3.0V, 3.3V, 3.6V, 3.9V, 4.2V, or 4.5V. Voltae supply to LDO must be at least 0.3V greater than selected AVDD!
myScale.setGain(nau7802py.NAU7802_Gain_Values['NAU7802_GAIN_128']) # Gain can be set to 1, 2, 4, 8, 16, 32, 64, or 128.
myScale.setSampleRate(nau7802py.NAU7802_SPS_Values['NAU7802_SPS_10']) # Sample rate can be set to 10, 20, 40, 80, or 320Hz
myScale.calibrateAFE() # Does an internal calibration. Recommended after power up, gain changes, sample rate changes, or channel changes.

system_check = readSystemSettings()
print("readSystemSettings returned: ", system_check)
sys.stdin.readline() #flush input buffer? need to do because reading user input is buggy
if system_check is False: # Check if scale calibrated
    calibrateScale()

# Function to run when the pin goes high
def button_pressed(button_pin):
    if button_pin.value() == 1:  # Button is initially pressed
        time.sleep_ms(20)  # Debounce time of 20ms
        if button_pin.value() == 1:  # Confirm button is still pressed after debounce
            start_time = time.ticks_ms()  # Record the time when the button was first pressed
            calibrate = False
            
            while button_pin.value() == 1:  # Keep checking as long as the button is pressed
                current_time = time.ticks_ms()
                elapsed_time = time.ticks_diff(current_time, start_time)
                
                if elapsed_time >= 1500:  # If button has been pressed for 1.5s or more
                    calibrate = True
                    break  # Break the while loop, as we've detected a long press
                
            # Button has been released or 1s has elapsed
            time.sleep_ms(20)  # Debounce time of 20ms
            if button_pin.value() == 0 or calibrate:  # Button is released or calibration flag is set
                if not calibrate:  # If button was pressed for less than 1s, tare the scale
                    print("Taring. This will take just a few seconds...")
                    myScale.calculateZeroOffset(64)  # Zero or Tare the scale. Average over 64 readings.
                    print("Tare complete. New zero offset: " + str(round(myScale.getZeroOffset())))
                else:  # If button was pressed for 1s or more, calibrate the scale
                    calibrateScale()
                    print("Calibration complete.")

# Initialize pin 15 as an input pin
button_pin = Pin(15, Pin.IN, Pin.PULL_UP)
button_pin.irq(trigger=Pin.IRQ_RISING, handler=button_pressed)

# Main loop (without non-blocking reading implemented. For whatever reason, this is not a feature in MicroPython: https://forum.micropython.org/viewtopic.php?t=7325)
while True:
    if myScale.available():
        currentReading = myScale.getReading()
        currentWeight = myScale.getWeight()
        
        print("Reading: " + str(round(currentReading)) + "\t", end='') # specifying "end=''" omits "\n" at the end
        print("Weight: " + str(round(currentWeight, 2)))    # Print 2 decimal places



#
# Simple LED and button code as a sanity test
#
# from machine import Pin
# import utime

# last_time = utime.ticks_ms()
# interval = 500  # 500 milliseconds

# button_pin = Pin(15, Pin.IN, Pin.PULL_UP)
# led_pin = Pin(2, Pin.OUT) #change 2 to correspond to your board's built-in LED. I used the ESP32 WROOM.

# while True:
#     # current_time = utime.ticks_ms()
#     # if utime.ticks_diff(current_time, last_time) >= interval:
#     #     print("Value: ", button_pin.value())
#     #     last_time = current_time

#     if button_pin.value() == 1:
#         led_pin.value(1)
#     else:
#         led_pin.value(0)
