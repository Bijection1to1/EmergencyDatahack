import pandas as pd
import numpy as np

def hydro_meteo_combine(hydro: pd.DataFrame, meteo: pd.DataFrame) -> pd.DataFrame:
    
    meteo = meteo.groupby(['date_local', 'station_id'])
    meteo = meteo.aggregate({'air_temperature': np.nanmean, 'precipitation': np.nansum, 'wind_speed_aver': np.nanmean})
    meteo = meteo.reset_index().pivot(index='date_local', columns='station_id')
    # add features
    # delta_air_temperature = meteo['air_temperature'].diff()
    # delta_air_temperature.columns = ['delta_air_temperature_' + str(station_id) for station_id in delta_air_temperature.columns]
    # delta_precipitaton = meteo['precipitation'].diff()
    # delta_precipitaton.columns = ['delta_precipitaton_' + str(station_id) for station_id in delta_precipitaton.columns]
    meteo.columns = [str(feature) + '_' + str(station_id) for feature, station_id in meteo.columns]
    # meteo = pd.concat([meteo, delta_air_temperature, delta_precipitaton], axis=1)

    hydro = hydro.pivot(index='date', columns='station_id', values='delta_stage_max')
    hydro.columns = ['delta_stage_max_' + str(station_id) for station_id in hydro.columns]

    res = pd.merge(hydro, meteo, left_index=True, right_index=True, how='left').reset_index()
    res.columns = ['date_local'] + res.columns[1:].to_list()
    return res