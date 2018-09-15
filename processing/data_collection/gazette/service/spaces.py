import os

from decouple import config

import boto3


class Spaces(object):

    def __init__(self):
        session = boto3.session.Session()
        self.client = session.client(
            's3',
            region_name=config('SPACES_REGION', ''),
            endpoint_url=config('SPACES_ENDPOINT_URL', ''),
            aws_access_key_id=config('SPACES_ACCESS_KEY_ID', ''),
            aws_secret_access_key=config('SPACES_SECRET_ACCESS_KEY', '')
        )

    def upload_file(self, file_path):
        self.client.upload_file(
            file_path,
            config('SPACES_NAME', default=''),
            file_path
        )
