"""
---------------------------------------------------------------------
OCR
---------------------------------------------------------------------

Tesseract OCR のWindowsインストーラをダウンロードしてインストール
https://github.com/UB-Mannheim/tesseract/wiki
https://github.com/tesseract-ocr/tesseract/releases
https://github.com/tesseract-ocr/tessdata_best/blob/main/jpn.traineddata
https://github.com/tesseract-ocr/tessdata_best/blob/main/jpn_vert.traineddata

python.exe -m pip install --upgrade pip
pip install --upgrade chardet
pip install --upgrade pillow
pip install --upgrade pytesseract
pip install --upgrade TkEasyGUI
pip install --upgrade PyInstaller

"""

import os
from typing import Any, List, Optional

import chardet
import pytesseract
import TkEasyGUI as eg
from chardet.resultdict import ResultDict
from PIL import Image, UnidentifiedImageError

# Page segmentation modeのオプションを定義
psm_options: List[tuple[int, str]] = [
    (0, "0 - 方向とスクリプトの検出 (OSD) のみ"),
    (1, "1 - 自動ページセグメンテーション、OSDあり"),
    (2, "2 - 自動ページセグメンテーション、OSDなし"),
    (3, "3 - 完全自動ページセグメンテーション、OSDなし"),
    (4, "4 - 段落のセグメンテーション"),
    (5, "5 - 垂直方向のテキスト行のセグメンテーション"),
    (6, "6 - 単一の均一なブロックのセグメンテーション"),
    (7, "7 - 単一のテキスト行のセグメンテーション"),
    (8, "8 - 単一の単語のセグメンテーション"),
    (9, "9 - 単一の円形の単語のセグメンテーション"),
    (10, "10 - 単一の文字のセグメンテーション"),
    (11, "11 - スパーステキスト。OSDなし"),
    (12, "12 - スパーステキスト。OSDあり"),
    (13, "13 - 原画像のセグメンテーション"),
]

# GUIのレイアウトを定義
MyLayout: List[Any] = [
    [eg.Text("OCR処理を行う画像ファイルを選択してください:")],
    [
        eg.Input(size=(50, 1)),
        eg.FileBrowse(file_types=(("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"),)),
    ],
    [eg.Text("OCR言語を選択してください:")],
    [
        eg.Combo(
            pytesseract.get_languages(config=""),
            default_value="jpn",
            key="language",
            size=(10, 8),
        )
    ],
    [eg.Text("Tesseract Layoutを選択してください:")],
    [
        eg.Combo(
            [f"{option[0]} - {option[1]}" for option in psm_options],
            default_value="3 - 完全自動ページセグメンテーション、OSDなし",
            key="layout",
            size=(50, 8),
        )
    ],
    [eg.Text("テキストの保存先を選択してください:")],
    [
        eg.Input(size=(50, 1)),
        eg.FolderBrowse(key="save_path"),
    ],
    [eg.Button("処理"), eg.Button("終了")],
]

# ウィンドウを作成
window = eg.Window("OCR処理", MyLayout)

while True:
    event, values = window.read()
    if event == eg.WINDOW_CLOSED or event == "終了":
        break
    if event == "処理":
        image_path: str = values[0]
        language: str = values["language"]
        layout: str = values["layout"].split(" ")[0]  # レイアウト番号を取得
        save_path: str = values[1]
        if image_path and save_path:
            try:
                # 選択された画像ファイルに対してOCRを実行
                custom_config = f"--oem 3 --psm {layout}"
                text: str = pytesseract.image_to_string(Image.open(image_path), lang=language, config=custom_config)

                # 文字コードを検出
                result: ResultDict = chardet.detect(text.encode())
                detected_encoding: Optional[str] = result["encoding"]

                # エンコーディングがNoneの場合や信頼度が低い場合の処理
                if detected_encoding is None or result["confidence"] < 0.5:
                    errMessage: str = "警告 :文字コード判定に自信がありません。デフォルトのUTF-8で処理します。"
                    eg.popup_warning(errMessage)
                    detected_encoding = "utf-8"  # デフォルトのエンコーディングをUTF-8に設定

                # 画像ファイルのベース名を取得し、テキストファイル名を作成
                base_name: str = os.path.splitext(os.path.basename(image_path))[0]
                text_file_name: str = os.path.normpath(os.path.join(save_path, f"{base_name}.txt"))

                # OCR結果をテキストファイルに保存
                with open(text_file_name, "w", encoding=detected_encoding) as text_file:
                    text_file.write(text)

                eg.popup(f"OCR処理が完了しました。結果は '{text_file_name}' に保存されました。")
            except FileNotFoundError:
                eg.popup_error("ファイルが見つかりません。正しいパスを指定してください。")
            except UnidentifiedImageError:
                eg.popup_error("画像ファイルの読み込みに失敗しました。対応している画像形式か確認してください。")
            except pytesseract.TesseractError as e:
                eg.popup_error(f"OCR処理中にエラーが発生しました: {str(e)}")
            except Exception as e:
                eg.popup_error(f"予期しないエラーが発生しました: {str(e)}")


window.close()
