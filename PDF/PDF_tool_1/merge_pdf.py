import os
from typing import Any, List, Tuple

import fitz  # PyMuPDF
import TkEasyGUI as sg


# PDF 結合ウィンドウを表示する関数
def merge_pdf_window() -> None:
    # レイアウトの定義
    layout: List[List[Any]] = [
        [sg.Text("PDF を結合", font=("Helvetica", 14))],
        [
            sg.Table(
                values=[],
                headings=["結合順", "PDF ファイル名", "ページ数"],
                auto_size_columns=False,
                col_widths=[8, 40, 8],
                enable_events=True,
                key="TABLE",
                select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            )
        ],
        [
            sg.Button("PDF ファイルを選択して一覧へ追加", key="ADD_FILES"),
            sg.Text(" "),
            sg.Button("↑", size=(3, 1), key="MOVE_UP"),
            sg.Button("↓", size=(3, 1), key="MOVE_DOWN"),
            sg.Text(" "),
            sg.Button("一覧から削除", key="DELETE"),
        ],
        [
            sg.Text("保存ファイル名"),
            sg.Text(" "),
            sg.InputText(key="OUTPUT_FILE", size=(80, 1)),
            sg.Text(" "),
            sg.FileSaveAs(" ... ", file_types=(("PDF Files", "*.pdf"),)),
        ],
        [sg.Text(" ")],
        [
            sg.Button("PDF ファイルを結合", size=(24, 2), key="MERGE"),
            sg.Text(" "),
            sg.Button("メインメニューへ戻る", size=(24, 2), key="BACK"),
        ],
    ]

    # ウィンドウの作成
    window: sg.Window = sg.Window("PDF を結合", layout, finalize=True)
    pdf_files: List[Tuple[int, str, int]] = []

    # イベントループ
    while True:
        event, values = window.read()

        # ウィンドウが閉じられた場合や「メインメニューへ戻る」ボタンが押された場合
        if event in (sg.WIN_CLOSED, "BACK"):
            break

        # 「PDF ファイルを選択して追加」ボタンが押された場合
        elif event == "ADD_FILES":
            files: List[str] = sg.popup_get_file(
                "PDF を選択", multiple_files=True, file_types=("PDF ファイル", "*.pdf")
            )
            if files:
                for file in files:
                    try:
                        doc = fitz.open(file)
                        pdf_files.append((len(pdf_files) + 1, os.path.basename(file), doc.page_count))
                    except Exception as e:
                        sg.popup_error(f"エラー: {str(e)}")
                window["TABLE"].update(values=pdf_files)

        # 「↑」ボタンが押された場合
        elif event == "MOVE_UP":
            selected_rows: List[int] = values["TABLE"]
            if selected_rows:
                idx: int = selected_rows[0]
                if idx > 0:
                    pdf_files[idx], pdf_files[idx - 1] = pdf_files[idx - 1], pdf_files[idx]
                    window["TABLE"].update(values=pdf_files)

        # 「↓」ボタンが押された場合
        elif event == "MOVE_DOWN":
            selected_rows: List[int] = values["TABLE"]
            if selected_rows:
                idx: int = selected_rows[0]
                if idx < len(pdf_files) - 1:
                    pdf_files[idx], pdf_files[idx + 1] = pdf_files[idx + 1], pdf_files[idx]
                    window["TABLE"].update(values=pdf_files)

        # 「削除」ボタンが押された場合
        elif event == "DELETE":
            selected_rows: List[int] = values["TABLE"]
            if selected_rows:
                idx: int = selected_rows[0]
                del pdf_files[idx]
                pdf_files = [(i + 1, *data[1:]) for i, data in enumerate(pdf_files)]
                window["TABLE"].update(values=pdf_files)

        # 「PDF ファイルを結合」ボタンが押された場合
        elif event == "MERGE":
            output_file: str = values["OUTPUT_FILE"].strip()
            if len(pdf_files) < 2:
                sg.popup_error("結合する PDF は 2 つ以上選択してください。")
                continue
            if not output_file:
                sg.popup_error("保存ファイル名を指定してください。")
                continue

            try:
                merger = fitz.open()
                for _, file_name, page_count in pdf_files:
                    doc = fitz.open(file)
                    merger.insert_pdf(doc)
                merger.save(output_file)
                merger.close()
                sg.popup("PDF の結合が完了しました。", title="完了")
            except Exception as e:
                sg.popup_error(f"エラー: {str(e)}")

    # ウィンドウを閉じる
    window.close()
