import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv(r'C:\Users\Randy Gala\Proyectos\linear-regression\suuk.csv')
indexNames = dataset[ dataset['GR'] == -999.25 ].index
dataset.drop(indexNames, inplace=True)

indexNames = dataset[ dataset['RES_DEP'] == -999.25 ].index
dataset.drop(indexNames, inplace=True)

percentage = .01
dataset = dataset[:int((len(dataset))*percentage)]

X = np.array(dataset.DEPT, dtype=np.int) #Well depth
Y = np.array(dataset.GR) #Gamma ray
Z = np.array(dataset.RES_DEP) #Resistive

interval = 2
param_depth = np.arange(np.around(Y[0], decimals=-2), np.around(Y[-1], decimals=-1), interval)

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(X, Y)
ax2.plot(X, Z)

X = np.array([np.ones(X.shape[0]),X]).T

B = np.linalg.inv(X.T @ X) @ X.T @ Y

print(B)

ax1.plot([X.T[1].min(), X.T[1].max()],[ B[0] + B[1] * X.T[1].min()*0.8, B[0] + B[1] * X.T[1].max()*1.2], c="red")

ax1.invert_yaxis()
ax2.invert_yaxis()
plt.show()


