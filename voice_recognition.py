import pyaudio
import threading
import io
import wave
import speech_recognition as sr

start_key = "s"
stop_key = "e"
stop_recording_flag = False


def wait_for_stop_key(stop_key="e"):
    """
    stop_keyが入力されるまで待機し、その後録音停止フラグをTrueにする。
    """
    global stop_recording_flag
    print(f"'{stop_key}'と入力しEnterで録音終了します。", flush=True)
    while True:
        user_input = input("> ")
        if user_input.strip() == stop_key:
            stop_recording_flag = True
            break


def record_and_recognize():
    """
    1回分の録音→認識のフローを行う。
    認識に成功すればtranscriptを返す。
    認識に失敗すればNoneを返す。
    """
    global stop_recording_flag
    stop_recording_flag = False  # 再録音時にフラグリセット

    # 's'で録音開始トリガー
    print(f"'{start_key}'と入力しEnterで録音開始します。", flush=True)
    while True:
        user_input = input("> ")
        if user_input.strip() == start_key:
            break

    # PyAudioで録音準備
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
    )

    frames = []

    # 別スレッドで録音終了キー待ち
    t = threading.Thread(target=wait_for_stop_key, args=(stop_key,))
    t.start()

    print("録音開始...録音終了後、認識結果を表示します。", flush=True)

    # stop_recording_flagがTrueになるまで録音ループ
    while not stop_recording_flag:
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    print("録音終了", flush=True)

    # リソース解放
    stream.stop_stream()
    stream.close()
    p.terminate()

    t.join()

    # 録音データをメモリ上でWAV化
    buf = io.BytesIO()
    wf = wave.open(buf, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b"".join(frames))
    wf.close()
    buf.seek(0)

    # SpeechRecognitionでまとめて認識
    r = sr.Recognizer()
    with sr.AudioFile(buf) as source:
        audio_data = r.record(source)

    # 音声認識中であることを表示
    print("音声認識中...", flush=True)

    try:
        transcript = r.recognize_google(audio_data, language="ja-JP")
    except sr.UnknownValueError:
        transcript = None
    except sr.RequestError:
        transcript = "[認識リクエストエラー]"

    if transcript is not None and transcript != "[認識リクエストエラー]":
        print("=== 認識結果 ===", flush=True)
        print(transcript, flush=True)
        return transcript
    else:
        if transcript is None:
            print("認識できませんでした。もう一度録音します。", flush=True)
        else:
            print(
                "認識リクエストエラーが発生しました。もう一度録音します。", flush=True
            )
        return None


if __name__ == "__main__":
    while True:
        result = record_and_recognize()
        if result is not None:
            # 認識成功
            print("録音・認識が正常に完了しました。", flush=True)
            break
        else:
            # 認識失敗→もう一度録音
            continue
