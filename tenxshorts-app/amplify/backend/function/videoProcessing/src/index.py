import json
import traceback

def response_proxy(data):
	'''
	For HTTP status codes, you can take a look at https://httpstatuses.com/
	'''
	response = {}
	response["isBase64Encoded"] = False
	response["statusCode"] = data["statusCode"]
	response["headers"] = {}
	if "headers" in data:
		response["headers"] = data["headers"]
	response["body"] = json.dumps(data["body"])
	return response

def request_proxy(data):
	request = {}
	request = data
	if data["body"]:
		request["body"]=json.loads(data["body"])
	return request

def handler(event, context):
    body = json.loads(event['body'])
    response = {}
    response = {
    "isBase64Encoded": False,
    "statusCode": 200,
    "headers": {'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'},
    "body": body
    }
		
    return response_proxy(response)