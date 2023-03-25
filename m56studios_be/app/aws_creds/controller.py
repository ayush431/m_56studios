import os

class GetAwsCredsController():
    def get_object(self):
        return {
            "aws_access_key_id": os.environ.get("ACCESS_KEY_ID"),
            "aws_secret_key": os.environ.get("SECRET_ACCESS_KEY"),
            "bucket_name": os.environ.get("BUCKET_NAME"),
            "region": os.environ.get("REGION"),
            "base_url": os.environ.get("BASE_URL")
        }
        