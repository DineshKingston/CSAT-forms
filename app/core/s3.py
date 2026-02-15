import boto3
from botocore.exceptions import ClientError
from typing import Optional
import uuid
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class S3Manager:
    """AWS S3 manager for file uploads"""
    
    def __init__(self):
        self.s3_client = None
        self.bucket_name = settings.AWS_S3_BUCKET_NAME
        self.enabled = False
        
        # Only initialize if credentials are provided
        if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
            logger.warning("AWS credentials not configured. S3 uploads will be disabled.")
            return
        
        if not settings.AWS_S3_BUCKET_NAME:
            logger.warning("AWS S3 bucket name not configured. S3 uploads will be disabled.")
            return
        
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            
            # Verify bucket exists and we have access
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            self.enabled = True
            logger.info(f"✅ S3 connection verified: {self.bucket_name}")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                logger.error(f"S3 bucket '{self.bucket_name}' not found. S3 uploads disabled.")
            elif error_code == '403':
                logger.error(f"Access denied to S3 bucket '{self.bucket_name}'. Check permissions.")
            else:
                logger.error(f"S3 initialization failed: {str(e)}. S3 uploads disabled.")
            self.s3_client = None
        except Exception as e:
            logger.error(f"S3 initialization failed: {str(e)}. S3 uploads disabled.")
            self.s3_client = None
    
    def upload_file(
        self, 
        file_content: bytes, 
        file_extension: str,
        folder: str = "screenshots"
    ) -> Optional[str]:
        if not self.enabled or not self.s3_client:
            logger.warning("S3 uploads are disabled. Skipping upload.")
            return None
        
        try:
            # Generate unique filename
            filename = f"{folder}/{uuid.uuid4()}.{file_extension}"
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=file_content,
                ContentType=f"image/{file_extension}"
            )
            
            # Generate URL
            url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
            logger.info(f"File uploaded successfully: {url}")
            return url
            
        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {str(e)}")
            return None
    
    def delete_file(self, file_url: str) -> bool:
        """Delete file from S3 using its URL"""
        try:
            # Extract key from URL
            key = file_url.split(f"{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/")[1]
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            logger.info(f"File deleted successfully: {key}")
            return True
            
        except (ClientError, IndexError) as e:
            logger.error(f"Failed to delete file from S3: {str(e)}")
            return False


# Global S3 manager instance
s3_manager = S3Manager()
