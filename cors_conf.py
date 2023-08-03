from google.cloud import storage


def cors_configuration(bucket_name):
    """버킷의 CORS 정책 구성을 설정합니다"""

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    bucket.cors = [
        {
            "origin": ["*"],
            "responseHeader": ["Content-Type", "x-goog-resumable"],
            "method": ["PUT", "POST", "GET"],
            "maxAgeSeconds": 3600,
        }
    ]

    bucket.patch()

    print("Set CORS policies for bucket {} is {}".format(bucket.name, bucket.cors))
    return bucket

# Windows: $env:GOOGLE_APPLICATION_CREDENTIALS="D:\Python_FastCampus\shrinkers_gcp_key\service_account_file.json"


cors_configuration("shrinkers-project")
