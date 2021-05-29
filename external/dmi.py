# Imports
from collections import defaultdict
import pandas as pd 
import requests
import json
import numpy as np
from datetime import datetime


class DMI:
    def __init__(self, key_path):
        if type(key_path) != str:
            raise TypeError('The type of key_path should be string')
        self.key_path = key_path
        self.key = self.__read_key()
        if not self.key:
            raise ValueError('Invalid key path')
        self.baseurl = 'https://dmigw.govcloud.dk/metObs/v1/observation'
        self.validFields = set(['temp_dry', 'temp_dew', 'temp_mean_past1h', 'temp_max_past1h', 'temp_min_past1h', 'temp_max_past12h', 'temp_min_past12h',
                                'temp_grass', 'temp_grass_max_past1h', 'temp_grass_mean_past1h', 'temp_grass_min_past1h',
                                'temp_soil', 'temp_soil_max_past1h', 'temp_soil_min_past1h', 'temp_soil_mean_past1h',
                                'humidity', 'humidity_past1h', 'pressure_at_sea', 'pressure',
                                'wind_speed', 'wind_max', 'wind_min', 'wind_dir', 'wind_dir_past1h', 'wind_speed_past1h', 'wind_gust_always_past1h', 'wind_min_past1h', 'wind_max_per10min_past1h',
                                'precip_past10min', 'precip_past1h', 'precip_past1min', 'precip_past24h*', 'precip_dur_past10min', 'precip_dur_past1h',
                                'snow_depth_man', 'snow_cover_man', 'visibility', 'visib_mean_last10min', 'cloud_height', 'cloud_cover', 'weather',
                                'sun_last10min_glob', 'radia_glob', 'radia_glob_past1h', 'sun_last1h_glob', 'leav_hum_dur_past10min', 'leav_hum_dur_past1h'
                                ])

    def __read_key(self):
        key = ''
        with open(self.key_path, 'r') as f:
            key = f.read()
        return key

    def get_all_stations(self):
        '''
        Get all stations and their location, return a pandas dataframe
        '''
        url_sta = 'https://dmigw.govcloud.dk/metObs/v1/station?limit=10000&api-key={0}'.format(
            self.key)

        try:
            r = requests.get(url_sta)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        if r.status_code != 200:
            raise ValueError('response code--'+str(r.status_code))
        data = r.json()

        # store json data in dataframe
        stations = pd.DataFrame(data)
        lat, lon = [], []

        # add lat lon data for each station
        for _, row in stations.iterrows():
            lat.append(row['location']['latitude'])
            lon.append(row['location']['longitude'])
        stations['lat'] = lat
        stations['lon'] = lon
        stations = stations[['stationId', 'country',
                             'name', 'type', 'lat', 'lon']]
        return stations

    def get_metdata(self, start_date, end_date, station_id=None, field=None, limit='100000'):
        '''
        Get meteorology data, return a a pandas dataframe
        Parameters:
            - field: 'temp_dry', 'humidity', 'wind_speed', 'sun_last1h_glob', full list https://confluence.govcloud.dk/pages/viewpage.action?pageId=26476616
            - start_date/end_date: 8-digit string, e.g. '20200602'
            - station_id: the ID of station, e.g. '06188'
            - limit: the maximum number of rows, e.g. '10000000'
        '''
        query = self.__generate_query(
            field, start_date, end_date, station_id, limit)

        try:
            r = requests.get(self.baseurl, params=query)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        if r.status_code != 200:
            raise ValueError('response code--'+str(r.status_code) +
                             ', please check the parameter input of .get_metdata method')
        json = r.json()

        # conver json data to data frame
        df = pd.DataFrame(json)
        df['time'] = pd.to_datetime(df['timeObserved'], unit='us')
        df = df.drop(['_id', 'timeCreated', 'timeObserved'], axis=1)    
        return df

    # get start date and end date in unixtime format
    def __get_timeinterval(self, start_date, end_date):
        start_date = self.__to_datetime(start_date)
        end_date = self.__to_datetime(end_date)
        return self.__datetime2unixtime(start_date), self.__datetime2unixtime(end_date)

    # convert 8-digit string to datetime
    def __to_datetime(self, date):
        if type(date) != str or len(date) != 8:
            raise TypeError(
                'Input of start_date/end_date should be a 8-digit string, e.g. "20201106"')
        return datetime(int(date[:4]), int(date[4:6]), int(date[6:]))

    # convert datetime to unixtime
    def __datetime2unixtime(self, datetime):
        return str(int(pd.to_datetime(datetime).value * 10**-3))

    # generate query parameters
    def __generate_query(self, field, start_date, end_date, station_id, limit):
        start_time, end_time = self.__get_timeinterval(start_date, end_date)
        query = {
            'api-key': self.key,
            'from': start_time,
            'to': end_time,
            'limit': limit
        }
        if field:
            if field in self.validFields:
                query['parameterId'] = field
            else:
                raise ValueError(
                    'Find the valid field input from the following list: '+str(self.validFields))
        if station_id:
            query['stationId'] = station_id
        return query