
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from scipy import stats
import tensorflow as tf
import math
import random


# In[2]:


fps=120
threshold=0.75
moving_avg_len=10


# In[13]:


def readFileData(file):
    column_names = ['wmx1', 'wmy1', 'wmz1']

    data = pd.read_csv(file, skiprows = 1 , names = column_names)
 
    wx = data["wmx1"]
    wy = data["wmy1"]
    wz = data["wmz1"]

    records=movingavg(wx,wy,wz)

    return np.dstack([wx,wy,wz])[0]

def readData(directory):
    records = []
    labels = np.empty(0)
    
    allFiles = glob.glob("*.csv")
    for i,file in enumerate(allFiles):
        fileName = os.path.basename(file)
        print("file name is", fileName,"num is",i)
        (name, ext) = os.path.splitext(fileName)
        parts = name.split("_")
        if (True):
            label = parts[0]
            fileData = readFileData(file)
            print("file datat is ",fileData)
            records.append(fileData)
            labels = np.append(labels, label)

    return (records, labels)

def movingavg(x,y,z):
    x_avg = np.zeros(moving_avg_len)/moving_avg_len
    y_avg = np.zeros(moving_avg_len)/moving_avg_len
    z_avg = np.zeros(moving_avg_len)/moving_avg_len
    x_avg = np.convolve(x,x_avg,'same')
    y_avg = np.convolve(y,y_avg,'same')
    z_avg = np.convolve(z,z_avg,'same')
    
    return [x_avg,y_avg,z_avg]

def splitData(records):##sungshil
    print("records is ",records[0][0])
    term=fps//4
    record_sum=[]
    record=[]
    record_all=[]
    ct=0
    sum_now=0.0
    sum_pre=0.0
    start=0
    end=0
    
    for i in range((len(records[0])//(term))-100):
        sum=0.0
        record_x=np.empty(shape=[1],dtype=float)
        record_y=np.empty(shape=[1],dtype=float)
        record_z=np.empty(shape=[1],dtype=float)
        for j in range(fps):
            record_x=np.append(record_x,records[0][term*i+j][0])
            record_y=np.append(record_y,records[0][term*i+j][1])
            record_z=np.append(record_z,records[0][term*i+j][2])
        for k in range(fps-2):
            sum=sum+(record_x[k]-record_x[k+1])**2+(record_y[k]-record_y[k+1])**2+(record_z[k]-record_z[k+1])**2
            
        sum_pre=sum_now
        sum_now=sum
        record_sum.append(sum)
        if (sum_pre<threshold and sum_now>threshold):
            
            ct=ct+1
            start=120*i
            print("start",start)
        if (sum_pre>threshold and sum_now<threshold):
            end=120*i  
            print("end",end)
            print("step is " ,ct)
            print("length of end-start",(end-start))
            s=[]
            for k in range(end-start):
                t=(records[0][term*i+j+k])
                #print("t is",t)
                s.append(t)
                #print("s is ",s)
            record_all.append(s)
            

         


    
    print("number of patterm : ",ct)
    print("average is",np.average(record_sum))
    print("number of term",len(record_sum))
    plt.plot(record_sum[1500:2500])
    
    return record_all


# In[17]:


(records,label)=readData("dr")
print("size of ",len(records[0]))
print("size of divide ",len(records[0])//40)
#records=filter_data(records)
records=splitData(records)


# In[5]:


tt=[]
tt.append([1])
print(tt)


# In[6]:


X= tf.placeholder()

