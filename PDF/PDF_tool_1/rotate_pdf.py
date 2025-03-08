import os
from typing import Any, List

import fitz  # PyMuPDF
import TkEasyGUI as sg


# PDF 回転ウィンドウを表示する関数
def rotate_pdf_pages_window() -> None:
    # レイアウトの定義
    layout: List[List[Any]] = [
        [sg.Text("PDF の指定したページを回転", font=("Helvetica", 14))],
        [
            sg.Text("ページを回転するPDFファイル名"),
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
        [
            sg.Radio("全てのページを対象", "PAGE_OPTION", default=True, key="ALL_PAGES"),
            sg.Radio("指定したページのみを対象", "PAGE_OPTION", key="SELECTED_PAGE"),
        ],
        [sg.Text("ページ番号:"), sg.Combo([], key="PAGE_NUMBER", disabled=True)],
        [sg.Text("回転方向:"), sg.Combo(["左 90 度", "右 90 度", "180 度"], default_value="左 90 度", key="ROTATION")],
        [
            sg.Text("保存ファイル名"),
            sg.InputText(key="SAVE_PATH", size=(80, 1)),
            sg.FileSaveAs(file_types=(("PDF Files", "*.pdf"),)),
        ],
        [sg.Text(" ")],
        [
            sg.Button("指定したページを回転", size=(24, 2), key="ROTATE"),
            sg.Text(" "),
            sg.Button("メインメニューへ戻", size=(24, 2), key="BACK"),
        ],
    ]

    # ウィンドウの作成
    window: sg.Window = sg.Window("PDF を回転", layout, finalize=True)

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

        # 「PDF ファイルを回転」ボタンが押された場合
        elif event == "ROTATE":
            pdf_path: str = values["FILE_PATH"]
            save_path: str = values["SAVE_PATH"]
            rotation_map: dict[str, int] = {"左 90 度": -90, "右 90 度": 90, "180 度": 180}
            rotation_angle: int = rotation_map[values["ROTATION"]]

            if not pdf_path or not save_path:
                sg.popup_error("エラー", "PDF ファイルと保存先を指定してください。")
                continue

            try:
                # PDF ファイルを開く
                doc: fitz.Document = fitz.open(pdf_path)
                total_pages: int = len(doc)

                # 全てのページを回転
                if values["ALL_PAGES"]:
                    for i in range(total_pages):
                        doc[i].set_rotation(rotation_angle)
                # 指定したページのみ回転
                else:
                    selected_page: int = int(values["PAGE_NUMBER"]) - 1
                    if 0 <= selected_page < total_pages:
                        doc[selected_page].set_rotation(rotation_angle)
                    else:
                        sg.popup_error("エラー", "無効なページ番号です。")
                        continue

                # PDF ファイルを保存
                doc.save(save_path)
                doc.close()
                sg.popup("完了", "PDF の回転が完了しました。")
            except Exception as e:
                sg.popup_error("エラー", f"PDF 処理エラー: {e}")

    # ウィンドウを閉じる
    window.close()


if __name__ == "__main__":
    rotate_pdf_window()
