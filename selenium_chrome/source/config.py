import os
from dotenv import load_dotenv
load_dotenv()
# 環境変数を参照

MY_SHIZUDAI_ID = os.getenv('MY_SHIZUDAI_ID')
MY_PASS_WORD = os.getenv('MY_PASS_WORD')
BASE_URL = os.getenv('BASE_URL')
LINE_NOTIFY_TOKEN = os.getenv('LINE_NOTIFY_TOKEN')
LINE_NOTIFY_API = os.getenv('LINE_NOTIFY_API')
