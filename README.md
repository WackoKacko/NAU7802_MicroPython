# NAU7802_MicroPython
### MicroPython library for the NAU7802 chip using the I2C interface. 

Hey, guys. Like you, I needed a MicroPython library for the NAU7802. I found the [CircuitPython library](https://github.com/adafruit/CircuitPython_NAU7802), and porting that to MicroPython proved a headache, but I was able to take the [plain Python library](https://github.com/longapalooza/nau7802py) for it and make some very slight modifications so it uses MicroPython's native _machine.I2C_.

_Definitely_ not thoroughly tested, but it seems to be working for what I use it for.

I've been developing in Pymakr on VSCode, which is why the contents of this repo are what they are. It's pretty neat, I recommend it, despite its 2-star rating on the VSCode extensions page. Here's a nice tutorial on how to use it: [link](https://www.youtube.com/watch?v=YOeV14SESls).

You may be delighted to hear that there is a Python translation of the CompleteScale example from Sparkfun ([link](https://github.com/sparkfun/SparkFun_Qwiic_Scale_NAU7802_Arduino_Library/blob/master/examples/Example2_CompleteScale/Example2_CompleteScale.ino)) which runs splendidly with this library. You'll find it [here](https://github.com/longapalooza/nau7802py/blob/master/Example2_CompleteScale.py), in the original NAU7802 Python library repo.

Hope I helped someone.

_“ Ka-chow! ”_
_-Lightning McQueen_
