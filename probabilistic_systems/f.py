# -*- coding: utf-8 -*-
# python 3.5

import numpy as np
import matplotlib.pyplot as plt
import math
# from scipy.stats import norm

#################################
# Parameter
data_length = 40
particle_number = 300
sigma_v = 5
sigma_w = 80
dimension = 2

u_list = np.zeros(data_length * 2).reshape(-1, dimension)
for i in range(data_length):
    u_list[i] = np.array([np.random.randint(16), np.random.randint(9)])


#################################
# State equation
# x(t+1) = f(x(t)) + N(0, sigma_v)
# y(t) = g(x(t)) + N(0, sigma_w)
def g(x):
    return x**3


# x = matrix.shape(2,1),  u = matrix.shape(2, 1)
def x_next(x, u, sig_v=1):
    x = x.reshape(dimension, 1)
    u = u.reshape(dimension, 1)
    v = np.random.multivariate_normal([0, 0], [[sig_v, 0], [0, sig_v]])
    return np.array((np.matrix([[1, 0], [0, 1]])*x + np.matrix([[1, 0], [0, 1]])*u).reshape(1, -1) + v)


def y(x, sig_w):
    return g(x) + np.random.multivariate_normal([0, 0], [[sig_w, 0], [0, sig_w]])


#################################
# Create Data_Set

TrueData = np.zeros(data_length * 2).reshape(-1, dimension)
for i in range(1, data_length):
    TrueData[i] = x_next(TrueData[i-1], u_list[i-1], sigma_v)

ObserveData = np.zeros(data_length * 2).reshape(-1, dimension)
for i in range(data_length):
    ObserveData[i] = y(TrueData[i], sigma_w)


##################################################################
# ParticleFilter
class ParticleFilter:
    def __init__(self, y_list, x_next, u, g, sig_w, particle_number, dimension):
        self.u_list = u
        self.dimension = dimension
        self.x_next = x_next
        self.u = u
        self.g = g
        self.y_list = y_list
        self.sig_w = sig_w
        self.particle_number = particle_number

        self.X = np.zeros(particle_number * self.dimension)
        self.X_weight = np.ones(particle_number)

    # init particle by Uniform Distribution
    def init_particle(self):
        for i in range(self.particle_number * self.dimension):
            self.X[i] = (np.random.rand()-0.5)*100
        self.X = self.X.reshape(-1, 2)

    def status_translate(self, u):
        for i in range(self.particle_number):
            self.X[i] = self.x_next(self.X[i], u)

    # likelihood = (1/sqrt(2*pi*sig_w)) * exp(-(y-g(x))**2 / sig_w**2)
    def likelihood(self, x, y):
        return np.exp(- np.linalg.norm(y - self.g(x)) / self.sig_w**2)

    def set_weight(self, y):
        for i in range(self.particle_number):
            self.X_weight[i] *= self.likelihood(self.X[i], y)

    def weight_normalization(self):
        sum_weight = sum(self.X_weight)
        for i in range(self.particle_number):
            self.X_weight[i] = (self.X_weight[i])/sum_weight

    def resample(self):
        X_resapmle = np.zeros(self.particle_number * self.dimension).reshape(-1, dimension)
        k = 0
        samples = np.random.multinomial(self.particle_number, self.X_weight)
        for i, n in enumerate(samples):
            for j in range(n):
                X_resapmle[k] = self.X[i]
                k += 1
        W_resample = np.ones(self.particle_number)
        return X_resapmle, W_resample

    def filter_step(self, y, u):
        """
        1. status translate
        2. set weight(by calculate likelihood)
        3. weight normalization
        4. resample -> value of x (by mean)
        """
        self.status_translate(u=u)
        self.set_weight(y)
        self.weight_normalization()
        X_resapmle, W_resample = self.resample()
        return X_resapmle, W_resample

    def run_filter(self):
        X_list = np.zeros([len(self.y_list), self.particle_number, self.dimension])
        X_value_list = np.zeros([len(self.y_list), self.dimension])

        self.init_particle()

        for i in range(len(self.y_list))[1:]:
            self.X, self.X_weight = self.filter_step(self.y_list[i], self.u_list[i-1])
            X_list[i] = self.X
            X_value_list[i] = (np.mean(self.X, axis=0))  # predict x  = mean(X)
            """
            mu, std = norm.fit(self.X)
            X_value_list[i] = mu
            """
        return X_list, X_value_list

# ParticleFilter END
##################################################################

# Run
p1 = ParticleFilter(y_list=ObserveData, x_next=x_next, u=u_list, g=g, sig_w=sigma_w, particle_number=particle_number, dimension=dimension)
particle_list, predict_data = p1.run_filter()


# Evaluate
PF_deviation = np.zeros(data_length)
for i in range(10, data_length):
    PF_deviation[i] = np.linalg.norm(predict_data[i] - TrueData[i])
sigma_PF = math.sqrt(sum(PF_deviation)/data_length)

print("Standard deviation of ParticleFilter is: %f" % sigma_PF)


# Prepare for Plot
TrueData_X = np.zeros(data_length)
TrueData_Y = np.zeros(data_length)
for i in range(data_length):
    TrueData_X[i] = TrueData[i][0]
    TrueData_Y[i] = TrueData[i][1]

predict_data_X = np.zeros(data_length)
predict_data_Y = np.zeros(data_length)
for i in range(data_length):
    predict_data_X[i] = predict_data[i][0]
    predict_data_Y[i] = predict_data[i][1]

particle_list_extend = np.zeros(data_length * particle_number * dimension).reshape(-1, dimension)
for i in range(data_length):
    for j in range(particle_number):
        particle_list_extend[i * particle_number + j] = particle_list[i][j]

particle_list_X = np.zeros(data_length * particle_number)
particle_list_Y = np.zeros(data_length * particle_number)
for i in range(data_length * particle_number):
    particle_list_X[i] = particle_list_extend[i][0]
    particle_list_Y[i] = particle_list_extend[i][1]


# Plot (True - Observe - PF)
plt.figure(1, figsize=(16, 9))
plt.grid(True, color=(0.2, 0.2, 0.2))
plt.plot(particle_list_X, particle_list_Y, '.', label="Particle", color="blue")
plt.plot(TrueData_X, TrueData_Y, '--', label="True Value", color="green", linewidth=2)
plt.plot(predict_data_X, predict_data_Y, label="Predict Value", color="red", linewidth=1)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Particle Filter")
plt.legend()
plt.show()
