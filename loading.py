import pickle
from datetime import datetime , timedelta
import pandas as pd

loaded_model=pickle.load(open("Final_Mod.pkl","rb"))

date=(input("enter the month and year for which you want to predict the sales of the product : "))

#this will be used when we have multiple models to predict on
# category=input("enter the product catergory you want to have")



converted_datetime=pd.to_datetime(date).date()

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


end_date= pd.to_datetime(converted_datetime+timedelta(dateaddition(converted_datetime)-1)).date().strftime("%d-%b-%Y")

#converting the file to the required format so as to enter it in the wwo-hist
start_date = converted_datetime.strftime("%d-%b-%Y")

print(start_date,"   ",end_date)




import requests
from wwo_hist import retrieve_hist_data
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

import numpy as np
monthly_weather_data=pd.read_csv("Month_Weather_data.csv")

monthly_weather_data=monthly_weather_data.drop(["date_time","totalSnow_cm","sunHour","uvIndex.1","uvIndex","moon_illumination","moonrise","moonset","sunrise","DewPointC","sunset","WindChillC","WindGustKmph","precipMM","pressure","visibility","winddirDegree","windspeedKmph","tempC"],axis=1)


monthly_weather_data["avg_temp"]=(monthly_weather_data["maxtempC"]+monthly_weather_data["mintempC"])/2

monthly_weather_data=monthly_weather_data.drop(["maxtempC","mintempC"],axis=1)

monthly_weather_data=monthly_weather_data[["avg_temp","FeelsLikeC","HeatIndexC","cloudcover","humidity",]]
# monthly_weather_data=monthly_weather_data[["avg_temp","FeelsLikeC","HeatIndexC","cloudcover","humidity","ishol/week"]]

# print(monthly_weather_data.head())

def cat_heat(heatindex):
    # monthly_heatindex=[]
    # for heatindex in data["HeatIndexC"]:
        if heatindex < -2:
            return (0)
        elif heatindex >=-1 and heatindex<=14:
            return (1)
        else:
            return (2)
        



def cat_cloud(cloudcover):
    # monthly_cloudcover=[]
    # for cloudcover in data["cloudcover"]:
        if cloudcover < 25:
            return(0)
        elif cloudcover >=25 and cloudcover<50:
            return(1)
        elif cloudcover >=50 and cloudcover<75:
            return(1)    
        else:
            return(3)
        
            

            

def mean_data(data):
    values=[]
    for key,value in data.iteritems():
        values.append(value.mean())
        print(key)
    return values

monthly_averages=np.around(mean_data(monthly_weather_data),2)
monthly_averages[2]=cat_heat(monthly_averages[2])
monthly_averages[3]=cat_cloud(monthly_averages[3])
        
print(monthly_averages)


#the following code isn't working out because the scaled info should come from the training data and not here why I'm going to do it manually
# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()
# print(scaler.fit_transform(monthly_averages.reshape(1,-1)))


#this is the manual way of standard scaling( also called z-score) where z= (x-u)/s where u is the mean and s is the standard deviation =
monthly_averages[0]=(monthly_averages[0]-9.938361618798812)/8.179640810862661
monthly_averages[1]=(monthly_averages[1]-7.918146214098957)/9.922044758131065
monthly_averages[2]=(monthly_averages[2]-1.3829416884247172)/0.608677389627343
monthly_averages[3]=(monthly_averages[3]-1.2075718015665797)/0.822514130746482
monthly_averages[4]=(monthly_averages[4]-75.15467362924234)/5.489277393805853

monthly_averages=np.around(monthly_averages,2)

monthly_averages=list(monthly_averages)

monthly_averages.insert(0,-0.381941)
monthly_averages.insert(0,2.524183)

monthly_averages=np.around(monthly_averages,2)

print(monthly_averages)
# monthly_averages=list(monthly_averages)


### BRO PLEASE CHECK THIS OUT. IT IS NOT ACCEPTING A NUMPY ARRAY PLEASE TRY TO DO WHAT YOU CAN. ABHI I AM VERY SLEEPY AND MY BRAIN IS FRIED 
### I HAVE SAVED THE PICKLE AS WELL AS THE OTHER NOTEBOOK IN THE REPO PLEASE CHECK IT.
### ALSO CHECK IF PYCARET SAVES THE MODEL AS A PROPER PICKLE FILE.  IDK WHT I AINT ABLE TO PREDCIT 



pred=loaded_model.predict([[ 2.52 ,-0.38 , 1.18 , 1.06,  1.01, -0.25 ,-0.34]])
print(pred)
# print(monthly_weather_data["avg_temp"])