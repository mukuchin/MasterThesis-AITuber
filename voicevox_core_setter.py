"""
VOICEVOX coreの設定
"""

from pathlib import Path
from voicevox_core import VoicevoxCore


# VOICEVOX coreに辞書ファイルのパスを指定して初期化
core = VoicevoxCore(open_jtalk_dict_dir=Path("open_jtalk_dic_utf_8-1.11"))

# ずんだもん、ノーマル
speaker_id = 3
