# License

{{ project }}
Copyright (C) {{ year }}  {{ organization }}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


# pixelit.py and Pixelit Server

## What is Pixelit?

>The PixelIt is an ESP8266 / ESP32 (under construction) and WS2812B-LED based PixelArt display, controlled and fed via a JSON API. Settings and small tests are possible via the web interface, also a node-red node (node-red-contrib-pixelit) for the JSON API is available.
Source: https://github.com/pixelit-project/PixelIt

Besides of that, one can send text and bitmap messages via REST or MQTT to display on the led matrix. 

## What is pixelit.py?

pixelit.py is a python library aimed to support creating python scripts that send data to display on a pixelit led matrix via REST or MQTT. These scripts does not run on the ESP, but on a seperate machine, like a Raspberry Pi or another kind of server.

> :warning:  To use pixelit.py via mqtt you will need a mqtt broker (e.g. mosquitto) in your network. 

Imagine you have some python scripts like grabing news from an RSS feed, following you favorite artists Toots on mastodon, showing the current weather or calulating your personal winrate in your favorite MOBA online game. You might want to display all this information on you led matrix. pixelit.py supports you encapsulating the logic from the api, so that you just need to call one pixelit.py function at the end of your custom script.

And hopefully you don't have do dig deep into pixelit.py's code since all important settings are easily accessible in a handy `config.py`.

#### Example Apps are:

* Simple Clock Display
* Current Weather Temperature
* Pi-Hole daily ads blocked
* RSS News Feed
* Dota2 Winrate Calculator
* Nightscout Bloodsugar Display
* tatort / Polizeiruf 110 Checker

### Sending Text to Matrix

```python
sendText(
   text_msg="Hello World",
   red=255,
   green=255,
   blue=255,
   bigFont="false",
   scrollText="auto",
   centerText="false"
   )
```
| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
|`text_msg`|String|        |Text to display on the led matrix|
|`red`, `green` and `blue`| Integer|0-255|values for text color|
|`bigFont`| Boolean / String | "true" / "false"|Alternates the font|
|`scrollText`|Boolean / String| "true" / "false" / "auto"| sets scrolling text |
|`centerText`|String| "true" / "false"| sets text to centered|


For details please also consider https://pixelit-project.github.io/api.html#text.


### Sending Bitmap and Text to Matrix

 ```python
 sendApp(
   text_msg="Hello World",
   red=255,
   green=255,
   blue=255,
   icon="[255]",
   bigFont="false",
   scrollText='auto',
   centerText="false"
   )
 ```

This functions shares the same arguments as sendText() but also has the `icon` argument, which needs a bitmap description in braces as String.

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
|`icon`|String|e.g. "[255,255,255,255]"|bitmap description in braces|

For details please also consider https://pixelit-project.github.io/api.html#text


##### `sendNotification()` (not implemented yet)

### Calucalting cache

### Calucalting timestamps

## What is Pixelit Server?

While the pixelit platform can only handle single calls via MQTT or REST, Pixelit Server collects multiple scripts and loops them, creating a constant varaity of information shown on your led matrix.

Therefore is dependent on functions defined in `pixelit.py`. While you can use `pixelit.py` on its own, the server always needs interaction with pixelit.py functions.

### Pixelit Server Features
* Automatically find, display and cycle all active python scripts using `pixelit.py`
* Approximate display time for longer messages


### How to setup Pixelit Server

1. Put all your python scripts using pixelit.py into a `./active-apps` directory. You may also just use symbolic links via `ln -s` for that. Also pixelit.py and config.py need to be in this directory. Symbolic links are highly recommended.
```text
Example stucture of the directory to cycle through dota-led.py and weathercurrent.py:

.
├── active-apps
│   ├── config.py -> ../config.py
│   ├── dota-led.py -> ../dota-led.py
│   ├── pixelit.py -> ../pixelit.py
│   └── weathercurrent.py -> ../weathercurrent.py
├── config.py
├── dota-led.py
├── pixelit.py
├── pixelit-server.py    <-- run this
└── weathercurrent.py    <-- or just run this (to test once)
```
2. Start pixelit- server via `python3 pixelit-server.py` or create a [systemd service](./pixelit.service) for that.
   * You might then start and stop this server via `systemctl start|stop|restart|status pixelit.service`.
3. Be sure that all required python libraries are installed like `requests`, `pickle`, `datetime` and `pytz`.  Depending on your apps you might also need `json`, `feedparser`, `random`, `bs4` and `urllib` and probably more for your own needs.




### How to create and define apps?

To create and define apps for pixelit and pixelit server you should use functions from pixelit.py

What is important here?
* When sending an app via `pixelit.sendApp()` it not only shows bitmap and text message, but also saves the length of the message via `pixelit.writeCharsToFile()`
* pixelit-server can read these chars to calculate the display duration for each show message via `calculateDisplayDuration()`. For every call of `pixelit.sendApp()` the amount of characters are saved into a local cache file called `.chars.cache`.
  * If a message is shorter than the configured `minSecondsPerApp` in `config.py`, then it waits for exactly this duration
  * If a massage is longer than the configured duration, it calculates the time depending on the length of the message.
  * If you call an script in your `./active-apps` directory but do not want anything to show, use `pixelit.skipApp()` to signalize skipping the char check and proceeding with the next app. This can be used to skip an app.



  * When your message is interrupted by the internal clock display consider setting a higher value in your Pixelit web UI for clock auto fallback time 

