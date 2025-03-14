"""
PDF ファイルの指定したページを削除
"""

import sys
import tkinter as tk
from tkinter import filedialog, ttk
from typing import List

from utility import mbox_err, mbox_info, set_Style


def delete_page(pages: List[int]) -> bool:  # TODO 引数設定
    # TODO ここに処理を追加
    return True


def delete_page_pdf_window(win_parent: tk.Tk) -> tk.Toplevel:
    """
    PDF ファイルを削除するウィンドウ
    """

    def on_close() -> None:
        win_me.destroy()
        win_parent.deiconify()
        win_parent.focus_force
        return None

    def cmd_select_file() -> None:
        """
        ファイル選択ダイアログを表示して、選択したファイルのパスをテキストボックスに設定
        """
        file_path: str = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            ent_target_file.delete(first=0, last=tk.END)
            ent_target_file.insert(index=0, string=file_path)
        return None

    def cmd_delete_page() -> None:
        """
        削除処理を実行
        """
        pdf_path: str = ent_target_file.get()
        if not pdf_path:
            mbox_err(message="PDF ファイルを選択してください。")
            return

        # TODO 出力先チェック

        # 指定ページ位置で削除
        page: str = ent_page_no.get()
        if not page:
            mbox_err(message="削除するページ番号を入力してください。")
            return
        # ページ番号の解析
        try:
            page_list: List[int] = [int(p.strip()) for p in page.split(sep=",")]
        except ValueError:
            mbox_err(message="ページ番号は整数で入力してください。")
            return
        if delete_page(
            pages=page_list,
        ):  # TODO 引数設定
            mbox_info(message="削除処理が完了しました。")
        else:
            mbox_err(message="削除処理が失敗しました。")

        return None

    #
    # GUI: Tkinter.tk & Tkinter.ttk
    #

    # Toplevel ウィンドウの設定

    win_me = tk.Toplevel()
    win_me.title(string="PDF ファイルの指定したページを削除")
    win_me.resizable(width=False, height=False)
    win_me.protocol(name="WM_DELETE_WINDOW", func=on_close)  # ウィンドウが閉じられたときのコールバックを設定
    win_me.focus_force()

    # タイトル

    lbl_title = ttk.Label(master=win_me, text="PDF ファイルの指定したページを削除", style="Title.TLabel")
    lbl_title.pack()

    # フレームの追加

    frame = ttk.Frame(master=win_me, padding=10)
    frame.pack()

    # 削除するPDFファイル

    lbl_target_file = ttk.Label(master=frame, text="削除するPDFファイル", style="TLabel")
    lbl_target_file.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    ent_target_file = ttk.Entry(master=frame, width=80, style="TEntry")
    ent_target_file.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

    btn_target_file = ttk.Button(master=frame, text="PDF ファイルを選択", style="TButton", command=cmd_select_file)
    btn_target_file.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)

    # ページ番号

    lbl_page_no_1 = ttk.Label(master=frame, text="削除するページ番号", style="TLabel")
    lbl_page_no_1.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    ent_page_no = ttk.Entry(master=frame, width=44, style="TEntry")
    ent_page_no.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

    lbl_page_no_2 = ttk.Label(master=frame, text="カンマ区切りで複数指定可", style="TLabel")
    lbl_page_no_2.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

    # 保存先、削除ボタン

    lbl_save_path = ttk.Label(master=frame, text="削除結果の保存場所", style="TLabel")
    lbl_save_path.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

    ent_save_path = ttk.Entry(master=frame, width=80, style="TEntry")
    ent_save_path.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

    btn_save_path = ttk.Button(master=frame, text="保存場所を選択", style="TButton", command=cmd_select_file)
    btn_save_path.grid(row=2, column=4, padx=5, pady=5, sticky=tk.W)

    # 削除ボタン

    btn_delete = ttk.Button(master=frame, text="指定したページを削除", style="TButton", command=cmd_delete_page)
    btn_delete.grid(row=3, column=4, padx=5, pady=5, sticky=tk.W)

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
        win_sub: tk.Toplevel = delete_page_pdf_window(win_parent=win_root)  # 必要に応じてここを変更する
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

    button = tk.Button(master=win_root, text="Open Sub Window", command=show_sub_window)
    button.pack(padx=10, pady=10)
    win_root.mainloop()
