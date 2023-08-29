# NAU7802_MicroPython
### MicroPython library for the NAU7802 chip

Hey, guys. Like you, I needed a MicroPython library for the NAU7802. I found the CircuitPython library (link), and porting that to MicroPython proved a headache, but I was able to take the plain Python library (link) for it and make some very slight modifications so it uses MicroPython's native _machine.I2C_.

_Definitely_ not thoroughly tested, but it seems to be working ok for what I need it for.

I've been developing in Pymakr on VSCode, which is why the contents of this repo are what they are. It's pretty neat, I recommend it, despite its 2 star rating on the VSCode extensions page. Here's a nice tutorial on how to use it: link.

You may be delighted to hear that there is a Python translation of the CompleteScale example from Sparkfun (link) which runs splendidly with this library. You'll find it here, in the original NAU7802 Python library repo.

Hope I helped someone.

_“ Ka-chow! ”_
_-Lightning McQueen_