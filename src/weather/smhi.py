import utils


smhiprefix = "https://opendata-download-metobs.smhi.se"

# core_stations_url = f"{smhiprefix}/api/version/{version}/parameter/{parameter}.{ext}?measuringStations=CORE"

def get_station_temp(filename, station):
    version = 'latest'
    parameter = 1
    station = stations[station]
    period = 'latest-hour'
    ext = 'json'
    datasuffix = f'api/version/{version}/parameter/{parameter}/station/{station}/period/{period}/data.{ext}'
    return utils.get_html(f'{smhiprefix}/{datasuffix}')
