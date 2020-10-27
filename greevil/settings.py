APP_SERVER = "http://localhost:5000"


class AWS:
    cognitoUserPoolId = "us-east-1_RthhXV3XY"
    cognitoUserPoolClientId = "20piadmcfn4hkt62oipkq5matk"
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
