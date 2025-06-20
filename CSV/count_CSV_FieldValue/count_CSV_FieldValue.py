import csv
import os
from datetime import datetime


def log_message(log_file, message):
    """ログファイルにメッセージを書き込む"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 現在の日時を取得
    with open(log_file, mode="a", encoding="cp932") as log:
        log.write(f"{timestamp} - {message}\n")  # 日時をメッセージに追加


def count_values_in_csv(file_path, log_file, field_size_limit):
    """CSVファイル内の各フィールドの値を持つフィールドの個数をカウントする"""
    field_count = {}
    fieldnames = []  # フィールド名のリスト
    has_data = False  # データが存在するかのフラグ

    # フィールドサイズ制限を設定
    csv.field_size_limit(field_size_limit)

    try:
        with open(file_path, mode="r", encoding="cp932") as csvfile:  # エンコーディングをcp932に設定
            # ファイルが空かどうかをチェック
            if os.stat(file_path).st_size == 0:
                log_message(log_file, f"{file_path}: 空ファイルです。")
                return field_count, fieldnames, has_data  # 空ファイルの場合はそのまま返す

            try:
                reader = csv.DictReader(csvfile)
                fieldnames = reader.fieldnames  # フィールド名を取得
                for row in reader:
                    if any(row.values()):  # 行に値がある場合
                        has_data = True
                        for field, value in row.items():
                            if value:  # 値を持つフィールドのみカウント
                                if field in field_count:
                                    field_count[field] += 1
                                else:
                                    field_count[field] = 1
            except csv.Error as e:
                log_message(log_file, f"{file_path}: CSVファイルの読み込み中にエラーが発生しました: {e}")
                return field_count, fieldnames, has_data  # エラーが発生した場合はそのまま返す

    except FileNotFoundError:
        log_message(log_file, f"{file_path}: ファイルが見つかりません。")
    except Exception as e:
        log_message(log_file, f"{file_path}: エラーが発生しました: {e}")

    return field_count, fieldnames, has_data


def write_counts_to_file(base_name, counts, fieldnames, csv_file_name, has_data, log_file):
    """カウント結果をテキストファイルに書き込む"""
    output_file = f"{base_name}.txt"
    try:
        with open(output_file, mode="w", encoding="cp932") as f:  # 出力ファイルもcp932に設定
            f.write(f"処理対象のCSVファイル: {csv_file_name}\n\n")  # CSVファイル名を出力
            if not has_data:  # データが無い場合の出力
                f.write("データがありません（ヘッダ行のみまたは空ファイル）。\n")
            else:
                for field in fieldnames:  # フィールド名の順序で出力
                    count = counts.get(field, 0)  # カウントが無い場合は0を返す
                    f.write(f"{field}: {count}\n")
    except Exception as e:
        log_message(log_file, f"{output_file}: 書き込み中にエラーが発生しました: {e}")


def main():
    # 現在のディレクトリとサブディレクトリを探す
    current_directory = os.getcwd()
    csv_files = []

    # ログファイル名を取得
    log_file = os.path.splitext(os.path.basename(__file__))[0] + ".log"  # 現在のファイル名のベース名に .log を付ける

    # フィールドサイズの制限を設定
    field_size_limit = 1024 * 1024 * 500  # 500 MB

    for dirpath, _, filenames in os.walk(current_directory):
        for filename in filenames:
            if filename.endswith(".csv"):
                csv_files.append(os.path.join(dirpath, filename))

    # 各CSVファイルを処理
    for csv_file in csv_files:
        counts, fieldnames, has_data = count_values_in_csv(csv_file, log_file, field_size_limit)
        base_name = os.path.splitext(csv_file)[0]  # 拡張子を除いたファイル名
        write_counts_to_file(
            base_name, counts, fieldnames, os.path.basename(csv_file), has_data, log_file
        )  # ファイル名とデータフラグを渡す
        log_message(log_file, f"{csv_file}: 処理が完了しました。")


if __name__ == "__main__":
    main()
