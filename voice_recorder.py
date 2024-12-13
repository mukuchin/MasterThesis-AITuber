import pyaudio
import threading


class VoiceRecorder:
    def __init__(
        self,
        start_key="s",
        stop_key="e",
        rate=44100,
        channels=1,
        chunk=1024,
        format=pyaudio.paInt16,
    ):
        self.start_key = start_key
        self.stop_key = stop_key
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.format = format
        self.stop_recording_flag = False

    def wait_for_stop_key(self):
        """
        stop_keyが入力されるまで待機し、その後録音停止フラグをTrueにする。
        """
        print(f"'{self.stop_key}'と入力しEnterで録音終了します。", flush=True)
        while True:
            user_input = input("> ")
            if user_input.strip() == self.stop_key:
                self.stop_recording_flag = True
                break

    def record_audio(self):
        """
        start_keyが入力されるまで待機し、その後録音を開始。
        stop_keyが入力されると録音を終了し、framesを返す。
        """
        self.stop_recording_flag = False

        print(f"'{self.start_key}'と入力しEnterで録音開始します。", flush=True)
        while True:
            user_input = input("> ")
            if user_input.strip() == self.start_key:
                break

        p = pyaudio.PyAudio()
        stream = p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )

        frames = []

        # 別スレッドで録音終了キー待ち
        t = threading.Thread(target=self.wait_for_stop_key)
        t.start()

        print("録音開始", flush=True)

        # stop_recording_flagがTrueになるまで録音ループ
        while not self.stop_recording_flag:
            data = stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)

        print("録音終了", flush=True)

        # リソース解放
        stream.stop_stream()
        stream.close()
        p.terminate()

        t.join()

        return frames
