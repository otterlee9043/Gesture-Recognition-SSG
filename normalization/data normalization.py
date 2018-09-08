
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from scipy import stats
import tensorflow as tf
import math
import random
###################################################


# In[10]:


fps=40
threshold=0.75
moving_avg_len=10


# In[17]:


def readFileData(file):
    column_names = ['wmx1', 'wmy1', 'wmz1']

    data = pd.read_csv(file, skiprows = 1 , names = column_names)
 
    wx = data["wmx1"]
    wy = data["wmy1"]
    wz = data["wmz1"]
#     bx1 = data["bmx1"] 
#     by1 = data["bmy1"]
#     bz1 = data["bmz1"]
#     bx2 = data["bmx2"]
#     by2 = data["bmy2"]
#     bz2 = data["bmz2"]
#     bx3 = data["bmx3"]
#     by3 = data["bmy3"]
#     bz3 = data["bmz3"]

#     w=np.dstack([wx,wy,wz])
#     b1=np.dstack([bx1,by1,bz1])
#     b2=np.dstack([bx2,by2,bz2])
#     b3=np.dstack([bx3,by3,bz3])
    
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

def splitData(records):
    print("records  is ",records[0])
    pd_records=pd.DataFrame(records[0])
    record_w=pd_records.fillna(0)
    term=fps//4
    record_sum=[]
    records=[]
    ct=0
    sum_now=0.0
    sum_pre=0.0
    
    for i in range((len(records[0])//(term))-20):
        sum=0.0
        record_x=np.empty(shape=[1],dtype=float)
        record_y=np.empty(shape=[1],dtype=float)
        record_z=np.empty(shape=[1],dtype=float)
        for j in range(fps):
            record_x=np.append(record_x,record_w[0][term*i+j])
            record_y=np.append(record_y,record_w[1][term*i+j])
            record_z=np.append(record_z,record_w[2][term*i+j])
        for k in range(fps-2):
            sum=sum+(record_x[k]-record_x[k+1])**2+(record_y[k]-record_y[k+1])**2+(record_z[k]-record_z[k+1])**2
            
        sum_pre=sum_now
        sum_now=sum
        record_sum.append(sum)
        if (sum_pre<threshold and sum_now>threshold):
            
            ct=ct+1
            start=120*i
        if (sum_pre>threshold and sum_now<threshold):
            ct=ct+1
            end=120*i
        for k in range(end-start):
            records=(record_x[start+k])
    
            
    print("number of patterm : ",ct)
    print("average is",np.average(record_sum))
    print("number of term",len(record_sum))
    plt.plot(record_sum[1500:2500])


# In[18]:


(records,label)=readData("dr")

#records=filter_data(records)
splitData(records)


# In[1]:


tt=[]
tt.append([1])
print(tt)


# In[ ]:


X= tf.placeholder()

