# In[]: Import the libraries
import sqlite3
import json
import urllib3
import requests
from sqlalchemy.types import Unicode
import pandas as pd
import pyodbc 
from datetime import datetime  
from datetime import timedelta  
import configparser
import urllib.parse
import http
import http.cookiejar
from dateutil.relativedelta import relativedelta
import sys


#Main class
class Exchange_Rate:
    
    base="EUR"
    base_url="http://data.fixer.io/api/"
    
    def __init__(self):
        # Initialize the class object with the access_key stored in the config file
        try:
            config=configparser.RawConfigParser()
            config.read("Config.ini")
            self.access_key = config.get("file","access_key")
        except :
            print("Failed to initialise the class object, Configuration file/access key not found")
            sys.exit(1)
            

    
    def Download_latestExchangeRates(self):
        #Standard url is the combination of base_url,keyword,access_key and base
        self.url=self.base_url+"latest?"+urllib.parse.urlencode({'access_key': self.access_key,'base': self.base})
        conn_url= requests.get(self.url)

        # Data downloaded from the API is stored in a variable
        json_data=conn_url.content
        data=json.loads(json_data)

        #Current_datetime        
        current_date=datetime.now()

        # Load the data retrieved from the API into a dataframe.
        latestrates=pd.DataFrame(columns=["base_code","date","rate","currency_code"])
        for key,value in data["rates"].items():
            latestrates=latestrates.append({"base_code":self.base,"date":current_date.date(),"rate":value,"currency_code":key}, ignore_index=True)

        # Return the dataframe
        return latestrates
        


    
    def Download_historicalExchangeRates(self,start_date,end_date):
       # self.url=self.base_url+"timeseries?"+urllib.parse.urlencode({'access_key': self.access_key,'start_date': start_date,'end_date': end_date})
       # Convert parameters into date format
        self.date1=datetime.strptime(start_date, '%Y-%m-%d')
        
        
        self.date2=datetime.strptime(end_date, '%Y-%m-%d')
        day = timedelta(days=1)
        historicalrates=pd.DataFrame(columns=["base_code","date","rate","currency_code"])

        #Call the API iteratively from start date to the end_date ( This is being used since timeseries endpoint is not supported for
        #FREE users)
        
        while self.date1 <= self.date2:
            self.url=self.base_url+str(self.date1.date())+"?"+urllib.parse.urlencode({'access_key': self.access_key})
            conn_url= requests.get(self.url)
            jd=conn_url.content
            data=json.loads(jd)
            #Append each data into the pandas dataframe
            for key,value in data["rates"].items():               
                historicalrates=historicalrates.append({"base_code":self.base,"date":self.date1,"rate":value,"currency_code":key}, ignore_index=True)
                
            self.date1 = self.date1 + day

        # Return the dataframe    
        return historicalrates
    

    # Load the dataframe into the datawarehouse
    def LoadintoDWH(self,rate):
        # Connect to the database and load the data from pandas into the dwh
        try:
            db=sqlite3.connect(':memory:')
            self.rate=rate
            self.rate.to_sql("EXCH_Rates",db, if_exists="replace") # replace is used only when to replace the existing data from the db
            db.commit()
            print("Data is inserted into DWH")
            
            #cursor3 = db.cursor()
            #cursor3.execute('''SELECT * FROM EXCH_Rates''')
            #all_rows = cursor3.fetchall()
            #for row in all_rows:
             #   print('{0} , {1}, {2},{3}'.format(row[0], row[1], row[2],row[3]))
            #db.commit()
            db.close()
        except:
            print("Data is Couldn't be loaded into DWH")
    
    

    def Calculate_Average(self,start_date,end_date,currency):
        #Calculate the average for a given currency in the specified date range
        #Download the data for the specified range using the previous function Download_historicalExchangeRates and store it in a dataframe
        #ave_rate is calculated for the given currency using groupby method of the pandas 
        hist_data=self.Download_historicalExchangeRates(start_date,end_date)
        ave_rate=hist_data[hist_data["currency_code"]==currency].groupby("currency_code").mean()
        print("Average exchange rate for the currency",currency,"against",self.base,"for the specidifed date  rangeis",ave_rate["rate"][0] )
        
        
    
        

def main():
    exch=Exchange_Rate()
    exch.base="EUR"
    latest=exch.Download_latestExchangeRates()  # Downloads the latest exchange rates into "latest"
    print(latest)
    exch.LoadintoDWH(latest)


    end_date=datetime.now()
    start_date=end_date-timedelta(days=2)  #end_date-relativedelta(years=2)

    date1=str(start_date.date())
    date2=str(end_date.date())
    historical=exch.Download_historicalExchangeRates(date1,date2)  # download historical exchangerates for any given specific dates
    print(historical)


    dateA="2018-07-01"
    dateB="2018-07-02"
    currency_code="INR"
    exch.Calculate_Average(dateA,dateB,currency_code) # Calculate the average of the currency code between dateA and dateB
    
  


if __name__ == '__main__':
    main()
