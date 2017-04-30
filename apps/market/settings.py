from apps.settings import BASE_DIR
import os

UPLOAD_URL = 'static/uploads/market'
UPLOAD_ROOT = os.path.join(BASE_DIR, UPLOAD_URL)

PAGE_LIMIT = 20