
smhiprefix = "https://opendata-download-metobs.smhi.se"

core_stations_url = f"{smhiprefix}/api/version/{version}/parameter/{parameter}.{ext}?measuringStations=CORE"

malmen = 85240
lkpg = 85250

datasuffix = f"{smhiprefix}/api/version/{version}/parameter/{parameter}/station/{station}/period/{period}/data.{ext}"


def get_malmen_temp():
    
