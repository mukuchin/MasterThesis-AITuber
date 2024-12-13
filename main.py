"""
メイン処理
"""

from response_talker import talk_response
from dify_response_getter import get_dify_response
from record_and_recognize import record_and_recognize


def main():
    # 録音と音声認識を行い、認識結果を取得
    transcript = record_and_recognize()

    # Dify APIにリクエストを送信して応答を取得
    response = get_dify_response(transcript)

    # 応答を音声に変換して再生
    talk_response(response)


if __name__ == "__main__":
    main()
