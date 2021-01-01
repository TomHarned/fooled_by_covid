import importlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import update_data
import datetime
import fbc_utils

pd.set_option('display.max_columns', None)
sns.set(rc={'figure.figsize':(11, 4)})
importlib.reload(update_data)
importlib.reload(fbc_utils)

updated = update_data.check_updated()
if not updated:
    update_data.replace_live_file()

# don't keep reading this one -- it's rude to constantly hit their site
# update_data.replace_live_file()
df = fbc_utils.read_data()


df_nums = fbc_utils.calc_daily_metrics(df)

filter_expr = (df_nums['state'] == "Connecticut")
groupby_vars = ['date', 'state']

df_ct = df_nums\
            .loc[filter_expr, :]\
            .groupby(groupby_vars)\
            .sum()\
            .reset_index()\
            .set_index('date')

df_ct['daily_cases'].plot()
plt.show()

data_cols = ['daily_cases', 'daily_deaths']
rolling_cols = ['daily_cases_7d_roll', 'daily_deaths_7d_roll']

df_ct[rolling_cols] = df_ct[data_cols].rolling(7, center=True).mean()

df_ct

pd.re
# TODO

# Create lagging 2 week metrics
## Look at the pandas book for time series

## Incorporate the metric calcs into the daily update script

## Total Case Count
## Total active cases (rolling two weeks??)
# daily new cases
# daily new deaths

# rolling 14 avg new daily cases
# change in rolling 14 day avg over the prior two week period


# TODO 3 - get population data from censes, and get new cases per 100 pop

# TODO 4 - move all this to a mysql DB

# TODO 5 - move this whole thing to aws
