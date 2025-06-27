"""
CSVファイルのフィールド値カウントツール

このスクリプトは、指定されたディレクトリ内のすべてのCSVファイルを解析し、
各フィールドに値が存在する行数をカウントします。

主な機能:
1. CSVファイルの検索とデータ解析
2. 各フィールドの値が存在する行数のカウント
3. データ行数の集計（ヘッダ行を除く）
4. フィールド数の整合性チェック（ヘッダ行と各データ行の比較）
5. 個別結果ファイルの出力（.txt形式）
6. 統合結果ファイルの出力（CSV形式）
7. エラーログの記録

処理の流れ:
1. カレントディレクトリ以下のCSVファイルを再帰的に検索
2. 各CSVファイルに対して以下の処理を実行:
   - フィールド数の整合性チェック
   - 各フィールドの値存在行数のカウント
   - データ行数の集計
   - 個別結果ファイルの生成
3. 全CSVファイルの結果を統合したファイルの生成

出力ファイル:
- 個別結果: [CSVファイル名].txt (各CSVファイルの解析結果)
- 統合結果: count_CSV_FieldValue.txt (全CSVファイルの統合結果)
- ログファイル: count_CSV_FieldValue.log (エラーログ)

Author: akira
Date: 2025年6月27日
"""

import csv
import os
import sys
from datetime import datetime
from typing import Dict, Tuple


def log_message(log_file: str, message: str, create_new: bool = False) -> None:
    """ログファイルにタイムスタンプ付きメッセージを書き込む

    Args:
        log_file (str): ログファイルのパス
        message (str): 書き込むメッセージ
        create_new (bool): 新規作成フラグ（True: 新規作成, False: 追記）

    Returns:
        None

    Raises:
        OSError: ログファイルの書き込み時にファイル操作エラーが発生した場合
        IOError: ログファイルの書き込み時にI/Oエラーが発生した場合
        Exception: その他の予期しないエラーが発生した場合

    Note:
        - メッセージは "YYYY-MM-DD HH:MM:SS - メッセージ" の形式で記録される
        - ファイルエンコーディングはcp932を使用
        - create_new=Trueの場合は新規作成、Falseの場合は追記
        - エラー発生時は標準エラー出力にエラーメッセージを出力
    """
    try:
        timestamp: str = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")
        mode: str = "w" if create_new else "a"
        with open(file=log_file, mode=mode, encoding="cp932") as log:
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

    CSVファイルを読み込み、各フィールドに値が存在する行の数をカウントします。
    ヘッダ行を除いたデータ行数も同時に取得します。
    また、各データ行のフィールド数がヘッダ行と異なる場合はエラーログを出力します。

    Args:
        file_path (str): 処理対象のCSVファイルのパス
        log_file (str): ログファイルのパス
        field_size_limit (int): CSVフィールドサイズの制限値（バイト）

    Returns:
        Tuple[Dict[str, int], list[str], bool, int]: 以下の要素を含むタプル
            - Dict[str, int]: 各フィールド名と値が存在する行数の辞書
            - list[str]: CSVファイルのフィールド名リスト（ヘッダ順）
            - bool: データが存在するかのフラグ（True: データあり, False: ヘッダのみ）
            - int: データ行数（ヘッダを除く総行数）

    Raises:
        FileNotFoundError: 指定されたCSVファイルが存在しない場合
        OSError: ファイルの読み込みやサイズ取得に失敗した場合
        csv.Error: CSV形式エラーが発生した場合
        Exception: その他の予期しないエラーが発生した場合

    Note:
        - ファイルエンコーディングはcp932を使用
        - 空のセルは値なしとして扱われる
        - データ行のフィールド数がヘッダ行と異なる場合、エラーログを出力
        - エラー発生時はログファイルに記録される
    """
    field_count: Dict[str, int] = {}
    fieldnames: list[str] = []
    has_data: bool = False
    data_row_count: int = 0  # データ行数（ヘッダを除く）

    # CSVファイルのサイズ制限を設定
    csv.field_size_limit(new_limit=field_size_limit)

    try:
        with open(file=file_path, mode="r", encoding="cp932") as csvfile:
            try:
                # ファイルサイズが0バイトかチェック（空ファイルの判定）
                if os.stat(path=file_path).st_size == 0:
                    log_message(log_file=log_file, message=f"{file_path}: 空ファイルです。")
                    return field_count, fieldnames, has_data, data_row_count
            except OSError as e:
                log_message(log_file=log_file, message=f"{file_path}: ファイル情報の取得に失敗しました: {e}")
                return field_count, fieldnames, has_data, data_row_count

            try:
                # 【フェーズ1】フィールド数の整合性チェック
                # まず、フィールド数チェック用にCSVファイルを読み込む
                csvfile.seek(0)  # ファイルの先頭に戻る
                raw_reader = csv.reader(csvfile)
                header_row: list[str] | None = next(raw_reader, None)
                expected_field_count: int = len(header_row) if header_row else 0

                # データ行のフィールド数をチェック
                row_index: int
                raw_row: list[str]
                for row_index, raw_row in enumerate(raw_reader, start=2):  # 2行目から開始（1行目はヘッダ）
                    actual_field_count: int = len(raw_row)
                    # ヘッダ行とデータ行のフィールド数が異なる場合はエラーログ出力
                    if actual_field_count != expected_field_count:
                        log_message(
                            log_file=log_file,
                            message=f"{file_path}: 行 {row_index} のフィールド数エラー - 期待値: {expected_field_count}, 実際: {actual_field_count}",
                        )

                # 【フェーズ2】データ処理とカウント
                # 次に、データ処理用にファイルを再読み込み
                csvfile.seek(0)  # ファイルの先頭に戻る
                reader: csv.DictReader[str] = csv.DictReader(f=csvfile)
                fieldnames = list(reader.fieldnames) if reader.fieldnames else []

                row: Dict[str, str]
                for row in reader:
                    data_row_count += 1  # 行数をカウント

                    # 行に何らかのデータが存在するかチェック
                    if any(row.values()):
                        has_data = True
                        # 各フィールドの値をチェックし、空でない場合はカウント
                        field: str
                        value: str
                        for field, value in row.items():
                            if value:  # 空文字列でない場合
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
    """カウント結果を個別のテキストファイルに書き込む

    CSVファイル毎にカウント結果をテキストファイルに出力します。
    ファイル名、データ行数、各フィールドのカウント結果が含まれます。

    Args:
        base_name (str): 出力ファイルのベース名（拡張子なし）
        counts (Dict[str, int]): 各フィールド名と値が存在する行数の辞書
        fieldnames (list[str]): CSVファイルのフィールド名リスト（ヘッダ順）
        csv_file_name (str): 処理対象のCSVファイル名
        has_data (bool): データが存在するかのフラグ
        data_row_count (int): データ行数（ヘッダを除く）
        log_file (str): ログファイルのパス

    Returns:
        None

    Raises:
        OSError: ファイル作成や書き込み時にファイル操作エラーが発生した場合
        IOError: ファイル書き込み時にI/Oエラーが発生した場合
        Exception: その他の予期しないエラーが発生した場合

    Note:
        - 出力ファイル名は "{base_name}.txt" 形式
        - ファイルエンコーディングはcp932を使用
        - フィールドはCSVのヘッダ順で出力される
        - エラー発生時はログファイルに記録される
    """
    output_file: str = f"{base_name}.txt"
    try:
        with open(file=output_file, mode="w", encoding="cp932") as f:
            # ファイルヘッダー情報の出力
            f.write(f"処理対象のCSVファイル: {csv_file_name}\n")
            f.write(f"データ行数: {data_row_count}\n\n")

            # データの有無によって出力内容を分岐
            if not has_data:
                f.write("データがありません（ヘッダ行のみまたは空ファイル）。\n")
            else:
                # 各フィールドのカウント結果をヘッダ順で出力
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
    """全てのカウント結果をまとめて1つのCSVファイルに書き込む

    複数のCSVファイルの処理結果を統合し、一つのCSVファイルに出力します。
    ヘッダ行を含む表形式で、各CSVファイルのフィールド毎の結果が記録されます。

    Args:
        summary_data (Dict[str, Dict[str, int]]): 各CSVファイルのカウント結果
            キー: CSVファイル名, 値: フィールド名とカウントの辞書
        fieldnames_data (Dict[str, list[str]]): 各CSVファイルのフィールド名リスト
            キー: CSVファイル名, 値: フィールド名のリスト（ヘッダ順）
        data_row_counts (Dict[str, int]): 各CSVファイルのデータ行数
            キー: CSVファイル名, 値: データ行数（ヘッダを除く）
        log_file (str): ログファイルのパス
        summary_file (str): まとめた結果を出力するファイル名

    Returns:
        None

    Raises:
        OSError: ファイル作成や書き込み時にファイル操作エラーが発生した場合
        IOError: ファイル書き込み時にI/Oエラーが発生した場合
        Exception: その他の予期しないエラーが発生した場合

    Note:
        - 出力形式: "CSVファイル名,データ総行数,項目名,項目の値の個数"
        - ファイルエンコーディングはcp932を使用
        - フィールドはCSVのヘッダ順で出力される
        - ヘッダ行が自動的に追加される
        - エラー発生時はログファイルに記録される
    """
    try:
        with open(file=summary_file, mode="w", encoding="cp932") as f:
            # CSVヘッダー行の出力
            f.write("CSVファイル名,CSVファイルデータ総行数,CSVファイルの項目名,CSVファイルの項目の値の個数\n")

            # 各CSVファイルの結果を統合して出力
            base_name: str
            counts: Dict[str, int]
            for base_name, counts in summary_data.items():
                fieldnames: list[str] = fieldnames_data.get(base_name, [])
                data_row_count: int = data_row_counts.get(base_name, 0)

                # 各フィールドの結果を1行ずつ出力
                field: str
                for field in fieldnames:
                    count: int = counts.get(field, 0)
                    f.write(f"{base_name},{data_row_count},{field},{count}\n")
    except (OSError, IOError) as e:
        log_message(log_file=log_file, message=f"{summary_file}: ファイル操作中にエラーが発生しました: {e}")
    except Exception as e:
        log_message(log_file=log_file, message=f"{summary_file}: 書き込み中にエラーが発生しました: {e}")


def main() -> None:
    """メイン処理を実行する

    カレントディレクトリとサブディレクトリからCSVファイルを検索し、
    各ファイルのフィールド値カウントを実行します。結果は個別ファイルと
    統合ファイルの両方に出力されます。

    Returns:
        None

    Raises:
        KeyboardInterrupt: ユーザーによる処理中断（Ctrl+C）
        Exception: その他の予期しないエラー

    Note:
        - 処理対象: カレントディレクトリ以下の全ての.csvファイル
        - 出力ファイル: 各CSVファイルに対応する.txtファイル + 統合.txtファイル
        - ログファイル: スクリプト名.log
        - フィールドサイズ制限: 500MB
        - エラー発生時は適切なログ記録と終了処理を実行
    """
    current_directory: str = os.getcwd()
    csv_files: list[str] = []
    log_file: str = os.path.splitext(p=os.path.basename(p=__file__))[0] + ".log"
    field_size_limit: int = 1024 * 1024 * 500  # 500MB

    # ログファイルを新規作成してプログラム開始ログを記録
    log_message(log_file=log_file, message="プログラム実行を開始しました。", create_new=True)

    # カレントディレクトリ以下のすべてのCSVファイルを検索
    dirpath: str
    filenames: list[str]
    filename: str
    for dirpath, _, filenames in os.walk(top=current_directory):
        for filename in filenames:
            if filename.endswith(".csv"):
                csv_files.append(os.path.join(dirpath, filename))

    # CSVファイルが見つからない場合は処理終了
    if not csv_files:
        log_message(log_file=log_file, message="処理対象のCSVファイルが見つかりません。")
        return

    log_message(log_file=log_file, message=f"処理対象のCSVファイル数: {len(csv_files)}")

    # 処理結果を保存するための辞書を初期化
    summary_data: Dict[str, Dict[str, int]] = {}  # 全てのカウント結果を保持する辞書
    fieldnames_data: Dict[str, list[str]] = {}  # 全てのフィールド名を保持する辞書
    data_row_counts: Dict[str, int] = {}  # 全てのデータ行数を保持する辞書
    summary_file: str = (
        os.path.splitext(os.path.basename(p=__file__))[0] + ".txt"
    )  # スクリプトのベース名に .txt を付けたファイル名

    # 各CSVファイルを順次処理
    csv_file: str
    for csv_file in csv_files:
        # CSVファイルの解析とカウント処理
        counts: Dict[str, int]
        fieldnames: list[str]
        has_data: bool
        data_row_count: int
        counts, fieldnames, has_data, data_row_count = count_values_in_csv(
            file_path=csv_file, log_file=log_file, field_size_limit=field_size_limit
        )

        # 個別結果ファイルの生成
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

        # 統合ファイル用にデータを蓄積
        csv_filename: str = os.path.basename(p=csv_file)
        summary_data[csv_filename] = counts
        fieldnames_data[csv_filename] = fieldnames
        data_row_counts[csv_filename] = data_row_count

    # 全CSVファイルの結果を統合したファイルを生成
    write_summary_to_file(
        summary_data=summary_data,
        fieldnames_data=fieldnames_data,
        data_row_counts=data_row_counts,
        log_file=log_file,
        summary_file=summary_file,
    )

    # プログラム終了ログを記録
    log_message(log_file=log_file, message="プログラム実行が正常に完了しました。")


if __name__ == "__main__":
    # プログラムのメイン実行部分
    # キーボード割り込み（Ctrl+C）やその他の例外をキャッチして適切に処理
    try:
        main()
    except KeyboardInterrupt:
        # ユーザーによる処理中断
        print("\n処理が中断されました。")
    except Exception as e:
        # 予期しないエラーが発生した場合
        print(f"予期しないエラーが発生しました: {e}")
        sys.exit(1)
