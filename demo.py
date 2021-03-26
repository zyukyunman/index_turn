import pandas as pd
import numpy as np
from function import *
import matplotlib.pyplot as plt

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 8000)  # 最多显示数据的行数
start_date = '2021/03/02'
end_date = '2020/03/02'

# 读取数据
df_big = pd.read_csv('./csv/sh000300.csv', encoding='gbk', parse_dates=['date'])
df_small = pd.read_csv('./csv/sh000905.csv', encoding='gbk', parse_dates=['date'])

# 设置参数
trade_rate = 0.6 / 10000  # 场内基金万分之0.6，买卖手续费相同，无印花税
momentum_days = 20  # 计算多少天的动量
# 重命名行
df_big.rename(columns={'open': 'big_open', 'close': 'big_close','change':'big_change'}, inplace=True)
df_small.rename(columns={'open': 'small_open', 'close': 'small_close','change':'small_change'}, inplace=True)
# 合并数据
df = pd.merge(left=df_big[['date', 'big_open', 'big_close', 'big_change']], left_on=['date'],
              right=df_small[['date', 'small_open', 'small_close', 'small_change']],
              right_on=['date'], how='left')
df = df.dropna()
df.dropna(subset=['big_change', 'small_change'])#去除有空值的行
#df['date'] = pd.to_datetime(df['date'])
#df = df.set_index('date') # 将date设置为index
df = df.sort_values(by = 'date')
#df.drop(df.head(3800).index,inplace=True) # 从头去掉n行


# 计算N日的动量momentum
df['big_mom'] = df['big_close'].pct_change(periods=momentum_days)
df['small_mom'] = df['small_close'].pct_change(periods=momentum_days)
# 风格变换条件
df.loc[df['big_mom'] > df['small_mom'], 'style'] = 'big'
df.loc[df['big_mom'] < df['small_mom'], 'style'] = 'small'
#df.loc[(df['big_mom'] < 0) & (df['small_mom'] < 0), 'style'] = 'empty'
# 相等时维持原来的仓位。
df['style'].fillna(method='ffill', inplace=True)
# 收盘才能确定风格，实际的持仓pos要晚一天。
df['pos'] = df['style'].shift(1)
# 删除持仓为nan的天数（创业板2010年才有）
df.dropna(subset=['pos'], inplace=True)
# 计算策略的整体涨跌幅strategy_amp
df.loc[df['pos'] == 'big', 'strategy_amp'] = df['big_change']
df.loc[df['pos'] == 'small', 'strategy_amp'] = df['small_change']
df.loc[df['pos'] == 'empty', 'strategy_amp'] = 0
df['strategy_amp'][2] = 0

# 调仓时间
df.loc[df['pos'] != df['pos'].shift(1), 'trade_time'] = df['date']
# 将调仓日的涨跌幅修正为开盘价买入涨跌幅（并算上交易费用，没有取整数100手，所以略有误差）
df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'big'), 'strategy_amp_adjust'] = df['big_close'] / (
        df['big_open'] * (1 + trade_rate)) - 1
df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'small'), 'strategy_amp_adjust'] = df['small_close'] / (
        df['small_open'] * (1 + trade_rate)) - 1
df.loc[df['trade_time'].isnull(), 'strategy_amp_adjust'] = df['strategy_amp']
# 扣除卖出手续费
df.loc[(df['trade_time'].shift(-1) .notnull()) & (df['pos'] != 'empty'), 'strategy_amp_adjust'] = (1 + df[
    'strategy_amp']) * (1 - trade_rate) - 1
# 空仓的日子，涨跌幅用0填充
df['strategy_amp_adjust'].fillna(value=0.0, inplace=True)
del df['strategy_amp'], df['style']

df.reset_index(drop=True, inplace=True)
# 计算净值
df['big_net'] = df['big_close'] / df['big_close'][0]
df['small_net'] = df['small_close'] / df['small_close'][0]
df['strategy_net'] = (1 + df['strategy_amp_adjust']).cumprod()

# 评估策略的好坏
res = evaluate_investment(df, 'strategy_net', time='date')
print(res)

# 绘制图片
plt.plot(df['date'], df['strategy_net'], label='strategy')
plt.plot(df['date'], df['big_net'], label='big_net')
plt.plot(df['date'], df['small_net'], label='small_net')
plt.show()
# 保存文件
print(df.tail(10))
df.to_csv('./csv/demo.csv', encoding='gbk', index=False)
