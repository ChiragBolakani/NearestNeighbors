import pandas as pd
import numpy as np
import os
from utils import create_logger, checkWordsInStepReason
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

log = create_logger()

def vectorizeReason(reason):
    vectorizer = TfidfVectorizer(analyzer="word")
    vectors = vectorizer.fit_transform([reason])
    if vectors.size==1:
        log.info("found step reason with single word - %s", reason)
        vector_single_elem = np.append(vectors, 0, 1)
        return vector_single_elem.toarray()
    return vectors.toarray()


# dict to track on which rows to remove from setups that can cause an issue while vectorizing
setup_rows_to_remove = {}

try:
    pkl_files = [f for f in os.listdir("setup_data_column_encoded")]
    if len(pkl_files) < 1:
        raise FileNotFoundError("folder setup_data_column_encoded has no files")
    else:
        log.info("Found following files in folder setup_data_column_encoded : %s", ",".join(pkl_files))

    for pkl_file in pkl_files:
        log.info("validating %s", pkl_file.split(".")[0])
        setup_df = pd.read_pickle("setup_data_column_encoded/" + pkl_file)
        indices_to_remove_list = []

        try:
            for index, row in setup_df.iterrows():
                if checkWordsInStepReason(row["failed_reasons"]) < 2:
                    setup_df.drop([index], inplace = True)
                    continue
                else:
                    vectorizeReason(row["failed_reasons"])
        except ValueError as e:
            indices_to_remove_list.append(index)


        setup_rows_to_remove[pkl_file] =  indices_to_remove_list

        if indices_to_remove_list!= []:
            log.info("removing rows : %s from %s", indices_to_remove_list, pkl_file)
            setup_df.drop(indices_to_remove_list, inplace=True)
            print(setup_df.head(20))

        with open("validated_setup_data_for_vectorizing/" + pkl_file, "wb") as f:
            pickle.dump(setup_df, f)
            f.close()
            log.info("Successfully validated %s. pkl file storated at %s",pkl_file.split(".")[0] ,"validated_setup_data_for_vectorizing/" + pkl_file)

except Exception as e:
    log.exception(e)
