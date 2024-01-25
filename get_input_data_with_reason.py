import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import create_logger, get_failure_msg, checkWordsInComment

log = create_logger()

def vectorizeReason(reason):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([reason])
    return vectors.toarray()


try:
    files = [f for f in os.listdir("setup_json_data")]
    if len(files) < 1:
        raise FileNotFoundError("folder setup_json_data has no files")
    else:
        log.info("Found following files in folder setup_json_data : %s", ",".join(files))

    for setup_json_file_name in files:
        df = pd.read_json("setup_json_data/" + setup_json_file_name)

        setup_df = df
        log.info("Validating %s for filtering short commments", setup_json_file_name)
        for index, row in setup_df.iterrows():
            len_matches, matches = checkWordsInComment(row.comments)
            if len_matches < 10:
                if any(word in 'rerun re-run overruled overrule Rerun [overruled] pass checked investigation required started' for word in matches):
                    log.info("removed row - %s. index - %s", row.comments.replace("\n", "\\n"), index)
                    setup_df.drop(index=[index])

        failed_reasons_list = []

        for steps in setup_df["result_per_step"]:
            failed_reasons_list.append(",".join(get_failure_msg(steps)))

        setup_df["failed_reasons"] = failed_reasons_list

        processed_cleaned_setup_df = setup_df[["result_per_step", "mnemonic", "fr", "comments", "id", "failed_reasons"]]
        processed_cleaned_setup_df.to_pickle("setup_columns_extracted_data_with_reason/" + setup_json_file_name.split(".")[0]+".pkl")
except FileNotFoundError as e:
    log.exception(e)
except Exception as e:
    log.exception(e)


