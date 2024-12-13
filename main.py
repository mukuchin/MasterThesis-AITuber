"""
メイン処理
"""

from response_talker import talk_response
from dify_response_getter import get_dify_response, user
from user_prompt import query


def main():
    # Dify APIにリクエストを送信して応答を取得
    response = get_dify_response(query, user)
    # 応答を音声に変換して再生
    talk_response(response)


if __name__ == "__main__":
    main()
