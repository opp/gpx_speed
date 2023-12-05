import time
import os
from random import randrange
import configparser
import ac
import acsys

pos = 0
speed = 0
l_speed = 0
saved_epoch = 0
hyphen_chance = 99

kmh = True
mph = False

show_text = ""
get_speed = ""

settings_default_ini_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings", "settings_defaults.ini")
settings_ini_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings", "settings.ini")
config      = configparser.ConfigParser()

if not os.path.isfile(settings_ini_path): # create empty if not there
    with open(settings_ini_path, "w", encoding="utf-8") as ini:
        ini.write("")

config.read(settings_ini_path)
kmh = config.getboolean("GENERAL", "kmh")
mph = config.getboolean("GENERAL", "mph")

if kmh:
    show_text = "km/h"
    get_speed = acsys.CS.SpeedKMH
if mph:
    show_text = "MPH"
    get_speed = acsys.CS.SpeedMPH

def acMain(ac_version):
    global l_speed
    
    pos = ac.newApp("GPX Speed")
    
    ac.setTitle(pos, "")
    ac.setIconPosition(pos, -10000, -10000)
    ac.setSize(pos, 100, 22)
    
    ac.setBackgroundOpacity(pos, 1)
    ac.drawBackground(pos, 1)
    ac.drawBorder(pos, 0)
   
    #ac.initFont(0, "Retro Gaming", 0, 0)
    
    l_speed = ac.addLabel(pos, "0 {}".format(show_text))
    ac.setPosition(l_speed, 50, -1)
    
    ac.setCustomFont(l_speed, "Retro Gaming", 0, 0)
    ac.setFontSize(l_speed, 18)
    ac.setFontAlignment(l_speed, "center")
    
    #return "GPX Speed"
    
def acUpdate(deltaT):
    global l_speed, speed, saved_epoch, hyphen_chance
    
    curr_epoch = int(time.time())
    if curr_epoch != saved_epoch:
        saved_epoch = curr_epoch
        hyphen_chance = randrange(100)
        speed = int(ac.getCarState(0, get_speed))
        ac.setText(l_speed, "---{}".format(show_text)) if hyphen_chance <= 1 else ac.setText(l_speed, "{:03d}{}".format(speed, show_text))