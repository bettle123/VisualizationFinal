'''
@author: Su Ming Yi
@date: 12/07/2018
@goal:
    use KDE(x) to detect abnormal temperature 



'''


from sklearn.neighbors.kde import KernelDensity

import numpy as np

np.random.seed(1)
N = 20
X = np.concatenate((np.random.normal(0, 1, int(0.3 * N)),
                    np.random.normal(5, 1, int(0.7 * N))))[:, np.newaxis]

print(X)
kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
score_X = kde.score_samples(X)

print(score_X);

print(X-score_X);