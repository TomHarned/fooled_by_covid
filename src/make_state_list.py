#!/usr/bin/env ipython
import pandas as pd
import pickle

df_states = pd.read_csv('../data/nyt_covid_data_base.csv')

states = sorted(df_states.state.unique())

states = [{'label': x, 'value': x} for x in states]

with open('../data/states.txt', 'wb') as f:
    pickle.dump(states, f)
