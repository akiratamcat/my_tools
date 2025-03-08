"""
-----------------------------------------------------------------------
EXCELファイルに grep する GUI ツール
-----------------------------------------------------------------------

python.exe -m pip install --upgrade pip
pip install --upgrade PyInstaller

import している他モジュールで以下が必要。
pip install xlrd==1.2.0
pip install --upgrade openpyxl
pip install --upgrade pandas

"""

import argparse
import csv
import os
import subprocess
from logging import Formatter, Logger, getLogger, handlers
from tkinter import (
    BooleanVar,
    Menu,
    Tk,
    filedialog,
    messagebox,
    ttk,
)
from typing import Any, List, Tuple

from excel_newtype import search_in_excel_file_new_type
from excel_oldtype import search_in_excel_file_old_type
from utility import normalize_string


# EXCELファイル内を検索する関数
def search_files(
    folder_path: str,
    search_term: str,
    recursive: bool,
    case_sensitive: bool,
    width_sensitive: bool,
    shape_search: bool,
    progress_callback: Any,
    logger: Logger,
) -> List[Tuple[str, str, str, str, str, str]]:
    """指定されたパスから EXCEL ファイルを探して、指定された検索語を含むセルを検索し、結果をリストで返す関数

    Args:
        folder_path (str): EXCELファイルを検索する起点となるフォルダのパス
        search_term (str): 検索したい語句
        recursive (bool): folder_path 以下を再帰的に検索するか否か
        case_sensitive (bool): 大文字/小文字を同一視するか否か
        width_sensitive (bool): 全角/半角を同一視するか否か
        shape_search (bool): 図形内のテキストも検索するか否か（但し 新形式 .xlsx, .xlsm ファイルのみ）
        progress_callback (Any): 進捗を更新するためのコールバック関数
        logger (Logger): logging.Logger

    Returns:
        List[Tuple[str, str, str, str, str]]: 検索結果をメインウィンドウのテーブル構造に合わせたリストで返す
    """

    logger.debug("search_in_excel_files()")

    # 検索条件に従って検索語句を正規化
    normalized_search_term: str = normalize_string(
        search_term,
        not case_sensitive,
        not width_sensitive,
        logger,
    )

    # 検索結果を格納するリストを初期化
    results: List[Tuple[str, str, str, str, str, str]] = []

    # 指定したフォルダ内のすべてのファイルを取得
    for root, dirs, files in os.walk(folder_path):
        msg: str = f"フォルダ: {root}"
        logger.debug(msg)
        progress_callback(msg)
        # ファイルごとに処理するループ
        for filename in files:
            if filename.endswith((".xlsx", ".xlsm", ".xls")):
                # ファイルのパスを組み立て
                file_path: str = os.path.join(root, filename).replace("/", os.sep)

                if filename.endswith(".xls"):
                    # EXCEL 旧型式.xlsファイル対応
                    logger.debug(f"EXCEL 旧型式.xlsファイルが見つかりました {file_path}")
                    search_in_excel_file_old_type(
                        file_path,
                        normalized_search_term,
                        case_sensitive,
                        width_sensitive,
                        progress_callback,
                        results,
                        logger,
                    )
                elif filename.endswith(".xlsx") or filename.endswith(".xlsm"):
                    # EXCEL 新形式 .xlsx, .xlsm ファイル対応
                    logger.debug(f"EXCEL 新形式 .xlsx, .xlsm ファイルが見つかりました {file_path}")
                    search_in_excel_file_new_type(
                        file_path,
                        normalized_search_term,
                        case_sensitive,
                        width_sensitive,
                        shape_search,
                        progress_callback,
                        results,
                        logger,
                    )
                else:
                    pass  # 処理対象のファイルではない

        # 再帰的に検索しない場合は、フォルダ内のファイルをすべて検索したら終了
        if not recursive:
            logger.debug("再帰的に検索しない。")
            break

    return results


# 検索を実行する関数
def run_search(
    folder_path: str,
    search_term: str,
    recursive: bool,
    case_sensitive: bool,
    width_sensitive: bool,
    shape_search: bool,
    progress_callback: Any,
    logger: Logger,
) -> List[Tuple[str, str, str, str, str, str]]:
    """EXCELファイル内を検索して、結果をリストで返す関数

    Args:
        folder_path (str): EXCELファイルを検索する起点となるフォルダのパス
        search_term (str): 検索したい語句
        recursive (bool): folder_path 以下を再帰的に検索するか否か
        case_sensitive (bool): 大文字/小文字を同一視するか否か
        width_sensitive (bool): 全角/半角を同一視するか否か
        shape_search (bool): 図形内のテキストも検索するか否か（但し 新形式 .xlsx, .xlsm ファイルのみ）
        progress_callback (Any): 進捗を更新するためのコールバック関数
        logger (Logger): logging.Logger

    Returns:
        List[Tuple[str, str, str, str, str]]: 検索結果をメインウィンドウのテービル構造に合わせたリストで返す
    """
    logger.debug("run_search()")
    try:
        results: List[Tuple[str, str, str, str, str, str]] = search_files(
            folder_path,
            search_term,
            recursive,
            case_sensitive,
            width_sensitive,
            shape_search,
            progress_callback,
            logger,
        )
        return results
    except Exception as e:
        msg: str = f"検索中にエラーが発生しました: {e}"
        logger.error(msg)
        messagebox.showerror("エラー", msg)
        return []


# メイン画面とイベントループ処理
def main() -> None:
    """メイン画面とイベントループ処理

    Args:
        None

    Returns:
        None
    """
    #
    # 起動引数の解析
    #
    parser = argparse.ArgumentParser(description="Excel grepツール")
    parser.add_argument("--debug", action="store_true", help="デバッグモードを有効にする")
    args = parser.parse_args()

    #
    # ロガーの初期化
    #
    logger: Logger = getLogger(__name__)
    logger.setLevel("DEBUG" if args.debug else "INFO")
    logger.setLevel("DEBUG")  # 開発中はログレベルを DEBUG に上書き設定
    rotating_handler = handlers.RotatingFileHandler(
        os.path.splitext(os.path.abspath(__file__))[0] + ".log",
        mode="w",
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    format = Formatter("%(asctime)s : %(levelname)s : %(filename)s - %(message)s")
    rotating_handler.setFormatter(format)
    logger.addHandler(rotating_handler)
    logger.debug("起動しました。")

    # フォルダ選択ダイアログを表示する関数
    def browse_folder() -> None:
        """フォルダ選択ダイアログを表示する関数

        Args:
            None

        Returns:
            None
        """
        logger.debug("browse_folder()")
        folder_selected: str = filedialog.askdirectory()
        if folder_selected:
            search_folder_entry.delete(0, "end")
            search_folder_entry.insert(0, folder_selected)
            logger.info(f"フォルダを選択しました。{folder_selected}")
        else:
            logger.info("フォルダ選択をキャンセルしました。")

    # ステータスバーのメッセージを更新する関数
    def update_status(message: str) -> None:
        """ステータスバーのメッセージを更新する関数

        Args:
            message (str): 更新するメッセージ

        Returns:
            None
        """
        status_bar.config(text=f"  {message}")
        root.update_idletasks()

    # 検索を開始する関数
    def start_search() -> None:
        """検索を開始する関数

        Args:
            None

        Returns:
            None
        """
        logger.debug("start_search()")

        folder_path: str = search_folder_entry.get()
        search_term: str = search_term_entry.get()

        # folder_path または search_term が空の場合は検索を実行しない
        if not folder_path or not search_term:
            logger.debug("folder_path または search_term が空")
            messagebox.showwarning("警告", "検索フォルダと検索語を入力してください。")
            return

        # 検索条件を取得
        recursive: bool = recursive_var.get()
        case_sensitive: bool = not ignore_case_var.get()
        width_sensitive: bool = not ignore_width_var.get()
        shape_search: bool = shape_search_var.get()

        # 検索開始
        result_table.delete(*result_table.get_children())
        update_status("検索中...")
        logger.info(
            "検索を開始しました。"
            f" folder_path={folder_path}"
            f" search_term={search_term}"
            f" recursive={recursive} "
            f" case_sensitive={case_sensitive}"
            f" width_sensitive={width_sensitive}"
            f" shape_search={shape_search}"
        )
        results: List[Tuple[str, str, str, str, str, str]] = run_search(
            folder_path,
            search_term,
            recursive,
            case_sensitive,
            width_sensitive,
            shape_search,
            update_status,
            logger,
        )
        logger.debug("len(results) = %d", len(results))
        for result in results:
            result_table.insert("", "end", values=result)

        # 検索結果の件数にあわせたメッセージを表示
        if len(results) == 0:
            msg: str = "該当するEXCELファイルは見つかりませんでした。"
            logger.info(msg)
            update_status(msg)
            messagebox.showinfo("情報", msg)
        else:
            msg = f"{len(results)} 件の結果が見つかりました。"
            logger.info(msg)
            update_status(msg + " 行を選択してダブルクリックするとEXCELファイルを開く事が出来ます。")
            messagebox.showinfo("情報", msg)

    # 検索結果 treeview をCSVファイルで保存する関数
    def save_csv_file() -> None:
        """検索結果 treeview をCSVファイルで保存する関数
        Args:
            None

        Returns:
            None
        """
        logger.debug("save_csv_file()")
        try:
            # treeview が 0 行の時は処理を行わない
            if not result_table.get_children():
                logger.debug("treeview が 0 行")
                return

            # ファイル保存ダイアログを表示
            file_path: str = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            )
            if not file_path:
                logger.debug("ファイル保存ダイアログを表示してキャンセルされました。")
                return

            logger.debug("CSVファイルに保存します。: %s", file_path)
            # CSVファイルに書き込む
            with open(file_path, mode="w", newline="", encoding="shift_jis") as file:  # 文字コードを Shift JIS に変更
                writer = csv.writer(file)
                # ヘッダーを書き込む
                writer.writerow(columns)
                # 各行のデータを書き込む
                for row_id in result_table.get_children():
                    row: Tuple[str, str, str, str, str, str] = result_table.item(row_id)["values"]
                    writer.writerow(row)

            msg: str = "CSVファイルに保存しました。"
            logger.info(msg + f" : {file_path}")
            update_status(msg + f" : {file_path}")
            messagebox.showinfo("情報", msg)
        except Exception as e:
            msg = f"CSVファイルの保存中にエラーが発生しました: {e}"
            logger.error(msg)
            messagebox.showerror("エラー", msg)

    # 一覧で選択されダブルクリックされた行のEXCELファイルを開く関数
    def open_excel_file(event: Any) -> None:
        """一覧で選択されダブルクリックされた行のEXCELファイルを開く関数

        Args:
            event (Any): イベントオブジェクト

        Returns:
            None
        """
        logger.debug("open_excel_file()")
        try:
            selected_item: Tuple[str, str, str, str, str, str] = result_table.selection()
            if selected_item:
                file_path: str = result_table.item(selected_item, "values")[5]
                msg: str = f"EXCELファイルを開いています : {file_path}"
                logger.debug(msg)
                update_status(msg)
                subprocess.Popen(["start", "excel", file_path], shell=True)
        except Exception as e:
            msg = f"EXCELファイルを開く際にエラーが発生しました: {e}"
            logger.error(msg)
            messagebox.showerror("エラー", msg)

    #
    # GUI 組み立て (Tkinter.tk & ttk)
    #

    try:
        logger.debug("メインウィンドウを作成します。")

        # メインウィンドウの作成
        root: Tk = Tk()
        root.title("Excel grepツール")

        # メニューバーの作成
        menu: Menu = Menu(root)
        root.config(menu=menu)
        file_menu: Menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="ファイル", menu=file_menu)
        file_menu.add_command(label="終了", command=root.quit)

        # メインウィンドウのレイアウト
        frame: ttk.Frame = ttk.Frame(root)
        frame.pack(padx=10, pady=10)

        # 検索条件入力部分の作成
        ttk.Label(frame, text="検索フォルダ:").grid(row=0, column=0, sticky="w")
        search_folder_entry: ttk.Entry = ttk.Entry(frame, width=110)
        search_folder_entry.grid(row=0, column=1, columnspan=5, padx=5, sticky="w")
        ttk.Button(frame, text="参照", command=browse_folder).grid(row=0, column=6, sticky="E")

        ttk.Label(frame, text="検索語:").grid(row=1, column=0, sticky="w")
        search_term_entry: ttk.Entry = ttk.Entry(frame, width=80)
        search_term_entry.grid(row=1, column=1, columnspan=4, padx=6, pady=5, sticky="w")

        # 検索条件チェックボックスの作成
        recursive_var: BooleanVar = BooleanVar()
        ignore_case_var: BooleanVar = BooleanVar()
        ignore_width_var: BooleanVar = BooleanVar()
        shape_search_var: BooleanVar = BooleanVar()
        ttk.Label(frame, text="検索条件:").grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(frame, text="指定フォルダ以下を再帰検索", variable=recursive_var).grid(
            row=2, column=1, padx=5, sticky="w"
        )
        ttk.Checkbutton(frame, text="大文字/小文字を同一視", variable=ignore_case_var).grid(row=2, column=2, sticky="w")
        ttk.Checkbutton(frame, text="全角/半角を同一視", variable=ignore_width_var).grid(row=2, column=3, sticky="w")
        ttk.Checkbutton(frame, text="図形も検索(新形式のみ)", variable=shape_search_var).grid(
            row=2, column=4, sticky="w"
        )

        # 検索開始ボタンの作成
        ttk.Button(frame, text="検索開始", command=start_search).grid(row=2, column=5, pady=10, sticky="E")

        # 検索結果をCSVで保存するボタンの作成
        ttk.Button(frame, text="CSVで保存", command=save_csv_file).grid(row=2, column=6, pady=10, sticky="E")

        # 検索結果表示テーブルの作成
        columns: List[str] = ["ファイル名", "シート名", "アドレス", "種類", "内容", "パス"]
        result_table: ttk.Treeview = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            result_table.heading(col, text=col)
            if col == "ファイル名":
                result_table.column(col, width=200, stretch=False)
            elif col == "シート名":
                result_table.column(col, width=120, stretch=False)
            elif col == "アドレス":
                result_table.column(col, width=56, stretch=False)
            elif col == "種類":
                result_table.column(col, width=56, stretch=False)

        # ダブルクリックイベントをバインド
        result_table.bind("<Double-1>", open_excel_file)

        # 縦スクロールバーの作成
        scrollbar: ttk.Scrollbar = ttk.Scrollbar(frame, orient="vertical", command=result_table.yview)
        result_table.configure(yscroll=scrollbar.set)

        result_table.grid(row=4, column=0, columnspan=7, pady=5, sticky="nsew")
        scrollbar.grid(row=4, column=7, sticky="ns")

        # ステータスバーの作成
        status_bar: ttk.Label = ttk.Label(root, text="", relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")

        logger.debug("メインウィンドウを作成してイベントループを開始します。")

        # メインウィンドウのイベントループ
        root.mainloop()

    except Exception as e:
        msg: str = f"メインウィンドウの作成中にエラーが発生しました: {e}"
        logger.error(msg)
        messagebox.showerror("エラー", msg)
        root.destroy()
        return


# お約束の main() 関数
if __name__ == "__main__":
    main()
