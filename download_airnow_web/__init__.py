import pandas as pd
import datetime
import pickle
import os
from urllib.error import HTTPError

def modification_date(filename):
    """
    Get the modification date in datetime format of a file
    """
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def modification_age(filename):
    """
    Get the number of seconds since a file was modified.
    """
    now = datetime.datetime.now()
    return (now-modification_date(filename)).total_seconds()

def downloadandconcat(df,url):
    """
    Download csv file at url and append to 'df' and return.
    Simply return the dataframe if 'df' is None.
    """
    try:
        newdf = pd.read_csv(url)
        if df is None:
            df = newdf
        else:
            df = pd.concat([df,newdf])
        return df
    except HTTPError:
        return df

def download(location,startyear=2010,pollutant='PM2.5',forcerefresh=False):
    """
    Returns a pandas dataframe of air pollution data from the Air Now website
    
    """
    now = datetime.datetime.now()
    if not forcerefresh:
        try:
            dfold = pickle.load(open('oldembassydata_%s.p' % location,'rb'))
            refresh = False
            if modification_date('oldembassydata_%s.p' % location).month!=now.month:
                refresh = True
        except FileNotFoundError:
            refresh = True
    else:
        refresh=True

    if refresh:
        dfold = None
        for y in range(startyear,now.year+1):
            dfold = downloadandconcat(dfold,'http://dosairnowdata.org/dos/historical/%s/%04d/%s_%s_%04d_YTD.csv' % (location,y,location,pollutant,y))    
        pickle.dump(dfold,open('oldembassydata_%s.p' % location,'wb'))

    if not forcerefresh:
        try:
            dfrecent = pickle.load(open('recentembassydata_%s.p' % location,'rb'))
            refresh = False
            if modification_age('recentembassydata_%s.p' % location)>3600:
                refresh = True #if more than an hour old, refresh.
        except FileNotFoundError:
            refresh = True
    else:
        refresh = True

    if refresh:
        dfrecent = downloadandconcat(None,'http://dosairnowdata.org/dos/historical/%s/%04d/%s_%s_%04d_%02d_MTD.csv' % (location,now.year,location,pollutant,now.year,now.month))
        pickle.dump(dfrecent,open('recentembassydata_%s.p' % location,'wb'))
    
    return pd.concat([dfold,dfrecent])
