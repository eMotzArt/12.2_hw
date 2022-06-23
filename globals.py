### глобальные переменные путей
import os
BASE_PATH = os.path.dirname(__name__)
POSTS_FILE = os.path.join(BASE_PATH, "posts.json")
UPLOAD_FOLDER = os.path.join(BASE_PATH, 'uploads', 'images')