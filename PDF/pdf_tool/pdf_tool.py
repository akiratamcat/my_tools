"""
PDF ツール
結合、分割、回転、テキストと画像を抽出。


### pip ###

python.exe -m pip install --upgrade pip

pip install --upgrade chardet
pip install --upgrade pillow
pip install --upgrade pymupdf
pip install --upgrade pytesseract
pip install --upgrade TkEasyGUI

"""

import os
import re
from enum import StrEnum, auto
from typing import Any, Optional

import chardet
import pymupdf as mupdf
import pytesseract as ocr
import TkEasyGUI as eg
from chardet.resultdict import ResultDict
from PIL import Image

# ---------------------------------------------------------------------------
# Enum 他


# Enum ログの出力レベル
class LOGLEVEL(StrEnum):
    LOG_ONLY = auto()
    POPUP_INFO = auto()
    POPUP_ERROR = auto()


# ---------------------------------------------------------------------------
# global 変数


# 文字コード判定関係
ENCODING_CONFIDENCE: float = 0.5


# Page segmentation mode のオプションを定義
psm_options: list[tuple[int, str]] = [
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


# ---------------------------------------------------------------------------
# GUI定義


# GUI レイアウト定義
# PDF 結合処理フレーム
MyFrame_merge: eg.Frame = eg.Frame(
    "PDFを結合",
    [
        [
            eg.Text("1個目のPDF"),
            eg.Input(key="merge_pdf1", size=(50, 1)),
            eg.FileBrowse(),
        ],
        [
            eg.Text("2個目のPDF"),
            eg.Input(key="merge_pdf2", size=(50, 1)),
            eg.FileBrowse(),
        ],
        [
            eg.Text("出力フォルダ"),
            eg.Input(key="merge_output_folder", size=(50, 1)),
            eg.FolderBrowse(),
        ],
        [eg.Button("結合", size=(8, 2))],
    ],
)

# GUI レイアウト定義
# PDF 分割処理フレーム
MyFrame_split: eg.Frame = eg.Frame(
    "PDFを分割",
    [
        [
            eg.Text("分割するPDF"),
            eg.Input(key="split_pdf", size=(50, 1)),
            eg.FileBrowse(),
        ],
        [
            eg.Text("分割するページ番号"),
            eg.Input(key="split_page", size=(6, 1)),
            eg.Text(" 1箇所のみ指定可"),
        ],
        [
            eg.Text("出力フォルダ "),
            eg.Input(key="split_output", size=(50, 1)),
            eg.FolderBrowse(),
        ],
        [eg.Button("分割", size=(8, 2))],
    ],
)

# GUI レイアウト定義
# PDF 回転処理フレーム
MyFrame_rotate: eg.Frame = eg.Frame(
    "PDFを回転",
    [
        [
            eg.Text("回転するPDF"),
            eg.Input(key="rotate_pdf", size=(50, 1)),
            eg.FileBrowse(),
        ],
        [
            eg.Text("回転するページ番号"),
            eg.Input(key="rotate_pages", size=(20, 1)),
            eg.Text(" カンマ区切りで複数指定可能"),
        ],
        [
            eg.Text("回転方向    "),
            eg.Combo(
                ["左へ90度", "右へ90度", "180度"],
                key="rotate_direction",
                default_value="左へ90度",
                size=(12, 8),
            ),
        ],
        [
            eg.Text("出力フォルダ"),
            eg.Input(key="rotate_output", size=(50, 1)),
            eg.FolderBrowse(),
        ],
        [eg.Button("回転", size=(8, 2))],
    ],
)

# GUI レイアウト定義
# PDF テキストと画像を抽出する処理フレーム
MyFrame_extract_text_and_images: eg.Frame = eg.Frame(
    "PDFからテキストと画像を抽出",
    [
        [
            eg.Text("抽出元のPDF"),
            eg.Input(key="extract_pdf", size=(50, 1)),
            eg.FileBrowse(),
        ],
        [
            eg.Text("出力フォルダ   "),
            eg.Input(key="extract_output", size=(50, 1)),
            eg.FolderBrowse(),
        ],
        [
            eg.Text("OCR有効化   "),
            eg.Combo(["ON", "off"], key="ocr_onoff", default_value="off", size=(8, 2)),
            eg.Text("検出言語"),
            eg.Combo(
                ocr.get_languages(config=""),
                default_value="jpn",
                key="ocr_language",
                size=(12, 8),
            ),
        ],
        [
            eg.Text("セグメントモード"),
            eg.Combo(
                [f"{option[0]} - {option[1]}" for option in psm_options],
                default_value="3 - 完全自動ページセグメンテーション、OSDなし",
                key="ocr_psm_options",
                size=(40, 10),
            ),
        ],
        [eg.Button("テキストと画像を抽出", size=(18, 2))],
    ],
)

# GUI レイアウト定義
# Window 全体レイアウト
MyLayout: list[list[Any]] = [
    [MyFrame_merge, MyFrame_split],
    [MyFrame_rotate, MyFrame_extract_text_and_images],
    [eg.Output(key="log", size=(114, 8))],
]


# ---------------------------------------------------------------------------
# 各処理


# ログ出力
def print_log(outstring: str, level: LOGLEVEL = LOGLEVEL.LOG_ONLY) -> None:
    main_window["log"].print(outstring)
    if level == LOGLEVEL.LOG_ONLY:
        return
    if level == LOGLEVEL.POPUP_INFO:
        eg.popup_info(outstring)
    if level == LOGLEVEL.POPUP_ERROR:
        eg.popup_error(outstring)


# allowed_charsに含まれていない文字がsに含まれているかをチェック
def contains_only_specified_chars(s: str, allowed_chars: str) -> bool:
    pattern = f"^[{re.escape(allowed_chars)}]*$"
    return bool(re.match(pattern, s))


# ２個の PDF を結合する
def merge_pdfs(pdf1_path: str, pdf2_path: str, output_folder: str) -> bool:
    try:
        # 結合する PDF1, PDF2 を両方とも開く
        pdf1: mupdf.Document = mupdf.open(pdf1_path)
        pdf2: mupdf.Document = mupdf.open(pdf2_path)

        # １個目のPDFのベース名を得る
        base_name: str = pdf1_path.split("/")[-1].split(".")[0]

        # PDF1 の末尾に PDF2 を挿入する
        pdf1.insert_pdf(pdf2)

        # 結果を出力する
        pdf1.save(f"{output_folder}/{base_name}_merge.pdf")

        # PDF ファイルを全て閉じる
        pdf1.close()
        pdf2.close()

        return True
    except Exception as e:
        print_log(f"PDF 結合中にエラーが発生しました。: {e}", LOGLEVEL.POPUP_ERROR)
        return False


# PDF を指定したページで分割する
def split_pdf(pdf_path: str, split_page: int, output_folder: str) -> bool:
    try:
        # 分割元の PDF0 を開く
        pdf0: mupdf.Document = mupdf.open(pdf_path)

        # 分割元のベース名を得る
        base_name: str = pdf_path.split("/")[-1].split(".")[0]

        # 分割結果の PDF1 PDF2 を空っぽの PDF として準備する。
        pdf1: mupdf.Document = mupdf.open()
        pdf2: mupdf.Document = mupdf.open()

        # 分割元 PDF0 をページごとにループして、現在のページ番号が区切りの
        # ページ番号の前か後かで PDF1 と PDF2 へ振り分ける
        for page_num in range(len(pdf0)):
            if page_num < split_page:
                pdf1.insert_pdf(pdf0, from_page=page_num, to_page=page_num)
            else:
                pdf2.insert_pdf(pdf0, from_page=page_num, to_page=page_num)

        # 分割結果の PDF1 PDF2 を出力する
        pdf1.save(f"{output_folder}/{base_name}_split_1.pdf")
        pdf2.save(f"{output_folder}/{base_name}_split_2.pdf")

        # PDF ファイルを全て閉じる
        pdf0.close()
        pdf1.close()
        pdf2.close()

        return True

    except Exception as e:
        print_log(f"PDF 分割中にエラーが発生しました。: {e}", LOGLEVEL.POPUP_ERROR)
        return False


# PDF の指定したページを、指定した方向へ回転する
def rotate_pdf(
    pdf_path: str,
    pages_to_rotate: list[int],
    direction: str,
    output_folder: str,
) -> bool:
    try:
        # 回転元 PDF を開く
        pdf1: mupdf.Document = mupdf.open(pdf_path)

        # 回転元 PDF のベース名を得る
        base_name: str = pdf_path.split("/")[-1].split(".")[0]

        # PDFのページ数を得る
        page_max: int = len(pdf1)

        # 指定されたページ番号ごとに処理
        page_num: int = 0
        for page_num in pages_to_rotate:
            # 指定されたページ番号が妥当ならば
            if (page_num > 0) and (page_num < page_max):
                # 対象ページを読み込み
                page: mupdf.Page = pdf1.load_page(page_num - 1)  # ※ PyMuPDF ページ番号は 0 開始
                # 回転
                if direction == "右へ90度":
                    page.set_rotation(90)
                elif direction == "左へ90度":
                    page.set_rotation(-90)
                elif direction == "180度":
                    page.set_rotation(180)

        # 結果を保存
        pdf1.save(f"{output_folder}/{base_name}_rotate.pdf")

        # PDF ファイルを全て閉じる
        pdf1.close()

        return True

    except Exception as e:
        print_log(f"PDF 回転中にエラーが発生しました。: {e}", LOGLEVEL.POPUP_ERROR)
        return False


# PDF からテキストと画像を抽出
def extract_text_and_images(
    pdf_path: str,
    output_folder: str,
    ocr_on: bool = False,
    ocr_lang: str = "jpn",
    orc_segment_mode: int = 3,
) -> bool:
    try:
        # 抽出元 PDF を開く
        pdf1: mupdf.Document = mupdf.open(pdf_path)

        # ファイルのベース名を得る
        base_name: str = pdf_path.split("/")[-1].split(".")[0]

        # PDF をページごとに
        for page_num in range(len(pdf1)):
            # ページロード
            page: mupdf.Page = pdf1.load_page(page_num)

            # テキスト抽出
            text: str = page.get_text("text")

            # テキストの文字コードを判定
            # 文字コードを判定できなかった場合は utf-8 とみなす
            result: ResultDict = chardet.detect(text.encode())
            detected_encoding: Optional[str] = (
                result["encoding"] if result["confidence"] > ENCODING_CONFIDENCE else "utf-8"
            )

            # テキストファイル出力
            with open(
                f"{output_folder}/{base_name}_page_{page_num + 1}.txt",
                "w",
                encoding=detected_encoding,
            ) as text_file:
                text_file.write(text)

            # ページ内の画像のリストを得る
            image_list: list[tuple] = page.get_images(full=True)

            # 画像出力
            # ページ内の画像のリストを順に処理
            for img_index, img in enumerate(image_list):
                # 画像データと画像情報を得る
                xref: int = img[0]  # 画像参照番号
                base_image: dict[Any, Any] = pdf1.extract_image(xref)
                image_bytes: bytes = base_image["image"]
                image_ext: str = base_image["ext"]

                # 画像ファイルを出力
                fname: str = f"{base_name}_page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
                fullpath: str = f"{output_folder}/{fname}"
                with open(
                    fullpath,
                    "wb",
                ) as image_file:
                    image_file.write(image_bytes)

                # 画像に対する OCR 処理
                if ocr_on:
                    # 画像ファイルからテキストを抽出
                    im = Image.open(fullpath)
                    text_from_image: str = ocr.image_to_string(
                        im,
                        lang=ocr_lang,
                        config=f"--psm {orc_segment_mode}",
                    )
                    im.close()

                    # 文字コードを検出
                    result = chardet.detect(text.encode())
                    detected_encoding = result["encoding"] if result["confidence"] > ENCODING_CONFIDENCE else "utf-8"

                    # OCR 処理結果をテキストファイルに出力
                    with open(
                        f"{output_folder}/{base_name}_page_{page_num + 1}_img_OCR_{img_index + 1}.txt",
                        "w",
                        encoding=detected_encoding,
                    ) as text_file:
                        text_file.write(text_from_image)

        # PDF ファイルを全て閉じる
        pdf1.close()

        return True

    except Exception as e:
        print_log(f"PDF からテキストと画像の抽出中にエラーが発生しました。: {e}", LOGLEVEL.POPUP_ERROR)
        return False


# ---------------------------------------------------------------------------
# global code
# メイン処理

# GUI ウィンドウ作成
main_window = eg.Window("PDF ツール", MyLayout)

# GUI イベントループ
while True:
    # イベント情報取得
    event, values = main_window.read()

    ret: bool = False

    # ウィンドウクローズ
    if event == eg.WINDOW_CLOSED:
        break

    # PDF 結合
    if event == "結合":
        # 設定内容チェック
        if os.path.isfile(values["merge_pdf1"]) and values["merge_pdf1"].lower().endswith(".pdf") == ".pdf":
            print_log(f"[{event}] PDF を指定してください。", LOGLEVEL.POPUP_ERROR)
            continue
        if os.path.isfile(values["merge_pdf2"]) and values["merge_pdf2"].lower().endswith(".pdf") == ".pdf":
            print_log(f"[{event}] PDF を指定してください。", LOGLEVEL.POPUP_ERROR)
            continue
        if not os.path.exists(values["merge_output_folder"]):
            print_log(f"[{event}] 出力先を指定してください。", LOGLEVEL.POPUP_ERROR)
            continue

        # 処理
        ret = merge_pdfs(values["merge_pdf1"], values["merge_pdf2"], values["merge_output_folder"])

        # 結果通知
        if ret:
            print_log(
                "[%s] %s と %s を結合して %s へ出力しました。"
                % (
                    event,
                    values["merge_pdf1"],
                    values["merge_pdf2"],
                    values["merge_output_folder"],
                ),
                LOGLEVEL.POPUP_INFO,
            )
        continue

    # PDF 分割
    if event == "分割":
        # 設定内容チェック
        if os.path.isfile(values["split_pdf"]) and values["split_pdf"].lower().endswith(".pdf") == ".pdf":
            print_log(f"[{event}] PDF を指定してください。", LOGLEVEL.POPUP_ERROR)
            continue
        values["split_page"] = values["split_page"].replace(" ", "")  # 半角空白除去
        if int(values["split_page"]) < 1:
            print_log(f"[{event}] ページ番号の内容が正しくありません。", LOGLEVEL.POPUP_ERROR)
            continue
        if not os.path.exists(values["split_output"]):
            print_log(f"[{event}] 出力先を指定してください。", LOGLEVEL.POPUP_ERROR)
            continue

        # 処理
        ret = split_pdf(
            values["split_pdf"],
            int(values["split_page"]),
            values["split_output"],
        )

        # 結果通知
        if ret:
            print_log(
                "[%s] %s をページ番号 %s で分割して %s へ出力しました。"
                % (event, values["split_pdf"], values["split_page"], values["split_output"]),
                LOGLEVEL.POPUP_INFO,
            )
        continue

    # PDF 回転
    if event == "回転":
        # 設定内容チェック

        if os.path.isfile(values["rotate_pdf"]) and values["rotate_pdf"].lower().endswith(".pdf") == ".pdf":
            print_log(f"[{event}] PDF を指定してください。", LOGLEVEL.POPUP_ERROR)
            continue
        values["rotate_pages"] = values["rotate_pages"].replace(" ", "")  # 半角空白除去
        if not contains_only_specified_chars(values["rotate_pages"], "1234567890, "):
            print_log(f"[{event}] ページ番号の内容が正しくありません。", LOGLEVEL.POPUP_ERROR)
            continue
        if not os.path.exists(values["rotate_output"]):
            print_log(f"[{event}] 出力先を指定してください。", LOGLEVEL.POPUP_ERROR)
            continue

        # 入力されているページ番号をカンマで区切って List へ変換
        pages_to_rotate: list = list(map(int, values["rotate_pages"].split(",")))

        # 処理
        ret = rotate_pdf(
            values["rotate_pdf"],
            pages_to_rotate,
            values["rotate_direction"],
            values["rotate_output"],
        )

        # 結果通知
        if ret:
            main_window["log"].print(
                "[%s] %s のページ番号 %s を %s して %s へ出力しました。"
                % (
                    event,
                    values["rotate_pdf"],
                    values["rotate_pages"],
                    values["rotate_direction"],
                    values["rotate_output"],
                ),
            )
        continue

    # PDF からテキストと画像を抽出
    if event == "テキストと画像を抽出":
        # 設定内容チェック
        if os.path.isfile(values["extract_pdf"]) and values["extract_pdf"].lower().endswith(".pdf") == ".pdf":
            print_log(f"[{event}] PDF を指定してください。", LOGLEVEL.POPUP_ERROR)
            continue
        if not os.path.exists(values["extract_output"]):
            print_log(f"[{event}] 出力先を指定してください。", LOGLEVEL.POPUP_ERROR)
            continue

        # 処理
        if values["ocr_onoff"] == "off":
            # OCR 処理無し
            ret = extract_text_and_images(values["extract_pdf"], values["extract_output"])
        elif values["ocr_onoff"] == "ON":
            # OCR 処理あり
            ret = extract_text_and_images(
                values["extract_pdf"],
                values["extract_output"],
                True,
                values["ocr_language"],
                values["ocr_psm_options"].split(" ")[0],
            )

        # 結果通知
        if ret:
            print_log(
                "[%s] %s からテキストと画像を抽出して %s へ出力しました。"
                % (event, values["extract_pdf"], values["extract_output"]),
                LOGLEVEL.POPUP_INFO,
            )
        continue

# GUI イベントループ を抜けた後の処理
main_window.close()

# ---------------------------------------------------------------------------
