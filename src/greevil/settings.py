import os

APP_SERVER = os.environ.get("APP_SERVER", "http://34.229.62.221/")


class AWS:
    cognitoUserPoolId = "us-east-1_N3LQnEiUA"
    cognitoUserPoolClientId = "2ar481vjkra0k54fu6c6vre6m0"
    awsRegion = 'us-east-1'

    def __init__(self):
        pass


def aws_message_processor(request):
    aws = AWS()
    aws_context = {
        "cognitoUserPoolId": aws.cognitoUserPoolId,
        "cognitoUserPoolClientId": aws.cognitoUserPoolClientId,
        "awsRegion": aws.awsRegion
    }
    return aws_context
