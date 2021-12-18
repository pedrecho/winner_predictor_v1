import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score, mean_squared_error


data = pd.read_csv("./dataset/" + 'data.csv', sep=',')
# print(data.head())

x_train, x_test, y_train, y_test = (train_test_split(data.iloc[:, 0:-1], data['win'], test_size=0.25))
# print(x_test)
# print(x_train)
# print(y_test)
# print(y_train)


# def print_metrics(y_preds, y):
#     print(f'R^2: {r2_score(y_preds, y)}')
#     print(f'MSE: {mean_squared_error(y_preds, y)}')


nn = MLPClassifier()
nn.fit(x_train, y_train)

count = 0
res = nn.predict(x_test)
# print(res)
# print(y_test)
for i in range(len(res)):
    if res[i] == y_test.values[i]:
        count += 1
print(count, len(res), str(count / len(res) * 100) + '%')




