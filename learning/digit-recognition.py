import numpy as np
import matplotlib.pyplot as pt
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


data = pd.read_csv('datasets/train.csv').as_matrix()
clf = DecisionTreeClassifier()

train_data = data[0:21000, 1:]
train_label = data[0:21000, 0]

clf.fit(train_data, train_label)

test_data = data[21000:, 1:]
test_label = data[21000:, 0]

# d = test_data[10]
# d.shape = (28, 28)
# pt.imshow(255 - d, cmap='gray')
# print(clf.predict([test_data[10]]))
# pt.show()


prediction = clf.predict(test_data)
count = 0
for i in range(0, 21000):
    count += 1 if prediction[i] == test_label[i] else 0
print('Accuracy: ' + str(count / 210) + '%')
