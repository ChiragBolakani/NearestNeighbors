import datetime
import logging
import sys
import re

def validate_date(date):
    try:
        datetime.datetime.strptime(date, r"%Y-%m-%d")
        return True, None
    except ValueError as e:
        return False, e

class Logger:
    def __init__(self, filename='', name='', fileLocation = '',fileMode = 'w', loggerLevel = 'debug', logFormatter = None, loggerType='console') -> None:
        self.name = name
        self.fileName = filename
        self.fileLocation = fileLocation
        self.fileMode = fileMode
        self.level = loggerLevel
        
        # print(self.loggerObject.__format__())


        self.createLogger()
        self.createHandler(loggerType)
        self.setFormat(logFormatter)
        self.setLoggerLevel(loggerLevel)
        self.connectHandler()

    
    def removeHandler(self):
        '''
        Remove all handlers which are connected to the logger object
        '''
        for i in self.loggerObject.handlers:
            print('Removing Handler %s' % i)
            self.loggerObject.removeHandler(i)

    def createHandler(self, loggerType='console'):
        loggerType = (loggerType.strip()).lower()
        if loggerType == 'console':
            # Only relevant for the handlers attached to the console handler
            self.removeHandler()
            self.logHandler = logging.StreamHandler(stream=sys.stdout)
#            self.logHandler = ConsoleHandler()
        elif loggerType == 'file':
            self.logHandler = logging.FileHandler('{fileName}.log'.format(fileName = self.fileName) ,mode=self.fileMode)
        else:
            self.logHandler = None
        self.loggerType = loggerType

    def setFormat(self, formatter):
        if not formatter:
            formatter = logging.Formatter('%(asctime)s %(levelname)-8s : %(module)s.%(funcName)s() => %(message)s', )
        self.logHandler.setFormatter(formatter)
        self.formatter = formatter

    def createLogger(self):
        self.loggerObject = logging.getLogger(self.name)

    def setLoggerLevel(self, level):
        if self.level == 'error':
            self.loggerObject.setLevel(logging.ERROR)
        elif self.level == 'info':
            self.loggerObject.setLevel(logging.INFO)
        elif self.level == 'debug':
            self.loggerObject.setLevel(logging.DEBUG)

    def connectHandler(self):
        self.loggerObject.addHandler(self.logHandler)
    
    def getLogger(self):
        return self.loggerObject

def create_logger(loggerType='console'):
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    log_obj = Logger(logFormatter=formatter, filename=str(datetime.date.today()), loggerType=loggerType, fileMode='a')
    return log_obj.getLogger()

# log = create_logger()
# log.error("fsfsfsfsfsf")
# log.debug("jrpowrpowr")
# log.info("dm;lamdmw")
# validate_date("2023-15-09")

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
            failure_reason.append(("{};{}").format(step['step'], step['msg'])
                                    )
    return failure_reason

def checkWordsInComment(comment):
    pattern = r"(?u)\b\w\w+\b"
    matches = re.findall(pattern=pattern, string=comment)
    return (len(matches), matches)