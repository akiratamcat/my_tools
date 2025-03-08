import os
from typing import Any, List

import fitz  # PyMuPDF
import TkEasyGUI as sg


# PDF ページ削除ウィンドウを表示する関数
def delete_pdf_pages_window() -> None:
    # レイアウトの定義
    layout: List[List[Any]] = [
        [sg.Text("PDF の指定したページを削除", font=("Helvetica", 14))],
        [
            sg.Text("ページを削除するPDFファイル名"),
            sg.InputText(key="FILE_PATH", enable_events=True, size=(80, 1)),
            sg.FileBrowse(file_types=(("PDF Files", "*.pdf"),)),
        ],
        [
            sg.Frame(
                "PDF ファイル情報",
                layout=[
                    [sg.Text("ファイル名: ", size=(15, 1)), sg.Text("", size=(30, 1), key="FILE_NAME")],
                    [sg.Text("総ページ数: ", size=(15, 1)), sg.Text("", size=(30, 1), key="TOTAL_PAGES")],
                    [sg.Text("ファイルサイズ: ", size=(15, 1)), sg.Text("", size=(30, 1), key="FILE_SIZE")],
                    [sg.Text("作成日: ", size=(15, 1)), sg.Text("", size=(30, 1), key="CREATION_DATE")],
                    [sg.Text("更新日: ", size=(15, 1)), sg.Text("", size=(30, 1), key="MOD_DATE")],
                ],
            )
        ],
        [sg.Text("削除するページ番号 (カンマ区切り):"), sg.InputText(key="PAGE_NUMBERS")],
        [
            sg.Text("保存ファイル名"),
            sg.InputText(key="SAVE_PATH", size=(80, 1)),
            sg.FileSaveAs(file_types=(("PDF Files", "*.pdf"),)),
        ],
        [sg.Text(" ")],
        [
            sg.Button("指定したページを削除", size=(24, 2), key="DELETE"),
            sg.Text(" "),
            sg.Button("メインメニューへ戻る", size=(24, 2), key="BACK"),
        ],
    ]

    # ウィンドウの作成
    window: sg.Window = sg.Window("PDF のページを削除", layout, finalize=True)

    # イベントループ
    while True:
        event, values = window.read()

        # ウィンドウが閉じられた場合や「メインメニューへ戻る」ボタンが押された場合
        if event in (sg.WIN_CLOSED, "BACK"):
            break

        # PDF ファイルが選択された場合
        elif event == "FILE_PATH":
            pdf_path: str = values["FILE_PATH"]
            if os.path.exists(pdf_path):
                try:
                    # PDF ファイルの情報を取得して表示
                    doc: fitz.Document = fitz.open(pdf_path)
                    window["FILE_NAME"].update(os.path.basename(pdf_path))
                    window["TOTAL_PAGES"].update(len(doc))
                    window["FILE_SIZE"].update(f"{os.path.getsize(pdf_path) / (1024 * 1024):.2f} MB")
                    window["PAGE_NUMBERS"].update(disabled=False)
                    doc.close()
                except Exception as e:
                    sg.popup_error("エラー", f"PDF 読み込みエラー: {e}")

        # 「指定したページを削除」ボタンが押された場合
        elif event == "DELETE":
            pdf_path: str = values["FILE_PATH"]
            save_path: str = values["SAVE_PATH"]
            page_numbers_str: str = values["PAGE_NUMBERS"]

            if not pdf_path or not save_path or not page_numbers_str:
                sg.popup_error("エラー", "PDF ファイル、保存先、および削除するページ番号を指定してください。")
                continue

            try:
                # PDF ファイルを開く
                doc: fitz.Document = fitz.open(pdf_path)
                total_pages: int = len(doc)

                # 削除するページ番号を取得
                page_numbers: List[int] = sorted(
                    set(int(num.strip()) - 1 for num in page_numbers_str.split(",") if num.strip().isdigit())
                )

                # ページ番号のバリデーション
                if any(num < 0 or num >= total_pages for num in page_numbers):
                    sg.popup_error("エラー", "無効なページ番号が含まれています。")
                    continue

                # 新しい PDF を作成してページをコピー
                new_doc: fitz.Document = fitz.open()
                for i in range(total_pages):
                    if i not in page_numbers:
                        new_doc.insert_pdf(doc, from_page=i, to_page=i)

                # PDF ファイルを保存
                new_doc.save(save_path)
                new_doc.close()
                doc.close()
                sg.popup("完了", "指定したページの削除が完了しました。")
            except Exception as e:
                sg.popup_error("エラー", f"PDF 処理エラー: {e}")

    # ウィンドウを閉じる
    window.close()


if __name__ == "__main__":
    delete_pdf_pages_window()
