# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MRaaKnjwUmqCBGtZU1N2fmD8AvdCpLTp
"""

import numpy as np
import pandas as pd
import re

# Vizualization Packages
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.basemap import Basemap

import sqlalchemy
import pymysql
from sqlalchemy import create_engine
import mysql.connector

# import sys
# sys.path.append(r'C:\Users\Rae-Djamaal\Anaconda3\Lib\Git_Uploads\chameleon_project_phase1_Final\Phase_1')

# User Defined Modules
from SQL_Mods.sql_mods import MySQL_Operations

"""**Load OOS Coordinates from MySQL**"""

# Call the instance MySQL Class
db_call_1 = MySQL_Operations('enter_your_user','enter_your_password','enter_your_host','enter_your_database')

# check the engine
print(db_call_1.Engine_Connection()[0])

# check the connection
print(db_call_1.Database_Connection()[0])

# get the connection object
connection = db_call_1.Database_Connection()[1]

# Create the cursor
cursor = connection.cursor(prepared=True)


# get the engine object
engine = db_call_1.Database_Connection()[1]

# Select the Out of service Service company coordinates table
OOS_Coords = pd.read_sql('SELECT * FROM oos_company_coordinates', con=engine)

# Select the Out Of Service carriers table(with name,address information etc.)
OOS_Carriers = pd.read_sql('SELECT * FROM out_of_service_carriers', con=engine)

# close cursor
cursor.close()

# # Merge both dataframes so we have all information for the IS Companies
# IS_Merged = pd.merge(IS_Carrier_Names,IS_Coords, on = ['USDOT'], how = 'inner')
# IS_Merged.shape

OOS_Coords.shape

OOS_Carriers.shape

def format_and_dtypes(df)
  """
  Format columns to necessary dtypes
  and drop duplicates
  """
  # Set necessary variable types
  df['USDOT'] = df['USDOT'].astype(int)
  df['LEGAL_NAME'] = df['LEGAL_NAME'].astype(str)
  df = df.sort_index()
  # Drop duplicates
  df.drop_duplicates(keep=False,inplace=True) 
  return df

# Apply to oos coords
OOS_Coords = format_and_dtypes(OOS_Coords)
# Apply to is carriers
OOS_Carriers = format_and_dtypes(OOS_Carriers)

# Rename columns for oos_carriers
OOS_Carriers.rename(columns={ 'usdot':'USDOT', 'legal_name':"LEGAL_NAME", 'dba_name':"DBA_NAME",'zip_code':
                         'ZIP_CODE','state':'STATE', 'city':'CITY','street':'STREET', 'oos_reason':
                         'OOS_REASON', 'oos_date':'OOS_DATE', 'oos_status':'OOS_STATUS'}, inplace=True)

# Full outer join based on matching 'USDOT','LEGAL_NAME', 'DBA_NAME', 'STATE'
Oos_Merge = pd.merge(OOS_Coords, OOS_Carriers, on = ['USDOT','LEGAL_NAME','DBA_NAME','STATE'], how = 'inner')
Oos_Merge.shape

# Create new engine object
engine1 = create_engine('mysql+mysqlconnector://enter_your_user:enter_your_password@enter_your_host/enter_your_database')
# Save the IS_Merged to MySQL Server
Cl_OS_Carr_Df.to_sql('OOS_Geocord_With_Address', engine1, if_exists='replace', index=False)