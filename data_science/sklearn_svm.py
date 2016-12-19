import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm

# create data
x = np.arange(1, 20, 0.1)
y = np.array([[x_var, x_var + np.random.normal(0, 8)] for x_var in x])

y1 = []
for n in y:
    if n[1] - n[0] + np.random.normal(0, 4) > 0:
        y1.append(n)

y1_x = [y1_v[0] for y1_v in y1]
y2 = []
for n in y:
    if n[0] not in y1_x:
        y2.append(n)

y_data = y1 + y2
y_target = [0 for n in range(len(y1))] + [1 for n in range(len(y2))]
np.array([y_data])
np.array([y_target])

# SVM
svc = svm.SVC(kernel='poly', degree=5)
svc.set_params(C=0.1)

# training
svc.fit(y_data, y_target)

x_c = np.linspace(0, 20, 200)
y_c = np.linspace(-20, 45, 200)
xx, yy = np.meshgrid(x_c, y_c)


z = np.array([[svc.predict([xx[i][j], yy[i][j]])[0] for j in range(len(xx[i]))] for i in range(len(xx))])

plt.contourf(xx, yy, z, 1)
plt.plot([y1_v[0] for y1_v in y1], [y1_v[1] for y1_v in y1], 'o', color='red')
plt.plot([y2_v[0] for y2_v in y2], [y2_v[1] for y2_v in y2], 'o', color='blue')

plt.xlabel("x")
plt.ylabel("y")
plt.show()