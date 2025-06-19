import csv
import os


def count_values_in_csv(file_path):
    """CSVファイル内の各フィールドの値を持つフィールドの個数をカウントする"""
    field_count = {}
    has_data = False  # データが存在するかのフラグ

    with open(file_path, mode="r", encoding="cp932") as csvfile:  # エンコーディングをcp932に設定
        reader = csv.DictReader(csvfile)
        for row in reader:
            if any(row.values()):  # 行に値がある場合
                has_data = True
                for field, value in row.items():
                    if value:  # 値を持つフィールドのみカウント
                        if field in field_count:
                            field_count[field] += 1
                        else:
                            field_count[field] = 1

    return field_count, has_data


def write_counts_to_file(base_name, counts, csv_file_name, has_data):
    """カウント結果をテキストファイルに書き込む"""
    output_file = f"{base_name}.txt"
    with open(output_file, mode="w", encoding="cp932") as f:  # 出力ファイルもcp932に設定
        f.write(f"処理対象のCSVファイル: {csv_file_name}\n\n")  # CSVファイル名を出力
        if not has_data:  # データが無い場合の出力
            f.write("データがありません（ヘッダ行のみ）。\n")
        for field, count in counts.items():
            f.write(f"{field}: {count}\n")


def main():
    # 現在のディレクトリとサブディレクトリを探す
    current_directory = os.getcwd()
    csv_files = []

    for dirpath, _, filenames in os.walk(current_directory):
        for filename in filenames:
            if filename.endswith(".csv"):
                csv_files.append(os.path.join(dirpath, filename))

    # 各CSVファイルを処理
    for csv_file in csv_files:
        counts, has_data = count_values_in_csv(csv_file)
        base_name = os.path.splitext(csv_file)[0]  # 拡張子を除いたファイル名
        write_counts_to_file(base_name, counts, os.path.basename(csv_file), has_data)  # ファイル名とデータフラグを渡す


if __name__ == "__main__":
    main()
