import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('50m.csv')
df2 = pd.read_csv('100m.csv')
df3 = pd.read_csv('2m.csv')
df4 = pd.read_csv('10m.csv')


indexNames = df[ df['GR50m_Espaciam'] == -999.25 ].index
df.drop(indexNames, inplace=True)

indexNames = df2[ df2['GR100m_Espaciam'] == -999.25 ].index
df2.drop(indexNames, inplace=True)

indexNames = df3[ df3['GR2mEspaciam'] == -999.25 ].index
df3.drop(indexNames, inplace=True)

indexNames = df4[ df4['GR10mEspaciam'] == -999.25 ].index
df4.drop(indexNames, inplace=True)

fig, ((ax1, ax2, ax3, ax4)) = plt.subplots(1, 4)


ax1.plot( df.GR50m_Espaciam, df.DEPT)
ax2.plot( df2.GR100m_Espaciam, df2.DEPT)
ax3.plot( df3.GR2mEspaciam, df3.DEPT)
ax4.plot( df4.GR10mEspaciam, df4.DEPT)

plt.show()
