#!/usr/bin/env python3

from thermostat import probethermostat
from remotehue import bluelight, redlight

# find out if the house is heating
heating = probethermostat()

# make light red if heating and blue if not
if heating == 'HEATING':
    redlight(2)
else:
    bluelight(2)
