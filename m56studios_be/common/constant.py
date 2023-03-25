import os
import glob

# String constants
SOMETHING_WENT_WRONG_MSG = "Something went wrong, please try again"
SUCCESS_MSG = "Successful"
MISSING_PARAMETER = "Missing parameter"
INVALID_PARAMETER = "Invalid parameter"
INVALID_REQUEST_TRY_AGAIN = "Invaild request, try again!"
ID_DOES_NOT_EXIST = "Id does not exist"
INCORRECT_USERNAME = "Incorrect username"
INCORRECT_PASSWORD = "Incorrect password"
INVALID_DATA_FOR_OPTIONS = "Invalid data for options"
MISSING_STATUS = "Missing status"
# Number constants
ERROR_RESPONSE_CODE = 0
SUCCESS_RESPONSE_CODE = 1
RESPONSE_STATUS_200 = 200
RESPONSE_STATUS_400 = 400
RESPONSE_STATUS_500 = 500
RESPONSE_STATUS_202 = 202

# Environment variable path
ENVIRONMENT_VARIABLE_DIR_PATH = "../env"
MYSQL_ENV_VARIABLE_PATH = os.path.join(
    ENVIRONMENT_VARIABLE_DIR_PATH, "mysqldb.env")

ALL_ENV_VARIABLE_FILES = glob.glob(ENVIRONMENT_VARIABLE_DIR_PATH + "/*.env")

MANDATORY_EXCEL_FILEDS = [
    "ISIMAGEAHINT",
    "QUESTION",
    "RESRCURL",
    "CATEGORY",
    "DIFFICULT",
    "CHOICE",
    "RIGHT_ANSWER",
    "ID"
]

MANDATORY_EXCEL_FILEDS_INHOUSE_QUESTIONS = [
    "ISIMAGEAHINT",
    "QUESTION",
    "RESRCTYPE",
    "REVEALIMAGEURL",
    "RESRCURL",
    "CATEGORY",
    "DIFFICULT",
    "CHOICE",
    "RIGHT_ANSWER",
    "ID"
]

VALID_FILTER_FIELDS = [
    "category",
    "difficulty_level",
    "qn_submitted_date"
]

CATEGORY_CHAPTER = {
    "PEOPLE": 11,
    "POLITICS": 1,
    "BUSINESS & TECH": 7,
    "CARS": 8,
    "ART": 10,
    "TRUE OR FALSE": 1,
    "I SPY": 6,
    "WHO's THIS": 1,
    "MATH": 3,
    "SCIENCE": 5,
    "FOOD": 1,
    "HISTORY": 4,
    "BOOKS": 2,
    "LIFESTYLE": 9,
    "MUSIC": 1,
    "WORD JAM": 1,
    "GEOGRAPHY": 1,
    "SPORTS": 1,
    "ENTERTAINMENT": 1,
    "HANX MOVIES": 1
}