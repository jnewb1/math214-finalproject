#!/usr/bin/env python

import numpy as np

def power_iteration(A, num_simulations: int):
    # Ideally choose a random vector
    # To decrease the chance that our vector
    # Is orthogonal to the eigenvector

    f = open("e.txt", "w")
    f.write(r"\\\\")
    b_k = np.random.rand(A.shape[1])
    
    k = 0
    f.write(r"$b_{" + str(k )+r"}$ = \begin{bmatrix}" +"\n")
    for c in b_k:
        f.write("{:0.3f}".format(float(c)) + r"\\"+"\n")
    f.write(r"\end{bmatrix} \\\\\\"+"\n")
    for _ in range(num_simulations):
        f.write(r"$b_{" + str(k+1 )+r"}$ = \begin{bmatrix}" +"\n")
        for c in b_k:
            f.write("{:0.3f}".format(float(c)) + r"\\"+"\n")
        f.write(r"\end{bmatrix}A "+"\n")
        # calculate the matrix-by-vector product Ab
        b_k1 = np.dot(A, b_k)
        

        # calculate the norm
        b_k1_norm = np.linalg.norm(b_k1)

        # re normalize the vector
        b_k = b_k1 / b_k1_norm

        f.write(r" = \begin{bmatrix}" +"\n")
        for c in b_k:
            f.write("{:0.3f}".format(float(c)) + r"\\"+"\n")
        f.write(r"\end{bmatrix} "+"\n")

        f.write(r"\\\\\\\\")

        k+=1
    f.close()

    return b_k

print(power_iteration(np.array([
    [0 , 0 , 0 , 0 , 1 , 0 , 0 , 0 , 1 , 0 ],
    [0 , 0 , 1 , 1 , 0 , 0 , 1 , 0 , 0 , 1 ],
    [0 , 1 , 0 , 1 , 0 , 0 , 0 , 0 , 1 , 0 ],
    [0 , 1 , 1 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ],
    [1 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 0 , 1 ],
    [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 0 ],
    [0 , 1 , 0 , 0 , 1 , 0 , 0 , 0 , 1 , 1 ],
    [0 , 0 , 0 , 1 , 1 , 0 , 0 , 0 , 0 , 1 ],
    [1 , 0 , 1 , 1 , 0 , 1 , 1 , 0 , 0 , 0 ],
    [0 , 1 , 0 , 1 , 1 , 0 , 1 , 1 , 0 , 0 ]
    ]),
         10))