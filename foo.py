#!/usr/bin/env python

# from fauxmo import poller, upnp_broadcast_responder, fauxmo, dbg
from fauxmo import *

import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
pin = 12
GPIO.setup(pin, GPIO.OUT)
class LightHandler():
    def light_toggle(self):
        GPIO.output(pin, 1)
        sleep(0.1)
        GPIO.output(pin, 0)

    def on(self):
        print "Light On"
        self.light_toggle()
        return True

    def off(self):
        print "Light off"
        for i in xrange(3):
            self.light_toggle()
            sleep(0.1)
        return True

import subprocess
class TVHandler():
    def on(self):
        subprocess.call(["irsend", "SEND_ONCE", "lg", "KEY_POWER"])
        return True
    def off(self):
        subprocess.call(["irsend", "SEND_ONCE", "lg", "KEY_POWER"])
        return True

class BTHandler():
    def on(self):
        subprocess.call(["irsend", "SEND_ONCE", "Edifier", "KEY_Bluetooth"])
        return True
    def off(self):
        return True

class AuxHandler():
    def on(self):
        subprocess.call(["irsend", "SEND_ONCE", "Edifier", "KEY_Aux"])
        return True
    def off(self):
        return True

# Each entry is a list with the following elements:
#
# name of the virtual switch
# object with 'on' and 'off' methods
# port # (optional; may be omitted)

# NOTE: As of 2015-08-17, the Echo appears to have a hard-coded limit of
# 16 switches it can control. Only the first 16 elements of the FAUXMOS
# list will be used.

FAUXMOS = [
    ['lg tv', TVHandler(), 46345],
    ['eclipse', LightHandler(), 60407],
    ['bluetooth speaker', BTHandler(), 50312],
    ['wired speaker', AuxHandler(), 48532],
    ]

DEBUG=True

# Set up our singleton for polling the sockets for data ready
p = poller()

# Set up our singleton listener for UPnP broadcasts
u = upnp_broadcast_responder()
u.init_socket()

# Add the UPnP broadcast listener to the poller so we can respond
# when a broadcast is received.
p.add(u)

# Create our FauxMo virtual switch devices
for one_faux in FAUXMOS:
    if len(one_faux) == 2:
        # a fixed port wasn't specified, use a dynamic one
        one_faux.append(0)
    switch = fauxmo(one_faux[0], u, p, None, one_faux[2], action_handler = one_faux[1])

dbg("Entering main loop\n")

while True:
    try:
        # Allow time for a ctrl-c to stop the process
        p.poll(100)
        time.sleep(0.1)
    except Exception, e:
        dbg(e)
        print e
        break

