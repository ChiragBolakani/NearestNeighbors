import numpy as np
from sklearn.neighbors import NearestNeighbors
import os
import pickle
from utils import create_logger
if 'BUILD_NUMBER' in os.environ:
    from config import K_VALUE, ALGORITHM_FOR_NEIGHBORS
else:
    from local_config import K_VALUE, ALGORITHM_FOR_NEIGHBORS

log = create_logger()

try:
    pkl_files = [f for f in os.listdir("x_data")]
    if len(pkl_files) < 1:
        raise FileNotFoundError("folder x_data has no files")
    else:
        log.info("Found following files in folder x_data : %s", ",".join(pkl_files))

    for pkl_file in pkl_files:
        with open("x_data/" + pkl_file, "rb") as f:
            data = np.load(f, allow_pickle=True)
            f.close()

        nbrs = NearestNeighbors(n_neighbors=K_VALUE, algorithm=ALGORITHM_FOR_NEIGHBORS)

        knn = nbrs.fit(data)
        log.info("Successfully trained KNN model for %s", pkl_file.split(".")[0])

        with open("models/" + pkl_file, "wb") as f:
            pickle.dump(knn, f)
            f.close()
            log.info("KNN model for setup %s stored at %s", pkl_file.split(".")[0], "models/" + pkl_file.split(".")[0])

except FileNotFoundError as e:
    log.error(e)
except Exception as e:
    log.exception(e)
