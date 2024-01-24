import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
import pickle
from utils import create_logger

log = create_logger()

try:
    pkl_files = [f for f in os.listdir("setup_columns_extracted_data_with_reason")]
    if len(pkl_files) < 1:
        raise FileNotFoundError("folder setup_columns_extracted_data_with_reason has no files")
    else:
        log.info("Found following files in setup_columns_extracted_data_with_reason : %s", ",".join(pkl_files))

    for pkl_file in pkl_files:
        setup_df = pd.read_pickle("setup_columns_extracted_data_with_reason/" + pkl_file)

        le2 = LabelEncoder()
        le2.fit(setup_df["mnemonic"]) 
        setup_df["mnemonic_encoded"] = le2.transform(setup_df["mnemonic"])
        log.info("Label encoding completed for %s", pkl_file)

        with open("label_encoders/" + pkl_file, "wb") as f:
            pickle.dump(le2, f)
            f.close()
            log.info("Label Encoder object for setup %s stored at %s", pkl_file, "label_encoders/"+pkl_file)

        setup_df.to_pickle("setup_data_column_encoded/" + pkl_file.split(".")[0]+".pkl")

        # log.info(setup_df)

except FileNotFoundError as e:
    log.error(e)
except Exception as e:
    log.exception(e)



