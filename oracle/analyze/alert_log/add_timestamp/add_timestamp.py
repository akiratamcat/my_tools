import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def add_timestamps(log_file, output_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()

    last_timestamp = None
    with open(output_file, 'w') as out:
        for line in lines:
            # 日時のパターンを正規表現でマッチ（行頭または行頭の空白の後）
            timestamp_match = re.match(r'^\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if timestamp_match:
                last_timestamp = timestamp_match.group(1)
            elif last_timestamp:
                # 日時がない行に前の日時を付与
                line = f"{last_timestamp} {line}"

            out.write(line)

def select_log_file():
    log_file_path = filedialog.askopenfilename(title="アラートログファイルを選択", filetypes=[("Log files", "*.log"), ("All files", "*.*")])
    log_file_entry.delete(0, tk.END)  # エントリをクリア
    log_file_entry.insert(0, log_file_path)  # 選択したファイルのパスをエントリに表示

def process_logs():
    log_file = log_file_entry.get()
    output_file = output_file_entry.get()

    if not log_file or not output_file:
        messagebox.showerror("エラー", "ファイルパスを入力してください。")
        return

    try:
        add_timestamps(log_file, output_file)
        messagebox.showinfo("成功", "タイムスタンプを付与したファイルが保存されました。")
    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました: {str(e)}")

# GUIの設定
root = tk.Tk()
root.title("Oracle アラートログ タイムスタンプ付与ツール")

# アラートログファイルの選択
ttk.Label(root, text="アラートログファイル:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
log_file_entry = ttk.Entry(root, width=50)
log_file_entry.grid(row=0, column=1, padx=10, pady=10)
ttk.Button(root, text="選択", command=select_log_file).grid(row=0, column=2, padx=10, pady=10)

# 保存ファイル名の入力
ttk.Label(root, text="保存ファイル名:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
output_file_entry = ttk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=10, pady=10)

# 処理ボタン
ttk.Button(root, text="処理", command=process_logs).grid(row=2, column=1, pady=20)

# GUIのメインループ
root.mainloop()
