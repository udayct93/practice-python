import os
from datetime import datetime
import boto3
profile_name = 'dev'
start_with = "2020/04/29"
lambda_name = '/aws/lambda/CMReconProcess-{}'.format(profile_name)
# lambda_name = '/aws/lambda/TelematicsQualcommInbound-{}'.format(profile_name)
# lambda_name = '/aws/lambda/TelematicsDispatchEngine-{}'.format(profile_name)
aws_creds = {
    "region_name": 'us-east-1',
    "verify": 'D:/Users/turamau/.aws/cacert.pem',
    "use_ssl": True
}
os.environ["AWS_PROFILE"] = profile_name
client = boto3.client('logs', **aws_creds)
date_ = lambda_name.split("/")[-1].split("-")[0] + \
    "/" + start_with + "/" + profile_name
response = client.describe_log_streams(
    logGroupName=lambda_name,
    logStreamNamePrefix=start_with,
    descending=True,
    limit=50
)
print(response)
lt = []


def get_event(event_stream, next_token):
    resp = client.get_log_events(
        logGroupName=lambda_name,
        logStreamName=event_stream,
        startFromHead=True,
        nextToken=next_token
    )
    # print(resp)
    lt.append(resp["events"])
    # print(lt)
    if "nextForwardToken" in resp.keys():
        fk = resp["nextForwardToken"]
        # print(fk)
        if next_token != fk:
            get_event(event_stream, fk)


if not os.path.exists(date_):
    os.makedirs(date_)
for stream in response["logStreams"]:
    stream_name = stream["logStreamName"]
    if not str(stream_name).startswith(start_with):
        continue
    resp1 = client.get_log_events(
        logGroupName=lambda_name,
        logStreamName=stream_name,
        startFromHead=True,
    )
    lt.append(resp1["events"])
    if "nextForwardToken" in resp1:
        get_event(stream_name, resp1["nextForwardToken"])
    dt_object = str(datetime.fromtimestamp(stream["creationTime"]/1000))
    file_name = "{}_{}.txt".format(
        "_".join(dt_object.split()[0].split("-")),
        "_".join("_".join(dt_object.split()[1].split(":")).split(".")))
    print(stream_name, file_name)
    f = open(date_ + "/" + file_name, "w")
    for x1 in lt:
        for y1 in x1:
            f.write(y1["message"])
    f.close()
    lt = []
