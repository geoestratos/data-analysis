import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import argparse
from libs.utils import find_index, aprox_search
from datetime import datetime
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument("--start")
parser.add_argument("--end")

args = parser.parse_args()

start_depth = float(args.start)
end_depth = float(args.end)
time_real = []
depth_real = []
print("Get data")
response = requests.get("http://167.71.240.14/api/drilling/?well=3&name=TIME")

if response.status_code == 200:
    print("Data received")
    res =  json.loads(response.content)
    for element in res:
        time_real.append(element["date"])
        depth_real.append(element["depth"])

program = pd.read_csv('./data/program.csv')
time_program, depth_program = program.iloc[:,1], program.iloc[:,0]

depth_real.reverse()
time_real.reverse()

start_depth_real_index = find_index(depth_real, start_depth, "start", step=1)
end_depth_real_index = find_index(depth_real, end_depth, "end", step=1)

time_real = time_real[start_depth_real_index:end_depth_real_index]
depth_real = depth_real[start_depth_real_index:end_depth_real_index]

program_start = aprox_search(depth_program)

# Date to days
days = []
init_date = datetime.strptime(time_real[0], '%Y-%m-%d %H:%M:%S')

for i, time in enumerate(time_real):
    date = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    fracc = date.hour/24
    days.append((date.day-init_date.day) + fracc)


plt.plot(time_program, depth_program)
plt.plot(days, depth_real)
plt.gca().invert_yaxis()
plt.show()

