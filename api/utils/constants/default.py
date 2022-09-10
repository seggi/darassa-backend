import os

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
