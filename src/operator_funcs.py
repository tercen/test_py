# ADD Func here for tests
from tercen.client import context as ctx
import numpy as np


def calc_mean(ctx):
    df = ctx.select(['.y', '.ci', '.ri'], df_lib="pandas")
    df = df.groupby(['.ci','.ri']).mean().rename(columns={".y":"mean"}).reset_index(inplace=False)
    # NOTE Ungrouping (reset_index) in pandas converts .ci and .ri to int64, which fails during saving, so we need to convert them back
    
    df = df.astype({".ci":np.int32, ".ri":np.int32})
    return df
    



