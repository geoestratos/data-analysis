import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import argparse
import requests
import json

def remove(dataset, label, value):
    indexNames = dataset[ dataset[label] == value ].index
    plan.drop(indexNames, inplace=True)

def sample_average(array, samples):
    mean = []
    for i, value in enumerate(array):
        if i<samples:
            mean.append(round(np.mean(array[i:i+samples]), 2))      
        elif i>=samples:
            mean.append(round(np.mean(array[i-samples:i+samples]), 2))  
    return mean

def find_index(dataset, value, type, step):
    for i, v in enumerate(dataset):
        if type == "end":
            if (v <= value and v > value-step):
                return i
            elif i == len(dataset)-1:
                return i
            # elif v <= value and v > value*0.8:
            #     print("Data missing")
        elif type == "start":
            if i < len(dataset)-1:
                if v >= value:
                    return i
            else: return i

def param_array_by(array, array_ref, param_array, method=None):
    result_array = []
    # depth = []    
    if method is None:
        for i, value in enumerate(param_array):
            index_low =  find_index(array, value, "start", step=1)
            if i != len(param_array)-1:
                index_high = find_index(array, param_array[i+1], "end", step=1)
            else:   
                index_high = find_index(array, value, "end", step=1)

            if index_high != None and index_low != None:
                consult = array_ref[index_low: index_high]
                # depth.append(array[index_low: index_high])
                if len(consult)>0:
                    result_array.append(np.mean(consult))
                
    # print(depth)
    return result_array

parser = argparse.ArgumentParser()

parser.add_argument("--variable")
parser.add_argument("--start")
parser.add_argument("--end")
parser.add_argument("--colors")

args = parser.parse_args()


real = []
depth_real = []

##Get real data
if args.variable == "resistive":
    response = requests.get("http://167.71.240.14/api/drilling/?well=3&name=LWD.%20Res%20Profunda")
elif args.variable == "gamma":
    response = requests.get("http://167.71.240.14/api/drilling/?well=3&name=LWD.%20Rayos%20Gamma")

if response.status_code == 200:
    res =  json.loads(response.content)
    for element in res:
        real.append(element["value"])
        depth_real.append(element["depth"])
depth_real.reverse()
real.reverse()
##Get programmed data
plan = pd.read_csv('./data/suuk.csv')

#Remove nulls
remove(plan, 'GR', -999.25)
remove(plan, 'RES_DEP', -999.25)


#Config programmed calculation
samples = 10
start_depth = float(args.start)
end_depth = float(args.end)
colors = args.colors.split(',')
interval_m = 1

config = [
    {
        'name': 'Pleistoceno',
        'depth': 85,
        'ok': 1,
        'warning': 3,
        'danger': 5,
    },
    {
        'name': 'Cretasico sup',
        'depth': 5759,
        'ok': 10,
        'warning': 15,
        'danger': 20,
    },
]

#Calculate interval data
start_depth_index = 0
end_depth_index = 0
if start_depth <= plan.DEPT[0]:
    start_depth =  plan.DEPT[0]

start_depth_index = find_index(plan.DEPT, start_depth, "start", step=1)
end_depth_index = find_index(plan.DEPT, end_depth, "end", step=1)


start_depth_real_index = find_index(depth_real, start_depth, "start", step=1)
end_depth_real_index = find_index(depth_real, end_depth, "end", step=1)

plan = plan[start_depth_index: end_depth_index]
depth_plan = np.array(plan.DEPT, dtype=np.int32) #Well depth

real = real[start_depth_real_index: end_depth_real_index]
depth_real = depth_real[start_depth_real_index: end_depth_real_index]

#filter zeros real and
start_real_index = 0
for i, value in enumerate(real):
    if value > 0:
        start_real_index = i
        break

real = real[start_real_index:]
depth_real = depth_real[start_real_index:]

#Select plan variable
if(args.variable == 'gamma'):
    plan = np.array(plan.GR) #Gamma ray
elif(args.variable == 'resistive'):   
    plan = np.array(plan.RES_DEP) #Resistive

#reduce noise on dataset
plan = sample_average(plan, 50)
real = sample_average(real, 10)

#create parameterized axis
param_depth_plan = np.arange(np.around(depth_plan[0]), np.around(depth_plan[-1]), interval_m)
param_plan = param_array_by(depth_plan, plan, param_depth_plan)


#Calculate plan ages
age1_index = find_index( param_depth_plan, config[0]['depth'], "start", step=1)
age2_index = find_index(param_depth_plan, config[1]['depth'], "start", step=1)

danger_line = []
warning_line = []
ok_line = []

if age2_index == len(param_plan)-1:
    age1 = np.array(param_plan[age1_index:])
else: 
    age1 = np.array(param_plan[age1_index:age2_index])


#Create limits
danger_line = np.append(danger_line, (age1 + config[0]['danger']))
warning_line = np.append(warning_line, (age1 + config[0]['warning']))
ok_line = np.append(ok_line, (age1 + config[0]['ok']))

if  param_depth_plan[age2_index] >= config[1]['depth']:
    age2 = np.array(param_plan)
    age2 = np.array(age2[age2_index:])
    danger_line = np.append(danger_line, (age2 + config[1]['danger']))
    warning_line = np.append(warning_line, (age2 + config[1]['warning']),)
    ok_line = np.append(ok_line, (age2 + config[1]['ok']))


fig, (plt1) = plt.subplots(1, 1)
plt1.plot(param_plan, param_depth_plan[:-1], colors[0], label="Plan")
plt1.plot(danger_line, param_depth_plan[:-1], color=colors[3], label="Danger line")
plt1.plot(warning_line, param_depth_plan[:-1], color=colors[2], label="Warning line")
plt1.plot(ok_line, param_depth_plan[:-1], color=colors[1], label="Good line")
plt1.plot(real, depth_real, label= "Real")

plt1.set_title(args.variable.capitalize())
plt1.invert_yaxis()

if(args.variable == 'resistive'):
    plt1.set_xscale('log')

plt.show()
