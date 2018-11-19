# CurrencyExchange
This code is used to connect to fixer.io api, Download the currency exchange rates as keeping EUR as base currency. It also provides functions to download the historical data for any date and the average conversion date between 2 dates.

The class Exchange_Rate objects are initialised by the credentials mentioned in the config files.

1. The function Download_latestExchangeRates() downloads the latest exchange rates for the given Base currency.
2. The function Download_historicalExchangeRates(start_date,end_date) downloads the historical exchange rates between two specified dates and stores in a dataframe.
3. LoadintoDWH(rate) loads the data into datawarehouse(sqllite in this case)
4. The Function Calculate_Average(self,start_date,end_date,currency) is used to calculate the average exchange rate for the currency between the specified dates.


