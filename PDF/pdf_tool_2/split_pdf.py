"""
PDF ファイルを分割
"""




import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List


def split_all() -> bool:  # TODO 引数設定
    # TODO ここに処理を追加
    return True


def split(pages: List[int]) -> bool:  # TODO 引数設定
    # TODO ここに処理を追加
    return True


def split_pdf_window() -> None:
    """
    PDF ファイルを分割するウィンドウ
    """

    def cmd_select_file() -> None:
        """
        ファイル選択ダイアログを表示して、選択したファイルのパスをテキストボックスに設定
        """
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            ent_target_file.delete(0, tk.END)
            ent_target_file.insert(0, file_path)
        return None

    def cmd_toggle_ent_page_no() -> None:
        """
        split_all_checkbutton の状態に応じて ent_page_no の入力を制御
        """
        if var_split_all.get():
            ent_page_no.delete(0, tk.END)
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
            messagebox.showerror("エラー", "PDF ファイルを選択してください。")
            return
        if var_split_all.get():
            # 全ページを分割
            if split_all():  # TODO 引数設定
                messagebox.showinfo("情報", "分割処理が完了しました。")
            else:
                messagebox.showinfo("情報", "分割処理が失敗しました。")
        else:
            # 指定ページ位置で分割
            page: str = ent_page_no.get()
            if not page:
                messagebox.showerror("エラー", "分割するページ番号を入力してください。")
                return
            # ページ番号の解析
            try:
                page_list: List[int] = [int(p.strip()) for p in page.split(",")]
            except ValueError:
                messagebox.showerror("エラー", "ページ番号は整数で入力してください。")
                return
            if split(page_list):  # TODO 引数設定
                messagebox.showinfo("情報", "分割処理が完了しました。")
            else:
                messagebox.showinfo("情報", "分割処理が失敗しました。")
        return None

    def on_close() -> None:
        """
        ウィンドウが閉じられたときの処理
        """
        win_split.destroy()
        return None

    #
    # GUI: Tkinter.tk & Tkinter.ttk
    #

    # root ウィンドウの設定
    win_split = tk.Tk()
    win_split.title("PDF ファイルを分割")
    win_split.resizable(False, False)
    win_split.focus_force()
    win_split.protocol("WM_DELETE_WINDOW", on_close)  # ウィンドウが閉じられたときのコールバックを設定

    # タイトル
    lbl_title = ttk.Label(win_split, text="PDF ファイルを分割", style="Title.TLabel")
    lbl_title.pack()

    # フレームの追加
    frame = ttk.Frame(win_split, padding=10)
    frame.pack()

    # 分割するPDFファイル
    lbl_target_file = ttk.Label(frame, text="分割するPDFファイル", style="TLabel")
    lbl_target_file.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    ent_target_file = ttk.Entry(frame, width=80, style="TEntry")
    ent_target_file.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

    btn_target_file = ttk.Button(frame, text="PDF ファイルを選択", style="TButton", command=cmd_select_file)
    btn_target_file.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

    # 全ページを分割するかどうか
    var_split_all = tk.BooleanVar()
    var_split_all.set(False)
    chk_split_all_checkbutton = ttk.Checkbutton(
        frame,
        text="全てのページを１ページずつ分割",
        variable=var_split_all,
        onvalue=True,
        offvalue=False,
        style="TCheckbutton",
        command=cmd_toggle_ent_page_no,
    )
    chk_split_all_checkbutton.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

    # ページ番号
    lbl_page_no_1 = ttk.Label(frame, text="分割するページ番号", style="TLabel")
    lbl_page_no_1.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

    ent_page_no = ttk.Entry(frame, width=55, style="TEntry")
    ent_page_no.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

    lbl_page_no_2 = ttk.Label(frame, text="カンマ区切りで複数指定可", style="TLabel")
    lbl_page_no_2.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)

    # 保存先、分割ボタン

    lbl_save_path = ttk.Label(frame, text="分割結果の保存場所", style="TLabel")
    lbl_save_path.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

    ent_save_path = ttk.Entry(frame, width=80, style="TEntry")
    ent_save_path.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

    btn_save_path = ttk.Button(frame, text="保存場所を選択", style="TButton", command=cmd_select_file)
    btn_save_path.grid(row=4, column=3, padx=5, pady=5, sticky=tk.W)

    # 分割ボタン

    btn_split = ttk.Button(frame, text="PDF ファイルを分割", style="TButton", command=cmd_split)
    btn_split.grid(row=5, column=3, padx=5, pady=5, sticky=tk.W)

    # ウィンドウを表示
    win_split.mainloop()

    return None


# お約束のおまじない
if __name__ == "__main__":
    split_pdf_window()
