import os
from django.core.exceptions import ValidationError
from common.constant import MANDATORY_EXCEL_FILEDS, VALID_FILTER_FIELDS, MANDATORY_EXCEL_FILEDS_INHOUSE_QUESTIONS

# from app.question.model import question

def is_path_exists(path):
    return os.path.exists(path)
    
def set_environment_variables(env_file_path):
    try:
        # os.environ[env_file_path]
        from dotenv import load_dotenv
        load_dotenv(env_file_path)
    except:
        import platform
        if platform.system() == 'Windows' and env_file_path and is_path_exists(path=env_file_path):
            from dotenv import load_dotenv
            load_dotenv(env_file_path)
            os.environ[env_file_path] = str(True)

def validate_capitalized(value):
    if value[0] != value[0].capitalize():
        raise ValidationError('First letter is not capitalized value: %(value)s',
                              code='invalid',
                              params={'value': value})

def isValidExcelFile(data):
    first_row = None
    if not len(data) > 0:
        return False
    first_row = data[0]
    is_valid_data = True
    for each_field in MANDATORY_EXCEL_FILEDS:
        if each_field not in first_row:
            is_valid_data = False
    
    if not is_valid_data:
        is_valid_data = True
        for each_field in MANDATORY_EXCEL_FILEDS_INHOUSE_QUESTIONS:
            if each_field not in first_row:
                is_valid_data = False

    return is_valid_data

def isValidFilterType(data):
    if not len(data) > 0:
        return False
    if data in VALID_FILTER_FIELDS:
        return True
    return False

def runSystemCheck(questionObj):

    status = "valid"
    inavlid_reason = ""
    # Check if question is duplicate
    
    # if question.objects.get(original_ques_id=questionObj["original_ques_id"]):
    #     print("ALREADY EXIST")
    #     print("HERE IS QUES ID {}".format(questionObj["original_ques_id"]))
    # # Check if question string is less than 60 chars
    # if len(questionObj["question"]) > 60:
    #     print("INVALID QUESTION STRING")
    #     print("HERE IS QUES ID {}".format(questionObj["original_ques_id"]))
    # # Check if each option is less than 30 chars

    # # Check if first char of option and question is capital

    questionObj["system_check"] = status
    questionObj["invalid_reason"] = inavlid_reason
    
    return questionObj