"""
Dify APIの設定
"""

import requests
from typing import Dict
import os


# Dify APIの認証キー
# 環境変数から取得するため、ターミナルで `export DIFY_API_KEY=Dify APIの認証キー` として設定しておく
API_KEY = os.getenv("DIFY_API_KEY")
# Dify APIのベースURL
BASE_URL = "https://api.dify.ai/v1/chat-messages"
# ユーザーのメールアドレス
user_mail = "haruto.mukuno@gmail.com"


def get_dify_response(query: str) -> str:
    """
    Dify APIにリクエストを送信し、応答を取得する関数
    """

    # ヘッダーの設定
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    # リクエストデータの設定
    data: Dict[str, any] = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "user": user_mail,
    }

    # リクエストを送信
    response = requests.post(BASE_URL, headers=headers, json=data)
    response.raise_for_status()

    # 応答テキストを返す
    return response.json()["answer"]
