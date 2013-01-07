from django.conf import settings

PASSBOOK_CERT = getattr(settings, 'PASSBOOK_CERT', '')
PASSBOOK_CERT_KEY = getattr(settings, 'PASSBOOK_CERT_KEY', '')
