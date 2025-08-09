# app/__init__.py

from flask import Flask, request
import os
import logging
from datetime import timedelta

from .token_manager import TokenCache, get_headers
from .like_routes import like_bp, initialize_routes

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ تعريف السيرفرات حسب المناطق، تمت إضافة منطقة الشرق الأوسط (ME)
SERVERS = {
    "EUROPE": os.getenv("EUROPE_SERVER", "https://clientbp.ggblueshark.com"),
    "IND": os.getenv("IND_SERVER", "https://client.ind.freefiremobile.com"),
    "BR": os.getenv("BR_SERVER", "https://client.us.freefiremobile.com"),
    "ME": os.getenv("ME_SERVER", "https://clientbp.ggblueshark.com")  # ✅ تمت إضافته
}

# ✅ تحميل التوكنات الخاصة بكل سيرفر
token_cache = TokenCache(servers_config=SERVERS)

# ✅ ميدلوير للتعامل مع الـ chunked requests (مهم لبعض السيرفرات)
@app.before_request
def handle_chunking():
    transfer_encoding = request.headers.get("Transfer-Encoding", "")
    if "chunked" in transfer_encoding.lower():
        request.environ["wsgi.input_terminated"] = True

# ✅ تفعيل المسارات الخاصة باللايكات وغيرها
initialize_routes(app, SERVERS, token_cache)