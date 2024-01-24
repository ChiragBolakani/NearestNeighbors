import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import create_logger, get_failure_msg, checkWordsInComment

log = create_logger()

# def get_results_per_step(result_per_step, indicate_error=False):
#     '''
#     Parse the result_per_step field to a list of elements {'step': ..., 'result': ..., 'msg': ...}
#     '''
#     if not result_per_step:
#         return []

#     # TODO: header could contain more than step/result/msg e.g. for init time test => not handled properly
#     regex = re.compile(r"(?P<step>^.*);(?P<result>PASS|FAIL|VOID|NOT\sRUN|WARNING|SKIP|UNKNOWN\sRETURN\sVALUE|UNEXPECTED\sRETURN\sVALUE);(?P<msg>.*)", re.DOTALL)
#     splitted = result_per_step.split('\n')
#     # If the <msg> has a newline we need to make sure we put it back together
#     result = []
#     for l in splitted:
#         match = regex.match(l)
#         if match:
#             parsed = match.groupdict()
#             if indicate_error:
#                 parsed['error'] = parsed['result'] in ["FAIL", "VOID", "NOT RUN", "WARNING", "UNKNOWN RETURN VALUE", "UNEXPECTED RETURN VALUE"]
#             result.append(parsed)
#         elif result:
#             # Assuming this is a continuation of previous msg so putting it back together
#             result[-1]['msg'] += "\n%s" % l
#     return result


# def get_failure_reason(result_per_step):
#     '''
#     Get list of (only the) failed steps in format ["<step>;<result>;<msg>", ..]
#     '''
#     failure_reason = []
#     parsed_result = get_results_per_step(result_per_step,indicate_error=True)
#     for step in parsed_result:
#         if step['error']:
#             failure_reason.append(("{}").format(step['step'])
#                                     )
#     return failure_reason

# def get_failure_msg(result_per_step):
#     '''
#     Get list of (only the) failed steps in format ["<step>;<result>;<msg>", ..]
#     '''
#     failure_reason = []
#     parsed_result = get_results_per_step(result_per_step,indicate_error=True)
#     for step in parsed_result:
#         if step['error']:
#             failure_reason.append(("{};{}").format(step['step'], step['msg'])
#                                     )
#     return failure_reason

# def checkWordsInComment(comment):
#     pattern = r"(?u)\b\w\w+\b"
#     matches = re.findall(pattern=pattern, string=comment)
#     return (len(matches), matches)

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


