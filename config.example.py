setup = {
  'pixeliturls' : ['http://192.168.178.1','http://192.168.178.2'], # Array of URLs of the microcontroller running pixelit with http://
  'minSecondsPerApp' : 10,      # Minimal display time per app
  'scrollTextDelay' : 38,       # Textspeed
  'starttime' : "08:00",        # When to start the display. Ignored when not set
  'stoptime' : "23:00",         # When to stop the display. Ignored when not set
}

mqtt = {
  'usage' : False,              # False = fallback to REST
  'broker' : '192.168.178.2',   # URL of the MQTT broker
  'port' : 1883,                # Port of the MQTT broker, default: 1883 
  'username' : 'myuser',        # mqtt username
  'password' : 'mypassword',    # mqtt password
  'topic' : 'smarthome/PixelIt',# Topic set in the pixelit web ui
  'qos': 1                      # default: 1
}

apps = {
  'clock' : './available-apps/clock-led.py',
  'tatort': './available-apps/tatort-ard-led.py'
}

dota = {
  'player' : 12345123,        # your Dota2 player ID. 
  'days' : 14,                # number of days to consider
  'gamemode' : 22,            # 22 = all pick, 18 = ability draft
  'fechtEveryMinutes' : 1440, # amount of minutes between fetching new data
}

fritzbox = {
  'ip' : '192.168.178.1',     # IP of your fritzbox
  'user': 'myusername',       # username of a fritzbox user
  'password': 'mypassword',   # password for that fritzbox user
  'fetchEveryMinutes' : 1440, # amount of minutes between fetching new data
}

tatort = {
  'fechtEveryMinutes' : 1440, # amount of minutes between fetching new data
}

rssnews = {
  'fechtEveryMinutes' : 180,  # amount of minutes between fetching new data
  'itemsPerFeed' : 15,        # count of items per feed to grab
  'newsfeed' : {
      'ARD' : {               # name for your first feed, URL and icon follow
        'url' : "https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml",
        'icon': "[21,21,21,21,21,21,65535,21,21,21,21,21,65535,65535,65535,21,21,21,65535,65535,65535,65535,65535,21,21,65535,21,65535,65535,65535,65535,21,21,21,21,65535,65535,65535,65535,21,21,21,21,65535,65535,65535,65535,21,21,21,21,65535,65535,21,21,21,21,21,21,21,21,21,21,21]"
        },
      'heise' : {
        'url' : "https://www.heise.de/rss/heise.rdf",
        'icon': "[0,0,0,0,33808,0,0,0,0,0,0,0,33808,0,0,0,0,0,0,33808,0,0,33808,0,0,0,0,33808,0,0,33808,0,0,0,33808,0,0,33808,0,0,0,0,33808,0,0,33808,0,0,0,33808,0,0,33808,0,0,0,0,0,0,0,0,0,0,0]"
        },
  },
}

jellyfin = {
  'url' : 'http://my.jellyfin.url:8096',        # URL and port for you jellyfin server
  'apikey' : 'abc0000000xxxxx',                 # apikey setup in jellyfin server
  'user' : 'myusername',                        # the jellyfin user listening
}

nightscout = {
  'baseurl' : "https://my.nightscout.url",     # URL of your nightscout instance without following dashes or other paths
  'token' : "display-00000000000000000xxx",         # token setup in nightscout with read/display permissions
}

weather = {
  'lat' : 51.17,                # lat of the desired location
  'lon' : 7.01,                 # lon of the desired location
  'fetchEveryMinutes' : 1440,   # amount of minutes between fetching new data
  'apikey' : "000x0x0x00x0xx0x", # openweathermap.com api key
}

pihole = {
  'url' : 'http://my.ip.address:8017',        # URL with Port   
  'apitoken': '000000000xxxx000000x0xxxx000', # API token from pihole webinterface
  'fechtEveryMinutes' : 1440,                 # amount of minutes between fetching new data
}

daycountdown = {
  'entry' : {
      'xmas-2027': {
        'targetdate' : "2027-12-24",              # future date in format YYYY-MM-DD
        'tragetname' : "Christmas of the future", # descibtion of that date to show in the messsage
        'topic'      : "xmas",                    # Determines the icon. currently "holiday", "birthday", "xmas", "calendar"
      }
      'trashcans': {
        'targetdate' : "2025-09-05",              # future date in format YYYY-MM-DD
        'tragetname' : "Take out trash cans",     # descibtion of that date to show in the messsage
      }
}
