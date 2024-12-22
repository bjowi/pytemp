from stations import smhi_key_to_station, smhi_name_to_station
import utils


smhiprefix = "https://opendata-download-metobs.smhi.se"

# core_stations_url = f"{smhiprefix}/api/version/{version}/parameter/{parameter}.{ext}?measuringStations=CORE"

def get_smhi_url(station_name, parameter,
                 period='latest-hour', version='latest', ext='json'):
    station_key = smhi_name_to_station[station_name]['key']
    datasuffix = f'api/version/{version}/parameter/{parameter}/station/{station_key}/period/{period}/data.{ext}'
    return f'{smhiprefix}/{datasuffix}'

