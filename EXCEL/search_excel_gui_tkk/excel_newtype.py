"""
-----------------------------------------------------------------------
excel_newtype.py
EXCEL 新形式 (.xlsx, .xlsm) ファイル用処理
-----------------------------------------------------------------------

python.exe -m pip install --upgrade pip
pip install --upgrade openpylx
pip install --upgrade pandas

"""

import os
from logging import Logger
from typing import Any, List, Tuple

import pandas as pd

from utility import normalize_string


# EXCEL 新形式 (.xlsx, .xlsm) ファイルをフルパスで受けて、そのファイル内を検索する
def search_in_excel_file_new_type(
    excel_file_path: str,
    search_term: str,
    case_sensitive: bool,
    width_sensitive: bool,
    shape_search: bool,
    progress_callback: Any,
    results: List[Tuple[str, str, str, str, str, str]],
    logger: Logger,
) -> None:
    """EXCEL 新形式 (.xlsx, .xlsm) ファイルをフルパスで受けて、そのファイル内を検索する

    Args:
        excel_file_path (str): 検索対象の EXCEL ファイル（新型式）
        search_term (str): 検索したい語句（正規化済）
        case_sensitive (bool): 大文字/小文字を同一視するか否か
        width_sensitive (bool): 全角/半角を同一視するか否か
        shape_search (bool): 図形内のテキストも検索するか否か（但し 新形式 .xlsx, .xlsm ファイルのみ）
        progress_callback (Any): 進捗を更新するためのコールバック関数
        results (List[Tuple[str, str, str, str, str, str]]): 検索結果を格納するリスト
        logger (Logger): logging.Logger
    """
    logger.debug("search_in_excel_file_new_type()")
    logger.debug(
        f" --> excel_file_path={excel_file_path}"
        f" search_term={search_term}"
        f" case_sensitive={case_sensitive}"
        f" width_sensitive={width_sensitive}"
        f" shape_search={shape_search}"
    )

    try:
        #
        # 対象ファイルの各シートの全てのセルを調べる
        #

        msg: str = "対象ファイルの各シートの全てのセルを調べる"
        logger.debug(msg)

        # EXCEL ファイルを開く
        # excel_file.close だけでEXCELファイルをオープンに関係するリソースの開放が不十分なため
        # with ブロックを使いブロックを抜けるとリソースを完全に開放するようにした。
        logger.debug(f"pd.ExcelFile({excel_file_path})")
        with pd.ExcelFile(excel_file_path) as excel_file:  # pandas で開く
            # シートごとに処理するループ
            for sheet_name in excel_file.sheet_names:
                # シート名を表示
                msg = f"ファイル: {os.path.basename(excel_file_path)} シート: {sheet_name}"
                logger.debug(msg)
                progress_callback(msg)
                # (pandas) シートから得たDataFrame内の全てのセルを検索
                df: pd.DataFrame = excel_file.parse(sheet_name)
                for row_index, row in df.iterrows():
                    for col_index, cell in enumerate(row):
                        # セルの値を取得
                        cell_value: str = str(cell) if pd.notna(cell) else ""
                        # セルが空なら loop continue
                        if len(cell_value) == 0:
                            continue
                        # セルの値を正規化
                        normalized_cell_value: str = normalize_string(
                            cell_value,
                            not case_sensitive,
                            not width_sensitive,
                            logger,
                        )
                        # 検索語が含まれる場合は結果に追加
                        if search_term in normalized_cell_value:
                            # 列番号を列文字に変換
                            col_letter: str = ""
                            temp_col_index: int = col_index
                            while temp_col_index >= 0:
                                col_letter = chr(65 + (temp_col_index % 26)) + col_letter
                                temp_col_index = temp_col_index // 26 - 1
                            # セルのアドレスを組み立て
                            cell_address: str = f"{col_letter}:{row_index + 2}"
                            # 結果リストに追加
                            # ここはセル検索のため "セル"
                            msg = f"{cell_address} : {normalized_cell_value} に {search_term} が含まれています。"
                            logger.debug(msg)
                            results.append(
                                (
                                    os.path.basename(excel_file_path),
                                    sheet_name,
                                    cell_address,
                                    "セル",
                                    cell_value,
                                    excel_file_path,
                                )
                            )

            excel_file.close
        # with ブロックを使い、ブロックを抜けるとリソースを完全に開放
    except Exception as e:
        msg = f"EXCEL 新形式 .xlsx, .xlsm ファイル grepエラー {os.path.basename(excel_file_path)}: {e}"
        logger.error(msg)

    #
    # shape_search != True ならば、ここで処理終了
    #
    if not shape_search:
        return

    msg = "対象ファイルの図形内のテキストを調べる"
    logger.debug(msg)

    #
    # shape_search = True ならば、対象ファイルの各シートの図形（Shape）を調べる
    #
    try:
        #
        # 対象ファイルの図形を全て調べる
        #
        # TODO 図形の検索処理を実装する。
        #
        # 参考 : https://learn.microsoft.com/ja-jp/dotnet/api/documentformat.openxml.drawing.spreadsheet?view=openxml-2.8.1
        # 参考 : https://lotus-base.com/blog/39/
        # 参考 : https://chrom-blog.com/how-to-get-image-placed-cell-address-xml/
        # 参考： https://zenn.dev/hodakam/articles/dc13ee7694ba08
        # 参考： https://gammasoft.jp/blog/how-to-extract-image-files-from-xlsx/
        #
        # file_path が対象ファイルのフルパス＋ファイル名
        # file_path を ZIP アーカイブファイルとしてオープンする。（拡張子制限あるか？）
        # /xl/workbook.xml にシートのリストが格納されている。 workbook > sheets > sheet がシート (※1)
        # シートのリストを得る。 name と r:id がシート名とリレーションシップID
        # /xl/_rels/workbook.xml.rels にシートのリレーションシップが格納されている。 relationships > relationship がリレーションシップ
        # シートのリレーションシップリストを得る。 id と target がリレーションシップIDとリレーションシップ先のファイル名。※1のr:id と一致する relationship を探して見つかった Target が sheet?.xml
        # /xl/worksheets/sheet?.xml に対応した /xl/worksheets/_rel/sheet?.xml.rels を参照して Relationships > Relationship の Target から図形の drawing?.xml を得る。
        # /xl/drawings/drawing?.xml に、シートごとの図形のファイルがある。ここまでの処理でシート名と drawing?.xml の対応リストが作成できる。
        #
        #   drawing?.xml のファイルリストを得る。
        #   シート（drawing?.xml）ごとにループ
        #       対象の drawing?.xml から図形のリストを得る。
        #       図形のリストをループ
        #           図形がテキストを持っているか？
        #               持っているならば、テキストを取得。（テキストは複数に分割されている可能性があるため結合する）
        #               図形のテキストを正規化
        #               図形のテキストに検索語が含まれる場合は、図形情報（図形の場所、図形の種類）も取得
        #               結果リストに追加
        #                   - ファイル名⇒ファイル名。
        #                   - シート名⇒シート名。
        #                   - 図形の場所⇒アドレス。図形のアドレスは包含矩形の対角線頂点のアドレスの組のため、図形の中心点のアドレスに変換する必要がある。
        #                   - 図形の種類⇒種類 "図形"。
        #                   - 図形のテキスト⇒内容。
        #                   - ファイルパス⇒パス。

        pass

    except Exception as e:
        msg = f"EXCEL 新形式 .xlsx, .xlsm ファイル grepエラー（図形） {os.path.basename(excel_file_path)}: {e}"
        logger.error(msg)

    return
