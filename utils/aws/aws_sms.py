import boto3
import csv

accesskey = ''
secretkey = ''
region = ''
# region = 'us-east-1'

sns = boto3.client('sns', aws_access_key_id=accesskey, aws_secret_access_key=secretkey, region_name=region)


def send_sms():
    sns.publish(
        PhoneNumber='+81' + '',
        Message='テスト',
        MessageAttributes={
            "AWS.SNS.SMS.SenderID": {'StringValue': "Name",
                                     'DataType': "String"},
            "AWS.SNS.SMS.SMSType": {'StringValue': "Transactional",
                                    'DataType': "String"}
            }
        )


if __name__ == '__main__':
    send_sms()
