#!/usr/bin/env python
# coding: utf-8

# # ILLEGAL FISHING ANALYSIS 
# ### Cleaning data
# 

# In[1]:


#importing libraries

import pandas as pd
import numpy as np


# In[2]:


#import first csv file

fishdf=pd.read_csv("../data_wrangling/fishvessel_clean.csv")


# In[3]:


#import second csv file

illegaldf=pd.read_csv("../data_wrangling/ts_clean.csv")


# In[4]:


#merging the illegal encounters to analyse

illegal_fish_df=fishdf.merge(illegaldf, left_on='mmsi', right_on='fishing_vessel_mmsi')


# In[5]:


#check

illegal_fish_df.head()


# In[6]:


#creating file

illegal_fish_df.to_csv('../tableau_csv_files/illegal_fullinfo.csv', index=False)


# In[7]:


# index
illegal_fish_df.index


# In[8]:


#check nulls

illegal_fish_df.isna().sum()


# In[9]:


#give a name to nulls since they are categorical data

illegal_fish_df['country_y'] = np.where(illegal_fish_df['country_y'].isna(), "NA", illegal_fish_df['country_y'])


# In[10]:


#check

illegal_fish_df.head()


# In[11]:


#which columns can be dropped already

illegal_fish_df=illegal_fish_df.drop(['flag','iso_3'], axis=1)


# In[12]:


#check 

illegal_fish_df.head()


# In[13]:


#check the types

illegal_fish_df.dtypes


# In[14]:


#extract the date and hour from start time

illegal_fish_df['start_time']=pd.to_datetime(illegal_fish_df['start_time'])

illegal_fish_df['start_month'] = illegal_fish_df['start_time'].dt.month

illegal_fish_df['start_hour'] = illegal_fish_df['start_time'].dt.hour


# In[15]:


#extract the date and hour from end time

illegal_fish_df['end_time']=pd.to_datetime(illegal_fish_df['end_time'])

illegal_fish_df['end_month'] = illegal_fish_df['end_time'].dt.month

illegal_fish_df['end_hour'] = illegal_fish_df['end_time'].dt.hour


# In[16]:


#check types again

illegal_fish_df.dtypes


# In[17]:


#check

illegal_fish_df.head()


# In[18]:


#check columns

illegal_fish_df.columns


# # LINEAR REGRESSION PREPRATION

# In[19]:


#creating copy

lindf=illegal_fish_df.copy()


# In[20]:


#the mmsi data is not relevant for the regression, only in case of blacklisting vessels. not unique either with this set up
#mmsi can be interesting to blacklist a certain mmsi only
# the date/time converted as well
#coordinates as well since country was extracted

todrop=['mmsi','fishing_vessel_mmsi', 'transshipment_vessel_mmsi','start_time', 'end_time','mean_latitude', 'mean_longitude','coordinates']


# In[21]:


#drop data

lindf=lindf.drop(todrop, axis=1)


# In[22]:


#check

lindf.head()


# In[23]:


#checking if it makes sense to bin by month - seasonal fishing

lindf.groupby('start_month').agg({'start_month':'count'})


# In[24]:


#check for bins, quarters are similar to seasons

cut_labels = ['q1','q2','q3','q4']
cut_bins = [0, 3, 6, 9,12]
lindf['seasons'] = pd.cut(lindf['start_month'], bins=cut_bins, labels=cut_labels)


# In[25]:


#confirm

lindf.head()


# In[26]:


#checking if start month and finish month are the same

(lindf['start_month']==lindf['end_month']).value_counts()


# In[27]:


#checking if it makes sense to bin by hour - time fishing

lindf.groupby('start_hour').agg({'start_hour':'count'})


# In[28]:


#change columns name

lindf.columns=['gear_type', 'length', 'tonnage', 'engine_power', 'country','IUU Fishing', 'duration_hr', 'median_distance_km','median_speed_knots', 'country_encounter', 'start_month', 'start_hour','end_month', 'end_hour', 'seasons']


# In[29]:


#check the types

lindf.dtypes


# In[30]:


#import csv to check seaosons

lindf.to_csv('../tableau_csv_files/time_season_illegal.csv', index=False)


# In[31]:


#import ploting and stats lib

import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


# In[32]:


lindf.head()


# In[34]:


#check country flag trends

lindf.groupby('country').agg({'country':'count'}).sort_values


# In[35]:


#check counter encounters trend

lindf.groupby('country_encounter').agg({'country_encounter':'count'})


# # PLOTTING

# In[36]:


#plot checking for trends

fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=lindf,
                x="duration_hr",
                y="IUU Fishing",
                #hue='country',
                legend=False,
                ax=ax);


# In[37]:


#plot checking

fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=lindf,
                x="length",
                y="IUU Fishing",
                hue='country',
                ax=ax);


# In[38]:


#plot checking

fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=lindf,
                x="tonnage",
                y="IUU Fishing",
                hue='country',
                legend=False,
                ax=ax);


# In[39]:


#plot checking

fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=lindf,
                x="gear_type",
                y="IUU Fishing",
                hue='country',
                size='engine_power',
                legend=False,
                ax=ax);


# In[40]:


#plot checking

fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=lindf,
                x="engine_power",
                y="IUU Fishing",
                hue='country',
                legend=False,
                ax=ax);


# In[41]:


#plot checking

fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=lindf,
                x="median_distance_km",
                y="IUU Fishing",
                hue='country',
                legend=False,
                ax=ax);


# In[42]:


#plot checking

fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=lindf,
                x="median_speed_knots",
                y="IUU Fishing",
                hue='country',
                legend=False,
                ax=ax);


# In[43]:


#plot checking

fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=lindf,
                x="country_encounter",
                y="IUU Fishing",
                hue='country',
                legend=False,
                ax=ax);


# In[44]:


#plot checking

fig, ax = plt.subplots(figsize=(10,6))
g = sns.barplot(data=lindf,
                x="seasons",
                y="IUU Fishing",
                hue='country',
                ax=ax);

g.legend_.remove()


# In[45]:


#plot checking

fig, ax = plt.subplots(figsize=(10,6))
g = sns.scatterplot(data=lindf,
                x="start_hour",
                y="IUU Fishing",
                hue='country',
                ax=ax);

g.legend_.remove()


# In[46]:


#plot checking

fig, ax = plt.subplots(figsize=(10,6))
g = sns.scatterplot(data=lindf,
                x="end_hour",
                y="IUU Fishing",
                hue='country',
                ax=ax);

g.legend_.remove()


# In[47]:


lindf.head()


# In[48]:


#check country occurences

encounters=lindf.groupby(['country_encounter']).agg({'country_encounter':'count'})


# In[49]:


encounters['country_enc']=encounters.index


# In[50]:


encounters.columns=['occurences','country_enc']


# In[51]:


encounters['occurences'].sort_values(ascending=False)


# In[52]:


#plot checking

fig, ax = plt.subplots(figsize=(10,6))
g = sns.barplot(data=encounters,
                x="country_enc",
                y="occurences",
                hue='country_enc',
                ax=ax);

g.set(ylim=(0, 600))
g.legend_.remove()
#g.set_xticklabels(g.get_xticklabels(),rotation=45)
plt.setp(ax.get_xticklabels(), rotation=45)


# In[53]:


#check further country analysis with IUU

country_an=lindf.groupby(['country']).agg({'country':'count','IUU Fishing':'mean'})


# In[54]:


country_an.columns=['Country_count','IUU Fishing']


# In[55]:


country_an


# In[56]:


#check for correlation

fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=country_an,
                x="IUU Fishing",
                y="Country_count",
                ax=ax);
ax.set(ylim=(0, 50))


# # BASIC OLS: LINEAR REGRESSION

# In[57]:


lindf.head()


# In[58]:


#create copy

lindf_2=lindf.copy()


# In[59]:


#dummy

dummycountry=pd.get_dummies(lindf_2['country'])
lindf_2 = lindf_2.drop(['country'],axis = 1)
lindf_2 = lindf_2.join(dummycountry)


# In[60]:


lindf_2.columns


# In[61]:


#try regression

lindf_2= sm.add_constant(lindf_2)
ylindf_2 = lindf_2["IUU Fishing"]
Xlindf_2 = lindf_2[["const",'Australia', 'Belize', 'Cambodia', 'Canada','Chile', 'China', 'Colombia', 'Comoros', "Côte d'Ivoire", 'Fiji','Germany', 'Iceland', 'India', 'Iran, Islamic Republic of', 'Japan','Kiribati', 'Korea, Republic of', 'Latvia', 'Lithuania','Micronesia, Federated States of', 'Netherlands', 'Norway', 'Oman','Papua New Guinea', 'Peru', 'Philippines', 'Poland','Russian Federation', 'Saint Kitts and Nevis', 'Seychelles', 'Spain','Taiwan, Province of China', 'Thailand', 'Ukraine', 'United Kingdom','United States', 'Vanuatu']]
reglindf_2 = sm.OLS(ylindf_2, Xlindf_2).fit()

reglindf_2.summary()


# # LINEAR MODEL IUU AND COUNTRY

# In[62]:


lindf_2.head()


# In[63]:


lindf_2.corr()['IUU Fishing']


# In[64]:


#check types to change

lindf_2.dtypes


# In[65]:


#creating copy just in case since the other model was already accurate

total_lindf=lindf_2.copy()


# In[66]:


#getting dummies for all

geardummies=pd.get_dummies(total_lindf['gear_type'])
encounterdummies=pd.get_dummies(total_lindf['country_encounter'], prefix='encounter')
seasondummies=pd.get_dummies(total_lindf['seasons'])


# In[67]:


#dropping before dummies columns

total_lindf = total_lindf.drop(['gear_type','country_encounter','seasons'],axis = 1)


# In[68]:


#join

total_lindf=total_lindf.join(geardummies)
total_lindf=total_lindf.join(encounterdummies)
total_lindf=total_lindf.join(seasondummies)


# In[69]:


#check

total_lindf.head()


# In[70]:


total_lindf.corr()['IUU Fishing'].sort_values(ascending=False)


# In[71]:


total_lindf.columns


# # TRYING TO IMPROVE THE MODEL
# 

# In[72]:


#creating copy

bin_df=lindf.copy()


# In[73]:


#check

bin_df.head()


# In[74]:


#binning length

bin_df['length'].sort_values().tolist()


# In[75]:


#setting conditions looking into the data

conditions = [
    (bin_df['length'] <= 25),
    ((bin_df['length'] > 25) & (bin_df['length'] <= 50)),
    ((bin_df['length'] > 50) & (bin_df['length'] <= 75)),
    ((bin_df['length'] > 75) & (bin_df['length'] <= 100)),
    ((bin_df['length'] > 100) & (bin_df['length'] <= 125)),
    (bin_df['length'] > 125)
]

choices = [
    'very small',
    'small',
    'medium',
    'medium/big',
    'big',
    'huge'
]

bin_df['length'] = np.select(conditions, choices, 'error')


# In[76]:


#confirm

bin_df['length'].value_counts()


# In[77]:


#tonnage conditions

conditions = [
    (bin_df['tonnage'] <= 50),
    ((bin_df['tonnage'] > 50) & (bin_df['tonnage'] <= 100)),
    ((bin_df['tonnage'] > 100) & (bin_df['tonnage'] <= 150)),
    ((bin_df['tonnage'] > 150) & (bin_df['tonnage'] <= 200)),
    ((bin_df['tonnage'] > 250) & (bin_df['tonnage'] <= 300)),
    (bin_df['tonnage'] > 350)
]

choices = [
    'very small',
    'small',
    'medium',
    'medium/big',
    'big',
    'huge'
]

bin_df['tonnage'] = np.select(conditions, choices, 'error')


# In[78]:


#engine power conditions

conditions = [
    (bin_df['engine_power'] <= 200),
    ((bin_df['engine_power'] > 200) & (bin_df['engine_power'] <= 400)),
    ((bin_df['engine_power'] > 400) & (bin_df['engine_power'] <= 600)),
    ((bin_df['engine_power'] > 600) & (bin_df['engine_power'] <= 800)),
    ((bin_df['engine_power'] > 800) & (bin_df['engine_power'] <= 1000)),
    (bin_df['engine_power'] > 1000)
]

choices = [
    'very small',
    'small',
    'medium',
    'medium/big',
    'big',
    'huge'
]

bin_df['engine_power'] = np.select(conditions, choices, 'error')


# In[79]:


#duration conditions

conditions = [
    (bin_df['duration_hr'] <= 2.5),
    ((bin_df['duration_hr'] > 2.5) & (bin_df['duration_hr'] <= 5)),
    ((bin_df['duration_hr'] > 5) & (bin_df['duration_hr'] <= 7.5)),
    ((bin_df['duration_hr'] > 7.5) & (bin_df['duration_hr'] <= 10)),
    ((bin_df['duration_hr'] > 10) & (bin_df['duration_hr'] <= 12.5)),
    (bin_df['duration_hr'] > 12.5)
]

choices = [
    'very small',
    'small',
    'medium',
    'medium/big',
    'big',
    'huge'
]

bin_df['duration_hr'] = np.select(conditions, choices, 'error')



# In[80]:


bin_df.columns


# In[81]:


coltodrop=['median_distance_km','median_speed_knots','start_month', 'start_hour','end_month', 'end_hour']


# In[82]:


bin_df=bin_df.drop(coltodrop, axis=1)
bin_df.head()


# In[83]:


#creating dummies

dfopt=bin_df.copy()

dummygear=pd.get_dummies(dfopt['gear_type'])
dfopt = dfopt.drop(['gear_type'],axis = 1)
dfopt = dfopt.join(dummygear)


# In[84]:


dummylength=pd.get_dummies(dfopt['length'], prefix='length')
dfopt = dfopt.drop(['length'],axis = 1)
dfopt = dfopt.join(dummylength)


# In[85]:


dummytonnage=pd.get_dummies(dfopt['tonnage'], prefix='tonnage')
dfopt = dfopt.drop(['tonnage'],axis = 1)
dfopt = dfopt.join(dummytonnage)


# In[86]:


dummyengine=pd.get_dummies(dfopt['engine_power'], prefix='engine_power')
dfopt = dfopt.drop(['engine_power'],axis = 1)
dfopt = dfopt.join(dummyengine)


# In[87]:


dummycountry=pd.get_dummies(dfopt['country'], prefix='country')
dfopt = dfopt.drop(['country'],axis = 1)
dfopt = dfopt.join(dummycountry)


# In[88]:


dummyduration=pd.get_dummies(dfopt['duration_hr'], prefix='duration_hr')
dfopt = dfopt.drop(['duration_hr'],axis = 1)
dfopt = dfopt.join(dummyduration)


# In[89]:


dummycountry_encounter=pd.get_dummies(dfopt['country_encounter'], prefix='country_encounter')
dfopt = dfopt.drop(['country_encounter'],axis = 1)
dfopt = dfopt.join(dummycountry_encounter)


# In[90]:


dummyseasons=pd.get_dummies(dfopt['seasons'], prefix='seasons')
dfopt = dfopt.drop(['seasons'],axis = 1)
dfopt = dfopt.join(dummyseasons)


# In[91]:


dfopt.head()


# In[92]:


dfopt.columns


# In[93]:


#checking OLS

dfopt1=dfopt.copy()

dfopt1= sm.add_constant(dfopt1)
ydfopt1 = dfopt1["IUU Fishing"]
Xdfopt1 = dfopt1[['const','drifting_longlines', 'fixed_gear', 'other_fishing','purse_seines', 'squid_jigger', 'trawlers', 'length_big', 'length_huge','length_medium', 'length_medium/big', 'length_small','length_very small', 'tonnage_big', 'tonnage_error', 'tonnage_huge','tonnage_medium', 'tonnage_medium/big', 'tonnage_small','tonnage_very small', 'engine_power_big', 'engine_power_huge','engine_power_medium', 'engine_power_medium/big', 'engine_power_small','engine_power_very small', 'country_Australia', 'country_Belize','country_Cambodia', 'country_Canada', 'country_Chile', 'country_China','country_Colombia', 'country_Comoros', "country_Côte d'Ivoire",'country_Fiji', 'country_Germany', 'country_Iceland', 'country_India','country_Iran, Islamic Republic of', 'country_Japan','country_Kiribati', 'country_Korea, Republic of', 'country_Latvia','country_Lithuania', 'country_Micronesia, Federated States of','country_Netherlands', 'country_Norway', 'country_Oman','country_Papua New Guinea', 'country_Peru', 'country_Philippines','country_Poland', 'country_Russian Federation','country_Saint Kitts and Nevis', 'country_Seychelles', 'country_Spain','country_Taiwan, Province of China', 'country_Thailand','country_Ukraine', 'country_United Kingdom', 'country_United States','country_Vanuatu', 'duration_hr_big', 'duration_hr_huge','duration_hr_medium', 'duration_hr_medium/big', 'duration_hr_small','duration_hr_very small', 'country_encounter_Afghanistan','country_encounter_Angola', 'country_encounter_Antarctica','country_encounter_Botswana', 'country_encounter_Brazil','country_encounter_China', "country_encounter_Côte d'Ivoire",'country_encounter_Estonia', 'country_encounter_Greenland','country_encounter_Guinea', 'country_encounter_Guinea-Bissau','country_encounter_Iceland', 'country_encounter_India','country_encounter_Kazakhstan', 'country_encounter_Kyrgyzstan','country_encounter_Liberia', 'country_encounter_Mali','country_encounter_NA', 'country_encounter_Namibia','country_encounter_Oman', 'country_encounter_Pakistan','country_encounter_Senegal', 'country_encounter_Sierra Leone','country_encounter_Sweden', 'country_encounter_Tajikistan', 'country_encounter_Uzbekistan', 'country_encounter_Zambia', 'seasons_q1', 'seasons_q2', 'seasons_q3', 'seasons_q4']]
regdfopt1 = sm.OLS(ydfopt1, Xdfopt1).fit()

regdfopt1.summary()


# # LINEAR REGRESSION

# In[94]:


dfopt1= sm.add_constant(dfopt1)
ydfopt1 = dfopt1["IUU Fishing"]
Xdfopt1 = dfopt1[['const','drifting_longlines', 'fixed_gear', 'other_fishing','purse_seines', 'squid_jigger', 'trawlers', 'length_big', 'length_huge','length_medium', 'length_medium/big', 'length_small','length_very small', 'tonnage_big', 'tonnage_error', 'tonnage_huge','tonnage_medium', 'tonnage_medium/big', 'tonnage_small','tonnage_very small', 'engine_power_big', 'engine_power_huge','engine_power_medium', 'engine_power_medium/big', 'engine_power_small','engine_power_very small','duration_hr_big', 'duration_hr_huge','duration_hr_medium', 'duration_hr_medium/big', 'duration_hr_small','duration_hr_very small', 'country_encounter_Afghanistan','country_encounter_Angola', 'country_encounter_Antarctica','country_encounter_Botswana', 'country_encounter_Brazil','country_encounter_China', "country_encounter_Côte d'Ivoire",'country_encounter_Estonia', 'country_encounter_Greenland','country_encounter_Guinea', 'country_encounter_Guinea-Bissau','country_encounter_Iceland', 'country_encounter_India','country_encounter_Kazakhstan', 'country_encounter_Kyrgyzstan','country_encounter_Liberia', 'country_encounter_Mali','country_encounter_NA', 'country_encounter_Namibia','country_encounter_Oman', 'country_encounter_Pakistan','country_encounter_Senegal', 'country_encounter_Sierra Leone','country_encounter_Sweden', 'country_encounter_Tajikistan', 'country_encounter_Uzbekistan', 'country_encounter_Zambia', 'seasons_q1', 'seasons_q2', 'seasons_q3', 'seasons_q4']]
regdfopt1 = sm.OLS(ydfopt1, Xdfopt1).fit()

regdfopt1.summary()


# In[95]:


dfopt1.corr()['IUU Fishing'].sort_values()


# ## LINEAR REGRESSION WITHOUTH BINNING 

# In[96]:


#check columns

bin_df.columns


# In[97]:


#check

bin_df.head()


# In[98]:


#checking full regression without the country effect

regtotaldf=total_lindf.copy()

regtotaldf.columns


# In[99]:


#checking OLS without bins

yregtotaldf = regtotaldf["IUU Fishing"]
Xregtotaldf = regtotaldf[['const', 'length', 'tonnage', 'engine_power','duration_hr', 'median_distance_km', 'median_speed_knots','start_month', 'start_hour', 'end_month', 'end_hour', 'drifting_longlines', 'fixed_gear', 'other_fishing', 'purse_seines', 'squid_jigger', 'trawlers','encounter_Afghanistan', 'encounter_Angola', 'encounter_Antarctica', 'encounter_Botswana', 'encounter_Brazil', 'encounter_China', "encounter_Côte d'Ivoire", 'encounter_Estonia', 'encounter_Greenland', 'encounter_Guinea', 'encounter_Guinea-Bissau', 'encounter_Iceland', 'encounter_India', 'encounter_Kazakhstan', 'encounter_Kyrgyzstan', 'encounter_Liberia', 'encounter_Mali', 'encounter_NA','encounter_Namibia', 'encounter_Oman', 'encounter_Pakistan','encounter_Senegal', 'encounter_Sierra Leone', 'encounter_Sweden','encounter_Tajikistan', 'encounter_Uzbekistan', 'encounter_Zambia','q1', 'q2', 'q3', 'q4']]
reg_regtotaldf = sm.OLS(yregtotaldf, Xregtotaldf).fit()

reg_regtotaldf.summary()


# In[100]:


#model improvement trial

regtotaldf2=total_lindf.copy()

yregtotaldf2 = regtotaldf2["IUU Fishing"]
Xregtotaldf2 = regtotaldf2[['const', 'start_month']]
reg_regtotaldf2 = sm.OLS(yregtotaldf2, Xregtotaldf2).fit()

reg_regtotaldf2.summary()



# # PROVING IUU ATTEMPT OLS

# In[101]:


#check

lindf.head()


# In[102]:


#check country flag trends

proofdf=lindf.groupby('country').agg({'country':'count','IUU Fishing':'mean'})


# In[103]:


proofdf.columns


# In[104]:


proofdf.columns=['country_illegal_count','IUU Fishing']


# In[105]:


proofdf.head(20)


# In[106]:


proofdf=proofdf.reset_index()


# In[107]:


proofdf.head()


# In[108]:


proofdf=sm.add_constant(proofdf)
yproofdf=proofdf['country_illegal_count']
Xproofdf=proofdf[['const','IUU Fishing']]
regproofdf=sm.OLS(yproofdf,Xproofdf).fit()
regproofdf.summary()


# In[109]:


#plot checking

fig, ax = plt.subplots(figsize=(10,6))
g = sns.scatterplot(data=proofdf,
                x="country_illegal_count",
                y="IUU Fishing",
                hue='country',
                ax=ax);
g.set(xlim=(0, 50))

g.legend_.remove()


# In[110]:


#improving it

descriptive=proofdf.describe().transpose()


# In[111]:


descriptive


# In[112]:


descriptive['IQR'] = descriptive['75%'] - descriptive['25%']
print(descriptive['IQR'])


# In[113]:


outlier25=descriptive['25%']-(1.5*descriptive['IQR'])

outlier75=descriptive['75%']+(1.5*descriptive['IQR'])


# In[114]:


print('outlier25', outlier25)
print('outlier75', outlier75)


# In[115]:


#copy to take outliers into consideation

outdf=proofdf.copy()


# In[116]:


outdf.head()


# In[117]:


outdf.drop(outdf[(outdf['country_illegal_count'] >= 89.5)].index, inplace=True)


# In[118]:


outdf


# In[119]:


youtdf=outdf['IUU Fishing']
Xoutdf=outdf[['const','country_illegal_count']]
regoutdf=sm.OLS(youtdf,Xoutdf).fit()
regoutdf.summary()


# In[120]:


outdf2=proofdf.copy()


# In[121]:


outdf2.drop(outdf2[(outdf2['country_illegal_count'] <= 89.5)].index, inplace=True)


# In[122]:


youtdf2=outdf2['IUU Fishing']
Xoutdf2=outdf2[['const','country_illegal_count']]
regoutdf2=sm.OLS(youtdf2,Xoutdf2).fit()
regoutdf2.summary()


# In[123]:


#check smaller cases from plot

outdf3=proofdf.copy()


# In[124]:


outdf3.drop(outdf3[(outdf3['country_illegal_count'] >=60 )].index, inplace=True)


# In[125]:


youtdf3=outdf3['IUU Fishing']
Xoutdf3=outdf3[['const','country_illegal_count']]
regoutdf3=sm.OLS(youtdf3,Xoutdf3).fit()
regoutdf3.summary()


# # ML LINEAR REGRESSION TRIAL (ALL FEATURES)

# In[127]:


import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split


# In[128]:


#check for nulls
total_lindf.isna().sum().tolist()


# In[129]:


#create copy

mlreg_df=total_lindf.copy()
mlreg_df=mlreg_df.drop('const', axis=1)


# In[130]:


#create train set

train, test = train_test_split(mlreg_df, test_size=.25, random_state=42)


# In[131]:


mlreg_df.columns


# In[132]:


target_col = ["IUU Fishing"]
num_cols = ['length', 'tonnage', 'engine_power', 'IUU Fishing', 'duration_hr','median_distance_km', 'median_speed_knots', 'start_month', 'start_hour','end_month', 'end_hour']
bool_cols = ['Australia', 'Belize', 'Cambodia', 'Canada','Chile', 'China', 'Colombia', 'Comoros', "Côte d'Ivoire", 'Fiji','Germany', 'Iceland', 'India', 'Iran, Islamic Republic of', 'Japan','Kiribati', 'Korea, Republic of', 'Latvia', 'Lithuania','Micronesia, Federated States of', 'Netherlands', 'Norway', 'Oman','Papua New Guinea', 'Peru', 'Philippines', 'Poland','Russian Federation', 'Saint Kitts and Nevis', 'Seychelles', 'Spain','Taiwan, Province of China', 'Thailand', 'Ukraine', 'United Kingdom','United States', 'Vanuatu', 'drifting_longlines', 'fixed_gear','other_fishing', 'purse_seines', 'squid_jigger', 'trawlers','encounter_Afghanistan', 'encounter_Angola', 'encounter_Antarctica','encounter_Botswana', 'encounter_Brazil', 'encounter_China',"encounter_Côte d'Ivoire", 'encounter_Estonia', 'encounter_Greenland','encounter_Guinea', 'encounter_Guinea-Bissau', 'encounter_Iceland','encounter_India', 'encounter_Kazakhstan', 'encounter_Kyrgyzstan','encounter_Liberia', 'encounter_Mali', 'encounter_NA','encounter_Namibia', 'encounter_Oman', 'encounter_Pakistan','encounter_Senegal', 'encounter_Sierra Leone', 'encounter_Sweden','encounter_Tajikistan', 'encounter_Uzbekistan', 'encounter_Zambia','q1', 'q2', 'q3', 'q4']


# In[133]:


mlreg_df['IUU Fishing'].value_counts(normalize=True)


# In[134]:


import sklearn

from sklearn.linear_model import LinearRegression
from sklearn.metrics import balanced_accuracy_score


# In[135]:


train_X = train[num_cols + bool_cols]
train_y = train[target_col]
test_X = test[num_cols + bool_cols]
test_y = test[target_col]


# In[136]:


test_y.shape


# In[137]:


#linear regression

lr = LinearRegression().fit(train_X, train_y)


# In[138]:


predictions = lr.predict(test_X)


# In[139]:


test_X.shape


# In[140]:


mlreg_df.shape


# In[141]:


predictions.shape


# In[142]:


predictions


# In[143]:


test_y


# In[146]:


lr.coef_


# # CHINA CASE

# In[147]:


china_df=bin_df.copy()


# In[148]:


china_df.columns


# In[149]:


china_df=china_df.loc[china_df["country"] == 'China']


# In[150]:


china_df.head()


# In[151]:


#checking trends with plot: gear_type

gearp = dict(china_df['gear_type'].value_counts())
names = list(gearp.keys())
values = list(gearp.values())

fig, ax = plt.subplots(figsize=(10,6))
ax.bar(names,values)


# In[152]:


#create function for the plots

def plot(variable):
    gearp = dict(china_df[variable].value_counts())
    names = list(gearp.keys())
    values = list(gearp.values())
    fig, ax = plt.subplots(figsize=(10,6))
    ax.bar(names,values)


# In[153]:


plot('country_encounter')


# In[154]:


china_df['gear_type'].value_counts()


# In[155]:


china_df['duration_hr'].value_counts()


# In[156]:


china_df['duration_hr'].sort_values().tolist()


# # PREDICTING ILLEGAL FISHING 
# ### DATA CLEANING

# In[157]:


#importing libraries

import pandas as pd
import numpy as np


# In[158]:


#import first csv file

fishdf=pd.read_csv("../data_wrangling/fishvessel_clean.csv")


# In[159]:


#check

fishdf.head()


# In[160]:


#check index

fishdf.index


# In[161]:


#import second csv file

illegaldf=pd.read_csv("../data_wrangling/ts_clean.csv")


# In[162]:


#check data gathered

illegaldf.index


# In[163]:


#check

illegaldf.head()


# In[164]:


#change country columns name before merge

illegaldf.columns=['fishing_vessel_mmsi', 'transshipment_vessel_mmsi', 'start_time','end_time', 'mean_latitude', 'mean_longitude', 'duration_hr','median_distance_km', 'median_speed_knots', 'coordinates', 'country_encounter','iso_3']


# In[165]:


#check

illegaldf.head()


# # MERGE

# In[166]:


#goal is a left join to introduce a binary column. checking if the mmsi matches between the two df
# it will be relevant later for illegal fishing analysis

trialfish_df=fishdf.merge(illegaldf, left_on='mmsi', right_on='fishing_vessel_mmsi')


# In[167]:


trialfish_df.index


# In[168]:


trialfish_df.head()


# In[169]:


#merge desired

finalfish_df=fishdf.merge(illegaldf, how= 'left',left_on='mmsi', right_on='fishing_vessel_mmsi')


# In[170]:


#check

finalfish_df.head()


# In[171]:


#check if it works

finalfish_df.groupby(['fishing_vessel_mmsi']).agg({'fishing_vessel_mmsi':'count'})


# In[172]:


# not many matches - as expected, number of illegal fishing should have been lower


# In[173]:


#adding column with binary information
# 1 means there is an illegal fishing match
#0 that illegal activity hasn´t been spotted 

finalfish_df['illegal_fishing'] = np.where(finalfish_df['fishing_vessel_mmsi'].isna(), 0, 1)


# In[174]:


#check df

finalfish_df.head()


# In[175]:


#check size

finalfish_df.index


# In[176]:


#check if it works

finalfish_df.groupby(['illegal_fishing']).agg({'illegal_fishing':'count'})


# # DATA PREP

# In[177]:


#check nulls

finalfish_df.isna().sum()


# In[178]:


#checking if the some nulls are relevant
#creating copy first

illegal_df=finalfish_df.copy()
illegal_df.loc[illegal_df['gear_type'].isna()]


# In[179]:


illegal_df=illegal_df.dropna(subset=['gear_type'])


# In[180]:


illegal_df.head()


# In[181]:


illegal_df.isna().sum()


# In[183]:


#check remaining nulls

illegal_df.loc[illegal_df['length'].isna()]


# In[184]:


illegal_df.loc[illegal_df['tonnage'].isna()]


# In[185]:


illegal_df.loc[illegal_df['engine_power'].isna()]


# In[186]:


#decided to drop them

illegal_df=illegal_df.dropna(subset=['engine_power'])


# In[187]:


#check

illegal_df.isna().sum()


# In[188]:


#check columns to drop

columns_drop=['fishing_vessel_mmsi','transshipment_vessel_mmsi', 'start_time', 'end_time', 'mean_latitude','mean_longitude', 'duration_hr', 'median_distance_km','median_speed_knots', 'coordinates', 'country_encounter', 'iso_3']


# In[189]:


#new df

model_df=illegal_df.drop(columns_drop, axis=1)


# In[190]:


#check

model_df.head()


# In[191]:


model_df.index


# In[192]:


model_df.nunique()


# In[193]:


model_df.columns


# In[194]:


#droping mmsi duplicates, existing because of the merge and different times

new_modeldf=model_df.copy()

new_modeldf=new_modeldf.drop_duplicates(subset=['mmsi'])


# In[195]:


#new_modeldf=model_df.groupby(['mmsi','flag', 'gear_type', 'length', 'tonnage', 'engine_power','country', 'IUU Fishing', 'illegal_fishing'], as_index=False).count()


# In[196]:


#check

new_modeldf.head()


# In[197]:


# check if it matches the its unique 

new_modeldf.index


# In[198]:


#check for uniques again

new_modeldf.nunique()


# In[199]:


#flag and country redundant

new_modeldf=new_modeldf.drop(['flag'], axis=1)


# In[200]:


#check

new_modeldf.head()


# # DATA CHECK AND FEATURES

# In[201]:


#check types

new_modeldf.dtypes


# In[202]:


#final check

new_modeldf.nunique()


# In[203]:


new_modeldf.head()


# In[204]:


#checking the model on csv file

new_modeldf.to_csv('../tableau_csv_files/binary_info.csv', index=False)


# # FURTHER DATA PROCESSING

# In[205]:


#create dummies for categorical data
#first for gear type

new_modeldf = new_modeldf.merge(pd.get_dummies(new_modeldf["gear_type"], drop_first=True, prefix="gear_type"), 
         left_index=True, 
         right_index=True)


# In[206]:


new_modeldf.head()


# In[207]:


new_modeldf.groupby(['gear_type','illegal_fishing']).agg({'illegal_fishing': 'count'})


# In[208]:


#second for countries

dummycountry=pd.get_dummies(new_modeldf['country'])

new_modeldf = new_modeldf.join(dummycountry)


# In[209]:


#drop unnecessary columns, now in dummies

new_modeldf = new_modeldf.drop(['gear_type','country'],axis = 1)


# In[210]:


#check

new_modeldf.head()


# In[211]:


new_modeldf.index


# # MACHINE LEARNING 
# ## LOGISTIC REGRESSION

# In[212]:


# import sklearn

from sklearn.model_selection import train_test_split


# In[213]:


# set up split

train, test = train_test_split(new_modeldf, test_size=.25, random_state=42)


# In[214]:


#check columns

new_modeldf.columns.tolist()


# In[215]:


#columns by category

id_col=['mmsi']
target_col=['illegal_fishing']
bool_col=[ 'gear_type_fixed_gear','gear_type_other_fishing','gear_type_purse_seines','gear_type_squid_jigger','gear_type_trawlers','Albania','Algeria','Angola','Argentina','Australia','Bahrain','Belgium','Belize','Brazil','Bulgaria','Cambodia','Cameroon','Canada','Cape Verde','Chile','China','Colombia','Comoros','Cook Islands','Costa Rica','Croatia','Cuba','Cyprus',"Côte d'Ivoire",'Denmark','Dominica','Ecuador','El Salvador','Equatorial Guinea','Estonia','Fiji','Finland','France','Germany','Ghana','Greece','Guatemala','Honduras','Iceland','India','Indonesia','Iran, Islamic Republic of','Ireland','Israel','Italy','Japan','Kiribati','Korea, Republic of','Latvia','Liberia','Libya','Lithuania','Malaysia','Maldives','Malta','Marshall Islands','Mauritania','Mauritius','Mexico','Micronesia, Federated States of','Montenegro','Morocco','Mozambique','Namibia','Netherlands','New Zealand','Nicaragua','Norway','Oman','Panama','Papua New Guinea','Peru','Philippines','Poland','Portugal','Qatar','Romania','Russian Federation','Saint Kitts and Nevis','Saint Vincent and the Grenadines','Sao Tome and Principe','Saudi Arabia','Senegal','Seychelles','Singapore','Slovenia','Solomon Islands','South Africa', 'Spain','Sri Lanka','Sweden','Taiwan, Province of China','Tanzania, United Republic of','Thailand','Tonga','Turkey','Ukraine','United Kingdom','United States','Uruguay','Vanuatu','Vietnam']
num_col=['length','tonnage','engine_power','IUU Fishing']


# In[216]:


#normalization

new_modeldf["illegal_fishing"].value_counts(normalize=True)


# In[217]:


#chek logistic regression

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score


# In[218]:


train_X = train[num_col + bool_col]
train_y = train[target_col]
test_X = test[num_col + bool_col]
test_y = test[target_col]


# In[219]:


train_y["illegal_fishing"]


# In[220]:


type(train_y.values.ravel())


# In[221]:


lr = LogisticRegression()
lr.fit(train_X, train_y.values.ravel())


# In[222]:


predictions = lr.predict(test_X)


# In[223]:


#prediction

predictions


# In[224]:


predictions.shape


# In[225]:


pred_df=pd.DataFrame(data=predictions)

pred_df.value_counts()


# In[226]:


#expected

test_y


# In[227]:


test_y.value_counts()


# In[228]:


#check accuracy

balanced_accuracy_score(test_y, predictions)


# # # CROSS VALIDATION

# In[229]:


import warnings
warnings.filterwarnings('ignore')


# In[230]:


from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate


# In[231]:


models = {"Logistic Regression": LogisticRegression(),
          "Decision Tree": DecisionTreeClassifier(random_state=42),
          "Random Forest": RandomForestClassifier(random_state = 1, n_estimators=1000, n_jobs=-1)}


# In[232]:


def validate_model(model):
    validation_results = cross_validate(model,
                                        train_X,
                                        train_y.values.ravel(), 
                                        cv=10,
                                        scoring="balanced_accuracy")
    acc = validation_results["test_score"].mean()
    print(f"Mean Balanced Accuracy Score: {acc}")


# In[233]:


for key, value in models.items():
    print(f"Model: {key}")
    validate_model(value)
    print("\n")


# # MODEL IMPROVEMENT INTRODUCING BINS

# In[234]:


#copy

bin_df=new_modeldf.copy()


# In[235]:


#check head

bin_df.head()


# In[236]:


#setting conditions looking into the data

conditions = [
    (bin_df['length'] <= 25),
    ((bin_df['length'] > 25) & (bin_df['length'] <= 50)),
    ((bin_df['length'] > 50) & (bin_df['length'] <= 75)),
    ((bin_df['length'] > 75) & (bin_df['length'] <= 100)),
    ((bin_df['length'] > 100) & (bin_df['length'] <= 125)),
    (bin_df['length'] > 125)
]

choices = [
    'very small',
    'small',
    'medium',
    'medium/big',
    'big',
    'huge'
]

bin_df['length'] = np.select(conditions, choices, 'error')


# In[237]:


#confirm

bin_df['length'].value_counts()


# In[238]:


#tonnage conditions

conditions = [
    (bin_df['tonnage'] <= 50),
    ((bin_df['tonnage'] > 50) & (bin_df['tonnage'] <= 100)),
    ((bin_df['tonnage'] > 100) & (bin_df['tonnage'] <= 150)),
    ((bin_df['tonnage'] > 150) & (bin_df['tonnage'] <= 200)),
    ((bin_df['tonnage'] > 250) & (bin_df['tonnage'] <= 300)),
    (bin_df['tonnage'] > 350)
]

choices = [
    'very small',
    'small',
    'medium',
    'medium/big',
    'big',
    'huge'
]

bin_df['tonnage'] = np.select(conditions, choices, 'error')


# In[239]:


#engine power conditions

conditions = [
    (bin_df['engine_power'] <= 200),
    ((bin_df['engine_power'] > 200) & (bin_df['engine_power'] <= 400)),
    ((bin_df['engine_power'] > 400) & (bin_df['engine_power'] <= 600)),
    ((bin_df['engine_power'] > 600) & (bin_df['engine_power'] <= 800)),
    ((bin_df['engine_power'] > 800) & (bin_df['engine_power'] <= 1000)),
    (bin_df['engine_power'] > 1000)
]

choices = [
    'very small',
    'small',
    'medium',
    'medium/big',
    'big',
    'huge'
]

bin_df['engine_power'] = np.select(conditions, choices, 'error')


# In[240]:


bin_df.head()


# In[241]:


#creating dummies

dfopt=bin_df.copy()


# In[242]:


dummylength=pd.get_dummies(dfopt['length'], prefix='length')
dfopt = dfopt.drop(['length'],axis = 1)
dfopt = dfopt.join(dummylength)


# In[243]:


dummytonnage=pd.get_dummies(dfopt['tonnage'], prefix='tonnage')
dfopt = dfopt.drop(['tonnage'],axis = 1)
dfopt = dfopt.join(dummytonnage)


# In[244]:


dummyengine=pd.get_dummies(dfopt['engine_power'], prefix='engine_power')
dfopt = dfopt.drop(['engine_power'],axis = 1)
dfopt = dfopt.join(dummyengine)


# In[245]:


dfopt.head()


# # SPLIT TRAINING AND TEST- SECOND ATTEMPT

# In[246]:


# set up split

train, test = train_test_split(dfopt, test_size=.25, random_state=42)


# In[247]:


dfopt.columns.tolist()


# In[248]:


#columns by category

id_col=['mmsi']
target_col=['illegal_fishing']
bool_col=['gear_type_fixed_gear','gear_type_other_fishing','gear_type_purse_seines','gear_type_squid_jigger','gear_type_trawlers','Albania','Algeria','Angola','Argentina','Australia','Bahrain','Belgium','Belize','Brazil','Bulgaria','Cambodia','Cameroon','Canada','Cape Verde','Chile','China','Colombia','Comoros','Cook Islands','Costa Rica','Croatia','Cuba','Cyprus',"Côte d'Ivoire",'Denmark','Dominica','Ecuador','El Salvador','Equatorial Guinea','Estonia','Fiji','Finland','France','Germany','Ghana','Greece','Guatemala','Honduras','Iceland','India','Indonesia','Iran, Islamic Republic of','Ireland','Israel','Italy','Japan','Kiribati','Korea, Republic of','Latvia','Liberia','Libya','Lithuania','Malaysia','Maldives','Malta','Marshall Islands','Mauritania','Mauritius','Mexico','Micronesia, Federated States of','Montenegro','Morocco','Mozambique','Namibia','Netherlands','New Zealand','Nicaragua','Norway','Oman','Panama','Papua New Guinea','Peru','Philippines','Poland','Portugal','Qatar','Romania','Russian Federation','Saint Kitts and Nevis','Saint Vincent and the Grenadines','Sao Tome and Principe','Saudi Arabia','Senegal','Seychelles','Singapore','Slovenia','Solomon Islands','South Africa','Spain','Sri Lanka','Sweden','Taiwan, Province of China','Tanzania, United Republic of','Thailand','Tonga','Turkey','Ukraine','United Kingdom','United States','Uruguay','Vanuatu','Vietnam','length_big','length_huge','length_medium','length_medium/big','length_small','length_very small','tonnage_big','tonnage_error','tonnage_huge','tonnage_medium','tonnage_medium/big','tonnage_small','tonnage_very small','engine_power_big','engine_power_huge','engine_power_medium','engine_power_medium/big','engine_power_small','engine_power_very small']
num_col=['IUU Fishing']


# In[249]:


#chek logistic regression

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score


# In[250]:


#normalization

dfopt["illegal_fishing"].value_counts(normalize=True)


# In[251]:


train_X = train[num_col + bool_col]
train_y = train[target_col]
test_X = test[num_col + bool_col]
test_y = test[target_col]


# In[252]:


lr = LogisticRegression()
lr.fit(train_X, train_y.values.ravel())


# In[253]:


predictions = lr.predict(test_X)


# In[254]:


balanced_accuracy_score(test_y, predictions)


# In[255]:


from sklearn.metrics import classification_report
print(classification_report(test_y, predictions))


# # RANDOM FOREST (BEST MODEL) 

# In[256]:


#check random forest

rf=RandomForestClassifier(random_state = 1,n_estimators=1000, n_jobs=-1)
rf.fit(train_X, train_y.values.ravel())


# In[257]:


predictions = rf.predict(test_X)
balanced_accuracy_score(test_y, predictions)


# In[258]:


predictions


# In[259]:


test_X


# In[260]:


print(classification_report(test_y, predictions))


# In[261]:


for key, value in models.items():
    print(f"Model: {key}")
    validate_model(value)
    print("\n")
    


# In[262]:


#check just another additional models
#svm

from sklearn import svm
clf = svm.SVC()
clf.fit(train_X, train_y.values.ravel())


# In[263]:


predictions = clf.predict(test_X)


# In[264]:


balanced_accuracy_score(test_y, predictions)


# In[265]:


#checking also gradient boosting classifier

from sklearn.datasets import make_classification
from sklearn.ensemble import GradientBoostingClassifier


# In[266]:


clf = GradientBoostingClassifier(random_state=0)
clf.fit(train_X, train_y.values.ravel())


# In[267]:


predictions = clf.predict(test_X)


# In[268]:


balanced_accuracy_score(test_y, predictions)


# In[269]:


print(classification_report(test_y, predictions))


# # SQUID JIGGER ANALYSIS: HIGH ILLEGAL FISHING RATE 

# In[270]:


#copy 

squiddf=dfopt.copy()


# In[271]:


squiddf.head()


# In[272]:


squiddf=squiddf.loc[squiddf['gear_type_squid_jigger']==1]


# In[273]:


squiddf=squiddf.drop(['gear_type_fixed_gear','gear_type_other_fishing','gear_type_purse_seines','gear_type_trawlers'], axis=1)


# In[274]:


squiddf.head()


# In[275]:


# set up split

train, test = train_test_split(squiddf, test_size=.25, random_state=42)


# In[276]:


#columns by category

id_col=['mmsi']
target_col=['illegal_fishing']
bool_col=['Albania','Algeria','Angola','Argentina','Australia','Bahrain','Belgium','Belize','Brazil','Bulgaria','Cambodia','Cameroon','Canada','Cape Verde','Chile','China','Colombia','Comoros','Cook Islands','Costa Rica','Croatia','Cuba','Cyprus',"Côte d'Ivoire",'Denmark','Dominica','Ecuador','El Salvador','Equatorial Guinea','Estonia','Fiji','Finland','France','Germany','Ghana','Greece','Guatemala','Honduras','Iceland','India','Indonesia','Iran, Islamic Republic of','Ireland','Israel','Italy','Japan','Kiribati','Korea, Republic of','Latvia','Liberia','Libya','Lithuania','Malaysia','Maldives','Malta','Marshall Islands','Mauritania','Mauritius','Mexico','Micronesia, Federated States of','Montenegro','Morocco','Mozambique','Namibia','Netherlands','New Zealand','Nicaragua','Norway','Oman','Panama','Papua New Guinea','Peru','Philippines','Poland','Portugal','Qatar','Romania','Russian Federation','Saint Kitts and Nevis','Saint Vincent and the Grenadines','Sao Tome and Principe','Saudi Arabia','Senegal','Seychelles','Singapore','Slovenia','Solomon Islands','South Africa','Spain','Sri Lanka','Sweden','Taiwan, Province of China','Tanzania, United Republic of','Thailand','Tonga','Turkey','Ukraine','United Kingdom','United States','Uruguay','Vanuatu','Vietnam','length_big','length_huge','length_medium','length_medium/big','length_small','length_very small','tonnage_big','tonnage_error','tonnage_huge','tonnage_medium','tonnage_medium/big','tonnage_small','tonnage_very small','engine_power_big','engine_power_huge','engine_power_medium','engine_power_medium/big','engine_power_small','engine_power_very small']
num_col=['IUU Fishing']


# In[277]:


#normalization

squiddf["illegal_fishing"].value_counts(normalize=True)


# In[278]:


train_X = train[num_col + bool_col]
train_y = train[target_col]
test_X = test[num_col + bool_col]
test_y = test[target_col]


# In[279]:


rf=RandomForestClassifier(random_state = 1,n_estimators=100, n_jobs=-1)
rf.fit(train_X, train_y.values.ravel())


# In[280]:


predictions = rf.predict(test_X)


# In[281]:


balanced_accuracy_score(test_y, predictions)


# # CHINA ANALYSIS: HIGH ILLEGAL FISHING RATE

# In[282]:


#copy 

chinadf=dfopt.copy()


# In[283]:


chinadf=chinadf.loc[chinadf['China']==1]


# In[284]:


chinadf.index


# In[285]:


chinadf.columns.tolist()


# In[286]:


drops=['IUU Fishing','Albania','Algeria','Angola','Argentina','Australia','Bahrain','Belgium','Belize','Brazil','Bulgaria','Cambodia','Cameroon','Canada','Cape Verde','Chile','China','Colombia','Comoros','Cook Islands','Costa Rica','Croatia','Cuba','Cyprus',"Côte d'Ivoire",'Denmark','Dominica','Ecuador','El Salvador','Equatorial Guinea','Estonia','Fiji','Finland','France','Germany','Ghana','Greece','Guatemala','Honduras','Iceland','India','Indonesia','Iran, Islamic Republic of','Ireland','Israel','Italy','Japan','Kiribati','Korea, Republic of','Latvia','Liberia','Libya','Lithuania','Malaysia','Maldives','Malta','Marshall Islands','Mauritania','Mauritius','Mexico','Micronesia, Federated States of','Montenegro','Morocco','Mozambique','Namibia','Netherlands','New Zealand','Nicaragua','Norway','Oman','Panama','Papua New Guinea','Peru','Philippines','Poland','Portugal','Qatar','Romania','Russian Federation','Saint Kitts and Nevis','Saint Vincent and the Grenadines','Sao Tome and Principe','Saudi Arabia','Senegal','Seychelles','Singapore','Slovenia','Solomon Islands','South Africa','Spain','Sri Lanka','Sweden','Taiwan, Province of China','Tanzania, United Republic of','Thailand','Tonga','Turkey','Ukraine','United Kingdom','United States','Uruguay','Vanuatu','Vietnam']


# In[287]:


chinadf=chinadf.drop(drops, axis=1)


# In[288]:


# set up split

train, test = train_test_split(chinadf, test_size=.25, random_state=42)


# In[289]:


chinadf.columns


# In[290]:


#columns by category

id_col=['mmsi']
target_col=['illegal_fishing']
bool_col=['gear_type_fixed_gear','gear_type_other_fishing', 'gear_type_purse_seines','gear_type_squid_jigger', 'gear_type_trawlers', 'length_big','length_huge', 'length_medium', 'length_medium/big', 'length_small','length_very small', 'tonnage_big', 'tonnage_error', 'tonnage_huge','tonnage_medium', 'tonnage_medium/big', 'tonnage_small','tonnage_very small', 'engine_power_big', 'engine_power_huge','engine_power_medium', 'engine_power_medium/big', 'engine_power_small','engine_power_very small']


# In[291]:


#normalization

chinadf["illegal_fishing"].value_counts(normalize=True)


# In[292]:


train_X = train[bool_col]
train_y = train[target_col]
test_X = test[bool_col]
test_y = test[target_col]


# In[293]:


rf=RandomForestClassifier(random_state = 1,n_estimators=10, n_jobs=-1)
rf.fit(train_X, train_y.values.ravel())


# In[294]:


predictions = rf.predict(test_X)


# In[295]:


balanced_accuracy_score(test_y, predictions)


# In[296]:


#checking logistic as well

lr = LogisticRegression()


# In[297]:


lr.fit(train_X, train_y.values.ravel())


# In[298]:


predictions = lr.predict(test_X)


# In[299]:


balanced_accuracy_score(test_y, predictions)


# # BLACKLIST MODEL

# # WHAT COUNTRIES WITH SIMILIAR BEHAVIOUR SHALL WE AVOID

# ### DATA CLEANING

# In[300]:


#importing libraries

import pandas as pd
import numpy as np


# In[301]:


#import first csv file

fishdf=pd.read_csv("../data_wrangling/fishvessel_clean.csv")


# In[302]:


#import second csv file

illegaldf=pd.read_csv("../data_wrangling/ts_clean.csv")


# In[303]:


#check first file

fishdf.head()


# In[304]:


#check second first

illegaldf.head()


# In[305]:


#merging the illegal encounters to analyse

fishillegaldf=fishdf.merge(illegaldf, left_on='mmsi', right_on='fishing_vessel_mmsi')


# In[306]:


#check dataframe

fishillegaldf.head()


# In[307]:


#add a new columns for unique if: combination vessel mmsi and transshipment mmsi

fishillegaldf['id_encounter'] = fishillegaldf.index


# In[308]:


#check

fishillegaldf.head()


# In[309]:


#check columns

fishillegaldf.columns


# In[310]:


#check index

fishillegaldf.index


# In[311]:


#columns to drop

columns_drop=['mmsi', 'flag', 'gear_type', 'length', 'tonnage', 'engine_power','fishing_vessel_mmsi','transshipment_vessel_mmsi', 'start_time', 'end_time', 'mean_latitude','mean_longitude', 'duration_hr', 'median_distance_km','median_speed_knots', 'coordinates', 'country_y', 'iso_3']


# In[312]:


#dropping columns

fishillegaldf=fishillegaldf.drop(columns_drop, axis=1)


# In[313]:


#check

fishillegaldf.head()


# In[314]:


#renaming columns

fishillegaldf=fishillegaldf.rename(columns={'country_x':'country'})


# In[315]:


#checking the number of occurrences by country

nr_occurrences=(fishillegaldf.groupby('country').agg({'country':'count'})
                     .rename(columns={'country':"nr_occurrences"})
                     .reset_index())


# In[316]:


#check

nr_occurrences.head()


# In[317]:


#checking the destribuition of data

nr_occurrences.describe()


# In[318]:


#preparing a dataframe for the matrix

totaldf = fishillegaldf.merge(nr_occurrences, how="left", on="country")


# In[319]:


#giving labels to the country in order to use it for the matrix

labels, levels = pd.factorize(totaldf['country'])


# In[320]:


#check the labels

labels


# In[321]:


#create new column with the country labels

totaldf['country_id']=labels


# In[322]:


#check if correct

totaldf


# # # MACHINE LEARNING PREPRATION

# In[323]:


#looking at the data, decided some countries had very little amount of occurences to be considered into the model

totaldf2 = totaldf[totaldf["nr_occurrences"] >= 7].copy()


# In[324]:


#prepare pivot table

features = totaldf2.pivot_table(index="country_id",
                    columns="id_encounter",
                    values="IUU Fishing")


# In[325]:


#check pivot table

features


# In[326]:


#fill nulls with zero to model the matrix

features=features.fillna(0)


# In[327]:


#confirm

features.head()


# In[328]:


#import more libraries

import matplotlib.pyplot as plt
import seaborn as sns
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

get_ipython().run_line_magic('matplotlib', 'inline')


# In[329]:


country_features = csr_matrix(features)


# In[330]:


#train the model


# In[331]:


model_knn = NearestNeighbors(metric="cosine",
                             algorithm="brute",
                             n_jobs=-1)
model_knn.fit(country_features)


# In[332]:


#check matrix

country_features


# In[333]:


#understanding features set up

features.head(20)


# In[334]:


#understanding datafram set up

totaldf2.groupby('country').agg({'country':'count'})


# In[335]:


#check how the index is working

features.loc[2].values.reshape(1, -1)


# In[336]:


#1st cosine
#2nd index of the country similar
#note: second array based on the row position

model_knn.kneighbors(features.loc[2].values.reshape(1, -1), n_neighbors=5)


# In[337]:


#set up to check other countries

def country_choice(country):
    return model_knn.kneighbors(features.loc[country].values.reshape(1, -1), n_neighbors=5)


# In[338]:


#call the country wished
#the inserted number is the country_id, not the index according to the outcome

country_choice(4)


# In[339]:


#confirming it

features.loc[4]


# In[340]:


#understanding the country_id set up

totaldf.groupby(["country", "country_id"]).count()


# # MACHINE LEARNING MODEL USER FRIENDLY

# In[341]:


#creating a data frame to take the right country_id and match with the index

newc_list=totaldf2.groupby('country', as_index=False).agg({'country_id':'mean'}).sort_values(by='country_id', ascending=True)
newc_list


# In[342]:


# taking the indeces

distances, indeces = model_knn.kneighbors(features.loc[4].values.reshape(1, -1), n_neighbors=5)




# In[343]:


#confirming indeces

indeces


# In[344]:


#check df

totaldf2.head()


# In[345]:


j = 0
for i in indeces.flatten():
    country = newc_list.iloc[i, 0]
    if j == 0:
        print("BLACKLIST")
        print(f"Countries with similar behaviour to {country}")
        print("\n")
    else:
        print(f"{j}: {country}")
    j += 1


# In[ ]:




