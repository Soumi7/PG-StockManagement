import numpy as np
import datetime as dt
import pandas as pd


date=input("enter date")
date=pd.to_datetime(date)

start = dt.date( 2014, 1, 1 )
end = dt.date( 2014, 1, 31 )

days = np.busday_count( start, end )
print(days)