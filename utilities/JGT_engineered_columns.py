# -*- coding: utf-8 -*-


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


def add_five_Truslow_cols(df):
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
    
    new_df = make_timelagged_daylight_col(new_df)
    
    new_df = make_timelagged_temperature_col(new_df)
    
    new_df = make_timelagged_precipitation_col(new_df)
    
    new_df = make_timelagged_windspeed_col(new_df)

    return new_df

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=