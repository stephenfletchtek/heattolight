# heattolight
Can interact with Nest Thermostat and Hue Lights
<h2>heattolight.py</h2>
<p>This simple program uses 'thermostat.py' to probe an attached Nest thermostat. It then uses 'remotehue.py' to set a light to blue if the heating is off or red if heating is on.</p>
<p>This shows simple ways to interact with Next and Hue home kit using python and it uses oAuth2 to grant access to the Nest and Hue kit via the web.</p>

<h2>Remotehue.py</h2>
<p>Use this to control hue colour lamps</p>
<p>redlight(<lamp_number>) will set a lamp to red</p>
<p>bluelight(<lamp_number>) will set a lamp to blue</p>
<p>lightOn(<lamp_number>,[0.4576, 0.4099]) will set a lamp to white</p>
<p>Web interaction with Hue lights uses oauth2. Calling refresh() will refresh the tokens and allow interaction.
<p>If the refresh token has become invalid then calling authorize() will allow you to reauthorize your app with the Hue API.</p>
<p>For authorize() to work it needs a valid ClientId and ClientSecret, both obtained from the Hue developers website.</p>
<h2>Thermostat.py</h2>
<p>Running probethermostat() will pole the related Nest Thermostat and determine if it is in 'HEAT' mode or 'OFF'. It needs  valid ClientId, ClientSecret and Token from the Nest developers site. When probethermostat() runs it will automatically refresh the token.
