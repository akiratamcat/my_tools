import os
from typing import Any, List

import fitz  # PyMuPDF
import TkEasyGUI as sg


# PDF 分割ウィンドウを表示する関数
def split_pdf_window() -> None:
    # レイアウトの定義
    layout: List[List[Any]] = [
        [sg.Text("PDF を分割", font=("Helvetica", 14))],
        [
            sg.Text("分割PDFファイル名"),
            sg.InputText(key="PDF_PATH", size=(80, 1), readonly=True),
            sg.FileBrowse(" ... ", file_types=(("PDF Files", "*.pdf"),)),
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
        [sg.Text("ページ番号 (カンマ区切り)"), sg.InputText(key="PAGE_NUMS", size=(30, 1))],
        [sg.Text("保存先"), sg.InputText(key="SAVE_FOLDER", size=(80, 1), readonly=True), sg.FolderBrowse(" ... ")],
        [sg.Text(" ")],
        [
            sg.Button("PDF ファイルを分割", size=(24, 2), key="SPLIT"),
            sg.Text(" "),
            sg.Button("メインメニューへ戻る", size=(24, 2), key="BACK"),
        ],
    ]

    # ウィンドウの作成
    window: sg.Window = sg.Window("PDF を分割", layout, finalize=True)

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
                    window["PAGE_NUMBER"].update(values=[str(i + 1) for i in range(len(doc))])
                    window["PAGE_NUMBER"].update(disabled=not values["SELECTED_PAGE"])
                    doc.close()
                except Exception as e:
                    sg.popup_error("エラー", f"PDF 読み込みエラー: {e}")

        # 「PDF ファイルを分割」ボタンが押された場合
        elif event == "SPLIT":
            pdf_path: str = values["PDF_PATH"]
            save_folder: str = values["SAVE_FOLDER"]
            page_nums: str = values["PAGE_NUMS"].replace(" ", "")

            # 入力チェック
            if not os.path.exists(pdf_path):
                sg.popup_error("PDF ファイルを選択してください。")
                continue
            if not os.path.exists(save_folder):
                sg.popup_error("保存先フォルダを選択してください。")
                continue
            if not page_nums:
                sg.popup_error("ページ番号を入力してください。")
                continue

            try:
                # ページ番号のリストを作成
                page_list: List[int] = [int(p) for p in page_nums.split(",") if p.isdigit() and int(p) > 0]
                doc: fitz.Document = fitz.open(pdf_path)
                total_pages: int = len(doc)

                # ページ番号が総ページ数を超えていないかチェック
                if any(p > total_pages for p in page_list):
                    sg.popup_error("指定されたページ番号が PDF の総ページ数を超えています。")
                    continue

                # 分割ポイントのリストを作成
                split_points: List[int] = sorted(set(page_list))
                split_docs: List[fitz.Document] = []
                prev_page: int = 0

                # 分割処理
                for idx, split_page in enumerate(split_points):
                    new_doc: fitz.Document = fitz.open()
                    new_doc.insert_pdf(doc, from_page=prev_page, to_page=split_page - 1)
                    split_docs.append(new_doc)
                    prev_page = split_page

                # 最後の部分
                if prev_page < total_pages:
                    new_doc: fitz.Document = fitz.open()
                    new_doc.insert_pdf(doc, from_page=prev_page, to_page=total_pages - 1)
                    split_docs.append(new_doc)

                # 保存処理
                for i, new_doc in enumerate(split_docs):
                    output_path: str = os.path.join(
                        save_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_split_{i + 1:03d}.pdf"
                    )
                    new_doc.save(output_path)
                    new_doc.close()

                doc.close()
                sg.popup("PDF 分割が完了しました！")
            except Exception as e:
                sg.popup_error(f"エラーが発生しました: {e}")

    # ウィンドウを閉じる
    window.close()
