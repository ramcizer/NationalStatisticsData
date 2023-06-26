import pandas as pd
import numpy as np
import re

# Filter all warnings. If you would like to see the warnings, please comment the two lines below.
import warnings
warnings.filterwarnings('ignore')

def answer_one():

    Energy = pd.read_excel('assets/Energy Indicators.xls', index_col=None, header=None, skiprows=18)

    Energy.drop(Energy.columns[[0, 1]], axis = 1, inplace=True)

    # Another way to drop rows
    # Required the drop here otherwise added a second layer of index
    # Energy = Energy[18:245].reset_index(drop=True)


    # Another way to rename
    Energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

    # Energy.rename(columns={1: 'Country', 2: 'Energy Supply'}, inplace=True)
    Energy["Energy Supply"] = Energy["Energy Supply"].replace({"...": np.nan}).apply(lambda x: x*1000000)
    # Energy['Energy Supply'] = 1000000 * Energy['Energy Supply']
    Energy['Country'] = Energy['Country'].replace({"Republic of Korea": "South Korea", "United States of America20": "United States", "United Kingdom of Great Britain and Northern Ireland19": "United Kingdom", "China, Hong Kong Special Administrative Region": "Hong Kong", "Japan10": "Japan", "France6": "France", "China2": "China", "Italy9": "Italy", "Spain16": "Spain", "Iran (Islamic Republic of)": "Iran", "Australia1": "Australia"})

    # A Regex for anything within a bracket. 
    # "." matches any character but a newline. 
    # the "\" indicates the start of see: https://docs.python.org/3/library/re.html#re.MULTILINE
    Energy['Country'] = Energy['Country'].str.replace(r" \(.*\)","")
    Energy = Energy.set_index('Country')

    GDP = pd.read_csv('assets/world_bank.csv', index_col=None, skiprows=4)
    GDP['Country Name'] = GDP['Country Name'].replace({"Korea, Rep.": "South Korea",  "Iran, Islamic Rep.": "Iran", "Hong Kong SAR, China": "Hong Kong"})
    GDP.rename(columns={'Country Name':'Country'}, inplace=True)
    GDP = GDP[['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
    GDP = GDP.set_index('Country')

    ScimEn = pd.read_excel('assets/scimagojr-3.xlsx')
    ScimEn = ScimEn.set_index('Country')

    # new_pd = Energy.merge(GDP, on='Country').merge(ScimEn, on='Country')

    # The following worked but created a problem of it not being a dataframe. 
    new_pd = ScimEn.merge(Energy, on='Country').merge(GDP, on='Country')
    # new_pd = pd.DataFrame.merge(ScimEn, Energy, on='Country').merge(GDP, on='Country')
    new_pd = new_pd[0:15]
    new_pd = pd.DataFrame(new_pd)

    return new_pd

def answer_two():
    Energy = pd.read_excel('assets/Energy Indicators.xls', index_col=None, header=None, skiprows=18)
    print(len(Energy))
    GDP = pd.read_csv('assets/world_bank.csv', index_col=None, skiprows=4)
    print(len(GDP))
    ScimEn = pd.read_excel('assets/scimagojr-3.xlsx')
    print(len(ScimEn))

    return len(Energy) - len(ScimEn)
   

def answer_three():
    new_pd = answer_one()
    avgGDP = new_pd[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].mean(axis=1).sort_values(ascending=False)
    avgGDP = pd.Series(avgGDP)
    return avgGDP

def answer_four():
    new_pd = answer_one()
    key = answer_three().index[5]
    GDP_change = new_pd.loc[key, '2015'] - new_pd.loc[key, '2006']
    return GDP_change    
    
def answer_five(): 
    new_pd = answer_one()
    mean_energy = new_pd['Energy Supply per Capita'].mean()
    return mean_energy

def answer_six():
    new_pd = answer_one()
    top_renewable = new_pd['% Renewable'].max()
    country = new_pd.index[new_pd['% Renewable'] == top_renewable].item()

    return (country, top_renewable)

def answer_seven(): 
    new_pd = answer_one()
    new_pd['Cit ratio'] = new_pd['Self-citations'] / new_pd['Citations']
    top_ratio = new_pd['Cit ratio'].max()
    cit_country = new_pd.index[new_pd['Cit ratio'] == top_ratio].item()

    return (cit_country, top_ratio)

def answer_eight(): 
    new_pd = answer_one()
    new_pd['Pop Estimate'] = new_pd['Energy Supply'] / new_pd['Energy Supply per Capita']
    
    # most_pop = new_pd['Pop Estimate'].max()
    # most_pop_country = new_pd.index[new_pd['Pop Estimate'] == most_pop].item()
    avgs_pd = new_pd.sort_values(by="Pop Estimate", ascending=False)
    print(avgs_pd)
   
    return avgs_pd.index[2]

def answer_nine(): 
    new_pd = answer_one()
    new_pd['Pop Estimate'] = new_pd['Energy Supply'] / new_pd['Energy Supply per Capita']
    new_pd['Citable docs per capita'] = new_pd['Citable documents'] / new_pd['Pop Estimate']
    return new_pd[['Citable docs per capita', 'Energy Supply per Capita']].corr(method='pearson').iloc[0,1]

# What I wrote before Chat GPT solved
# Error was: "TypeError: 'numpy.float64' object does not support item assignment"
# def answer_ten():
#     renew_median = new_pd['% Renewable'].median()
#     new_pd['High Renew'] = None
#     for i in new_pd['% Renewable'].values:
#         if i > renew_median:
#             new_pd['High Renew'] = 1
#         else:
#             i['High Renew'] = 0

#     return pd.Series(new_pd['High Renew'])


def answer_ten():
    new_pd = answer_one()
    renew_median = new_pd['% Renewable'].median()
    new_pd['High Renew'] = 0 
    new_pd.loc[new_pd['% Renewable'] >= renew_median, 'High Renew'] = 1  
    return pd.Series(new_pd['High Renew'])

                     
def answer_eleven(): 
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
    new_pd['Pop Estimate'] = new_pd['Energy Supply'] / new_pd['Energy Supply per Capita']
    new_pd["Pop Estimate"] = pd.to_numeric(new_pd["Pop Estimate"])  
    new_grid = new_pd  
    new_grid["Continent"] = new_pd.index.map(ContinentDict)
    new_grid = new_pd.groupby("Continent")['Pop Estimate'].agg([len, np.sum, np.mean, np.std])
    new_grid = new_grid.rename(columns={'len': 'size'})

    return new_grid

def answer_twelve(): 

    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    new_pd = answer_one()
    new_grid = new_pd
    new_grid = new_grid.reset_index()  
    new_grid["Continent"] = new_pd.index.map(ContinentDict)
    new_grid['bins'] = pd.cut(new_grid['% Renewable'], 5)
    new_grid = new_grid.groupby(['Continent', 'bins']).size()
    # new_grid = new_grid.groupby(['Continent', 'bins']).agg({"Continent": pd.Series.nunique})
    # new_grid = new_grid["Continent"].dropna()

    return pd.Series(new_grid)

def answer_thirteen(): 
    new_pd = answer_one()
    new_pd['Pop Estimate'] = new_pd['Energy Supply'] / new_pd['Energy Supply per Capita']
    new_pd['Pop Estimate'] = new_pd['Pop Estimate'].apply(lambda num: f"{num:,}")

    return new_pd['Pop Estimate']
