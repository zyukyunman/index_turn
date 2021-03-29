import pandas as pd
import os
import talib as tal
'''
计算出日线的其他数据如MACD等
计算出周线、月线的所有数据
'''
def produce_week_stockdata(file_name,day_data_path,week_data_path):
    '''
    判断带生成的文件是否存在，若存在读取数据增量生成数据（检查行检查列）
    '''
    file_path = day_data_path + '/' + file_name
    df = pd.read_csv(file_path, encoding='gbk', parse_dates=['date'])
    df = df.sort_values(by = 'date')

    '''
    生成基础数据
    '''

    '''
    通过Talib生成更多数据
    '''
    return 0

def produce_week_indexdata(file_name,day_data_path,week_data_path):
    return 0

def produce_month_stockdata(file_name,day_data_path,month_data_path):
    #print(day_data_path+"/"+file_name)
    #print(month_data_path+"/"+file_name)
    return 0

def produce_month_indexdata(file_name,day_data_path,month_data_path):
    return 0

def produce_datas():
    day_data_path = '../data/trading_data_day/'
    week_data_path = '../data/trading_data_week/'
    month_data_path = '../data/trading_data_month/'
    data_type = ['indexdata','stockdata']
    for x in data_type:
        day_path = day_data_path + x
        week_path = week_data_path + x
        month_path = month_data_path + x
        if(x == 'indexdata'):
            day_data_list = os.listdir(day_path)
            for file_name in day_data_list:
                produce_week_indexdata(file_name,day_path,week_path)
                produce_month_indexdata(file_name,day_path,month_path)
        else:
            day_data_list = os.listdir(day_path)
            for file_name in day_data_list:
                produce_week_stockdata(file_name,day_path,week_path)
                produce_month_stockdata(file_name,day_path,month_path)
    return 0