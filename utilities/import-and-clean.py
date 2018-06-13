# -*- coding: utf-8 -*-
"""
Created on Monday June 11, 2018

@author: Jon, James, Schubert
"""
## Dummies for neighborhood, species (pip-rest, pip, rest, other)
## Neighborhood maker
## park distance (area/distance)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

import numpy as np
import pandas as pd
import datetime as dt
import json

def dummy_species(df):
    """
    Converts the "Species" column of a dataset to dummies.
    Since there are only three options for species that matter,
    it first transforms the column and then creates the dummies."""
    ## Imports: pandas for dataframe manipulation
    import pandas as pd

    ## Make sure everything is good
    assert df["Species"].isnull().sum() == 0

    ## map the column
    df['Species'] = df['Species'].map(lambda x: "OTHER" if ((x != 'CULEX PIPIENS/RESTUANS') & (x != 'CULEX RESTUANS') & (x != 'CULEX PIPIENS')) else x)

    ## make dummies from the Species_modfied column
    df = pd.get_dummies(df, columns = ['Species'])

    ## drop the 'other' column
    df.drop(labels = ['Species_OTHER'],  axis = 1, inplace=True)

    return df
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def dummy_neighborhood(df):
    """
    Converts the "neighborhood" column of a dataset to dummies.
    Drops the first one. This produces a very wide dataset."""
    ## Imports: pandas for dataframe manipulation
    import pandas as pd

    ## Make sure everything is good
    # assert df["neighborhood"].isnull().sum() == 0

    ## make dummies from the Species_modfied column
    flag = False
    if len(df['neighborhood'].unique()) == 65:
        flag = True
    df = pd.get_dummies(df, columns = ['neighborhood'])
    if flag:
        df['neighborhood_Hermosa'] = 0
        df['neighborhood_West Pullman'] = 0

    return df
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def point_inside_polygon(x,y,poly):
    """Return True if the point described by x, y is inside of the polygon
    described by the list of points [(x0, y0), (x1, y1), ... (xn, yn)] in
    ``poly``

    Code from http://www.ariel.com.au/a/python-point-int-poly.html which
    in turn was adapted from C code found at
    http://local.wasp.uwa.edu.au/~pbourke/geometry/insidepoly/
    """
    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def lat_lon_ds(p_1, p_2):
    """Argument 'p1' is a list of decimal [lat, lon] coords in degrees. 'p2' is another list.
    Function returns the distance between them in meters, without correction for curvature of the earth.
    Distance will be slightly underestimated by a fraction approximately (t - sin(t)), where t is the angular separation
    between the two points in radians.  For 1 degree of latitude, the relative error is < 1e-6."""

    import numpy as np

    # http://frederic.chambat.free.fr/geophy/inertie_pepi01/article.pdf
    # Equitorial radius, eqn. 15
    R_earth = 6378137  # meters

    # Distance btw O'Hare and Wrigley field is 20879.8 meters, along a great circle
    # coords are [41.94885800000001, 87.65774809999999], [41.9741625, 87.9073214]
    # According to http://edwilliams.org/gccalc.htm
    # This gives a Chicago-area correction factor of (20879.8/20849.9),
    # where the denominator is calculated using uncorrected R_earth.

    R = R_earth*(20879.8/20849.9)

    theta_1 = (90 - p_1[0])*(2*np.pi/360)
    phi_1 = p_1[1]*(2*np.pi/360)
    theta_2 = (90 - p_2[0])*(2*np.pi/360)
    phi_2 = p_2[1]*(2*np.pi/360)

    def x(r,phi,theta):
        return r*np.sin(theta)*np.cos(phi)

    def y(r,phi,theta):
        return r*np.sin(theta)*np.sin(phi)

    def z(r,phi,theta):
        return r*np.cos(theta)

    # Calculate euclidean distance
    delta_s= np.sqrt(
        (x(R, phi_1, theta_1) - x(R, phi_2, theta_2))**2 + \
        (y(R, phi_1, theta_1) - y(R, phi_2, theta_2))**2 + \
        (z(R, phi_1, theta_1) - z(R, phi_2, theta_2))**2 \
    )

    return delta_s

def modify_parks_csv(parks_csv = '../Parks_-_Locations__deprecated_November_2016_.csv'):
    parks_df = pd.read_csv(parks_csv)

    parks_df = parks_df[['ACRES', 'LOCATION']]

    parks_df.drop(labels = [0,1,2,3], axis = 0, inplace=True)

    pat1 = "\((\d{2}\.\d{2,})"
    pat2 = ", (-\d{2}\.\d{2,})"
    parks_df['lat'] = parks_df.LOCATION.str.extract(pat1)
    parks_df['lon'] = parks_df.LOCATION.str.extract(pat2)
    parks_df.drop(labels= ['LOCATION'], axis = 1, inplace=True)
    parks_df.to_csv("modified_parks.csv")

def score(entry_lat, entry_lon, area_col, lat_col, lon_col):
    score = 0
    for lat, lon, area in zip(lat_col, lon_col, area_col):
        score += area / lat_lon_ds((entry_lat,entry_lon), (lat,lon))
        # print(score)
    return score

def make_score_column(df, park_df):
    lat_col = park_df['lat'].astype(float)
    lon_col = park_df['lon'].astype(float)
    area_col = park_df['ACRES'].astype(float)

    entry_lat_col = df['Latitude']
    entry_lon_col = df['Longitude']
    score_column = []
    for entry_lat, entry_lon in zip(entry_lat_col, entry_lon_col):
        score_column.append(score(entry_lat, entry_lon, area_col, lat_col, lon_col))

    df['park_score'] = score_column
    return df

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def make_datetimeobject_col(df):
    new_df = df.copy()
    new_df['dtDate'] = pd.to_datetime(new_df['Date'])
    return new_df


def timelagged_daylight(obs_date):
    """
    Calcuates the hours of daylight 35 days prior to a given date.
    Formula is from Lebl et at, eqn. 1, modified by James Truslow because they screwed
    up the daylength coefficient.

    Parameters
    ----------
    obs_date: a datetime timestamp for the observation


    Returns
    -------
    Number of daylight hours 35 days prior to 'obs_date'
    """

    import datetime as dt

    lag_days = 35
    time_lag = dt.timedelta(days=lag_days)
    lagged_date = obs_date - time_lag

    # This calculation of day of year will by off by leap years, and maybe an off-by-one for day 0
    day_of_year = (lagged_date.toordinal() - dt.datetime(2007,1,1).toordinal())%365
    eps = np.arcsin(0.39795 * np.cos(0.2163108 + 2 * np.arctan(0.9671396 * np.tan(0.0086*(day_of_year - 186)))))
    phi = 41.983*2*np.pi/360
    D = 24 - (24/np.pi)*np.arccos((np.sin(0.8333*np.pi/180)+np.sin(phi)*np.sin(eps))/(np.cos(phi)*np.cos(eps)))

    return D


def make_timelagged_daylight_col(df):
    new_df = df.copy()
    new_df['TimeLaggedDaylight'] = new_df['dtDate'].map(timelagged_daylight)
    return new_df


def timelagged_temperature(df, obs_date, lag_days_LB=7, lag_days_UB=0):
    """
    Calculates the average temperature in Chicago in some time window before an observation

    Parameters
    ----------
    df: dataframe with weather info.  I hope there is date info as datetime objects
    obs_date: a datetime timestamp for the observation
    lag_days_LB: chronological lower bound of time window (inclusive), in number of days *before* observation
    lag_days_UB: chronological upper bound of time window (inclusive), in number of days *before* observation

    Returns
    -------
    Average temperature in time window
    """

    Date_obs = obs_date

    time_lag_LB = dt.timedelta(days=lag_days_LB)
    time_lag_UB = dt.timedelta(days=lag_days_UB)

    Date_LB = Date_obs - time_lag_LB
    Date_UB = Date_obs - time_lag_UB

    window_Tmean = df[(df.dtDate >= Date_LB) & (df.dtDate <= Date_UB)].Tavg.mean()

    return window_Tmean


def make_timelagged_temperature_col(df):
    new_df = df.copy()
    new_df['TimeLaggedTemperature'] = df['dtDate'].map(lambda row: timelagged_temperature(df,row))
    return new_df


def timelagged_precipitation(df, obs_date, lag_days_LB=70, lag_days_UB=0):
    """
    Calcuates the average precipitation in Chicago in some time window before an observation

    Parameters
    ----------
    df: dataframe with weather info.  I hope there is date info as datetime objects
    obs_date: a datetime timestamp for the observation
    lag_days_LB: chronological lower bound of time window (inclusive), in number of days *before* observation
    lag_days_UB: chronological upper bound of time window (inclusive), in number of days *before* observation

    Returns
    -------
    Average precipitation in time window
    """

    Date_obs = obs_date

    time_lag_LB = dt.timedelta(days=lag_days_LB)
    time_lag_UB = dt.timedelta(days=lag_days_UB)

    Date_LB = Date_obs - time_lag_LB
    Date_UB = Date_obs - time_lag_UB

    window_Pmean = df[(df.dtDate >= Date_LB) & (df.dtDate <= Date_UB)].PrecipTotal.mean()

    return window_Pmean


def make_timelagged_precipitation_col(df):
    new_df = df.copy()
    new_df['TimeLaggedPrecipitation'] = df['dtDate'].map(lambda row: timelagged_precipitation(df,row))
    return new_df


def timelagged_windspeed(df, obs_date, lag_days_LB=21, lag_days_UB=0):
    """
    Calcuates the average windspeed in Chicago in some time window before an observation

    Parameters
    ----------
    df: dataframe with weather info.  I hope there is date info as datetime objects
    obs_date: a datetime timestamp for the observation
    lag_days_LB: chronological lower bound of time window (inclusive), in number of days *before* observation
    lag_days_UB: chronological upper bound of time window (inclusive), in number of days *before* observation
    Returns
    -------
    Average precipitation in time window
    """

    Date_obs = obs_date

    time_lag_LB = dt.timedelta(days=lag_days_LB)
    time_lag_UB = dt.timedelta(days=lag_days_UB)

    Date_LB = Date_obs - time_lag_LB
    Date_UB = Date_obs - time_lag_UB

    window_Vmean = df[(df.dtDate >= Date_LB) & (df.dtDate <= Date_UB)].AvgSpeed.mean()

    return window_Vmean


def make_timelagged_windspeed_col(df):
    new_df = df.copy()
    new_df['TimeLaggedWindspeed'] = df['dtDate'].map(lambda row: timelagged_windspeed(df,row))
    return new_df

def clean_data(weather):
    '''
    Function that cleans the weather data by removing unwanted columns,
    and imputing missing values
    Parameter: weather dataframe
    Returns: cleaned weather dataframe
    '''

    # filling out the missing Tavg
    weather.loc[weather["Tavg"] == 'M', 'Tavg'] = round((weather["Tmax"] + weather["Tmin"])/2)

    # imputing missing values for WetBulb
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

    #droppin Sunrise and sunset as no longer needed
    weather.drop(['Sunrise', 'Sunset'], axis=1, inplace=True)

    #dropping other columns I dont intend to use for further imputation or analysis
    weather.drop(['SnowFall', 'Water1', 'Depth', 'CodeSum'], axis=1, inplace=True)

    # converting Trace amounts to 0.005 and M as 0.00
    weather.loc[weather["PrecipTotal"] == '  T', 'PrecipTotal'] = 0.005
    weather.loc[weather["PrecipTotal"] == 'M', 'PrecipTotal'] = 0.00
    weather["PrecipTotal"] = weather["PrecipTotal"].astype(float)

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

    weather["dtDate"] = pd.to_datetime(weather["Date"])
    # cols = weather.columns.drop("Date")
    # cols = weather.columns.drop("Depart")
    # cols = weather.columns.drop("StnPressure")
    # weather[cols] = weather[cols].apply(pd.to_numeric)
    weather.drop(['Depart','StnPressure'], axis = 1, inplace = True)
    weather['Tavg'] = weather['Tavg'].astype(float)
    weather['PrecipTotal'] = weather['PrecipTotal'].astype(float)
    weather['AvgSpeed'] = weather['AvgSpeed'].astype(float)

    return weather

def make_avg_weather_columns(df):
    """ Calculates average meterological data on a given date.  Average of both
    weather stations

    Parameters
    ----------
    df: dataframe with weather info.  I hope there is date info as datetime objects


    Returns
    -------
    new_df: copy of 'df' with new columns added

    """

    new_df = clean_data(df.copy())


    # new_df['avg_Tavg'] = new_df.groupby(by ='Date').Tavg.mean()
    # new_df['avg_PrecipTotal'] = new_df.groupby(by = 'Date').PrecipTotal.mean()
    # new_df['avg_AvgSpeed'] = new_df.groupby(by = 'Date').AvgSpeed.mean()
    avg_Tavg_dict = dict(new_df.groupby(by ='Date').Tavg.mean())
    avg_PrecipTotal_dict = dict(new_df.groupby(by ='Date').PrecipTotal.mean())
    avg_AvgSpeed_dict = dict(new_df.groupby(by ='Date').AvgSpeed.mean())

    new_df['avg_Tavg'] = new_df['Date'].map(avg_Tavg_dict)
    new_df['avg_PrecipTotal'] = new_df['Date'].map(avg_PrecipTotal_dict)
    new_df['avg_AvgSpeed'] = new_df['Date'].map(avg_AvgSpeed_dict)

    return new_df



def add_six_Truslow_cols(df):
    """Calls a sequence of functions to add five engineered-feature columns to a dataframe.
    Input dataframe must include the original columns from the 'weather.csv' dataset, or
    at least a cleaned version with the same column titles, and with all numeric data.

    Parameters
    ----------
    df: Dataframe with weather info.
    Returns
    -------
    Modified version of 'df', with five columns added.
    """

    new_df = make_datetimeobject_col(df)

    new_df = make_avg_weather_columns(new_df)

    new_df = make_timelagged_daylight_col(new_df)

    new_df = make_timelagged_temperature_col(new_df)

    new_df = make_timelagged_precipitation_col(new_df)

    new_df = make_timelagged_windspeed_col(new_df)

    return new_df

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def fix_column_names(df):
    """Returns the dataframe with column names in snake_case"""
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('/','_')
    return df

def make_datetimeobject_col(df):
    new_df = df.copy()
    new_df['dtDate'] = pd.to_datetime(new_df['Date'])
    return new_df
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def get_neighborhood_for_point(lat, lng):
    """Given a latitude and longitude, find the neighborhood that this point is
    inside.  data is in a file in assets"""

    dictionaryfile = open('../assets/community_areas.json')
    dictionarystring = dictionaryfile.read()
    dictionaryfile.close()

    data = json.loads(dictionarystring)

    for commarea, commdata in data.items():
        if point_inside_polygon(lng, lat, commdata):
            return commarea
    else:
        return None
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def make_neighborhood_column(df):
    """Makes neighborhood column using functions above"""
    neighborhood_col = []
    for i in range(len(df['Latitude'])):
       neighborhood_col.append(get_neighborhood_for_point(df['Latitude'][i], df['Longitude'][i]))
    df['neighborhood'] = neighborhood_col
    return df

def add_neighborhood_infection_column(df):
    """takes a dataframe with a neighborhood column and a WnvPresent column and adds a column"""
    d = {"O'Hare": 'high',
     'South Deering': 'high',
     'Dunning': 'high',
     'Fringe': 'high',
     'Norwood Park': 'high',
     'New City': 'medium',
     'Calumet Heights': 'medium',
     'Humboldt Park': 'medium',
     'Sauganash,Forest Glen': 'medium',
     'Portage Park': 'medium',
     'Edison Park': 'medium',
     'Belmont Cragin': 'medium',
     'Hegewisch': 'medium',
     'Clearing': 'medium',
     'Little Italy, UIC': 'medium',
     'Mount Greenwood': 'medium',
     'Ashburn': 'medium',
     'Beverly': 'medium',
     'Lincoln Park': 'medium',
     'Grand Crossing': 'medium',
     'Archer Heights': 'medium',
     'West Ridge': 'medium',
     'East Side': 'medium',
     'Morgan Park': 'medium',
     'Irving Park': 'medium',
     'North Park': 'medium',
     'Chicago Lawn': 'medium',
     'Austin': 'medium',
     'Galewood': 'medium',
     'Little Village': 'medium',
     'Washington Heights': 'medium',
     'Woodlawn': 'medium',
     'Lincoln Square': 'medium',
     'Auburn Gresham': 'medium',
     'Ukrainian Village': 'medium',
     'Burnside': 'medium',
     'Avondale': 'medium',
     'Englewood': 'medium',
     'Edgewater': 'medium',
     'Grand Boulevard': 'low',
     'South Chicago': 'low',
     'North Lawndale': 'low',
     'Chatham': 'low',
     'Wicker Park': 'low',
     'Avalon Park': 'low',
     'Garfield Ridge': 'low',
     'South Shore': 'low',
     'Riverdale': 'low',
     'West Town': 'low',
     'Roseland': 'low',
     'Lake View': 'low',
     'Pullman': 'low',
     'Gage Park': 'low',
     'Montclare': 'low',
     'Mckinley Park': 'low',
     'Loop': 'low',
     'Rogers Park': 'none',
     'Bridgeport': 'none',
     'Hyde Park': 'none',
     'Garfield Park': 'none',
     'Streeterville': 'none',
     'Washington Park': 'none',
     'Lower West Side': 'none',
     'Logan Square': 'none',
     'Printers Row': 'none'}

    df['neighborhood_infection_category'] = df['neighborhood'].map(d)

    return df

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def master_clean(df, parkdf, weatherdf, nbhood = True):
    """
    Combines functions to make neighborhood column (optional), dummy species,
    dummy neighborhood, make score column, add columns for time-delayed weather,
    and fix the column names
    """
    ## Don't bother adding the neighborhood column if it's already there
    if nbhood == False:
        df = make_neighborhood_column(df)

    df = make_datetimeobject_col(df)

    df = dummy_species(df)

    df = add_neighborhood_infection_column(df)

    df = pd.get_dummies(df, columns = ['neighborhood_infection_category'])

    ## We're assuming that the binned neighborhoods will be better
    # df = dummy_neighborhood(df)



    df = make_score_column(df, parkdf)

    weatherdf = add_six_Truslow_cols(weatherdf)

    print("####################")
    print(df.columns)

    weather_to_join = weatherdf[['dtDate','Daylight','avg_Tavg', 'avg_PrecipTotal', 'avg_AvgSpeed', 'TimeLaggedDaylight', 'TimeLaggedTemperature','TimeLaggedPrecipitation','TimeLaggedWindspeed' ]]

    df = pd.merge(df, weather_to_join, how = 'left', on = 'dtDate', sort = False)

    df = fix_column_names(df)

    df = df.drop_duplicates()

    print(list(df.columns))

    return df


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

train = pd.read_csv('../assets/train_with_neighborhoods.csv', index_col = 0)
test = pd.read_csv('../assets/test_with_neighborhoods.csv', index_col = 0)
park = pd.read_csv('../modified_parks.csv', index_col = 0)
weather = pd.read_csv('../assets/input/weather.csv')

# train_mini = train.head(100)
# test_mini = test.head(100)
#
# master_clean(train_mini, park, weather).to_csv('mini_master_clean_train.csv', index = False)
# master_clean(test_mini, park, weather).to_csv('mini_master_clean_test.csv', index = False)

master_clean(train, park, weather).to_csv('../assets/master_clean_train.csv', index = False)
master_clean(test, park, weather).to_csv('../assets/master_clean_test.csv', index = False)
