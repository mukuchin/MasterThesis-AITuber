"""
メイン処理
"""

from response_talker import talk_response
from dify_response_getter import get_dify_response
from record_and_recognize import record_and_recognize


def main():
    # 会話ID
    conversation_id = ""

    while True:
        # 録音と音声認識を行い、認識結果を取得
        transcript = record_and_recognize()

        # Dify APIにリクエストを送信して応答, 会話IDを取得
        response, conversation_id = get_dify_response(transcript, conversation_id)

        # <END_OF_CONVERSATION>が含まれている場合は会話終了
        if "<END_OF_CONVERSATION>" in response:
            # 含まれている場合は削除
            response = response.replace("<END_OF_CONVERSATION>", "")
            print(f"respose: {response}", flush=True)
            print(f"conversation_id: {conversation_id}", flush=True)

            # # 応答を音声に変換して再生
            # talk_response(response)

            break
        else:
            # 含まれていない場合はそのまま処理を続行
            response = response.replace("<END_OF_CONVERSATION>", "")
            print(f"respose: {response}", flush=True)
            print(f"conversation_id: {conversation_id}", flush=True)
            # talk_response(response)


if __name__ == "__main__":
    main()
