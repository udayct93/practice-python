import boto3
client=boto3.client('sqs')
recieve_queue_message_response = client.receive_message(
    QueueUrl='https://queue.amazonaws.com/936788838029/CMFSConsume-dev',
    MaxNumberOfMessages=10
)
data = recieve_queue_message_response['Messages'][0]['Body']
f = open("cmf_sqs_response1.txt", "w+")
f.write(data)
print(data)

# sqs_obj = boto3.resource('sqs')
# responce=sqs_obj.rec
# sqs_queue = sqs_obj.get_queue_by_name(QueueName='CMFSConsume-dev')
#
# sqs_msgs = sqs_queue.receive_messages(
#         AttributeNames=['All'],
#         MessageAttributeNames=['All']
#        )
# print(sqs_msgs[0])

# import boto3
#
# # Create SQS client
# client = boto3.client('sqs')
#
# # Create a SQS queue with long polling enabled
# response = client.get_queue_url(
#     QueueName='CMFSConsume',
#     Attributes={'ReceiveMessageWaitTimeSeconds': '20'}
# )
#
# print(response['QueueUrl'])
