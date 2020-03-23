
# coding: utf-8

# In[4]:

## Import relevant libraries
import pandas as pd
from geopy.distance import geodesic ## Will be used to calculate distance

## Import data
## Data was crawled from the website www.nynjt.org
raw_data = pd.read_csv("hiking.csv")


# In[5]:

## Preprocessing steps
## Remove "\n" and "mile" from text
data = raw_data.applymap(lambda x: x.replace('\n', '')
                         .replace(' miles','')
                         .replace('            ','')
                         .replace('          ',''))

## Split geography coordinate into latitude and longitude
data['latitude'], data['longitude'] = data['geography'].str.split(',', 1).str
data = data.drop(['geography'], axis = 1)

## Convert distance, latitude and longitude into numerics
data[['latitude','longitude','length']]=data[['latitude','longitude','length']].apply(pd.to_numeric)

## Check missing values
data.isnull().sum()


# In[6]:

## Enriching dataset


# In[7]:

## Rank "difficulty" of hikes
## Step 1: List of unique values for the column "difficulty"
data.difficulty.unique()


# In[8]:

## Step 2
data['level'] = data['difficulty'].map({'Easy':1,'Easy to Moderate':2,
                 'Moderate':3,'Moderate to Strenuous':4,
                 'Strenuous':5,'Very Strenuous':6})


# In[9]:

## Find latitude and longitude of address
from geopy.geocoders import Nominatim
our_home = Nominatim()
location = our_home.geocode("66 N 6th street Brooklyn") ## Use generic address in Williamsburg
print(location.address)
print((location.latitude, location.longitude))


# In[10]:

## Calculate the distance between generic address and each hike
for index, row in data.iterrows():
    start = (location.latitude, location.longitude)
    destination = (row['latitude'],row['longitude'])
    data.loc[index,'distance in miles']=(geodesic(start,destination).miles)


# In[11]:

## View data
data.head()


# In[12]:

data.to_csv('final_dataset.csv',index=False)


# In[ ]:



