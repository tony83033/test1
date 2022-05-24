import pandas as pd
import numpy as np
import pymongo
import plotly.graph_objects as go
import sys


# Increase number of recursion  
sys.setrecursionlimit(100000)
fig = go.Figure()
# Connect to mondoDB
client = pymongo.MongoClient('localhost', 27017)
# Connect to forx_database
db = client['forx_database']
# Connect to collection rowdata
collection = db['rowdata']
# Fetch all data from rowdata
cursor = collection.find({})
df = pd.DataFrame(cursor)

  
def showdata():
    print(df.head())

def find_index(time_gape,mytag):
    # Finding Start and end time
    global df
    start_time = df['Local time'].head(1)
    start_time = pd.to_datetime(start_time)
    end_time   = start_time + pd.to_timedelta(time_gape,'s')
    print(end_time)
    # Finding Index for End time
    time_list = df['Local time']
    # Making a list with length of time_tist
    find_index = [None] * (len(time_list))
    # Making a numpy array with a dtype bool
    compare1 = np.array([True], dtype=bool)
    hint = False                                                                                             
    for i in range (len(find_index)):
        try:
            find_index[i] = [time_list[i] > end_time]
        except:
            print("WE are done")
            exit()

        
        if(find_index[i]==compare1[0]):
            print(i)
            #self.df.drop(self.df.iloc[:75],axis=1)
            df2 = df.iloc[:i]
            hint = True
            df = df.drop(range(0,i))
            df = df.reset_index(drop=True)
            #print(mydf.head())
            break
    if(hint):
        mean_and_median(df2,time_gape,end_time,mytag)
    else:
        fig.show()
        mean_median_graph()
    
    
def making_graph(df2,time_gape,end_time,mytag):
    # a = time_gape
    fig.add_trace(go.Violin(y=df2['Ask'],
                    # x0=my_time[s1],
                    legendgroup='chart',
                    name='my chart',
                    line_color='green',
                    y0="Time",
                    
                    ))
    fig.update_traces(box_visible=True, meanline_visible=True)
    fig.update_layout(violinmode='group')
    find_index(time_gape,mytag)


def mean_and_median(df2,time_gape,end_time,mytag):
    
    mymean = df2['Ask'].mean()
    mymedian = df2['Ask'].median()
    post = {
        "Time": str(end_time),
        "mean": mymean,
        "median": mymedian
    }

    collection = db[str(mytag)]
    post_id = collection.insert_one(post).inserted_id
    print(post_id)
    making_graph(df2,time_gape,end_time,mytag)

def mean_median_graph():
    global tag
    collection = db[str(tag)]
    cursor = collection.find({})

    for document in cursor:
        print(document)
    
        

if __name__ == "__main__":
    
    
    while (True):
        mymessage =  ''' ====Welcome====
                    Please chose an options
                    1) Enter time for analysis
                    2) show data frame
                    3) Exit 
                    '''
        print(mymessage)
        try:
            b = int(input("Enter any choise: "))
        except NameError:
            print("Invalid Input")
            continue
        if(b==1):
            time = int(input("Enter time in minutes : "))
            time = time *60
            mytag = input("Enter a Tag: ")
            find_index(time,mytag)
        elif(b==2):
            showdata()
        elif(b==3):
            exit()
        else:
            print("Invalid Input")



        






