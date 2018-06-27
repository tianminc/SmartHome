## Overview
This is my personal project to connect a few "not-so-smart" devices to Amazon Alexa.
So far this project involes three devices: a LG C7 TV, a pair of Edifier S2000Pro speakers
and an [Eclipse floor lamp](https://www.amazon.com/gp/product/B01KKZRF5C). The communication
hub between Alexa and these devices (a.k.a. where most of the code in this project runs) is
a Raspberry Pi Zero W running Raspbian. I also have a PC connected to the TV and speakers.

## Code Used and Dependencies
* [fauxmo](https://github.com/makermusings/fauxmo) for emulating Belkin WeMo devices with Alexa
* [LIRC](http://www.lirc.org/) for recording IR remote and sending emualted IR remote signals.

## Components
* Raspberry Pi Zero W. Heart of the project. It is connected to two hardware devices: an IR
  LED for sending IR signals to TV and speaker, and a relay to control Eclipse lamp. It runs
  fauxmo to emulate a couple smart switches for Alexa.
* LG C7 TV. LG ThinQ Alexa skill only works on 2018 models, not my C7. To work around this,
  I recorded the power signal from the remote control and use fauxmo to emulate a smart switch.
  When the fauxmo switch is turned on/off, Raspberry Pi sends the IR signal to TV.
* Edifier S2000Pro speakers. Connected to TV via optical and to PC with aux input. It comes with
  an IR remote control to control power, volume, EQ modes and input selection. IR LED on Raspberry
  Pi emulates this remote to control the speaker.
* [Eclipse floor lamp](https://www.amazon.com/gp/product/B01KKZRF5C). I like how it looks but
  out of box it's not Alexa friendly. It does not turn itself on when plugged into power and
  requires a touch on its capacitance switch to turn on or dim. This makes it impossible to
  simply put a smart switch on it and turn it into an Alexa controlled light. After some scrutinization
  I found its capacitance switch is clipped onto the lamp body and is easily removeable.
  I soldered a piece of wire onto the copper foil inside the capacitance switch. The wire
  connects to a relay, which also connects to ground of Raspberry Pi. When the relay closes,
  the wire becomes connected to ground, which to the capacitance switch is equivalent to
  touching the switch. When Alexa instructs fauxmo to turn on/off the Eclipse light, fauxo
  closes the relay through GPIO to emulates touching the switch to control the light. (More pictures to follow)
