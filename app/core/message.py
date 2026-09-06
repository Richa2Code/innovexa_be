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
    SCHEMES_FETCHED_SUCCESSFULLY = "Schemes Fetched Successfully"
    SCHEME_DETAILS_FETCHED_SUCCESSFULLY = "Scheme Details Fetched Successfully"
    EMI_CALCULATED_SUCCESSFULLY = "EMI Calculated Successfully"
    CHANNEL_PARTNERS_FETCHED_SUCCESSFULLY = "Channel Partners Fetched Successfully"


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
    SCHEME_NOT_FOUND = "Scheme Not Found!"
    INVALID_LOAN_AMOUNT = "Loan Amount must be greater than 0"
    INVALID_TENURE = "Tenure must be greater than 0"
    INTEREST_RATE_REQUIRED = "Interest rate is required or scheme must specify an interest rate"




class LoggerMessage:
    ExpiredSignatureError_Logtext = "user_id :: {user_id} & error :: {e}"

