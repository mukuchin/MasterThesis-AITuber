"""
Dify APIにリクエストを送信し、応答を取得する関数を定義している
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
# 環境変数から取得するため、ターミナルで `export USER_MAIL=ユーザーのメールアドレス` として設定しておく
USER_MAIL = os.getenv("USER_MAIL")


def get_dify_response(query: str, conversation_id: str = "") -> str:
    """
    Dify APIにリクエストを送信し、応答を取得する関数
    """

    # 回答を生成していることを表示
    print("回答生成中...", flush=True)

    # ヘッダーの設定
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    # リクエストデータの設定
    data: Dict[str, any] = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "conversation_id": conversation_id,
        "user": {"email": USER_MAIL},
    }

    # リクエストを送信
    response = requests.post(BASE_URL, headers=headers, json=data)
    response.raise_for_status()

    # 応答、会話ID、イベントを返す
    return (
        response.json()["answer"],
        response.json()["conversation_id"],
    )
