"""
共通部分
"""

import sys
from tkinter import messagebox, ttk


def mbox_err(message: str) -> str:
    """エラーメッセージボックス

    Args:
        message (str): エラーメッセージ

    Returns:
        str: _description_
    """
    return messagebox.showerror(title="エラー", message=message)


def mbox_info(message: str) -> str:
    """情報メッセージボックス

    Args:
        message (str): 情報メッセージ

    Returns:
        str: _description_
    """
    return messagebox.showinfo(title="情報", message=message)


def mbox_warning(message: str) -> str:
    """警告メッセージボックス

    Args:
        message (str): 警告メッセージ

    Returns:
        str: _description_
    """
    return messagebox.showwarning(title="警告", message=message)


# スタイル設定
def set_Style(s: ttk.Style) -> None:
    """スタイル設定

    Args:
        s (ttk.Style): ttk.Style オブジェクト

    Returns:
        None
    """
    # style & Font
    FONT_SIZE_NORMAL: int = 10
    FONT_SIZE_BIG: int = 14
    FONT_SIZE_MINI: int = 12

    fontname: str = ""
    if sys.platform == "win32":
        fontname = "Meiryo UI"
    else:
        fontname = "System"

    s.theme_use(themename="default")

    # Label
    s.configure(style="TLabel", font=(fontname, FONT_SIZE_NORMAL), padding=2)
    s.configure(style="Title.TLabel", font=(fontname, FONT_SIZE_BIG), padding=2)
    # Entry
    s.configure(style="TEntry", font=(fontname, FONT_SIZE_NORMAL), padding=2)
    # Checkbutton
    s.configure(style="TCheckbutton", font=(fontname, FONT_SIZE_NORMAL), padding=2)
    # Checkbutton
    s.configure(style="TCombobox", font=(fontname, FONT_SIZE_NORMAL), padding=2)
    # Button
    s.configure(style="TButton", font=(fontname, FONT_SIZE_NORMAL), padding=2)
    s.configure(style="MiniTButton", font=(fontname, FONT_SIZE_MINI), padding=2)
    # Treeview
    s.configure(style="Treeview", font=(fontname, FONT_SIZE_NORMAL), padding=2)
    s.configure(style="Treeview.Heading", font=(fontname, FONT_SIZE_NORMAL), padding=2)

    return None
