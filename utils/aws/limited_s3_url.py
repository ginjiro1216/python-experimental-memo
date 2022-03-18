import boto3

accesskey = 'ロールのアクセスキーを入力'
secretkey = 'ロールのシークレットキーを入力'
region = 'リージョン'


BUCKET = ''
KEY = ''


def create_limited_s3_url(time):
    s3 = boto3.client(
        service_name='s3',
    )

    presigned_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': BUCKET,
            'Key': KEY
        },
        ExpiresIn=time,
        HttpMethod='GET'
    )

    print(presigned_url)


if __name__ == '__main__':
# //引数に期限の秒数を入力する。最大で7日間までなので、最大の期限を定める場合は、604800を入力する。
    create_limited_s3_url(time=604800)
