import json
import boto3
def lambda_handler(event, context):
    client = boto3.client(
        "sns")
    client.publish(
        PhoneNumber = event['mobile_number'],
        Message = event['message_value'])
    # TODO implement
    print(event['message_value'])
    print(event['mobile_number'])
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
