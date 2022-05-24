
import random
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import csv

fig = go.Figure()
df3 =1
df = pd.read_csv('data.csv')


#Function for taking time gape as input
def take_input():
    input_time = int(input("Enter time in minutes = "))
    print("Calculating time pls wait")
    calu_start_time(input_time                                                                                 )

#function for calculating first start_time
def calu_start_time(input_time):
    start_time = df['Local time'].head(1)
    start_time = pd.to_datetime(start_time)

    # Adding start time and input time to find end time
    end_time = start_time + pd.to_timedelta(input_time,'m')
    # Now we have start_time and end_time
    print(" First End time is = ",end_time)
    first_index_find(start_time,end_time,input_time)
    #calu2_start_time(end_time,input_time)
    

# Make graph will call this function
def calu2_start_time(end_time,input_time,i):
    start_time = end_time
    # input_time = input_time
    
    # print("Input is = ",input_time)
    end2_time = start_time + pd.to_timedelta(input_time,'m')
    print(start_time," To ",end2_time)
    first_index_find(start_time,end2_time,input_time,i)

def first_index_find(start_time,end_time,input_time,i):
    # =============================== For End time index ===============
    i=i
    time_list = df['Local time']
    # Making a list with length of time_list
    find_index = [None] * (len(time_list))
    #make a numpy array with a value of dtype bool True
    compare1 = np.array([True], dtype=bool)
    #Storing true and false value in find_index list according to time
    for i in range(len(find_index)):
        find_index[i] = [time_list[i] > end_time]
        if(find_index[i]==compare1[0]):
            break
    
    # Storing End time Index number in End_time_index
    try:
        end_time_index = find_index.index(compare1[0])
        print("End time index is = ",end_time_index)
    except:
        print("=============== WE ARE DONE ===============")
        fig.show()
        exit()
    # ====================================For Start time index===================================
    find_index = [None] * (len(time_list))
    compare1 = np.array([True], dtype=bool)
    for i in range(len(find_index)):
        find_index[i] = [time_list[i] > start_time]
        if(find_index[i]==compare1[0]):
            break
    try:
        start_time_index = find_index.index(compare1[0])
    except:
        print("=============== WE ARE DONE ===============")
        fig.show()
        exit()
    
    # print("Start time index = ",start_time_index)
    mean_and_median(start_time_index,end_time_index,end_time,input_time,i)

def mean_and_median(start_time_index,end_time_index,end_time,input_time,i):
    df2 = df.iloc[start_time_index:end_time_index]
    time1 = df2['Local time'].head(1)
    time2 = df2['Local time'].tail(1)
    # final_time = str(time1) + str(time2)

    # For Ask================================
    ask_mean   = df2['Ask'].mean()
    ask_median = df2['Ask'].median()
    fields = ['Start time','End time','Mean','Median']
    rows =[[time1,time2,ask_mean,ask_median]]
    # writing csv file for Ask
    filename = "Ask.csv"
    with open (filename,'a') as csvfile:
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile)
        # creating a csv dict writer object 
        writer = csv.DictWriter(csvfile, fieldnames = fields) 
        # 5writer.writeheader()
        # writing the data rows 
        csvwriter.writerows(rows)
    
    #Calling Graph function
    making_graph(start_time_index,end_time_index,end_time,input_time,ask_median,i)
    

def making_graph(start_time_index,end_time_index,end_time,input_time,ask_median,i):
    global df3
    # data = df.iloc[[0,55],[0,1]]
    # data = df.iloc[45:55,0:1]
    df2 = df.iloc[start_time_index:end_time_index]
    # print(df2['Ask'])
    # print(df2['Bid'])
    name = "Time ",df2['Local time'].head(1)," To ",df2['Local time'].tail(1)
    print("Median of ask is = ",df2['Ask'].median())
    print("Mean of ask is = ",df2['Ask'].mean())

    # print(df2['AskVolume'])
    # print(df['BidVolume'])
    # data = df["Local time"].head(1)
    # print(data)
    print("Making Graph pls wait ... ")
    # fig = go.Figure(data=go.Violin(y=df2['Ask'], box_visible=True, line_color='black',points='all',
                            #    meanline_visible=True, fillcolor='lightseagreen', opacity=0.6,
                            #    x0='Time'))
    # a = str(mycount)
    
    my_median = df2['Ask'].mean()
    Ask_df = pd.read_csv('Ask.csv')
    last_median = Ask_df.tail(2)
    my_time = df2['Local time'].head(1)
    my_time = str(my_time)
    s1 =slice(26)

    if(last_median.iloc[0,2] >= my_median):
        fig.add_trace(go.Violin(y=df2['Ask'],
                        x0=my_time[s1],
                        legendgroup=str(df3),
                        name=str(df3),
                        line_color='red',
                        y0="Time",
                        
                        )
             )
    else:
        fig.add_trace(go.Violin(y=df2['Ask'],
                        x0=my_time[s1],
                        legendgroup='Ask',
                        name=str(df3),
                        line_color='green',
                        y0="Time",
                        
                        )
             )
    
    df3 = df3+1
    # mycount = mycount+1
    # fig.add_trace(go.Violin(y=df2['Bid'],
    #                     x0="Bid",
    #                     legendgroup='Bid',
    #                     name='Bid',
    #                     line_color='red',
    #                     y0="Time")
    #          )
    # fig.add_trace(go.Violin(y=df2['AskVolume'],
    #                     x0="AskVolume",
    #                     legendgroup='AskVolume',
    #                     name='AskVolume',
    #                     line_color='green',
    #                     y0="Time")
    #          )
    # fig.add_trace(go.Violin(y=df2['BidVolume'],
    #                     x0="BidVolume",
    #                     legendgroup='BidVolume',
    #                     name='BidVolume',
    #                     line_color='orange',
    #                     y0="Time")
    #          )
    fig.update_traces(box_visible=True, meanline_visible=True)
    fig.update_layout(violinmode='group')
    
    

    
    # fig.update_layout(violinmode='group')
    
    #fig.write_image('mgraph.pdf',engine="kaleido")

    # with open('p_graph.pdf', 'a') as f:
    #     fig.write_image(f,engine="kaleido",'a')

    calu2_start_time(end_time,input_time,i)

    # end_time = df.iloc[55,0]
    # end_time = pd.to_datetime(end_time)
    # calu2_start_time(end_time,input_time)

a =1
take_input()
# take_input()


