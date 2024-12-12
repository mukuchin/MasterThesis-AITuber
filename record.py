import pyaudio
import threading

start_key = "s"
stop_key = "e"

stop_recording_flag = False


def wait_for_stop_key(stop_key="e"):
    """
    終了キー(stop_key)が入力されるまで待機するスレッド関数。
    入力されればstop_recording_flagをTrueにして録音を止める。
    """
    global stop_recording_flag
    print(f"'{stop_key}'と入力しEnterで録音終了します。")
    while True:
        user_input = input("> ")
        if user_input.strip() == stop_key:
            stop_recording_flag = True
            break


def play_audio(frames, rate=44100, channels=1, format=pyaudio.paInt16):
    """
    framesに格納された音声データを再生する関数。
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, output=True)

    print("録音された音声を再生します...")
    for frame in frames:
        stream.write(frame)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("再生終了")


if __name__ == "__main__":
    # 's'と入力するまで待機して録音開始
    print(f"'{start_key}'と入力しEnterで録音開始します。")
    while True:
        user_input = input("> ")
        if user_input.strip() == start_key:
            break

    # 録音開始準備
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
    )

    frames = []

    # 録音停止キー待機用のスレッドを開始
    t = threading.Thread(target=wait_for_stop_key, args=(stop_key,))
    t.start()

    print("録音開始...")
    # stop_recording_flagがTrueになるまで録音し続ける
    while not stop_recording_flag:
        data = stream.read(1024)
        frames.append(data)

    print("録音終了")

    # リソースクリーンアップ
    stream.stop_stream()
    stream.close()
    p.terminate()

    t.join()  # 停止キー待機スレッド終了待ち

    # 録音データを再生
    play_audio(frames)
