import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import warnings
from utils import create_logger, checkWordsInStepReason

log = create_logger()

# See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
# removing SettingWithCopyWarning
warnings.filterwarnings('ignore')

def vectorizeReason(reason):
    vectorizer = TfidfVectorizer(analyzer="word")
    vectors = vectorizer.fit_transform([reason])
    # print(reason)
    if vectors.size==1:
        print(reason)
        vector_single_elem = np.append(vectors, 0, 1)
        return vector_single_elem.toarray()
    return vectors.toarray()

try:
    pkl_files = [f for f in os.listdir("validated_setup_data_for_vectorizing")]
    if len(pkl_files) < 1:
        raise FileNotFoundError("folder validated_setup_data_for_vectorizing has no files")
    else:
        log.info("Found following files in folder validated_setup_data_for_vectorizing : %s", ",".join(pkl_files))

    meta_data = {}

    for pkl_file in pkl_files:
        setup_df = pd.read_pickle("validated_setup_data_for_vectorizing/" + pkl_file)
        setup_df["reason_encoded"] = None
        
        for index, row in setup_df.iterrows():
            setup_df["reason_encoded"].loc[index] = vectorizeReason(row["failed_reasons"])[0]
        
        data = np.array(setup_df[["reason_encoded"]])
        data_lens = []

        for encoded_reason in data:
            data_lens.append(len(encoded_reason[0]))

        padded_reason_encoded_temp = []
        for encoded_reason in data:
            data_lens.append(len(encoded_reason[0]))
            padded_reason_encoded_temp.append(np.pad(encoded_reason[0], (0,max(data_lens)-len(encoded_reason[0])), constant_values=(0)))
        
        # print(max(data_lens))

        meta_data[pkl_file.split(".")[0]] = max(data_lens)

        padded_reason_encoded = np.array(padded_reason_encoded_temp)

        mnemonic_encoded = np.array(setup_df["mnemonic_encoded"])
        x_data = []

        for mnemonic, reason in zip(mnemonic_encoded, padded_reason_encoded):
            x_data.append(np.insert(reason, 0, mnemonic))

        # x_data_df = pd.DataFrame({"x_data" : x_data, "id" : np.array(setup_df["id"])})

        # with open("x_data_dfs/" + pkl_file, "wb") as f:
        #     pickle.dump(x_data_df, f)
        #     f.close()
        
        log.info("Total number of rows in %s, max_data_length = %s, x_data_shape = %s", pkl_file.split(".")[0], max(data_lens), np.array(x_data).shape)
        # print(np.array(x_data).shape)
        with open("x_data/" + pkl_file.split(".")[0] + ".pkl", "wb") as f:
            pickle.dump(x_data, f)
            f.close()
            log.info("Vectorizing completed for %s. Stored at %s", pkl_file.split(".")[0], "x_data/" + pkl_file.split(".")[0] + ".pkl")


    with open("meta_data.pkl", "wb") as f:
            pickle.dump(meta_data, f)
            f.close()
            log.info("Meta data for vectorized setups stored in meta_data.pkl")

except ValueError as e:
    log.exception(e)
except FileNotFoundError as e:
    log.exception(e)
except Exception as e:
    log.exception(e)


