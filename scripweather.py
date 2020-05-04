import requests
from wwo_hist import retrieve_hist_data
frequency = 24
start_date = '1-JAN-2018'
end_date = '1-MAR-2018'
api_key = '12b2c18a34194a8ca93113127200405'
location_list = ['poland']
hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)
