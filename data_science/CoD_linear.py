import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 20, 0.1)
y = np.array([(x_var + np.random.normal(0, 5)) for x_var in x])

f1 = np.polyfit(x, y, 1)
fmax = np.polyfit(x, y, 20)

plot = plt.plot(x, y, '.', color='blue')
plot = plt.plot(x, np.poly1d(f1)(x), 'r', label="fit", color='green')
plot = plt.plot(x, np.poly1d(fmax)(x), 'r', label="overfitting", color='red')

plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()