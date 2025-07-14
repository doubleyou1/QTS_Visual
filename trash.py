import numpy as np

array4d = np.zeros((4,3,2,3))

for i in range(len(array4d)):
    print("i")
    for j in range(len(array4d[i])):
        print("j")
        for k in range(len(array4d[i][j])):
            print("k")
            print(array4d[i][j][k])
            