"""
PDF ファイルを結合
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.ttk import Treeview
from typing import Literal

from utility import mbox_err, mbox_info, set_Style


def update_order(tree: Treeview) -> None:
    """
    ツリービュー内のアイテムの順序を更新する。
    """
    for index, item in enumerate(iterable=tree.get_children()):
        tree.item(
            item=item,
            values=(
                index + 1,
                tree.item(item=item, option="values")[1],
                tree.item(item=item, option="values")[2],
            ),
        )
    return None


def merge_pdf_all(tree: Treeview) -> bool:  # TODO 引数設定
    """
    ツリービュー内のすべての PDF ファイルを結合する。
    """
    # TODO ここに処理を追加
    return True


def merge_pdf_window(win_parent: tk.Tk) -> tk.Toplevel:
    """
    PDF ファイルを結合するためのウィンドウを表示する。
    """

    def on_close() -> None:
        """
        メニューへ戻る
        """
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

    def cmd_add_file() -> None:
        """
        一覧へ PDF ファイルを追加
        """
        # 10個以を超えたファイルを追加できないようにする
        if len(tree_pdf.get_children()) >= 10:
            return
        # ファイルダイアログを開いて PDF ファイルを選択
        file_path: str = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            file_name: str = os.path.normpath(path=file_path).split(sep=os.sep)[-1]
            path_name: str = os.path.dirname(p=os.path.normpath(path=file_path))
            tree_pdf.insert(parent="", index="end", values=(len(tree_pdf.get_children()) + 1, file_name, path_name))
        return None

    def cmd_move_up() -> None:
        """
        ↑：一覧で選択した行と、ひとつ上の行を入れ替える
        """
        selected_item: tuple[str, ...] = tree_pdf.selection()
        if selected_item:
            index: int = tree_pdf.index(item=selected_item[0])
            if index > 0:
                tree_pdf.move(item=selected_item[0], parent="", index=index - 1)
                update_order(tree=tree_pdf)
        return None

    def cmd_move_down() -> None:
        """
        ↓：一覧で選択した行と、ひとつ下の行を入れ替える
        """
        selected_item: tuple[str, ...] = tree_pdf.selection()
        if selected_item:
            index: int = tree_pdf.index(item=selected_item[0])
            if index < (len(tree_pdf.get_children()) - 1):
                tree_pdf.move(item=selected_item[0], parent="", index=index + 1)
                update_order(tree=tree_pdf)
        return None

    def cmd_delete_item() -> None:
        """
        一覧から PDF ファイルを削除
        """
        # 選択されたアイテムがない場合は何もしない
        if len(tree_pdf.get_children()) <= 0:
            return
        # 選択されたアイテムを削除
        selected_item: tuple[str, ...] = tree_pdf.selection()
        if selected_item:
            tree_pdf.delete(selected_item[0])
            update_order(tree=tree_pdf)
        return None

    def cmd_save_as() -> None:
        """
        ファイル保存ダイアログを開いて保存場所とファイル名を設定
        """
        file_path: str = save_path.get() if save_path.get() else os.getcwd()
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            save_path.set(file_path)
        return None

    def cmd_merge_pdf_all() -> None:
        """
        一覧の PDF ファイルを順に結合
        """
        if merge_pdf_all(tree=tree_pdf):  # TODO 引数設定
            mbox_info(message="結合処理が完了しました。")
        else:
            mbox_err(message="結合処理が失敗しました。")
        return None

    #
    # GUI: Tkinter.tk & Tkinter.ttk
    #

    # Toplevel ウィンドウの設定

    win_me = tk.Toplevel()
    win_me.title(string="PDF Tool")
    win_me.resizable(width=False, height=False)
    win_me.protocol(name="WM_DELETE_WINDOW", func=on_close)  # ウィンドウが閉じられたときのコールバックを設定
    win_me.focus_force()

    # フレーム

    frame_main = ttk.Frame(master=win_me, padding=10)
    frame_main.pack()

    # タイトル

    btn_add = ttk.Button(master=frame_main, text="メニューへ戻る", style="Mini.TButton", command=cmd_back_to_menu)
    btn_add.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

    lbl_title = ttk.Label(master=frame_main, text="PDF ファイルを結合", style="Title.TLabel")
    lbl_title.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

    lbl_dummy = ttk.Label(master=frame_main, text="", style="TLabel")
    lbl_dummy.grid(row=0, column=3, padx=5, pady=5)

    # 連結委する PDF ファイルの一覧

    columns: tuple[Literal["結合順"], Literal["ファイル名"], Literal["パス"]] = ("結合順", "ファイル名", "パス")
    tree_pdf = ttk.Treeview(master=frame_main, columns=columns, show="headings", height=12, style="Treeview")

    for col in columns:
        tree_pdf.heading(column=col, text=col)
    tree_pdf.column(column="結合順", width=50, anchor="center")
    tree_pdf.column(column="ファイル名", width=280)
    tree_pdf.column(column="パス", width=560)
    tree_pdf.grid(row=1, column=0, padx=10, pady=5, columnspan=4)

    # 一覧を操作するためのボタンを一覧の下に配置するためのフレーム

    btn_add = ttk.Button(master=frame_main, text="一覧へ PDF ファイルを追加", style="TButton", command=cmd_add_file)
    btn_add.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

    btn_up = ttk.Button(master=frame_main, text="↑", style="TButton", command=cmd_move_up)
    btn_up.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)

    btn_down = ttk.Button(master=frame_main, text="↓", style="TButton", command=cmd_move_down)
    btn_down.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

    btn_delete = ttk.Button(
        master=frame_main, text="一覧から PDF ファイルを削除", style="TButton", command=cmd_delete_item
    )
    btn_delete.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)

    # 保存場所とファイル名の設定に関するフレーム

    lbl_save_path = ttk.Label(master=frame_main, text="保存ファイル名", style="TLabel")
    lbl_save_path.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

    save_path = tk.StringVar()
    ent_save_path = ttk.Entry(master=frame_main, textvariable=save_path, width=90, style="TEntry")
    ent_save_path.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

    btn_save_as = ttk.Button(master=frame_main, text="保存場所とファイル名を設定", style="TButton", command=cmd_save_as)
    btn_save_as.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)

    # 結合ボタンのフレーム

    btn_merge_pdf_all = ttk.Button(
        master=frame_main, text="一覧の PDF ファイルを順に結合", style="TButton", command=cmd_merge_pdf_all
    )
    btn_merge_pdf_all.grid(row=4, column=3, padx=5, pady=5, sticky=tk.E)

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
        win_sub: tk.Toplevel = merge_pdf_window(win_parent=win_root)  # 必要に応じてここを変更する
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

    button = ttk.Button(master=win_root, text="Open Sub Window", command=show_sub_window)
    button.pack(padx=20, pady=20)
    win_root.mainloop()
