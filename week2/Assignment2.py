
# coding: utf-8

# # Assignment 2
#
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
#
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
#
# Each row in the assignment datafile corresponds to a single observation.
#
# The following variables are provided to you:
#
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
#
# For this assignment, you must:
#
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
#
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

#get_ipython().magic('matplotlib notebook')


# In[2]:

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
#import mplleaflet
import pandas as pd
import numpy as np
import re

#def leaflet_plot_stations(binsize, hashid):

#    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

#    station_locations_by_hash = df[df['hash'] == hashid]

#    lons = station_locations_by_hash['LONGITUDE'].tolist()
#    lats = station_locations_by_hash['LATITUDE'].tolist()

#    plt.figure(figsize=(8,8))

#    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

#    return mplleaflet.display()

#leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[3]:

df = pd.read_csv('data/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df = df.set_index('Date')
df = df.Data_Value
def get_day(item):
    return item[5:]
def choose_day(x):
    if re.search('02-29$',x) or re.search('^2015',x): return False
    else: return True
def choose_2015(x):
    if re.search('^2015',x) and not re.search('02-29$',x): return True
    else: return False
def choose_min(x):
    if data_15.amin[x] < data.amin[x]: return True
    else: return False
def choose_max(x):
    if data_15.amax[x] > data.amax[x]: return True
    else: return False

newdf = df[df.index.map(choose_day)]
df_15 = df[df.index.map(choose_2015)]

data = newdf.groupby(get_day).agg([np.amin,np.amax])/10
data_15 = df_15.groupby(get_day).agg([np.amin,np.amax])/10

dates = pd.to_datetime(data.index,format='%m-%d')

mindata_15 = data_15.amin[data_15.index.map(choose_min)]
mindata_15.index = pd.to_datetime(mindata_15.index,format='%m-%d')

maxdata_15 = data_15.amax[data_15.index.map(choose_max)]
maxdata_15.index = pd.to_datetime(maxdata_15.index,format='%m-%d')

combodata_15 = pd.concat([mindata_15,maxdata_15])


# In[4]:

plt.figure()
ax = plt.gca()

plt.plot(dates,data.amin,label='_nolegend_')
plt.plot(dates,data.amax,label='_nolegend_',c='r')
plt.scatter(combodata_15.index,combodata_15,c='g',label='Record Broken In 2015')

ax.fill_between(dates,
                  data.amin, data.amax,
                       facecolor='grey',
                       alpha=0.25)
ax.xaxis.set_major_locator(mdates.MonthLocator())
# 16 is a slight approximation since months differ in number of days.
ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=16))

ax.xaxis.set_major_formatter(ticker.NullFormatter())
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))

for tick in ax.xaxis.get_minor_ticks():
    tick.tick1line.set_markersize(0)
    tick.tick2line.set_markersize(0)
    tick.label1.set_horizontalalignment('center')
ax.margins(x=0)
plt.ylabel("Degrees in Celsius")
plt.title('Record High And Low Temperature By Day Of The Year (2005-2014)')
plt.legend(loc=4)
plt.show()


# In[ ]:
