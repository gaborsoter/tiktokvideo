import json

def handler(event, context):  
    request_body = json.loads(event['body'])
    response_body = {
    'message': f'Hello, {request_body["name"]}!'}

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(response_body)
    }