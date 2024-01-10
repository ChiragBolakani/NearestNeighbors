import pandas as pd
import re
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def get_results_per_step(result_per_step, indicate_error=False):
    '''
    Parse the result_per_step field to a list of elements {'step': ..., 'result': ..., 'msg': ...}
    '''
    if not result_per_step:
        return []

    # TODO: header could contain more than step/result/msg e.g. for init time test => not handled properly
    regex = re.compile(r"(?P<step>^.*);(?P<result>PASS|FAIL|VOID|NOT\sRUN|WARNING|SKIP|UNKNOWN\sRETURN\sVALUE|UNEXPECTED\sRETURN\sVALUE);(?P<msg>.*)", re.DOTALL)
    splitted = result_per_step.split('\n')
    # If the <msg> has a newline we need to make sure we put it back together
    result = []
    for l in splitted:
        match = regex.match(l)
        if match:
            parsed = match.groupdict()
            if indicate_error:
                parsed['error'] = parsed['result'] in ["FAIL", "VOID", "NOT RUN", "WARNING", "UNKNOWN RETURN VALUE", "UNEXPECTED RETURN VALUE"]
            result.append(parsed)
        elif result:
            # Assuming this is a continuation of previous msg so putting it back together
            result[-1]['msg'] += "\n%s" % l
    return result


def get_failure_reason(result_per_step):
    '''
    Get list of (only the) failed steps in format ["<step>;<result>;<msg>", ..]
    '''
    failure_reason = []
    parsed_result = get_results_per_step(result_per_step,indicate_error=True)
    for step in parsed_result:
        if step['error']:
            # failure_reason.append(("{};{};{}").format(step['step'],
            #                                             step['result'],
            #                                             step['msg'].replace('\n', ', '))
            #                         )
            failure_reason.append(("{}").format(step['step'])
                                    )
    return failure_reason

def get_failure_msg(result_per_step):
    '''
    Get list of (only the) failed steps in format ["<step>;<result>;<msg>", ..]
    '''
    failure_reason = []
    parsed_result = get_results_per_step(result_per_step,indicate_error=True)
    for step in parsed_result:
        if step['error']:
            # failure_reason.append(("{};{};{}").format(step['step'],
            #                                             step['result'],
            #                                             step['msg'].replace('\n', ', '))
            #                         )
            failure_reason.append(("{};{}").format(step['step'], step['msg'])
                                    )
    return failure_reason


def vectorizeReason(reason):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([reason])
    return vectors.toarray()

files = [f for f in os.listdir("setup_json_data")]
# print(files)

def checkWordsInComment(comment):
    pattern = r"(?u)\b\w\w+\b"
    matches = re.findall(pattern=pattern, string=comment)
    return (len(matches), matches)


for setup_json_file_name in files:
    # print("reading..." + setup_json_file_name)
    df = pd.read_json("setup_json_data/" + setup_json_file_name)
    df

    # setup_df = df.loc[(df["fr"]!="")]
    setup_df = df
    
    for index, row in setup_df.iterrows():
        len_matches, matches = checkWordsInComment(row.comments)
        if len_matches < 10:
            if any(word in 'rerun re-run overruled overrule Rerun [overruled] pass checked investigation required started' for word in matches):
                # print("short commment")
                print("removed row", row.comments, index)
                setup_df.drop(index=[index])

    # failed_mnemonics_list = []
    failed_reasons_list = []

    for steps in setup_df["result_per_step"]:
        # failed_mnemonics_list.append(",".join(get_failure_reason(steps)))
        failed_reasons_list.append(",".join(get_failure_msg(steps)))
        # chn_ndps_d_DF["failed_test_mnemonics"] = ",".join(get_failure_reason(steps))

    # setup_df["failed_test_mnemonics"] = failed_mnemonics_list
    setup_df["failed_reasons"] = failed_reasons_list

    processed_cleaned_setup_df = setup_df[["result_per_step", "mnemonic", "fr", "comments", "id", "failed_reasons"]]
    # print(processed_cleaned_setup_df)

    processed_cleaned_setup_df.to_pickle("setup_columns_extracted_data_with_reason/" + setup_json_file_name.split(".")[0]+".pkl")

