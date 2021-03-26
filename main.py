import pandas as pd
import numpy as np
from function import *

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 8000)  # 最多显示数据的行数

momentum_days = 8  # 计算多少天的动量


if __name__ == "__main__":
    # 读取数据
    data1_path = '../trading-data/indexdata/sh000300.csv'
    data1_res_path = './csv/sh000300.csv'
    data1 = pd.read_csv(data1_path, encoding='gbk', parse_dates=['date'])
    data1 = data1.sort_values(by = 'date')
    '''
    data2_path = '../trading-data/indexdata/sh000905.csv'
    data2_res_path = './csv/sh000905.csv'
    data2 = pd.read_csv(data2_path, encoding='gbk', parse_dates=['date'])
    data2 = data2.sort_values(by = 'date')
    '''
    #生成周K线、BBI、MACD
    data1 = get_more_data(data1,data1_res_path)