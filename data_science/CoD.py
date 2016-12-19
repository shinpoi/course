import matplotlib.pyplot as plt
import numpy as np
import math


x = np.arange(1, 20, 0.1)
y = np.array([ (math.sin(x_var) + np.random.normal(0, 0.7)) for x_var in x])

f7 = np.polyfit(x, y, 7)
f10 = np.polyfit(x, y, 10)
fmax = np.polyfit(x, y, 50)

plot = plt.plot(x, y, '.', color='blue')
plot = plt.plot(x, np.poly1d(f7)(x), 'r', label="underfitting", color='black')
plot = plt.plot(x, np.poly1d(f10)(x), 'r', label="fit", color='green')
plot = plt.plot(x, np.poly1d(fmax)(x), 'r', label="overfitting", color='red')

plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()