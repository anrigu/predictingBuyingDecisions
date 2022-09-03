# -*- coding: utf-8 -*-
"""Product Buy

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wWv-GgJy8rVwBiXT7LqsyzihJtKoxEiR
"""

import pandas as pd
import numpy as np
# Comment out the next two lines after uploading data. Only needs to be done once per session!
from google.colab import files
uploaded = files.upload()
df = pd.read_csv('Buying_decisions_data.csv')
X = df[['Gender', 'Age', 'EstimatedSalary']]
y = df['Purchased']
m = X.shape[0]
a = np.ones((m,1))
X.insert(loc = 0, column = 'Ones', value = a)
X.loc[X['Gender'] == 'Male', 'Gender_Male'] = 1         #1 if male
X.loc[X['Gender'] == 'Female', 'Gender_Male'] = 0       #0 if female
del X['Gender']               
#Comment out the lines below if you want to test non-feature scaling runtime and accuracy
age_std = X['Age'].std()
age_ave = X['Age'].mean()
sala_std = X['EstimatedSalary'].std()
sala_ave = X['EstimatedSalary'].mean()
X['Age'] = (X['Age'].subtract(age_ave)).divide(age_std)
X['EstimatedSalary'] =(X['EstimatedSalary'].subtract(sala_ave)).divide(sala_std)
print(X)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

X_train, X_test, y_train, y_test = X_train.to_numpy(), X_test.to_numpy(), y_train.to_numpy(), y_test.to_numpy()

def sigmoid(x):
 return (1/(1+np.exp(-x)))

def hPredict(theta, X):
  result = [[0 for i in range(len(theta[0]))] for j in range(len(X))]
  # Following code is unvectorized implementation
  # for i in range(len(X)):
  #  # iterate through columns of Y
  #  for j in range(len(theta[0])):
  #      # iterate through rows of Y
  #      for k in range(len(theta)):
  #          result[i][j] += X[i][k] * theta[k][j]
  # return sigmoid(np.array(result))
  return sigmoid(np.matmul(X, theta))

def cost_function(X, y, theta, m):
  y = y.reshape(y.shape[0], 1)
  H = hPredict(theta, X)
  return (sum((y)*np.log(H) + (1-y)*np.log(1-H))) / (-m)

def gradient_descent(theta, X, y, alpha, m):
  H = hPredict(theta, X)
  H = H.reshape((H.shape[0],))
  diff = np.subtract(H, y)
  a = np.matmul(np.transpose(X), diff).reshape((theta.shape[0],1))
  theta = theta - (alpha/m) * a
  return theta

def train(X, y, theta, alfa, m, num_iter):
  for i in range(num_iter):
    theta = gradient_descent(theta, X, y, alfa, m)
    if i % 200== 0:
      print("Cost: ", cost_function(X, y, theta, m))
  return theta

def predict(X, theta, threshold = 0.5):
  a = hPredict(theta, X)
  a [a >= threshold] = 1
  a [a < threshold]  = 0
  return a

def score(y1, y2):
  #y1 is the correct answers
  #y2 is calculated by the model
  y1 = y1.reshape(y1.shape[0], 1)
  y2 = y2.reshape(y2.shape[0], 1)
  y1_not = (1 - y1).reshape(y1.shape[0], 1)
  y2_not = (1 - y2).reshape(y1.shape[0], 1)
  a = np.multiply(y1_not, y2_not) + np.multiply(y1, y2)   
  #1 means  correct prediction, 0 means wrong prediction

  ones_ = np.count_nonzero(a == 1)  #count ones to get the percentage
  return (ones_ / y1.shape[0]) * 100

m = X_train.shape[0]  #number of rows
n = X_train.shape[1]  #number of columns
theta = np.zeros((n, 1))
num_iter = 8000
alpha = 0.1

import timeit

start = timeit.default_timer()
opt_theta = train(X_train, y_train, theta, alpha, m, num_iter)
y_ = predict(X_test, opt_theta)
print("Accuracy: ", score(y_test, y_))
stop = timeit.default_timer()

print('Time: ', stop - start)

