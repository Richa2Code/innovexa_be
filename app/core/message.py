"""
Static API response and logger messages.
"""


class SuccessMessage:
    SERVER_HEALTHY = "Server is Healthy!"
    RESPONSE_FETCHED_SUCCESSFULLY = "Response Fetched Successfully"
    USER_REGISTERED_SUCCESSFULLY = "User Registered Successfully!"
    USER_VERIFICATION_EMAIL_SEND = "User Verification Email Sent"
    USER_OTP_VERIFIED_SUCCESSFULLY = "User OTP Verified Successfully"
    COUNTRIES_FETCHED_SUCCESSFULLY = "Countries Fetched Successfully"
    STATES_FETCHED_SUCCESSFULLY = "States Fetched Successfully"
    DISTRICTS_FETCHED_SUCCESSFULLY = "Districts Fetched Successfully"


class ErrorMessage:
    TOKEN_EXPIRE = "Token Expired"
    INVALID_TOKEN = "Token Invalid"
    INTERNAL_SERVER_ERROR = "Internal Server Error"
    UNAUTHORIZED_ACCESS = "You are not Authorized to Access!"
    INVALID_CREDENTIALS = "Invalid Credentials"
    USER_ALREADY_EXIST = "User Already Exists"
    ROLE_NOT_FOUND = "Role Not Found!"
    USER_ALREADY_VERIFIED = "User Already Verified"
    OTP_EXPIRED = "OTP Expired!"
    OTP_INVALID = "OTP Invalid!"
    COUNTRY_ID_REQUIRED = "Country ID is Required"
    STATE_ID_REQUIRED = "State ID is Required"


class LoggerMessage:
    ExpiredSignatureError_Logtext = "user_id :: {user_id} & error :: {e}"

