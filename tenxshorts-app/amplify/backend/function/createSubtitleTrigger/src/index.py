import json
import boto3

def handler(event, context):
    print('received event:')
    print(event)

    # Create an AWS Lambda client
    lambda_client = boto3.client('lambda')

    # Invoke the target Lambda function
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:eu-west-2:254108557594:function:createSubtitle-staging',
        InvocationType='Event',
        Payload=json.dumps(event)
    )

    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Subtitle ok')
    }