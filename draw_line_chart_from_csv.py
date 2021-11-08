import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

function_string = "Inverse Geodesic Length"

df = pd.read_csv(f"{function_string}.csv")
in_x = list(range(162))
line_R = df.iloc[:162,1]
line_ID = df.iloc[162:162*2,1]
line_RD = df.iloc[162*2:162*3,1]
line_IB = df.iloc[162*3:162*4,1]
line_RB = df.iloc[162*4:,1]



fig = plt.figure(function_string, figsize=(8, 8))
plt.plot(in_x, line_R,color="grey",label="Random")
plt.plot(in_x, line_ID,color="r",label="ID")
plt.plot(in_x, line_RD,color="g",label="RD")
plt.plot(in_x, line_IB,color="b",label="IB")
plt.plot(in_x, line_RB,color="y",label="RB")


plt.title(f'{function_string} Evolution')
plt.xlabel('N nodes removed')
plt.ylabel(function_string)
plt.legend()
plt.show()