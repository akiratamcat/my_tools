"""
共通部分
"""

import sys
from tkinter import messagebox, ttk


def mbox_err(message: str) -> None:
    """
    エラーメッセージボックス
    """
    messagebox.showerror(title="エラー", message=message)
    return None


def mbox_info(message: str) -> None:
    """
    情報メッセージボックス
    """
    messagebox.showinfo(title="情報", message=message)
    return None


# スタイル設定
def set_Style(s: ttk.Style) -> None:
    """スタイル設定

    Args:
        s (ttk.Style): ttk.Style オブジェクト

    Returns:
        None
    """
    # style & Font
    fontname: str = ""
    if sys.platform == "win32":
        s.theme_use(themename="winnative")
        fontname = "Meiryo UI"
    else:
        s.theme_use(themename="default")
        fontname = "System"

    fsize_normal: int = 10
    fsize_big: int = 14

    # Label
    s.configure(style="TLabel", font=(fontname, fsize_normal), padding=5)
    s.configure(style="Title.TLabel", font=(fontname, fsize_big), padding=5)
    # Entry
    s.configure(style="TEntry", font=(fontname, fsize_normal), padding=5)
    # Checkbutton
    s.configure(style="TCheckbutton", font=(fontname, fsize_normal), padding=5)
    # Checkbutton
    s.configure(style="TCombobox", font=(fontname, fsize_normal), padding=1)
    # Button
    s.configure(style="TButton", font=(fontname, fsize_normal), padding=5)
    # Treeview
    s.configure(style="Treeview", font=(fontname, fsize_normal), padding=2)
    s.configure(style="Treeview.Heading", font=(fontname, fsize_normal), padding=2)

    return None
