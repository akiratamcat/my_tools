"""
PDF ファイル 加工ツール

### pip ###

python.exe -m pip install --upgrade pip
pip install --upgrade PyMuPDF
pip install --upgrade chardet
pip install --upgrade pillow
pip install --upgrade pytesseract

"""

import sys
import tkinter as tk
from tkinter import Menu, Tk, ttk

from delete_page_pdf import delete_page_pdf_window
from extract_text_and_image_pdf import extract_text_and_image_pdf_window
from insert_pdf import insert_pdf_window
from merge_pdf import merge_pdf_window
from rotate_page_pdf import rotate_page_pdf_window
from split_pdf import split_pdf_window
from utility import set_Style


def main() -> None:
    """
    メイン
    """

    def on_exit() -> None:
        """
        終了
        """
        win_main.quit()
        sys.exit()  # アプリケーション終了

    def on_merge_pdf() -> None:
        """
        PDF ファイルを結合
        """
        win_main.withdraw()
        win_sub: tk.Toplevel = merge_pdf_window(win_parent=win_main)
        win_sub.focus_force()
        return

    def on_split_pdf() -> None:
        """
        PDF ファイルを分割
        """
        win_main.withdraw()
        win_sub: tk.Toplevel = split_pdf_window(win_parent=win_main)
        win_sub.focus_force()
        return

    def on_rotate_page_pdf() -> None:
        """
        指定したページを回転
        """
        win_main.withdraw()
        win_sub: tk.Toplevel = rotate_page_pdf_window(win_parent=win_main)
        win_sub.focus_force()
        return

    def on_delete_page_pdf() -> None:
        """
        指定したページを削除
        """
        win_main.withdraw()
        win_sub: tk.Toplevel = delete_page_pdf_window(win_parent=win_main)
        win_sub.focus_force()
        return

    def on_insert_pdf() -> None:
        """
        指定したページ位置へ別の PDF ファイルを挿入
        """
        win_main.withdraw()
        win_sub: tk.Toplevel = insert_pdf_window(win_parent=win_main)
        win_sub.focus_force()
        return

    def on_extract_text_and_image_pdf() -> None:
        """
        PDF ファイルからテキストと画像を抽出
        """
        win_main.withdraw()
        win_sub: tk.Toplevel = extract_text_and_image_pdf_window(win_parent=win_main)
        win_sub.focus_force()
        return

    #
    # GUI: Tkinter.tk & Tkinter.ttk
    #

    # root ウィンドウの設定

    win_main: Tk = tk.Tk()
    win_main.title(string="PDF ファイル 加工ツール")
    win_main.resizable(width=False, height=False)  # ウィンドウのサイズ変更を無効化
    win_main.protocol(name="WM_DELETE_WINDOW", func=on_exit)
    win_main.focus_force()

    # スタイルの設定

    style = ttk.Style()
    set_Style(s=style)

    # メニューバーの設定

    menu_bar: Menu = Menu(master=win_main)
    win_main.config(menu=menu_bar)

    # ファイルメニューの設定

    file_menu: Menu = Menu(master=menu_bar, tearoff=0)
    menu_bar.add_cascade(label="ファイル", menu=file_menu)
    file_menu.add_command(label="終了", command=on_exit)

    # メインフレームの設定

    frame = ttk.Frame(win_main, padding=20)
    frame.grid(row=0, column=0)

    # 各ボタンの設定

    button_width: int = 46
    merge_btn: ttk.Button = ttk.Button(
        master=frame,
        text="PDF ファイルを結合",
        width=button_width,
        command=on_merge_pdf,
        style="TButton",
        padding=10,
    )
    merge_btn.grid(row=0, column=0, padx=5)

    split_btn = ttk.Button(
        master=frame,
        text="PDF ファイルを分割",
        width=button_width,
        command=on_split_pdf,
        style="TButton",
        padding=10,
    )
    split_btn.grid(row=1, column=0, padx=5)

    rotate_page_btn = ttk.Button(
        master=frame,
        text="指定したページを回転",
        width=button_width,
        command=on_rotate_page_pdf,
        style="TButton",
        padding=10,
    )
    rotate_page_btn.grid(row=2, column=0, padx=5)

    delete_page_btn = ttk.Button(
        master=frame,
        text="指定したページを削除",
        width=button_width,
        command=on_delete_page_pdf,
        style="TButton",
        padding=10,
    )
    delete_page_btn.grid(row=3, column=0, padx=5)

    insert_btn = ttk.Button(
        master=frame,
        text="指定したページ位置へ別の PDF ファイルを挿入",
        width=button_width,
        command=on_insert_pdf,
        style="TButton",
        padding=10,
    )
    insert_btn.grid(row=4, column=0, padx=5)

    extract_text_and_image_btn = ttk.Button(
        master=frame,
        text="PDF ファイルからテキストと画像を抽出",
        width=button_width,
        command=on_extract_text_and_image_pdf,
        style="TButton",
        padding=10,
    )
    extract_text_and_image_btn.grid(row=5, column=0, padx=5)

    # メインループの開始
    win_main.mainloop()


# お約束のおまじない
if __name__ == "__main__":
    main()
