"""
PDF ファイル 加工ツール

python.exe -m pip install --upgrade pip

pip install --upgrade PyMuPDF

"""

import tkinter as tk
from tkinter import Menu, Tk, ttk

import utility
from merge_pdf import merge_pdf_window
from split_pdf import split_pdf_window


def main() -> None:
    """
    メイン
    """

    def on_exit() -> None:
        """
        終了
        """
        root_window.quit()

    def on_merge_pdf() -> None:
        """
        PDF ファイルを結合
        """
        root_window.withdraw()
        merge_pdf_window()
        root_window.deiconify()
        root_window.focus_force()

    def on_split_pdf() -> None:
        """
        PDF ファイルを分割
        """
        root_window.withdraw()
        split_pdf_window()
        root_window.deiconify()
        root_window.focus_force()

    def on_rotate_page_pdf() -> None:
        """
        指定したページを回転
        """
        pass

    def on_delete_page_pdf() -> None:
        """
        指定したページを削除
        """
        pass

    def on_insert_pdf() -> None:
        """
        指定したページ位置へ別の PDF ファイルを挿入
        """
        pass

    def on_extract_text_and_image_pdf() -> None:
        """
        PDF ファイルからテキストと画像を抽出
        """
        pass

    #
    # GUI: Tkinter.tk & Tkinter.ttk
    #

    # root ウィンドウの設定
    root_window: Tk = tk.Tk()
    root_window.title("PDF ファイル 加工ツール")
    root_window.resizable(False, False)  # ウィンドウのサイズ変更を無効化
    root_window.focus_force()

    # スタイルの設定
    style = ttk.Style()
    utility.set_Style(style)

    # メニューバーの設定
    menu_bar: Menu = Menu(root_window)
    root_window.config(menu=menu_bar)

    # ファイルメニューの設定
    file_menu: Menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="ファイル", menu=file_menu)
    file_menu.add_command(label="終了", command=on_exit)

    # メインフレームの設定
    frame = ttk.Frame(root_window, padding=10)
    frame.grid(row=0, column=0)

    # 各ボタンの設定
    button_width: int = 46
    merge_btn: ttk.Button = ttk.Button(
        frame, text="PDF ファイルを結合", width=button_width, command=on_merge_pdf, style="TButton"
    )
    merge_btn.grid(row=0, column=0, padx=5)

    split_btn = ttk.Button(frame, text="PDF ファイルを分割", width=button_width, command=on_split_pdf, style="TButton")
    split_btn.grid(row=1, column=0, padx=5)

    rotate_page_btn = ttk.Button(
        frame, text="指定したページを回転", width=button_width, command=on_rotate_page_pdf, style="TButton"
    )
    rotate_page_btn.grid(row=2, column=0, padx=5)

    delete_page_btn = ttk.Button(
        frame, text="指定したページを削除", width=button_width, command=on_delete_page_pdf, style="TButton"
    )
    delete_page_btn.grid(row=3, column=0, padx=5)

    insert_btn = ttk.Button(
        frame,
        text="指定したページ位置へ別の PDF ファイルを挿入",
        width=button_width,
        command=on_insert_pdf,
        style="TButton",
    )
    insert_btn.grid(row=4, column=0, padx=5)

    extract_text_and_image_btn = ttk.Button(
        frame,
        text="PDF ファイルからテキストと画像を抽出",
        width=button_width,
        command=on_extract_text_and_image_pdf,
        style="TButton",
    )
    extract_text_and_image_btn.grid(row=5, column=0, padx=5)

    # メインループの開始
    root_window.mainloop()


# お約束のおまじない
if __name__ == "__main__":
    main()
