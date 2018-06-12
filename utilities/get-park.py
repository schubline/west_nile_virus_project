import pandas as pd

def modify_parks_csv(parks_csv = 'Parks_-_Locations__deprecated_November_2016_.csv'):
    parks_df = pd.read_csv(parks_csv)

    parks_df = parks_df[['ACRES', 'LOCATION']]

    parks_df.drop(labels = [0,1,2,3], axis = 0, inplace=True)

    pat1 = "\((\d{2}\.\d{2,})"
    pat2 = ", (-\d{2}\.\d{2,})"
    parks_df['lat'] = parks_df.LOCATION.str.extract(pat1)
    parks_df['lon'] = parks_df.LOCATION.str.extract(pat2)
    parks_df.drop(labels= ['LOCATION'], axis = 1, inplace=True)
    parks_df.to_csv("modified_parks.csv")

def park_distance(modparks_csv = "modified_parks.csv"):
    df = pd.read_csv(modparks_csv)
    
