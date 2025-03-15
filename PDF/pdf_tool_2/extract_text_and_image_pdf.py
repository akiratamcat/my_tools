"""
PDF ファイルからテキストと画像を抽出
"""

import sys
import tkinter as tk
from tkinter import ttk

from utility import set_Style


def extract_text_and_image_pdf_window(win_parent: tk.Tk) -> tk.Toplevel:
    """
    PDF ファイルからテキストと画像を抽出するウィンドウ
    """

    def on_close() -> None:
        win_me.destroy()
        win_parent.deiconify()
        win_parent.focus_force
        return None

    #
    # GUI: Tkinter.tk & Tkinter.ttk
    #
    # Toplevel ウィンドウの設定

    win_me = tk.Toplevel()
    win_me.title(string="PDF ファイルからテキストと画像を抽出")
    win_me.resizable(width=False, height=False)
    win_me.protocol(name="WM_DELETE_WINDOW", func=on_close)  # ウィンドウが閉じられたときのコールバックを設定
    win_me.focus_force()

    # タイトル

    lbl_title = ttk.Label(master=win_me, text="PDF ファイルからテキストと画像を抽出", style="Title.TLabel")
    lbl_title.pack()

    return win_me


# お約束のおまじない
if __name__ == "__main__":
    """
    お約束のおまじない
    """

    def on_close() -> None:
        win_root.destroy()
        sys.exit()

    def show_sub_window() -> None:
        win_root.withdraw()
        win_sub: tk.Toplevel = extract_text_and_image_pdf_window(win_parent=win_root)  # 必要に応じてここを変更する
        win_sub.focus_force()

    win_root = tk.Tk()
    win_root.title(string="Dummy Main Window")
    win_root.geometry(newGeometry="400x100")
    win_root.resizable(width=False, height=False)
    win_root.protocol(name="WM_DELETE_WINDOW", func=on_close)
    win_root.focus

    # スタイルの設定
    style = ttk.Style()
    set_Style(s=style)

    button = ttk.Button(master=win_root, text="Open Sub Window", padding=10, command=show_sub_window)
    button.pack(padx=20, pady=20)
    win_root.mainloop()
