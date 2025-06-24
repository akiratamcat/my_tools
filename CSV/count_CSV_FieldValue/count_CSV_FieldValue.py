import csv
import os
import sys
from datetime import datetime
from typing import Dict, Tuple


def log_message(log_file: str, message: str) -> None:
    """ログファイルにメッセージを書き込む"""
    try:
        timestamp: str = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")
        with open(file=log_file, mode="a", encoding="cp932") as log:
            log.write(f"{timestamp} - {message}\n")
    except (OSError, IOError) as e:
        # ログファイルへの書き込みに失敗した場合、標準エラー出力に出力
        print(f"ログファイルへの書き込みエラー: {e}", file=sys.stderr)
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}", file=sys.stderr)


def count_values_in_csv(
    file_path: str, log_file: str, field_size_limit: int
) -> Tuple[Dict[str, int], list[str], bool, int]:
    """CSVファイル内の各フィールドの値を持つフィールドの個数をカウントする

    Args:
        file_path (str): CSVファイルのパス
        log_file (str): ログファイルのパス
        field_size_limit (int): フィールドサイズの制限

    Returns:        Tuple[Dict[str, int], list[str], bool, int]: フィールドのカウント、フィールド名のリスト、データが存在するかのフラグ、データ行数
    """
    field_count: Dict[str, int] = {}
    fieldnames: list[str] = []
    has_data: bool = False
    data_row_count: int = 0  # データ行数（ヘッダを除く）
    csv.field_size_limit(new_limit=field_size_limit)
    try:
        with open(file=file_path, mode="r", encoding="cp932") as csvfile:
            try:
                if os.stat(path=file_path).st_size == 0:
                    log_message(log_file=log_file, message=f"{file_path}: 空ファイルです。")
                    return field_count, fieldnames, has_data, data_row_count
            except OSError as e:
                log_message(log_file=log_file, message=f"{file_path}: ファイル情報の取得に失敗しました: {e}")
                return field_count, fieldnames, has_data, data_row_count

            try:
                reader: csv.DictReader[str] = csv.DictReader(f=csvfile)
                fieldnames = list(reader.fieldnames) if reader.fieldnames else []
                for row in reader:
                    data_row_count += 1  # 行数をカウント
                    if any(row.values()):
                        has_data = True
                        for field, value in row.items():
                            if value:
                                if field in field_count:
                                    field_count[field] += 1
                                else:
                                    field_count[field] = 1
            except csv.Error as e:
                log_message(
                    log_file=log_file, message=f"{file_path}: CSVファイルの読み込み中にエラーが発生しました: {e}"
                )
                return field_count, fieldnames, has_data, data_row_count

    except FileNotFoundError:
        log_message(log_file=log_file, message=f"{file_path}: ファイルが見つかりません。")
    except Exception as e:
        log_message(log_file=log_file, message=f"{file_path}: エラーが発生しました: {e}")

    return field_count, fieldnames, has_data, data_row_count


def write_counts_to_file(
    base_name: str,
    counts: Dict[str, int],
    fieldnames: list[str],
    csv_file_name: str,
    has_data: bool,
    data_row_count: int,
    log_file: str,
) -> None:
    """カウント結果をテキストファイルに書き込む

    Args:
        base_name (str): 出力ファイルのベース名
        counts (Dict[str, int]): 各フィールドのカウント
        fieldnames (list): フィールド名のリスト
        csv_file_name (str): 処理対象のCSVファイル名
        has_data (bool): データが存在するかのフラグ
        data_row_count (int): データ行数（ヘッダを除く）        log_file (str): ログファイルのパス
    """
    output_file: str = f"{base_name}.txt"
    try:
        with open(file=output_file, mode="w", encoding="cp932") as f:
            f.write(f"処理対象のCSVファイル: {csv_file_name}\n")
            f.write(f"データ行数: {data_row_count}\n\n")
            if not has_data:
                f.write("データがありません（ヘッダ行のみまたは空ファイル）。\n")
            else:
                for field in fieldnames:
                    count: int = counts.get(field, 0)
                    f.write(f"{field}: {count}\n")
    except (OSError, IOError) as e:
        log_message(log_file=log_file, message=f"{output_file}: ファイル操作中にエラーが発生しました: {e}")
    except Exception as e:
        log_message(log_file=log_file, message=f"{output_file}: 書き込み中にエラーが発生しました: {e}")


def write_summary_to_file(
    summary_data: Dict[str, Dict[str, int]],
    fieldnames_data: Dict[str, list[str]],
    data_row_counts: Dict[str, int],
    log_file: str,
    summary_file: str,
) -> None:
    """全てのカウント結果をまとめて1つのファイルに書き込む

    Args:
        summary_data (Dict[str, Dict[str, int]]): 各CSVファイルのカウント結果
        fieldnames_data (Dict[str, list[str]]): 各CSVファイルのフィールド名リスト
        data_row_counts (Dict[str, int]): 各CSVファイルのデータ行数
        log_file (str): ログファイルのパス        summary_file (str): まとめた結果を出力するファイル名
    """
    try:
        with open(file=summary_file, mode="w", encoding="cp932") as f:
            for base_name, counts in summary_data.items():
                fieldnames: list[str] = fieldnames_data.get(base_name, [])
                data_row_count: int = data_row_counts.get(base_name, 0)
                for field in fieldnames:
                    count = counts.get(field, 0)
                    f.write(f"{base_name},{data_row_count},{field},{count}\n")
    except (OSError, IOError) as e:
        log_message(log_file=log_file, message=f"{summary_file}: ファイル操作中にエラーが発生しました: {e}")
    except Exception as e:
        log_message(log_file=log_file, message=f"{summary_file}: 書き込み中にエラーが発生しました: {e}")


def main() -> None:
    """メイン処理を実行する"""
    current_directory: str = os.getcwd()
    csv_files: list[str] = []
    log_file: str = os.path.splitext(p=os.path.basename(p=__file__))[0] + ".log"
    field_size_limit: int = 1024 * 1024 * 500  # 500MB

    for dirpath, _, filenames in os.walk(top=current_directory):
        for filename in filenames:
            if filename.endswith(".csv"):
                csv_files.append(os.path.join(dirpath, filename))

    if not csv_files:
        log_message(log_file=log_file, message="処理対象のCSVファイルが見つかりません。")
        return

    summary_data: Dict[str, Dict[str, int]] = {}  # 全てのカウント結果を保持する辞書
    fieldnames_data: Dict[str, list[str]] = {}  # 全てのフィールド名を保持する辞書
    data_row_counts: Dict[str, int] = {}  # 全てのデータ行数を保持する辞書
    summary_file: str = (
        os.path.splitext(os.path.basename(p=__file__))[0] + ".txt"
    )  # スクリプトのベース名に .txt を付けたファイル名

    for csv_file in csv_files:
        counts, fieldnames, has_data, data_row_count = count_values_in_csv(
            file_path=csv_file, log_file=log_file, field_size_limit=field_size_limit
        )
        base_name: str = os.path.splitext(p=csv_file)[0]  # 拡張子を除いたファイル名
        write_counts_to_file(
            base_name=base_name,
            counts=counts,
            fieldnames=fieldnames,
            csv_file_name=os.path.basename(p=csv_file),
            has_data=has_data,
            data_row_count=data_row_count,
            log_file=log_file,
        )
        log_message(log_file=log_file, message=f"{csv_file}: 処理が完了しました。")

        # カウント結果とフィールド名をまとめる
        csv_filename = os.path.basename(p=csv_file)
        summary_data[csv_filename] = counts
        fieldnames_data[csv_filename] = fieldnames
        data_row_counts[csv_filename] = data_row_count

    # まとめた結果を1つのファイルに書き込む
    write_summary_to_file(
        summary_data=summary_data,
        fieldnames_data=fieldnames_data,
        data_row_counts=data_row_counts,
        log_file=log_file,
        summary_file=summary_file,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n処理が中断されました。")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        sys.exit(1)
