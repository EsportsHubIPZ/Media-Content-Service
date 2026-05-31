import boto3
from app.config import settings

class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY
        )
        self.bucket = settings.S3_BUCKET_NAME
        self._ensure_bucket()
        
    def _ensure_bucket(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket)
        except:
            self.s3.create_bucket(Bucket=self.bucket)

    def upload_file(self, file_obj, object_name: str, content_type: str):
        self.s3.upload_fileobj(
            file_obj, 
            self.bucket, 
            object_name,
            ExtraArgs={'ContentType': content_type}
        )
        return object_name
