from datetime import datetime , timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pycaret.regression import *
import requests
from wwo_hist import retrieve_hist_data

date=(input("enter the month and year for which you want to predict the sales of the product [EXAMPLE : 02-2020 (FEB 2020)]: "))
print("The Products are : \n  ALCOHOL ,  BREAD  , CHEMISTRY , CHEWING_GUM_LOLIPOPS  \n   CHIPS_FLAKES  ,  CIGARETTES  ,  COFFEE TEA  ,  COOKIES_BULK \n DAIRY_CHESSE  ,  DRINK_JUICE  ,  GENERAL  ,  GENERAL_FOOD \n GENERAL_ITEMS  ,  GROATS_RICE_PASTA  ,  ICE_CREAMS_FROZEN,  KETCH_CONCETRATE_MUSTARD_MAJO_HORSERADISH \n OCCASIONAL  ,  POULTRY  ,  SPICES  ,  SWEETS  ,  TABLETS  ,  VEGETABLES")
group=input("Enter the group of products for which you want to predict the sales for the above entered month : ")


converted_datetime=pd.to_datetime(date).date()

# this function makes sure that when the user enters a date, it calculates the ending of the month the user entered  
def dateaddition (converted_datetime):
    if int(str(converted_datetime).split("-")[0])%4 ==0:
        if (int(str(converted_datetime).split("-")[1])) ==2:
            added_days=29
        elif int(str(converted_datetime).split("-")[1]) %2 ==0 and int(str(converted_datetime).split("-")[1]) <=6:   
            added_days=30
        elif int(str(converted_datetime).split("-")[1]) %2 ==1 and int(str(converted_datetime).split("-")[1]) <=6:
            added_days=31
        elif  int(str(converted_datetime).split("-")[1]) %2 ==0 and int(str(converted_datetime).split("-")[1]) >=7:
            added_days=31
        elif int(str(converted_datetime).split("-")[1]) %2 ==1 and int(str(converted_datetime).split("-")[1]) >=7:
            added_days=30  
    elif int(str(converted_datetime).split("-")[0])%4 !=0:
        if (int(str(converted_datetime).split("-")[1])) ==2:
            added_days=28
        elif int(str(converted_datetime).split("-")[1]) %2 ==0 and int(str(converted_datetime).split("-")[1]) <=6:   
            added_days=30
        elif int(str(converted_datetime).split("-")[1]) %2 ==1 and int(str(converted_datetime).split("-")[1]) <=6:
            added_days=31
        elif  int(str(converted_datetime).split("-")[1]) %2 ==0 and int(str(converted_datetime).split("-")[1]) >=7:
            added_days=31
        elif int(str(converted_datetime).split("-")[1]) %2 ==1 and int(str(converted_datetime).split("-")[1]) >=7:
            added_days=30  

    return added_days


#converting the dates to strings to pass them through the weather-collecting api
start_date = converted_datetime.strftime("%d-%b-%Y")

# calculating the end date based on the function dateaddition
end_date= pd.to_datetime(converted_datetime+timedelta(dateaddition(converted_datetime)-1)).date()

#if the user enters the present month, the end date will be calculated based on the present day 
if end_date > datetime.now().date():
    end_date= datetime.now().date().strftime("%d-%b-%Y")
else:
    end_date=end_date.strftime("%d-%b-%Y")


# this is an api to collect the necessary weather data we need 
frequency = 24
start_date = start_date
end_date = end_date
api_key = '12b2c18a34194a8ca93113127200405'
location_list = ['Mlawa']
hist_weather_data = retrieve_hist_data(api_key,
                                        location_list,
                                        start_date,
                                        end_date,
                                        frequency,
                                        location_label = False,
                                        export_csv = True,
                                        store_df = True)

   #the weather data is stored in the file "Mlawa.csv", hence we read from that 
monthly_weather_data=pd.read_csv("Mlawa.csv")


def final_weather(monthly_weather_data):
    #dropping the unecessary columns
    monthly_weather_data=monthly_weather_data.drop(["date_time","totalSnow_cm","sunHour","uvIndex.1","uvIndex","moon_illumination","moonrise","moonset","sunrise","DewPointC","sunset","WindChillC","WindGustKmph","precipMM","pressure","visibility","winddirDegree","windspeedKmph","tempC"],axis=1)
    monthly_weather_data["avg_temp"]=(monthly_weather_data["maxtempC"]+monthly_weather_data["mintempC"])/2
    monthly_weather_data=monthly_weather_data.drop(["maxtempC","mintempC"],axis=1)
    # rearranging the data
    monthly_weather_data=monthly_weather_data[["avg_temp","FeelsLikeC","HeatIndexC","cloudcover","humidity",]]
    values=[]
    monthly_averages=[]

    def mean_data(data):
        
        for key,value in data.iteritems():
            values.append(value.mean())
            print(key)
        return values

    #categorising the heat_index data into three different types
    def cat_heat(heatindex):
        if heatindex < -2:
            return (0)
        elif heatindex >=-1 and heatindex<=14:
            return (1)
        else:
            return (2)   


    #categorising the cloud cover into 4 different types
    def cat_cloud(cloudcover):
        if cloudcover < 25:
            return(0)
        elif cloudcover >=25 and cloudcover<50:
            return(1)
        elif cloudcover >=50 and cloudcover<75:
            return(1)    
        else:
            return(3)

    monthly_averages=np.around(mean_data(monthly_weather_data),2)
    monthly_averages[2]=cat_heat(monthly_averages[2])
    monthly_averages[3]=cat_cloud(monthly_averages[3])

    return monthly_averages

monthly_weather_data=final_weather(monthly_weather_data)
        
# print(monthly_weather_data)

final_data=pd.read_csv("GROUP_OF_ITEMS_FINAL/"+group.upper()+".csv")



# final_data["ishol/week"]=9
# final_data["monthly_Avgtemp"]=monthly_weather_data[0]
# final_data["monthly_avg_FeelsLikeC"]=monthly_weather_data[1]
# final_data["monthly_avg_HeatIndexC"]=monthly_weather_data[2]
# final_data["monthly_avg_cloudcover"]=monthly_weather_data[3]
# final_data["monthly_avg_humidity"]=monthly_weather_data[4]

# # # test_data=pd.read_csv("GROUP_OF_DATASETS/SWEETS.csv")
# # test_data=test_data.rename(columns={0:"weekend"})
# # test_data=test_data.drop(test_data["quantity"])

# # print(final_data.head())

# loaded_model=load_model("Final_Mod")

# pred=predict_model(loaded_model, data= final_data)

# print(pred.head())


