from re import L
from turtle import st
import pandas as pd
import numpy as np

df = pd.read_csv('data2.csv')
start_time = df['Local time'].head(1)
end_time   = '11.04.2022 02:35:22.051'
# Change Local time dtype to datetime
df['Local time'] = pd.to_datetime(df['Local time'])

#Set Local time as index in dataframe
df = df.set_index(['Local time'])

#Taking input for time gape 

time_gape = int(input("Enter time in minutes: "))

# Convert minutes into second
time_gape_second = time_gape*60

time_gape_milisecond = time_gape_second*1000

print("Time in second is : ",time_gape_second)
print("Time in milisecond is : ",time_gape_milisecond)
# Calculating End time
start_time = pd.to_datetime(start_time)
print("Start time is : ",start_time)

end_time = start_time + pd.to_timedelta(time_gape_second,'s')
print("End time is : ", end_time)

print(df[start_time:end_time])