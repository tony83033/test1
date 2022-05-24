
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pymongo
import sys
sys.setrecursionlimit(100000)


client = pymongo.MongoClient('localhost', 27017)
db = client['forx_database']
collection = db['rowdata']
# Fetch all data from rowdata
cursor = collection.find({})



fig = go.Figure()
mydf = pd.DataFrame(cursor)

def showdata():
    print(mydf.head()) 
def find_index(time_gape):
    # Finding Start and end time
    global mydf
    start_time = mydf['Local time'].head(1)
    start_time = pd.to_datetime(start_time)
    end_time   = start_time + pd.to_timedelta(time_gape,'s')
    print(end_time)
    # Finding Index for End time
    time_list = mydf['Local time']
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
            df2 = mydf.iloc[:i]
            hint = True
            mydf = mydf.drop(range(0,i))
            mydf = mydf.reset_index(drop=True)
            #print(mydf.head())
            break
    if(hint):
        mean_and_median(df2,time_gape,end_time)
    else:
        fig.show()
        mean_median_graph()
    
    
def making_graph(df2,time_gape,end_time):
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
    find_index(time_gape)


def mean_and_median(df2,time_gape,end_time):
    global tag
    mytag = tag
    mymean = df2['Ask'].mean()
    mymedian = df2['Ask'].median()
    post = {
        "Time": str(end_time),
        "mean": mymean,
        "median": mymedian
    }

    collection = db[str(tag)]
    post_id = collection.insert_one(post).inserted_id
    print(post_id)
    making_graph(df2,time_gape,end_time)

def mean_median_graph():
    global tag
    collection = db[str(tag)]
    cursor = collection.find({})

    for document in cursor:
        print(document)
    start()
def start():
    global tag
    message = '''====Welcome====
                Please chose an options
                1) Enter time for analysis
                2) show data frame
                3) Exit
    '''
    
    print(message)
    a= 0
    a = int(input("Enter a choise : "))

    if(a==1):
        tag = input("Enter a tag : ")
        b = int(input("Enter time in minutes: "))
        b = b*60
        find_index(b)
    elif(a==2):
        showdata()
    elif(a==3):
        try:
            exit()
        except:
            print("Some Error ")
            exit()
    else:
        print("Invalid Input")


        
if __name__ == "__main__":
    start()
   
    


    # mydata.showdata()