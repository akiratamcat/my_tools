"""
指定したページ位置へ別の PDF ファイルを挿入
"""

import sys
import tkinter as tk
from tkinter import ttk

from utility import set_Style


def insert_pdf_window(win_parent: tk.Tk) -> tk.Toplevel:
    """
    指定したページ位置へ別の PDF ファイルを挿入するウィンドウ
    """

    def on_close() -> None:
        win_me.destroy()
        win_parent.deiconify()
        win_parent.focus_force
        return None

    def cmd_back_to_menu() -> None:
        """
        メニューへ戻る
        """
        on_close()
        return None

    #
    # GUI: Tkinter.tk & Tkinter.ttk
    #

    win_me = tk.Toplevel()
    win_me.title(string="PDF ファイルの指定したページを削除")
    win_me.resizable(width=False, height=False)
    win_me.protocol(name="WM_DELETE_WINDOW", func=on_close)  # ウィンドウが閉じられたときのコールバックを設定
    win_me.focus_force()

    # フレーム

    frame_main = ttk.Frame(master=win_me, padding=10)
    frame_main.pack()

    # タイトル

    btn_add = ttk.Button(master=frame_main, text="メニューへ戻る", style="Mini.TButton", command=cmd_back_to_menu)
    btn_add.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

    lbl_title = ttk.Label(master=frame_main, text="指定したページ位置へ別の PDF ファイルを挿入", style="Title.TLabel")
    lbl_title.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

    lbl_dummy = ttk.Label(master=frame_main, text="", style="TLabel")
    lbl_dummy.grid(row=0, column=3, padx=5, pady=5)

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
        win_sub: tk.Toplevel = insert_pdf_window(win_parent=win_root)  # 必要に応じてここを変更する
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
