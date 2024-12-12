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


def play_audio(frames, transcript, rate=44100, channels=1, format=pyaudio.paInt16):
    """
    framesに格納されたオーディオデータを最後まで再生する関数。
    再生開始直後に、まとめてtranscriptを表示する。
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, output=True)
    print("録音された音声を再生します...", flush=True)

    # 再生開始直後にテキストをまとめて表示
    print("=== 音声再生中の認識結果（まとめ） ===", flush=True)
    print(transcript, flush=True)

    for frame in frames:
        stream.write(frame)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("再生終了", flush=True)


if __name__ == "__main__":
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

    print("録音開始...録音終了後、音声再生中に認識結果を表示します。", flush=True)

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
    try:
        transcript = r.recognize_google(audio_data, language="ja-JP")
    except sr.UnknownValueError:
        transcript = "[認識できませんでした]"
    except sr.RequestError:
        transcript = "[認識リクエストエラー]"

    # 音声再生中にテキストをまとめて表示
    play_audio(frames, transcript)
