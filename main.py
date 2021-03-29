import pandas as pd
import numpy as np
import data_producer

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 8000)  # 最多显示数据的行数

if __name__ == "__main__":
    # 检查数据完整性以及生成数据
    data_producer.produce_datas()