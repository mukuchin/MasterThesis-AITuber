import io
import wave
import speech_recognition as sr


class VoiceRecognizer:
    def __init__(self, language="ja-JP"):
        self.language = language

    def recognize(self, frames, rate=44100, channels=1, format_width=2):
        """
        framesの音声データをWAVに変換して音声認識を行い、その結果を返す。
        認識できなければNoneを返す。
        """
        buf = io.BytesIO()
        # WAV化
        wf = wave.open(buf, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(format_width)  # 16bitの場合は2
        wf.setframerate(rate)
        wf.writeframes(b"".join(frames))
        wf.close()
        buf.seek(0)

        r = sr.Recognizer()
        with sr.AudioFile(buf) as source:
            audio_data = r.record(source)

        print("音声認識中...", flush=True)
        try:
            transcript = r.recognize_google(audio_data, language=self.language)
            return transcript
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return "[認識リクエストエラー]"
