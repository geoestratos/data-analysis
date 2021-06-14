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
            mean.append(round(np.mean(array[i:i+samples]), 2))      
        elif i>=samples:
            mean.append(round(np.mean(array[i-samples:i+samples]), 2))  
    return mean


df = pd.read_csv('suuk.csv')

remove(df, 'GR', -999.25)
remove(df, 'RES_DEP', -999.25)

percentage = .07
samples = 50
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

df = df[:int((len(df))*percentage)]

X = np.array(df.DEPT, dtype=np.int32) #Well depth
Y = np.array(df.GR) #Gamma ray
Z = np.array(df.RES_DEP) #Resistive


# poly_reg = PolynomialFeatures(degree=16)
# x_poly = poly_reg.fit_transform(X[samples-1:-2].reshape(-1,1))
# lin_reg_2 = LinearRegression()
# lin_reg_2.fit(x_poly, meanY)
# plt.plot(lin_reg_2.predict(poly_reg.fit_transform(X[samples-1:-2].reshape(-1,1))), X[samples-1:-2] , color='green')


fig, (plt1) = plt.subplots(1, 1)

limit_gamma=20
limit_res=3

index1 = np.where((X > config[0]['depth']) & (X < config[1]['depth']))
index2 = np.where(X > config[1]['depth'])

age1 = np.array(sample_average(Z, 50))
# age1 = np.array(age1[index1[0][0]:index2[0][0]-1])


# age2 = np.array(sample_average(Z, 50))
# age2 = np.array(age2[index2[0][0]:index2[0][-1]])

red = age1 - config[0]['red']
orange = age1 - config[0]['orange']
yellow = age1 - config[0]['yellow']
red_sup = age1 + config[0]['red']
orange_sup = age1 + config[0]['orange']
yellow_sup = age1 + config[0]['yellow']
# red = np.append((age1 - config[0]['red']),(age2 - config[1]['red']))
# orange = np.append((age1 - config[0]['orange']),(age2 - config[1]['orange']))
# yellow = np.append((age1 - config[0]['yellow']),(age2 - config[1]['yellow']))
# red_sup = np.append((age1 + config[0]['red']),(age2 + config[1]['red']))
# orange_sup = np.append((age1 + config[0]['orange']),(age2 + config[1]['orange']))
# yellow_sup = np.append((age1 + config[0]['yellow']),(age2 + config[1]['yellow']))

# plt1.plot(Y, X, color="red")
# plt1.plot(sample_average(Y, 50), X, color = 'blue')
# plt1.plot(np.array(sample_average(Y, 50))-limit_gamma, X, color = 'yellow')
# plt1.plot(np.array(sample_average(Y, 50))+limit_gamma, X, color = 'yellow')
# plt1.set_title('Gamma Ray 100samp')
# plt1.invert_yaxis()

# plt2.plot(Y, X, color="red")
# plt2.plot(sample_average(Y, 100), X, color = 'blue')
# plt2.set_title('Gamma Ray 200samp')
# plt2.invert_yaxis()


plt1.plot(Z, X, color="gray", alpha = 0.5)
plt1.plot(sample_average(Z, 50), X, color = 'blue')

plt1.plot(red,X[:], color="red")
plt1.plot(orange,X[:], color="orange")
plt1.plot(yellow,X[:], color="yellow")

plt1.plot(red_sup,X[:], color="red")
plt1.plot(orange_sup,X[:], color="orange")
plt1.plot(yellow_sup,X[:], color="yellow")
plt1.set_title('Resistivo 100samp')
plt1.invert_yaxis()
# plt2.set_xscale('log')

# plt4.plot(Z, X, color="red")
# plt4.plot(sample_average(Z, 100), X, color = 'blue')
# plt4.set_title('Resistivo 200samp')
# plt4.invert_yaxis()
# plt4.set_xscale('log')



plt.show()
