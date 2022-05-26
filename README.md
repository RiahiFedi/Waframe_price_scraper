# Waframe_price_scraper
Price scraper that used the Warframe Market API

If you wanna use it just run the file dataset_creation.py. 
There are two main functions:
1) data_gen () will create a .xlsx file that has all the items listed on Warframe Market. You can also use your own spreadsheet if you just want to track specific items. Just make sure it's in the same format. I would recommend creating one using he function then to delete anything you don't need.

2) prices() this function will check the items listed in the Item_data.xlsx file and add two columns
  - Prices: is the price in platinum
  - Mode: Is the status of the trade the price was taken from. The algorithm will prioritize getting the lowest price from the currently online users. If it can't find anyone online that is offering that item it will just grab the lowest price from the offline listings. I was thinking about adding some optimization so it does not get anything too old but i got cba out of it. So, feel free to add whatever version you like :)
