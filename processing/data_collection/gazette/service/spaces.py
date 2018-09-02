import os

import boto3


class Spaces(object):

    def __init__(self):
        session = boto3.session.Session()
        self.client = session.client(
            's3',
            region_name=os.getenv('SPACES_REGION'),
            endpoint_url=os.getenv('SPACES_ENDPOINT_URL'),
            aws_access_key_id=os.getenv('SPACES_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('SPACES_SECRET_ACCESS_KEY')
        )

    def upload_file(self, file_path):
        self.client.upload_file(file_path, 'test-scrapy', file_path)
