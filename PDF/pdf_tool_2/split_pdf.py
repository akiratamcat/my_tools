"""
PDF ファイルを分割
"""

import sys
import tkinter as tk
from tkinter import filedialog, ttk
from typing import List

from utility import mbox_err, mbox_info, set_Style


def split_all() -> bool:  # TODO 引数設定
    # TODO ここに処理を追加
    return True


def split(pages: List[int]) -> bool:  # TODO 引数設定
    # TODO ここに処理を追加
    return True


def split_pdf_window(win_parent: tk.Tk) -> tk.Toplevel:
    """
    PDF ファイルを分割するウィンドウ
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

    def cmd_toggle_ent_page_no() -> None:
        """
        split_all_checkbutton の状態に応じて ent_page_no の入力を制御
        """
        if var_split_all.get():
            ent_page_no.delete(first=0, last=tk.END)
            ent_page_no.config(state="disabled")
        else:
            ent_page_no.config(state="normal")
        return None

    def cmd_split() -> None:
        """
        分割処理を実行
        """
        pdf_path: str = ent_target_file.get()
        if not pdf_path:
            mbox_err(message="PDF ファイルを選択してください。")
            return

        # TODO 出力先チェック

        if var_split_all.get():
            # 全ページを分割
            if split_all():  # TODO 引数設定
                mbox_info(message="分割処理が完了しました。")
            else:
                mbox_err(message="分割処理が失敗しました。")
        else:
            # 指定ページ位置で分割
            page: str = ent_page_no.get()
            if not page:
                mbox_err(message="分割するページ番号を入力してください。")
                return
            # ページ番号の解析
            try:
                page_list: List[int] = [int(p.strip()) for p in page.split(sep=",")]
            except ValueError:
                mbox_err(message="ページ番号は整数で入力してください。")
                return
            if split(pages=page_list):  # TODO 引数設定
                mbox_info(message="分割処理が完了しました。")
            else:
                mbox_err(message="分割処理が失敗しました。")
        return None

    #
    # GUI: Tkinter.tk & Tkinter.ttk
    #

    # root ウィンドウの設定
    win_me = tk.Toplevel()
    win_me.title(string="PDF ファイルを分割")
    win_me.resizable(width=False, height=False)
    win_me.protocol(name="WM_DELETE_WINDOW", func=on_close)  # ウィンドウが閉じられたときのコールバックを設定
    win_me.focus_force()

    # タイトル
    lbl_title = ttk.Label(master=win_me, text="PDF ファイルを分割", style="Title.TLabel")
    lbl_title.pack()

    # フレームの追加
    frame = ttk.Frame(master=win_me, padding=10)
    frame.pack()

    # 分割するPDFファイル
    lbl_target_file = ttk.Label(master=frame, text="分割するPDFファイル", style="TLabel")
    lbl_target_file.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    ent_target_file = ttk.Entry(master=frame, width=80, style="TEntry")
    ent_target_file.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

    btn_target_file = ttk.Button(master=frame, text="PDF ファイルを選択", style="TButton", command=cmd_select_file)
    btn_target_file.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)

    # 全ページを分割するかどうか
    var_split_all = tk.BooleanVar()
    var_split_all.set(value=False)
    chk_split_all_checkbutton = ttk.Checkbutton(
        master=frame,
        text="全てのページを１ページずつ分割",
        variable=var_split_all,
        onvalue=True,
        offvalue=False,
        style="TCheckbutton",
        command=cmd_toggle_ent_page_no,
    )
    chk_split_all_checkbutton.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky=tk.W)

    # ページ番号
    lbl_page_no_1 = ttk.Label(master=frame, text="分割するページ番号", style="TLabel")
    lbl_page_no_1.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

    ent_page_no = ttk.Entry(master=frame, width=44, style="TEntry")
    ent_page_no.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

    lbl_page_no_2 = ttk.Label(master=frame, text="カンマ区切りで複数指定可", style="TLabel")
    lbl_page_no_2.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)

    # 保存先、分割ボタン

    lbl_save_path = ttk.Label(master=frame, text="分割結果の保存場所", style="TLabel")
    lbl_save_path.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

    ent_save_path = ttk.Entry(master=frame, width=80, style="TEntry")
    ent_save_path.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

    btn_save_path = ttk.Button(master=frame, text="保存場所を選択", style="TButton", command=cmd_select_file)
    btn_save_path.grid(row=4, column=4, padx=5, pady=5, sticky=tk.W)

    # 分割ボタン

    btn_split = ttk.Button(master=frame, text="PDF ファイルを分割", style="TButton", command=cmd_split)
    btn_split.grid(row=5, column=4, padx=5, pady=5, sticky=tk.W)

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
        win_sub: tk.Toplevel = split_pdf_window(win_parent=win_root)  # 必要に応じてここを変更する
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
