ABOUT:

In this project, I applied statistical and machine learning models to predict the Return on Investment (ROI) of stocks from companies in the S&P 500 index. The program is designed for swing traders who may want to consider the next day's predicted ROI from multiple models. 

FILES:

- testing.ipynb: Contains a detailed explanation of how I came up with the final configurations for each model to optimize their performance.
- product.ipynb: Contains the code that can be executed on a daily basis to predict the ROI for the next day, for all companies in the index and using multiple models. It retrieves the tickers for the companies in the S&P 500 index through Wikipedia's [List of S&P 500 companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) updated on a daily basis, and later uses the yfinance API to retrieve the historical stock prices for each company. It returns a csv file with the ROI predictions, with the models as columns and the companies as rows. 
