import update_data
import importlib

importlib.reload(update_data)

updated = update_data.check_updated()

# don't keep reading this one -- it's rude to constantly hit their site
# update_data.replace_live_file()

df = update_data.read_data()


# TODO

# Create daily metrics
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
