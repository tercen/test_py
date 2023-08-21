from tercen.client import context as ctx
import numpy as np

tercenCtx = ctx.TercenContext()

df = (
    tercenCtx
    .select(['.y', '.ci', '.ri'], df_lib="pandas")
    .groupby(['.ci','.ri'])
    .mean()
    .rename({".y":"mean"})
)

df = tercenCtx.add_namespace(df) 
tercenCtx.save(df)
