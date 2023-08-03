from django.conf import settings

from storages.utils import setting
from storages.backends.gcloud import GoogleCloudStorage

from urllib.parse import urljoin


class GoogleCloudMediaStorage(GoogleCloudStorage):
    """Django의 미디어 파일에 적합한 GoogleCloudStorage"""

    def __init__(self, *args, **kwargs):
        if not settings.MEDIA_URL:
            raise Exception('MEDIA_URL has not been configured')

        kwargs['bucket_name'] = setting('GS_MEDIA_BUCKET_NAME')
        super(GoogleCloudMediaStorage, self).__init__(*args, **kwargs)

    def url(self, name):
        """Google을 호출하지 않는 .url"""
        return urljoin(settings.MEDIA_URL, name)


class GoogleCloudStaticStorage(GoogleCloudStorage):
    """Django의 정적 파일에 적합한 GoogleCloudStorage"""

    def __init__(self, *args, **kwargs):
        if not settings.STATIC_URL:
            raise Exception('STATIC_URL has not been configured')

        kwargs['bucket_name'] = setting('GS_STATIC_BUCKET_NAME')
        super(GoogleCloudStaticStorage, self).__init__(*args, **kwargs)

    def url(self, name):
        """Google을 호출하지 않는 .url"""
        return urljoin(settings.STATIC_URL, name)
