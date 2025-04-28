import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional
from datetime import datetime, timedelta

def main() -> None:

    def add_timestamps(log_file: str, output_file: str) -> None:
        with open(log_file, 'r') as f:
            lines: list[str] = f.readlines()  # 型アノテーションを追加

        last_timestamp: Optional[str] = None
        with open(output_file, 'w') as out:
            for line in lines:
                # 空白行や空白文字のみの行をスキップ
                if line.strip() == "":
                    continue

                # 日時のパターンを正規表現でマッチ（行頭または行頭の空白の後）
                timestamp_match: Optional[re.Match] = re.match(r'^\s*(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})(?:\.\d+)?([+-]\d{2}:\d{2})?', line)

                if timestamp_match:
                    # yyyy-mm-dd hh:mm:ss 形式にフォーマット
                    date_part: str = timestamp_match.group(1)
                    time_part: str = timestamp_match.group(2)
                    offset_part: Optional[str] = timestamp_match.group(3)

                    # UTCのタイムスタンプを作成
                    utc_timestamp: datetime = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")

                    # 時差が指定されている場合、現地時間に変換
                    if offset_part:
                        offset_hours, offset_minutes = map(int, offset_part[1:].split(':'))
                        offset: timedelta = timedelta(hours=offset_hours, minutes=offset_minutes)
                        if offset_part.startswith('-'):
                            offset = -offset
                        local_timestamp: datetime = utc_timestamp + offset
                    else:
                        local_timestamp = utc_timestamp  # 時差がない場合はそのまま

                    # フォーマットしたタイムスタンプを作成
                    formatted_timestamp: str = local_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    last_timestamp = formatted_timestamp

                    # 行のタイムスタンプを置き換え
                    line = re.sub(r'^\s*(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})(?:\.\d+)?([+-]\d{2}:\d{2})?', formatted_timestamp, line)

                elif last_timestamp:
                    # タイムスタンプだけの行をスキップし、前のタイムスタンプと空白文字を挟んで連結
                    if re.match(r'^\s*(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})\s*$', line):
                        continue
                    else:
                        line = f"{last_timestamp} {line}"

                # 行を出力する際、タイムスタンプだけまたはタイムスタンプと空白文字だけの行は出力しない
                if not re.match(r'^\s*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})\s*$', line):
                    out.write(line)

    def select_log_file() -> None:
        log_file_path: str = filedialog.askopenfilename(title="アラートログファイルを選択", filetypes=[("Log files", "*.log"), ("All files", "*.*")])
        log_file_entry.delete(0, tk.END)  # エントリをクリア
        log_file_entry.insert(0, log_file_path)  # 選択したファイルのパスをエントリに表示

    def process_logs() -> None:
        log_file: str = log_file_entry.get()
        output_file: str = output_file_entry.get()

        if not log_file or not output_file:
            messagebox.showerror("エラー", "ファイルパスを入力してください。")
            return

        try:
            add_timestamps(log_file, output_file)
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

    # 処理ボタン
    ttk.Button(root, text="処理", command=process_logs).grid(row=2, column=1, pady=20)

    # GUIのメインループ
    root.mainloop()


# お約束の main() 関数
if __name__ == "__main__":
    main()

# EOF