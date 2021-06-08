import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def remove(dataset, label, value):
    indexNames = dataset[ dataset[label] == value ].index
    df.drop(indexNames, inplace=True)

def sample_average(array, samples):
    mean = []
    for i, value in enumerate(array):
        if i<samples:
            mean.append(round(np.mean(Y[i:i+samples]), 2))      
        elif i>=samples:
            mean.append(round(np.mean(Y[i-samples:i+samples]), 2))  
    return mean


df = pd.read_csv('suuk.csv')

remove(df, 'GR', -999.25)
remove(df, 'RES_DEP', -999.25)

percentage = .1
samples = 50

df = df[:int((len(df))*percentage)]

X = np.array(df.DEPT, dtype=np.int32) #Well depth
Y = np.array(df.GR) #Gamma ray
Z = np.array(df.RES_DEP) #Resistive

meanY = sample_average(X, samples)

# poly_reg = PolynomialFeatures(degree=16)
# x_poly = poly_reg.fit_transform(X[samples-1:-2].reshape(-1,1))
# lin_reg_2 = LinearRegression()
# lin_reg_2.fit(x_poly, meanY)
# plt.plot(lin_reg_2.predict(poly_reg.fit_transform(X[samples-1:-2].reshape(-1,1))), X[samples-1:-2] , color='green')


fig, (plt1, plt2, plt3, plt4) = plt.subplots(1, 4)

plt1.plot(Y, X, color="red")
plt1.plot(meanY, X, color = 'blue')
plt1.set_title('Gamma Ray 100samp')
plt1.invert_yaxis()

plt2.plot(Y, X, color="red")
plt2.plot(sample_average(X, 100), X, color = 'blue')
plt2.set_title('Gamma Ray 200samp')
plt2.invert_yaxis()

plt3.plot(Y, X, color="red")
plt3.plot(sample_average(Z, 50), X, color = 'blue')
plt3.set_title('Resistivo 100samp')
plt3.invert_yaxis()
plt3.set_xscale('log')

plt4.plot(Y, X, color="red")
plt4.plot(sample_average(Z, 100), X, color = 'blue')
plt4.set_title('Resistivo 200samp')
plt4.invert_yaxis()
plt4.loglog()


plt.show()
