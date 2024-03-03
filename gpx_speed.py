import time
import os
from random import randrange
import configparser
import ac
import acsys


""""Global variables; can ignore almost everything under here"""

pos = 0 # on-screen app; DO NOT TOUCH
speed = 0 # stores car's current speed
l_speed = 0 # on-screen label showing car's speed
saved_epoch = 0 # saves time in epoch format; used to emulate 1s delay on speed updates
hyphen_chance = 99 # temporary hyphen (dashes) that replaces the speed; emulates temporary GPX malfunction during high speeds

kmh = True # car's speed in kilometres per hour; default
mph = False # car's speed in miles per hour

show_text = "" # on-screen label that determines whether to show km/h or mph
get_speed = "" # used to get car's speed in km/h or mph

"""END Global Variables"""


"""Settings .ini setup; can largely be ignored"""

settings_default_ini_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings", "settings_defaults.ini")
settings_ini_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings", "settings.ini")
config = configparser.ConfigParser()

if not os.path.isfile(settings_ini_path): # create empty settings.ini if it does not exist
    with open(settings_ini_path, "w", encoding="utf-8") as ini:
        ini.write("")

config.read(settings_ini_path)
kmh = config.getboolean("GENERAL", "kmh") # checks if kmh is being used
mph = config.getboolean("GENERAL", "mph") # checks if mph is being used

"""END Settings .ini setup"""


"""Text and unit of speed setup"""

if kmh:
    show_text = "km/h" # text after the speed
    get_speed = acsys.CS.SpeedKMH
if mph:
    show_text = "MPH" # text after the speed
    get_speed = acsys.CS.SpeedMPH

"""END Text and unit of speed setup"""


"""Main functions"""

def acMain(ac_version):
    global l_speed, pos, show_text # gets global variables; DO NOT TOUCH
    
    pos = ac.newApp("GPX Speed") # sets app's name
    
    ac.setTitle(pos, "") # sets empty app title name; can ignore
    ac.setIconPosition(pos, -10000, -10000) # moves the default icon out of screen; can ignore
    ac.setSize(pos, 100, 22) # sets app's size; can ignore
    
    ac.setBackgroundOpacity(pos, 0.5) # sets background opacity; can be adjusted from 0 to 1 in decimals like 0, 0.2, 0.7, etc.
    ac.drawBackground(pos, 0) # can ignore
    ac.drawBorder(pos, 0) # disables border around app; can ignore
    
    l_speed = ac.addLabel(pos, "0 {}".format(show_text)) # prepares on-screen label
    ac.setPosition(l_speed, 50, -1) # positions speed label inside app; may need to be adjusted depending on screen size or aspect ratio beyond 16:9
    
    ac.setCustomFont(l_speed, "Retro Gaming", 0, 0) # sets custom font to emulate font used by popular dashcam manufacturers; can ignore
    ac.setFontSize(l_speed, 18) # sets font size; adjust for different screen size or aspect ratio
    ac.setFontAlignment(l_speed, "center") # alignment; no need to touch
    ac.setFontColor(l_speed, 1, 1, 1, 0.3) # sets font's color to white and turns down opacity to 0.3
    
    #return "GPX Speed"
    
def acUpdate(deltaT):
    global l_speed, speed, saved_epoch, hyphen_chance # gets global variables; DO NOT TOUCH
    
    curr_epoch = int(time.time()) # gets current unix time; can ignore
    if curr_epoch != saved_epoch: # checking against last saved time
        saved_epoch = curr_epoch
        hyphen_chance = randrange(100) # random chance for hyphens (dashes); can ignore
        speed = int(ac.getCarState(0, get_speed)) # gets car's current speed
        ac.setText(l_speed, "---{}".format(show_text)) if hyphen_chance <= 1 else ac.setText(l_speed, "{:03d}{}".format(speed, show_text)) # 2% chance for speed to be replaced by hyphens otherwise populates on-screen label with car's speed; random num generation is 0-99 so 0 is interpreted as 1, 1 is 2, etc.

"""END Main functions"""