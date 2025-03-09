"""
スタイルの設定
"""

from tkinter import ttk


def set_Style(
    s: ttk.Style,
) -> None:
    # style
    # s.theme_use("winnative")
    s.theme_use("default")
    # Label
    s.configure("TLabel", font=("Helvetica", 12), padding=5)
    s.configure("Title.TLabel", font=("Helvetica", 16), padding=5)
    # Entry
    s.configure("TEntry", font=("Helvetica", 12), padding=5)
    # Checkbutton
    s.configure("TCheckbutton", font=("Helvetica", 12), padding=5)
    # Button
    s.configure("TButton", font=("Helvetica", 12), padding=5)
    # Treeview
    s.configure("Treeview", font=("Helvetica", 12))  # フォントサイズを 12 に設定
    s.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))  # ヘッダーのフォントサイズを 12 に設定
    return None
