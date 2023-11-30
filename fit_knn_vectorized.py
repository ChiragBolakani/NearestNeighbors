import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import os
import pickle

pkl_files = [f for f in os.listdir("x_data")]

for pkl_file in pkl_files:
    with open("x_data/" + pkl_file, "rb") as f:
        data = np.load(f, allow_pickle=True)
        # print(data)
        # print(np.array(data).shape)
        f.close()

    nbrs = NearestNeighbors(n_neighbors=7, algorithm='ball_tree')

    knn = nbrs.fit(data)
    with open("models/" + pkl_file, "wb") as f:
        pickle.dump(knn, f)
        f.close()

