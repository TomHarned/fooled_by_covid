
NYT_DATA_LIVE = ('https://raw.githubusercontent.com/nytimes/covid-19-data'
            + '/master/live/us-counties.csv')

NYT_DATA_ALL = ('https://raw.githubusercontent.com'
                + '/nytimes/covid-19-data/master/us-counties.csv')

NYT_DATA_FILE = '../data/nyt_covid_data_base.csv'
NYT_BACKUP_FILE = '../data/nyt_covid_data_base_backup.csv'

DATA_TYPES = {'date': 'str',
              'county': 'str',
              'state': 'str',
              'fips': 'str',
              'cases': 'float',
              'deaths': 'float'
              }

PARSE_DATES = ['date']
