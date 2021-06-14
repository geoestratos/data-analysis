import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import argparse
import requests
import json

def remove(dataset, label, value):
    indexNames = dataset[ dataset[label] == value ].index
    df.drop(indexNames, inplace=True)

def sample_average(array, samples):
    mean = []
    for i, value in enumerate(array):
        if i<samples:
            mean.append(round(np.mean(array[i:i+samples]), 2))      
        elif i>=samples:
            mean.append(round(np.mean(array[i-samples:i+samples]), 2))  
    return mean

def find_index(dataset, value, type):
    for i, v in enumerate(dataset):
        if type == "end":
            if v <= value and v > value-1:
                return i
        elif type == "start":
            if i < len(dataset) - 1:
                if v >= value:
                    return i
            else: return i

parser = argparse.ArgumentParser()

parser.add_argument("--variable")
parser.add_argument("--start")
parser.add_argument("--end")
parser.add_argument("--colors")



args = parser.parse_args()

df = pd.read_csv('./data/suuk.csv')

real = []
response = requests.get("http://167.71.240.14/api/drilling/?well=3&name=LWD.%20Rayos%20Gamma")
if response.status_code == 200:
    res =  json.loads(response.content)
    for element in res:
        real.append(element["value"])


remove(df, 'GR', -999.25)
remove(df, 'RES_DEP', -999.25)

percentage = .75
samples = 50
step = 0.1524 ## Meters/register
start = float(args.start)
end = float(args.end)
colors = args.colors.split(',')

config = [
    {
        'name': 'Pleistoceno',
        'depth': 85,
        'yellow': 1,
        'orange': 3,
        'red': 5,
    },
    {
        'name': 'Cretasico sup',
        'depth': 5759,
        'yellow': 10,
        'orange': 15,
        'red': 20,
    },
]

if float(start) <= df.DEPT[0]:
    start =  df.DEPT[0]

start = find_index(df.DEPT, start, "start")
end = find_index(df.DEPT, end, "end")
        

df = df[start:end]

X = np.array(df.DEPT, dtype=np.int32) #Well depth
Y = []

if(args.variable == 'gamma'):
    Y = np.array(df.GR) #Gamma ray
elif(args.variable == 'resistive'):   
    Y = np.array(df.RES_DEP) #Resistive


fig, (plt1) = plt.subplots(1, 1)

index1 = find_index(X, config[0]['depth'], "start")
index2 = find_index(X, config[1]['depth'], "start")

red_sup = []
orange_sup = []
yellow_sup = []

age1 = np.array(sample_average(Y, 50))
age1 = np.array(age1[index1:index2-1])

###SUPERIOR LIMITS
red_sup = np.append(red_sup, (age1 + config[0]['red']))
orange_sup = np.append(orange_sup, (age1 + config[0]['orange']))
yellow_sup = np.append(yellow_sup, (age1 + config[0]['yellow']))

if X[index2] >= config[1]['depth']:
    age2 = np.array(sample_average(Y, 50))
    age2 = np.array(age2[index2:])
    red_sup = np.append(red_sup, (age2 + config[1]['red']))
    orange_sup = np.append(orange_sup, (age2 + config[1]['orange']),)
    yellow_sup = np.append(yellow_sup, (age2 + config[1]['yellow']))


### INFERIOR LIMITS
# red = np.append((age1 - config[0]['red']),(age2 - config[1]['red']))
# orange = np.append((age1 - config[0]['orange']),(age2 - config[1]['orange']))
# yellow = np.append((age1 - config[0]['yellow']),(age2 - config[1]['yellow']))


# plt1.plot(Y, X, color="gray", alpha = 0.5)
plt1.plot(sample_average(Y, 50), X, color = colors[0], alpha = 0.5)

plt1.plot(red_sup,X[:-1], color=colors[1])
plt1.plot(orange_sup,X[:-1], color=colors[2])
plt1.plot(yellow_sup,X[:-1], color=colors[3])
plt1.set_title('Resistivo 100samp')
plt1.invert_yaxis()
if(args.variable == 'resistive'):
    plt1.set_xscale('log')




plt.show()
