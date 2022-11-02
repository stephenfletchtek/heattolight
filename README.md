# Heat to Light

## heattolight.py

This program interacts with a Nest Thermostat and Hue Lights. It shows simple ways of using python to interact with Nest and Hue home kit, and **OAuth 2.0** to grant access via the web. User interface is via the command line.

### Structure

* _remotehue.py_ sets a light to blue if the heating is off, or red if heating is on
* _thermostat.py_ probes an attached Nest thermostat

## remotehue.py

### These commands control hue colour lamps:
* ```redlight(<lamp_number>)``` sets a lamp to red
* ```bluelight(<lamp_number>)``` sets a lamp to blue
* ```lightOn(<lamp_number>,[0.4576, 0.4099])``` sets a lamp using XY colour - [0.4576, 0.4099] is white

### Note:
* Web interaction with Hue lights uses OAuth 2.0. ```refresh()``` refreshes the tokens needed for interaction
* If the refresh token has become invalid ```authorize()``` reauthorizes your app with the Hue API
* For ```authorize()``` to work it needs a valid **ClientId** and **ClientSecret**, both obtained from the Hue developers website

## thermostat.py
```probethermostat()``` poles the related Nest Thermostat to determine if it is in 'HEAT' mode or 'OFF'.

### You need these from the Nest developers site
* ClientId
* ClientSecret
* Token

When ```probethermostat()``` runs it automatically refreshes the token.
