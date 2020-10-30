APP_SERVER = "http://localhost:5000"


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
