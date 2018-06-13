# Weather Data clean and joining script

import pandas as pd
import numpy as np

weather = pd.read_csv('/assets/input/weather.csv')
train = pd.read_csv('/assets/input/train.csv')
test = pd.read_csv('/assets/input/test.csv')

def clean_data(weather):
    '''
    Function that cleans the weather data by removing unwanted columns,
    and imputing missing values
    Parameter: weather dataframe
    Returns: cleaned weather dataframe
    '''

    # Filling out the missing Tavg
    weather.loc[weather["Tavg"] == 'M', 'Tavg'] = round((weather["Tmax"] + weather["Tmin"])/2)

    # Imputing missing values for WetBulb
    ff_missing = [848, 2410, 2412]
    weather.iloc[ff_missing, weather.columns.get_loc('WetBulb')] = np.nan
    weather.fillna(method='ffill', inplace=True)

    weather.iloc[2415, weather.columns.get_loc('WetBulb')] = np.nan
    ffinv = lambda s: s.mask(s == s.shift())
    weather.assign(WetBulb=ffinv(weather["WetBulb"]))

    # Filling missing sunset and getting right dtype
    weather.loc[weather["Sunrise"] == '-', 'Sunrise'] = np.nan
    weather.loc[weather["Sunset"] == '-', 'Sunset'] = np.nan
    weather.fillna(method='ffill', inplace=True)
    weather[['Sunrise','Sunset']] = weather[['Sunrise','Sunset']].apply(pd.to_numeric)

    # Creating daylight, Let there be light!
    weather["Daylight"] = weather["Sunset"] - weather["Sunrise"]
    weather["Daylight"] = weather["Daylight"].astype(str).str[:-2].astype(np.int64)

    # Dropping Sunrise and sunset as no longer needed
    weather.drop(['Sunrise', 'Sunset'], axis=1, inplace=True)

    # Dropping other columns I dont intend to use for further imputation or analysis
    weather.drop(['SnowFall', 'Water1', 'Depth', 'Codesum'], axis=1, inplace=True)

    # Converting Trace amounts to 0.005 and M as 0.00
    weather.loc[weather["PrecipTotal"] == '  T', 'PrecipTotal'] = 0.005
    weather.loc[weather["PrecipTotal"] == 'M', 'PrecipTotal'] = 0.00
    weather["PrecipTotal"] = weather["PrecipTotal"].astype(float)

    # Imputing StnPressure
    ff_missing = [848, 2410]
    weather.iloc[ff_missing, weather.columns.get_loc('StnPressure')] = np.nan
    weather.fillna(method='ffill', inplace=True)

    bf_missing = [87, 2411]
    weather.iloc[bf_missing, weather.columns.get_loc('StnPressure')] = np.nan
    ffinv = lambda s: s.mask(s == s.shift())
    weather.assign(StnPressure=ffinv(weather["StnPressure"]))

    # Imputing missing SeaLevel values
    ff_missing = [832, 994, 1732, 1756, 2090]
    weather.iloc[ff_missing, weather.columns.get_loc('SeaLevel')] = np.nan
    weather.fillna(method='ffill', inplace=True)

    bf_missing = [87, 1745, 2067, 2743]
    weather.iloc[bf_missing, weather.columns.get_loc('SeaLevel')] = np.nan
    ffinv = lambda s: s.mask(s == s.shift())
    weather.assign(SeaLevel=ffinv(weather["SeaLevel"]))

    # Imputing missing Heat and Cool values
    weather.loc[weather["AvgSpeed"] == 'M', 'AvgSpeed'] = np.nan
    weather.loc[weather["Heat"] == 'M', 'Heat'] = np.nan
    weather.loc[weather["Cool"] == 'M', 'Cool'] = np.nan
    ffinv = lambda s: s.mask(s == s.shift())
    weather.assign(AvgSpeed=ffinv(weather["AvgSpeed"]))
    weather.fillna(method='ffill', inplace=True)

    # Split station 1 and 2 and join horizontally
    weather_stn1 = weather[weather['Station']==1]
    weather_stn2 = weather[weather['Station']==2]
    weather_stn1 = weather_stn1.drop('Station', axis=1)
    weather_stn2 = weather_stn2.drop('Station', axis=1)
    weather = weather_stn1.merge(weather_stn2, on='Date')

    # Drop Depart_y and Daylight_y
    weather.drop([['Depart_y', 'Daylight_y'], axis=1, inplace=True

    # Getting the right data types
    weather["Date"] = pd.to_datetime(weather["Date"])
    cols = weather.columns.drop("Date")
    weather[cols] = weather[cols].apply(pd.to_numeric)


    return weather


weather = clean_data(weather)

# def create_features(data):
#     '''
#     Creates features in weather data based off off cleaned dataframe
#     '''
#     pass
#
# def
#
# def join_to_train(weather, train):
#     '''
#     Joins weather data to train on the date columns
#     '''
#     pass
#
# def join_to_test(weather, test):
#     '''
#     Joins weather to test data on date columns
#     '''
#     pass
