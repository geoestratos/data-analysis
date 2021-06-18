import numpy as np
from data.config import config

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

def substring_by_limits(array, start, end):
    start_index = aprox_search(array, start)

def aprox_search(array, value):
    for i, value in reversed(list(enumerate(array))):
       if value < value:
           return i