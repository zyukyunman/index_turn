import pandas as pd
import talib
import numpy as np

def get_more_data(dataFrame,path):
    #日线MA20、20日动量变化率、MACD三个指标参数
    dataFrame['day_MA20'] = talib.MA(dataFrame['close'],20)
    dataFrame['day_20_mompercent'] = dataFrame['close'].pct_change(periods=20)
    dataFrame['day_MACD'],dataFrame['day_MACDsignal'],dataFrame['day_MACDhist'] = talib.MACD(dataFrame['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    return dataFrame

def evaluate_investment(source_data, tittle,time='交易日期'):
    temp = source_data.copy()
    # ===新建一个dataframe保存回测指标
    results = pd.DataFrame()

    # ===计算累积净值
    results.loc[0, '累积净值'] = round(temp[tittle].iloc[-1], 2)

    # ===计算年化收益
    annual_return = (temp[tittle].iloc[-1]) ** (
            '1 days 00:00:00' / (temp[time].iloc[-1] - temp[time].iloc[0]) * 365) - 1
    results.loc[0, '年化收益'] = str(round(annual_return * 100, 2)) + '%'

    # ===计算最大回撤，最大回撤的含义：《如何通过3行代码计算最大回撤》https://mp.weixin.qq.com/s/Dwt4lkKR_PEnWRprLlvPVw
    # 计算当日之前的资金曲线的最高点
    temp['max2here'] = temp[tittle].expanding().max()
    # 计算到历史最高值到当日的跌幅，drowdwon
    temp['dd2here'] = temp[tittle] / temp['max2here'] - 1
    # 计算最大回撤，以及最大回撤结束时间
    end_date, max_draw_down = tuple(temp.sort_values(by=['dd2here']).iloc[0][[time, 'dd2here']])
    # 计算最大回撤开始时间
    start_date = temp[temp[time] <= end_date].sort_values(by=tittle, ascending=False).iloc[0][
        time]
    # 将无关的变量删除
    temp.drop(['max2here', 'dd2here'], axis=1, inplace=True)
    results.loc[0, '最大回撤'] = format(max_draw_down, '.2%')
    results.loc[0, '最大回撤开始时间'] = str(start_date)
    results.loc[0, '最大回撤结束时间'] = str(end_date)

    # ===年化收益/回撤比：我个人比较关注的一个指标
    results.loc[0, '年化收益/回撤比'] = round(annual_return / abs(max_draw_down), 2)

    return results.T
