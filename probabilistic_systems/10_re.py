import matplotlib.pyplot as plt
import math
import numpy as np

# parameter
a = 0.75
mu0 = 0
beta0 = 20
e20 = 0
z0 = 10
sigv1 = 60
sigv2 = 60
x_0 = np.matrix([[mu0], [beta0], [e20]])
A = np.matrix([[a, 0, 0], [0, 1, 0], [0, 0, 0]])
B = np.matrix([[1-a, 0], [0, 0], [0, 1]])
cT = np.matrix([[1], [1], [-1]])
Q = np.diag([60, 60])
R = 0.0001
x0 = np.matrix([[10], [30], [20]])
p = 0
p0 = np.matrix([[1000, 0, 0], [0, 1000, 0], [0, 0, 1000]])
n = 300


def z_set(n, z0):
    z_data = [z0]
    z = z0
    for i in range(1,n):
        z = z + 2*math.cos(0.05*i) + np.random.normal(0, 5)
        z_data.append(z)
    return z_data


def sensor1(z_data, mu0, a, sigv1, beta):
    sensor1_data = []
    mu_data = []
    mu = mu0
    for z in z_data:
        mu = a*mu + (1-a)*np.random.normal(0, sigv1)
        sensor1 = z + mu + beta
        sensor1_data.append(sensor1)
        mu_data.append(mu)
    return np.array(sensor1_data), np.array(mu_data)


def sensor2(z_data, sigv2):
    sensor2_data = []
    e2_data = []
    for z in z_data:
        e2 = np.random.normal(0, sigv2)
        sensor2 = z + e2
        sensor2_data.append(sensor2)
        e2_data.append(e2)
    return np.array(sensor2_data), np.array(e2_data)


# Kalman Filter
def kalmanfilter(y_data, A, B, Q, cT, R, x0, p0, ):
    x_hat = x0
    p_k = p0
    xhat_data = []
    for y_k in y_data:
        x_hat_pri = A * x_hat
        p_pri = A * p_k + A.transpose() + B * Q * B.transpose()
        g = (p_pri * cT) * ((cT.transpose() * p_pri * cT + R)**-1)
        x_hat = x_hat_pri + g * (y_k - cT.transpose() * x_hat_pri)
        p_k = (np.identity(len(x0)) - g * cT.transpose()) * p_pri
        xhat_data.append(x_hat)
    return xhat_data


# create dataset
z_data = z_set(n=n, z0=z0)
sensor1_data, mu_data = sensor1(z_data=z_data, mu0=mu0, a=a, sigv1=sigv1, beta=beta0)
sensor2_data, e2_data = sensor2(z_data=z_data, sigv2=sigv2)

y_data = sensor1_data - sensor2_data

# Run Kalman Filter
xhat_data = kalmanfilter(y_data, A, B, Q, cT, R, x0, p0)

mu_data_hat = [mu.tolist()[0][0] for mu in xhat_data]
e2_data_hat = [mu.tolist()[2][0] for mu in xhat_data]

z_data_hat = sensor2_data - np.array(e2_data_hat)

# plot
plt.rcParams['font.sans-serif'] = ['IPAPGothic']

plt.figure(1)
plt.plot(range(n), sensor1_data, label="センサー１", color="red", linewidth=1)
plt.plot(range(n), z_data, label="真値", color="gray", linewidth=1)
plt.xlabel("k")
plt.ylabel("value")
plt.title("センサー１ - 真値")
plt.legend()

plt.figure(2)
plt.plot(range(n), sensor2_data, label="センサー２", color="blue", linewidth=1)
plt.plot(range(n), z_data, label="真値", color="gray", linewidth=1)
plt.xlabel("k")
plt.ylabel("value")
plt.title("センサー２ - 真値")
plt.legend()

plt.figure(3)
plt.plot(range(n), z_data, label="真値", color="gray", linewidth=1)
plt.plot(range(n), sensor1_data, label="センサー１", color="red", linewidth=1)
plt.plot(range(n), z_data_hat, label="補正値", color="orange", linewidth=1)
plt.xlabel("k")
plt.ylabel("value")
plt.title("真値 - センサー１ - 補正値")
plt.legend()

plt.figure(4)
plt.plot(range(n), z_data, label="真値", color="gray", linewidth=1)
plt.plot(range(n), sensor2_data, label="センサー２", color="blue", linewidth=1)
plt.plot(range(n), z_data_hat, label="補正値", color="orange", linewidth=1)
plt.xlabel("k")
plt.ylabel("value")
plt.title("真値 - センサー２ - 補正値")
plt.legend()

plt.show()
