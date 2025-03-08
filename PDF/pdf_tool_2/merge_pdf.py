"""
PDF ファイルを結合
"""





import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import Treeview


def add_file(tree: Treeview) -> None:
    """
    ファイルダイアログを開いて PDF ファイルを選択し、ツリービューに追加する。
    """
    # 10個以を超えたファイルを追加できないようにする
    if len(tree.get_children()) >= 10:
        return
    # ファイルダイアログを開いて PDF ファイルを選択
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        file_name = os.path.normpath(file_path).split(os.sep)[-1]
        path_name = os.path.dirname(os.path.normpath(file_path))
        tree.insert("", "end", values=(len(tree.get_children()) + 1, file_name, path_name))
    return None


def move_up(tree: Treeview) -> None:
    """
    選択されたアイテムを一つ上に移動する。
    """
    selected_item = tree.selection()
    if selected_item:
        index = tree.index(selected_item)
        if index > 0:
            tree.move(selected_item, "", index - 1)
            update_order(tree)
    return None


def move_down(tree: Treeview) -> None:
    """
    選択されたアイテムを一つ下に移動する。
    """
    selected_item = tree.selection()
    if selected_item:
        index = tree.index(selected_item)
        if index < (len(tree.get_children()) - 1):
            tree.move(selected_item, "", index + 1)
            update_order(tree)
    return None


def delete_item(tree: Treeview) -> None:
    """
    選択されたアイテムを削除する。
    """
    # 選択されたアイテムがない場合は何もしない
    if len(tree.get_children()) <= 0:
        return
    # 選択されたアイテムを削除
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)
        update_order(tree)
    return None


def update_order(tree: Treeview) -> None:
    """
    ツリービュー内のアイテムの順序を更新する。
    """
    for index, item in enumerate(tree.get_children()):
        tree.item(item, values=(index + 1, tree.item(item, "values")[1], tree.item(item, "values")[2]))
    return None


def merge_pdf_all(tree: Treeview) -> bool:  # TODO 引数設定
    """
    ツリービュー内のすべての PDF ファイルを結合する。
    """
    # TODO ここに処理を追加
    return True


def merge_pdf_window() -> None:
    """
    PDF ファイルを結合するためのウィンドウを表示する。
    """

    def cmd_add_file() -> None:
        """
        一覧へ PDF ファイルを追加
        """
        add_file(tree)
        return None

    def cmd_move_up() -> None:
        """
        ↑：一覧で選択した行と、ひとつ上の行を入れ替える
        """
        move_up(tree)
        return None

    def cmd_move_down() -> None:
        """
        ↓：一覧で選択した行と、ひとつ下の行を入れ替える
        """
        move_down(tree)
        return None

    def cmd_delete_item() -> None:
        """
        一覧から PDF ファイルを削除
        """
        delete_item(tree)
        return None

    def cmd_save_as() -> None:
        """
        ファイル保存ダイアログを開いて保存場所とファイル名を設定
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            save_path.set(file_path)
        return None

    def cmd_merge_pdf_all() -> None:
        """
        一覧の PDF ファイルを順に結合
        """
        if merge_pdf_all(tree):  # TODO 引数設定
            messagebox.showinfo("情報", "結合処理が完了しました。")
        else:
            messagebox.showinfo("情報", "結合処理が失敗しました。")
        return None

    def on_close() -> None:
        """
        ウィンドウが閉じられたときの処理
        """
        win_merge.destroy()
        return None

    #
    # GUI: Tkinter.tk & Tkinter.ttk
    #

    # root ウィンドウの設定
    win_merge = tk.Tk()
    win_merge.title("PDF Tool")
    win_merge.resizable(False, False)
    win_merge.focus_force()
    win_merge.protocol("WM_DELETE_WINDOW", on_close)  # ウィンドウが閉じられたときのコールバックを設定

    # タイトル
    lbl_title = ttk.Label(win_merge, text="PDF ファイルを結合", style="Title.TLabel")
    lbl_title.pack()

    # 一覧
    columns = ("結合順", "ファイル名", "パス")
    tree = ttk.Treeview(win_merge, columns=columns, show="headings", height=10, style="Treeview")
    for col in columns:
        tree.heading(col, text=col)
    tree.column("結合順", width=80, anchor="center")
    tree.column("ファイル名", width=400)
    tree.column("パス", width=720)
    tree.pack()

    # 一覧を操作するためのボタンを一覧の下に配置するためのフレーム
    frame1 = ttk.Frame(win_merge)
    frame1.pack()

    btn_add = ttk.Button(frame1, text="一覧へ PDF ファイルを追加", style="TButton", command=cmd_add_file)
    btn_add.grid(row=0, column=0, padx=5, pady=5)

    btn_up = ttk.Button(frame1, text="↑", style="TButton", command=cmd_move_up)
    btn_up.grid(row=0, column=1)

    btn_down = ttk.Button(frame1, text="↓", style="TButton", command=cmd_move_down)
    btn_down.grid(row=0, column=2)

    btn_delete = ttk.Button(frame1, text="一覧から PDF ファイルを削除", style="TButton", command=cmd_delete_item)
    btn_delete.grid(row=0, column=3, padx=5, pady=5)

    # 保存場所とファイル名の設定に関するフレーム
    frame2 = ttk.Frame(win_merge)
    frame2.pack(fill="x")

    lbl_save_path = ttk.Label(frame2, text="保存ファイル名", style="TLabel")
    lbl_save_path.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    save_path = tk.StringVar()
    ent_save_path = ttk.Entry(frame2, textvariable=save_path, width=134, style="TEntry")
    ent_save_path.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="W")

    btn_save_as = ttk.Button(frame2, text="保存場所とファイル名を設定", style="TButton", command=cmd_save_as)
    btn_save_as.grid(row=0, column=3, pady=10, sticky="w")

    # 結合ボタンのフレーム
    frame3 = ttk.Frame(win_merge)
    frame3.pack(fill="x")
    frame3.columnconfigure(0, weight=1)  # btn_merge_pdf_all を右端へ寄せるための設定

    btn_merge_pdf_all = ttk.Button(
        frame3, text="一覧の PDF ファイルを順に結合", style="TButton", command=cmd_merge_pdf_all
    )
    btn_merge_pdf_all.grid(row=0, column=1, padx=10, pady=10, sticky="E")

    # ウィンドウを表示
    win_merge.mainloop()

    return None


# お約束のおまじない
if __name__ == "__main__":
    merge_pdf_window()
