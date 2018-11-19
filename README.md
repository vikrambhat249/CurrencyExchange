# CurrencyExchange
This code is used to connect to fixer.io api, Download the currency exchange rates as keeping EUR as base currency. It also provides functions to download the historical data for any date and the average conversion date between 2 dates.

The class Exchange_Rate objects are initialised by the credentials mentioned in the config files.

1. The function Download_latestExchangeRates() downloads the latest exchange rates for the given Base currency.
2. The function Download_historicalExchangeRates(start_date,end_date) downloads the historical exchange rates between two specified dates and stores in a dataframe.
3. LoadintoDWH(rate) loads the data into datawarehouse(sqllite in this case)
4. The Function Calculate_Average(self,start_date,end_date,currency) is used to calculate the average exchange rate for the currency between the specified dates.


When the code is executed, 
1. It displays the latest exchange rates for all the currencies against EURO and loads the data into the data warehouse on Sqllite. 
2. It displays the historical data of last two days and loads the data into the data warehouse on Sqllite. Here last two days are considered just to display them on the screen. The process remains the same for any date range. 
3. It calculates the average currency rate of a specified currency for specified time range. EUR is used as base currency for these calculations which can also be changed. 
 
I have subscribed for a free fixer account with my username and password. In order to avoid sharing the username and password, I have included the access_key in the configuration file. This access_key is used to authenticate the account in the code. My fixer account is a free account which comes with few limitations. One of which was downloading the data from the APIs with date range endpoints. So in order to download the data from the api between two dates I had to call the API multiple times by specifying the date and iterate through data. 
