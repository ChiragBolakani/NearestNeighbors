import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import warnings

warnings.filterwarnings('ignore')

def vectorizeReason(reason):
    vectorizer = TfidfVectorizer(analyzer="word")
    vectors = vectorizer.fit_transform([reason])
    if vectors.size==1:
        vector_single_elem = np.append(vectors, 0, 1)
        return vector_single_elem.toarray()
    # print(vectors.size)
    return vectors.toarray()

pkl_files = [f for f in os.listdir("setup_data_column_encoded")]
# le_pkl_files = [f for f in os.listdir("setup_mnemonic_label_encoders")]


meta_data = {}

for pkl_file in pkl_files:
    setup_df = pd.read_pickle("setup_data_column_encoded/" + pkl_file)
    # setup_df.set_index("id", inplace = True)
    # print(setup_df)

    setup_df["reason_encoded"] = None

    try:
        for index, row in setup_df.iterrows():
            setup_df["reason_encoded"].loc[index] = vectorizeReason(row["failed_reasons"])[0]
    except ValueError:
        continue

    
    data = np.array(setup_df[["reason_encoded"]])
    # data
    data_lens = []
    print(pkl_file)
    for encoded_reason in data:
        # print(encoded_reason)
        data_lens.append(len(encoded_reason[0]))
        # data_lens.append(encoded_reason[0].size)

    padded_reason_encoded_temp = []
    for encoded_reason in data:
        data_lens.append(len(encoded_reason[0]))
        # data_lens.append(encoded_reason[0].size)
        padded_reason_encoded_temp.append(np.pad(encoded_reason[0], (0,max(data_lens)-len(encoded_reason[0])), constant_values=(0)))
        # padded_reason_encoded_temp.append(np.pad(encoded_reason[0], (0,max(data_lens)-encoded_reason[0].size), constant_values=(0)))

    meta_data[pkl_file.split(".")[0]] = max(data_lens)

    padded_reason_encoded = np.array(padded_reason_encoded_temp)

    mnemonic_encoded = np.array(setup_df["mnemonic_encoded"])
    x_data = []

    for mnemonic, reason in zip(mnemonic_encoded, padded_reason_encoded):
        x_data.append(np.insert(reason, 0, mnemonic))

    x_data_df = pd.DataFrame({"x_data" : x_data, "id" : np.array(setup_df["id"])})

    with open("x_data_dfs/" + pkl_file, "wb") as f:
        pickle.dump(x_data_df, f)
        f.close()
    
    print(np.array(x_data).shape)
    with open("x_data/" + pkl_file.split(".")[0] + ".pkl", "wb") as f:
        pickle.dump(x_data, f)
        f.close()


with open("meta_data.pkl", "wb") as f:
        pickle.dump(meta_data, f)
        f.close()
    
    # with open("setup_data_column_vectorized/" + pkl_file.split(".")[0] + ".npy", "wb") as f:
    #     np.save(f, padded_reason_encoded)
    #     f.close()
    

    # setup_df.to_pickle("setup_data_column_encoded/" + "encoded_" + pkl_file.split(".")[0]+".pkl")

    # print(setup_df)



