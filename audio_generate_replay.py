"""
Dify APIで応答を取得し、VOICEVOX coreで音声に変換して再生する
"""

import pyaudio
import wave
import io
import requests
from dify_api_setting import get_dify_response, user
from voicevox_core_setting import core, speaker_id
from user_prompt import query


def play_audio():
    try:
        # Dify APIにリクエストを送信して応答を取得
        answer = get_dify_response(query, user)

        # モデルが読み込まれていない場合は読み込む
        if not core.is_model_loaded(speaker_id):
            core.load_model(speaker_id)

        # テキストを合成してwavデータを取得
        wave_bytes = core.tts(answer, speaker_id)

        # PyAudioを使用して音声データを再生
        p = pyaudio.PyAudio()

        # WAVデータをBytesIOでラップして読み込む
        wave_file = wave.open(io.BytesIO(wave_bytes), "rb")

        # オーディオストリームを開く
        stream = p.open(
            format=p.get_format_from_width(wave_file.getsampwidth()),
            channels=wave_file.getnchannels(),
            rate=wave_file.getframerate(),
            output=True,
        )

        # データを再生
        data = wave_file.readframes(1024)
        while data:
            stream.write(data)
            data = wave_file.readframes(1024)

        # ストリームを終了
        stream.stop_stream()
        stream.close()

        # PyAudioを終了
        p.terminate()

    except requests.RequestException as e:
        print(f"エラーが発生しました: {e}")