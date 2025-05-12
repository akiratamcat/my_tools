import re
import tkinter as tk
from datetime import datetime, timedelta  # timedelta を追加
from tkinter import filedialog, messagebox, ttk
from typing import Optional


def main() -> None:
    def add_timestamps(log_file: str, output_file: str, offset_hours: int) -> None:
        with open(log_file, "r") as f:
            lines: list[str] = f.readlines()  # 型アノテーションを追加

        last_timestamp: Optional[str] = None
        with open(output_file, "w") as out:
            for line in lines:
                # 空白行や空白文字のみの行をスキップ
                if line.strip() == "":
                    continue

                # 日時のパターンを正規表現でマッチ（行頭または行頭の空白の後）
                timestamp_match: Optional[re.Match] = re.match(
                    r"^\s*(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})(?:\.\d+)?([+-]\d{2}:\d{2})?", line
                )

                if timestamp_match:
                    # yyyy-mm-dd hh:mm:ss 形式にフォーマット
                    date_part: str = timestamp_match.group(1)
                    time_part: str = timestamp_match.group(2)

                    # タイムスタンプを作成
                    timestamp: datetime = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")
                    local_timestamp = timestamp + timedelta(hours=offset_hours)  # 時差補正を適用

                    # フォーマットしたタイムスタンプを作成
                    formatted_timestamp: str = local_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    last_timestamp = formatted_timestamp

                    # 行のタイムスタンプを置き換え
                    line = re.sub(
                        r"^\s*(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})(?:\.\d+)?([+-]\d{2}:\d{2})?",
                        formatted_timestamp,
                        line,
                    )

                elif last_timestamp:
                    # タイムスタンプだけの行をスキップし、前のタイムスタンプと空白文字を挟んで連結
                    if re.match(r"^\s*(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})\s*$", line):
                        continue
                    else:
                        line = f"{last_timestamp} {line}"

                # 行を出力する際、タイムスタンプだけまたはタイムスタンプと空白文字だけの行は出力しない
                if not re.match(r"^\s*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})\s*$", line):
                    out.write(line)

    def select_log_file() -> None:
        log_file_path: str = filedialog.askopenfilename(
            title="アラートログファイルを選択", filetypes=[("Log files", "*.log"), ("All files", "*.*")]
        )
        log_file_entry.delete(0, tk.END)  # エントリをクリア
        log_file_entry.insert(0, log_file_path)  # 選択したファイルのパスをエントリに表示

    def process_logs() -> None:
        log_file: str = log_file_entry.get()
        output_file: str = output_file_entry.get()
        offset_hours: str = offset_entry.get()

        if not log_file or not output_file:
            messagebox.showerror("エラー", "ファイルパスを入力してください。")
            return

        try:
            offset_hours_int = int(offset_hours)  # 時差補正を整数に変換
        except ValueError:
            messagebox.showerror("エラー", "時差補正には整数を入力してください。")
            return

        try:
            add_timestamps(log_file, output_file, offset_hours_int)
            messagebox.showinfo("成功", "タイムスタンプを付与したファイルが保存されました。")
        except Exception as e:
            messagebox.showerror("エラー", f"エラーが発生しました: {str(e)}")

    # GUIの設定
    root: tk.Tk = tk.Tk()
    root.title("Oracle アラートログ タイムスタンプ付与ツール")

    # アラートログファイルの選択
    ttk.Label(root, text="アラートログファイル:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    log_file_entry: ttk.Entry = ttk.Entry(root, width=50)
    log_file_entry.grid(row=0, column=1, padx=10, pady=10)
    ttk.Button(root, text="選択", command=select_log_file).grid(row=0, column=2, padx=10, pady=10)

    # 保存ファイル名の入力
    ttk.Label(root, text="保存ファイル名:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    output_file_entry: ttk.Entry = ttk.Entry(root, width=50)
    output_file_entry.grid(row=1, column=1, padx=10, pady=10)

    # 時差補正の入力
    ttk.Label(root, text="時差補正（時間）:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
    offset_entry: ttk.Entry = ttk.Entry(root, width=10)
    offset_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
    offset_entry.insert(0, "0")  # デフォルト値を 0 に設定

    # 処理ボタン
    ttk.Button(root, text="処理", command=process_logs).grid(row=3, column=1, pady=20)

    # GUIのメインループ
    root.mainloop()


# お約束の main() 関数
if __name__ == "__main__":
    main()

# EOF
