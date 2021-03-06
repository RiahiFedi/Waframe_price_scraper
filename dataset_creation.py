from urllib.request import urlopen as req_url
import json
import string
import webbrowser
import pandas as pd
import time


def warframe(search):

    main_url = req_url('https://api.warframe.market/v1/items/' + search + '/orders')
    data = main_url.read()
    parsed = json.loads(data)
    if len(parsed['payload']['orders'])>0:
        parsed_data = list([parsed['payload']['orders'][i]['platinum'],
                            parsed['payload']['orders'][i]['user']['status'],
                            parsed['payload']['orders'][i]['quantity']
                            ] for i in range(len(parsed['payload']['orders'])))
        temp_ = []
        for j in range(len(parsed_data)):
            if parsed_data[j][1]!='offline':
                temp_.append(parsed_data[j])
        if len(temp_)>0:
            minimal_price_ = min(list(temp_[k][0] for k in range(len(temp_)))) 
            status = 'Online'
            t_ = list(temp_[k][0] for k in range(len(temp_)))
            quantity = temp_[t_.index(minimal_price_)][2]
        else:
            minimal_price_ = min(list(parsed_data[p][0] for p in range(len(parsed_data))))
            status = 'Offline'
            #minimal_price_ = min(list(parsed['payload']['orders'][i]['platinum'] for i in range(len(parsed['payload']['orders']))))    
            t_ = list(parsed_data[p][2] for p in range(len(parsed_data)))
            #t_ = list(list(parsed['payload']['orders'][i]['quantity'] for i in range(len(parsed['payload']['orders']))))
            quantity = t_[list(parsed_data[p][0] for p in range(len(parsed_data))).index(minimal_price_)]
        #date_time = parsed['payload']['orders'][-1]['last_update']
    else:
        minimal_price_ = '0'
        status = 'Not found'
        quantity = '0'
        
    return minimal_price_, status, quantity

def gen_data(update=True):
    main_url = req_url('https://api.warframe.market/v1/items')
    data = main_url.read()
    parsed = json.loads(data)
    parsed_data = parsed['payload']['items']
    if update:
        df = pd.DataFrame(parsed_data)
        df = df.drop(['id','thumb'], axis =1)
        df.to_excel('Item_data.xlsx')
    else:
        df = pd.read_excel('Item_data.xlsx')
        for i in range(len(parsed_data)):
            d_temp={}
            if not(parsed_data[i]['url_name'] in df['url_name'].tolist()):
                d_temp['url_name'] = parsed_data[i]['url_name']
                d_temp['item_name'] = parsed_data[i]['item_name']
                print(d_temp)
                df_temp = pd.DataFrame(d_temp, index=[len(parsed_data)])
                df= df.append(df_temp)
        df.info()
        df.to_excel('Item_data.xlsx')


def prices(update = True):
    df = pd.read_excel('Item_data.xlsx')
    prices_ = []
    mode_ = []
    for i in range(len(df['url_name'].tolist())):
        time.sleep(0.4)
        price_temp, status, quantity = warframe(df['url_name'].tolist()[i])
        prices_.append(price_temp)
        #last_update.append(date_temp)
        print(df['url_name'].tolist()[i])
        print('price: ' + str(price_temp) + " nbr: "+ str(i) )
        #print(date_temp)
    df['prices'] =prices_
    df['Mode'] = status
    df['Quantity'] = quantity
    df.info()
    df.to_excel('Item_data.xlsx')
    
gen_data()
prices()
