"""
メイン処理
"""

from response_talker import talk_response
from dify_response_getter import get_dify_response
from user_prompt import tmp_prompt
from record_and_recognize import record_and_recognize


def main():
    transcript = record_and_recognize()
    # transcriptには認識されたテキストが格納されています
    # このテキストを他の処理で利用できます
    # print("メイン処理でテキストを使用可能:", transcript)

    # Dify APIにリクエストを送信して応答を取得
    response = get_dify_response(tmp_prompt)
    # 応答を音声に変換して再生
    talk_response(response)


if __name__ == "__main__":
    main()
