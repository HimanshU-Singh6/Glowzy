from google.cloud import storage
from app.config import Config
import uuid
from datetime import timedelta
import os

# Ensure the credentials are loaded
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = Config.GOOGLE_APPLICATION_CREDENTIALS

BUCKET_NAME = Config.GOOGLE_CLOUD_BUCKET_NAME

def upload_file_to_gcs(file_obj, user_id, folder='images'):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)

        # Generate a unique filename
        filename = f"{folder}/{user_id}/{uuid.uuid4().hex}_{file_obj.filename}"

        # Create a blob object
        blob = bucket.blob(filename)

        # Upload the file object
        blob.upload_from_file(file_obj, content_type=file_obj.content_type)

        # Generate a Signed URL for accessing the uploaded file
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(hours=1),  # URL will be valid for 1 hour
            method="GET"
        )

        return {
            'message': 'File uploaded successfully',
            'file_url': url,
            'gcs_path': filename
        }
        
    except Exception as e:
        raise Exception(f"Failed to upload image to GCS: {str(e)}")

# def upload_files_to_gcs(file_objs, user_id, folder='uploads'):
#     try:
#         storage_client = storage.Client()
#         bucket = storage_client.bucket(BUCKET_NAME)

#         results = []

#         for file_obj in file_objs:
#             filename = f"{folder}/{user_id}/{uuid.uuid4().hex}_{file_obj.filename}"
#             blob = bucket.blob(filename)

#             blob.upload_from_file(file_obj, content_type=file_obj.content_type)

#             # Generate a Signed URL (valid for 1 hour)
#             url = blob.generate_signed_url(
#                 version="v4",
#                 expiration=timedelta(hours=1),  # URL valid for 1 hour
#                 method="GET"
#             )

#             results.append({
#                 'message': 'File uploaded successfully',
#                 'file_url': url,
#                 'gcs_path': filename
#             })

#         return results

#     except Exception as e:
#         raise Exception(f"Failed to upload files: {str(e)}")