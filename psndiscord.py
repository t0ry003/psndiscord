# PSNDiscord RP, by tory#3784 forked from https://github.com/elsorino/playstationpresence

from psnawp_api import psnawp
from pypresence import Presence
import time
import configparser

# get npsso, PSNID from psnconfig.ini (can be created with "config-creator.exe")

config = configparser.ConfigParser()
config.read('psnconfig.ini')
npsso = config['main']['npsso']
PSNID = config['main']['PSNID']

start_time = int(time.time())
oldpresence = ""
psnawp = psnawp.PSNAWP(npsso)
# initial usage => clear status if online

RPC = Presence("829124881324048404", pipe=0)
RPC.connect()

print(f"User: {PSNID} connected!")

while True:
    user_online_id = psnawp.user(online_id=PSNID)
    mainpresence = str(user_online_id.get_presence())
    print(mainpresence)
    start_time = int(time.time())
    if 'offline' in mainpresence:
        print("User is offline, clearing status")
        RPC.clear()
    else:
        if (oldpresence == mainpresence):
            pass
        else:
            # Best way to work with backwards compatability is a seprate RPClient named Playstation 5 with PS4 game assets
            if 'PS5' in mainpresence:
                system = "ps5"
                if 'CUSA' in mainpresence:
                    RPC.clear()
                    RPC = Presence("829746683835187220", pipe=0)
                    RPC.connect()
                else:
                    RPC.clear()
                    RPC = Presence("829547127809638451", pipe=0)
                    RPC.connect()
            else:
                system = "ps4"
                RPC.clear()
                RPC = Presence("829124881324048404", pipe=0)
                RPC.connect()
            current = mainpresence.split("'")
            if (len(current) == 19):
                RPC.update(state="Idling", start=start_time, small_image=system, small_text=PSNID, large_image=system,
                           large_text="Homescreen")
                print("Idling")
            else:
                if 'gameStatus' in mainpresence:
                    gametext = current[39]
                else:
                    gametext = current[27]
                gameid = current[23]
                gamename = current[27]
                # gamestatus = current[]
                RPC.update(state=gamename, start=start_time, small_image=system, small_text=PSNID,
                           large_image=gameid.lower(), large_text=gametext)
                print("Playing %s" % gamename)
    time.sleep(15)
    oldpresence = mainpresence
