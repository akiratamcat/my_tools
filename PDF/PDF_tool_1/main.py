from typing import Any, Dict

import TkEasyGUI as sg

from delete_pdf import delete_pdf_pages_window
from merge_pdf import merge_pdf_window
from rotate_pdf import rotate_pdf_pages_window
from split_pdf import split_pdf_window


# メイン関数
def main() -> None:
    # レイアウトの定義
    layout: list[list[Any]] = [
        [sg.Menu([["ファイル", ["終了"]]])],  # メニュー
        [
            sg.Button("PDF ファイルを結合", size=(38, 2), font=("Helvetica", 12), key="MERGE"),
            sg.Button("PDF ファイルを分割", size=(38, 2), font=("Helvetica", 12), key="SPLIT"),
        ],
        [
            sg.Button("指定したページを回転", size=(38, 2), font=("Helvetica", 12), key="ROTATE"),
            sg.Button("指定したページを削除", size=(38, 2), font=("Helvetica", 12), key="DELEET"),
        ],
        [
            sg.Button("指定した位置へPDFファイルを挿入", size=(38, 2), font=("Helvetica", 12), key="INSERT"),
            sg.Button("PDF ファイルからテキストと画像を抽出", size=(38, 2), font=("Helvetica", 12), key="EXTRACT"),
        ],
    ]

    # ウィンドウの作成
    window: sg.Window = sg.Window("PDF ツール", layout, resizable=False, finalize=True)

    # イベントループ
    while True:
        event: str
        values: Dict[str, Any]
        event, values = window.read()

        # ウィンドウが閉じられた場合や終了ボタンが押された場合
        if event in (sg.WIN_CLOSED, "EXIT", "終了"):
            break
        # 結合ボタンが押された場合
        elif event == "MERGE":
            window.hide()
            merge_pdf_window()
            window.un_hide()
            continue
        # 分割ボタンが押された場合
        elif event == "SPLIT":
            window.hide()
            split_pdf_window()
            window.un_hide()
            continue
        # 回転ボタンが押された場合
        elif event == "ROTATE":
            window.hide()
            rotate_pdf_pages_window()
            window.un_hide()
            continue
        # 削除ボタンが押された場合
        elif event == "DELETE":
            window.hide()
            delete_pdf_pages_window()
            window.un_hide()
            continue

    # ウィンドウを閉じる
    window.close()


# メイン関数の呼び出し
if __name__ == "__main__":
    main()
