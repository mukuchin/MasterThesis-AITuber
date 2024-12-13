from voice_recorder import VoiceRecorder
from voice_recognizer import VoiceRecognizer


def record_and_recognize():
    recorder = VoiceRecorder(start_key="s", stop_key="e")
    recognizer = VoiceRecognizer(language="ja-JP")

    while True:
        frames = recorder.record_audio()
        transcript = recognizer.recognize(frames)

        if transcript is not None and transcript != "[認識リクエストエラー]":
            # 認識成功
            print("=== 認識結果 ===", flush=True)
            print(transcript, flush=True)
            print("録音・認識が正常に完了しました。", flush=True)
            return transcript
        else:
            # 認識失敗またはリクエストエラー
            if transcript is None:
                print("認識できませんでした。もう一度録音します。", flush=True)
            else:
                print(
                    "認識リクエストエラーが発生しました。もう一度録音します。",
                    flush=True,
                )
            # 失敗時はループして再録音
